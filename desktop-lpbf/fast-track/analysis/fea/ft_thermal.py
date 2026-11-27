"""Thermal FE of FT-1's heated cassette (cases 1-3 of the fast-track FEA, #260).

Geometry comes from the parametric model (cad/ft_model.py: build(state, pz), P, levels()), so the script re-runs on a
changed model. Each body (substrate, heater plate, rope, well block, standoffs, deck, enclosure floor, rod, gland,
rod clamp, the X-VSR20A's platform, column, body and riser, the recoater stage, the nozzle and the collector) is
exported to BREP and meshed on its own with gmsh (linear tetrahedra). The bodies are joined by surface couplings
found by casting rays along each boundary face's outward normal:

  - faces that touch (gap < 0.06 mm) get a contact conductance h_c (by pair, estimates);
  - faces facing each other across a gas gap up to 6 mm get h = k_Ar / (gap + 2 g) + a grey-body radiation term
    (the 0.1 mm radial gap between the plate and the bore is one of these);
  - every other face loses heat by natural convection (orientation-dependent correlations, argon at the film
    temperature) and radiation to its surroundings: the enclosure air inside, the room outside;
  - the block top and the substrate (or powder) top between the nozzle and the collector see the 2.5 m/s slot
    cross-flow: laminar flat-plate correlation, combined with natural convection.

CalculiX can't carry an open-gap conductance in a heat-transfer step (its gap conductance needs mechanical contact)
or a heater controller, so the solve is done here: P1 conductivity and lumped capacity, Picard iterations on the
convection and radiation coefficients, the two heater powers as extra unknowns so that the substrate top centre and
the well-block thermocouple sit at their setpoints, and implicit Euler with PI or on/off control for transients.
`verify` checks the solver against CalculiX (ccx 2.21, C3D4 *HEAT TRANSFER, *FILM, *RADIATE, *DFLUX BF) on the
well block alone.

Run (worktree root):
  OMP_NUM_THREADS=1 /tmp/tools/capmem 3 /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/fea/ft_thermal.py steady
  ... ft_thermal.py verify | warmup | laser | md
Scratch goes to /tmp/workerA/thermal (FT_THERMAL_RUN); results to analysis/out/fea/ (thermal.json, PNGs).
Units inside: m, W, K (temperatures in °C where printed).
"""
from __future__ import annotations

import csv
import itertools
import json
import math
import os
import pathlib
import subprocess
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.spatial import cKDTree

HERE = pathlib.Path(__file__).resolve().parent
FT = HERE.parents[1]                                  # desktop-lpbf/fast-track
sys.path.insert(0, str(FT / "cad"))
import cadquery as cq  # noqa: E402
import ft_model as M  # noqa: E402
from lpbf_model import box, cyl, tube  # noqa: E402

OUT = FT / "analysis" / "out" / "fea"
RUN = pathlib.Path(os.environ.get("FT_THERMAL_RUN", "/tmp/workerA/thermal"))
HEAT_CSV = pathlib.Path(os.environ.get("FT_HEAT_CSV", "/tmp/ft-process/heat_input.csv"))
SIGMA = 5.670374e-8
G = 9.81
P = M.P

# ------------------------------------------------------------------------------------------------
# Inputs (sources in the comments; "est." = estimate)
# ------------------------------------------------------------------------------------------------
MAT = {   # k W/mK, rho kg/m3, cp J/kgK
    "al6061": dict(k=167.0, rho=2700.0, cp=896.0, src="6061-T6 at 25 °C (ASM Handbook vol. 2 / MatWeb); k ~175 at 200 °C"),
    "ss304": dict(k=16.2, rho=8000.0, cp=500.0, src="AISI 304 (Incropera Table A.1: k 14.9 at 300 K, 16.6 at 400 K)"),
    "macor": dict(k=1.46, rho=2520.0, cp=790.0, src="Corning Macor datasheet"),
    "rope": dict(k=0.05, rho=500.0, cp=840.0, src="est. (packed fibreglass rope, cf. glass-fibre insulation 0.04-0.06)"),
    "powder": dict(k=0.15, rho=1350.0, cp=900.0, src="est. (AlSi10Mg powder bed in argon, ~50 % packing: 0.1-0.3)"),
    "stage": dict(k=167.0, rho=1100.0, cp=896.0, src="Zaber stage envelope as aluminium with the density cut to ~40 % (hollow body, est.)"),
}
EPS = dict(al=0.10, sub=0.30, ss=0.30, macor=0.90, rope=0.90, stage=0.85, floor=0.20, powder=0.40)
H_CONTACT = {   # W/m2K for touching faces, by body-name pair (sorted); default below (est., gas-filled joints)
    ("heater plate", "substrate"): 2000.0,
    ("block", "standoffs"): 1000.0, ("deck", "standoffs"): 1000.0,
    ("deck", "floor"): 200.0,               # 10 mm plate resting on a 14 ga sheet: partial contact, est.
    ("heater plate", "rope"): 200.0, ("block", "rope"): 200.0,
    ("block", "powder"): 500.0, ("powder", "substrate"): 500.0,
}
H_CONTACT_DEFAULT = 2000.0
GAP_MAX = 6.0e-3          # m: beyond this, facing surfaces are treated as exposed (natural convection + radiation)
TOUCH = 0.06e-3           # m: below this the faces are in contact
T_REF_RAD = 450.0         # K: reference temperature of the radiation term across gas gaps (small next to conduction)
U_JET = 2.5               # m/s at the 45 x 4 mm slot (study)
T_ROOM = 25.0             # °C (study's T_AMB)
CASES_AIR = {"fan": 39.0, "still": 71.0}                 # box air, study (fast_track.py heat())
CUBE_AIR = {"fan": 36.0, "still": 61.0}                  # cube air, cad/out/checks.md
SET_SUB, SET_TC = 200.0, 200.0
H_RISER_BOTTOM = 50.0     # W/m2K from the stage bracket plate into the T-slot rails and bench at room temperature (est.)
Q_MAX = dict(plate=100.0, block=100.0)                  # 2 x 50 W each (study); the block may get 4 x 50 W
HEATER = dict(d=6.0, l=20.0)                            # plate heaters Ø6 x 20 mm, 24 V 50 W (lead, 2026-11-27)


