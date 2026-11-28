"""Compare vendor_parts.py builders with the vendor's own CAD: aligned volume IoU and surface-to-surface distance (issue #260).

    python desktop-lpbf/cad/oem/compare_cad.py PATH/TO/vendor_parts.py TAG [key ...]

PATH is the vendor_parts.py to test, so the committed copy and a working copy can be compared ("before" / "after").
Vendor files are read from $VCAD (default /tmp/agentE/vcad); they are never committed (cad/oem/cad-manifest.csv has
their URLs and sha256). Vendor meshes are cached in $MESH_CACHE (default /tmp/agentE/mesh).

Method, per builder:
1. Tessellate both shapes (OCC BRepMesh, linear tolerance 0.1 % of the largest extent, at least 0.02 mm), merge vertices,
   and make each solid a manifold3d Manifold; the vendor's solids are unioned.
2. Align the vendor mesh to ours: the 24 proper axis rotations about matched bounding-box centres, each scored by exact
   mesh-boolean IoU; the best is refined by ICP (trimesh.registration.icp on 4000 surface samples, rigid, no scale) and
   the ICP result is kept only if it raises the IoU.
3. IoU = vol(A n B) / vol(A u B) from manifold3d booleans. Distances: 20 000 area-weighted surface samples on each mesh,
   exact point-to-surface distance to the other mesh (vtkImplicitPolyDataDistance through pyvista); mean, RMS, P95 and
   max each way, and the symmetric figures (mean of both means, larger P95, Hausdorff).
Run under the memory cap: OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python ... (the Teknic STEP is 64 MB).
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE.parent.parent / "analysis" / "out" / "oem"
VCAD = pathlib.Path(os.environ.get("VCAD", "/tmp/agentE/vcad"))
CACHE = pathlib.Path(os.environ.get("MESH_CACHE", "/tmp/agentE/mesh"))

# builder key -> (how to call it, vendor file name in VCAD, vendor part number)
CASES = {
    "clearpath_sd_231x": ("clearpath_sd_231x()", "CPM-231x-Q.STEP", "Teknic CPM-SDSK-231x (-Q STEP)"),
    "mcm_6627T91": ("mcm_6627T91()", "6627T91.STEP", "McMaster 6627T91"),
    "mcm_6709K12": ("mcm_6709K12()", "6709K12.STEP", "McMaster 6709K12"),
    "mcm_4566N401": ("mcm_4566N401()", "4566N401.STEP", "McMaster 4566N401"),
    "mcm_5786N23": ("kf_weld_stub(25)", "5786N23.STEP", "McMaster 5786N23"),
    "mcm_5786N25": ("kf_weld_stub(40)", "5786N25.STEP", "McMaster 5786N25"),
    "mcm_4518K72": ("kf_wing_clamp(25)", "4518K72.STEP", "McMaster 4518K72"),
    "mcm_4518K73": ("kf_wing_clamp(40)", "4518K73.STEP", "McMaster 4518K73"),
    "mcm_4123K45": ("mcm_4123K45('-x')", "4123K45.STEP", "McMaster 4123K45"),
    "mcm_3861N11": ("mcm_3861N11()", "3861N11.STEP", "McMaster 3861N11 (coiled lead dropped)"),
    "mcm_5169K72": ("mcm_5169K72()", "5169K72.STEP", "McMaster 5169K72"),
}


def load_vp(path):
    path = pathlib.Path(path).resolve()
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("vp_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tess_solid(solid, tol):
    import trimesh
    vs, ts = solid.tessellate(tol, 0.2)
    v = np.array([(p.x, p.y, p.z) for p in vs], dtype=np.float64)
    t = np.array(ts, dtype=np.int64)
    m = trimesh.Trimesh(v, t, process=True)
    m.merge_vertices()
    if m.volume < 0:
        m.invert()
    return m


def to_manifold(tm):
    import manifold3d as mf
    mesh = mf.Mesh(vert_properties=np.asarray(tm.vertices, dtype=np.float32), tri_verts=np.asarray(tm.faces, dtype=np.uint32))
    M = mf.Manifold(mesh)
    if M.status() != mf.Error.NoError or M.is_empty():
        raise ValueError(f"not manifold: {M.status()}")
    return M


def shape_to_manifold(shape, tol):
    """Union of the shape's solids as one Manifold, and the trimesh of that union."""
    import manifold3d as mf
    import trimesh
    sols = shape.Solids() if hasattr(shape, "Solids") else [shape]
    ms, bad = [], 0
    for s in sols:
        tm = tess_solid(s, tol)
        try:
            ms.append(to_manifold(tm))
        except ValueError:
            trimesh.repair.fill_holes(tm)
            trimesh.repair.fix_normals(tm)
            try:
                ms.append(to_manifold(tm))
            except ValueError:
                bad += 1
    if not ms:
        raise ValueError("no manifold solid")
    U = mf.Manifold.batch_boolean(ms, mf.OpType.Add) if len(ms) > 1 else ms[0]
    return U, bad, len(sols)


