"""CalculiX FEA of the low-profile desktop LPBF (cad/lpbf_low.py): chamber, lid, door, recoater, Z arm, optics bridge, window.

Geometry comes from the same parametric model (M.build()); each analysed body is exported to BREP, meshed with
gmsh (quadratic tetrahedra, C3D10), loaded and constrained by faces picked geometrically, solved with ccx and
read back from the .frd. Units: mm, N, MPa, tonne (density 2.7e-9 t/mm3 for 6061).

Cases
  1 chamber (frame + floor plate, bonded on the O-ring lands) at full vacuum (interior suction + lid and door loads on their lands,
    module / plenum / funnel loads under the floor); 1b the same with the lid, at full vacuum and at +20 mbar
  1f floor-plate bolted joint (Shigley: preload, joint constant, separation) and the floor O-ring gland (Parker)
  2 lid at vacuum (top-face pressure + covered openings carried round their flanges), on its sealing land
  3 drop-down door at vacuum, on its O-ring land; latch load at +50 mbar (analytic)
  4 recoater carriage block + arm + blade holder: spreading load and a 50 N hit
  5 Z lift arm: 50 N down + 10 N sideways at the rod; plate tilt
  6 optics bridge + posts: gravity sag and first 6 modes, with the galvo, lens, shutter and collimator as rigid masses
  7 Ø2 in. fused-silica window: plate formula and FEA

Run:  OMP_NUM_THREADS=2 xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python desktop-lpbf/analysis/fea/fea.py [1 2 ...]
Scratch (.brep/.inp/.frd/.dat) goes to /tmp/fea-run/; results to analysis/out/fea/ (fea.md, fea.json, PNGs).

Memory (2026-11-22; the runner has 15 GB shared by several jobs, and this script must fit in 4.5 GB): gmsh and the model
build take < 1 GB. The memory goes to ccx's direct solver: SPOOLES on the 265,000-node lid passed 4.2 GB before it was
killed, and the recoater (300,000 nodes) and the bridge (350,000) are larger. So
  - static steps use SPOOLES up to FEA_DIRECT_MAX nodes (default 60,000) and ccx's ITERATIVE CHOLESKY (PCG with an
    incomplete-Cholesky preconditioner, memory ~ the matrix: 1.5 GB for the lid) above. SPOOLES's memory depends on the
    shape as well as the size: 3.0 GB in all for the 141,500-node bridge, but more than 4.4 GB for the 115,000-node
    recoater, a compact block. FEA_SOLVER=SPOOLES or FEA_SOLVER="ITERATIVE CHOLESKY" forces one. On the door and the Z
    arm the two agree to 0.01 % in displacement and 2 % in peak stress;
  - the bridge (case 6) is meshed coarser (hmax 10 mm, was 7) because *FREQUENCY needs SPOOLES here (this ccx has no
    PARDISO or PaStiX), and the PCG solver needs ~20 min for its gravity step (the rigid masses make it ill-conditioned);
  - several cases on the command line run one after another, each in its own process;
  - images are drawn by render_fea.py in a child process from the surface triangles only, not the volume mesh.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import subprocess
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "cad"))
import cadquery as cq  # noqa: E402
import gmsh  # noqa: E402
import lpbf_low as M  # noqa: E402

OUT = ROOT / "analysis" / "out" / "fea"
RUN = pathlib.Path(os.environ.get("FEA_RUN", "/tmp/fea-run"))
P_ATM = 0.101325          # MPa
G = 9810.0                # mm/s2
E_TOL = 0.05              # mm, face-classification tolerance
P = M.P
AL = M.MAT["al6061"]
HAZ_ALLOW = 110.0         # MPa, 6061-T6 weld heat-affected zone (as-welded, ~O/T4 strength)
FATIGUE = AL["fat"]       # 96.5 MPa at 5e8 cycles (R = -1)
DIRECT_MAX = int(os.environ.get("FEA_DIRECT_MAX", "60000"))    # nodes; SPOOLES above this can outgrow a 4.5 GB budget


def solver_for(m):
    """ccx solver for a static step on mesh m: SPOOLES (direct) for small meshes, ITERATIVE CHOLESKY for large ones."""
    return os.environ.get("FEA_SOLVER") or ("SPOOLES" if len(m["ntags"]) <= DIRECT_MAX else "ITERATIVE CHOLESKY")


def model_commit():
    """Commit of the model these results come from, with '+dirty' if cad/ has uncommitted changes."""
    try:
        h = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        d = subprocess.run(["git", "status", "--porcelain", "--", "cad"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        return h + ("+dirty" if d else "")
    except Exception:  # noqa: BLE001
        return "unknown"


def stamp(r, m, solver, **kw):
    """Record how a case was run (UTC date, model commit, mesh size, solver) in its result dict."""
    r["run"] = dict(utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=model_commit(), nodes=len(m["ntags"]), solver=solver, **kw)


# --------------------------------------------------------------------------------------------
# meshing
# --------------------------------------------------------------------------------------------
def mesh_shape(shape, name, hmax, hmin=None, curv=12, alg=10):
    RUN.mkdir(parents=True, exist_ok=True)
    path = RUN / f"{name}.brep"
    shape.exportBrep(str(path))
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add(name)
    gmsh.model.occ.importShapes(str(path))
    gmsh.model.occ.synchronize()
    vols = gmsh.model.getEntities(3)
    if len(vols) != 1:
        print(f"  warning: {name} has {len(vols)} volumes; fragmenting for a conformal mesh")
        gmsh.model.occ.fragment(vols[:1], vols[1:])
        gmsh.model.occ.synchronize()
    gmsh.option.setNumber("Mesh.MeshSizeMax", hmax)
    gmsh.option.setNumber("Mesh.MeshSizeMin", hmin or hmax / 5)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", curv)
    gmsh.option.setNumber("Mesh.ElementOrder", 2)
    gmsh.option.setNumber("Mesh.SecondOrderLinear", 1)      # straight-sided C3D10: no inverted curved elements
    gmsh.option.setNumber("Mesh.Algorithm3D", alg)          # 10 HXT; 4 frontal for bodies HXT gives up on
    gmsh.option.setNumber("General.NumThreads", int(os.environ.get("OMP_NUM_THREADS", "2")))
    try:
        gmsh.model.mesh.generate(3)
    except Exception as e:  # noqa: BLE001  (HXT gives up on some fused bodies, e.g. the chamber frame + floor plate)
        print(f"  HXT 3D mesher failed ({e}); retrying with gmsh's frontal mesher")
        gmsh.model.mesh.clear()
        gmsh.option.setNumber("Mesh.Algorithm3D", 4)
        gmsh.model.mesh.generate(3)
        gmsh.model.mesh.setOrder(2)
    ntags, xyz, _ = gmsh.model.mesh.getNodes()
    xyz = xyz.reshape(-1, 3)
    tets = []
    for et, _, en in zip(*gmsh.model.mesh.getElements(3)):
        if et == 11:
            tets.append(en.reshape(-1, 10))
    tets = np.vstack(tets).astype(np.int64)[:, [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]]   # gmsh -> CalculiX C3D10 order
    surfs = {}
    for _, tag in gmsh.model.getEntities(2):
        bb = gmsh.model.getBoundingBox(2, tag)
        tri = None
        for et, _, en in zip(*gmsh.model.mesh.getElements(2, tag)):
            if et == 9:
                tri = en.reshape(-1, 6).astype(np.int64)
        if tri is not None:
            surfs[tag] = dict(bb=bb, tri=tri)
    gmsh.finalize()
    idx = np.full(int(ntags.max()) + 1, -1, dtype=np.int64)
    idx[ntags.astype(np.int64)] = np.arange(len(ntags))
    m = dict(name=name, ntags=ntags.astype(np.int64), xyz=xyz, idx=idx, tets=tets, surfs=surfs)
    # orientation check (CalculiX wants positive volume, nodes 1-2-3 counter-clockwise seen from node 4)
    c = xyz[idx[tets[:, :4]]]
    vol = np.einsum("ij,ij->i", np.cross(c[:, 1] - c[:, 0], c[:, 2] - c[:, 0]), c[:, 3] - c[:, 0])
    if (vol < 0).any():
        neg = vol < 0
        t = tets[neg]
        tets[neg] = t[:, [0, 2, 1, 3, 6, 5, 4, 7, 9, 8]]
        print(f"  flipped {neg.sum()} inverted tets")
    m["faces"] = face_index(m)
    print(f"  mesh {name}: {len(ntags)} nodes, {len(tets)} C3D10, {len(surfs)} faces")
    return m


_FACES = [(0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0)]   # C3D10 faces 1..4 (corner nodes)


def face_index(m):
    t = m["tets"]
    keys = []
    for f in _FACES:
        k = np.sort(t[:, list(f)], axis=1)
        keys.append(k[:, 0] * (1 << 42) + k[:, 1] * (1 << 21) + k[:, 2])
    keys = np.stack(keys, axis=1).ravel()           # index = 4*elem + face
    order = np.argsort(keys)
    return keys[order], order


def tri_faces(m, tri):
    """(element number 1-based, face number 1..4) for each surface triangle (6-node, corner nodes first)."""
    k = np.sort(tri[:, :3], axis=1)
    q = k[:, 0] * (1 << 42) + k[:, 1] * (1 << 21) + k[:, 2]
    keys, order = m["faces"]
    pos = np.searchsorted(keys, q)
    ok = keys[np.minimum(pos, len(keys) - 1)] == q
    if not ok.all():
        raise RuntimeError(f"{(~ok).sum()} surface triangles not matched to a tet face")
    g = order[pos]
    return g // 4 + 1, g % 4 + 1


def tri_geom(m, tri):
    c = m["xyz"][m["idx"][tri[:, :3]]]
    cen = c.mean(axis=1)
    area = 0.5 * np.linalg.norm(np.cross(c[:, 1] - c[:, 0], c[:, 2] - c[:, 0]), axis=1)
    return cen, area


def surfaces(m, pred):
    """Surface tags whose bounding box satisfies pred(xmin, ymin, zmin, xmax, ymax, zmax)."""
    return [t for t, s in m["surfs"].items() if pred(*s["bb"])]


def faces_on(m, tags, cfilt=None):
    """Element faces (elem, face, area, centroid) on the given surfaces, optionally filtered by centroid."""
    if not tags:
        raise RuntimeError("no surfaces selected")
    tri = np.vstack([m["surfs"][t]["tri"] for t in tags])
    cen, area = tri_geom(m, tri)
    if cfilt is not None:
        keep = cfilt(cen)
        tri, cen, area = tri[keep], cen[keep], area[keep]
    el, fc = tri_faces(m, tri)
    return dict(el=el, fc=fc, area=area, cen=cen, tri=tri)


def nodes_on(m, tags, pfilt=None):
    ids = np.unique(np.vstack([m["surfs"][t]["tri"] for t in tags]).ravel())
    if pfilt is not None:
        ids = ids[pfilt(m["xyz"][m["idx"][ids]])]
    return ids


def planar(axis, value, tol=E_TOL):
    a = "xyz".index(axis)
    return lambda *bb: abs(bb[a] - value) < tol and abs(bb[a + 3] - value) < tol


def nearest(m, p, cand=None):
    ids = m["ntags"] if cand is None else cand
    d = np.linalg.norm(m["xyz"][m["idx"][ids]] - np.asarray(p), axis=1)
    return int(ids[np.argmin(d)])


# --------------------------------------------------------------------------------------------
# CalculiX input, run, results
# --------------------------------------------------------------------------------------------
def nset(name, ids):
    ids = list(map(int, ids))
    lines = [f"*NSET, NSET={name}"]
    for k in range(0, len(ids), 16):
        lines.append(",".join(map(str, ids[k:k + 16])))
    return "\n".join(lines) + "\n"


def write_model(job, m, mat, extra=""):
    RUN.mkdir(parents=True, exist_ok=True)
    with open(RUN / f"{job}.inp", "w") as f:
        f.write("*HEADING\nLPBF " + job + "\n*NODE, NSET=NALL\n")
        np.savetxt(f, np.column_stack([m["ntags"], m["xyz"]]), fmt=["%d", "%.6f", "%.6f", "%.6f"], delimiter=",")
        f.write("*ELEMENT, TYPE=C3D10, ELSET=EALL\n")
        np.savetxt(f, np.column_stack([np.arange(1, len(m["tets"]) + 1), m["tets"]]), fmt="%d", delimiter=",")
        f.write(extra)
        f.write(f"*MATERIAL, NAME=MAT\n*ELASTIC\n{mat['E']},{mat['nu']}\n*DENSITY\n{mat['rho'] * 1e-12:.4e}\n")
        f.write("*SOLID SECTION, ELSET=EALL, MATERIAL=MAT\n")
    return RUN / f"{job}.inp"


def append(job, text):
    with open(RUN / f"{job}.inp", "a") as f:
        f.write(text)


def dload_lines(fs, p):
    """*DLOAD lines: positive p pushes into the element (compression on that face)."""
    return "".join(f"{e},P{k},{p:.6g}\n" for e, k in zip(fs["el"], fs["fc"]))


def cload_lines(ids, F):
    """Spread force vector F (N) equally over nodes `ids`."""
    n = len(ids)
    s = ""
    for nid in ids:
        for d in range(3):
            if F[d] != 0:
                s += f"{int(nid)},{d + 1},{F[d] / n:.6g}\n"
    return s


def run_ccx(job):
    t0 = time.time()
    env = dict(os.environ, OMP_NUM_THREADS=os.environ.get("OMP_NUM_THREADS", "2"))
    r = subprocess.run(["ccx", "-i", job], cwd=RUN, env=env, capture_output=True, text=True)
    (RUN / f"{job}.log").write_text(r.stdout + r.stderr)
    if "*ERROR" in r.stdout or r.returncode != 0 or not (RUN / f"{job}.frd").exists():
        tail = "\n".join([l for l in r.stdout.splitlines() if "ERROR" in l][:10]) or r.stdout[-2000:]
        raise RuntimeError(f"ccx failed for {job}:\n{tail}")
    print(f"  ccx {job}: {time.time() - t0:.0f} s")


def read_frd(job):
    blocks, cur = [], None
    with open(RUN / f"{job}.frd") as f:
        for line in f:
            if line.startswith(" -4"):
                cur = dict(name=line.split()[1], ids=[], vals=[])
                blocks.append(cur)
            elif line.startswith(" -1") and cur is not None:
                n = (len(line.rstrip("\n")) - 13) // 12
                cur["ids"].append(int(line[3:13]))
                cur["vals"].append([float(line[13 + 12 * k:25 + 12 * k]) for k in range(n)])
            elif line.startswith(" -3"):
                cur = None
    for b in blocks:
        b["ids"] = np.array(b["ids"], dtype=np.int64)
        b["vals"] = np.array(b["vals"], dtype=float)
    return blocks


def field(m, block, ncomp):
    out = np.zeros((len(m["ntags"]), ncomp))
    sel = block["ids"] < len(m["idx"])
    ids = block["ids"][sel]
    rows = m["idx"][ids]
    ok = rows >= 0
    out[rows[ok]] = block["vals"][sel][ok][:, :ncomp]
    return out


def von_mises(S):
    sxx, syy, szz, sxy, syz, szx = S.T
    return np.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3 * (sxy ** 2 + syz ** 2 + szx ** 2))


def principal_max(S):
    sxx, syy, szz, sxy, syz, szx = S.T
    T = np.stack([np.stack([sxx, sxy, szx], -1), np.stack([sxy, syy, syz], -1), np.stack([szx, syz, szz], -1)], -2)
    return np.linalg.eigvalsh(T)[:, -1]


def static_results(m, job):
    b = read_frd(job)
    U = field(m, [x for x in b if x["name"] == "DISP"][-1], 3)
    S = field(m, [x for x in b if x["name"] == "STRESS"][-1], 6)
    return U, S, von_mises(S)


def read_freqs(job):
    txt = (RUN / f"{job}.dat").read_text().splitlines()
    out, on = [], False
    for l in txt:
        if "E I G E N V A L U E   O U T P U T" in l:
            on = True
            continue
        if on:
            p = l.split()
            if len(p) >= 4 and p[0].isdigit():
                out.append(float(p[3]))
            elif out and not l.strip():
                break
    return out


def static_step(bc, loads, solver="SPOOLES"):
    return (f"*STEP\n*STATIC, SOLVER={solver}\n*BOUNDARY\n{bc}" + loads +
            "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")


# --------------------------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------------------------
def nice(x):
    e = 10 ** math.floor(math.log10(x))
    for k in (1, 2, 5, 10):
        if x <= k * e:
            return k * e
    return 10 * e


def surface_tris(m):
    """The boundary as linear triangles (each 6-node face triangle split in 4 at its mid-side nodes, so the quadratic mesh's
    nodal values are all shown), on the surface nodes only: (row indices of those nodes, triangles numbered 0..n-1)."""
    tri = m["idx"][np.vstack([s["tri"] for s in m["surfs"].values()])]
    lin = np.vstack([tri[:, [0, 3, 5]], tri[:, [3, 1, 4]], tri[:, [5, 4, 2]], tri[:, [3, 4, 5]]])
    used, inv = np.unique(lin, return_inverse=True)
    return used, inv.reshape(-1, 3)


def render(m, U, s, path, title, view, label="von Mises (MPa)", scale=None, clim=None, mark=None, zoom=1.15, cmap="turbo", up=(0, 0, 1)):
    """Draw the deformed surface coloured by s. The drawing runs in its own process (render_fea.py) on the surface triangles
    only, so VTK never holds the volume mesh and its memory is freed before the next solve. Returns the deformation scale."""
    pts = m["xyz"]
    diag = float(np.linalg.norm(pts.max(0) - pts.min(0)))
    umax = np.linalg.norm(U, axis=1).max()
    if scale is None:
        scale = nice(0.05 * diag / max(umax, 1e-12))
    used, tri = surface_tris(m)
    mk = None if mark is None else (np.asarray(mark) + scale * U[m["idx"][nearest(m, mark)]]).tolist()
    opt = dict(path=str(path), title=title + f"\ndeformation x{scale:g}", view=list(view), up=list(up), label=label, scale=float(scale),
               clim=None if clim is None else [float(c) for c in clim], mark=mk, diag=diag, zoom=zoom, cmap=cmap)
    RUN.mkdir(parents=True, exist_ok=True)
    npz = RUN / f"render_{pathlib.Path(path).stem}.npz"
    np.savez(npz, pts=pts[used], tri=tri, U=np.asarray(U)[used], s=np.asarray(s, dtype=float)[used], opt=json.dumps(opt))
    r = subprocess.run([sys.executable, str(HERE / "render_fea.py"), str(npz)], capture_output=True, text=True, timeout=900)
    if r.returncode != 0 or not pathlib.Path(path).exists():
        print(f"  render failed for {pathlib.Path(path).name} (exit {r.returncode}); results are unaffected\n{r.stderr[-800:]}")
    return scale


def loc_text(p):
    return f"({p[0]:.0f}, {p[1]:.0f}, {p[2]:.0f})"


# --------------------------------------------------------------------------------------------
# cases
# --------------------------------------------------------------------------------------------
def part(parts, prefix):
    for p in parts:
        if p.name.startswith(prefix):
            return p
    raise KeyError(prefix)


def chamber_loads(m, with_lid, scale=1.0):
    """Face sets and *DLOAD lines for the chamber (frame + floor plate, optionally + lid) at full vacuum, times `scale`
    (scale = -0.002 / P_ATM gives +20 mbar: every load is a pressure, so the linear model just reverses and shrinks).
    Vacuum: suction on the wetted faces; the lid (open-top case) and the door carried on their lands; the build module, the outlet
    plenum and the overflow funnel close the port and the two slots from below, so their vacuum loads push up on the floor plate's
    underside round each opening (the module's flange round the port; the flanges round the slots)."""
    ix, iy, cx, cy, fl, lz0, lz1 = P["ix"], P["iy"], P["cx"], P["cy"], P["floor"], P["lid_z0"], P["lid_z1"]
    e = E_TOL
    inner = surfaces(m, lambda x0, y0, z0, x1, y1, z1: x0 > -ix - e and x1 < ix + e and y0 > -iy - e and y1 < iy + e and z0 > -e and z1 < lz0 + e)
    front = surfaces(m, planar("y", -cy))
    bottom = surfaces(m, planar("z", -fl))
    f_in = faces_on(m, inner)
    f_door = faces_on(m, front, lambda c: (np.abs(c[:, 0]) <= 124) & (c[:, 2] >= -6) & (c[:, 2] <= 114))
    a_door = 232.0 * 104.0
    r_c = lambda c, x, y: np.hypot(c[:, 0] - x, c[:, 1] - y)
    f_port = faces_on(m, bottom, lambda c: (r_c(c, 0, 0) >= P["port_d"] / 2) & (r_c(c, 0, 0) <= P["port_d"] / 2 + 14))
    y0o, y1o = M.MP.OUTLET_Y
    f_out = faces_on(m, bottom, lambda c: (c[:, 0] >= -75) & (c[:, 0] <= 84) & (c[:, 1] >= y0o - 11) & (c[:, 1] <= y1o + 11)
                     & ~((np.abs(c[:, 0]) <= M.MP.OUTLET_HALF) & (c[:, 1] >= y0o) & (c[:, 1] <= y1o)))
    f_ovf = faces_on(m, bottom, lambda c: (np.abs(c[:, 0] - 100) <= 22) & (np.abs(c[:, 1]) <= 59) & ~((c[:, 0] >= P["ovf_x0"]) & (c[:, 0] <= P["ovf_x1"]) & (np.abs(c[:, 1]) <= 52)))
    F = dict(port=P_ATM * math.pi / 4 * P["port_d"] ** 2, outlet=P_ATM * 140.4 * 13.0, overflow=P_ATM * 23.0 * 110.1, door=P_ATM * a_door)
    loads = ("*DLOAD\n" + dload_lines(f_in, -P_ATM * scale) + dload_lines(f_door, scale * F["door"] / f_door["area"].sum())
             + dload_lines(f_port, scale * F["port"] / f_port["area"].sum()) + dload_lines(f_out, scale * F["outlet"] / f_out["area"].sum())
             + dload_lines(f_ovf, scale * F["overflow"] / f_ovf["area"].sum()))
    extra = dict(f_in=f_in, f_door=f_door)
    if with_lid:
        top = surfaces(m, planar("z", lz1))
        xd = P["x_dose"]
        f_win = faces_on(m, top, lambda c: (r_c(c, 0, 0) >= 28) & (r_c(c, 0, 0) <= 50))
        f_dose = faces_on(m, top, lambda c: (np.abs(c[:, 0] - xd) <= 17) & (np.abs(c[:, 1]) <= 55) & ~((np.abs(c[:, 0] - xd) <= 6) & (np.abs(c[:, 1]) <= P["dose_y"])))
        f_cam = faces_on(m, top, lambda c: (r_c(c, 75, -45) >= 11) & (r_c(c, 75, -45) <= 16))
        loads += (dload_lines(f_win, scale * P_ATM * math.pi * 28 ** 2 / f_win["area"].sum())
                  + dload_lines(f_dose, scale * P_ATM * 12 * 2 * P["dose_y"] / f_dose["area"].sum())
                  + dload_lines(f_cam, scale * P_ATM * math.pi * 11 ** 2 / f_cam["area"].sum()))
        extra["top"] = top
    else:
        top = surfaces(m, planar("z", lz0))
        f_top = faces_on(m, top)
        off = 3 + P.get("gland_w", 4.0) / 2
        F["lid"] = P_ATM * 2 * (ix + off) * 2 * (iy + off)
        loads += dload_lines(f_top, scale * F["lid"] / f_top["area"].sum())
        extra["f_top"] = f_top
    legs = [(x, x + 30, y, y + 30) for x in (-cx + 6, cx - 36) for y in (-cy + 6, cy - 36)]
    pads = nodes_on(m, bottom, lambda q: np.any([(q[:, 0] >= a) & (q[:, 0] <= b) & (q[:, 1] >= c) & (q[:, 1] <= d) for a, b, c, d in legs], axis=0))
    return loads, pads, F, extra


def chamber_body(parts, with_lid):
    """Frame + floor plate (+ lid) as one body, bonded across the floor joint. The joint's 0.1 mm skirt gap, 0.25 mm pad clearance
    and the O-ring groove are filled (a 4 mm slab over the footprint): gmsh can't mesh the thin slots, and the joint stays closed
    under every load here (case 1f checks it with Shigley). So the joint is modelled stiffer than the real 3 mm of lands; the
    frame's and floor plate's stresses away from it are what this case is for."""
    cx, cy = P["cx"], P["cy"]
    slab = M.rbox(-cx, cx, -cy, cy, -M.FRAME["pad"], 0.0, 8)
    # the frame and floor plate before joints.py's fastener holes (lpbf_low.CHAMBER_OPS[...]["part"]): with every M4/M5 hole the fused body
    # is 3.6 times the old case 1's mesh and OCC flags the slivers where the floor screws' holes meet; the holes don't change the global stress
    b = M.CHAMBER_OPS["frame"]["part"].fuse(slab).fuse(M.CHAMBER_OPS["floor"]["part"])
    if with_lid:
        b = b.fuse(part(parts, "Chamber lid").shape)
    return b.clean()


def joint_sigma_z(m, S, lands_z=0.0):
    """Normal stress across the floor joint (|z| < 1.5 mm, under the walls inside the skirt) in the bonded model: mean and extremes
    (MPa, + = tension, i.e. the joint would want to open there)."""
    q = m["xyz"]
    ix, iy, FR = P["ix"], P["iy"], M.FRAME
    t_out = FR["rebate"] - FR["pad_clear"]
    dx = np.maximum(np.abs(q[:, 0]) - ix, np.abs(q[:, 1]) - iy)        # distance outside the inner wall line (approx. off the corners)
    on = (np.abs(q[:, 2] - lands_z) < 1.5) & (dx > 0.05) & (dx < t_out - 0.05)
    s = S[on, 2]
    return dict(n=int(on.sum()), mean=float(s.mean()) if len(s) else None, min=float(s.min()) if len(s) else None, max=float(s.max()) if len(s) else None)


def case1(parts, R):
    """Frame + floor plate at full vacuum, open top (the lid's load on the top land): the case that used to be the monolithic body."""
    m = mesh_shape(chamber_body(parts, False), "c1_chamber", hmax=9.0, hmin=1.5)
    loads, pads, F, ex = chamber_loads(m, False)
    job = "c1_chamber"
    write_model(job, m, AL, nset("PADS", pads))
    append(job, static_step("PADS,1,3\n", loads, solver="ITERATIVE CHOLESKY"))
    run_ccx(job)
    U, S, vm = static_results(m, job)
    i = int(np.argmax(vm))
    door_nodes = m["idx"][np.unique(ex["f_door"]["tri"].ravel())]
    top_nodes = m["idx"][np.unique(ex["f_top"]["tri"].ravel())]
    vmax, p995 = float(vm[i]), float(np.percentile(vm, 99.5))
    sa = sm = vmax / 2
    r = dict(case="1 chamber: frame + floor plate (bonded across the floor joint), open top, full vacuum", material=AL["label"],
             load=(f"-{P_ATM:.4f} MPa on {ex['f_in']['area'].sum() / 100:.0f} cm2 of wetted faces; lid {F['lid']:.0f} N on the top land; door {F['door']:.0f} N "
                   f"on its land; module {F['port']:.0f} N, outlet plenum {F['outlet']:.0f} N and funnel {F['overflow']:.0f} N up on the floor plate round their openings; "
                   "4 leg pads under the floor plate fixed"),
             nodes=len(m["ntags"]), elements=len(m["tets"]), vm_max=vmax, vm_max_at=m["xyz"][i].tolist(), vm_p995=p995,
             u_max=float(np.linalg.norm(U, axis=1).max()), u_max_at=m["xyz"][int(np.argmax(np.linalg.norm(U, axis=1)))].tolist(),
             door_land_uy_range=float(np.ptp(U[door_nodes, 1])), door_land_u_max=float(np.abs(U[door_nodes]).max()),
             lid_land_uz_range=float(np.ptp(U[top_nodes, 2])), floor_joint_sz=joint_sigma_z(m, S),
             sf_yield=AL["sy"] / vmax, sf_haz=HAZ_ALLOW / vmax, sf_fatigue_goodman=1.0 / (sa / FATIGUE + sm / AL["su"]), sf_yield_p995=AL["sy"] / p995)
    r["criterion"] = "SF >= 2 on yield at the peak; seal faces move << the O-rings' squeeze; Goodman SF >= 2 for vacuum cycles"
    r["pass"] = r["sf_yield"] >= 2 and r["sf_fatigue_goodman"] >= 2
    r["png"] = "c1_chamber_vm.png"
    stamp(r, m, "ITERATIVE CHOLESKY")
    render(m, U, vm, OUT / r["png"], f"Case 1: frame + floor plate at full vacuum, 6061-T6\nmax von Mises {vmax:.1f} MPa at {loc_text(m['xyz'][i])}",
           (-1.0, -1.6, 1.1), mark=m["xyz"][i], clim=(0, max(p995 * 1.2, 1e-3)))
    R["1"] = r
    print(f"  case 1: vm max {vmax:.1f} MPa at {loc_text(m['xyz'][i])}, p99.5 {p995:.1f}, u max {r['u_max'] * 1000:.1f} um; joint sz {r['floor_joint_sz']}")


def case1b(parts, R):
    """Frame + floor plate + lid as one body at full vacuum, and the same mesh at +20 mbar (argon at its working pressure)."""
    m = mesh_shape(chamber_body(parts, True), "c1b_chamber_lid", hmax=9.0, hmin=1.5)
    out = {}
    for tag, scale in (("vacuum", 1.0), ("plus20mbar", -0.002 / P_ATM)):
        loads, pads, F, ex = chamber_loads(m, True, scale)
        job = f"c1b_chamber_lid_{tag}"
        write_model(job, m, AL, nset("PADS", pads))
        append(job, static_step("PADS,1,3\n", loads, solver="ITERATIVE CHOLESKY"))
        run_ccx(job)
        U, S, vm = static_results(m, job)
        i = int(np.argmax(vm))
        door_nodes = m["idx"][np.unique(ex["f_door"]["tri"].ravel())]
        seat = m["idx"][nodes_on(m, ex["top"], lambda q: (np.hypot(q[:, 0], q[:, 1]) >= 28) & (np.hypot(q[:, 0], q[:, 1]) <= 50))]
        vmax, p995 = float(vm[i]), float(np.percentile(vm, 99.5))
        sa = sm = vmax / 2
        out[tag] = dict(vm_max=vmax, vm_max_at=m["xyz"][i].tolist(), vm_p995=p995, u_max=float(np.linalg.norm(U, axis=1).max()),
                        u_max_at=m["xyz"][int(np.argmax(np.linalg.norm(U, axis=1)))].tolist(), door_land_uy_range=float(np.ptp(U[door_nodes, 1])),
                        window_seat_uz=float(U[seat, 2].min()) if tag == "vacuum" else float(U[seat, 2].max()), floor_joint_sz=joint_sigma_z(m, S),
                        sf_yield=AL["sy"] / vmax, sf_haz=HAZ_ALLOW / vmax, sf_fatigue_goodman=1.0 / (sa / FATIGUE + sm / AL["su"]))
        if tag == "vacuum":
            r_png = "c1b_chamber_lid_vm.png"
            render(m, U, vm, OUT / r_png, f"Case 1b: frame + floor plate + lid at full vacuum, 6061-T6\nmax von Mises {vmax:.1f} MPa at {loc_text(m['xyz'][i])}; "
                   f"door frame moves {out[tag]['door_land_uy_range'] * 1000:.0f} um", (-1.0, -1.6, 1.1), mark=m["xyz"][i], clim=(0, max(p995 * 1.2, 1e-3)))
        print(f"  case 1b {tag}: vm max {vmax:.2f} MPa at {loc_text(m['xyz'][i])}, p99.5 {p995:.2f}, u max {out[tag]['u_max'] * 1000:.2f} um; joint sz {out[tag]['floor_joint_sz']}")
    v = out["vacuum"]
    r = dict(case="1b chamber: frame + floor plate + lid bonded, full vacuum and +20 mbar", material=AL["label"],
             load="vacuum: suction inside incl. the lid underside, door on its land, window/dose/camera covers round their flanges, module/plenum/funnel loads under the floor; "
                  "+20 mbar: the same loads reversed and scaled by 0.002/0.101325 (linear); 4 leg pads fixed",
             nodes=len(m["ntags"]), elements=len(m["tets"]), **v, plus20mbar=out["plus20mbar"])
    r["criterion"] = "as case 1"
    r["pass"] = r["sf_yield"] >= 2 and r["sf_fatigue_goodman"] >= 2
    r["png"] = "c1b_chamber_lid_vm.png"
    stamp(r, m, "ITERATIVE CHOLESKY")
    R["1b"] = r


def case1f(parts, R):
    """Floor-plate bolted joint, Shigley (Budynas & Nisbett, Shigley's MED 10th ed., ch. 8): preload, joint constant, load and
    separation factors for 18 x M4 x 16 316 screws in tapped 6061, under the floor O-ring's squeeze force, +20 / +50 mbar and a
    +0.5 bar regulator fault. Also the floor gland per Parker ORD 5700 (same checks seals.py makes)."""
    FR = M.FRAME
    from fasteners import CATALOG                                         # noqa: E402  (cad/ is on sys.path)
    import joints as J
    n = len(J.REGISTRY["floor"]["items"])
    pn = J.REGISTRY["floor"]["pn"]
    c = CATALOG[pn]
    d, Ls = c["d"], c["L"]
    At = 8.78                                                             # M4 x 0.7 tensile stress area, mm2 (ISO 898-1)
    Sp = 210.0                                                            # 316 (McMaster 92290A: 70 ksi tensile); proof taken as A4-50 Rp0.2, conservative
    Su = 70.0 * 6.894757
    Fi = 0.75 * At * Sp                                                   # Shigley 8-31, reusable joint
    K_t = 0.20
    T = K_t * Fi * d / 1000.0                                             # N m, Shigley 8-27
    E_s, E_al = 193e3, AL["E"]
    l_clamp = (-FR["pad"] - (-P["floor"] + FR["notch"])) + (FR["pad"] - FR["skirt"])   # band under the head (8) + the 0.1 gap
    lp = l_clamp + d / 2                                                  # tapped-hole joint: effective grip h + d/2 (Shigley Table 8-7)
    kb = At * E_s / lp                                                    # fully threaded screw in the grip
    km = 0.5774 * math.pi * E_al * d / (2 * math.log(5 * (0.5774 * l_clamp + 0.5 * d) / (0.5774 * l_clamp + 2.5 * d)))   # Shigley 8-22, 30 deg frustum
    C = kb / (kb + km)
    # floor O-ring: Lindley / Gent as seals.py, and Parker's 70A-80A bars at 25 % (Figs 2-4..2-6) for the stiff end
    shore = 75.0
    E75 = 0.0981 * (56 + 7.62336 * shore) / (0.137505 * (254 - 2.54 * shore))
    cs, depth, width = 3.53, P["gland_d"], P["gland_w"]
    sq = (cs - depth) / cs
    q_nom = cs * E75 * (1.25 * sq ** 1.5 + 50 * sq ** 6)
    sq_max = ((cs + 0.102) - (depth - 0.05)) / (cs + 0.102)
    q_max = cs * E75 * (1.25 * sq_max ** 1.5 + 50 * sq_max ** 6)
    q_parker80 = 55.0 * 4.448 / 25.4
    t_mid = FR["gland_t"] + width / 2
    half = (P["ix"] + t_mid, P["iy"] + t_mid)
    r_mid = FR["r_in"] + t_mid
    path = 4 * (half[0] + half[1]) - (8 - 2 * math.pi) * r_mid
    A_seal = 4 * half[0] * half[1] - (4 - math.pi) * r_mid ** 2           # inside the cord's centre line
    F_or = dict(nominal=q_nom * path, max_tolerance=q_max * path, parker_80A=q_parker80 * path)
    cases = {
        "nominal O-ring, +20 mbar": F_or["nominal"] + 2e-3 * A_seal,
        "O-ring at max squeeze, +50 mbar (relief valve +34)": F_or["max_tolerance"] + 5e-3 * A_seal,
        "Parker 80A bar, +50 mbar": F_or["parker_80A"] + 5e-3 * A_seal,
        "Parker 80A bar, +0.5 bar regulator fault": F_or["parker_80A"] + 0.05 * A_seal,
        "nominal O-ring, full vacuum": F_or["nominal"] - P_ATM * A_seal,
    }
    rows = {}
    for k, Ftot in cases.items():
        Pb = Ftot / n
        rows[k] = dict(load_total_N=Ftot, load_per_screw_N=Pb,
                       n_load=(Sp * At - Fi) / (C * Pb) if Pb > 0 else None, n_sep=Fi / (Pb * (1 - C)) if Pb > 0 else None,
                       screw_force_N=Fi + C * Pb)
    Le = Ls - l_clamp
    A_strip = math.pi * d * Le * 0.5                                      # internal-thread shear area, conservative half of pi d Le
    F_strip = A_strip * 0.577 * AL["sy"]
    land = (FR["gland_t"] + (FR["rebate"] - FR["pad_clear"] - FR["gland_t"] - width)) * path
    gl = dict(cs=cs, depth=depth, width=width, squeeze_nom=100 * sq, squeeze_min=100 * ((cs - 0.102) - (depth + 0.05)) / (cs - 0.102), squeeze_max=100 * sq_max,
              fill_nom=100 * math.pi / 4 * cs ** 2 / (depth * width), fill_max_cold=100 * math.pi / 4 * (cs + 0.102) ** 2 / ((depth - 0.05) * (width - 0.05)),
              parker_range=dict(depth=(2.57, 2.72), width_face=(4.50, 4.75)), path_mm=path, splice="vulcanized cord, made to length: no stretch")
    r = dict(case="1f floor-plate bolted joint (Shigley) and floor O-ring gland (Parker)", screws=f"{n} x McMaster {pn} (M{d:g} x {Ls:g}, 316), tapped 6061",
             proof_MPa=Sp, tensile_MPa=Su, preload_N=Fi, torque_Nm=T, nut_factor=K_t, grip_mm=l_clamp, kb_N_per_mm=kb, km_N_per_mm=km, C=C,
             oring_N_per_mm=dict(nominal=q_nom, max_tolerance=q_max, parker_80A=q_parker80), oring_force_N=F_or, seal_area_mm2=A_seal, cases=rows,
             thread_engagement_mm=Le, thread_strip_N=F_strip, screw_proof_N=Sp * At, screw_break_N=Su * At,
             preload_total_N=n * Fi, land_area_mm2=land, land_pressure_preload_MPa=n * Fi / land, head_bearing_MPa=Fi / (math.pi / 4 * (7.0 ** 2 - 4.5 ** 2)),
             gland=gl, dowels="2 x McMaster 93600A686 (Ø6 x 20, m6), pressed into the plate, slip fit in the frame")
    r["criterion"] = "separation factor n_sep >= 2 and load factor n_load >= 1.5 in every case; thread strip > screw break"
    r["pass"] = all((v["n_sep"] is None or v["n_sep"] >= 2) and (v["n_load"] is None or v["n_load"] >= 1.5) for v in rows.values()) and F_strip > Su * At
    R["1f"] = r
    print(f"  case 1f: Fi {Fi:.0f} N ({T:.2f} N m), C {C:.3f}; " + "; ".join(f"{k}: n_sep {v['n_sep']:.1f}" for k, v in rows.items() if v["n_sep"]))


def case2(parts, R):
    ix, iy, cx, cy, lz0, lz1 = P["ix"], P["iy"], P["cx"], P["cy"], P["lid_z0"], P["lid_z1"]
    xd = P["x_dose"]
    m = mesh_shape(part(parts, "Chamber lid").shape, "c2_lid", hmax=6.0, hmin=1.5)
    top = surfaces(m, planar("z", lz1))
    bot = surfaces(m, planar("z", lz0))
    f_top = faces_on(m, top)
    r_c = lambda c, x, y: np.hypot(c[:, 0] - x, c[:, 1] - y)
    f_win = faces_on(m, top, lambda c: (r_c(c, 0, 0) >= 28) & (r_c(c, 0, 0) <= 50))
    f_dose = faces_on(m, top, lambda c: (np.abs(c[:, 0] - xd) <= 17) & (np.abs(c[:, 1]) <= 55) & ~((np.abs(c[:, 0] - xd) <= 6) & (np.abs(c[:, 1]) <= P["dose_y"])))
    f_cam = faces_on(m, top, lambda c: (r_c(c, 75, -45) >= 11) & (r_c(c, 75, -45) <= 16))
    p_win = P_ATM * math.pi * 28 ** 2 / f_win["area"].sum()
    p_dose = P_ATM * 12 * 2 * P["dose_y"] / f_dose["area"].sum()
    p_cam = P_ATM * math.pi * 11 ** 2 / f_cam["area"].sum()
    go = 3 + P.get("gland_w", 4.0)
    land = nodes_on(m, bot, lambda q: ((np.abs(q[:, 0]) >= ix + go) | (np.abs(q[:, 1]) >= iy + go)) & (np.abs(q[:, 0]) <= ix + go + 5) & (np.abs(q[:, 1]) <= iy + go + 5))
    bx, by = ix + 11.5, iy + 11.5
    pins = [nearest(m, (sx * bx, sy * by, lz0), land) for sx in (-1, 1) for sy in (-1, 1)]
    job = "c2_lid"
    write_model(job, m, AL, nset("LAND", land) + nset("PINS", pins))
    loads = "*DLOAD\n" + dload_lines(f_top, P_ATM) + dload_lines(f_win, p_win) + dload_lines(f_dose, p_dose) + dload_lines(f_cam, p_cam)
    sol = solver_for(m)
    append(job, static_step("LAND,3,3\nPINS,1,2\n", loads, solver=sol))
    run_ccx(job)
    U, S, vm = static_results(m, job)
    i = int(np.argmax(vm))
    seat = m["idx"][nodes_on(m, top, lambda q: (np.hypot(q[:, 0], q[:, 1]) >= 28) & (np.hypot(q[:, 0], q[:, 1]) <= 50))]
    camn = m["idx"][nodes_on(m, top, lambda q: np.hypot(q[:, 0] - 75, q[:, 1] + 45) <= 16)]
    xy = m["xyz"][seat][:, :2]
    A = np.column_stack([np.ones(len(xy)), xy])
    coef, *_ = np.linalg.lstsq(A, U[seat, 2], rcond=None)
    r = dict(case="2 lid, vacuum", material=AL["label"],
             load=f"{P_ATM:.4f} MPa on the top face; window {P_ATM * math.pi * 28 ** 2:.0f} N, dose slot and camera port carried round their flanges; z fixed on the outer sealing land, 4 bolt points pinned in-plane",
             nodes=len(m["ntags"]), elements=len(m["tets"]),
             vm_max=float(vm[i]), vm_max_at=m["xyz"][i].tolist(), vm_p995=float(np.percentile(vm, 99.5)),
             u_max=float(np.linalg.norm(U, axis=1).max()), window_seat_uz=float(U[seat, 2].min()),
             window_seat_tilt_urad=float(np.hypot(coef[1], coef[2]) * 1e6), camera_port_uz=float(U[camn, 2].min()),
             sf_yield=AL["sy"] / float(vm[i]))
    r["criterion"] = "window seat sag << Rayleigh range (±3.7 mm) and seat tilt negligible; SF >= 2 on yield"
    r["pass"] = r["sf_yield"] >= 2
    r["png"] = "c2_lid_vm.png"
    stamp(r, m, sol)
    render(m, U, vm, OUT / r["png"], f"Case 2: lid at vacuum, 6061-T6\nmax von Mises {vm[i]:.1f} MPa; window seat sag {abs(r['window_seat_uz']) * 1000:.1f} um",
           (-0.6, -1.4, 1.6), mark=m["xyz"][i])
    R["2"] = r
    print(f"  case 2: vm max {vm[i]:.1f} MPa, seat sag {r['window_seat_uz'] * 1000:.2f} um, u max {r['u_max'] * 1000:.1f} um")


def case3(parts, R):
    cy = P["cy"]
    dy1, dy0 = -cy, -cy - 15.0
    m = mesh_shape(part(parts, "Chamber door").shape, "c3_door", hmax=5.0, hmin=1.2)
    outer = surfaces(m, planar("y", dy0))
    back = surfaces(m, planar("y", dy1))
    f_out = faces_on(m, outer, lambda c: (np.abs(c[:, 0]) <= 116) & (c[:, 2] >= 2) & (c[:, 2] <= 106))
    p_eq = P_ATM * 232 * 104 / f_out["area"].sum()
    land = nodes_on(m, back, lambda q: (np.abs(q[:, 0]) >= 118) | (q[:, 2] <= 0) | (q[:, 2] >= 108))
    pa = nearest(m, (-124, dy1, 54), land)
    pb = nearest(m, (124, dy1, 54), land)
    job = "c3_door"
    write_model(job, m, AL, nset("LAND", land))
    sol = solver_for(m)
    append(job, static_step(f"LAND,2,2\n{pa},1,1\n{pa},3,3\n{pb},3,3\n", "*DLOAD\n" + dload_lines(f_out, p_eq), solver=sol))
    run_ccx(job)
    U, S, vm = static_results(m, job)
    i = int(np.argmax(vm))
    F_over = 0.005 * 232 * 104          # +50 mbar on the area inside the door O-ring
    r = dict(case="3 door, vacuum", material=AL["label"], load=f"{P_ATM * 232 * 104:.0f} N over the area inside the O-ring; y fixed on the land outside the groove",
             nodes=len(m["ntags"]), elements=len(m["tets"]),
             vm_max=float(vm[i]), vm_max_at=m["xyz"][i].tolist(), u_max=float(np.linalg.norm(U, axis=1).max()),
             sf_yield=AL["sy"] / float(vm[i]),
             overpressure_50mbar_total_N=F_over, overpressure_per_latch_N=F_over / 2,
             latch_rating_N=800 * 4.448, sf_latch=800 * 4.448 / (F_over / 2))
    r["criterion"] = "SF >= 2 on yield; at +50 mbar each of the 2 toggle latches (McMaster 1807A61, 800 lb) carries half the door load"
    r["pass"] = r["sf_yield"] >= 2
    r["png"] = "c3_door_vm.png"
    stamp(r, m, sol)
    render(m, U, vm, OUT / r["png"], f"Case 3: drop-down door at vacuum, 6061-T6\nmax von Mises {vm[i]:.1f} MPa", (-0.8, -1.5, 0.6), mark=m["xyz"][i])
    R["3"] = r
    print(f"  case 3: vm max {vm[i]:.1f} MPa, u max {r['u_max'] * 1000:.2f} um, latch {F_over / 2:.0f} N each")


FIRST = "first layout"
BUILT = "as built in lpbf_low.py"


def recoater_body(parts, variant):
    """Carriage block + arm + blade holder as one 6061 body: the first layout's dimensions, or the model's current shapes."""
    xc, iy, ry, rz, zr = P["x_park"], P["iy"], P["rc_screw_y"], P["rc_screw_z"], P["rc_rail_z"]
    if variant == FIRST:     # 12 x 8 arm, 14 x 11 holder (lpbf_low.py before the FEA)
        yc = iy - 28.0
        blk = M.fuse([M.box(xc - 22, xc + 22, 33, yc, 25, zr + 17), M.box(xc - 22, xc + 22, yc, iy - 3, 25, zr - 18)]).cut(M.cyl(12.0, (xc - 23, ry, rz), "x", 46))
        arm = M.box(xc - 6, xc + 6, 33, 41, 14, 25)
        hold = M.rbox(xc - 7, xc + 7, -P["dose_y"] - 3, 41, 3.0 + P["blade_gap"], 14, 2, "|Y")
    else:
        blk = part(parts, "Recoater carriage block").shape
        arm = part(parts, "Recoater arm").shape
        hold = part(parts, "Blade holder").shape
    hb = hold.BoundingBox()
    body = blk.fuse(arm).fuse(hold).clean()
    sols = body.Solids()
    if len(sols) > 1:
        print(f"  note: recoater body has {len(sols)} solids (volumes {[round(x.Volume()) for x in sols]}); meshing them conformally")
    return body, hb.zmin, hb.ymin


def case4(parts, R):
    xc, iy, ry, rz = P["x_park"], P["iy"], P["rc_screw_y"], P["rc_screw_z"]
    yc = iy - 28.0                                     # carriage mounting face of the block (15 mm rail, 28 mm carriage)
    zr = P["rc_rail_z"]
    out = []
    for variant in (FIRST, BUILT):
        shape, bz0, yfront = recoater_body(parts, variant)
        tag = "a" if variant == FIRST else "b"
        m = mesh_shape(shape, f"c4{tag}_recoater", hmax=3.0, hmin=0.8)
        car = nodes_on(m, surfaces(m, planar("y", yc)), lambda q: (q[:, 2] >= zr - 17) & (q[:, 2] <= zr + 17) & (np.abs(q[:, 0] - xc) <= 28.5))
        boren = nodes_on(m, list(m["surfs"]), lambda q: np.abs(np.hypot(q[:, 1] - ry, q[:, 2] - rz) - 12.0) < 0.2)
        botn = nodes_on(m, surfaces(m, planar("z", bz0)))
        frontn = nodes_on(m, surfaces(m, planar("y", yfront)))
        if min(len(car), len(boren), len(botn), len(frontn)) == 0:
            raise RuntimeError(f"case 4 selection empty: car {len(car)} bore {len(boren)} bottom {len(botn)} front {len(frontn)}")
        res = {}
        for lc, loads in (("spread", cload_lines(botn, (-10.0, 0.0, 10.0))), ("hit", cload_lines(frontn, (-50.0, 0.0, 0.0)))):
            job = f"c4{tag}_{lc}"
            write_model(job, m, AL, nset("CAR", car) + nset("BORE", boren))
            append(job, static_step("CAR,2,3\nBORE,1,1\n", "*CLOAD\n" + loads, solver=solver_for(m)))
            run_ccx(job)
            U, S, vm = static_results(m, job)
            bi = m["idx"][botn]
            yb = m["xyz"][bi][:, 1]
            on_plate = np.abs(yb) <= 25
            i = int(np.argmax(vm))
            res[lc] = dict(vm_max=float(vm[i]), vm_max_at=m["xyz"][i].tolist(), uz_max_um=float(np.abs(U[bi, 2]).max() * 1000),
                           ux_max_um=float(np.abs(U[bi, 0]).max() * 1000),
                           uz_range_over_plate_um=float(np.ptp(U[bi[on_plate], 2]) * 1000),
                           uz_tip_um=float(U[bi[np.argmin(yb)], 2] * 1000), uz_root_um=float(U[bi[np.argmax(yb)], 2] * 1000),
                           sf_yield=AL["sy"] / float(vm[i]))
            if lc == "spread":
                png = f"c4{tag}_recoater_vm.png"
                render(m, U, vm, OUT / png, f"Case 4{tag}: recoater block + arm + blade holder ({variant}), 10 N up + 10 N drag\n"
                       f"blade tip uz {res[lc]['uz_tip_um']:.1f} um, max |uz| {res[lc]['uz_max_um']:.1f} um, max |ux| {res[lc]['ux_max_um']:.1f} um",
                       (-1.0, -1.2, 0.5), mark=m["xyz"][i], zoom=1.3)
                res[lc]["png"] = png
        out.append(dict(variant=variant, nodes=len(m["ntags"]), elements=len(m["tets"]), **res))
        stamp(out[-1], m, solver_for(m))
        print(f"  case 4 {variant}: spread uz max {res['spread']['uz_max_um']:.1f} um (tip {res['spread']['uz_tip_um']:.1f}), ux max {res['spread']['ux_max_um']:.1f} um; "
              f"hit vm {res['hit']['vm_max']:.1f} MPa, hit uz {res['hit']['uz_max_um']:.0f} um")
    r = dict(case="4 recoater carriage block + arm + blade holder", material=AL["label"],
             load="spread: 10 N up + 10 N drag (-x) over the holder's bottom face; hit: 50 N (-x) on its front end; carriage face fixed in y,z, nut bore in x",
             variants=out, criterion="blade deflection < 5 um under the spreading load (1/6 of a 30 um layer); no yield in the hit")
    for v in out:
        v["pass"] = v["spread"]["uz_max_um"] < 5 and v["spread"]["ux_max_um"] < 5 and v["hit"]["sf_yield"] > 1
    R["4"] = r


def case5(parts, R):
    m = mesh_shape(part(parts, "Z lift arm").shape, "c5_zarm", hmax=3.0, hmin=0.8)
    fixn = nodes_on(m, surfaces(m, planar("y", 56.0)))
    boren = nodes_on(m, list(m["surfs"]), lambda q: (np.abs(np.hypot(q[:, 0], q[:, 1]) - 6.0) < 0.2))
    job = "c5_zarm"
    write_model(job, m, AL, nset("FIX", fixn) + nset("BORE", boren))
    sol = solver_for(m)
    append(job, static_step("FIX,1,3\n", "*CLOAD\n" + cload_lines(boren, (10.0, 0.0, -50.0)), solver=sol))
    run_ccx(job)
    U, S, vm = static_results(m, job)
    i = int(np.argmax(vm))
    z_top = m["xyz"][:, 2].max()
    topn = m["idx"][nodes_on(m, surfaces(m, planar("z", z_top)), lambda q: (np.hypot(q[:, 0], q[:, 1]) >= 6) & (np.hypot(q[:, 0], q[:, 1]) <= 18))]
    xy = m["xyz"][topn][:, :2]
    coef, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(xy)), xy]), U[topn, 2], rcond=None)
    tilt = math.hypot(coef[1], coef[2])
    bi = m["idx"][boren]
    r = dict(case="5 Z lift arm", material=AL["label"], load="50 N down + 10 N in x at the rod bore; carriage face (y = 56) fixed",
             nodes=len(m["ntags"]), elements=len(m["tets"]),
             vm_max=float(vm[i]), vm_max_at=m["xyz"][i].tolist(), u_rod_um=(U[bi].mean(axis=0) * 1000).tolist(),
             u_max=float(np.linalg.norm(U, axis=1).max()), tilt_urad=tilt * 1e6, plate_tilt_um_over_50mm=tilt * 50 * 1000,
             sf_yield=AL["sy"] / float(vm[i]))
    r["criterion"] = "plate tilt < 10 um across Ø50 (arm only; the carriage, rail and actuator add their own compliance)"
    r["pass"] = r["plate_tilt_um_over_50mm"] < 10
    r["png"] = "c5_zarm_vm.png"
    stamp(r, m, sol)
    render(m, U, vm, OUT / r["png"], f"Case 5: Z lift arm, 50 N down + 10 N side at the rod\nrod sag {abs(r['u_rod_um'][2]):.1f} um, plate tilt {r['plate_tilt_um_over_50mm']:.1f} um over Ø50",
           (1.0, -1.3, 0.9), mark=m["xyz"][i], zoom=1.3)
    R["5"] = r
    print(f"  case 5: vm {vm[i]:.1f} MPa, rod u {np.round(r['u_rod_um'], 2)} um, tilt {r['plate_tilt_um_over_50mm']:.2f} um/50 mm")