def argon(Tk):
    """Argon at 1 atm: (k, nu, alpha, Pr). NIST WebBook (Lemmon and Jacobsen 2004 transport), power-law fits 300-500 K."""
    Tk = np.asarray(Tk, dtype=float)
    k = 0.0177 * (Tk / 300.0) ** 0.79
    mu = 22.7e-6 * (Tk / 300.0) ** 0.80
    rho = 101325.0 * 39.948e-3 / (8.314462 * Tk)
    cp = 520.3
    return k, mu / rho, k / (rho * cp), mu * cp / k


def h_natural(dT, orient, L, Tf):
    """Natural convection h (W/m2K). orient: +1 face up, -1 face down, 0 vertical. Incropera eqs 9.26-9.32 (Churchill-
    Chu for vertical faces; 0.54/0.15 Ra^n for a hot face up, 0.27 Ra^0.25 for a hot face down; reversed when cold)."""
    k, nu, al, Pr = argon(Tf)
    Ra = G * np.abs(dT) / Tf * L ** 3 / (nu * al) + 1e-9
    vert = (0.825 + 0.387 * Ra ** (1 / 6) / (1 + (0.492 / Pr) ** (9 / 16)) ** (8 / 27)) ** 2
    up = np.where(Ra < 1e7, 0.54 * Ra ** 0.25, 0.15 * Ra ** (1 / 3))
    down = 0.27 * Ra ** 0.25
    hot = dT > 0
    up_like = (orient > 0) & hot | (orient < 0) & ~hot
    dn_like = (orient < 0) & hot | (orient > 0) & ~hot
    Nu = np.where(orient == 0, vert, np.where(up_like, np.maximum(up, 1.0), np.where(dn_like, np.maximum(down, 0.5), vert)))
    return Nu * k / L


def h_jet(xs, Tf):
    """Laminar flat plate, local: Nu_x = 0.332 Re_x^0.5 Pr^(1/3) (Incropera eq. 7.23), x from the slot exit."""
    k, nu, al, Pr = argon(Tf)
    xs = np.maximum(xs, 1e-3)
    return 0.332 * k / xs * np.sqrt(U_JET * xs / nu) * Pr ** (1 / 3)


# ------------------------------------------------------------------------------------------------
# Bodies from the model
# ------------------------------------------------------------------------------------------------
def find(parts, pid=None, name=None):
    for p in parts:
        if (pid is None or p.pid == pid) and (name is None or p.name.lower().startswith(name.lower())):
            return p
    return None


def bodies(state="FT-1", pz=0.0, powder=False, recoater="model"):
    """The thermal bodies of a state: list of dicts (name, shape, mat, eps, h mm, plus geometry helpers) and the
    sensor points (mm)."""
    parts = M.build(state, pz=pz)
    L = M.levels(state)
    cube = state == "FT-1V"
    zbed = L["floor_top"] + P["deck_t"] + P["so_l"] + P["well"][2]
    zt = zbed + pz
    R = P["plate_d"] / 2
    hp_z0 = zt - P["sub_t"] - P["hp_t"]
    zg = zt - P["sub_t"] - 7.0                                      # rope groove bottom (as in ft_model)
    B = []

    def add(name, shape, mat, eps, h, **kw):
        B.append(dict(name=name, shape=shape, mat=mat, eps=eps, h=h, **kw))

    add("substrate", cyl(R, (0, 0, zt - P["sub_t"]), "z", P["sub_t"]), "al6061", EPS["sub"], 2.0)
    hp = cyl(R, (0, 0, hp_z0), "z", P["hp_t"])
    hp = hp.cut(tube(R + 1, R - P["rope"], (0, 0, zg), "z", P["rope"]))
    hp = hp.cut(cyl(P["rod_od"] / 2 + 0.05, (0, 0, hp_z0 - 1), "z", P["socket"] + 1))
    hole_top = hp_z0 + P["heater_l"] + 0.5                         # heater holes as drilled in the model
    heaters = [((P["heater_r"] * math.cos(math.radians(a)), P["heater_r"] * math.sin(math.radians(a))),
                hole_top - HEATER["l"], hole_top) for a in (30.0, 150.0)]
    add("heater plate", hp, "al6061", EPS["al"], 2.0, src=dict(kind="plate", cyl=[(xy, z0, z1, HEATER["d"] / 2) for xy, z0, z1 in heaters]))
    add("rope", tube(R + 0.08, R - P["rope"], (0, 0, zg), "z", P["rope"]), "rope", EPS["rope"], 1.3)
    bw, bd, bh = P["well"]
    zb0 = zbed - bh
    blk = box(-bw / 2, bw / 2, -bd / 2, bd / 2, zb0, zbed).cut(cyl(P["bore"] / 2, (0, 0, zb0 - 1), "z", bh + 2))
    blk = blk.cut(box(P["ovf_x"][0], P["ovf_x"][1], -P["ovf_y"], P["ovf_y"], zb0 - 1, zbed + 1))
    add("block", blk, "al6061", EPS["al"], 3.0,
        src=dict(kind="block", xcyl=[((-bw / 2, 0.0), sy, zb0 + bh / 2, 3.0) for sy in (-30.0, 30.0)]))
    so = cq.Compound.makeCompound([cyl(P["so_d"] / 2, (sx, sy, zb0 - P["so_l"]), "z", P["so_l"])
                                   for sx in (-P["so_xy"], P["so_xy"]) for sy in (-P["so_xy"], P["so_xy"])])
    add("standoffs", so, "macor", EPS["macor"], 1.6)
    add("deck", find(parts, "MK-01").shape, "al6061", EPS["al"], 7.0)
    xc, yc = P["deck_c"]
    if cube:
        add("floor", find(parts, "MK-14").shape, "al6061", EPS["al"], 9.0)
    else:
        bx, by, _ = P["box_in"]
        t = P["box_t"]
        fl = box(xc - bx / 2 - t, xc + bx / 2 + t, yc - by / 2 - t, yc + by / 2 + t, L["floor_top"] - t, L["floor_top"])
        add("floor", fl.cut(cyl(10.0, (0, 0, L["floor_top"] - t - 1), "z", t + 2)), "ss304", EPS["floor"], 6.0)
    rod = find(parts, "MK-06")
    rin = P["rod_od"] / 2 - P["rod_wall"]
    add("rod", rod.shape, "ss304", EPS["ss"], 1.5, adiabatic=("r_lt", rin + 0.3))
    add("gland", find(parts, "MK-07").shape, "ss304", EPS["ss"], 3.0)
    if find(parts, "MK-15", "Rod clamp") is not None:
        add("clamp", find(parts, "MK-15", "Rod clamp").shape, "al6061", EPS["al"], 2.5)
        add("platform", find(parts, "M2", "X-VSR20A platform").shape, "stage", EPS["stage"], 6.0)
        add("column", find(parts, "M2", "X-VSR20A lift column").shape, "stage", EPS["stage"], 6.0)
        add("stage body", find(parts, "M2", "Zaber X-VSR20A").shape, "stage", EPS["stage"], 9.0)
        rs = find(parts, "MK-15", "Piston-stage bracket").shape
        add("riser", rs, "al6061", EPS["al"], 9.0, fixed=("z_lt", rs.BoundingBox().zmin + 0.5, H_RISER_BOTTOM))
    rc = find(parts, "M1b") or find(parts, None, "Zaber X-LS")
    if rc is not None:
        shp = rc.shape
        if recoater == "X-LSM100B":     # lead, 2026-11-27: 21 mm tall body, 239 mm long, same footprint line
            bb = shp.BoundingBox()
            shp = box(bb.xmin, bb.xmin + 239.0, bb.ymin + 10, bb.ymax - 10, bb.zmin, bb.zmin + 21.0)
        add("recoater stage", shp, "stage", EPS["stage"], 9.0)
    add("nozzle", find(parts, "MK-11", "Slot nozzle").shape, "ss304", EPS["ss"], 2.5)
    add("collector", find(parts, "MK-11", "Exhaust collector").shape, "ss304", EPS["ss"], 2.5)
    if powder and pz < -0.5:
        add("powder", cyl(P["bore"] / 2 - 0.005, (0, 0, zt), "z", -pz), "powder", EPS["powder"], 2.0)
    sens = dict(sub_top=(0.0, 0.0, zt), tc_block=(-30.0, 10.0, zb0 + bh / 2),
                tc_plate=(P["heater_r"] * math.cos(math.radians(270)), P["heater_r"] * math.sin(math.radians(270)), hole_top))
    geo = dict(state=state, pz=pz, zbed=zbed, zt=zt, zb0=zb0, hp_z0=hp_z0, under=L["under"], floor_top=L["floor_top"],
               cube=cube, xc=xc, yc=yc, gland=(L["gland_bot"], L["under"]), deck_top=L["floor_top"] + P["deck_t"],
               cube_in=P["cube_in"] if cube else None)
    return B, sens, geo