def man_to_tm(M):
    import trimesh
    m = M.to_mesh()
    return trimesh.Trimesh(np.asarray(m.vert_properties)[:, :3], np.asarray(m.tri_verts), process=False)


def rotations24():
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            R = np.zeros((3, 3))
            for i, (j, s) in enumerate(zip(perm, signs)):
                R[i, j] = s
            if np.linalg.det(R) > 0:
                out.append(R)
    return out


def xform(M, T):
    return M.transform(np.asarray(T[:3, :4], dtype=np.float64))


def iou(A, B):
    inter = (A ^ B).volume()
    va, vb = A.volume(), B.volume()
    return inter / (va + vb - inter), inter


def bbox_centre(M):
    b = M.bounding_box()
    return (np.array(b[:3]) + np.array(b[3:])) / 2


def surf_dist(src_tm, dst_tm, n=20000, seed=1):
    import pyvista as pv
    import trimesh
    pts, _ = trimesh.sample.sample_surface(src_tm, n, seed=seed)
    faces = np.hstack([np.full((len(dst_tm.faces), 1), 3), dst_tm.faces]).ravel()
    surf = pv.PolyData(np.asarray(dst_tm.vertices), faces)
    d = np.abs(pv.PolyData(pts).compute_implicit_distance(surf)["implicit_distance"])
    return dict(mean=round(float(d.mean()), 3), rms=round(float(np.sqrt((d ** 2).mean())), 3), p95=round(float(np.percentile(d, 95)), 3), max=round(float(d.max()), 3))


def vendor_manifold(key, fname, tol):
    p = VCAD / fname
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    c = CACHE / f"{key}_{h}_{tol:.3f}.npz"
    import manifold3d as mf
    hits = sorted(CACHE.glob(f"{key}_{h}_*.npz"))          # reuse any cached tessellation of the same file
    if hits:
        c = hits[0]
    if c.exists():
        z = np.load(c)
        info = json.loads(str(z["info"]))
        return mf.Manifold(mf.Mesh(vert_properties=z["v"], tri_verts=z["t"])), info
    import cadquery as cq
    t0 = time.time()
    vals = cq.importers.importStep(str(p)).vals()
    shape = vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)
    sols = list(shape.Solids())
    note = ""
    if key == "mcm_3861N11" and os.environ.get("LEAD_RULE", "r6") == "r5":   # round 5: drop the lead solid only
        sols.sort(key=lambda q: -max(q.BoundingBox().xlen, q.BoundingBox().ylen, q.BoundingBox().zlen))
        sols = sols[1:]
        note = "coiled lead solid dropped"
    elif key == "mcm_3861N11":         # round 6: drop the lead AND its 7 stripped wire ends (every solid beyond the gland,
        sols = [q for q in sols if max(abs(q.BoundingBox().ymin), abs(q.BoundingBox().ymax)) <= 34.0]   # |y| > 34 mm)
        note = "lead and its stripped wire ends dropped (solids beyond the gland, |y| > 34 mm); round 5 kept the wire ends"
    U, bad, n = shape_to_manifold(cq.Compound.makeCompound(sols), tol)
    info = dict(solids=n, non_manifold_solids_dropped=bad, note=note, load_s=round(time.time() - t0, 1), sha256_16=h)
    m = U.to_mesh()
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez(c, v=np.asarray(m.vert_properties, dtype=np.float32), t=np.asarray(m.tri_verts, dtype=np.uint32), info=json.dumps(info))
    return U, info


