"""CalculiX FEA of the fast-track machines' structure (#260, PR 294 round 2): the box lid, the cube's top plate and window,
the scan-head plate on its gantry, and the piston rod.

Geometry comes from the fast-track CadQuery model (cad/ft_model.py: build(state, pz), P, levels()), so the script re-runs on a
changed model. Each analysed body is exported to BREP and meshed with gmsh (quadratic tetrahedra, C3D10). Bodies of different
materials are fragmented into one conformal mesh (bonded where they touch) and keep their own material. Loads and supports
are put on faces picked geometrically; ccx 2.21 solves; results are read back from the .frd/.dat. Units: mm, N, MPa, tonne.
The helpers follow PR 266's desktop-lpbf/analysis/fea/fea.py (mesh, C3D10 node order, face loads, .frd reader, child-process
rendering with render_fea.py).

Cases
  4a  FT-1 box lid (14 ga 304, 1.9 mm, with the window stack) on its lid gasket, held by the four lid clamps and the hinge:
      gasket preload, +10 mbar purge overpressure, +50 mbar fault (linear, and NLGEOM at +50 mbar). Two gaskets: a solid
      FKM cord and a closed-cell silicone sponge strip. 4a-check: a clamped 1.9 mm plate on the same mesh size against
      Timoshenko, to show what one quadratic tet through the sheet gives.
  4b  FT-1V: the Ideal Vacuum 12 in. top plate blank bored for the window ring (MK-13) at 1 atm, clamped and simply
      supported on the cube frame; the Ø50.8 x 9.53 mm fused-silica window on its O-ring at 1 atm (Roark + FEA), and the
      same window in the box at +50 mbar.
  4c  the scan-head plate MK-09 under the T-slot gantry cross-beam, with the hurrySCAN 25 and the lens as one rigid mass:
      gravity sag and tilt, the beam's position error at the bed, and the first modes of plate + cross-beam + uprights.
  4d  the piston rod MK-06 (analytic): Euler buckling, lateral stiffness under the blade's drag, the axial load on the
      Zaber X-VSR20A, and the rod's thermal growth.

Run:  cd <repo> && OMP_NUM_THREADS=2 /tmp/tools/capmem 3 xvfb-run -a -s "-screen 0 1920x1080x24" \\
          /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/fea/ft_struct.py [4a 4b 4c 4d]
Scratch (.brep/.inp/.frd/.dat) goes to /tmp/workerA/struct/ (env FT_STRUCT_RUN); results to analysis/out/fea/ (struct.json,
struct.md, struct-*.png). Cases not run keep their previous results in struct.json.
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

HERE = pathlib.Path(__file__).resolve().parent            # desktop-lpbf/fast-track/analysis/fea
FT = HERE.parents[1]                                       # desktop-lpbf/fast-track
ROOT = FT.parent                                           # desktop-lpbf
sys.path.insert(0, str(FT / "cad"))
import cadquery as cq  # noqa: E402
import gmsh  # noqa: E402
import ft_model as M  # noqa: E402

OUT = FT / "analysis" / "out" / "fea"
RUN = pathlib.Path(os.environ.get("FT_STRUCT_RUN", "/tmp/workerA/struct"))
RENDER = ROOT / "analysis" / "fea" / "render_fea.py"
P_ATM = 0.101325          # MPa
G = 9810.0                # mm/s2
E_TOL = 0.05              # mm, face-classification tolerance
DIRECT_MAX = int(os.environ.get("FEA_DIRECT_MAX", "60000"))
P = M.P

# Materials (rho in kg/m3). Sources: 6061-T6 and 304: ASM / MatWeb data sheets (304 yield 215 MPa as in PR 266's MAT; ASTM
# A240 minimum is 205 MPa); fused silica: Corning 7980 data sheet (E 72.7 GPa, nu 0.16, abraded modulus of rupture 52.4 MPa).
MAT = {
    "al6061": dict(E=68.9e3, nu=0.33, rho=2700.0, sy=276.0, su=310.0, label="6061-T6 aluminium"),
    "ss304": dict(E=193e3, nu=0.29, rho=8000.0, sy=215.0, su=505.0, label="304 stainless (annealed sheet)"),
    "fused_silica": dict(E=72.7e3, nu=0.16, rho=2201.0, mor=52.4, design=6.9, label="UV fused silica (Corning 7980)"),
}


def solver_for(n_nodes):
    return os.environ.get("FEA_SOLVER") or ("SPOOLES" if n_nodes <= DIRECT_MAX else "ITERATIVE CHOLESKY")


def model_commit():
    try:
        h = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=FT, capture_output=True, text=True, check=True).stdout.strip()
        d = subprocess.run(["git", "status", "--porcelain", "--", "cad"], cwd=FT, capture_output=True, text=True, check=True).stdout.strip()
        return h + ("+dirty" if d else "")
    except Exception:  # noqa: BLE001
        return "unknown"


def stamp(r, m, solver, **kw):
    r["run"] = dict(utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=model_commit(), nodes=int(len(m["ntags"])),
                    elements=int(len(m["tets"])), solver=solver, **kw)


# --------------------------------------------------------------------------------------------
# meshing: several bodies fragmented into one conformal C3D10 mesh; m["body"] gives each element's body
# --------------------------------------------------------------------------------------------
def mesh_bodies(bodies, name, hmax, hmin=None, curv=12, alg=10):
    RUN.mkdir(parents=True, exist_ok=True)
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add(name)
    vols_in = []
    for k, (_, shape) in enumerate(bodies):
        path = RUN / f"{name}_{k}.brep"
        shape.exportBrep(str(path))
        dts = gmsh.model.occ.importShapes(str(path))
        vols_in.append([t for d, t in dts if d == 3])
    gmsh.model.occ.synchronize()
    allv = [(3, t) for vs in vols_in for t in vs]
    owner = [k for k, vs in enumerate(vols_in) for _ in vs]
    body_of_vol = {}
    if len(allv) > 1:
        _, omap = gmsh.model.occ.fragment(allv[:1], allv[1:])
        gmsh.model.occ.synchronize()
        for i, ents in enumerate(omap):
            for d, t in ents:
                if d == 3:
                    body_of_vol.setdefault(t, owner[i])
    else:
        body_of_vol[allv[0][1]] = 0
    gmsh.option.setNumber("Mesh.MeshSizeMax", hmax)
    gmsh.option.setNumber("Mesh.MeshSizeMin", hmin or hmax / 5)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", curv)
    gmsh.option.setNumber("Mesh.ElementOrder", 2)
    gmsh.option.setNumber("Mesh.SecondOrderLinear", 1)
    gmsh.option.setNumber("Mesh.Algorithm3D", alg)
    gmsh.option.setNumber("General.NumThreads", int(os.environ.get("OMP_NUM_THREADS", "2")))
    try:
        gmsh.model.mesh.generate(3)
    except Exception as e:  # noqa: BLE001
        print(f"  HXT failed ({e}); retrying with the frontal mesher")
        gmsh.model.mesh.clear()
        gmsh.option.setNumber("Mesh.Algorithm3D", 4)
        gmsh.model.mesh.generate(3)
        gmsh.model.mesh.setOrder(2)
    ntags, xyz, _ = gmsh.model.mesh.getNodes()
    xyz = xyz.reshape(-1, 3)
    tets, body = [], []
    for _, vt in gmsh.model.getEntities(3):
        for et, _, en in zip(*gmsh.model.mesh.getElements(3, vt)):
            if et == 11:
                t = en.reshape(-1, 10)
                tets.append(t)
                body.append(np.full(len(t), body_of_vol.get(vt, 0), dtype=np.int64))
    tets = np.vstack(tets).astype(np.int64)[:, [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]]     # gmsh -> CalculiX C3D10 order
    body = np.concatenate(body)
    surfs = {}
    for _, tag in gmsh.model.getEntities(2):
        bb = gmsh.model.getBoundingBox(2, tag)
        up, _ = gmsh.model.getAdjacencies(2, tag)
        tri = None
        for et, _, en in zip(*gmsh.model.mesh.getElements(2, tag)):
            if et == 9:
                tri = en.reshape(-1, 6).astype(np.int64)
        if tri is not None:
            surfs[tag] = dict(bb=bb, tri=tri, nvol=len(up))
    gmsh.finalize()
    idx = np.full(int(ntags.max()) + 1, -1, dtype=np.int64)
    idx[ntags.astype(np.int64)] = np.arange(len(ntags))
    m = dict(name=name, ntags=ntags.astype(np.int64), xyz=xyz, idx=idx, tets=tets, body=body, surfs=surfs)
    c = xyz[idx[tets[:, :4]]]
    vol = np.einsum("ij,ij->i", np.cross(c[:, 1] - c[:, 0], c[:, 2] - c[:, 0]), c[:, 3] - c[:, 0])
    if (vol < 0).any():
        neg = vol < 0
        tets[neg] = tets[neg][:, [0, 2, 1, 3, 6, 5, 4, 7, 9, 8]]
        print(f"  flipped {neg.sum()} inverted tets")
    m["faces"] = face_index(m)
    print(f"  mesh {name}: {len(ntags)} nodes, {len(tets)} C3D10, {len(surfs)} faces, bodies {np.bincount(body).tolist()}")
    return m


_FACES = [(0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0)]   # C3D10 faces 1..4 (corner nodes)


def face_index(m):
    t = m["tets"]
    keys = []
    for f in _FACES:
        k = np.sort(t[:, list(f)], axis=1)
        keys.append(k[:, 0] * (1 << 42) + k[:, 1] * (1 << 21) + k[:, 2])
    keys = np.stack(keys, axis=1).ravel()
    order = np.argsort(keys, kind="stable")
    return keys[order], order


def tri_faces(m, tri):
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


def surfaces(m, pred, boundary=True):
    """Surface tags whose bounding box satisfies pred(xmin, ymin, zmin, xmax, ymax, zmax); outer boundary only by default."""
    return [t for t, s in m["surfs"].items() if pred(*s["bb"]) and (not boundary or s["nvol"] == 1)]


def faces_on(m, tags, cfilt=None):
    if not tags:
        raise RuntimeError("no surfaces selected")
    tri = np.vstack([m["surfs"][t]["tri"] for t in tags])
    cen, area = tri_geom(m, tri)
    if cfilt is not None:
        keep = cfilt(cen)
        tri, cen, area = tri[keep], cen[keep], area[keep]
    if len(tri) == 0:
        raise RuntimeError("face filter selected nothing")
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


def write_model(job, m, mats, extra=""):
    """mats: one material dict per body index in m['body']. EALL = every solid element (for gravity)."""
    RUN.mkdir(parents=True, exist_ok=True)
    eids = np.arange(1, len(m["tets"]) + 1)
    with open(RUN / f"{job}.inp", "w") as f:
        f.write("*HEADING\nFT " + job + "\n*NODE, NSET=NALL\n")
        np.savetxt(f, np.column_stack([m["ntags"], m["xyz"]]), fmt=["%d", "%.6f", "%.6f", "%.6f"], delimiter=",")
        bodies = np.unique(m["body"])
        for k in bodies:
            sel = m["body"] == k
            f.write(f"*ELEMENT, TYPE=C3D10, ELSET=B{k}\n")
            np.savetxt(f, np.column_stack([eids[sel], m["tets"][sel]]), fmt="%d", delimiter=",")
        f.write(f"*ELSET, ELSET=EALL, GENERATE\n1,{len(eids)},1\n")
        f.write(extra)
        for k in bodies:
            mat = mats[int(k)]
            f.write(f"*MATERIAL, NAME=M{k}\n*ELASTIC\n{mat['E']},{mat['nu']}\n*DENSITY\n{mat['rho'] * 1e-12:.5e}\n")
            f.write(f"*SOLID SECTION, ELSET=B{k}, MATERIAL=M{k}\n")
    return RUN / f"{job}.inp"


def append(job, text):
    with open(RUN / f"{job}.inp", "a") as f:
        f.write(text)


def dload_lines(fs, p):
    """*DLOAD lines: positive p pushes into the element."""
    return "".join(f"{e},P{k},{p:.6g}\n" for e, k in zip(fs["el"], fs["fc"]))


def run_ccx(job):
    t0 = time.time()
    env = dict(os.environ, OMP_NUM_THREADS=os.environ.get("OMP_NUM_THREADS", "2"))
    r = subprocess.run(["ccx", "-i", job], cwd=RUN, env=env, capture_output=True, text=True)
    (RUN / f"{job}.log").write_text(r.stdout + r.stderr)
    if "*ERROR" in r.stdout or r.returncode != 0 or not (RUN / f"{job}.frd").exists():
        tail = "\n".join([l for l in r.stdout.splitlines() if "ERROR" in l][:10]) or r.stdout[-2000:]
        raise RuntimeError(f"ccx failed for {job}:\n{tail}")
    dt = time.time() - t0
    print(f"  ccx {job}: {dt:.0f} s")
    return dt


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


def node_value(block, nid):
    j = np.nonzero(block["ids"] == nid)[0]
    return block["vals"][j[0]] if len(j) else None


def von_mises(S):
    sxx, syy, szz, sxy, syz, szx = S.T
    return np.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3 * (sxy ** 2 + syz ** 2 + szx ** 2))


def principal_max(S):
    sxx, syy, szz, sxy, syz, szx = S.T
    T = np.stack([np.stack([sxx, sxy, szx], -1), np.stack([sxy, syy, syz], -1), np.stack([szx, syz, szz], -1)], -2)
    return np.linalg.eigvalsh(T)[:, -1]


def step_results(m, job):
    """[(U, S, vm)] for every step in the .frd."""
    b = read_frd(job)
    D = [x for x in b if x["name"] == "DISP"]
    S_ = [x for x in b if x["name"] == "STRESS"]
    out = []
    for d, s in zip(D, S_):
        U = field(m, d, 3)
        S = field(m, s, 6)
        out.append((U, S, von_mises(S)))
    return out


def last_totals(tot):
    """{set name: (fx, fy, fz)} of the last print of each set (the converged end of the last step or increment)."""
    out = {}
    for (name, k), v in tot.items():
        if name not in out or k > out[name][0]:
            out[name] = (k, v)
    return {n: v for n, (k, v) in out.items()}


def read_totals(job):
    """{(set name, k-th print): (fx, fy, fz)} from *NODE PRINT, TOTALS=ONLY of RF (one print per increment)."""
    out, pending, counts = {}, None, {}
    for line in (RUN / f"{job}.dat").read_text().splitlines():
        if "total force" in line and "for set" in line:
            name = line.split("for set")[1].split()[0]
            counts[name] = counts.get(name, 0) + 1
            pending = (name, counts[name])
            continue
        if pending is not None:
            p = line.split()
            if len(p) == 3:
                try:
                    out[pending] = tuple(float(x) for x in p)
                    pending = None
                except ValueError:
                    pass
    return out


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


# --------------------------------------------------------------------------------------------
# rendering (child process, surface triangles only; same as fea.py)
# --------------------------------------------------------------------------------------------
def nice(x):
    e = 10 ** math.floor(math.log10(x))
    for k in (1, 2, 5, 10):
        if x <= k * e:
            return k * e
    return 10 * e


def surface_tris(m):
    tri = m["idx"][np.vstack([s["tri"] for s in m["surfs"].values() if s["nvol"] == 1])]
    lin = np.vstack([tri[:, [0, 3, 5]], tri[:, [3, 1, 4]], tri[:, [5, 4, 2]], tri[:, [3, 4, 5]]])
    used, inv = np.unique(lin, return_inverse=True)
    return used, inv.reshape(-1, 3)


def render(m, U, s, path, title, view, label="von Mises (MPa)", scale=None, clim=None, mark=None, zoom=1.15, cmap="turbo", up=(0, 0, 1)):
    pts = m["xyz"]
    diag = float(np.linalg.norm(pts.max(0) - pts.min(0)))
    umax = np.linalg.norm(U, axis=1).max()
    if scale is None:
        scale = nice(0.05 * diag / max(umax, 1e-12))
    used, tri = surface_tris(m)
    mk = None if mark is None else (np.asarray(mark) + scale * U[m["idx"][nearest(m, mark)]]).tolist()
    opt = dict(path=str(path), title=title + f"\ndeformation x{scale:g}", view=list(view), up=list(up), label=label, scale=float(scale),
               clim=None if clim is None else [float(c) for c in clim], mark=mk, diag=diag, zoom=zoom, cmap=cmap)
    npz = RUN / f"render_{pathlib.Path(path).stem}.npz"
    np.savez(npz, pts=pts[used], tri=tri, U=np.asarray(U)[used], s=np.asarray(s, dtype=float)[used], opt=json.dumps(opt))
    r = subprocess.run([sys.executable, str(RENDER), str(npz)], capture_output=True, text=True, timeout=900)
    if r.returncode != 0 or not pathlib.Path(path).exists():
        print(f"  render failed for {pathlib.Path(path).name} (exit {r.returncode}); results are unaffected\n{r.stderr[-800:]}")
    return scale


def part(parts, prefix):
    for p in parts:
        if p.name.startswith(prefix):
            return p
    raise KeyError(prefix)


# --------------------------------------------------------------------------------------------
# 4a  box lid on its gasket
# --------------------------------------------------------------------------------------------
def lindley(cs, shore, s):
    """Force per unit length (N/mm) to compress an O-ring cord of section cs (mm) by the fraction s (Lindley 1967, the formula
    PR 266's seals.py uses; E from Gent's hardness relation)."""
    E = 0.0981 * (56 + 7.62336 * shore) / (0.137505 * (254 - 2.54 * shore))
    return cs * E * (1.25 * s ** 1.5 + 50 * s ** 6), E


def lid_geometry():
    """CAD v2: the Saginaw SCE-16EL1208SSLP's own door is the lid (0.075 in. 304, a dished panel with a 5.5 mm return as
    drawn), on the box's poured-in-place gasket (8 x 4 mm, drawn on the body's lip, 4 mm in from the door's edge). It is
    held by one quarter-turn latch at the middle of the front (-y) edge and two concealed hinges at the back (+y) edge,
    both inside the gasket line (ft_vendor.saginaw_16el1208sslp). The window stack sits at P['win_c']['box'] and the
    layer camera's port ring (MK-19) at P['cam_xy'], each over a bore in the door."""
    xc, yc = P["deck_c"]
    t = P["box_t"]
    L = M.levels("FT-1")
    S_ = M.VEN.SAG
    dx, dy = S_["door"]
    gw, gh = S_["gasket"]
    iy = S_["out"][1] - 2 * t
    zr = L["roof_in"]                                              # the door's inner face
    g_out = (xc - dx / 2 + 4, xc + dx / 2 - 4, yc - dy / 2 + 4, yc + dy / 2 - 4)
    g_in = (g_out[0] + gw, g_out[1] - gw, g_out[2] + gw, g_out[3] - gw)
    ys = -iy / 2 + S_["lip"] + 8.0                                 # latch shaft (local y)
    yh = iy / 2 - S_["lip"]                                        # concealed hinges: leaf on the door's inner face
    wx, wy = P["win_c"]["box"]
    cam = M.camera_geometry("FT-1")["W"]
    return dict(xc=xc, yc=yc, t=t, zr=zr, ltop=zr + t, skirt_bot=L["rim"] + gh, g_out=g_out, g_in=g_in, gasket_w=gw,
                gasket_h=gh, door=(xc - dx / 2, xc + dx / 2, yc - dy / 2, yc + dy / 2), latch=(xc, yc + ys), latch_r=S_["latch_d"] / 2,
                hinges=[(xc + hx_ - 20.0, xc + hx_ + 20.0, yc + yh - 16.0, yc + yh - 1.0) for hx_ in S_["hinge_x"]],
                win=(wx, wy), cam=(cam[0], cam[1]), flange_ceiling=zr + t + 10 - 0.1 + 1.8, cam_top=zr + t + 7.0)