# ------------------------------------------------------------------------------------------------
# Meshing (one gmsh session per body), boundary faces
# ------------------------------------------------------------------------------------------------
def mesh_body(b, scale=1.0):
    import gmsh
    RUN.mkdir(parents=True, exist_ok=True)
    path = RUN / f"{b['name'].replace(' ', '_')}.brep"
    b["shape"].exportBrep(str(path))
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add(b["name"])
    gmsh.model.occ.importShapes(str(path))
    gmsh.model.occ.synchronize()
    h = b["h"] * scale
    gmsh.option.setNumber("Mesh.MeshSizeMax", h)
    gmsh.option.setNumber("Mesh.MeshSizeMin", h / 4)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 12)
    gmsh.option.setNumber("Mesh.ElementOrder", 1)
    gmsh.option.setNumber("Mesh.Algorithm3D", 10)
    gmsh.option.setNumber("General.NumThreads", 1)
    try:
        gmsh.model.mesh.generate(3)
    except Exception:  # noqa: BLE001
        gmsh.model.mesh.clear()
        gmsh.option.setNumber("Mesh.Algorithm3D", 1)
        gmsh.model.mesh.generate(3)
    ntags, xyz, _ = gmsh.model.mesh.getNodes()
    tets = [en.reshape(-1, 4) for et, _, en in zip(*gmsh.model.mesh.getElements(3)) if et == 4]
    gmsh.finalize()
    tets = np.vstack(tets).astype(np.int64)
    idx = np.full(int(ntags.max()) + 1, -1, dtype=np.int64)
    idx[ntags.astype(np.int64)] = np.arange(len(ntags))
    tets = idx[tets]
    used = np.unique(tets)
    remap = np.full(len(ntags), -1, dtype=np.int64)
    remap[used] = np.arange(len(used))
    X = xyz.reshape(-1, 3)[used] * 1e-3
    tets = remap[tets]
    c = X[tets]
    vol = np.einsum("ij,ij->i", np.cross(c[:, 1] - c[:, 0], c[:, 2] - c[:, 0]), c[:, 3] - c[:, 0])
    neg = vol < 0
    tets[neg] = tets[neg][:, [0, 2, 1, 3]]
    return X, tets


def boundary(X, tets):
    """Boundary triangles with outward orientation."""
    f = np.vstack([tets[:, [0, 1, 2]], tets[:, [0, 1, 3]], tets[:, [0, 2, 3]], tets[:, [1, 2, 3]]])
    opp = np.concatenate([tets[:, 3], tets[:, 2], tets[:, 1], tets[:, 0]])
    s = np.sort(f, axis=1).astype(np.int64)
    nmax = int(tets.max()) + 1
    key = (s[:, 0] * nmax + s[:, 1]) * nmax + s[:, 2]
    _, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
    once = cnt[inv.ravel()] == 1
    f, opp = f[once], opp[once]
    a, b_, c = X[f[:, 0]], X[f[:, 1]], X[f[:, 2]]
    n = np.cross(b_ - a, c - a)
    flip = np.einsum("ij,ij->i", n, X[opp] - a) > 0
    f[flip] = f[flip][:, [0, 2, 1]]
    n[flip] *= -1
    area = 0.5 * np.linalg.norm(n, axis=1)
    return f, n / (2 * area[:, None]), area


# ------------------------------------------------------------------------------------------------
# Model assembly
# ------------------------------------------------------------------------------------------------
QP = np.array([[2 / 3, 1 / 6, 1 / 6], [1 / 6, 2 / 3, 1 / 6], [1 / 6, 1 / 6, 2 / 3]])