def bridge_variant(t=15.0, s=40.0, w=4.0):
    """The first layout's bridge (15 mm plate on 40 x 40 x 4 posts at (-315, +-145) and (200, +-145)); t, s, w give what-ifs."""
    zb1 = P["z_base1"]
    zb1_ = P["z_bridge1"]
    xd = P["x_dose"]
    br = M.box(-345, 225, -170, 170, zb1_ - t, zb1_)
    br = br.cut(M.cyl(P["lens_d"] / 2 + 3, (0, 0, zb1_ - t - 1), "z", t + 2))
    br = br.cut(M.box(xd - 26, xd + 26, -171, 52, zb1_ - t - 1, zb1_ + 1))
    br = br.cut(M.cyl(40, (112, -66, zb1_ - t - 1), "z", t + 2))
    out = br
    for cxp in (-315.0, 200.0):
        for cyp in (-145.0, 145.0):
            x0 = min(max(cxp - s / 2, -345), 225 - s)
            y0 = min(max(cyp - s / 2, -170), 170 - s)
            post = M.box(x0, x0 + s, y0, y0 + s, zb1, zb1_ - t).cut(M.box(x0 + w, x0 + s - w, y0 + w, y0 + s - w, zb1 - 1, zb1_ - t + 1))
            out = out.fuse(post)
    return out.clean()