GASKETS = {
    # CAD v2: the box's own poured-in-place foam gasket, 8 mm wide x 4 mm, modelled as a closed-cell sponge squeezed 25 %
    # (1.0 mm, estimate). Its maker's compression data were not found, so two ASTM D1056 grades bracket it:
    # 2A2 (5-9 psi at 25 %: 7 psi = 0.048 MPa) and 2A4 (13-17 psi: 15 psi = 0.103 MPa).
    "foam_2a2": dict(label="poured foam gasket 8 x 4 mm as ASTM D1056 2A2 sponge (7 psi at 25 %), 25 % squeeze (1.0 mm)",
                     cs=4.0, cfd=7.0 * 0.006894757, s=0.25, rho=300.0),
    "foam_2a4": dict(label="poured foam gasket 8 x 4 mm as ASTM D1056 2A4 sponge (15 psi at 25 %), 25 % squeeze (1.0 mm)",
                     cs=4.0, cfd=15.0 * 0.006894757, s=0.25, rho=300.0),
}
# door return (the dished panel's skirt) as drawn (5.5 mm) and a deeper one for the sensitivity run (the maker's
# render shows a deeper formed return than the CAD envelope; its depth is not published)
DOOR_RETURN_DEEP = 20.0


SPRING_T = 10.0   # mm: the gasket's spring bed is a 10 mm layer on the drawn gasket's footprint, so the squeeze is a small strain
                  # (on a thin layer a 1 mm squeeze is a large strain, where NLGEOM's St. Venant-Kirchhoff material softens)


def gasket_props(gk, width):
    """Secant stiffness of the gasket per unit length (N/mm per mm) at its squeeze, and the equivalent modulus of a
    SPRING_T x width layer (nu = 0, a bed of springs)."""
    d0 = gk["s"] * gk["cs"]
    if "shore" in gk:
        fl, E = lindley(gk["cs"], gk["shore"], gk["s"])
    else:
        fl, E = gk["cfd"] * width, None
    kL = fl / d0
    E_eq = kL * SPRING_T / width
    return dict(squeeze_mm=d0, force_per_mm=fl, k_per_mm=kL, E_layer=E_eq, E_rubber=E)