def raycast(o, d, tmax, tri_xyz, tree, rmax):
    """First hit (t, tri, u, v) of rays o + t d (t in [0, tmax]) on triangles; -1 where none. Möller-Trumbore."""
    n = len(o)
    best_t = np.full(n, np.inf)
    best_i = np.full(n, -1)
    best_uv = np.zeros((n, 2))
    dist, _ = tree.query(o + d * (tmax / 2), k=1, distance_upper_bound=tmax / 2 + rmax)
    sel = np.where(np.isfinite(dist))[0]
    for c0 in range(0, len(sel), 20000):
        s = sel[c0:c0 + 20000]
        cand = tree.query_ball_point(o[s] + d[s] * (tmax / 2), r=tmax / 2 + rmax)
        lens = np.fromiter((len(c) for c in cand), dtype=np.int64, count=len(cand))
        if lens.sum() == 0:
            continue
        ri = np.repeat(s, lens)
        ti = np.fromiter(itertools.chain.from_iterable(cand), dtype=np.int64, count=int(lens.sum()))
        v0, v1, v2 = tri_xyz[ti, 0], tri_xyz[ti, 1], tri_xyz[ti, 2]
        e1, e2 = v1 - v0, v2 - v0
        dd = d[ri]
        pv = np.cross(dd, e2)
        det = np.einsum("ij,ij->i", e1, pv)
        ok = np.abs(det) > 1e-18
        inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
        tv = o[ri] - v0
        u = np.einsum("ij,ij->i", tv, pv) * inv
        qv = np.cross(tv, e1)
        v = np.einsum("ij,ij->i", dd, qv) * inv
        t = np.einsum("ij,ij->i", e2, qv) * inv
        hit = ok & (u >= -1e-9) & (v >= -1e-9) & (u + v <= 1 + 1e-9) & (t >= 0) & (t <= tmax)
        if not hit.any():
            continue
        ri, ti, t, u, v = ri[hit], ti[hit], t[hit], u[hit], v[hit]
        order = np.lexsort((t, ri))
        ri, ti, t, u, v = ri[order], ti[order], t[order], u[order], v[order]
        first = np.r_[True, ri[1:] != ri[:-1]]
        ri, ti, t, u, v = ri[first], ti[first], t[first], u[first], v[first]
        better = t < best_t[ri]
        best_t[ri[better]] = t[better]
        best_i[ri[better]] = ti[better]
        best_uv[ri[better]] = np.column_stack([u[better], v[better]])
    return best_t, best_i, best_uv