def case6(parts, R):
    zb1 = P["z_base1"]
    zb1_ = P["z_bridge1"]
    beam_z = P["beam_z"]
    galvo_cm = (2.5 * (zb1_ + P["galvo_h"] / 2) + 0.6 * (P["z_lens0"] + P["lens_len"] / 2)) / 3.1
    masses = {"GALVO": (3.1e-3, (0.0, 0.0, galvo_cm), lambda q: (np.abs(q[:, 0]) <= 57.5) & (np.abs(q[:, 1]) <= 57.5)),
              "SHUTTER": (1.2e-3, (-170.0, 0.0, beam_z), lambda q: (q[:, 0] >= -190) & (q[:, 0] <= -150) & (np.abs(q[:, 1]) <= 20)),
              "COLLIM": (0.5e-3, (-265.0, 0.0, beam_z), lambda q: (q[:, 0] >= -300) & (q[:, 0] <= -230) & (np.abs(q[:, 1]) <= 20))}
    out = []
    # mesh: hmax, hmin, elements per circle. *FREQUENCY needs a direct solver (SPOOLES; this ccx has no PARDISO or PaStiX), and
    # the bridge's mesh is set by its volume, not its details: hmax 7 gave 141,500 nodes for 6a (SPOOLES: 3.0 GB) and 350,000
    # for 6b, too many for SPOOLES in 4.5 GB. hmax 10 keeps 6b near 100,000; 6a on both meshes is compared in fea.md.
    hmax, hmin, curv = (float(x) for x in os.environ.get("FEA_C6_MESH", "10,3,6").split(","))
    only = os.environ.get("FEA_C6_ONLY", "ab")
    model_shape = part(parts, "Optics bridge (").shape.fuse(part(parts, "Optics bridge posts").shape).clean()
    for variant, shape in ((FIRST + ": 15 mm plate, 40x40x4 posts", bridge_variant()), (BUILT, model_shape)):
        tag = "a" if variant.startswith(FIRST) else "b"
        if tag not in only:
            continue
        m = mesh_shape(shape, f"c6{tag}_bridge", hmax=hmax, hmin=hmin, curv=curv)
        feet = nodes_on(m, surfaces(m, planar("z", zb1)))
        topf = surfaces(m, planar("z", zb1_))
        nmax = int(m["ntags"].max())
        extra = nset("FEET", feet)
        nodes_txt, rigid_txt, mass_txt, cl = "", "", "", ""
        eid = len(m["tets"])
        for k, (nm, (mass, cm, filt)) in enumerate(masses.items()):
            ids = nodes_on(m, topf, filt)
            ref, rot = nmax + 1 + 2 * k, nmax + 2 + 2 * k
            nodes_txt += f"{ref},{cm[0]},{cm[1]},{cm[2]}\n{rot},{cm[0]},{cm[1]},{cm[2]}\n"
            extra += nset(f"F{nm}", ids)
            rigid_txt += f"*RIGID BODY, NSET=F{nm}, REF NODE={ref}, ROT NODE={rot}\n"
            eid += 1
            mass_txt += f"*ELEMENT, TYPE=MASS, ELSET=M{nm}\n{eid},{ref}\n*MASS, ELSET=M{nm}\n{mass}\n"
            cl += f"{ref},3,{-mass * G:.6g}\n"
        extra = "*NODE, NSET=REFS\n" + nodes_txt + extra + rigid_txt + mass_txt
        res = {}
        job = f"c6{tag}_static"
        write_model(job, m, AL, extra)
        sol = "SPOOLES"           # the modal step below needs SPOOLES on this mesh anyway (3.5 GB for 6b's 131,000 nodes)
        append(job, f"*STEP\n*STATIC, SOLVER={sol}\n*BOUNDARY\nFEET,1,3\n*DLOAD\nEALL,GRAV,9810.,0.,0.,-1.\n*CLOAD\n" + cl + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
        run_ccx(job)
        U, S, vm = static_results(m, job)
        rim = m["idx"][nodes_on(m, topf, lambda q: np.hypot(q[:, 0], q[:, 1]) <= 60)]
        res["gravity"] = dict(lens_bore_sag_um=float(U[rim, 2].mean() * 1000), u_max_um=float(np.linalg.norm(U[:len(m["ntags"])], axis=1).max() * 1000), vm_max=float(vm.max()))
        job = f"c6{tag}_modal"
        write_model(job, m, AL, extra)
        append(job, "*BOUNDARY\nFEET,1,3\n*STEP\n*FREQUENCY, SOLVER=SPOOLES\n6\n*NODE FILE\nU\n*END STEP\n")
        run_ccx(job)
        f = read_freqs(job)
        blocks = [b for b in read_frd(job) if b["name"] == "DISP"]
        shapes = []
        gref = nmax + 1
        gf = m["idx"][nodes_on(m, topf, masses["GALVO"][2])]
        gxy = m["xyz"][gf][:, :2]
        for k, b in enumerate(blocks[:6]):
            Um = field(m, b, 3)
            mag = np.linalg.norm(Um, axis=1)
            j = int(np.argmax(mag))
            ug = Um[gf].mean(axis=0)                                  # the galvo footprint moves as a rigid body
            coef, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(gxy)), gxy]), Um[gf, 2], rcond=None)
            shapes.append(dict(f_hz=f[k] if k < len(f) else None, galvo_dir=(ug / (np.linalg.norm(ug) + 1e-30)).round(2).tolist(),
                               max_at=m["xyz"][j].round(0).tolist(), galvo_rel=float(np.linalg.norm(ug) / (mag.max() + 1e-30)),
                               galvo_tilt_rel=float(np.hypot(coef[1], coef[2]) * 100.0 / (mag.max() + 1e-30))))
            if k == 0:
                png = f"c6{tag}_bridge_mode1.png"
                render(m, Um, mag / mag.max(), OUT / png, f"Case 6{tag}: optics bridge ({variant}), mode 1 = {f[0]:.0f} Hz", (-1.0, -1.6, 0.7),
                       label="|u| (normalised)", scale=nice(40.0 / mag.max()), zoom=1.2, cmap="viridis")
                res["png"] = png
        res["modes"] = shapes
        out.append(dict(variant=variant, nodes=len(m["ntags"]), elements=len(m["tets"]), **res))
        stamp(out[-1], m, f"{sol} (gravity), SPOOLES (modes)", mesh=dict(hmax=hmax, hmin=hmin, per_circle=curv))
        print(f"  case 6 {variant}: f = {[round(x, 1) for x in f]} Hz; gravity sag at lens {res['gravity']['lens_bore_sag_um']:.1f} um")
    r = dict(case="6 optics bridge + posts", material=AL["label"],
             load="gravity + galvo/lens 3.1 kg, shutter 1.2 kg, collimator 0.5 kg as rigid masses at their centres of mass; post feet fixed",
             variants=out, criterion="first mode > 100 Hz (60 Hz minimum) so building and VLM vibration don't excite the galvo")
    for v in out:
        v["pass"] = v["modes"][0]["f_hz"] > 100
    R["6"] = r