def case4a_check(R):
    """A clamped 400 x 300 plate of the door's gauge at 1 kPa on the lid's mesh size, against Timoshenko's clamped-plate coefficient."""
    hmax = float(os.environ.get("FT_LID_HMAX", "7"))
    a, b, t = 400.0, 300.0, P["box_t"]
    shape = cq.Solid.makeBox(a, b, t, cq.Vector(-a / 2, -b / 2, 0))
    m = mesh_bodies([("plate", shape)], "c4a_check", hmax=hmax, hmin=1.0)
    edges = surfaces(m, lambda x0, y0, z0, x1, y1, z1: abs(x0 - x1) < E_TOL or abs(y0 - y1) < E_TOL)
    ids = nodes_on(m, edges)
    top = faces_on(m, surfaces(m, planar("z", t)))
    job = "c4a_check"
    mat = MAT["ss304"]
    write_model(job, m, [mat], nset("EDGE", ids))
    sol = solver_for(len(m["ntags"]))
    append(job, f"*STEP\n*STATIC, SOLVER={sol}\n*BOUNDARY\nEDGE,1,3\n*DLOAD\n" + dload_lines(top, 0.001) + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
    run_ccx(job)
    U, S, vm = step_results(m, job)[-1]
    c = m["idx"][nearest(m, (0, 0, t / 2))]
    D = mat["E"] * t ** 3 / (12 * (1 - mat["nu"] ** 2))
    # Timoshenko & Woinowsky-Krieger, Table 35 (clamped edges): alpha = 0.00191 at b/a... a/b = 1.3, 0.00207 at 1.4
    ab = a / b
    alpha = 0.00191 + (ab - 1.3) / 0.1 * (0.00207 - 0.00191)
    w_th = alpha * 0.001 * b ** 4 / D
    r = dict(case=f"4a-check: clamped 400 x 300 x {t:.3f} mm 304 plate at 1 kPa, lid mesh size", hmax=hmax,
             w_fe_mm=float(-U[c, 2]), w_timoshenko_mm=w_th, ratio=float(-U[c, 2] / w_th))
    stamp(r, m, sol, hmax=hmax)
    R["4a_check"] = r
    print(f"  4a-check: w FE {-U[c, 2]:.4f} mm vs Timoshenko {w_th:.4f} mm (ratio {r['ratio']:.3f})")


def door_shape(g, ret):
    """The door as a dished panel with a return of depth ret (mm) round its edge, the window and camera bores cut (the
    drawn door has ret = 5.5 mm; the drawn shape is used when ret is None)."""
    x0, x1, y0, y1 = g["door"]
    t, zr = g["t"], g["zr"]
    d = M.box(x0, x1, y0, y1, zr, zr + t).fuse(M.box(x0, x1, y0, y1, zr - ret, zr).cut(M.box(x0 + t, x1 - t, y0 + t, y1 - t, zr - ret - 1, zr + 1)))
    d = d.cut(M.cyl(26.5, (g["win"][0], g["win"][1], zr - 12), "z", 30)).cut(M.cyl(14.0, (g["cam"][0], g["cam"][1], zr - 12), "z", 30))
    return d


def case4a(R):
    g = lid_geometry()
    parts = M.build("FT-1")
    hmax = float(os.environ.get("FT_LID_HMAX", "7"))
    gi, go = g["g_in"], g["g_out"]
    z_gb = g["zr"] - SPRING_T                                     # the spring bed's fixed bottom (the body's lip, moved down)
    spring = M.box(go[0], go[1], go[2], go[3], z_gb, g["zr"]).cut(M.box(gi[0], gi[1], gi[2], gi[3], z_gb - 1, g["zr"] + 1))
    door_drawn = part(parts, "Box door (the lid)").shape
    configs = {"drawn": door_drawn}
    if os.environ.get("FT_LID_DEEP", "1") == "1":
        configs["deep_return"] = door_shape(g, DOOR_RETURN_DEEP)
    xc, yc = g["xc"], g["yc"]
    width = g["gasket_w"]
    cx0, cx1, cy0, cy1 = go[0] + width / 2, go[1] - width / 2, go[2] + width / 2, go[3] - width / 2
    Lx, Ly = cx1 - cx0, cy1 - cy0
    r_seal, r_cam = 23.7, 12.7
    sol = os.environ.get("FEA_SOLVER") or "SPOOLES"     # the soft gasket layer makes the PCG solver crawl; SPOOLES if it fits
    gas_todo = os.environ.get("FT_LID_GASKETS", ",".join(GASKETS)).split(",")
    out_cfg = {}
    for cname, door in configs.items():
        bodies = [("door", door), ("gasket spring bed", spring),
                  ("inner ring", part(parts, "Inner clamp ring (MK-02)").shape), ("window ring", part(parts, "Window ring (MK-02)").shape),
                  ("flange", part(parts, "Window retaining flange (MK-02)").shape),
                  ("camera port ring", part(parts, "Camera port ring").shape)]
        m = mesh_bodies(bodies, f"c4a_door_{cname}", hmax=hmax, hmin=1.0, curv=10)
        inside = lambda c: (c[:, 0] > gi[0]) & (c[:, 0] < gi[1]) & (c[:, 1] > gi[2]) & (c[:, 1] < gi[3])
        f_lid = faces_on(m, surfaces(m, planar("z", g["zr"])), inside)
        f_ring = faces_on(m, surfaces(m, planar("z", g["zr"] - 6.0)))
        f_ceil = faces_on(m, surfaces(m, planar("z", g["flange_ceiling"])))
        f_cam = faces_on(m, surfaces(m, planar("z", g["cam_top"])))
        a_ceil, a_cam = f_ceil["area"].sum(), f_cam["area"].sum()
        gb = nodes_on(m, surfaces(m, planar("z", z_gb)))
        q = m["xyz"]
        door_nodes = np.unique(m["idx"][m["tets"][m["body"] == 0]].ravel())
        in_door = np.zeros(len(q), bool)
        in_door[door_nodes] = True
        lx_, ly_ = g["latch"]
        latch = m["ntags"][in_door & (np.abs(q[:, 2] - g["ltop"]) < 1e-3) & (np.hypot(q[:, 0] - lx_, q[:, 1] - ly_) <= g["latch_r"])]
        hinges = {}
        for k, (hx0, hx1, hy0, hy1) in enumerate(g["hinges"]):
            hinges[f"HINGE{k + 1}"] = m["ntags"][in_door & (np.abs(q[:, 2] - g["zr"]) < 1e-3) & (q[:, 0] >= hx0) & (q[:, 0] <= hx1)
                                                 & (q[:, 1] >= hy0) & (q[:, 1] <= hy1)]
        print(f"  4a {cname}: latch {len(latch)} nodes, hinges {[len(v) for v in hinges.values()]}, gasket bottom {len(gb)}")
        band = ((q[:, 0] <= gi[0] + 1e-6) | (q[:, 0] >= gi[1] - 1e-6) | (q[:, 1] <= gi[2] + 1e-6) | (q[:, 1] >= gi[3] - 1e-6)) & \
               (q[:, 0] >= go[0] - 1e-6) & (q[:, 0] <= go[1] + 1e-6) & (q[:, 1] >= go[2] - 1e-6) & (q[:, 1] <= go[3] + 1e-6)
        gtop = np.nonzero(band & (np.abs(q[:, 2] - g["zr"]) < 1e-3))[0]
        seat = m["idx"][np.unique(f_ceil["tri"].ravel())]
        p = q[gtop]
        dist = np.stack([np.abs(p[:, 1] - cy0), np.abs(p[:, 0] - cx1), np.abs(p[:, 1] - cy1), np.abs(p[:, 0] - cx0)], 1)
        side = np.argmin(dist, 1)
        s_coord = np.where(side == 0, p[:, 0] - cx0, np.where(side == 1, Lx + p[:, 1] - cy0,
                           np.where(side == 2, Lx + Ly + cx1 - p[:, 0], 2 * Lx + Ly + cy1 - p[:, 1])))
        on_line = dist[np.arange(len(p)), side] <= 2.0
        s_sup = {"LATCH": lx_ - cx0, "HINGE1": Lx + Ly + cx1 - (g["hinges"][0][0] + 20.0), "HINGE2": Lx + Ly + cx1 - (g["hinges"][1][0] + 20.0)}
        A_p = f_lid["area"].sum() + f_ring["area"].sum()
        # nodes away from the idealised supports (30 mm from the latch's axis and from each hinge leaf)
        dmin = np.hypot(q[:, 0] - lx_, q[:, 1] - ly_)
        for (hx0, hx1, hy0, hy1) in g["hinges"]:
            dmin = np.minimum(dmin, np.hypot(np.maximum(np.maximum(hx0 - q[:, 0], q[:, 0] - hx1), 0), np.maximum(np.maximum(hy0 - q[:, 1], q[:, 1] - hy1), 0)))
        away = dmin > 30.0
        ring_zone = np.hypot(q[:, 0] - g["win"][0], q[:, 1] - g["win"][1]) <= 75.0
        set_names = ["LATCH"] + list(hinges)

        def profile(U):
            comp = -U[gtop, 2]
            sc, cc = s_coord[on_line], comp[on_line]
            nb = int(math.ceil((2 * Lx + 2 * Ly) / 5.0))
            bins = np.minimum((sc / 5.0).astype(int), nb - 1)
            prof = np.full(nb, np.nan)
            for b_ in np.unique(bins):
                prof[b_] = cc[bins == b_].mean()
            return prof

        out = {}
        for gname, gk in GASKETS.items():
            if gname not in gas_todo:
                continue
            if cname != "drawn" and gname != "foam_2a2":
                continue
            gp = gasket_props(gk, width)
            mats = [MAT["ss304"], dict(E=gp["E_layer"], nu=0.0, rho=gk["rho"]), MAT["al6061"], MAT["al6061"], MAT["al6061"], MAT["al6061"]]
            sets = nset("GBOT", gb) + nset("LATCH", latch) + "".join(nset(k, v) for k, v in hinges.items())
            d0 = gp["squeeze_mm"]
            bc = f"GBOT,3,3\nLATCH,3,3,{-d0}\n" + "".join(f"{k},1,2\n{k},3,3,{-d0}\n" for k in hinges)
            prints = "".join(f"*NODE PRINT, NSET={k}, TOTALS=ONLY\nRF\n" for k in set_names) + "*NODE PRINT, NSET=GBOT, TOTALS=ONLY\nRF\n"

            def loads(pr):
                if pr == 0:
                    return ""
                return ("*DLOAD, OP=NEW\n" + dload_lines(f_lid, pr) + dload_lines(f_ring, pr) + dload_lines(f_ceil, pr * math.pi * r_seal ** 2 / a_ceil)
                        + dload_lines(f_cam, -pr * math.pi * r_cam ** 2 / a_cam))

            job = f"c4a_door_{cname}_{gname}"
            write_model(job, m, mats, sets)
            txt = ""
            for pr in (0.0, 0.001, 0.005):
                txt += f"*STEP\n*STATIC, SOLVER={sol}\n*BOUNDARY\n{bc}" + loads(pr) + prints + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n"
            append(job, txt)
            t_lin = run_ccx(job)
            res = step_results(m, job)
            tot = read_totals(job)
            steps = {}
            lid_nodes = door_nodes
            ring_nodes = np.unique(m["idx"][m["tets"][m["body"] >= 2]].ravel())
            far = lid_nodes[away[lid_nodes]]
            for k, (tag, pr) in enumerate((("preload", 0.0), ("plus10mbar", 0.001), ("plus50mbar", 0.005))):
                U, S, vm = res[k]
                prof = profile(U)
                vm_lid = vm[lid_nodes]
                j = lid_nodes[int(np.argmax(vm_lid))]
                rf = {k2: tot.get((k2, k + 1)) for k2 in set_names + ["GBOT"]}
                steps[tag] = dict(p_MPa=pr, vm_lid_max=float(vm_lid.max()), vm_lid_max_at=m["xyz"][j].tolist(),
                                  vm_lid_p995=float(np.percentile(vm_lid, 99.5)), vm_ring_max=float(vm[ring_nodes].max()),
                                  vm_lid_away_max=float(vm[far].max()), vm_lid_away_at=m["xyz"][far[int(np.argmax(vm[far]))]].tolist(),
                                  vm_ring_zone_max=float(vm[lid_nodes[ring_zone[lid_nodes]]].max()),
                                  u_max_mm=float(np.linalg.norm(U, axis=1).max()),
                                  lid_uz_max_mm=float(U[lid_nodes, 2].max()), lid_uz_max_at=m["xyz"][lid_nodes[int(np.argmax(U[lid_nodes, 2]))]].tolist(),
                                  window_seat_uz_mm=float(U[seat, 2].mean()),
                                  gasket_comp_min_mm=float(np.nanmin(prof)), gasket_comp_max_mm=float(np.nanmax(prof)),
                                  gasket_comp_mean_mm=float(np.nanmean(prof)),
                                  gasket_comp_min_at_s=float(np.nanargmin(prof) * 5.0 + 2.5),
                                  gasket_open_length_mm=float(np.sum(prof < 0) * 5.0),
                                  gasket_below_half_length_mm=float(np.sum(prof < d0 / 2) * 5.0),
                                  reactions_N={k2: (None if v is None else [round(x, 2) for x in v]) for k2, v in rf.items()},
                                  profile=[None if np.isnan(x) else round(float(x), 4) for x in prof])
                if tag == "plus50mbar":
                    steps[tag]["_U"], steps[tag]["_vm"] = U, vm
            # NLGEOM at +50 mbar: preload then pressure, in increments
            job_nl = f"c4a_door_{cname}_{gname}_nl"
            write_model(job_nl, m, mats, sets)
            append(job_nl, f"*STEP, NLGEOM, INC=100\n*STATIC, SOLVER={sol}\n0.5,1.0,1e-4,1.0\n*BOUNDARY\n{bc}" + prints + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n"
                   + f"*STEP, NLGEOM, INC=100\n*STATIC, SOLVER={sol}\n0.25,1.0,1e-4,0.5\n" + loads(0.005) + prints + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
            try:
                t_nl = run_ccx(job_nl)
                U, S, vm = step_results(m, job_nl)[-1]
                prof = profile(U)
                tot = last_totals(read_totals(job_nl))
                nl = dict(vm_lid_max=float(vm[lid_nodes].max()), vm_lid_p995=float(np.percentile(vm[lid_nodes], 99.5)),
                          vm_lid_away_max=float(vm[far].max()), vm_lid_away_at=m["xyz"][far[int(np.argmax(vm[far]))]].tolist(),
                          vm_ring_zone_max=float(vm[lid_nodes[ring_zone[lid_nodes]]].max()),
                          lid_uz_max_mm=float(U[lid_nodes, 2].max()), window_seat_uz_mm=float(U[seat, 2].mean()),
                          gasket_comp_min_mm=float(np.nanmin(prof)), gasket_comp_mean_mm=float(np.nanmean(prof)),
                          gasket_open_length_mm=float(np.sum(prof < 0) * 5.0),
                          gasket_below_half_length_mm=float(np.sum(prof < d0 / 2) * 5.0),
                          reactions_N={k2: (None if tot.get(k2) is None else [round(x, 2) for x in tot.get(k2)]) for k2 in set_names + ["GBOT"]},
                          profile=[None if np.isnan(x) else round(float(x), 4) for x in prof], ccx_s=round(t_nl))
            except RuntimeError as e:
                print(f"  NLGEOM run failed: {str(e)[:400]}")
                nl = dict(error=str(e)[:400])
            U50, vm50 = steps["plus50mbar"].pop("_U"), steps["plus50mbar"].pop("_vm")
            out[gname] = dict(gasket=gk["label"], **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in gp.items()},
                              total_preload_N=gp["force_per_mm"] * 2 * (Lx + Ly), steps=steps, nlgeom_plus50mbar=nl, ccx_s=round(t_lin))
            if gname == "foam_2a2" and cname == "drawn":
                i = int(np.argmax(vm50))
                png = "struct-lid-v2.png"
                render(m, U50, vm50, OUT / png, f"4a (CAD v2): Saginaw door on its poured foam gasket (2A2), latch + 2 hinges, +50 mbar inside (linear)\n"
                       f"max von Mises {vm50.max():.0f} MPa", (-0.9, -1.4, 1.3), mark=m["xyz"][i], clim=(0, float(np.percentile(vm50, 99.5)) * 1.1))
                out[gname]["png"] = png
            print(f"  4a {cname} {gname}: preload {out[gname]['total_preload_N']:.0f} N; " + "; ".join(
                f"{k}: lid uz max {v['lid_uz_max_mm']:.3f} mm, vm away {v['vm_lid_away_max']:.0f} MPa, gasket comp min {v['gasket_comp_min_mm']:.3f} mm, open {v['gasket_open_length_mm']:.0f} mm"
                for k, v in steps.items()) + f"; NLGEOM +50: comp min {nl.get('gasket_comp_min_mm', float('nan')):.3f} mm, open {nl.get('gasket_open_length_mm', float('nan')):.0f} mm", flush=True)
        out_cfg[cname] = dict(gaskets=out, nodes=int(len(m["ntags"])), elements=int(len(m["tets"])), pressure_area_mm2=float(A_p),
                              door_return_mm=(g["zr"] - g["skirt_bot"]) if cname == "drawn" else DOOR_RETURN_DEEP)
    r = dict(case="4a (CAD v2) FT-1 box door (Saginaw SCE-16EL1208SSLP) on its poured gasket: latch and hinges closed, +10 mbar purge, +50 mbar fault",
             material="door: " + MAT["ss304"]["label"] + f" {g['t']:.3f} mm; rings: " + MAT["al6061"]["label"],
             window_seal_r_mm=r_seal, gasket_width_mm=width, perimeter_mm=2 * (Lx + Ly), support_s_mm=s_sup,
             sides_s_mm=dict(front=(0, Lx), right=(Lx, Lx + Ly), back=(Lx + Ly, 2 * Lx + Ly), left=(2 * Lx + Ly, 2 * Lx + 2 * Ly)),
             latch_xy=list(g["latch"]), hinge_patches=g["hinges"], window_xy=list(g["win"]), camera_port_xy=list(g["cam"]),
             supports="gasket bottom (the body's lip) fixed in z; the latch pulls a Ø25 patch of the door's top face down by the squeeze; "
                      "each concealed hinge holds its 40 x 15 mm leaf on the door's inner face in x and y and pulls it down by the squeeze",
             configs=out_cfg)
    A_p = out_cfg["drawn"]["pressure_area_mm2"]
    r["force_10mbar_N"] = 0.001 * A_p + 0.001 * math.pi * r_seal ** 2
    r["force_50mbar_N"] = 0.005 * A_p + 0.005 * math.pi * r_seal ** 2
    r["run"] = dict(utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=model_commit(), solver=sol, hmax=hmax,
                    nodes={k: v["nodes"] for k, v in out_cfg.items()})
    R["4a"] = r


# --------------------------------------------------------------------------------------------
# 4b  cube top plate and window
# --------------------------------------------------------------------------------------------
def roark_window(p, a, t, nu, E):
    D = E * t ** 3 / (12 * (1 - nu ** 2))
    return dict(ss_sigma=3 * (3 + nu) * p * a ** 2 / (8 * t ** 2), ss_w=p * a ** 4 * (5 + nu) / (64 * D * (1 + nu)),
                cl_sigma=3 * p * a ** 2 / (4 * t ** 2), cl_w=p * a ** 4 / (64 * D))


def case4b(R):
    parts = M.build("FT-1V")
    L = M.levels("FT-1V")
    xc, yc = P["deck_c"]
    sh = part(parts, "Cube top plate").shape
    m = mesh_bodies([("top plate", sh)], "c4b_plate", hmax=8.0, hmin=2.0, curv=10)
    pt, bs = P["cube_plate_t"], P["cube_boss"]
    z_top, z_land = L["roof_out"], L["roof_out"] - (pt - bs)
    op = P["cube_open"]
    top = surfaces(m, planar("z", z_top))
    land = surfaces(m, planar("z", z_land))
    rc = lambda c: np.hypot(c[:, 0], c[:, 1])
    f_top = faces_on(m, top)
    f_ring = faces_on(m, top, lambda c: (rc(c) >= 26.5) & (rc(c) <= 50.0))
    F_win = P_ATM * math.pi * 26.5 ** 2
    cheb = lambda q: np.maximum(np.abs(q[:, 0] - xc), np.abs(q[:, 1] - yc))
    clamped = nodes_on(m, land, lambda q: cheb(q) >= op / 2)
    ss = nodes_on(m, land, lambda q: (cheb(q) >= op / 2) & (cheb(q) <= op / 2 + 4.0))
    print(f"  4b supports: clamped {len(clamped)} nodes, simply supported band {len(ss)} nodes")
    pw = P["cube_plate"] / 2
    n1 = nearest(m, (xc + pw, yc + pw, z_land))
    n2 = nearest(m, (xc - pw, yc + pw, z_land))
    bore = m["idx"][nodes_on(m, top, lambda q: rc(q) <= 27.0)]
    out = {}
    for tag, ids in (("clamped", clamped), ("simply_supported", ss)):
        job = f"c4b_plate_{tag}"
        write_model(job, m, [MAT["al6061"]], nset("LAND", ids))
        sol = solver_for(len(m["ntags"]))
        append(job, f"*STEP\n*STATIC, SOLVER={sol}\n*BOUNDARY\nLAND,3,3\n{n1},1,2\n{n2},2,2\n*DLOAD\n" + dload_lines(f_top, P_ATM)
               + dload_lines(f_ring, F_win / f_ring["area"].sum()) + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
        run_ccx(job)
        U, S, vm = step_results(m, job)[-1]
        i = int(np.argmax(vm))
        out[tag] = dict(u_max_mm=float(np.abs(U[:, 2]).max()), u_max_at=m["xyz"][int(np.argmax(np.abs(U[:, 2])))].tolist(),
                        bore_uz_mm=float(U[bore, 2].mean()), vm_max=float(vm[i]), vm_max_at=m["xyz"][i].tolist(),
                        vm_p995=float(np.percentile(vm, 99.5)), sf_yield=MAT["al6061"]["sy"] / float(vm[i]))
        print(f"  4b plate {tag}: u max {out[tag]['u_max_mm'] * 1000:.1f} um, bore {out[tag]['bore_uz_mm'] * 1000:.1f} um, vm {vm[i]:.1f} MPa")
    # Roark check: clamped / simply supported square plate of side = the frame opening, the full 22.9 mm thick
    a = op
    D = MAT["al6061"]["E"] * pt ** 3 / (12 * (1 - MAT["al6061"]["nu"] ** 2))
    roark = dict(side_mm=a, t_mm=pt, ss_w_mm=0.00406 * P_ATM * a ** 4 / D, cl_w_mm=0.00126 * P_ATM * a ** 4 / D,
                 ss_sigma=0.2874 * P_ATM * a ** 2 / pt ** 2, cl_sigma=0.3078 * P_ATM * a ** 2 / pt ** 2)
    plate = dict(load=f"{P_ATM} MPa on the outer face; the window ring's {F_win:.0f} N spread round the bore (r 26.5-50 mm)",
                 supports="clamped: z fixed on the land outside the frame opening (bolted flange); simply supported: z fixed on a 4 mm band at the opening's edge; two corners pinned in-plane",
                 frame_opening_mm_est=op, roark_square_plate=roark, **out)
    stamp(plate, m, solver_for(len(m["ntags"])), hmax=8.0)
    # window
    fs = MAT["fused_silica"]
    r0, t, ru = P["window_d"] / 2, P["window_t"], 23.7
    shape = cq.Solid.makeCylinder(r0, t, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
    mw = mesh_bodies([("window", shape)], "c4b_window", hmax=2.0, hmin=0.6)
    wt = surfaces(mw, planar("z", t))
    wb = surfaces(mw, planar("z", 0.0))
    ring = nodes_on(mw, wb, lambda q: np.abs(np.hypot(q[:, 0], q[:, 1]) - ru) <= 0.6)
    c0 = nearest(mw, (0, 0, 0))
    c1 = nearest(mw, (ru, 0, 0), ring)
    job = "c4b_window"
    write_model(job, mw, [fs], nset("RING", ring))
    sol = solver_for(len(mw["ntags"]))
    append(job, f"*STEP\n*STATIC, SOLVER={sol}\n*BOUNDARY\nRING,3,3\n{c0},1,2\n{c1},2,2\n*DLOAD\n" + dload_lines(faces_on(mw, wt), P_ATM)
           + "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
    run_ccx(job)
    U, S, vm = step_results(mw, job)[-1]
    s1 = principal_max(S)
    i = int(np.argmax(s1))
    ro = roark_window(P_ATM, ru, t, fs["nu"], fs["E"])
    ro_edge = roark_window(P_ATM, r0, t, fs["nu"], fs["E"])
    win = dict(window=f"Ø{2 * r0} x {t} mm fused silica (Edmund 38-990)", seat_r_mm=ru,
               seat="O-ring on the window ring's ledge (r 22.0-25.65 mm as drawn): support circle at its middle, r = 23.7 mm",
               fe_s1_max_MPa=float(s1[i]), fe_s1_at=mw["xyz"][i].tolist(), fe_u_max_um=float(np.linalg.norm(U, axis=1).max() * 1000),
               roark_at_seat=ro, roark_at_edge_r25_4=ro_edge, mor_MPa=fs["mor"], design_MPa=fs["design"],
               sf_mor_fe=fs["mor"] / float(s1[i]), sf_design_fe=fs["design"] / float(s1[i]),
               box_plus50mbar=dict(s1_MPa=float(s1[i]) * 0.005 / P_ATM, sf_design=fs["design"] / (float(s1[i]) * 0.005 / P_ATM)))
    stamp(win, mw, sol, hmax=2.0)
    R["4b"] = dict(case="4b FT-1V: cube top plate MK-13 and the window at 1 atm", material=MAT["al6061"]["label"] + "; " + fs["label"],
                   plate=plate, window=win)
    print(f"  4b window: s1 {s1[i]:.3f} MPa (Roark SS {ro['ss_sigma']:.3f}, clamped {ro['cl_sigma']:.3f}); SF {fs['mor'] / s1[i]:.0f} vs MOR, {fs['design'] / s1[i]:.1f} vs 6.9 MPa")


# --------------------------------------------------------------------------------------------
# 4c  scan-head plate on the T-slot gantry
# --------------------------------------------------------------------------------------------
I_TSLOT = 27000.0      # mm4, 30 mm 8-slot profile: catalogues give 2.6-2.8 cm4 (estimate; McMaster's 5537T101 page was not read)


def tslot_section():
    """Area and second moment of the model's 30 mm T-slot drawing (lpbf_model._tslot_sketch), from OCC, about the profile's
    centre (each piece's own moment plus A d^2). The drawing's four corner pieces are cut off from the core by its undercuts,
    so it is not a load-bearing section: its area sets the mass per length, I_TSLOT sets the stiffness."""
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from lpbf_model import _tslot_sketch
    faces = _tslot_sketch()._faces.Faces()
    A = Ixx = 0.0
    for f in faces:
        g = GProp_GProps()
        BRepGProp.SurfaceProperties_s(f.wrapped, g)
        a, c = g.Mass(), g.CentreOfMass()
        A += a
        Ixx += g.MatrixOfInertia().Value(1, 1) + a * c.Y() ** 2
    return dict(A=A, Ixx_drawing=Ixx, pieces=len(faces), Ixx=I_TSLOT)


def equivalent_tube(I, A_real, s=30.0):
    """Square tube s x s with the same second moment I: wall t, its area and Bredt torsion constant."""
    inner = (s ** 4 - 12 * I) ** 0.25
    t = (s - inner) / 2
    A = s ** 2 - inner ** 2
    am = (s - t) ** 2
    J = 4 * am ** 2 * t / (4 * (s - t))
    return dict(t=t, A=A, J=J, rho_scale=A_real / A)


def rigid_fit(m, U, ids, c):
    """Translation (at point c) and small rotation of the rigid footprint nodes ids, by least squares on u = u0 + theta x r."""
    rows = m["idx"][ids]
    r = m["xyz"][rows] - np.asarray(c)
    n = len(rows)
    A = np.zeros((3 * n, 6))
    for k in range(3):
        A[k::3, k] = 1.0
    # theta x r = [ty*rz - tz*ry, tz*rx - tx*rz, tx*ry - ty*rx]
    A[0::3, 4], A[0::3, 5] = r[:, 2], -r[:, 1]
    A[1::3, 3], A[1::3, 5] = -r[:, 2], r[:, 0]
    A[2::3, 3], A[2::3, 4] = r[:, 1], -r[:, 0]
    sol, *_ = np.linalg.lstsq(A, U[rows].ravel(), rcond=None)
    return sol[:3], sol[3:]


def tube_box(x0, x1, y0, y1, z0, z1, t, axis):
    b = cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))
    if axis == "x":
        h = cq.Solid.makeBox(x1 - x0 + 2, y1 - y0 - 2 * t, z1 - z0 - 2 * t, cq.Vector(x0 - 1, y0 + t, z0 + t))
    else:
        h = cq.Solid.makeBox(x1 - x0 - 2 * t, y1 - y0 - 2 * t, z1 - z0 + 2, cq.Vector(x0 + t, y0 + t, z0 - 1))
    return b.cut(h)


BRACE_TOP_Z = 330.0       # braced variant: brace from the upright's centre line at this height ...
BRACE_FOOT_Z = -49.6      # ... down to 15 mm above the front support rail's top (z = -64.6), at y = the front rail

# The scan head and objective (the lead's update of 2026-11-27, from the makers' datasheets): SCANLAB's standard hurrySCAN
# 20/30 housing, 206.9 x 140 x 180 mm (along the beam's entrance axis x, across y, tall z), 5.8 kg without objective; the LINOS
# F-Theta-Ronar f = 254 mm objective, 1.34 kg, its flange 348.1 mm above the bed and the head's bottom face on that flange.
# The head and lens move 30 mm toward -Y (the back-reflection fix), so the head plate grows 30 mm further out from the same
# cross-beam. The CAD model is being redrawn with the head hung from a bracket on its entrance face; until then the head is
# placed here on the model's lens axis moved to AXIS_Y.
HEAD = dict(size=(206.9, 140.0, 180.0), mass=5.8, src="SCANLAB hurrySCAN 20/30 standard housing datasheet (without objective)")
LENS = dict(mass=1.34, flange_z=348.1, src="LINOS F-Theta-Ronar f = 254 mm datasheet")
AXIS_Y = -30.0
I_TSLOT45, A_TSLOT45 = 140000.0, 700.0   # 45 mm 8-slot profile: catalogue-typical second moment and area (estimates)
VARIANTS = ("drawn", "braced", "four_post", "four_post_braced", "four_post_braced_45")


def gantry_case(variant):
    """Head plate MK-09 + gantry with the head and lens as one rigid mass.
    'drawn': the model's frame (a 30 mm cross-beam on two 30 mm uprights, the plate cantilevered from it);
    'braced': a 30 x 60 cross-beam (60 tall) and one diagonal 30 mm brace per upright down to the front support rail;
    'four_post': the plate's front edge on a second 30 mm cross-beam under it, on two more uprights;
    'four_post_braced': four posts + a diagonal per side (front post's top to back post's base) + two knee braces at the back;
    'four_post_braced_45': the same with 45 mm posts."""
    parts = M.build("FT-1")
    L = M.levels("FT-1")
    sec = tslot_section()
    eq = equivalent_tube(sec["Ixx"], sec["A"])
    t = eq["t"]
    plate0 = part(parts, "Scan-head plate (MK-09)").shape
    lbb = part(parts, "f-theta lens").shape.BoundingBox()
    shift = AXIS_Y - (lbb.ymin + lbb.ymax) / 2              # 0 once the CAD model carries the 30 mm move
    bbp = plate0.BoundingBox()
    hb = bbp.zmax                                             # the plate's top face
    y_ax = AXIS_Y
    hl, hwid, hh = HEAD["size"]
    r_lens = P["lens_d"] / 2
    bb_b = part(parts, "Gantry cross-beam").shape.BoundingBox()
    bb_u = part(parts, "Gantry uprights").shape.BoundingBox()
    ux = (bb_u.xmin + 15.0, bb_u.xmax - 15.0)
    yu = (bb_u.ymin + bb_u.ymax) / 2
    y_front = P["deck_c"][1] - 115.0                          # the front base and support rails (ft_model: ry[0])
    four = variant.startswith("four_post")
    if four:
        # front beam 10 mm clear of the lens housing and 5 mm clear of the head's front face; plate 5 mm past the beam
        fb_y1 = min(y_ax - r_lens - 10.0, y_ax - hwid / 2 - 5.0)
        fb_y0 = fb_y1 - 30.0
        y_plate0 = fb_y0 - 5.0
    else:
        y_plate0 = bbp.ymin + shift
    plate = cq.Solid.makeBox(bbp.xlen, bbp.ymax - y_plate0, bbp.zlen, cq.Vector(bbp.xmin, y_plate0, bbp.zmin)).cut(
        cq.Solid.makeCylinder(r_lens + 3, bbp.zlen + 2, cq.Vector(0, y_ax, bbp.zmin - 1), cq.Vector(0, 0, 1)))
    al = MAT["al6061"]
    frame = dict(al, rho=al["rho"] * eq["rho_scale"])
    heavy = variant.endswith("_45")
    if heavy:
        eq45 = equivalent_tube(I_TSLOT45, A_TSLOT45, s=45.0)
        post_s, post_t, post_mat = 45.0, eq45["t"], dict(al, rho=al["rho"] * eq45["rho_scale"])
    else:
        eq45 = None
        post_s, post_t, post_mat = 30.0, t, frame
    hs = post_s / 2
    ups = [tube_box(x - hs, x + hs, yu - hs, yu + hs, bb_u.zmin, bb_u.zmax, post_t, "z") for x in ux]
    r_in = (30.0 ** 4 - 64 * I_TSLOT / math.pi) ** 0.25 / 2      # round 30 mm brace tube with the T-slot's I

    def rtube(p0, p1):
        A_, B_ = cq.Vector(*p0), cq.Vector(*p1)
        d_ = B_ - A_
        return cq.Solid.makeCylinder(15.0, d_.Length, A_, d_.normalized()).cut(cq.Solid.makeCylinder(r_in, d_.Length, A_, d_.normalized()))
    braces = []
    if variant == "braced":
        beam = tube_box(bb_b.xmin, bb_b.xmax, bb_b.ymin, bb_b.ymax, bb_b.zmin, bb_b.zmin + 60.0, t, "x")
        a60 = 30 * 60 - (30 - 2 * t) * (60 - 2 * t)
        beam_mat = dict(al, rho=al["rho"] * 2 * sec["A"] / a60)
        for k, x in enumerate(ux):
            A_ = cq.Vector(x, yu, BRACE_TOP_Z)
            B_ = cq.Vector(x, y_front, BRACE_FOOT_Z)
            d = B_ - A_
            ups[k] = ups[k].fuse(rtube((x, yu, BRACE_TOP_Z), (x, y_front, BRACE_FOOT_Z))).clean()
            braces.append((np.array([x, y_front, BRACE_FOOT_Z]), np.array([d.x, d.y, d.z]) / d.Length))
    else:
        beam = tube_box(bb_b.xmin, bb_b.xmax, bb_b.ymin, bb_b.ymax, bb_b.zmin, bb_b.zmax, t, "x")
        beam_mat = frame
    bodies = [("head plate", plate), ("cross-beam", beam), ("upright L", ups[0]), ("upright R", ups[1])]
    mats = [al, beam_mat, post_mat, post_mat]
    yf = None
    if four:
        yf = (fb_y0 + fb_y1) / 2
        fb = tube_box(bb_b.xmin, bb_b.xmax, fb_y0, fb_y1, hb - 12 - 30, hb - 12, t, "x")
        fu = [tube_box(x - hs, x + hs, yf - hs, yf + hs, bb_u.zmin, hb - 12, post_t, "z") for x in ux]
        if variant != "four_post":
            zc_b = (bb_b.zmin + bb_b.zmax) / 2
            for k, x in enumerate(ux):
                inboard = 110.0 if k == 0 else -110.0
                ups[k] = ups[k].fuse(rtube((x, yu, -40.0), (x, yf, 340.0))).fuse(rtube((x, yu, 260.0), (x + inboard, yu, zc_b))).clean()
        bodies = [("head plate", plate), ("cross-beam", beam), ("upright L", ups[0]), ("upright R", ups[1]), ("front beam", fb),
                  ("front upright L", fu[0]), ("front upright R", fu[1])]
        mats = [al, beam_mat, post_mat, post_mat, frame, post_mat, post_mat]
    hmax = float(os.environ.get("FT_GANTRY_HMAX", "8"))
    m = mesh_bodies(bodies, f"c4c_{variant}", hmax=hmax, hmin=1.5, curv=8)
    m_head, m_lens = HEAD["mass"], LENS["mass"]
    z_head = LENS["flange_z"] + hh / 2                        # mid-height of the 180 mm housing above the lens flange
    z_lens = (LENS["flange_z"] + L["lens_bot"]) / 2            # midway between the flange and the lens's bottom (est.)
    cm = (0.0, y_ax, (m_head * z_head + m_lens * z_lens) / (m_head + m_lens))
    mass_t = (m_head + m_lens) * 1e-3
    top = surfaces(m, planar("z", hb))
    foot = nodes_on(m, top, lambda q: (np.abs(q[:, 0]) <= hl / 2) & (np.abs(q[:, 1] - y_ax) <= hwid / 2)
                    & (np.hypot(q[:, 0], q[:, 1] - y_ax) > r_lens + 3 + 0.5))
    feet = nodes_on(m, surfaces(m, planar("z", bb_u.zmin)))
    for bp, bd in braces:                                     # brace feet: the end ring, bolted to the rail with a bracket
        rel = m["xyz"] - bp
        s_ax = rel @ bd
        rad = np.linalg.norm(rel - np.outer(s_ax, bd), axis=1)
        feet = np.union1d(feet, m["ntags"][(np.abs(s_ax) < 0.3) & (rad < 15.2)])
    nmax = int(m["ntags"].max())
    ref, rot = nmax + 1, nmax + 2
    eid = len(m["tets"]) + 1
    extra = (f"*NODE, NSET=REFS\n{ref},{cm[0]},{cm[1]},{cm[2]}\n{rot},{cm[0]},{cm[1]},{cm[2]}\n" + nset("FOOT", foot) + nset("FEET", feet)
             + f"*RIGID BODY, NSET=FOOT, REF NODE={ref}, ROT NODE={rot}\n*ELEMENT, TYPE=MASS, ELSET=MHEAD\n{eid},{ref}\n*MASS, ELSET=MHEAD\n{mass_t}\n")
    job = f"c4c_{variant}_gravity"
    write_model(job, m, mats, extra)
    sol = "SPOOLES"
    append(job, f"*STEP\n*STATIC, SOLVER={sol}\n*BOUNDARY\nFEET,1,3\n*DLOAD\nEALL,GRAV,9810.,0.,0.,-1.\n*CLOAD\n{ref},3,{-mass_t * G:.6g}\n"
           "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
    t_s = run_ccx(job)
    b = read_frd(job)
    D = [x for x in b if x["name"] == "DISP"][-1]
    Ss = [x for x in b if x["name"] == "STRESS"][-1]
    vm = von_mises(field(m, Ss, 6))
    U = field(m, D, 3)
    u_ref, th = rigid_fit(m, U, foot, cm)
    bed = np.array([0.0, y_ax, 0.0])

    def rigid_point(pt):
        return np.asarray(u_ref) + np.cross(th, np.asarray(pt) - np.asarray(cm))
    u_lens = rigid_point((0, y_ax, L["lens_bot"]))
    u_bed = rigid_point(bed)
    grav = dict(head_ref_u_um=(np.asarray(u_ref) * 1000).round(2).tolist(), tilt_urad=(np.asarray(th) * 1e6).round(1).tolist(),
                lens_u_um=(u_lens * 1000).round(2).tolist(), beam_error_at_bed_um=(u_bed[:2] * 1000).round(1).tolist(),
                focus_shift_um=float(u_bed[2] * 1000), vm_max=float(vm.max()), u_max_um=float(np.linalg.norm(U, axis=1).max() * 1000))
    print(f"  4c {variant} gravity: tilt {grav['tilt_urad']} urad, lens {grav['lens_u_um']} um, beam error at bed {grav['beam_error_at_bed_um']} um")
    job = f"c4c_{variant}_modal"
    write_model(job, m, mats, extra)
    append(job, "*BOUNDARY\nFEET,1,3\n*STEP\n*FREQUENCY, SOLVER=SPOOLES\n6\n*NODE FILE\nU\n*END STEP\n")
    t_m = run_ccx(job)
    f = read_freqs(job)
    modes = []
    blocks = [x for x in read_frd(job) if x["name"] == "DISP"]
    names = ("x (along the cross-beam)", "y (fore-aft)", "z (vertical)")
    for k, blk in enumerate(blocks[:6]):
        Um = field(m, blk, 3)
        ur, tr = rigid_fit(m, Um, foot, cm)
        mag = np.linalg.norm(Um, axis=1)
        jmax = int(np.argmax(mag))
        ub = np.asarray(ur) + np.cross(tr, bed - np.asarray(cm))     # the bed point carried by the head
        modes.append(dict(f_hz=f[k] if k < len(f) else None, head_translation_dir=(np.asarray(ur) / (np.linalg.norm(ur) + 1e-30)).round(2).tolist(),
                          head_rotation_dir=(np.asarray(tr) / (np.linalg.norm(tr) + 1e-30)).round(2).tolist(),
                          rot_per_mm_head_translation=float(np.linalg.norm(tr) / (np.linalg.norm(ur) + 1e-30)),
                          bed_motion_dir=(ub[:2] / (np.linalg.norm(ub[:2]) + 1e-30)).round(2).tolist(),
                          max_at=m["xyz"][jmax].round(0).tolist(), dominant_head_axis=names[int(np.argmax(np.abs(ur)))]))
        if k == 0 and variant == "drawn":
            render(m, Um, mag / mag.max(), OUT / "struct-gantry-mode1.png",
                   f"4c: head plate MK-09 on the T-slot gantry as drawn, mode 1 = {f[0]:.0f} Hz\n"
                   f"hurrySCAN 20/30 5.8 kg + LINOS objective 1.34 kg (datasheets) as one rigid mass, 30 mm toward -Y",
                   (-1.2, -1.6, 0.8), label="|u| (normalised)", scale=nice(60.0 / mag.max()), zoom=1.1, cmap="viridis")
    print(f"  4c {variant} modes: {[round(x, 1) for x in f]} Hz")
    r = dict(variant=variant, gravity=grav, modes=modes, ccx_s=dict(gravity=round(t_s), modal=round(t_m)),
             masses_kg=dict(head=m_head, lens=m_lens, cm_mm=[round(c_, 1) for c_ in cm], head_src=HEAD["src"], lens_src=LENS["src"],
                            note="one rigid body on the head's 206.9 x 140 mm footprint on the plate; head CoM at mid-height of its housing "
                                 "above the lens flange, lens CoM midway between the flange and the lens's bottom"),
             axis_y_mm=y_ax, model_shift_applied_mm=shift, plate_y_mm=[y_plate0, bbp.ymax], front_beam_y_mm=[fb_y0, fb_y1] if four else None,
             front_posts_y_mm=yf, posts=dict(size_mm=post_s, wall_mm=post_t, I_mm4=(I_TSLOT45 if heavy else I_TSLOT)),
             upright_x_mm=list(ux), upright_z_mm=[bb_u.zmin, bb_u.zmax], beam_x_mm=[bb_b.xmin, bb_b.xmax],
             beam_z_mm=[bb_b.zmin, bb_b.zmin + (60.0 if variant == "braced" else 30.0)],
             braces=[dict(foot=bp.round(1).tolist(), top=[float(bp[0]), yu, BRACE_TOP_Z]) for bp, _ in braces],
             tslot_section=dict(A_drawing_mm2=sec["A"], I_drawing_mm4=sec["Ixx_drawing"], pieces_in_drawing=sec["pieces"], I_used_mm4=sec["Ixx"]),
             equivalent_tube=dict(wall_mm=eq["t"], A_mm2=eq["A"], J_bredt_mm4=eq["J"], density_scale=eq["rho_scale"]),
             equivalent_tube_45=None if eq45 is None else dict(wall_mm=eq45["t"], A_mm2=eq45["A"], J_bredt_mm4=eq45["J"], density_scale=eq45["rho_scale"]))
    r["pass"] = bool(f and f[0] > 60)
    r["pass100"] = bool(f and f[0] > 100)
    stamp(r, m, "SPOOLES", hmax=hmax)
    return r


def case4c(R):
    todo = os.environ.get("FT_GANTRY_VARIANTS", ",".join(VARIANTS)).split(",")
    prev = R.get("4c", {}).get("variants", {})
    out = {v: (gantry_case(v) if v in todo else prev[v]) for v in VARIANTS if v in todo or v in prev}
    R["4c"] = dict(case="4c scan-head plate MK-09 + T-slot gantry, gravity and modes, hurrySCAN 20/30 housing and LINOS objective",
                   material=MAT["al6061"]["label"], head=HEAD, lens=LENS, axis_y_mm=AXIS_Y,
                   head_operating_range_C="25 +- 10 (15-35)",
                   criterion="first mode > 100 Hz (60 Hz minimum), as PR 266's optics bridge (fea.py case 6)", png="struct-gantry-mode1.png",
                   variants=out)


def gantry_model_case(gantry=None):
    """4c on the frame as the CAD model draws it (P['gantry'] = 'four_post'): four 45 mm posts, 30 mm front and back
    cross-beams, a diagonal per side (front post's top to the back post's foot) and two knee braces at the back, and the
    head hung by its entrance face from the flange plate MK-09 between the beams, with its angle brackets. Posts and
    beams are equivalent tubes at the drawn positions; braces are round 30 mm tubes on the drawn axes (centre of mass +
    principal axis of each brace solid), run 20 mm into the members they meet so that they bond; the diagonals' lower
    ends run on to the back posts' front face at the foot and are held there (bolted to the base rail). The head (5.8 kg)
    and lens (1.34 kg) are one rigid mass on the flange's face under the head's footprint. gantry: ft_model's
    P['gantry'] option to draw (None = the model's default); 'four_post_braced_front' adds the front knee braces, the
    head plate's top flange on both cross-beams and its three gussets, which are taken as drawn."""
    g_old = M.P.get("gantry")
    if gantry:
        M.P["gantry"] = gantry
    try:
        parts = M.build("FT-1")
    finally:
        M.P["gantry"] = g_old
    L = M.levels("FT-1")
    sec = tslot_section()
    eq = equivalent_tube(sec["Ixx"], sec["A"])
    eq45 = equivalent_tube(I_TSLOT45, A_TSLOT45, s=45.0)
    al = MAT["al6061"]
    frame30 = dict(al, rho=al["rho"] * eq["rho_scale"])
    frame45 = dict(al, rho=al["rho"] * eq45["rho_scale"])
    posts = []
    for s_ in part(parts, "Gantry uprights").shape.Solids():
        bb = s_.BoundingBox()
        c = ((bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2)
        for g_ in posts:
            if abs(g_["c"][0] - c[0]) < 40 and abs(g_["c"][1] - c[1]) < 40:
                b_ = g_["bb"]
                g_["bb"] = [min(b_[0], bb.xmin), max(b_[1], bb.xmax), min(b_[2], bb.ymin), max(b_[3], bb.ymax), min(b_[4], bb.zmin), max(b_[5], bb.zmax)]
                break
        else:
            posts.append(dict(c=c, bb=[bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]))
    assert len(posts) == 4, len(posts)
    bodies, mats = [], []
    for k, g_ in enumerate(posts):
        bodies.append((f"post {k}", tube_box(*g_["bb"], eq45["t"], "z")))
        mats.append(frame45)
    for nm, tag in (("Gantry cross-beam (clamped", "back beam"), ("Gantry cross-beam, front", "front beam")):
        bb = part(parts, nm).shape.BoundingBox()
        bodies.append((tag, tube_box(bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax, eq["t"], "x")))
        mats.append(frame30)
    r_in = (30.0 ** 4 - 64 * I_TSLOT / math.pi) ** 0.25 / 2
    braces, held = [], []
    back_front_face = min(g_["bb"][2] for g_ in posts if g_["c"][1] > 0)       # y of the back posts' front face
    brace_solids = list(part(parts, "Gantry braces").shape.Solids())
    if any(p_.name.startswith("Gantry knee braces, front") for p_ in parts):
        brace_solids += list(part(parts, "Gantry knee braces, front").shape.Solids())
    for k, s_ in enumerate(brace_solids):
        V = np.array([v.toTuple() for v in s_.Vertices()])
        C = np.array(s_.Center().toTuple())
        d = np.linalg.svd(V - V.mean(0))[2][0]
        pr = (V - C) @ d
        e0, e1 = C + pr.min() * d, C + pr.max() * d
        if e0[2] > e1[2]:
            e0, e1 = e1, e0
        d = (e1 - e0) / np.linalg.norm(e1 - e0)
        if np.linalg.norm(e1 - e0) > 400:                                  # diagonal: foot at the back post's front face
            t_ = (back_front_face - e0[1]) / d[1] if abs(d[1]) > 1e-6 else 0.0
            p0 = e0 + min(t_, 0.0) * d if t_ < 0 else e0 - 20.0 * d
            held.append((p0.copy(), d.copy()))
        else:
            p0 = e0 - 20.0 * d
        p1 = e1 + 20.0 * d
        A_, B_ = cq.Vector(*p0), cq.Vector(*p1)
        dd = B_ - A_
        tube = cq.Solid.makeCylinder(15.0, dd.Length, A_, dd.normalized()).cut(cq.Solid.makeCylinder(r_in, dd.Length, A_, dd.normalized()))
        bodies.append((f"brace {k}", tube))
        mats.append(frame30)
        braces.append(dict(p0=p0.round(1).tolist(), p1=p1.round(1).tolist(), drawn=[e0.round(1).tolist(), e1.round(1).tolist()]))
    fl = part(parts, "Scan-head flange plate (MK-09)").shape
    bodies += [("flange plate", fl), ("angle brackets", part(parts, "Flange-to-beam angle brackets (MK-09)").shape)]
    mats += [al, al]
    extras_drawn = []
    for nm in ("Head-plate top flange", "Head-plate gussets", "Head far-side support plate", "Far-side support angle brackets"):
        if any(p_.name.startswith(nm) for p_ in parts):
            bodies.append((nm, part(parts, nm).shape))
            mats.append(al)
            extras_drawn.append(nm)
    hmax = float(os.environ.get("FT_GANTRY_HMAX", "8"))
    m = mesh_bodies(bodies, f"c4c_model_{gantry or 'default'}", hmax=hmax, hmin=1.5, curv=8)
    hbb = part(parts, "SCANLAB hurrySCAN").shape.BoundingBox()
    fbb = fl.BoundingBox()
    ax_xy = P["axis_off"]
    m_head, m_lens = HEAD["mass"], LENS["mass"]
    c_head = np.array([(hbb.xmin + hbb.xmax) / 2, (hbb.ymin + hbb.ymax) / 2, (hbb.zmin + hbb.zmax) / 2])
    c_lens = np.array([ax_xy[0], ax_xy[1], (LENS["flange_z"] + L["lens_bot"]) / 2])
    cm = tuple(((m_head * c_head + m_lens * c_lens) / (m_head + m_lens)).tolist())
    mass_t = (m_head + m_lens) * 1e-3
    face = surfaces(m, planar("x", fbb.xmax))
    foot = nodes_on(m, face, lambda q: (q[:, 1] >= hbb.ymin) & (q[:, 1] <= hbb.ymax) & (q[:, 2] >= max(hbb.zmin, fbb.zmin)))
    if any(p_.name.startswith("Head far-side support plate") for p_ in parts):     # g3: the head's far face on its own plate
        xb_ = part(parts, "Head far-side support plate").shape.BoundingBox()
        foot = np.union1d(foot, nodes_on(m, surfaces(m, planar("x", xb_.xmin)),
                                         lambda q: (q[:, 1] >= hbb.ymin) & (q[:, 1] <= hbb.ymax) & (q[:, 2] >= max(hbb.zmin, xb_.zmin))))
    feet = np.array([], dtype=int)
    for zb in sorted({round(g_["bb"][4], 3) for g_ in posts}):
        feet = np.union1d(feet, nodes_on(m, surfaces(m, planar("z", zb))))
    for bp, bd in held:
        rel = m["xyz"] - bp
        s_ax = rel @ bd
        rad = np.linalg.norm(rel - np.outer(s_ax, bd), axis=1)
        feet = np.union1d(feet, m["ntags"][(np.abs(s_ax) < 0.3) & (rad < 15.2)])
    nmax = int(m["ntags"].max())
    ref, rot = nmax + 1, nmax + 2
    eid = len(m["tets"]) + 1
    extra = (f"*NODE, NSET=REFS\n{ref},{cm[0]},{cm[1]},{cm[2]}\n{rot},{cm[0]},{cm[1]},{cm[2]}\n" + nset("FOOT", foot) + nset("FEET", feet)
             + f"*RIGID BODY, NSET=FOOT, REF NODE={ref}, ROT NODE={rot}\n*ELEMENT, TYPE=MASS, ELSET=MHEAD\n{eid},{ref}\n*MASS, ELSET=MHEAD\n{mass_t}\n")
    job = f"c4c_model_{gantry or 'default'}_gravity"
    write_model(job, m, mats, extra)
    append(job, f"*STEP\n*STATIC, SOLVER=SPOOLES\n*BOUNDARY\nFEET,1,3\n*DLOAD\nEALL,GRAV,9810.,0.,0.,-1.\n*CLOAD\n{ref},3,{-mass_t * G:.6g}\n"
           "*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
    t_s = run_ccx(job)
    b = read_frd(job)
    D = [x for x in b if x["name"] == "DISP"][-1]
    Ss = [x for x in b if x["name"] == "STRESS"][-1]
    vm = von_mises(field(m, Ss, 6))
    U = field(m, D, 3)
    u_ref, th = rigid_fit(m, U, foot, cm)
    bed = np.array([ax_xy[0], ax_xy[1], 0.0])

    def rigid_point(pt):
        return np.asarray(u_ref) + np.cross(th, np.asarray(pt) - np.asarray(cm))
    u_lens = rigid_point((ax_xy[0], ax_xy[1], L["lens_bot"]))
    u_bed = rigid_point(bed)
    grav = dict(head_ref_u_um=(np.asarray(u_ref) * 1000).round(2).tolist(), tilt_urad=(np.asarray(th) * 1e6).round(1).tolist(),
                lens_u_um=(u_lens * 1000).round(2).tolist(), beam_error_at_bed_um=(u_bed[:2] * 1000).round(1).tolist(),
                focus_shift_um=float(u_bed[2] * 1000), vm_max=float(vm.max()), u_max_um=float(np.linalg.norm(U, axis=1).max() * 1000))
    print(f"  4c model gravity: tilt {grav['tilt_urad']} urad, lens {grav['lens_u_um']} um, beam error at bed {grav['beam_error_at_bed_um']} um", flush=True)
    job = f"c4c_model_{gantry or 'default'}_modal"
    write_model(job, m, mats, extra)
    append(job, "*BOUNDARY\nFEET,1,3\n*STEP\n*FREQUENCY, SOLVER=SPOOLES\n6\n*NODE FILE\nU\n*END STEP\n")
    t_m = run_ccx(job)
    f = read_freqs(job)
    modes = []
    names = ("x (along the cross-beams)", "y (fore-aft)", "z (vertical)")
    for k, blk in enumerate([x for x in read_frd(job) if x["name"] == "DISP"][:6]):
        Um = field(m, blk, 3)
        ur, tr = rigid_fit(m, Um, foot, cm)
        mag = np.linalg.norm(Um, axis=1)
        ub = np.asarray(ur) + np.cross(tr, bed - np.asarray(cm))
        modes.append(dict(f_hz=f[k] if k < len(f) else None, head_translation_dir=(np.asarray(ur) / (np.linalg.norm(ur) + 1e-30)).round(2).tolist(),
                          head_rotation_dir=(np.asarray(tr) / (np.linalg.norm(tr) + 1e-30)).round(2).tolist(),
                          bed_motion_dir=(ub[:2] / (np.linalg.norm(ub[:2]) + 1e-30)).round(2).tolist(),
                          max_at=m["xyz"][int(np.argmax(mag))].round(0).tolist(), dominant_head_axis=names[int(np.argmax(np.abs(ur)))]))
    print(f"  4c model modes: {[round(x, 1) for x in f]} Hz", flush=True)
    r = dict(variant=f"model (as drawn, P['gantry'] = {gantry or g_old!r}: four 45 mm posts, braces, head hung from the flange plate)",
             gantry_option=gantry or g_old, extra_parts_as_drawn=extras_drawn, n_braces=len(braces), gravity=grav, modes=modes,
             ccx_s=dict(gravity=round(t_s), modal=round(t_m)), masses_kg=dict(head=m_head, lens=m_lens, cm_mm=[round(c_, 1) for c_ in cm]),
             posts=[dict(bb=[round(v, 1) for v in g_["bb"]]) for g_ in posts], braces=braces, foot_nodes=int(len(foot)), feet_nodes=int(len(feet)),
             note="angle brackets and flange plate as drawn; posts/beams equivalent tubes (I from the T-slot section); base rails rigid")
    r["pass"] = bool(f and f[0] > 60)
    r["pass100"] = bool(f and f[0] > 100)
    stamp(r, m, "SPOOLES", hmax=hmax)
    return r


def case4c_model(R):
    g = os.environ.get("FT_GANTRY_MODEL") or None          # e.g. four_post_braced_front; default: the model's own
    R.setdefault("4c", {}).setdefault("variants", {})["model_" + (g or "four_post")] = gantry_model_case(g)


# --------------------------------------------------------------------------------------------
# 4d  the piston rod (analytic)
# --------------------------------------------------------------------------------------------
def case4d(R):
    parts = {s: M.build(s) for s in ("FT-1", "FT-1V")}
    od, wall = P["rod_od"], P["rod_wall"]
    idd = od - 2 * wall
    A = math.pi / 4 * (od ** 2 - idd ** 2)
    I = math.pi / 64 * (od ** 4 - idd ** 4)
    E20, E200 = 193e3, 193e3 * 27.0 / 28.3          # ASME BPVC II-D Table TM-1, 304: 28.3e6 psi at 70 F, 27.0e6 at 400 F
    rho = dict(al=2.70e-3, ss=8.0e-3, heater=6.0e-3, rope=0.6e-3)   # g/mm3; heater (sheath, MgO, coil) and rope are estimates
    vol = lambda st, prefix: part(parts[st], prefix).shape.Volume()
    mass_g = dict(substrate=vol("FT-1", "Substrate disc") * rho["al"], heater_plate=vol("FT-1", "Heater plate") * rho["al"],
                  plate_heaters=vol("FT-1", "Plate heaters") * rho["heater"], rope=vol("FT-1", "Fibreglass rope") * rho["rope"],
                  rod_box=vol("FT-1", "Piston rod") * rho["ss"], rod_cube=vol("FT-1V", "Piston rod") * rho["ss"],
                  rod_clamp=vol("FT-1", "Rod clamp") * rho["al"], leads_est=15.0, build_45g_est=45.0)
    m_box = sum(v for k, v in mass_g.items() if k not in ("rod_cube",))
    m_cube = m_box - mass_g["rod_box"] + mass_g["rod_cube"]
    out = dict(section=dict(od_mm=od, wall_mm=wall, A_mm2=A, I_mm4=I, E20_MPa=E20, E200_MPa=E200), mass_g={k: round(v, 1) for k, v in mass_g.items()},
               payload_N=dict(box=m_box * 9.81e-3, cube=m_cube * 9.81e-3))
    cases = {}
    for st in ("FT-1", "FT-1V"):
        Lv = M.levels(st)["rod_vis"]
        Lfree = Lv - (P["clamp_h"] - 2.0)                # clamp grips the bottom 23 mm; socket the top 8 mm (not in rod_vis)
        h = P["sub_t"] + P["hp_t"]                       # socket bottom to substrate top: the plate as a rigid lever
        Pcr = {k: math.pi ** 2 * E * I / (2.0 * Lfree) ** 2 for k, E in (("20C", E20), ("200C", E200))}   # fixed-free, K = 2
        lat = {}
        for F in (1.0, 5.0):
            EI = E200 * I
            d = F * Lfree ** 3 / (3 * EI) + F * h * Lfree ** 2 / (2 * EI)
            th = F * Lfree ** 2 / (2 * EI) + F * h * Lfree / EI
            lat[f"{F:g}N"] = dict(top_shift_um=(d + th * h) * 1000, socket_shift_um=d * 1000, tilt_urad=th * 1e6,
                                  edge_lift_um=th * P["plate_d"] / 2 * 1000)
        cases[st] = dict(rod_vis_mm=Lv, free_length_mm=Lfree, lever_mm=h, euler_fixed_free_N=Pcr, lateral=lat,
                         stiffness_N_per_um=1.0 / lat["1N"]["top_shift_um"])
    # axial load on the X-VSR20A
    cs, shore = 2.62, 70.0                         # AS568-110/-111 class O-ring (0.103 in.) on a 1/2 in. rod; 70A FKM (assumed)
    fr = {}
    for s in (0.10, 0.15, 0.20):
        fl, Eo = lindley(cs, shore, s)
        fr[f"{int(s * 100)}%"] = dict(radial_N_per_oring=fl * math.pi * od, running_mu_0p1_0p3_N=[0.1 * 2 * fl * math.pi * od, 0.3 * 2 * fl * math.pi * od],
                                      breakout_mu_0p5_N=0.5 * 2 * fl * math.pi * od)
    vac = P_ATM * math.pi / 4 * od ** 2
    W_box, W_cube = out["payload_N"]["box"], out["payload_N"]["cube"]
    run_lo, run_hi = fr["15%"]["running_mu_0p1_0p3_N"]
    brk = fr["15%"]["breakout_mu_0p5_N"]
    rope = (1.0, 5.0)                              # N, estimate: fibreglass rope lightly pressed on the bore
    loads = {          # what the stage must supply; each range runs from low running friction to breakout
        "FT-1, lifting: push": [W_box + run_lo + rope[0], W_box + brk + rope[1]],
        "FT-1, lowering: pull (friction exceeds the weight)": [run_lo + rope[0] - W_box, brk + rope[1] - W_box],
        "FT-1V, lifting: push (the vacuum helps; < 0 = hold back)": [W_cube - vac + run_lo + rope[0], W_cube - vac + brk + rope[1]],
        "FT-1V, lowering: pull (against the vacuum)": [vac - W_cube + run_lo + rope[0], vac - W_cube + brk + rope[1]],
    }
    _ = run_hi
    # the two piston stages against each load case, for the gland as drawn (two O-rings at 15 %) and for one O-ring at 10 %
    stages = {"X-VSR20A": dict(rating_N=100.0, src="Zaber X-VSR20A datasheet: 100 N (direction of the rating not stated)"),
              "MTS50/M-Z8": dict(rating_N=4.5 * 9.81, src="Thorlabs MTS50/M-Z8 catalogue page and 2016 MTS50-Z8E datasheet: 4.5 kg vertical, "
                                 "12 kg horizontal, 2.4-3 mm/s; a leadscrew carriage, so it drives both ways (its vertical rating taken as the limit both ways)")}
    seals = {"two O-rings at 15 % (as drawn)": (2, 0.15), "one O-ring at 10 %": (1, 0.10)}
    table = {}
    for sname, (n_or, s_) in seals.items():
        fl, _ = lindley(cs, shore, s_)
        rad = fl * math.pi * od
        f3 = dict(run_lo=(0.1 * n_or * rad, rope[0]), run_hi=(0.3 * n_or * rad, rope[1]), breakout=(0.5 * n_or * rad, rope[1]))
        rows = {}
        for case, fn in (("FT-1 lifting (push)", lambda f, rp: W_box + f + rp), ("FT-1 lowering (pull)", lambda f, rp: f + rp - W_box),
                         ("FT-1V lifting (push; < 0 = hold back)", lambda f, rp: W_cube - vac + f + rp),
                         ("FT-1V lowering (pull, against the vacuum)", lambda f, rp: vac - W_cube + f + rp)):
            rows[case] = {k: round(fn(*v), 1) for k, v in f3.items()}
        verdict = {}
        for st, sd in stages.items():
            for state in ("FT-1", "FT-1V"):
                rr = [v for k, v in rows.items() if k.startswith(state + " ")]
                run_max = max(v["run_hi"] for v in rr)
                brk_max = max(v["breakout"] for v in rr)
                verdict[f"{st} in {state}"] = dict(running_max_N=run_max, breakout_max_N=brk_max,
                                                   running_pct=round(100 * run_max / sd["rating_N"]), breakout_pct=round(100 * brk_max / sd["rating_N"]),
                                                   verdict=("yes" if brk_max <= sd["rating_N"] else "only while friction stays at running levels"
                                                            if run_max <= sd["rating_N"] else "no"))
        table[sname] = dict(friction_N={k: round(v[0], 1) for k, v in f3.items()}, loads_N=rows, stages=verdict)
    out.update(cases=cases, oring=dict(cs_mm=cs, shore=shore, count=2, method="Lindley contact force x friction coefficient (greased FKM on 304: running 0.1-0.3, breakout 0.5; estimates)",
                                       by_squeeze=fr), vacuum_load_N=vac, rope_drag_N_est=rope, stage_rating_N=100.0,
               axial_load_ranges_N={k: [round(v[0], 1), round(v[1], 1)] for k, v in loads.items()},
               stages=stages, stage_check=table)
    # thermal growth of the rod (linear 200 -> 30 C along the free length plus the socket at 200 C; the thermal FE gives the real profile)
    a304 = 17.3e-6
    for st in ("FT-1", "FT-1V"):
        Lf = cases[st]["free_length_mm"]
        grow = a304 * (Lf * ((200 + 30) / 2 - 20) + P["socket"] * 180)
        cases[st]["thermal_growth_um_est"] = grow * 1000
    R["4d"] = dict(case="4d piston rod MK-06: column, lateral stiffness, axial load on the X-VSR20A (analytic)", **out)
    R["4d"]["run"] = dict(utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=model_commit(), method="analytic")
    print(f"  4d: Euler (box) {cases['FT-1']['euler_fixed_free_N']['200C']:.0f} N; 5 N drag -> {cases['FT-1']['lateral']['5N']['top_shift_um']:.1f} um (box), "
          f"{cases['FT-1V']['lateral']['5N']['top_shift_um']:.1f} um (cube); loads {out['axial_load_ranges_N']}")


# --------------------------------------------------------------------------------------------
# plot and write-up
# --------------------------------------------------------------------------------------------
def plot_gasket(R):
    """Gasket compression along the door's gasket line (CAD v2): one panel per run (door return x gasket grade), load
    steps light -> dark (one blue ramp); dashed lines: the latch and the two hinges."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    r = R["4a"]
    ramp = {"preload": "#84b9f3", "plus10mbar": "#2370cd", "plus50mbar": "#0e3d7e"}
    names = {"preload": "latch and hinges closed", "plus10mbar": "+10 mbar purge", "plus50mbar": "+50 mbar fault (NLGEOM)"}
    ink, ink2, grid, bad = "#191919", "#666666", "#e6e6e6", "#c0392b"
    runs = [(c, gname, gk) for c, cfg in r["configs"].items() for gname, gk in cfg["gaskets"].items()]
    title = {("drawn", "foam_2a2"): "door return 5.5 mm (as drawn), foam 2A2", ("drawn", "foam_2a4"): "door return 5.5 mm (as drawn), foam 2A4",
             ("deep_return", "foam_2a2"): f"door return {DOOR_RETURN_DEEP:.0f} mm, foam 2A2"}
    fig, axes = plt.subplots(1, len(runs), figsize=(4.6 * len(runs), 4.0), sharey=True, dpi=130)
    axes = np.atleast_1d(axes)
    ymin, ymax = 0.0, 0.0
    for ax, (c, gname, g) in zip(axes, runs):
        for tag in ("preload", "plus10mbar", "plus50mbar"):
            prof = g["nlgeom_plus50mbar"]["profile"] if tag == "plus50mbar" and "profile" in g["nlgeom_plus50mbar"] else g["steps"][tag]["profile"]
            y = np.array([np.nan if v is None else v for v in prof], dtype=float)
            x = np.arange(len(y)) * 5.0 + 2.5
            ax.plot(x, y, color=ramp[tag], lw=2.0, label=names[tag], solid_capstyle="round")
            ymax, ymin = max(ymax, np.nanmax(y)), min(ymin, np.nanmin(y))
        for k, s in r["support_s_mm"].items():
            ax.axvline(s, color=ink2, lw=0.8, ls=(0, (3, 3)))
        for side, (a, b) in r["sides_s_mm"].items():
            ax.text((a + b) / 2, 1.02, side + (" (latch)" if side == "front" else " (hinges)" if side == "back" else ""),
                    transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=8, color=ink2)
            ax.axvline(a, color=grid, lw=0.8)
        ax.axhline(g["squeeze_mm"], color=ink2, lw=0.8)
        ax.axhline(0.0, color=bad, lw=0.9)
        ax.text(r["perimeter_mm"] * 0.995, g["squeeze_mm"], f"set squeeze {g['squeeze_mm']:.2f} mm", ha="right", va="bottom", fontsize=8, color=ink2)
        ax.text(r["perimeter_mm"] * 0.5, 0.0, "below: open", ha="center", va="top", fontsize=8, color=bad)
        ax.set_title(title.get((c, gname), f"{c}, {gname}") + f": {g['total_preload_N']:.0f} N to close", fontsize=9.5, color=ink, pad=16)
        ax.set_xlim(0, r["perimeter_mm"])
        ax.set_xlabel("position along the gasket line from the front-left corner (mm)", fontsize=8.5, color=ink)
        ax.grid(axis="y", color=grid, lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(colors=ink2, labelsize=8)
    axes[0].set_ylabel("gasket compression (mm)", fontsize=9, color=ink)
    axes[0].set_ylim(min(-0.3, ymin * 1.1), max(1.1, ymax * 1.1))
    axes[-1].legend(loc="lower right", fontsize=8, frameon=False)
    fig.suptitle("4a (CAD v2): Saginaw door's gasket compression, one latch (front middle) and two hinges (back), dashed "
                 "(CalculiX, door + window stack + gasket as a bonded spring bed)", fontsize=10, color=ink, y=1.0)
    fig.tight_layout()
    fig.savefig(OUT / "struct-lid-gasket-v2.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def describe_mode(md):
    T, Rr = np.abs(md["head_translation_dir"]), np.abs(md["head_rotation_dir"])
    trans = ("sideways along the cross-beam (x)", "fore-aft (y)", "up and down (z)")[int(np.argmax(T))]
    rot = ("pitch about the cross-beam axis (x)", "roll about y", "yaw about z")[int(np.argmax(Rr))]
    return f"head moves {trans} with {rot}"


def f_(x, n=1):
    return f"{x:,.{n}f}"


def off_um(g):
    return float(np.hypot(*g["beam_error_at_bed_um"]))


def tilt_urad(g):
    return float(np.linalg.norm(g["tilt_urad"]))


def write_md(R):
    L = ["## Structure (case 4): box lid, cube top plate and window, scan-head plate and gantry, piston rod", ""]
    a, b, c, d = (R.get(k) for k in ("4a", "4b", "4c", "4d"))
    # ---------------- short answer
    L += ["### Short answer", ""]
    if a:
        fk, sp = a["gaskets"]["fkm"], a["gaskets"]["sponge"]
        fkn, spn = fk["nlgeom_plus50mbar"], sp["nlgeom_plus50mbar"]
        L.append(f"- **Box lid (4a): it seals at +10 mbar and at a +50 mbar fault with either gasket, and the 14 ga lid does not yield, "
                 f"but the solid FKM cord is the wrong gasket.** Squeezing a Ø3 mm 75A FKM cord by 22 % round the {f_(a['perimeter_mm'], 0)} mm "
                 f"gasket line takes {f_(fk['total_preload_N'] / 1000, 1)} kN: about {f_(abs(fk['steps']['preload']['reactions_N']['CLF1'][2]), 0)} N "
                 f"on each front clamp, {f_(abs(fk['steps']['preload']['reactions_N']['CLL'][2]), 0)} N on each side clamp and "
                 f"{f_(abs(fk['steps']['preload']['reactions_N']['HINGE'][2]), 0)} N on the hinge, and the lid's middle then sits "
                 f"{f_((fk['steps']['preload']['window_seat_uz_mm'] + fk['squeeze_mm']) * 1000, 0)} µm higher than its clamped edges before any pressure. "
                 f"A closed-cell silicone sponge strip (ASTM D1056 2A2, like the box's own foam) needs {f_(sp['total_preload_N'], 0)} N in all and "
                 f"stays at ≥ {f_(spn.get('gasket_comp_min_mm', 0), 2)} mm of its 0.75 mm squeeze at +50 mbar. **Change: keep a soft sponge or "
                 f"hollow-bulb silicone gasket, not a solid cord**, and add a relief valve set below +50 mbar if the purge line has none.")
    if b:
        pl, w = b["plate"], b["window"]
        L.append(f"- **Cube top plate and window (4b): pass by a wide margin.** The 22.9 mm blank bored for the window ring deflects "
                 f"{f_(pl['clamped']['u_max_mm'] * 1000, 0)}-{f_(pl['simply_supported']['u_max_mm'] * 1000, 0)} µm at 1 atm (bolted to simply supported), "
                 f"peak {f_(pl['simply_supported']['vm_max'], 1)} MPa: safety factor {f_(pl['simply_supported']['sf_yield'], 0)} on yield. The "
                 f"Ø50.8 x 9.53 mm window on its O-ring peaks at {f_(w['fe_s1_max_MPa'], 2)} MPa (Roark simply supported {f_(w['roark_at_seat']['ss_sigma'], 2)}): "
                 f"factor {f_(w['sf_mor_fe'], 0)} on Corning 7980's abraded modulus of rupture and {f_(w['sf_design_fe'], 1)} on a 6.9 MPa (1000 psi) design stress.")
    if c:
        v = c["variants"]
        dr = v["drawn"]
        hd_, ln_ = c.get("head", HEAD), c.get("lens", LENS)
        txt = (f"- **Head plate on the gantry (4c): too soft as drawn.** With the datasheet head and objective ({f_(hd_['mass'], 1)} + "
               f"{f_(ln_['mass'], 2)} kg, moved 30 mm toward -Y on a plate 30 mm longer), its first three modes are "
               f"{', '.join(f_(m_['f_hz'], 0) for m_ in dr['modes'][:3])} Hz, against PR 266's 100 Hz goal (60 Hz minimum); the first is the "
               f"head nodding about the cross-beam. Gravity tilts the head {f_(tilt_urad(dr['gravity']) / 1000, 2)} mrad, which puts the spot "
               f"{f_(off_um(dr['gravity']), 0)} µm off at the bed: a fixed offset that the scanner's correction file absorbs, unlike the low modes.")
        lab = {"braced": "two diagonal braces and a 30 x 60 cross-beam", "four_post": "a front cross-beam on two more posts",
               "four_post_braced": "four posts with a diagonal per side and two knee braces at the back",
               "four_post_braced_45": "that frame with 45 mm posts"}
        full = {"braced": "brace each upright diagonally to the front rail and use a 30 x 60 cross-beam",
                "four_post": "carry the plate's front edge on a front cross-beam and two more posts",
                "four_post_braced": "four 30 mm posts, a front cross-beam under the plate, a diagonal on each side and two knee braces at the back",
                "four_post_braced_45": "four 45 mm posts, a front cross-beam under the plate, a diagonal on each side and two knee braces at the back"}
        txt += " Stiffer frames: " + "; ".join(f"{lab[k]}, {', '.join(f_(m_['f_hz'], 0) for m_ in v[k]['modes'][:3])} Hz" for k in lab if k in v) + "."
        ok60 = [k for k in lab if k in v and v[k]["modes"][0]["f_hz"] > 60]
        ok100 = [k for k in lab if k in v and v[k]["modes"][0]["f_hz"] > 100]
        if ok60:
            txt += (f" Only {' and '.join(lab[k] for k in ok60)} clear{'s' if len(ok60) == 1 else ''} the 60 Hz minimum"
                    + (f", and {' and '.join(lab[k] for k in ok100)} the 100 Hz goal." if ok100 else "; none reaches the 100 Hz goal.")
                    + f" **Change: {full[ok60[0]]}** (all outside the box; the front posts stand 20-50 mm in front of the front rail, on a foot bracket).")
        else:
            txt += " **None of them reaches 60 Hz with the datasheet masses: the frame needs heavier sections than tried here.**"
        L.append(txt + " These are upper bounds (equivalent tubes, bonded joints, the head rigid on the plate), so real frequencies will be lower: "
                 "tap-test the built frame. The CAD model is being redrawn with the head hung from a bracket on its entrance face, which will be "
                 "softer still; re-run 4c on it.")
    if d:
        cb, cc = d["cases"]["FT-1"], d["cases"]["FT-1V"]
        loads = d["axial_load_ranges_N"]
        L.append(f"- **Piston rod (4d): passes as a column and laterally; the stage's direction of load is the open point.** Euler buckling "
                 f"(fixed-free, 200 °C) is {f_(cb['euler_fixed_free_N']['200C'] / 1000, 0)} kN in the box and {f_(cc['euler_fixed_free_N']['200C'] / 1000, 0)} kN in the "
                 f"cube, against < 60 N. A 5 N blade drag moves the substrate top {f_(cb['lateral']['5N']['top_shift_um'], 0)} µm (box) and "
                 f"{f_(cc['lateral']['5N']['top_shift_um'], 0)} µm (cube), inside the 100 µm clearance. The two greased O-rings' friction "
                 f"(estimate {f_(d['oring']['by_squeeze']['15%']['running_mu_0p1_0p3_N'][0], 0)}-{f_(d['oring']['by_squeeze']['15%']['running_mu_0p1_0p3_N'][1], 0)} N running, "
                 f"up to {f_(d['oring']['by_squeeze']['15%']['breakout_mu_0p5_N'], 0)} N at breakout) is "
                 f"{f_(d['oring']['by_squeeze']['15%']['running_mu_0p1_0p3_N'][0] / d['payload_N']['box'], 0)}-"
                 f"{f_(d['oring']['by_squeeze']['15%']['breakout_mu_0p5_N'] / d['payload_N']['box'], 0)} times the plate stack's "
                 f"{f_(d['payload_N']['box'], 1)} N weight, so the X-VSR20A has to pull the rod down every layer: "
                 f"{loads['FT-1, lowering: pull (friction exceeds the weight)'][0]:.0f}-{loads['FT-1, lowering: pull (friction exceeds the weight)'][1]:.0f} N in the box and "
                 f"{loads['FT-1V, lowering: pull (against the vacuum)'][0]:.0f}-{loads['FT-1V, lowering: pull (against the vacuum)'][1]:.0f} N in the cube, "
                 f"where the vacuum adds {f_(d['vacuum_load_N'], 1)} N. Pushing, the worst case is {loads['FT-1, lifting: push'][1]:.0f} N of its 100 N. **Check that "
                 f"the X-VSR20A takes a pulling load** (its datasheet gives a centred load); if not, use one O-ring at about 10 % squeeze, "
                 f"a PTFE lip seal, or a return spring.")
        sc = d.get("stage_check")
        if sc:
            two, one = sc["two O-rings at 15 % (as drawn)"]["stages"], sc["one O-ring at 10 %"]["stages"]
            plain = lambda vd: "acceptable" if vd == "yes" else "not acceptable"
            L.append(f"- **Thorlabs MTS50/M-Z8 (the PCard route, 4.5 kg = 44 N vertical):** with the gland as drawn (two O-rings at 15 %) it is "
                     f"{plain(two['MTS50/M-Z8 in FT-1']['verdict'])} in FT-1 (up to {two['MTS50/M-Z8 in FT-1']['running_max_N']:.0f} N running, "
                     f"{two['MTS50/M-Z8 in FT-1']['breakout_max_N']:.0f} N at breakout) and {plain(two['MTS50/M-Z8 in FT-1V']['verdict'])} in FT-1V, where "
                     f"pulling the rod down against the vacuum takes up to {two['MTS50/M-Z8 in FT-1V']['running_max_N']:.0f} N running "
                     f"({two['MTS50/M-Z8 in FT-1V']['running_pct']} % of 44 N) and {two['MTS50/M-Z8 in FT-1V']['breakout_max_N']:.0f} N at breakout. With one O-ring "
                     f"at 10 % it is {plain(one['MTS50/M-Z8 in FT-1']['verdict'])} in FT-1 and {plain(one['MTS50/M-Z8 in FT-1V']['verdict'])} in FT-1V "
                     f"(worst {one['MTS50/M-Z8 in FT-1V']['breakout_max_N']:.0f} N, {one['MTS50/M-Z8 in FT-1V']['breakout_pct']} %), pull-down included: its "
                     f"leadscrew drives both ways. One O-ring gives up the second seal, so check the leak in FT-1V. At 2.4-3 mm/s a 30 µm layer "
                     f"step is instant and the 20 mm lift for removal takes 7-8 s. The X-VSR20A carries every case with either seal (worst "
                     f"{two['X-VSR20A in FT-1V']['breakout_max_N']:.0f} N of 100 N) if it can pull.")
    L.append("")
    # ---------------- 4a
    if a:
        L += ["### 4a FT-1 box lid on its gasket", "",
              f"The lid as drawn (14 ga 304, 1.9 mm, 416 x 315 mm with a 15 mm skirt and the Ø53 mm window bore), bonded to the window stack "
              f"(inner clamp ring, window ring and retaining flange, 6061) and to a spring bed on the drawn gasket's 7.9 mm wide footprint: "
              f"a {SPRING_T:g} mm layer with ν = 0 whose stiffness per length is the cord's secant stiffness at its squeeze (on the drawn 1 mm "
              f"layer the squeeze would be a 66 % strain, too large for NLGEOM's linear material). The four clamps pull the skirt's lower edge "
              f"down by the squeeze over 24 mm each; the hinge is a pin "
              f"line at its height along the back face. Pressure acts on the {f_(a['pressure_area_mm2'] / 100, 0)} cm² inside the gasket "
              f"({f_(a['force_10mbar_N'], 0)} N at +10 mbar, {f_(a['force_50mbar_N'], 0)} N at +50 mbar, with the window's load on its retaining flange).",
              "", "![Lid gasket compression](struct-lid-gasket.png)", "",
              "| | Solid FKM cord Ø3 mm, 75A, 22 % (0.66 mm) | Silicone sponge 3 x 7.9 mm, 2A2, 25 % (0.75 mm) |", "|---|---|---|"]
        rows = []

        def both(fn):
            return " | ".join(fn(a["gaskets"][g]) for g in ("fkm", "sponge"))
        rows.append("| Force to close (Lindley / ASTM D1056 CFD) | " + both(lambda g: f"{f_(g['force_per_mm'], 2)} N/mm, {f_(g['total_preload_N'], 0)} N") + " |")
        rows.append("| Clamp loads when closed: front, side, hinge | " + both(lambda g: f"{f_(abs(g['steps']['preload']['reactions_N']['CLF1'][2]), 0)} N, "
                    f"{f_(abs(g['steps']['preload']['reactions_N']['CLL'][2]), 0)} N, {f_(abs(g['steps']['preload']['reactions_N']['HINGE'][2]), 0)} N") + " |")
        rows.append("| Clamp loads at +50 mbar (linear): front, side, hinge | " + both(lambda g: f"{f_(abs(g['steps']['plus50mbar']['reactions_N']['CLF1'][2]), 0)} N, "
                    f"{f_(abs(g['steps']['plus50mbar']['reactions_N']['CLL'][2]), 0)} N, {f_(abs(g['steps']['plus50mbar']['reactions_N']['HINGE'][2]), 0)} N") + " |")
        rows.append("| Least gasket compression: closed / +10 mbar / +50 mbar linear / +50 mbar NLGEOM | " + both(
            lambda g: f"{f_(g['steps']['preload']['gasket_comp_min_mm'], 3)} / {f_(g['steps']['plus10mbar']['gasket_comp_min_mm'], 3)} / "
                      f"{f_(g['steps']['plus50mbar']['gasket_comp_min_mm'], 3)} / {f_(g['nlgeom_plus50mbar'].get('gasket_comp_min_mm', float('nan')), 3)} mm") + " |")
        rows.append("| Gasket length open (compression < 0) at +50 mbar | " + both(lambda g: f"{f_(g['steps']['plus50mbar']['gasket_open_length_mm'], 0)} mm") + " |")
        rows.append("| Window seat height, closed → +10 mbar → +50 mbar NLGEOM | " + both(
            lambda g: f"{f_(g['steps']['preload']['window_seat_uz_mm'] * 1000, 0)} → {f_(g['steps']['plus10mbar']['window_seat_uz_mm'] * 1000, 0)} → "
                      f"{f_(g['nlgeom_plus50mbar'].get('window_seat_uz_mm', float('nan')) * 1000, 0)} µm") + " |")
        rows.append("| Lid's highest point at +50 mbar: linear / NLGEOM | " + both(
            lambda g: f"{f_(g['steps']['plus50mbar']['lid_uz_max_mm'] * 1000, 0)} / {f_(g['nlgeom_plus50mbar'].get('lid_uz_max_mm', float('nan')) * 1000, 0)} µm") + " |")
        rows.append("| Peak von Mises in the lid away from the clamps and hinge: closed / +10 / +50 mbar NLGEOM | " + both(
            lambda g: f"{f_(g['steps']['preload']['vm_lid_away_max'], 0)} / {f_(g['steps']['plus10mbar']['vm_lid_away_max'], 0)} / "
                      f"{f_(g['nlgeom_plus50mbar'].get('vm_lid_away_max', float('nan')), 0)} MPa") + " |")
        rows.append("| Peak von Mises at a clamp patch's end (singular in this model), +50 mbar linear | " + both(
            lambda g: f"{f_(g['steps']['plus50mbar']['vm_lid_max'], 0)} MPa (99.5 %: {f_(g['steps']['plus50mbar']['vm_lid_p995'], 0)})") + " |")
        rows.append("| Safety factor on 304's 215 MPa yield, away from the clamps, +50 mbar NLGEOM | " + both(
            lambda g: f"{f_(215.0 / g['nlgeom_plus50mbar'].get('vm_lid_away_max', float('nan')), 1)}") + " |")
        L += rows
        ck = R.get("4a_check")
        L += ["", f"- **Mesh check:** one quadratic tetrahedron through the 1.9 mm sheet (hmax {a['run'].get('hmax', 7):g} mm, {f_(a['run']['nodes'], 0)} nodes): a clamped "
              f"400 x 300 x 1.9 mm 304 plate at 1 kPa on the same mesh size deflects {f_(ck['w_fe_mm'] * 1000, 1)} µm against Timoshenko's "
              f"{f_(ck['w_timoshenko_mm'] * 1000, 1)} µm (ratio {ck['ratio']:.3f})." if ck else "",
              "- **Linear vs NLGEOM:** at +50 mbar the lid's middle moves about half its thickness, so membrane action matters: NLGEOM gives a "
              "smaller bulge, more gasket compression and lower stress than the linear run. At +10 mbar the linear run is enough.",
              "- **Gasket model:** the band is bonded to the lid and stiff in compression and tension. That is valid only while it stays compressed "
              "everywhere, which it does in every step here (no open length).",
              "- **Clamp loads:** no load rating for the box's clamps was found. They are made for a foam gasket, so the 0.55-0.62 kN each "
              "(1.5 kN on the hinge) that the FKM cord needs is probably beyond them; with the sponge each clamp carries about 0.1 kN. "
              "The clamps are modelled as rigid, so a real clamp that gives a little loses some of the squeeze.",
              "- **Stress at the clamps:** the clamp patches are 24 x 2 mm areas of prescribed displacement, so the peak at their ends is "
              "a singularity of the model, not a number to design to. Away from them the sheet stays below a third of its yield.", ""]
    # ---------------- 4b
    if b:
        pl, w = b["plate"], b["window"]
        L += ["### 4b FT-1V: cube top plate and window at 1 atm", "",
              "| | Bolted (z fixed on the land outside the frame opening) | Simply supported (z fixed on a 4 mm band at the opening's edge) |", "|---|---|---|",
              f"| Largest deflection | {f_(pl['clamped']['u_max_mm'] * 1000, 1)} µm | {f_(pl['simply_supported']['u_max_mm'] * 1000, 1)} µm |",
              f"| Deflection at the window bore | {f_(abs(pl['clamped']['bore_uz_mm']) * 1000, 1)} µm | {f_(abs(pl['simply_supported']['bore_uz_mm']) * 1000, 1)} µm |",
              f"| Peak von Mises (99.5 %) | {f_(pl['clamped']['vm_max'], 1)} ({f_(pl['clamped']['vm_p995'], 1)}) MPa | {f_(pl['simply_supported']['vm_max'], 1)} ({f_(pl['simply_supported']['vm_p995'], 1)}) MPa |",
              f"| Safety factor on 6061-T6 yield (276 MPa) | {f_(pl['clamped']['sf_yield'], 0)} | {f_(pl['simply_supported']['sf_yield'], 0)} |",
              f"| Roark, square plate {f_(pl['roark_square_plate']['side_mm'], 0)} mm, 22.9 mm thick: deflection, stress | {f_(pl['roark_square_plate']['cl_w_mm'] * 1000, 1)} µm, {f_(pl['roark_square_plate']['cl_sigma'], 1)} MPa | "
              f"{f_(pl['roark_square_plate']['ss_w_mm'] * 1000, 1)} µm, {f_(pl['roark_square_plate']['ss_sigma'], 1)} MPa |", "",
              f"Load: 1 atm on the outer face, and the window ring's {f_(P_ATM * math.pi * 26.5 ** 2, 0)} N spread round the bore. The FE plate is softer "
              "than Roark's uniform 22.9 mm plate because its edge band outside the boss is 15.3 mm thick. The frame opening (266 mm) is an estimate.", "",
              "| Window Ø50.8 x 9.53 mm fused silica on its O-ring (support r = 23.7 mm) | Peak tensile stress | Deflection | SF on 52.4 MPa (abraded MOR) | SF on 6.9 MPa (1000 psi design) |",
              "|---|---|---|---|---|",
              f"| FEA, simply supported on the O-ring circle, 1 atm (FT-1V) | {f_(w['fe_s1_max_MPa'], 3)} MPa | {f_(w['fe_u_max_um'], 2)} µm | {f_(w['sf_mor_fe'], 0)} | {f_(w['sf_design_fe'], 1)} |",
              f"| Roark simply supported, a = 23.7 mm | {f_(w['roark_at_seat']['ss_sigma'], 3)} MPa | {f_(w['roark_at_seat']['ss_w'] * 1000, 2)} µm | {f_(52.4 / w['roark_at_seat']['ss_sigma'], 0)} | {f_(6.9 / w['roark_at_seat']['ss_sigma'], 1)} |",
              f"| Roark clamped, a = 23.7 mm | {f_(w['roark_at_seat']['cl_sigma'], 3)} MPa | {f_(w['roark_at_seat']['cl_w'] * 1000, 2)} µm | {f_(52.4 / w['roark_at_seat']['cl_sigma'], 0)} | {f_(6.9 / w['roark_at_seat']['cl_sigma'], 1)} |",
              f"| Roark simply supported at the window's edge, a = 25.4 mm (upper bound) | {f_(w['roark_at_edge_r25_4']['ss_sigma'], 3)} MPa | {f_(w['roark_at_edge_r25_4']['ss_w'] * 1000, 2)} µm | {f_(52.4 / w['roark_at_edge_r25_4']['ss_sigma'], 0)} | {f_(6.9 / w['roark_at_edge_r25_4']['ss_sigma'], 1)} |",
              f"| FT-1 box, +50 mbar (window pushed up against its flange) | {f_(w['box_plus50mbar']['s1_MPa'], 4)} MPa | – | – | {f_(w['box_plus50mbar']['sf_design'], 0)} |", ""]
    # ---------------- 4c
    if c:
        v = c["variants"]
        L += ["### 4c Scan-head plate MK-09 on the T-slot gantry", "",
              "![Gantry mode 1](struct-gantry-mode1.png)", "",
              "| Frame | Mode 1 | Mode 2 | Mode 3 | Gravity tilt of the head | Lens sag | Static spot offset at the bed | First mode > 60 Hz / > 100 Hz |", "|---|---|---|---|---|---|---|---|"]
        dr = v["drawn"]
        names = {"drawn": f"as drawn: 30 mm cross-beam on two 30 mm uprights, plate cantilevered {f_(145.0 - dr['plate_y_mm'][0], 0)} mm",
                 "braced": "+ a diagonal brace per upright to the front rail, 30 x 60 cross-beam",
                 "four_post": "as drawn + a front cross-beam under the plate's front edge on two more posts",
                 "four_post_braced": "four posts + a diagonal per side (front post's top to back post's base) + two knee braces at the back",
                 "four_post_braced_45": "the same with 45 mm posts (I = 140,000 mm⁴, estimate)"}
        for k, r in v.items():
            ms = r["modes"]
            g = r["gravity"]
            L.append(f"| {names.get(k, k)} | " + " | ".join(f"{f_(ms[i]['f_hz'], 1)} Hz: {describe_mode(ms[i])}" for i in range(3))
                     + f" | {f_(tilt_urad(g), 0)} µrad | {f_(abs(g['lens_u_um'][2]), 0)} µm | "
                     f"{f_(off_um(g), 0)} µm | {'yes' if r['pass'] else 'no'} / {'yes' if r.get('pass100') else 'no'} |")
        mk = dr["masses_kg"]
        fpv = next((r for k, r in v.items() if k.startswith("four_post")), None)
        L += ["", f"- Masses (datasheets, the lead's update of 2026-11-27): SCANLAB's standard hurrySCAN 20/30 housing, 206.9 x 140 x 180 mm, "
              f"{f_(mk['head'], 1)} kg without objective, and the LINOS f = 254 mm objective, {f_(mk['lens'], 2)} kg; the head's bottom face sits on "
              f"the lens flange 348.1 mm above the bed. One rigid body on the head's 206.9 x 140 mm footprint on the plate, centre of mass at "
              f"({f_(mk['cm_mm'][0], 0)}, {f_(mk['cm_mm'][1], 0)}, {f_(mk['cm_mm'][2], 0)}) mm: the head's at mid-height of its housing, the lens's midway "
              f"between the flange and its bottom (300 mm, estimate). The collimator, fibre and cables are left out.",
              f"- The head and lens sit 30 mm toward -Y (the back-reflection fix), so the plate is 30 mm longer than in the CAD model "
              f"(y {f_(dr['plate_y_mm'][0], 0)} to {f_(dr['plate_y_mm'][1], 0)} mm), with the lens hole moved with the axis. The CAD model is "
              f"being redrawn with the head hung from a bracket on its beam-entrance face; that bracket is not modelled here (the head is "
              f"rigid on its footprint), so re-run 4c on the redrawn model.",
              (f"- Four-post variants: the front beam is under the plate at y {f_(fpv['front_beam_y_mm'][0], 0)} to {f_(fpv['front_beam_y_mm'][1], 0)} mm, "
               f"10 mm clear of the lens housing and 5 mm clear of the head's front face; the front posts (y = {f_(fpv['front_posts_y_mm'], 0)}) stand "
               f"in front of the front support rail and need a foot bracket. Front knee braces were left out because the lid swings "
               f"through that space.") if fpv else None,
              "- The head's operating range is 25 ± 10 °C (15-35 °C, SCANLAB); the thermal cases compare it with the box's air.",
              f"- Frame members: square tubes 30 x 30 x {f_(dr['equivalent_tube']['wall_mm'], 2)} mm with the second moment of a 30 mm 8-slot "
              f"profile (27,000 mm⁴, catalogue-typical, estimate) and the density raised to the drawn profile's mass per length "
              f"({f_(dr['tslot_section']['A_drawing_mm2'], 0)} mm², x{f_(dr['equivalent_tube']['density_scale'], 2)}). The closed tube's torsion "
              f"constant ({f_(dr['equivalent_tube']['J_bredt_mm4'], 0)} mm⁴) is above a slotted profile's, and the joints are bonded, so these are "
              f"upper bounds on stiffness: real corner brackets will give lower frequencies. The model's T-slot drawing itself is five unconnected "
              f"pieces, so it can't be meshed as a load path.",
              "- The static tilt is calibrated out by the scan head's correction grid; it matters only if it changes (heating, a knock). The modes "
              "matter because the floor, the recoater's moves and the hopper's vibration motor can drive them while the beam is on.", ""]
    # ---------------- 4d
    if d:
        cb, cc = d["cases"]["FT-1"], d["cases"]["FT-1V"]
        L += ["### 4d Piston rod MK-06 (analytic)", "",
              f"Rod: 1/2 in. x 0.035 in. 304 tube, A = {f_(d['section']['A_mm2'], 1)} mm², I = {f_(d['section']['I_mm4'], 0)} mm⁴. Free length = the "
              "visible rod less the 23 mm in the clamp; the heater plate is a rigid lever from the socket to the substrate top.", "",
              "| | FT-1 box | FT-1V cube |", "|---|---|---|",
              f"| Free length (clamp top to socket) | {f_(cb['free_length_mm'], 1)} mm | {f_(cc['free_length_mm'], 1)} mm |",
              f"| Euler load, fixed-free (K = 2), 20 °C / 200 °C | {f_(cb['euler_fixed_free_N']['20C'] / 1000, 0)} / {f_(cb['euler_fixed_free_N']['200C'] / 1000, 0)} kN | "
              f"{f_(cc['euler_fixed_free_N']['20C'] / 1000, 0)} / {f_(cc['euler_fixed_free_N']['200C'] / 1000, 0)} kN |",
              f"| 1 N blade drag at the substrate top: shift, tilt | {f_(cb['lateral']['1N']['top_shift_um'], 1)} µm, {f_(cb['lateral']['1N']['tilt_urad'], 0)} µrad | "
              f"{f_(cc['lateral']['1N']['top_shift_um'], 1)} µm, {f_(cc['lateral']['1N']['tilt_urad'], 0)} µrad |",
              f"| 5 N blade drag: shift, tilt, rise of the plate's edge | {f_(cb['lateral']['5N']['top_shift_um'], 1)} µm, {f_(cb['lateral']['5N']['tilt_urad'], 0)} µrad, "
              f"{f_(cb['lateral']['5N']['edge_lift_um'], 1)} µm | {f_(cc['lateral']['5N']['top_shift_um'], 1)} µm, {f_(cc['lateral']['5N']['tilt_urad'], 0)} µrad, "
              f"{f_(cc['lateral']['5N']['edge_lift_um'], 1)} µm |",
              f"| Thermal growth of the rod, 20 → 200 °C at the socket, linear to 30 °C at the clamp (estimate; the thermal FE has the real profile) | "
              f"{f_(cb['thermal_growth_um_est'], 0)} µm | {f_(cc['thermal_growth_um_est'], 0)} µm |", "",
              "| Axial load the stage must supply (low running friction to breakout) | Range |", "|---|---|"]
        for k2, v2 in d["axial_load_ranges_N"].items():
            L.append(f"| {k2} | {v2[0]:.0f} to {v2[1]:.0f} N |")
        sc = d.get("stage_check")
        if sc:
            L += ["", "| Seal | Stage (rating) | FT-1: worst running / breakout | FT-1V: worst running / breakout | FT-1 | FT-1V |", "|---|---|---|---|---|---|"]
            for sname, sd in sc.items():
                for st, info in d["stages"].items():
                    a1, a2 = sd["stages"][f"{st} in FT-1"], sd["stages"][f"{st} in FT-1V"]
                    L.append(f"| {sname} | {st} ({f_(info['rating_N'], 0)} N) | {a1['running_max_N']:.0f} / {a1['breakout_max_N']:.0f} N "
                             f"({a1['running_pct']} / {a1['breakout_pct']} %) | {a2['running_max_N']:.0f} / {a2['breakout_max_N']:.0f} N "
                             f"({a2['running_pct']} / {a2['breakout_pct']} %) | {a1['verdict']} | {a2['verdict']} |")
            L += ["", "- Worst case = the larger of lifting and lowering. In FT-1V the worst case is always the pull-down against the vacuum. "
                  "Running = friction coefficient 0.3 and 5 N of rope drag; breakout = 0.5 (estimates).",
                  f"- {d['stages']['MTS50/M-Z8']['src']}. {d['stages']['X-VSR20A']['src']}."]
        mg = d["mass_g"]
        L += ["", f"- Plate stack: substrate {f_(mg['substrate'], 0)} g, heater plate {f_(mg['heater_plate'], 0)} g, heaters {f_(mg['plate_heaters'], 0)} g, rod "
              f"{f_(mg['rod_box'], 0)} g (cube {f_(mg['rod_cube'], 0)} g), clamp {f_(mg['rod_clamp'], 0)} g, rope {f_(mg['rope'], 1)} g, plus 15 g of leads and a 45 g "
              f"build (estimates): {f_(d['payload_N']['box'], 2)} N.",
              f"- Two O-rings, 2.62 mm section (AS568-110/-111 class), 70A FKM, greased: Lindley's contact force at 10/15/20 % squeeze is "
              + ", ".join(f"{f_(v3['radial_N_per_oring'], 0)}" for v3 in d["oring"]["by_squeeze"].values())
              + " N per O-ring round the rod; friction = 0.1-0.3 of it running and 0.5 at breakout (estimates). Parker's method "
              "(fc x Lp + fh x Ap) needs its Fig. 5-10/5-11 values, which were not read. Measure the drag on the bench before choosing the seal.",
              f"- Vacuum in FT-1V: 1 atm on the rod's Ø12.7 mm section = {f_(d['vacuum_load_N'], 1)} N upward (the rod's lower end is plugged). "
              "Rope wiper drag 1-5 N (estimate).",
              f"- The rod grows about {f_(cb['thermal_growth_um_est'] / 1000, 1)} mm as the plate heats, 3-4 layers of 30 µm: set the "
              "plate's zero height at temperature.",
              "- Not included: the stage's own tilt stiffness (not published), the gland's centring of the rod (which helps), and side loads "
              "from the blade on the plate's rim.", ""]
    # ---------------- method
    L += ["### Method and assumptions (case 4)", "",
          "- **Script:** `desktop-lpbf/fast-track/analysis/fea/ft_struct.py` (cases `4a_check 4a 4b 4c 4d`). Geometry from `cad/ft_model.py` "
          "(`build('FT-1')`, `build('FT-1V')`, `P`, `levels()`), exported as BREP, meshed by gmsh 4.15 (quadratic tetrahedra, straight-sided), "
          "solved by CalculiX 2.21 (SPOOLES; NLGEOM for the lid at +50 mbar), read from the .frd/.dat. Bodies of different materials are "
          "fragmented into one conformal mesh and bonded where they touch. Meshes: lid 61k nodes, cube plate 34k, window 18k, gantry "
          "51k-141k (the larger gantry variants' modal solves exceed the usual 60k-node SPOOLES limit; peak 2.7 GB). Images: `render_fea.py` from PR 266.",
          "- **Materials:** 6061-T6: E 68.9 GPa, ν 0.33, yield 276 MPa (ASM / MatWeb). 304 annealed sheet: E 193 GPa, ν 0.29, yield "
          "215 MPa (ASTM A240 minimum 205 MPa); at 200 °C E = 184 GPa (ASME BPVC II-D, Table TM-1). Fused silica: Corning 7980 data "
          "sheet, E 72.7 GPa, ν 0.16, modulus of rupture 52.4 MPa abraded; the 1000 psi (6.9 MPa) design stress is the usual "
          "allowable for glass windows under steady pressure.",
          "- **Formulas:** circular plates, Roark's Formulas for Stress and Strain (Young & Budynas, 7th ed., Table 11.2, uniform load, "
          "simply supported and fixed edges); rectangular and square plates, Timoshenko & Woinowsky-Krieger, Theory of Plates and Shells, "
          "Tables 8 and 35; Euler buckling P = π²EI/(KL)²; O-ring and cord force, Lindley (1967) with E from Shore hardness (Gent 1958), "
          "as in PR 266's `seals.py` and `fea.py` case 1f; sponge, ASTM D1056 grade 2A2 (5-9 psi at 25 % deflection).",
          "- **Estimates:** hurrySCAN 25 and lens masses; the T-slot's second moment; the cube's frame opening (266 mm); the gasket's size "
          "and squeeze; O-ring section, hardness, squeeze and friction coefficients; the rope's drag.",
          "- **Not done:** fasteners and welds, the clamps' and hinge's own stiffness, contact at the gasket (it stays compressed, so the "
          "bonded spring bed holds), thermal stress in the lid, window and plate, fatigue over purge cycles, the X-VSR20A's tilt stiffness, "
          "the head's own rotary inertia (frequencies a few % high).", ""]
    (OUT / "struct.md").write_text("\n".join(x for x in L if x is not None) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RUN.mkdir(parents=True, exist_ok=True)
    jf = OUT / "struct.json"
    R = json.loads(jf.read_text()) if jf.exists() else {}
    # round 3: the round-1 model's (v1, model d117ba8) results of 4a, 4a-check, 4b and 4d are kept under R["v1"]; the
    # cases now run on CAD v2 and write R["4a"] etc.
    if "v1" not in R:
        R["v1"] = {k: R[k] for k in ("4a_check", "4a", "4b", "4d") if k in R}
        R["v1"]["note"] = "round-1 CAD model (d117ba8): 14 ga custom lid on four clamps and a hinge line, window stack at (0, 0)"
    todo = sys.argv[1:] or ["4a_check", "4a", "4b", "4d"]
    fn = {"4a": case4a, "4a_check": case4a_check, "4b": case4b, "4c": case4c, "4d": case4d, "4c_model": case4c_model}
    for c in todo:
        if c in ("md", "plot"):
            continue
        t0 = time.time()
        print(f"case {c}")
        fn[c](R)
        print(f"  case {c} done in {time.time() - t0:.0f} s")
        jf.write_text(json.dumps(R, indent=1, default=float))
    if "4a" in R and "configs" in R["4a"] and ("4a" in todo or "plot" in todo):
        plot_gasket(R)
    # struct.md is maintained by hand since round 2 (the 4c addendum, the round-3 section); write_md(R) wrote round 1's
    # version from R and is kept for reference only (it reads the v1 result layout)
    if "md" in todo:
        write_md(R["v1"] | {k: v for k, v in R.items() if k == "4c"})


if __name__ == "__main__":
    main()