class Model:
    def __init__(self, state="FT-1", pz=0.0, air="fan", powder=False, scale=1.0, recoater="model", verbose=True):
        t0 = time.time()
        self.state, self.pz, self.air_case = state, pz, air
        Bs, sens, geo = bodies(state, pz, powder=powder, recoater=recoater)
        self.geo = geo
        self.T_in = (CUBE_AIR if geo["cube"] else CASES_AIR)[air] if isinstance(air, str) else float(air)
        self.T_out = T_ROOM
        Xs, Ts, offs = [], [], [0]
        for b in Bs:
            X, tets = mesh_body(b, scale)
            b["n0"], b["nn"], b["ne"] = offs[-1], len(X), len(tets)
            Xs.append(X)
            Ts.append(tets + offs[-1])
            offs.append(offs[-1] + len(X))
        self.B = Bs
        self.X = np.vstack(Xs)
        self.N = len(self.X)
        self.body_of_node = np.repeat(np.arange(len(Bs)), [b["nn"] for b in Bs])
        self.tets = Ts
        if verbose:
            print(f"  meshed {len(Bs)} bodies: {self.N} nodes, {sum(len(t) for t in Ts)} tets ({time.time() - t0:.0f} s)")
        self._assemble_volume()
        self._sources(sens)
        self._surfaces()
        if verbose:
            print(f"  assembled ({time.time() - t0:.0f} s): {len(self.cq['w'])} coupling points, {len(self.ex['w'])} exposed points")

    # ---- volume terms
    def _assemble_volume(self):
        rows, cols, vals = [], [], []
        C = np.zeros(self.N)
        self.vol_e = []
        for b, tets in zip(self.B, self.tets):
            m = MAT[b["mat"]]
            c = self.X[tets]
            J = np.stack([c[:, 1] - c[:, 0], c[:, 2] - c[:, 0], c[:, 3] - c[:, 0]], axis=2)   # columns = edges
            det = np.linalg.det(J)
            V = np.abs(det) / 6.0
            Ji = np.linalg.inv(J)                          # rows: grad of barycentric 1..3
            Gr = np.concatenate([-Ji.sum(axis=1, keepdims=True), Ji], axis=1)      # (ne, 4, 3)
            Ke = m["k"] * V[:, None, None] * np.einsum("eik,ejk->eij", Gr, Gr)
            rows.append(np.repeat(tets, 4, axis=1).ravel())
            cols.append(np.tile(tets, (1, 4)).ravel())
            vals.append(Ke.ravel())
            np.add.at(C, tets.ravel(), np.repeat(m["rho"] * m["cp"] * V / 4.0, 4))
            b["mass_kg"] = float(m["rho"] * V.sum())
            b["heat_cap_JK"] = float(m["rho"] * m["cp"] * V.sum())
            self.vol_e.append(V)
        self.Kc = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(self.N, self.N))
        self.C = C

    # ---- heater and sensor vectors
    def _sources(self, sens):
        self.src = {}
        for b, tets, V in zip(self.B, self.tets, self.vol_e):
            s = b.get("src")
            if not s:
                continue
            cen = self.X[tets].mean(axis=1) * 1e3
            inside = np.zeros(len(tets), bool)
            if s["kind"] == "plate":
                for (xy, z0, z1, r) in s["cyl"]:
                    inside |= (np.hypot(cen[:, 0] - xy[0], cen[:, 1] - xy[1]) <= r) & (cen[:, 2] >= z0) & (cen[:, 2] <= z1)
            else:
                for ((x0, x1), sy, zc, r) in s["xcyl"]:
                    inside |= (np.hypot(cen[:, 1] - sy, cen[:, 2] - zc) <= r) & (cen[:, 0] >= x0) & (cen[:, 0] <= x1)
            v = np.zeros(self.N)
            np.add.at(v, tets[inside].ravel(), np.repeat(V[inside] / 4.0, 4))
            self.src[s["kind"]] = v / v.sum()
            b["src_elems"] = int(inside.sum())
        self.sens = {}
        for k, p in sens.items():
            self.sens[k] = self._interp_vec(np.array(p))

    def _interp_vec(self, p_mm):
        """Vector e with e @ T = T at the point (barycentric in its tet, else the nearest node)."""
        p = p_mm * 1e-3
        e = np.zeros(self.N)
        for tets in self.tets:
            c = self.X[tets]
            lo, hi = c.min(axis=1) - 1e-9, c.max(axis=1) + 1e-9
            cand = np.where(np.all((p >= lo) & (p <= hi), axis=1))[0]
            for i in cand:
                J = np.column_stack([c[i, 1] - c[i, 0], c[i, 2] - c[i, 0], c[i, 3] - c[i, 0]])
                l = np.linalg.solve(J, p - c[i, 0])
                lam = np.r_[1 - l.sum(), l]
                if lam.min() >= -1e-6:
                    e[tets[i]] = lam
                    return e
        e[np.argmin(np.linalg.norm(self.X - p, axis=1))] = 1.0
        return e

    # ---- surfaces: couplings and exposed faces
    def _surfaces(self):
        g = self.geo
        S = []
        for bi, (b, tets) in enumerate(zip(self.B, self.tets)):
            f, n, A = boundary(self.X, tets)
            S.append(dict(f=f, n=n, A=A, xyz=self.X[f], cent=self.X[f].mean(axis=1)))
            bb = self.X[np.unique(f)]
            b["bb"] = np.r_[bb.min(0), bb.max(0)]
        trees = [cKDTree(s["cent"]) for s in S]
        rmax = [float(np.linalg.norm(s["xyz"] - s["cent"][:, None, :], axis=2).max()) for s in S]
        allF = np.vstack([s["f"] for s in S])          # global node ids of every face
        foff = np.cumsum([0] + [len(s["f"]) for s in S])[:-1]
        cq_, ex = {k: [] for k in ("na", "la", "nb", "lb", "w", "h", "d", "ba", "bb_")}, {k: [] for k in ("nodes", "lam", "w", "body", "orient", "env", "jet_x", "fixed_h")}
        eps_back = 0.05e-3
        tmax = GAP_MAX + eps_back
        for si, s in enumerate(S):
            b = self.B[si]
            nq = len(s["A"]) * 3
            lam = np.tile(QP, (len(s["A"]), 1))
            tri = np.repeat(np.arange(len(s["A"])), 3)
            p = np.einsum("qk,qkj->qj", lam, s["xyz"][tri])
            nrm = s["n"][tri]
            w = s["A"][tri] / 3.0
            best = np.full(nq, np.inf)
            hit_b = np.full(nq, -1)
            hit_t = np.full(nq, -1)
            hit_uv = np.zeros((nq, 2))
            for ti_, t in enumerate(S):
                if ti_ == si:
                    continue
                bbt = self.B[ti_]["bb"]
                if np.any(b["bb"][:3] > bbt[3:] + tmax) or np.any(bbt[:3] > b["bb"][3:] + tmax):
                    continue
                tt, it, uv = raycast(p - nrm * eps_back, nrm, tmax, t["xyz"], trees[ti_], rmax[ti_])
                ok = (it >= 0)
                ok[ok] &= np.einsum("ij,ij->i", nrm[ok], t["n"][it[ok]]) < -0.5
                better = ok & (tt < best)
                best[better], hit_b[better], hit_t[better], hit_uv[better] = tt[better], ti_, it[better], uv[better]
            cpl = hit_b >= 0
            # couplings
            idx = np.where(cpl)[0]
            if len(idx):
                gap = np.maximum(best[idx] - eps_back, 0.0)
                tb = hit_b[idx]
                tgt = allF[foff[tb] + hit_t[idx]]
                u, v = hit_uv[idx, 0], hit_uv[idx, 1]
                lb = np.column_stack([1 - u - v, u, v])
                hc = np.array([H_CONTACT.get(tuple(sorted((b["name"], self.B[k]["name"]))), H_CONTACT_DEFAULT) for k in tb])
                kgas = argon(T_REF_RAD)[0]
                lam_mfp = 0.11e-6 * T_REF_RAD / 473.0
                eA = b["eps"]
                eB = np.array([self.B[k]["eps"] for k in tb])
                eeff = 1.0 / (1.0 / eA + 1.0 / eB - 1.0)
                hgap = kgas / (gap + 2 * 2.8 * lam_mfp) + eeff * SIGMA * 4 * T_REF_RAD ** 3
                h = np.where(gap < TOUCH, hc, hgap)
                cq_["na"].append(s["f"][tri[idx]])
                cq_["la"].append(lam[idx])
                cq_["nb"].append(tgt)
                cq_["lb"].append(lb)
                cq_["w"].append(w[idx])
                cq_["h"].append(h)
                cq_["d"].append(gap)
                cq_["ba"].append(np.full(len(idx), si))
                cq_["bb_"].append(tb)
            # exposed
            idx = np.where(~cpl)[0]
            pm = p[idx] * 1e3
            keep = np.ones(len(idx), bool)
            if b.get("adiabatic"):
                kind, val = b["adiabatic"]
                if kind == "r_lt":
                    keep &= np.hypot(pm[:, 0], pm[:, 1]) >= val
            fixed = np.full(len(idx), np.nan)
            if b.get("fixed"):
                kind, val, hf = b["fixed"]
                fixed[(pm[:, 2] < val) & (nrm[idx, 2] < -0.9)] = hf
            idx, pm, fixed = idx[keep], pm[keep], fixed[keep]
            nz = nrm[idx, 2]
            orient = np.where(nz > 0.7, 1, np.where(nz < -0.7, -1, 0))
            if g["cube"]:
                ci = g["cube_in"] / 2
                inside = (pm[:, 2] > g["floor_top"] - 0.5) & (np.abs(pm[:, 0] - g["xc"]) < ci) & (np.abs(pm[:, 1] - g["yc"]) < ci)
            else:
                inside = pm[:, 2] > g["under"] + 0.5
            jet = (orient == 1) & (np.abs(pm[:, 2] - g["zbed"]) < 0.5) & (np.abs(pm[:, 0]) <= 22.5) & (pm[:, 1] > -27.0) & (pm[:, 1] < 27.0)
            ex["nodes"].append(s["f"][tri[idx]])
            ex["lam"].append(lam[idx])
            ex["w"].append(w[idx])
            ex["body"].append(np.full(len(idx), si))
            ex["orient"].append(orient)
            ex["env"].append(inside)
            ex["jet_x"].append(np.where(jet, (pm[:, 1] + 27.0) * 1e-3, np.nan))
            ex["fixed_h"].append(fixed)
        self.cq = {k: np.concatenate(v) for k, v in cq_.items()}
        self.ex = {k: np.concatenate(v) for k, v in ex.items()}
        # coupling matrix: each side carries half of its own points' conductance (symmetric, conservative)
        na, la, nb, lb, hw = self.cq["na"], self.cq["la"], self.cq["nb"], self.cq["lb"], 0.5 * self.cq["h"] * self.cq["w"]
        nodes = np.hstack([na, nb])
        Nv = np.hstack([la, -lb])
        vals = hw[:, None, None] * Nv[:, :, None] * Nv[:, None, :]
        self.Kp = sp.csr_matrix((vals.ravel(), (np.repeat(nodes, 6, axis=1).ravel(), np.tile(nodes, (1, 6)).ravel())), shape=(self.N, self.N))
        # exposed-face characteristic lengths per body (bounding box)
        Lv, Lh = [], []
        for b in self.B:
            d = (b["bb"][3:] - b["bb"][:3])
            Lv.append(max(min(d[2], 0.2), 0.003))
            Lh.append(max(d[0] * d[1] / (2 * (d[0] + d[1])), 0.003))
        e = self.ex
        e["Lv"], e["Lh"] = np.array(Lv)[e["body"]], np.array(Lh)[e["body"]]
        e["eps"] = np.array([b["eps"] for b in self.B])[e["body"]]
        e["Tinf"] = np.where(e["env"], self.T_in, self.T_out)

    # ---- Robin terms at a temperature field
    def robin(self, T, T_in=None):
        e = self.ex
        Tinf = e["Tinf"] if T_in is None else np.where(e["env"], T_in, self.T_out)
        Tq = np.einsum("qk,qk->q", e["lam"], T[e["nodes"]])
        Tf = 0.5 * (Tq + Tinf) + 273.15
        L = np.where(e["orient"] == 0, e["Lv"], e["Lh"])
        hn = h_natural(Tq - Tinf, e["orient"], L, Tf)
        jet = np.isfinite(e["jet_x"])
        hc = hn.copy()
        if jet.any():
            hf = h_jet(e["jet_x"][jet], Tf[jet])
            hc[jet] = (hf ** 3 + hn[jet] ** 3) ** (1 / 3)
        Tk, Ts = Tq + 273.15, Tinf + 273.15
        hr = e["eps"] * SIGMA * (Tk ** 2 + Ts ** 2) * (Tk + Ts)
        h = hc + hr
        fx = np.isfinite(e["fixed_h"])
        h[fx] = e["fixed_h"][fx]
        Tinf = np.where(fx, self.T_out, Tinf)
        hw = h * e["w"]
        vals = hw[:, None, None] * e["lam"][:, :, None] * e["lam"][:, None, :]
        nd = e["nodes"]
        K = sp.csr_matrix((vals.ravel(), (np.repeat(nd, 3, axis=1).ravel(), np.tile(nd, (1, 3)).ravel())), shape=(self.N, self.N))
        f = np.zeros(self.N)
        np.add.at(f, nd.ravel(), (hw * Tinf)[:, None].repeat(3, axis=1).ravel() * e["lam"].ravel())
        self._last = dict(h=h, hc=hc, hr=hr, Tq=Tq, Tinf=Tinf)
        return K, f

    # ---- steady state with the heaters controlled (or fixed)
    def steady(self, setp=(SET_SUB, SET_TC), fixed=None, laser_W=0.0, laser_vec=None, T0=None, tol=0.005, it_max=40, verbose=False,
               sensor_plate="sub_top", T_in=None):
        """fixed: dict(plate=W or None, block=W or None) to fix a heater instead of controlling it. Controlled heaters
        that would need negative power are switched off (Q = 0) and the setpoint is dropped."""
        T = np.full(self.N, 150.0) if T0 is None else T0.copy()
        fixed = dict(fixed or {})
        ctrl = [k for k in ("plate", "block") if fixed.get(k) is None]
        target = {"plate": (sensor_plate, setp[0]), "block": ("tc_block", setp[1])}
        for it in range(it_max):
            Kr, fr = self.robin(T, T_in)
            A = (self.Kc + self.Kp + Kr).tocsc()
            lu = spla.splu(A)
            rhs = fr.copy()
            for k, q in fixed.items():
                if q:
                    rhs += q * self.src[k]
            if laser_W:
                rhs += laser_W * laser_vec
            T0_ = lu.solve(rhs)
            sol = {k: lu.solve(self.src[k]) for k in ctrl}
            act = list(ctrl)
            Q = {}
            for _ in range(3):
                if not act:
                    break
                Mx = np.array([[self.sens[target[c][0]] @ sol[a] for a in act] for c in act])
                r = np.array([target[c][1] - self.sens[target[c][0]] @ T0_ for c in act])
                qv = np.linalg.solve(Mx, r)
                Q = dict(zip(act, qv))
                neg = [k for k in act if Q[k] < 0]
                if not neg:
                    break
                act = [k for k in act if k not in neg]
                Q = {}
            Tn = T0_ + sum(Q.get(k, 0.0) * sol[k] for k in Q)
            Qall = {k: (fixed[k] if k in fixed else Q.get(k, 0.0)) for k in ("plate", "block")}
            dTm = np.abs(Tn - T).max()
            T = Tn if it == 0 else 0.3 * T + 0.7 * Tn
            if verbose:
                print(f"    it {it}: Q {Qall}, dT {dTm:.3f}")
            if dTm < tol:
                break
        self.Kr = Kr
        return T, Qall

    def at(self, T, key):
        return float(self.sens[key] @ T)

    # ---- energy balance by body and by surface group
    def balance(self, T, Q, laser_W=0.0):
        Kr, fr = self.robin(T)
        e, l = self.ex, self._last
        q = l["h"] * e["w"] * (l["Tq"] - l["Tinf"])
        out = {}
        for bi, b in enumerate(self.B):
            m = e["body"] == bi
            out[b["name"]] = dict(conv_rad_W=float(q[m].sum()), fixed_W=float(q[m & np.isfinite(e["fixed_h"])].sum()))
        jet = np.isfinite(e["jet_x"])
        c = self.cq
        Ta = np.einsum("qk,qk->q", c["la"], T[c["na"]])
        Tb = np.einsum("qk,qk->q", c["lb"], T[c["nb"]])
        qc = 0.5 * c["h"] * c["w"] * (Ta - Tb)
        names = [b["name"] for b in self.B]
        F = np.zeros((len(names), len(names)))
        np.add.at(F, (c["ba"], c["bb_"]), qc)
        F = F - F.T
        return dict(bodies=out, jet_W=float(q[jet].sum()), exposed_total_W=float(q.sum()), names=names, flows=F,
                    heaters_W=float(sum(Q.values())), laser_W=laser_W)