def compare(vp, key):
    import cadquery as cq  # noqa: F401
    import trimesh
    call, fname, pn = CASES[key]
    ours = eval("vp." + call)
    bb = ours.BoundingBox()
    tol = max(0.02, 0.001 * max(bb.xlen, bb.ylen, bb.zlen))
    A, badA, nA = shape_to_manifold(ours, tol)
    B, info = vendor_manifold(key, fname, tol)
    ca = bbox_centre(A)
    cb = bbox_centre(B)
    best = (-1, None, None)
    for i, R in enumerate(rotations24()):
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, 3] = ca - R @ cb
        val, _ = iou(A, xform(B, T))
        if val > best[0]:
            best = (val, T, i)
    iou0, T0, rot = best
    # ICP refinement (vendor samples -> our surface)
    tmA = man_to_tm(A)
    tmB = man_to_tm(xform(B, T0))
    pts, _ = trimesh.sample.sample_surface(tmB, 4000, seed=2)
    icp_used = False
    try:
        Ticp, _, cost = trimesh.registration.icp(pts, tmA, initial=np.eye(4), threshold=1e-6, max_iterations=40, reflection=False, scale=False)
        val, _ = iou(A, xform(B, Ticp @ T0))
        if val > iou0 + 1e-4:
            iou0, T0, icp_used = val, Ticp @ T0, True
    except Exception as e:  # noqa: BLE001
        print(key, "icp failed", e)
    Bt = xform(B, T0)
    val, inter = iou(A, Bt)
    tmB = man_to_tm(Bt)
    d_ov = surf_dist(tmA, tmB)
    d_vo = surf_dist(tmB, tmA)
    ea = sorted(np.round(np.array(A.bounding_box()[3:]) - np.array(A.bounding_box()[:3]), 2).tolist())
    eb = sorted(np.round(np.array(B.bounding_box()[3:]) - np.array(B.bounding_box()[:3]), 2).tolist())
    return dict(key=key, vendor_part=pn, call=call, tess_tol_mm=round(tol, 3), iou=round(val, 4), iou_method="manifold3d mesh booleans",
                ours_mm3=round(A.volume(), 1), vendor_mm3=round(B.volume(), 1), inter_mm3=round(inter, 1),
                dvol_pct=round(100 * (A.volume() - B.volume()) / B.volume(), 1), ours_ext=ea, vendor_ext=eb,
                dext_max_mm=round(max(abs(a - b) for a, b in zip(ea, eb)), 2),
                rotation_index=rot, icp_kept=icp_used, transform=np.round(T0, 4).tolist(),
                ours_to_vendor=d_ov, vendor_to_ours=d_vo,
                sym_mean_mm=round((d_ov["mean"] + d_vo["mean"]) / 2, 3), sym_p95_mm=max(d_ov["p95"], d_vo["p95"]), hausdorff_mm=max(d_ov["max"], d_vo["max"]),
                vendor_info=info, ours_solids=nA, ours_nonmanifold_dropped=badA)


def main():
    vp = load_vp(sys.argv[1])
    tag = sys.argv[2]
    keys = sys.argv[3:] or list(CASES)
    OUTD.mkdir(parents=True, exist_ok=True)
    jf = OUTD / f"cad_compare_{tag}.json"
    res = {r["key"]: r for r in (json.loads(jf.read_text()) if jf.exists() else [])}
    for k in keys:
        if not (VCAD / CASES[k][1]).exists():
            print(k, "vendor file missing", flush=True)
            continue
        t0 = time.time()
        try:
            r = compare(vp, k)
        except Exception as e:  # noqa: BLE001
            r = dict(key=k, error=f"{type(e).__name__}: {e}")
        r["wall_s"] = round(time.time() - t0, 1)
        res = {q["key"]: q for q in (json.loads(jf.read_text()) if jf.exists() else [])}   # re-read: parallel runs share the file
        res[k] = r
        print(json.dumps({q: r.get(q) for q in ("key", "iou", "dvol_pct", "sym_mean_mm", "sym_p95_mm", "hausdorff_mm", "icp_kept", "wall_s", "error")}), flush=True)
        jf.write_text(json.dumps([res[q] for q in CASES if q in res], indent=1))
    res = {q["key"]: q for q in (json.loads(jf.read_text()) if jf.exists() else [])}
    lines = [f"# Vendor CAD vs vendor_parts.py builders ({tag})", "",
             "Aligned volume IoU (manifold3d booleans) and surface-to-surface distance (20k samples each way). Made by cad/oem/compare_cad.py.", "",
             "| Builder | Vendor CAD | IoU | Δ volume | mean dist (mm) | P95 (mm) | max (mm) | extents ours / vendor (mm) |", "|---|---|---|---|---|---|---|---|"]
    for q in CASES:
        r = res.get(q)
        if not r:
            continue
        if "error" in r:
            lines.append(f"| `{q}` | {CASES[q][2]} | error: {r['error'][:60]} | | | | | |")
            continue
        lines.append(f"| `{r['call']}` | {r['vendor_part']} | {r['iou']:.3f} | {r['dvol_pct']:+.1f} % | {r['sym_mean_mm']:.2f} | {r['sym_p95_mm']:.2f} | {r['hausdorff_mm']:.2f} | {r['ours_ext']} / {r['vendor_ext']} |")
    (OUTD / f"cad_compare_{tag}.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