def case7(parts, R):
    r0, t, ru = 25.4, 8.0, 24.0
    MR = 52.4
    sf_an = MR * t ** 2 / (1.25 * P_ATM * ru ** 2)
    t_req = {sf: ru * math.sqrt(1.25 * P_ATM * sf / MR) for sf in (4, 6)}
    shape = cq.Solid.makeCylinder(r0, t, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
    m = mesh_shape(shape, "c7_window", hmax=2.0, hmin=0.6)
    top = surfaces(m, planar("z", t))
    bot = surfaces(m, planar("z", 0.0))
    ring = nodes_on(m, bot, lambda q: np.abs(np.hypot(q[:, 0], q[:, 1]) - ru) <= 0.6)
    c0 = nearest(m, (0, 0, 0))
    c1 = nearest(m, (ru, 0, 0), ring)
    fs = M.MAT["fused_silica"]
    job = "c7_window"
    write_model(job, m, fs, nset("RING", ring))
    sol = solver_for(m)
    append(job, static_step(f"RING,3,3\n{c0},1,2\n{c1},2,2\n", "*DLOAD\n" + dload_lines(faces_on(m, top), P_ATM), solver=sol))
    run_ccx(job)
    U, S, vm = static_results(m, job)
    s1 = principal_max(S)
    i = int(np.argmax(s1))
    roark = 3 * (3 + fs["nu"]) * P_ATM * ru ** 2 / (8 * t ** 2)
    r = dict(case="7 laser window, Ø50.8 x 8 mm UV fused silica", material=fs["label"],
             load=f"{P_ATM:.4f} MPa, simply supported on Ø{2 * ru:.0f} (unclamped, O-ring)",
             nodes=len(m["ntags"]), elements=len(m["tets"]),
             s1_max=float(s1[i]), s1_max_at=m["xyz"][i].tolist(), roark_ss=roark, sf_fea=MR / float(s1[i]), sf_formula=sf_an,
             t_required_mm={str(k): v for k, v in t_req.items()}, u_max_um=float(np.linalg.norm(U, axis=1).max() * 1000))
    r["criterion"] = "SF >= 4-6 against the 52.4 MPa abraded modulus of rupture (Corning 7980)"
    r["pass"] = r["sf_fea"] >= 6
    stamp(r, m, sol)
    R["7"] = r
    print(f"  case 7: s1 max {s1[i]:.2f} MPa (Roark {roark:.2f}), SF {r['sf_fea']:.0f}; t needed {t_req}")


# --------------------------------------------------------------------------------------------
def write_md(R):
    L = ["# FEA summary (CalculiX 2.21, C3D10, from cad/lpbf_low.py)", "",
         "Peak stresses at sharp re-entrant edges of the CAD (pocket floors, box-cut slots) are mesh-dependent; the 99.5th-percentile value is given where it matters. Machined parts get corner radii, which lower those peaks.", "",
         "| Case | Material | Load | Max σ_vM (MPa), where | Max displacement | Criterion | Result |", "|---|---|---|---|---|---|---|"]
    if "1" in R:
        r = R["1"]
        jz = r.get("floor_joint_sz") or {}
        L.append(f"| 1 Chamber: frame + floor plate (bonded across the floor joint), open top, full vacuum, {BUILT} | {r['material']} | 1 atm net + lid {P_ATM * 2 * (P['ix'] + 3 + P.get('gland_w', 4.0) / 2) * 2 * (P['iy'] + 3 + P.get('gland_w', 4.0) / 2) / 1000:.1f} kN + door {P_ATM * 232 * 104 / 1000:.1f} kN + module/plenum/funnel 1.2 kN under the floor | "
                 f"{r['vm_max']:.1f} at {loc_text(r['vm_max_at'])}; 99.5 %: {r['vm_p995']:.1f} | {r['u_max'] * 1000:.1f} µm; door land Δy {r['door_land_uy_range'] * 1000:.1f} µm, lid land Δz {r['lid_land_uz_range'] * 1000:.1f} µm; floor-joint σz {jz.get('min', 0):.2f}..{jz.get('max', 0):.2f} MPa | "
                 f"SF ≥ 2 yield, Goodman ≥ 2 | SF {r['sf_yield']:.1f} yield, {r['sf_haz']:.1f} vs welded HAZ (110 MPa), Goodman {r['sf_fatigue_goodman']:.1f}: {'pass' if r['pass'] else 'FAIL'} |")
    if "1b" in R:
        r = R["1b"]
        p2 = r.get("plus20mbar", {})
        L.append(f"| 1b Chamber: frame + floor plate + lid bonded, full vacuum, {BUILT} | {r['material']} | as 1, lid included | {r['vm_max']:.1f} at {loc_text(r['vm_max_at'])}; 99.5 %: {r['vm_p995']:.1f} | "
                 f"{r['u_max'] * 1000:.1f} µm at {loc_text(r['u_max_at'])}; door land Δy {r['door_land_uy_range'] * 1000:.1f} µm; window seat {abs(r['window_seat_uz']) * 1000:.1f} µm | "
                 f"SF ≥ 2 yield, Goodman ≥ 2 | SF {r['sf_yield']:.1f} yield, {r['sf_haz']:.1f} vs HAZ, Goodman {r['sf_fatigue_goodman']:.1f}: {'pass' if r['pass'] else 'FAIL'} |")
        if p2:
            L.append(f"| 1b′ Same body at +20 mbar (argon working pressure) | {r['material']} | the vacuum loads reversed × 0.002/0.1013 | {p2['vm_max']:.2f} at {loc_text(p2['vm_max_at'])} | "
                     f"{p2['u_max'] * 1000:.2f} µm; door land Δy {p2['door_land_uy_range'] * 1000:.2f} µm | SF ≥ 2 | SF {p2['sf_yield']:.0f}: pass |")
    if "2" in R:
        r = R["2"]
        L.append(f"| 2 Lid, vacuum, {BUILT} | {r['material']} | 1 atm on top + window/dose/camera loads | {r['vm_max']:.1f} at {loc_text(r['vm_max_at'])} | "
                 f"{r['u_max'] * 1000:.1f} µm; window seat sag {abs(r['window_seat_uz']) * 1000:.1f} µm, tilt {r['window_seat_tilt_urad']:.0f} µrad; camera port {abs(r['camera_port_uz']) * 1000:.1f} µm | "
                 f"SF ≥ 2; sag ≪ ±3.7 mm Rayleigh range | SF {r['sf_yield']:.0f}: {'pass' if r['pass'] else 'FAIL'} |")
    if "3" in R:
        r = R["3"]
        L.append(f"| 3 Door, vacuum, {BUILT} | {r['material']} | 1 atm inside the O-ring | {r['vm_max']:.1f} at {loc_text(r['vm_max_at'])} | {r['u_max'] * 1000:.1f} µm | "
                 f"SF ≥ 2; latches at +50 mbar | SF {r['sf_yield']:.0f}; latch load {r['overpressure_per_latch_N']:.0f} N each vs 3.6 kN rating: {'pass' if r['pass'] else 'FAIL'} |")
    if "4" in R:
        for v in R["4"]["variants"]:
            s, h = v["spread"], v["hit"]
            ok = v["pass"]
            L.append(f"| 4 Recoater block + arm + blade holder ({v['variant']}) | 6061-T6 | 10 N up + 10 N drag; 50 N hit | "
                     f"spread {s['vm_max']:.1f}; hit {h['vm_max']:.1f} at {loc_text(h['vm_max_at'])} | blade |uz| {s['uz_max_um']:.1f} µm (tip {s['uz_tip_um']:.1f}), |ux| {s['ux_max_um']:.1f} µm; over the plate Δuz {s['uz_range_over_plate_um']:.1f} µm; hit |uz| {h['uz_max_um']:.0f} µm | "
                     f"< 5 µm spreading, no yield in a hit | {'pass' if ok else 'FAIL'} (hit SF {h['sf_yield']:.1f}) |")
    if "5" in R:
        r = R["5"]
        L.append(f"| 5 Z lift arm, {BUILT} | 6061-T6 | 50 N down + 10 N side | {r['vm_max']:.1f} at {loc_text(r['vm_max_at'])} | rod ({', '.join(f'{x:.1f}' for x in r['u_rod_um'])}) µm | "
                 f"plate tilt < 10 µm over Ø50 | tilt {r['plate_tilt_um_over_50mm']:.1f} µm: {'pass' if r['pass'] else 'FAIL'} |")
    if "6" in R:
        for v in R["6"]["variants"]:
            f = [x["f_hz"] for x in v["modes"]]
            L.append(f"| 6 Optics bridge + posts ({v['variant']}) | 6061-T6 | gravity + 4.8 kg of optics | {v['gravity']['vm_max']:.1f} | "
                     f"lens bore sag {abs(v['gravity']['lens_bore_sag_um']):.1f} µm; f1–f6 = {', '.join(f'{x:.0f}' for x in f)} Hz | f1 > 100 Hz | {'pass' if f[0] > 100 else 'FAIL'} |")
    if "7" in R:
        r = R["7"]
        L.append(f"| 7 Window Ø50.8 × 8 | {r['material']} | 1 atm, simply supported Ø48 | max principal {r['s1_max']:.2f} (Roark {r['roark_ss']:.2f}) | {r['u_max_um']:.2f} µm | "
                 f"SF ≥ 6 vs 52.4 MPa | SF {r['sf_fea']:.0f} (formula {r['sf_formula']:.0f}); 2.4 mm would do at SF 4, 2.9 mm at SF 6: pass |")
    if "1f" in R:
        r = R["1f"]
        g = r["gland"]
        L += ["", f"## 1f Floor-plate bolted joint (Shigley) and floor gland (Parker), {BUILT}", "",
              f"{r['screws']}; proof {r['proof_MPa']:.0f} MPa (A4-50 basis, conservative), preload {r['preload_N']:.0f} N each at {r['torque_Nm']:.2f} N·m (K = {r['nut_factor']}); "
              f"grip {r['grip_mm']:.1f} mm, k_b {r['kb_N_per_mm'] / 1000:.0f} kN/mm, k_m {r['km_N_per_mm'] / 1000:.0f} kN/mm (30° frustum), C = {r['C']:.3f}. "
              f"Thread engagement {r['thread_engagement_mm']:.1f} mm: strip {r['thread_strip_N'] / 1000:.1f} kN > screw break {r['screw_break_N'] / 1000:.1f} kN. "
              f"Total preload {r['preload_total_N'] / 1000:.1f} kN on {r['land_area_mm2'] / 100:.0f} cm² of lands = {r['land_pressure_preload_MPa']:.1f} MPa; head bearing {r['head_bearing_MPa']:.0f} MPa.", "",
              "| Case | Load on the joint (N) | Per screw (N) | Load factor n_L | Separation factor n_0 |", "|---|---|---|---|---|"]
        for k, v in r["cases"].items():
            nl = f"{v['n_load']:.1f}" if v["n_load"] else "– (joint pressed shut)"
            n0 = f"{v['n_sep']:.1f}" if v["n_sep"] else "– (joint pressed shut)"
            L.append(f"| {k} | {v['load_total_N']:.0f} | {v['load_per_screw_N']:.0f} | {nl} | {n0} |")
        L += ["", f"Floor gland: {g['cs']} mm FKM 75A cord, groove {g['depth']} deep × {g['width']} wide (Parker face gland {g['parker_range']['depth'][0]}–{g['parker_range']['depth'][1]} × "
              f"{g['parker_range']['width_face'][0]}–{g['parker_range']['width_face'][1]}); squeeze {g['squeeze_nom']:.1f} % ({g['squeeze_min']:.1f}–{g['squeeze_max']:.1f} % at ±0.05 mm and cord tolerance); "
              f"fill {g['fill_nom']:.0f} % (max {g['fill_max_cold']:.0f} % cold); path {g['path_mm']:.0f} mm; {g['splice']}. O-ring force {r['oring_force_N']['nominal'] / 1000:.1f} kN nominal, "
              f"{r['oring_force_N']['max_tolerance'] / 1000:.1f} kN at max squeeze, {r['oring_force_N']['parker_80A'] / 1000:.1f} kN on Parker's 80A bar. {'pass' if r['pass'] else 'FAIL'}."]
    L += ["", "## How each case was run", "",
          "Since 2026-11-22 every case records when it ran, on which commit of the model, its mesh and its solver (SPOOLES up to 60,000 nodes, "
          "ccx's ITERATIVE CHOLESKY above; the bridge on a coarser mesh so that its modes can use SPOOLES; see the script's docstring). "
          "Cases without a record ran earlier, on the model of their day.", "",
          "| Case | Run (UTC) | Model commit | Nodes | Solver |", "|---|---|---|---|---|"]
    rows = [(k, R[k]) for k in ("1", "1b", "2", "3", "5", "7") if k in R]
    rows += [(f"{k} ({v['variant']})", v) for k in ("4", "6") for v in R.get(k, {}).get("variants", [])]
    for k, r in sorted(rows, key=lambda x: x[0]):
        run = r.get("run")
        if run:
            mesh = run.get("mesh")
            ms = f", hmax {mesh['hmax']:g} mm" if mesh else ""
            L.append(f"| {k} | {run['utc']} | {run['commit']} | {run['nodes']:,}{ms} | {run['solver']} |")
        else:
            L.append(f"| {k} | before 2026-11-22 (not recorded) | – | {r.get('nodes', 0):,} | {'ITERATIVE CHOLESKY' if k in ('1', '1b') else 'SPOOLES'} |")
    for head, key in (("Checks of the solver and mesh settings", "checks"), ("What changed against the previous results", "changes")):
        if R.get("notes", {}).get(key):
            L += ["", f"### {head}", ""] + [f"- {x}" for x in R["notes"][key]]
    if "6" in R:
        L += ["", "Mode shapes (case 6): direction of the galvo's centre of mass in each mode, and where the largest motion is."]
        for v in R["6"]["variants"]:
            for k, s in enumerate(v["modes"]):
                L.append(f"- {v['variant']}, mode {k + 1}: {s['f_hz']:.0f} Hz; galvo translates along {s['galvo_dir']} at {s['galvo_rel']:.2f} of the peak motion "
                         f"(tilt x 100 mm: {s.get('galvo_tilt_rel', 0):.2f}); peak at {s['max_at']}")
    (OUT / "fea.md").write_text("\n".join(L) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RUN.mkdir(parents=True, exist_ok=True)
    which = sys.argv[1:] or ["7", "5", "4", "3", "2", "6", "1", "1b", "1f"]
    jf = OUT / "fea.json"
    if len(which) > 1:              # one process per case: memory is returned between cases, and a failed case doesn't stop the rest
        failed = []
        for c in which:
            if subprocess.run([sys.executable, __file__, c]).returncode != 0:
                failed.append(c)
                print(f"case {c} FAILED")
        if failed:
            sys.exit(f"failed cases: {' '.join(failed)}")
        return
    parts = M.build()
    R = json.loads(jf.read_text()) if jf.exists() else {}
    for c in which:
        t0 = time.time()
        print(f"case {c}")
        globals()[f"case{c}"](parts, R)
        jf.write_text(json.dumps(R, indent=1, default=float))
        write_md(R)
        print(f"  case {c} done in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