# ------------------------------------------------------------------------------------------------
# Post-processing helpers
# ------------------------------------------------------------------------------------------------
def body_nodes(m, name):
    for b in m.B:
        if b["name"] == name:
            return np.arange(b["n0"], b["n0"] + b["nn"])
    return np.array([], dtype=int)


def stats(m, T, name):
    ids = body_nodes(m, name)
    if not len(ids):
        return None
    return dict(min=round(float(T[ids].min()), 2), mean=round(float(T[ids].mean()), 2), max=round(float(T[ids].max()), 2))


def substrate_top(m, T, r_mm=15.0):
    ids = body_nodes(m, "substrate")
    p = m.X[ids] * 1e3
    top = ids[(np.abs(p[:, 2] - m.geo["zt"]) < 1e-3) & (np.hypot(p[:, 0], p[:, 1]) <= r_mm + 1e-6)]
    return dict(min=round(float(T[top].min()), 2), max=round(float(T[top].max()), 2), range_K=round(float(np.ptp(T[top])), 2),
                n=int(len(top)))


def clearance(m, T, alpha=23.6e-6, T0=20.0, dz=2.0):
    """Radial clearance change along the plate's engagement: plate rim growth = alpha R mean(ΔT) over the plate's cross
    section (free disc, plane stress: exact for any radial profile); bore growth = alpha R mean(ΔT) over the block's cross
    section at that height (near-uniform block). Positive = the gap opens."""
    out = []
    pl = np.r_[body_nodes(m, "heater plate"), body_nodes(m, "substrate")]
    bk = body_nodes(m, "block")
    zp, zk = m.X[pl, 2] * 1e3, m.X[bk, 2] * 1e3
    rb = np.hypot(m.X[bk, 0], m.X[bk, 1]) * 1e3
    z0 = max(m.geo["zt"] - P["sub_t"] - P["hp_t"], m.geo["zb0"])
    z1 = m.geo["zt"]
    for z in np.arange(z0 + dz / 2, z1, dz):
        a = np.abs(zp - z) <= dz / 2
        b = (np.abs(zk - z) <= dz / 2)
        bw = b & (rb <= P["bore"] / 2 + 3.0)
        if a.sum() < 3 or bw.sum() < 3:
            continue
        Tp, Tb, Tbw = T[pl[a]].mean(), T[bk[b]].mean(), T[bk[bw]].mean()
        dc = alpha * (P["bore"] / 2 * (Tb - T0) - P["plate_d"] / 2 * (Tp - T0)) * 1e3
        out.append(dict(z_mm=round(float(z), 1), T_plate=round(float(Tp), 2), T_bore_wall=round(float(Tbw), 2), T_block=round(float(Tb), 2),
                        dT_plate_minus_bore=round(float(Tp - Tbw), 2), d_clearance_um=round(float(dc * 1e3), 2)))
    return out


def summarize(m, T, Q, label):
    g = m.geo
    s = dict(label=label, state=m.state, pz=m.pz, T_in=m.T_in, T_room=m.T_out, nodes=m.N,
             heaters_W={k: round(v, 2) for k, v in Q.items()}, heaters_total_W=round(sum(Q.values()), 2),
             sensors={k: round(m.at(T, k), 2) for k in m.sens},
             substrate_top_r15=substrate_top(m, T, 15.0), substrate_top_r19=substrate_top(m, T, 19.5),
             bodies={b["name"]: stats(m, T, b["name"]) for b in m.B})
    # O-rings: the rod surface at the gland's upper and lower thirds; and the gland bore
    rod = body_nodes(m, "rod")
    pr = m.X[rod] * 1e3
    zb, zu = g["gland"]
    outer = np.hypot(pr[:, 0], pr[:, 1]) > P["rod_od"] / 2 - 0.2
    for nm, zz in (("oring_upper", zu - 3.0), ("oring_lower", zb + 3.0)):
        sel = outer & (np.abs(pr[:, 2] - zz) < 1.5)
        s[nm] = round(float(T[rod[sel]].mean()), 2) if sel.any() else None
    # deck under the recoater stage, and deck near the well
    dk = body_nodes(m, "deck")
    pd_ = m.X[dk] * 1e3
    rc = [b for b in m.B if b["name"] == "recoater stage"]
    if rc:
        bb = rc[0]["bb"] * 1e3
        sel = (pd_[:, 0] > bb[0]) & (pd_[:, 0] < bb[3]) & (pd_[:, 1] > bb[1]) & (pd_[:, 1] < bb[4]) & (np.abs(pd_[:, 2] - g["deck_top"]) < 0.01)
        s["deck_under_recoater"] = dict(mean=round(float(T[dk[sel]].mean()), 2), max=round(float(T[dk[sel]].max()), 2))
    s["clearance"] = clearance(m, T)
    bal = m.balance(T, Q)
    nm = bal["names"]
    F = bal["flows"]
    grp = lambda names: [nm.index(n) for n in names if n in nm]   # noqa: E731
    plate_g = grp(["substrate", "heater plate", "rope"])
    s["flows_W"] = dict(
        plate_stack_to_block=round(float(F[np.ix_(plate_g, grp(["block"]))].sum()), 3),
        plate_stack_to_rod=round(float(F[np.ix_(plate_g, grp(["rod"]))].sum()), 3),
        plate_stack_to_powder=round(float(F[np.ix_(plate_g, grp(["powder"]))].sum()), 3),
        plate_stack_exposed=round(sum(bal["bodies"][n]["conv_rad_W"] for n in ("substrate", "heater plate", "rope") if n in bal["bodies"]), 3),
        rod_to_clamp=round(float(F[np.ix_(grp(["rod"]), grp(["clamp"]))].sum()), 3),
        rod_to_gland=round(float(F[np.ix_(grp(["rod"]), grp(["gland"]))].sum()), 3),
        block_to_standoffs=round(float(F[np.ix_(grp(["block"]), grp(["standoffs"]))].sum()), 3),
        block_to_nozzle_collector=round(float(F[np.ix_(grp(["block"]), grp(["nozzle", "collector"]))].sum()), 3),
        deck_to_floor=round(float(F[np.ix_(grp(["deck"]), grp(["floor"]))].sum()), 3),
        jet_faces=round(bal["jet_W"], 3), exposed_total=round(bal["exposed_total_W"], 3),
        exposed_by_body={k: round(v["conv_rad_W"], 3) for k, v in bal["bodies"].items()})
    s["heat_cap_JK"] = {b["name"]: round(b["heat_cap_JK"], 1) for b in m.B}
    s["mass_kg"] = {b["name"]: round(b["mass_kg"], 4) for b in m.B}
    return s


# ------------------------------------------------------------------------------------------------
# Rendering (child process, as fea.py does)
# ------------------------------------------------------------------------------------------------
RENDER = FT.parent / "analysis" / "fea" / "render_fea.py"


def render(m, T, path, title, names=None, view=(-1.0, -1.5, 0.8), clim=None, zoom=1.3, clip_y=None):
    tris, keep = [], []
    for b, tets in zip(m.B, m.tets):
        if names and b["name"] not in names:
            continue
        f, n, A = boundary(m.X, tets)
        if clip_y is not None:
            cen = m.X[f].mean(axis=1) * 1e3
            f = f[cen[:, 1] <= clip_y]
        tris.append(f)
    f = np.vstack(tris)
    used, inv = np.unique(f, return_inverse=True)
    pts = m.X[used] * 1e3
    RUN.mkdir(parents=True, exist_ok=True)
    npz = RUN / f"render_{pathlib.Path(path).stem}.npz"
    diag = float(np.linalg.norm(pts.max(0) - pts.min(0)))
    opt = dict(path=str(path), title=title, view=list(view), up=[0, 0, 1], label="T (°C)", scale=0.0,
               clim=None if clim is None else [float(c) for c in clim], mark=None, diag=diag, zoom=zoom, cmap="inferno")
    np.savez(npz, pts=pts, tri=inv.reshape(-1, 3), U=np.zeros_like(pts), s=T[used], opt=json.dumps(opt))
    r = subprocess.run([sys.executable, str(RENDER), str(npz)], capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        print(f"  render failed: {r.stderr[-600:]}")


# ------------------------------------------------------------------------------------------------
# Cases
# ------------------------------------------------------------------------------------------------
def load_json():
    p = OUT / "thermal.json"
    return json.loads(p.read_text()) if p.exists() else {}


def save_json(R):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "thermal.json").write_text(json.dumps(R, indent=1, default=float))


def stamp():
    try:
        h = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=FT, capture_output=True, text=True).stdout.strip()
    except Exception:  # noqa: BLE001
        h = "unknown"
    return dict(utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), commit=h)


def case_steady(R, which):
    R.setdefault("steady", {})
    runs = {
        "ft1_pz0_fan": dict(state="FT-1", pz=0.0, air="fan"),
        "ft1_pz0_still": dict(state="FT-1", pz=0.0, air="still"),
        "ft1_pz-15_fan_powder": dict(state="FT-1", pz=-15.0, air="fan", powder=True),
        "ft1_pz-15_still_powder": dict(state="FT-1", pz=-15.0, air="still", powder=True),
        "ft1v_pz0_fan": dict(state="FT-1V", pz=0.0, air="fan"),
        "ft1v_pz0_still": dict(state="FT-1V", pz=0.0, air="still"),
        "ft1_pz0_fan_fine": dict(state="FT-1", pz=0.0, air="fan", scale=0.7),
        "ft1_pz0_fan_lsm100b": dict(state="FT-1", pz=0.0, air="fan", recoater="X-LSM100B"),
    }
    for key in which:
        kw = runs[key]
        t0 = time.time()
        print(f"case 1 steady {key}")
        m = Model(**kw)
        T, Q = m.steady(verbose=False)
        s = summarize(m, T, Q, key)
        s["run"] = dict(stamp(), seconds=round(time.time() - t0, 1), mesh_scale=kw.get("scale", 1.0))
        R["steady"][key] = s
        print(f"  Q {s['heaters_W']} W; sub top r15 {s['substrate_top_r15']}; TC plate {s['sensors']['tc_plate']}; "
              f"platform {s['bodies'].get('platform')}; o-rings {s['oring_upper']}/{s['oring_lower']}; {time.time() - t0:.0f} s")
        if key in ("ft1_pz0_fan", "ft1_pz-15_fan_powder"):
            png = f"thermal-{key.replace('_', '-')}.png"
            names = ["substrate", "heater plate", "rope", "block", "standoffs", "deck", "rod", "gland", "clamp", "platform", "column",
                     "stage body", "nozzle", "collector", "recoater stage", "powder"]
            render(m, T, OUT / png, f"FT-1 steady, plate at pz = {m.pz:g} mm, box air {m.T_in:g} °C: heaters "
                   f"{Q['plate']:.1f} W plate + {Q['block']:.1f} W block (section y <= 0)", names=names, clip_y=0.0,
                   view=(0.25, -1.0, 0.35), zoom=1.6)
            s["png"] = png
        save_json(R)


def main():
    args = sys.argv[1:] or ["steady"]
    R = load_json()
    if args[0] == "steady":
        which = args[1:] or ["ft1_pz0_fan", "ft1_pz0_still", "ft1_pz-15_fan_powder", "ft1v_pz0_fan"]
        case_steady(R, which)
    save_json(R)


if __name__ == "__main__":
    main()
