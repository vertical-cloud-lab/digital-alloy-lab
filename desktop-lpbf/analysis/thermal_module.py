"""Axisymmetric CalculiX heat-transfer model of the heated build modules S25, M50 and L75 (issue #260, PR #266).

It answers: what heater power holds the plate top centre at the set point; what the bore seal, the spigot O-ring,
the rod-gland O-rings and the Z-coupling magnet see; how much heat goes into the chamber floor; how long the plate
takes to heat up, and to cool to the door-interlock temperature.

Model: an r-z half-section, axisymmetric about the module axis, z = 0 at the powder plane. Every part is a
rectangle in r-z, so the mesh is a conformal structured grid of 8-node axisymmetric quads (CAX8) built here
(no gmsh). All dimensions come from cad/module_params.py. Thin gaps and contact faces are thin element layers whose
conductivity gives the stated conductance (k = h * t). Material and boundary-condition assumptions are the named
constants below.

Units inside ccx: mm, t, s, mJ (so power in mW). k in W/m.K is unchanged; h in W/m2.K is x1e-3; the
Stefan-Boltzmann constant is 5.669e-11; density in kg/m3 is x1e-12; specific heat in J/kg.K is x1e6. CalculiX gives
the reaction heat (RFL) of a CAX model for a 2-degree sector, so it is x180 for the whole ring (checked against
the analytic annulus, film, radiation and body-flux cases in sanity()).

Run:   python desktop-lpbf/analysis/thermal_module.py          all cases (~10 min on 4 cores)
       python desktop-lpbf/analysis/thermal_module.py quick    M50 cases 1, 2 and the cool-down only
       python desktop-lpbf/analysis/thermal_module.py sanity   the unit and convention checks only
Scratch (.inp/.dat/.frd) goes to /tmp/thermal-run/ (THERMAL_RUN overrides); results to analysis/out/thermal/.
"""
from __future__ import annotations

import concurrent.futures as cf
import contextlib
import io
import json
import math
import os
import pathlib
import subprocess
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "cad"))
import module_params as MP  # noqa: E402

OUT = HERE / "out" / "thermal"
RUN = pathlib.Path(os.environ.get("THERMAL_RUN", "/tmp/thermal-run"))
WORKERS = int(os.environ.get("THERMAL_WORKERS", "4"))

# ---------------------------------------------------------------- assumptions (W, m, K unless noted)
SIGMA = 5.669e-8
T_ROOM = 25.0                    # air under the floor, rod-end coupling
H_UNDER, EPS_UNDER = 5.0, 0.3    # natural convection + radiation on the module outside, under the floor
H_ROD_END = 10.0                 # rod end with the NdFeB pot-magnet coupling
H_TOP_D50 = 17.0                 # argon cross-flow 2 m/s over a 50 mm plate; h ~ D^-0.5
EPS_POWDER, EPS_BARE = 0.5, 0.1
H_PB, T_PB = 2000.0, 0.1         # plate-block preloaded Al-Al face, as a 0.1 mm layer (mm)
H_FF, T_FF = 1500.0, 0.1         # module flange pulled against the floor underside, as a 0.1 mm layer (mm)
EPS_BREAK = 0.15                 # block underside, 2 polished 316 shields, head top: radiation across the break
K_SEAL, K_FKM, K_POWDER = 0.10, 0.20, 0.20
ORING_GROOVE_D = 90.2            # SPIGOT_ORING groove diameter on the spigot OD (module_params comment)
ORING_Z, ORING_DEPTH, ORING_W = -14.0, (MP.PORT_D - ORING_GROOVE_D) / 2, 4.8   # FKM O-ring band (mm)
SEAL_BELOW_HEAD_TOP, SEAL_H, SEAL_DEPTH = 8.0, 6.0, 2.0   # felt + PTFE bore seal on the piston-head rim (mm)
GLAND_CLR, GLAND_DEPTH, GLAND_W, GLAND_INSET = 0.10, 2.3, 3.6, 2.6   # double FKM rod gland (mm)
STRIKER_T = 5.0                  # rod end: 430 striker (5 mm) under a potted end cap (ROD_END_T - 5); coupling face below
R_FLOOR = 120.0                  # floor modelled to r = 120 mm, edge held at the chamber temperature
HEATER_DZ = 3.0                  # heater ring half-height (mm)
ALPHA = dict(AL=23.6e-6, SS=16.5e-6)
T_WATER = 30.0                   # Tier B cooled faces
FLANGE_BAND = 5.0                # Tier B: cooled band on the module-flange underside (mm, outer rim inwards)
LIMITS = dict(seal=204.0, oring=200.0, oring_pref=150.0, gland=200.0, magnet=80.0, tco=MP.TCO_A)
H0 = 1.0                         # baseline element size (mm) in the module; grows to 4x at the floor edge
H0_TRANSIENT = 2.0               # transients run on the coarse mesh (its steady power is checked against H0)


def k_ar(T):
    return 0.018 + 4.5e-5 * (T - 25.0)


def k_air(T):
    return 0.0263 + 7.2e-5 * (T - 25.0)


def k_break(T):
    """Argon plus radiation across the BREAK_T gap with RAD_SHIELDS shields: q = sigma (T1^4 - T2^4) / ((N+1)(2/eps-1)),
    which a conductivity 4 sigma T^3 L / ((N+1)(2/eps-1)) evaluated at the local temperature reproduces exactly in 1D."""
    tk = T + 273.15
    return k_ar(T) + 4 * SIGMA * tk ** 3 * (MP.BREAK_T * 1e-3) / ((MP.RAD_SHIELDS + 1) * (2 / EPS_BREAK - 1))


# name: (k [W/mK] or k(T), rho [kg/m3], c [J/kgK])
MATS = {
    "AL6061": (167.0, 2700.0, 896.0),
    "SS316L": (16.0, 8000.0, 500.0),
    "MACOR": (MP.MACOR["k"], 2520.0, 790.0),
    "ARGON": (k_ar, 1.6, 520.0),
    "AIR": (k_air, 1.2, 1005.0),
    "BREAK": (k_break, 160.0, 500.0),     # gas + the two 0.1 mm shields' heat capacity smeared over the gap
    "SEAL": (K_SEAL, 1200.0, 1100.0),
    "FKM": (K_FKM, 1850.0, 1400.0),
    "POWDER": (K_POWDER, 1350.0, 900.0),
    "C_PB": (H_PB * T_PB * 1e-3, 2700.0, 896.0),
    "C_FF": (H_FF * T_FF * 1e-3, 8000.0, 500.0),
    "SS430": (26.1, 7740.0, 460.0),
    "POTTING": (0.5, 1500.0, 1000.0),
}
REGION_MAT = dict(plate="AL6061", cpb="C_PB", block="AL6061", heater="AL6061", gap_p="ARGON", gap_b="ARGON",
                  brk="BREAK", macor="MACOR", head="AL6061", gap_h="ARGON", seal="SEAL", rod="SS316L",
                  rodcap="SS316L", potting="POTTING", striker="SS430",
                  spigot="SS316L", mflange="SS316L", tube="SS316L", oring="FKM", sgap_ar="ARGON", sgap_air="AIR",
                  cff="C_FF", floor="AL6061", botfl="SS316L", ggap="ARGON", goring="FKM", cake="POWDER")
RODLIKE = ("rod", "rodcap", "potting", "striker")


def kfun(mat):
    k = MATS[mat][0]
    return k if callable(k) else (lambda T, k=k: k + 0 * T)


# ---------------------------------------------------------------- geometry
def geometry(key, z_p, tier="A", gap_fill="ARGON", clear_plate=None):
    """Rectangles (region, r0, r1, z0, z1) in paint order (later wins) and the levels the post-processing needs."""
    m = MP.MODULES[key]
    c = dict(MP.CLEAR[tier])
    if tier == "A":
        c["plate"] = m["plate_clear"]          # Tier A cold radial plate clearance is set per size
    if clear_plate is not None:
        c["plate"] = clear_plate
    g = dict(key=key, z_p=z_p, tier=tier, gap_fill=gap_fill)
    g["Rb"] = Rb = m["bore"] / 2
    g["Rp"] = Rp = Rb - c["plate"]
    g["Rk"] = Rk = Rb - c["block"]
    g["Ro"] = Ro = Rb + m["wall"]
    g["Rs"] = Rs = MP.PORT_D / 2
    g["Rsg"] = Rsg = Rs + MP.SPIGOT_FIT
    g["Rf"] = Rf = MP.FLANGE_D / 2
    Rbf = Ro + 8.0
    rri, rro = MP.ROD_ID / 2, MP.ROD_OD / 2
    rg = rro + GLAND_CLR
    zF = -MP.FLOOR_T
    zFb = zF - MP.FLANGE_T
    g["zBT"] = zBT = MP.Z_P_MIN - MP.STACK
    zBB = zBT - MP.BOT_FLANGE_T
    g["zpb"] = zpb = z_p - MP.PLATE_T
    zbb = zpb - MP.BLOCK_T
    zht = zbb - MP.BREAK_T
    g["zhb"] = zhb = zht - MP.HEAD_T
    g["zre"] = zre = zhb - MP.ROD_L
    g["rri"], g["rro"] = rri, rro
    zmid = 0.5 * (zpb + zbb)
    # vertical cartridges from below; axisymmetric stand-in: a ring at block mid-height (S25: one central cartridge)
    hr = (0.0, m["heater_d"] / 2) if key == "S25" else (0.45 * Rk, 0.65 * Rk)
    if m["standoff_r"] == 0:
        mc = (0.0, MP.MACOR["d"] / 2)
    else:
        w = m["n_standoffs"] * math.pi * MP.MACOR["d"] ** 2 / 4 / (2 * math.pi * m["standoff_r"])
        mc = (m["standoff_r"] - w / 2, m["standoff_r"] + w / 2)
    zs1 = zht - SEAL_BELOW_HEAD_TOP
    zo0, zo1 = ORING_Z - ORING_W / 2, ORING_Z + ORING_W / 2
    gl1 = (zBT - GLAND_INSET - GLAND_W / 2, zBT - GLAND_INSET + GLAND_W / 2)
    gl2 = (zBB + GLAND_INSET - GLAND_W / 2, zBB + GLAND_INSET + GLAND_W / 2)
    g["heater"] = (hr[0], hr[1], zmid - HEATER_DZ, zmid + HEATER_DZ)
    g["V_heater"] = math.pi * (hr[1] ** 2 - hr[0] ** 2) * 2 * HEATER_DZ          # mm3
    R = []

    def add(name, r0, r1, z0, z1):
        R.append((name, r0, r1, z0, z1))

    add("floor", Rsg, R_FLOOR, zF, 0.0)
    add("sgap_ar", Rs, Rsg, zo1, 0.0)
    add("sgap_air", Rs, Rsg, zF, zo0)
    add("spigot", Rb, Rs, zF, 0.0)
    add("oring", Rs - ORING_DEPTH, Rsg, zo0, zo1)
    add("mflange", Rb, Rf, zFb, zF)
    add("cff", Rsg, Rf, zF - T_FF, zF)
    add("tube", Rb, Ro, zBT, zFb)
    add("botfl", rg, Rbf, zBB, zBT)
    add("ggap", rro, rg, zBB, zBT)
    add("goring", rro, rg + GLAND_DEPTH, *gl1)
    add("goring", rro, rg + GLAND_DEPTH, *gl2)
    if z_p < 0:
        add("cake", 0.0, Rb, z_p, 0.0)
    add("plate", 0.0, Rp, zpb, z_p)
    add("gap_p", Rp, Rb, zpb, z_p)
    add("gap_b", Rk, Rb, zbb, zpb)
    add("cpb", 0.0, Rk, zpb - T_PB, zpb)
    add("block", 0.0, Rk, zbb, zpb - T_PB)
    add("heater", *g["heater"])
    add("brk", 0.0, Rb, zht, zbb)
    add("macor", mc[0], mc[1], zht, zbb)
    add("head", 0.0, Rk, zhb, zht)
    add("gap_h", Rk, Rb, zhb, zht)
    add("seal", Rb - SEAL_DEPTH, Rb, zs1 - SEAL_H, zs1)
    zcap = zre + MP.ROD_END_T
    add("rod", rri, rro, zcap, zhb)
    add("rodcap", rri, rro, zre + STRIKER_T, zcap)
    add("potting", 0.0, rri, zre + STRIKER_T, zcap)
    add("striker", 0.0, rro, zre, zre + STRIKER_T)
    g["rects"] = R
    g["extra_r"] = [Rf - FLANGE_BAND]
    mats = dict(REGION_MAT)
    mats["gap_p"] = mats["gap_b"] = gap_fill
    if tier == "B":
        mats["head"] = "SS316L"     # 316L head with a water channel (module_params docstring)
    g["mats"] = mats
    return g


def _refine(lines, size):
    out = [lines[0]]
    for a, b in zip(lines[:-1], lines[1:]):
        n = max(1, math.ceil((b - a) / size(0.5 * (a + b)) - 1e-9))
        out += [a + (b - a) * k / n for k in range(1, n + 1)]
    return np.array(out)


def _idx(arr, v):
    i = int(np.argmin(np.abs(arr - v)))
    assert abs(arr[i] - v) < 1e-6, (v, arr[i])
    return i


class Mesh:
    """Structured CAX8 mesh: cells (i, j) between grid lines rl[i]..rl[i+1], zl[j]..zl[j+1]; nodes on a
    (2nr+1) x (2nz+1) lattice (corners and mid-sides, no centres)."""
    OFFS = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 0), (2, 1), (1, 2), (0, 1)]          # CAX8 node order
    FACE = {1: [(0, 0), (1, 0), (2, 0)], 2: [(2, 0), (2, 1), (2, 2)],
            3: [(2, 2), (1, 2), (0, 2)], 4: [(0, 2), (0, 1), (0, 0)]}

    def __init__(self, g, h0):
        rects = g["rects"]
        Rf = MP.FLANGE_D / 2
        rs = sorted({round(v, 6) for rc in rects for v in rc[1:3]} | {0.0} | {round(v, 6) for v in g["extra_r"]})
        zs = sorted({round(v, 6) for rc in rects for v in rc[3:5]})
        self.rl = _refine(rs, lambda r: h0 if r < Rf + 2 else h0 * (1 + 3 * (r - Rf - 2) / (R_FLOOR - Rf - 2)))
        self.zl = _refine(zs, lambda z: h0)
        nr, nz = len(self.rl) - 1, len(self.zl) - 1
        self.names = list(dict.fromkeys(rc[0] for rc in rects))
        reg = np.full((nr, nz), -1, int)
        for name, r0, r1, z0, z1 in rects:
            reg[_idx(self.rl, r0):_idx(self.rl, r1), _idx(self.zl, z0):_idx(self.zl, z1)] = self.names.index(name)
        self.reg = reg
        act = reg >= 0
        self.Rn = np.empty(2 * nr + 1)
        self.Rn[0::2], self.Rn[1::2] = self.rl, 0.5 * (self.rl[:-1] + self.rl[1:])
        self.Zn = np.empty(2 * nz + 1)
        self.Zn[0::2], self.Zn[1::2] = self.zl, 0.5 * (self.zl[:-1] + self.zl[1:])
        I, J = np.nonzero(act)
        used = np.zeros((2 * nr + 1, 2 * nz + 1), bool)
        for di, dj in self.OFFS:
            used[2 * I + di, 2 * J + dj] = True
        nid = np.zeros(used.shape, int)
        nid[used] = np.arange(1, used.sum() + 1)
        self.nid, self.used = nid, used
        self.I, self.J = I, J
        self.ereg = reg[I, J]
        self.conn = np.stack([nid[2 * I + di, 2 * J + dj] for di, dj in self.OFFS], axis=1)
        self.eid = np.zeros((nr, nz), int)
        self.eid[I, J] = np.arange(1, len(I) + 1)
        self.nr, self.nz = nr, nz
        self.g = g
        A = np.pad(act, 1)
        free = {1: ~A[I + 1, J], 2: ~A[I + 2, J + 1], 3: ~A[I + 1, J + 2], 4: ~A[I, J + 1] & (I > 0)}
        self.bc = self._classify(free)

    def region(self, name):
        return np.nonzero(self.ereg == self.names.index(name))[0] if name in self.names else np.array([], int)

    def neighbour(self, e, face):
        di, dj = {1: (0, -1), 2: (1, 0), 3: (0, 1), 4: (-1, 0)}[face]
        i, j = self.I[e] + di, self.J[e] + dj
        if 0 <= i < self.nr and 0 <= j < self.nz and self.reg[i, j] >= 0:
            return self.names[self.reg[i, j]]
        return None

    def _classify(self, free):
        """Free faces -> 'top' (chamber), 'under' (air under the floor), 'rod' (rod in air), 'rodend', or adiabatic."""
        g = self.g
        out = {"top": [], "under": [], "rod": [], "rodend": []}
        for f, mask in free.items():
            for e in np.nonzero(mask)[0]:
                name = self.names[self.ereg[e]]
                i, j = self.I[e], self.J[e]
                r0, r1, z0, z1 = self.rl[i], self.rl[i + 1], self.zl[j], self.zl[j + 1]
                rm, zm = {1: (0.5 * (r0 + r1), z0), 2: (r1, 0.5 * (z0 + z1)), 3: (0.5 * (r0 + r1), z1),
                          4: (r0, 0.5 * (z0 + z1))}[f]
                n = {1: (0, -1), 2: (1, 0), 3: (0, 1), 4: (-1, 0)}[f]
                pr, pz = rm + 1e-3 * n[0], zm + 1e-3 * n[1]
                if f == 3 and abs(z1) < 1e-9:
                    if name != "floor":
                        out["top"].append((e, f))
                elif name == "floor":
                    continue                       # floor top and underside adiabatic; its edge is held at T_ch
                elif name in RODLIKE and f == 1 and abs(z0 - g["zre"]) < 1e-9:
                    out["rodend"].append((e, f))   # coupling face (pot magnet in the Z arm)
                elif pr < g["rri"] and name in RODLIKE:
                    continue                       # inside the hollow rod
                elif pr < g["Rb"] and g["zBT"] < pz < g["zhb"]:
                    continue                       # argon inside the cylinder, below the piston head
                else:
                    assert pz < -MP.FLOOR_T + 1e-6, (name, f, rm, zm)
                    out["rod" if name in RODLIKE else "under"].append((e, f))
        return out

    # --- field helpers -------------------------------------------------------------------------
    def lattice(self, T_by_node):
        L = np.full(self.used.shape, np.nan)
        L[self.used] = T_by_node[self.nid[self.used]]
        return L

    def elem_T(self, L, e):
        i, j = self.I[e], self.J[e]
        return np.array([L[2 * i + di, 2 * j + dj] for di, dj in self.OFFS])

    def nodes_of(self, elems):
        return np.unique(self.conn[elems].ravel())


# CAX8 shape functions on the reference square, nodes as in Mesh.OFFS
_XI = np.array([-1, 1, 1, -1, 0, 1, 0, -1], float)
_ET = np.array([-1, -1, 1, 1, -1, 0, 1, 0], float)


def shape(x, y):
    N, dx, dy = np.zeros(8), np.zeros(8), np.zeros(8)
    for a in range(8):
        xi, et = _XI[a], _ET[a]
        if xi != 0 and et != 0:
            N[a] = 0.25 * (1 + x * xi) * (1 + y * et) * (x * xi + y * et - 1)
            dx[a] = 0.25 * xi * (1 + y * et) * (2 * x * xi + y * et)
            dy[a] = 0.25 * et * (1 + x * xi) * (x * xi + 2 * y * et)
        elif xi == 0:
            N[a] = 0.5 * (1 - x * x) * (1 + y * et)
            dx[a] = -x * (1 + y * et)
            dy[a] = 0.5 * (1 - x * x) * et
        else:
            N[a] = 0.5 * (1 + x * xi) * (1 - y * y)
            dx[a] = 0.5 * xi * (1 - y * y)
            dy[a] = -y * (1 + x * xi)
    return N, dx, dy


_GP = [(-math.sqrt(0.6), 5 / 9), (0.0, 8 / 9), (math.sqrt(0.6), 5 / 9)]
GL = 1 / math.sqrt(3)       # 2-point Gauss line: where a CAX8 gradient is most accurate


def face_flux(mesh, L, elems, face, mat_of, at=1.0):
    """Heat flow (W) across each element next to `face`, positive in +r (faces 2, 4) or +z (faces 1, 3), from the
    CAX8 gradient at 3 Gauss points along a line parallel to the face. at = 1 is on the face; at = 0 is the element
    mid-line, the accurate choice for a thin gap layer that is one element across."""
    Q = 0.0
    for e in elems:
        i, j = mesh.I[e], mesh.J[e]
        dr, dz = mesh.rl[i + 1] - mesh.rl[i], mesh.zl[j + 1] - mesh.zl[j]
        Te = mesh.elem_T(L, e)
        k = kfun(mat_of(e))
        for s, w in _GP:
            x, y = {1: (s, -at), 2: (at, s), 3: (s, at), 4: (-at, s)}[face]
            N, dx, dy = shape(x, y)
            T = N @ Te
            r = mesh.rl[i] + (x + 1) / 2 * dr
            if face in (2, 4):
                Q += w * (-k(T) * (2 / dr) * (dx @ Te)) * 2 * math.pi * r * dz / 2
            else:
                Q += w * (-k(T) * (2 / dz) * (dy @ Te)) * 2 * math.pi * r * dr / 2
    return Q * 1e-3        # W/m.K * K/mm * mm2 = mW -> W


def surface_loss(mesh, L, faces, h, eps, T_inf):
    """Heat leaving through boundary faces (W): h (T - T_inf) + eps sigma (T^4 - T_inf^4), integrated over 2 pi r ds."""
    Q = 0.0
    for e, f in faces:
        i, j = mesh.I[e], mesh.J[e]
        pts = [(2 * i + di, 2 * j + dj) for di, dj in mesh.FACE[f]]
        Tn = np.array([L[p] for p in pts])
        rn = np.array([mesh.Rn[p[0]] for p in pts])
        zn = np.array([mesh.Zn[p[1]] for p in pts])
        ds = math.hypot(rn[2] - rn[0], zn[2] - zn[0])
        for s, w in _GP:
            Nf = np.array([0.5 * s * (s - 1), 1 - s * s, 0.5 * s * (s + 1)])
            T, r = Nf @ Tn, Nf @ rn
            q = h * (T - T_inf) + eps * SIGMA * ((T + 273.15) ** 4 - (T_inf + 273.15) ** 4)
            Q += w * q * 2 * math.pi * r * ds / 2
    return Q * 1e-6        # W/m2 * mm2 -> W


def face_mean(mesh, L, faces):
    """Area-weighted mean temperature over boundary faces."""
    num = den = 0.0
    for e, f in faces:
        i, j = mesh.I[e], mesh.J[e]
        pts = [(2 * i + di, 2 * j + dj) for di, dj in mesh.FACE[f]]
        Tn = np.array([L[p] for p in pts])
        rn = np.array([mesh.Rn[p[0]] for p in pts])
        zn = np.array([mesh.Zn[p[1]] for p in pts])
        ds = math.hypot(rn[2] - rn[0], zn[2] - zn[0])
        for s, w in _GP:
            Nf = np.array([0.5 * s * (s - 1), 1 - s * s, 0.5 * s * (s + 1)])
            a = w * (Nf @ rn) * ds
            num += a * (Nf @ Tn)
            den += a
    return num / den if den else float("nan")


def area_mean(mesh, L, elems):
    """Area-weighted (2 pi r dA) mean temperature of a set of elements (centre value of each CAX8)."""
    if len(elems) == 0:
        return float("nan")
    N, _, _ = shape(0.0, 0.0)
    num = den = 0.0
    for e in elems:
        i, j = mesh.I[e], mesh.J[e]
        w = (mesh.rl[i] + mesh.rl[i + 1]) / 2 * (mesh.rl[i + 1] - mesh.rl[i]) * (mesh.zl[j + 1] - mesh.zl[j])
        num += w * (N @ mesh.elem_T(L, e))
        den += w
    return num / den


# ---------------------------------------------------------------- ccx input / output
def _lines(ids, per=16):
    ids = [str(int(v)) for v in ids]
    return [", ".join(ids[k:k + per]) for k in range(0, len(ids), per)]


def write_inp(job, mesh, case, P_w, T0=None, transient=None, probe=None):
    g = mesh.g
    L = ["*HEADING", f"{job}", "*NODE"]
    used = np.argwhere(mesh.used)
    for (a, b) in used:
        L.append(f"{mesh.nid[a, b]}, {mesh.Rn[a]:.6f}, {mesh.Zn[b]:.6f}")
    L.append("*ELEMENT, TYPE=CAX8, ELSET=EALL")
    for k, row in enumerate(mesh.conn):
        L.append(f"{k + 1}, " + ", ".join(map(str, row)))
    mats_used = set()
    for name in mesh.names:
        L += [f"*ELSET, ELSET=R_{name.upper()}"] + _lines(mesh.region(name) + 1)
        mats_used.add(g["mats"][name])
    for mat in sorted(mats_used):
        k, rho, c = MATS[mat]
        L += [f"*MATERIAL, NAME={mat}", "*CONDUCTIVITY"]
        if callable(k):
            L += [f"{k(T):.6g}, {T:.1f}" for T in np.arange(0.0, 801.0, 50.0)]
        else:
            L.append(f"{k:.6g}")
        L += ["*DENSITY", f"{rho * 1e-12:.6g}", "*SPECIFIC HEAT", f"{c * 1e6:.6g}"]
    for name in mesh.names:
        L.append(f"*SOLID SECTION, ELSET=R_{name.upper()}, MATERIAL={g['mats'][name]}")
    L += ["*NSET, NSET=NALL"] + _lines(np.arange(1, mesh.used.sum() + 1))
    edge = mesh.nid[-1, :][mesh.nid[-1, :] > 0]
    L += ["*NSET, NSET=NEDGE"] + _lines(edge)
    fixed = [("NEDGE", case["T_ch"])]
    if case.get("tier") == "B":
        hb = _idx(mesh.Zn, g["zhb"])
        head = [mesh.nid[a, hb] for a in range(mesh.used.shape[0]) if mesh.used[a, hb] and mesh.Rn[a] <= g["Rk"] + 1e-9]
        zfb = _idx(mesh.Zn, -MP.FLOOR_T - MP.FLANGE_T)
        band = [mesh.nid[a, zfb] for a in range(mesh.used.shape[0])
                if mesh.used[a, zfb] and g["Rf"] - FLANGE_BAND - 1e-9 <= mesh.Rn[a] <= g["Rf"] + 1e-9]
        L += ["*NSET, NSET=NHEADW"] + _lines(head) + ["*NSET, NSET=NFLGW"] + _lines(band)
        fixed += [("NHEADW", T_WATER), ("NFLGW", T_WATER)]
    if probe is not None:
        L += ["*NSET, NSET=NPROBE"] + _lines(probe)
    bcsets = []
    for grp, faces in mesh.bc.items():
        for f in (1, 2, 3, 4):
            els = [e + 1 for e, ff in faces if ff == f]
            if els:
                nm = f"B_{grp.upper()}_F{f}"
                L += [f"*ELSET, ELSET={nm}"] + _lines(els)
                bcsets.append((grp, f, nm))
    L.append("*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.669E-11")
    L.append("*INITIAL CONDITIONS, TYPE=TEMPERATURE")
    if T0 is None:
        L.append(f"NALL, {case.get('T_init', 100.0):.3f}")
    else:
        L += [f"{n}, {T0[n]:.4f}" for n in range(1, mesh.used.sum() + 1)]
    if transient is None:
        L += ["*STEP, INC=200", "*HEAT TRANSFER, STEADY STATE", "1., 1."]
    else:
        L += [f"*STEP, INC=100000", f"*HEAT TRANSFER, DELTMX={transient['dTmax']}",
              f"{transient['dt0']}, {transient['t_end']}, 1e-3, {transient['dt_max']}"]
    L.append("*BOUNDARY")
    L += [f"{s}, 11, 11, {T:.3f}" for s, T in fixed]
    if P_w > 0:
        q = P_w * 1e3 / g["V_heater"]                 # mW/mm3
        L += ["*DFLUX", f"R_HEATER, BF, {q:.8g}"]
    h_top = H_TOP_D50 * math.sqrt(50.0 / MP.MODULES[g["key"]]["plate_d"])
    par = {"top": (h_top, case["eps"], case["T_ch"]), "under": (H_UNDER, EPS_UNDER, T_ROOM),
           "rod": (H_UNDER, EPS_UNDER, T_ROOM), "rodend": (H_ROD_END, 0.0, T_ROOM)}
    L.append("*FILM")
    L += [f"{nm}, F{f}, {par[grp][2]:.3f}, {par[grp][0] * 1e-3:.6g}" for grp, f, nm in bcsets]
    rad = [(grp, f, nm) for grp, f, nm in bcsets if par[grp][1] > 0]
    if rad:
        L.append("*RADIATE")
        L += [f"{nm}, R{f}, {par[grp][2]:.3f}, {par[grp][1]:.4g}" for grp, f, nm in rad]
    if transient is None:
        L += ["*NODE PRINT, NSET=NALL", "NT"]
    else:
        L += ["*NODE PRINT, NSET=NPROBE, FREQUENCY=1", "NT"]
    for s, _ in fixed:
        L += [f"*NODE PRINT, NSET={s}, TOTALS=ONLY" + (", FREQUENCY=1" if transient else ""), "RFL"]
    L.append("*END STEP")
    (RUN / f"{job}.inp").write_text("\n".join(L) + "\n")
    return par


def run_ccx(job):
    env = dict(os.environ, OMP_NUM_THREADS=os.environ.get("OMP_NUM_THREADS", "1"))
    r = subprocess.run(["ccx", "-i", job], cwd=RUN, env=env, capture_output=True, text=True)
    if r.returncode != 0 or "Job finished" not in r.stdout:
        raise RuntimeError(f"ccx failed for {job}:\n" + "\n".join((r.stdout + r.stderr).splitlines()[-25:]))


def read_dat(job):
    """Blocks of the .dat: list of (kind, set, time, rows)."""
    blocks, cur = [], None
    for line in (RUN / f"{job}.dat").read_text().splitlines():
        s = line.strip()
        if " for set " in s and " and time " in s:
            kind = s.split(" for set ")[0]
            parts = s.split()
            cur = (kind, parts[parts.index("set") + 1], float(parts[-1]), [])
            blocks.append(cur)
        elif cur is not None and s:
            try:
                cur[3].append([float(v) for v in s.split()])
            except ValueError:
                cur = None
    return blocks


# ---------------------------------------------------------------- steady solve and post-processing
def run_steady(mesh, case, P_w, T0, job):
    par = write_inp(job, mesh, case, P_w, T0=T0)
    run_ccx(job)
    T = np.full(mesh.used.sum() + 1, np.nan)
    rfl = {}
    for kind, s, t, rows in read_dat(job):
        if kind == "temperatures":
            a = np.array(rows)
            T[a[:, 0].astype(int)] = a[:, 1]
        elif kind.startswith("total heat generation"):
            rfl[s] = rows[0][0] * 180 * 1e-3            # 2-degree sector, mW -> W for the whole ring
    return T, rfl, par


def centre_node(mesh):
    g = mesh.g
    return mesh.nid[0, _idx(mesh.Zn, g["z_p"])], mesh.nid[_idx(mesh.Rn, g["Rp"]), _idx(mesh.Zn, g["z_p"])]


def solve_steady(case):
    """Find the heater power that puts the plate top centre at case['T_set'] (secant on P), then post-process."""
    t0 = time.time()
    g = geometry(case["key"], case["z_p"], case.get("tier", "A"), case.get("gap", "ARGON"), case.get("clear_plate"))
    mesh = Mesh(g, case.get("h0", H0))
    nc, _ = centre_node(mesh)
    job = case["name"]
    T_set, T_ch = case["T_set"], case["T_ch"]
    P = case.get("P_guess", 0.6 * (T_set - T_ch) * MP.MODULES[case["key"]]["bore"] / 50.8)
    hist, T0 = [], None
    for it in range(14):
        T, rfl, par = run_steady(mesh, case, P, T0, job)
        Tc = T[nc]
        hist.append((P, Tc))
        if abs(Tc - T_set) < 0.02:
            break
        if len(hist) == 1:
            ref = T_WATER if case.get("tier") == "B" else T_ch
            P = P * (T_set - ref) / max(Tc - ref, 1.0)
        else:
            (p1, t1), (p2, t2) = hist[-2], hist[-1]
            P = p2 + (T_set - t2) * (p2 - p1) / (t2 - t1)
        T0 = T
    res = post(mesh, case, P_w=hist[-1][0], T=T, rfl=rfl, par=par)
    res.update(iterations=len(hist), seconds=round(time.time() - t0, 1),
               nodes=int(mesh.used.sum()), elements=int(len(mesh.I)), h0=case.get("h0", H0))
    np.save(RUN / f"{job}_T.npy", T)
    return res


def post(mesh, case, P_w, T, rfl, par):
    g = mesh.g
    L = mesh.lattice(T)
    nc, ne = centre_node(mesh)
    mat_of = lambda e: g["mats"][mesh.names[mesh.ereg[e]]]  # noqa: E731

    def tmax(*regions):
        els = np.concatenate([mesh.region(r) for r in regions])
        return float(np.nanmax(T[mesh.nodes_of(els)])) if len(els) else float("nan")

    def with_nb(region, face, nbs):
        return [e for e in mesh.region(region) if mesh.neighbour(e, face) in nbs]

    r = dict(case={k: v for k, v in case.items() if k not in ("P_guess",)})
    r["P_heater_W"] = P_w
    r["T_plate_centre"] = float(T[nc])
    r["T_plate_edge"] = float(T[ne])
    r["dT_centre_edge"] = float(T[nc] - T[ne])
    r["T_block_max"] = tmax("block", "heater", "cpb")
    r["T_seal_max"] = tmax("seal")
    r["T_oring_max"] = tmax("oring")
    r["T_gland_max"] = tmax("goring")
    r["T_rod_end"] = face_mean(mesh, L, mesh.bc["rodend"])
    r["T_rod_at_gland"] = float(np.nanmax(L[_idx(mesh.Rn, g["rro"]), _idx(mesh.Zn, g["zBT"] - MP.BOT_FLANGE_T):_idx(mesh.Zn, g["zBT"]) + 1]))
    r["T_head_mean"] = area_mean(mesh, L, mesh.region("head"))
    # where the heat ends up
    top_plate = [(e, f) for e, f in mesh.bc["top"] if mesh.names[mesh.ereg[e]] in ("plate", "cake", "gap_p")]
    top_spig = [(e, f) for e, f in mesh.bc["top"] if (e, f) not in set(top_plate)]
    s = {}
    s["chamber_plate_top"] = surface_loss(mesh, L, top_plate, *par["top"])
    s["chamber_spigot_top"] = surface_loss(mesh, L, top_spig, *par["top"])
    s["floor"] = -rfl["NEDGE"]
    s["under_floor_module"] = surface_loss(mesh, L, mesh.bc["under"], *par["under"])
    s["rod"] = surface_loss(mesh, L, mesh.bc["rod"], *par["rod"]) + surface_loss(mesh, L, mesh.bc["rodend"], *par["rodend"])
    if case.get("tier") == "B":
        s["water_head"] = -rfl["NHEADW"]
        s["water_flange"] = -rfl["NFLGW"]
    r["sinks_W"] = s
    r["into_chamber_W"] = s["chamber_plate_top"] + s["chamber_spigot_top"] + s["floor"]
    r["balance_err_pct"] = 100 * (sum(s.values()) - P_w) / P_w
    # where the heat leaves the plate + heater block
    x = {}
    if case["z_p"] < 0:
        x["plate_top"] = face_flux(mesh, L, with_nb("cake", 1, {"plate"}), 1, mat_of, at=GL)
    else:
        x["plate_top"] = surface_loss(mesh, L, [(e, f) for e, f in top_plate if mesh.names[mesh.ereg[e]] == "plate"], *par["top"])
    x["radial_gaps"] = (face_flux(mesh, L, with_nb("gap_p", 4, {"plate"}), 4, mat_of, at=0.0)
                        + face_flux(mesh, L, with_nb("gap_b", 4, {"block", "heater", "cpb"}), 4, mat_of, at=0.0)
                        - face_flux(mesh, L, with_nb("gap_b", 3, {"plate"}), 3, mat_of, at=0.0))
    x["break"] = -face_flux(mesh, L, [e for e in np.concatenate([mesh.region("brk"), mesh.region("macor")])
                                       if mesh.neighbour(e, 3) in ("block", "heater")], 3, mat_of, at=GL)
    x["through_macor"] = -face_flux(mesh, L, with_nb("macor", 3, {"block", "heater"}), 3, mat_of, at=GL)
    r["exit_balance_err_pct"] = 100 * (x["plate_top"] + x["radial_gaps"] + x["break"] - P_w) / P_w
    if case["z_p"] < 0:     # the cake gradient at the plate's top corner is under-resolved: take the top share as the remainder
        x["plate_top_direct"] = x["plate_top"]
        x["plate_top"] = P_w - x["radial_gaps"] - x["break"]
    r["exit_W"] = x
    # hot running clearances (plane-stress rings and discs grow with their area-mean temperature)
    zl, zh = g["zpb"], g["z_p"]
    ring = [e for e in np.concatenate([mesh.region(n) for n in ("spigot", "tube", "mflange", "oring")])
            if mesh.zl[mesh.J[e]] >= zl - 1e-9 and mesh.zl[mesh.J[e] + 1] <= zh + 1e-9 and mesh.rl[mesh.I[e]] < g["Rs"] - 1e-9]
    Tp, Tr = area_mean(mesh, L, mesh.region("plate")), area_mean(mesh, L, ring)
    c0 = g["Rb"] - g["Rp"]
    r["T_plate_mean"], r["T_bore_ring_mean"] = Tp, Tr
    r["clear_plate_hot_mm"] = c0 + g["Rb"] * ALPHA["SS"] * (Tr - 20) - g["Rp"] * ALPHA["AL"] * (Tp - 20)
    Tsp = area_mean(mesh, L, np.concatenate([mesh.region("spigot"), mesh.region("oring")]))
    Tfl = area_mean(mesh, L, mesh.region("floor"))
    r["T_spigot_mean"], r["T_floor_mean"] = Tsp, Tfl
    r["T_floor_port"] = float(np.nanmean(L[_idx(mesh.Rn, g["Rsg"]), _idx(mesh.Zn, -MP.FLOOR_T):_idx(mesh.Zn, 0.0) + 1]))
    r["clear_spigot_hot_mm"] = MP.SPIGOT_FIT + g["Rsg"] * ALPHA["AL"] * (Tfl - 20) - g["Rs"] * ALPHA["SS"] * (Tsp - 20)
    return r


# ---------------------------------------------------------------- transients
def run_transient(spec):
    """spec: name, key, z_p, T_ch, eps, P_w (0 = cool-down), T_init_from (steady job name) or T_init (uniform),
    t_end, stop (plate-centre temperature of interest)."""
    t0 = time.time()
    g = geometry(spec["key"], spec["z_p"])
    mesh = Mesh(g, spec.get("h0", H0_TRANSIENT))
    nc, ne = centre_node(mesh)
    plate_els = mesh.region("plate")
    ring_els = [e for e in np.concatenate([mesh.region(n) for n in ("spigot", "tube", "mflange", "oring")])
                if mesh.zl[mesh.J[e]] >= g["zpb"] - 1e-9 and mesh.zl[mesh.J[e] + 1] <= g["z_p"] + 1e-9
                and mesh.rl[mesh.I[e]] < g["Rs"] - 1e-9]
    blk = np.concatenate([mesh.region("block"), mesh.region("heater"), mesh.region("cpb")])
    probe = sorted(set(mesh.nodes_of(np.concatenate([plate_els, np.array(ring_els, int), blk]))) | {nc, ne})
    T0 = np.load(RUN / f"{spec['T_init_from']}_T.npy") if spec.get("T_init_from") else None
    case = dict(T_ch=spec["T_ch"], eps=spec["eps"], T_init=spec.get("T_init", 25.0))
    write_inp(spec["name"], mesh, case, spec["P_w"], T0=T0, probe=probe,
              transient=dict(dTmax=8.0, dt0=0.01 if spec["P_w"] > 0 else 1.0, t_end=spec["t_end"],
                             dt_max=60.0 if spec["P_w"] > 0 else 120.0))
    run_ccx(spec["name"])
    blk_nodes = mesh.nodes_of(blk)
    out = []
    Tn = np.full(mesh.used.sum() + 1, np.nan)
    for kind, s, t, rows in read_dat(spec["name"]):
        if kind == "temperatures" and s == "NPROBE":
            a = np.array(rows)
            Tn[a[:, 0].astype(int)] = a[:, 1]
            L = mesh.lattice(Tn)
            Tp, Tr = area_mean(mesh, L, plate_els), area_mean(mesh, L, ring_els)
            clr = (g["Rb"] - g["Rp"]) + g["Rb"] * ALPHA["SS"] * (Tr - 20) - g["Rp"] * ALPHA["AL"] * (Tp - 20)
            out.append((t, float(Tn[nc]), float(np.nanmax(Tn[blk_nodes])), float(Tn[ne]), clr))
    ts = np.array(out)
    res = dict(spec=spec, seconds=round(time.time() - t0, 1), t=ts[:, 0].tolist(), T_centre=ts[:, 1].tolist(),
               T_block_max=ts[:, 2].tolist(), T_edge=ts[:, 3].tolist(), clear_plate_mm=ts[:, 4].tolist())
    y, target = ts[:, 1], spec["stop"]
    hit = np.nonzero(y <= target)[0] if spec["P_w"] == 0 else np.nonzero(y >= target)[0]
    if len(hit) and hit[0] > 0:
        k = hit[0]
        tt = ts[k - 1, 0] + (target - y[k - 1]) * (ts[k, 0] - ts[k - 1, 0]) / (y[k] - y[k - 1])
        res["t_target_min"] = tt / 60
        res["T_block_at_target"] = float(np.interp(tt, ts[:, 0], ts[:, 2]))
        res["clear_plate_at_target_mm"] = float(np.interp(tt, ts[:, 0], ts[:, 4]))
    else:
        res["t_target_min"] = None
        res["T_centre_end"] = float(y[-1])
    res["T_block_peak"] = float(ts[:, 2].max())
    res["clear_plate_min_mm"] = float(ts[:, 4].min())
    return res


# ---------------------------------------------------------------- sanity checks (units, RFL convention)
def sanity():
    """1D checks of the ccx conventions on a small structured mesh: annulus conduction, film, radiation."""
    out = {}
    for name, rects, extra in [
        ("annulus", [("plate", 10.0, 20.0, 0.0, 10.0)], "cond"),
        ("film", [("plate", 0.0, 10.0, 0.0, 1.0)], "film"),
        ("rad", [("plate", 0.0, 10.0, 0.0, 1.0)], "rad"),
    ]:
        nodes = {}
        r = np.linspace(rects[0][1], rects[0][2], 11)
        z = np.linspace(rects[0][3], rects[0][4], 5)
        Rn = np.linspace(r[0], r[-1], 21)
        Zn = np.linspace(z[0], z[-1], 9)
        L = ["*NODE"]
        k = 0
        for a in range(21):
            for b in range(9):
                if a % 2 == 1 and b % 2 == 1:
                    continue
                k += 1
                nodes[(a, b)] = k
                L.append(f"{k}, {Rn[a]:.6f}, {Zn[b]:.6f}")
        L.append("*ELEMENT, TYPE=CAX8, ELSET=EALL")
        e = 0
        top = []
        for i in range(10):
            for j in range(4):
                e += 1
                L.append(f"{e}, " + ", ".join(str(nodes[(2 * i + di, 2 * j + dj)]) for di, dj in Mesh.OFFS))
                if j == 3:
                    top.append(e)
        inner = [v for (a, b), v in nodes.items() if a == 0]
        outer = [v for (a, b), v in nodes.items() if a == 20]
        bot = [v for (a, b), v in nodes.items() if b == 0]
        L += ["*NSET, NSET=NIN"] + _lines(inner) + ["*NSET, NSET=NOUT"] + _lines(outer) + ["*NSET, NSET=NBOT"] + _lines(bot)
        L += ["*ELSET, ELSET=ETOP"] + _lines(top)
        L += ["*MATERIAL, NAME=M", "*CONDUCTIVITY", "16.", "*SOLID SECTION, ELSET=EALL, MATERIAL=M",
              "*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.669E-11",
              "*STEP", "*HEAT TRANSFER, STEADY STATE", "1., 1.", "*BOUNDARY"]
        A = math.pi * 0.01 ** 2
        if extra == "cond":
            L += ["NIN, 11, 11, 100.", "NOUT, 11, 11, 0.", "*NODE PRINT, NSET=NIN, TOTALS=ONLY", "RFL"]
            expect = 2 * math.pi * 16 * 0.010 * 100 / math.log(2)
        elif extra == "film":
            L += ["NBOT, 11, 11, 100.", "*FILM", f"ETOP, F3, 0., {100 * 1e-3}", "*NODE PRINT, NSET=NBOT, TOTALS=ONLY", "RFL"]
            expect = 100 * A * 100 / (1 + 100 * 0.001 / 16)
        else:
            L += ["NBOT, 11, 11, 200.", "*RADIATE", "ETOP, R3, 0., 1.0", "*NODE PRINT, NSET=NBOT, TOTALS=ONLY", "RFL"]
            expect = SIGMA * A * (473.15 ** 4 - 273.15 ** 4)
        L.append("*END STEP")
        job = f"sanity_{name}"
        (RUN / f"{job}.inp").write_text("\n".join(L) + "\n")
        run_ccx(job)
        got = [rows[0][0] for kind, s, t, rows in read_dat(job) if kind.startswith("total")][0] * 180 * 1e-3
        out[name] = dict(ccx_W=got, analytic_W=expect, err_pct=100 * (got - expect) / expect)
    return out


# ---------------------------------------------------------------- lumped comparison (requirements_budgets.py)
def lumped():
    sys.path.insert(0, str(ROOT))
    with contextlib.redirect_stdout(io.StringIO()):
        import requirements_budgets as RB
    res = {}
    for key, d in (("S25", 0.025), ("M50", 0.050), ("L75", 0.075)):
        m, qr, qc, qp, qy, ql, ph, tc = RB.plate_budget(d, MP.T_SET_A)
        res[key] = dict(rad=qr, conv=qc, posts=qp, cyl=qy, loss=ql, heater_15min=ph, cool_min=tc / 60)
    return res


# ---------------------------------------------------------------- plots
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984"
SERIES = {"S25": "#2a78d6", "M50": "#eb6834", "L75": "#1baf7a"}     # categorical slots 1-3, fixed order


def plot_map(case_name, res, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.colors import LinearSegmentedColormap

    c = res["case"]
    g = geometry(c["key"], c["z_p"])
    mesh = Mesh(g, c.get("h0", H0))
    T = np.load(RUN / f"{case_name}_T.npy")
    L = mesh.lattice(T)
    N, _, _ = shape(0.0, 0.0)
    C = np.full((mesh.nr, mesh.nz), np.nan)
    for e in range(len(mesh.I)):
        C[mesh.I[e], mesh.J[e]] = N @ mesh.elem_T(L, e)
    cm = LinearSegmentedColormap.from_list("heat1", ["#fdf1e7", "#f6b48f", "#eb6834", "#b8461b", "#6e2508"])
    fig, ax = plt.subplots(figsize=(8.6, 6.4), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    vmin, vmax = c["T_ch"], math.ceil(np.nanmax(C) / 10) * 10
    Cm = np.ma.masked_invalid(C)
    for sgn in (1, -1):
        rl = mesh.rl if sgn > 0 else -mesh.rl[::-1]
        data = Cm.T if sgn > 0 else Cm.T[:, ::-1]
        pc = ax.pcolormesh(rl, mesh.zl, data, cmap=cm, vmin=vmin, vmax=vmax, shading="flat", rasterized=True)
        rc = 0.5 * (rl[:-1] + rl[1:])
        zc = 0.5 * (mesh.zl[:-1] + mesh.zl[1:])
        cs = ax.contour(rc, zc, data, levels=np.arange(50, vmax, 25), colors=INK2, linewidths=0.5)
        if sgn < 0:
            ax.clabel(cs, fmt="%d", fontsize=6, colors=INK2)
    # part outlines (region boundaries)
    segs = []
    reg = mesh.reg
    for i in range(mesh.nr):
        for j in range(mesh.nz):
            a = reg[i, j]
            if a < 0:
                continue
            if i + 1 < mesh.nr and reg[i + 1, j] != a:
                segs.append([(mesh.rl[i + 1], mesh.zl[j]), (mesh.rl[i + 1], mesh.zl[j + 1])])
            if j + 1 < mesh.nz and reg[i, j + 1] != a:
                segs.append([(mesh.rl[i], mesh.zl[j + 1]), (mesh.rl[i + 1], mesh.zl[j + 1])])
            if i + 1 == mesh.nr or (i + 1 < mesh.nr and reg[i + 1, j] < 0):
                segs.append([(mesh.rl[i + 1], mesh.zl[j]), (mesh.rl[i + 1], mesh.zl[j + 1])])
            if j + 1 == mesh.nz or reg[i, j + 1] < 0:
                segs.append([(mesh.rl[i], mesh.zl[j + 1]), (mesh.rl[i + 1], mesh.zl[j + 1])])
            if j == 0 or reg[i, j - 1] < 0:
                segs.append([(mesh.rl[i], mesh.zl[j]), (mesh.rl[i + 1], mesh.zl[j])])
            if i > 0 and reg[i - 1, j] < 0:
                segs.append([(mesh.rl[i], mesh.zl[j]), (mesh.rl[i], mesh.zl[j + 1])])
    mir = [[(-p[0], p[1]) for p in s] for s in segs]
    ax.add_collection(LineCollection(segs + mir, colors="#3d3c39", linewidths=0.35))
    ax.axvline(0, color=MUTED, lw=0.5, ls=(0, (4, 3)))
    # labelled points (right half)
    marks = [((0.0, c["z_p"]), f"plate top centre {res['T_plate_centre']:.0f} °C (set point)", (30, 8)),
             ((g["Rb"] - 1, g["zhb"] + MP.HEAD_T - SEAL_BELOW_HEAD_TOP - SEAL_H / 2), f"bore seal ≤ {res['T_seal_max']:.0f} °C", (60, 8)),
             ((g["Rs"] - 1.4, ORING_Z), f"spigot O-ring ≤ {res['T_oring_max']:.0f} °C", (62, -4)),
             ((g["rro"] + 1.0, g["zBT"] - 6), f"rod-gland O-rings ≤ {res['T_gland_max']:.0f} °C", (40, -4)),
             ((g["rro"] / 2, g["zre"]), f"coupling face (magnet) {res['T_rod_end']:.0f} °C", (30, -2))]
    for (x, y), text, (tx, ty) in marks:
        ax.plot([x], [y], marker="o", ms=4, mfc=INK, mec=SURFACE, mew=0.8, zorder=5)
        ax.annotate(text, (x, y), xytext=(tx, y + ty), fontsize=7, color=INK, va="center",
                    arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6), zorder=6)
    ax.set_xlim(-70, 125)
    ax.set_ylim(g["zre"] - 6, 13)
    ax.set_aspect("equal")
    ax.set_xlabel("r (mm); left half mirrored with isotherms every 25 °C", color=INK2, fontsize=8)
    ax.set_ylabel("z (mm), 0 = powder plane", color=INK2, fontsize=8)
    ax.tick_params(colors=INK2, labelsize=7)
    for sp in ax.spines.values():
        sp.set_color("#c9c8c3")
    lab = MP.MODULES[c["key"]]["label"]
    ax.set_title(f"{c['key']} ({lab}), build start (z_p = 0): plate at {MP.T_SET_A:.0f} °C, chamber {c['T_ch']:.0f} °C, "
                 f"powder ε {c['eps']}\nheater {res['P_heater_W']:.0f} W, {res['into_chamber_W']:.0f} W of it into the chamber"
                 f" (floor {res['sinks_W']['floor']:.0f} W)", fontsize=8.5, color=INK, loc="left")
    cb = fig.colorbar(pc, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label("temperature (°C)", color=INK2, fontsize=8)
    cb.ax.tick_params(colors=INK2, labelsize=7)
    cb.outline.set_edgecolor("#c9c8c3")
    ax.text(119, -22, "floor (6061) runs to r = 120;\nedge held at the chamber temperature", fontsize=6.5, color=INK2,
            ha="right", va="top")
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def plot_transients(tr, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.0), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    panels = [("heat", "Heat-up from 25 °C at the installed power (build start, z_p = 0)", MP.T_SET_A, "set point 200 °C"),
              ("cool", "Cool-down, heaters off, from the build-end steady state (z_p = −40)", MP.T_DOOR_OPEN,
               "door unlocks below 50 °C")]
    for ax, (kind, title, ref, reflab) in zip(axs, panels):
        ax.set_facecolor(SURFACE)
        ax.axhline(ref, color=MUTED, lw=0.8, ls=(0, (4, 3)))
        xmax = 0
        for n, key in enumerate(("S25", "M50", "L75")):
            r = tr.get(f"{kind}_{key}")
            if not r:
                continue
            t = np.array(r["t"]) / 60
            y = np.array(r["T_centre"])
            if kind == "cool" and r["t_target_min"]:
                keep = t <= r["t_target_min"] * 1.25
                t, y = t[keep], y[keep]
            if kind == "heat" and r["t_target_min"]:          # no controller in the model: stop at the set point
                keep = t <= r["t_target_min"] + 1e-9
                t, y = np.append(t[keep], r["t_target_min"]), np.append(y[keep], ref)
            ax.plot(t, y, color=SERIES[key], lw=2, label=f"{key}" + (f", {r['spec']['P_w']:.0f} W" if kind == "heat" else ""))
            xmax = max(xmax, t[-1] * (2.5 if kind == "heat" and r["t_target_min"] else 1.0))
            tt = r["t_target_min"]
            if tt:
                ax.plot([tt], [ref], marker="o", ms=6, mfc=SERIES[key], mec=SURFACE, mew=1.5, zorder=5)
                ax.annotate(f"{key} {tt:.1f} min" if kind == "heat" else f"{key} {tt:.0f} min", (tt, ref),
                            xytext=(6, (10 + 12 * n) if kind == "heat" else -12), textcoords="offset points", fontsize=7, color=INK)
            else:
                ax.annotate(f"{key}: levels at {y[-1]:.0f} °C", (t[-1], y[-1]), xytext=(-90, -12 - 11 * n),
                            textcoords="offset points", fontsize=7, color=INK)
        ax.text(xmax, ref + (-9 if kind == "heat" else 3), reflab, fontsize=7, color=INK2, ha="right")
        ax.set_title(title, fontsize=8.5, color=INK, loc="left")
        ax.set_xlabel("time (min)", color=INK2, fontsize=8)
        ax.set_ylabel("plate top centre (°C)", color=INK2, fontsize=8)
        ax.set_xlim(0, xmax)
        ax.grid(True, color="#e6e5e0", lw=0.5)
        ax.tick_params(colors=INK2, labelsize=7)
        for sp in ax.spines.values():
            sp.set_color("#c9c8c3")
        ax.legend(fontsize=7, frameon=False, labelcolor=INK)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------- cases
def steady_cases(quick=False):
    cs = []
    keys = ["M50"] if quick else ["S25", "M50", "L75"]
    for key in keys:
        for z_p, pos in ((0.0, "start"), (-MP.BUILD_STROKE, "end")):
            for T_ch in (25.0, 60.0):
                for eps in ((EPS_POWDER, EPS_BARE) if z_p == 0 else (EPS_POWDER,)):
                    if quick and (T_ch != 25.0 or eps != EPS_POWDER):
                        continue
                    cs.append(dict(name=f"{key}_{pos}_ch{T_ch:.0f}_e{eps:g}", key=key, z_p=z_p, pos=pos, T_set=MP.T_SET_A,
                                   T_ch=T_ch, eps=eps, group="base"))
    for key in keys:                       # build-end fields on the transient mesh: initial state of the cool-downs
        cs.append(dict(name=f"{key}_end_ch25_e0.5_h2", key=key, z_p=-MP.BUILD_STROKE, pos="end", T_set=MP.T_SET_A,
                       T_ch=25.0, eps=EPS_POWDER, h0=H0_TRANSIENT, group="transient_init"))
    if quick:
        return cs
    for z_p, pos in ((0.0, "start"), (-MP.BUILD_STROKE, "end")):
        cs.append(dict(name=f"M50_{pos}_powdergaps", key="M50", z_p=z_p, pos=pos, T_set=MP.T_SET_A, T_ch=25.0,
                       eps=EPS_POWDER, gap="POWDER", group="powder_gaps"))
        cs.append(dict(name=f"M50_{pos}_tierB", key="M50", z_p=z_p, pos=pos, T_set=MP.CLEAR["B"]["t_max"], T_ch=25.0,
                       eps=EPS_POWDER, tier="B", group="tierB", T_init=200.0))
    for h0, lab in ((2.0, "coarse"), (0.5, "fine")):
        cs.append(dict(name=f"M50_start_mesh_{lab}", key="M50", z_p=0.0, pos="start", T_set=MP.T_SET_A, T_ch=25.0,
                       eps=EPS_POWDER, h0=h0, group="mesh"))
    for cp in (0.10, 0.20):
        cs.append(dict(name=f"M50_start_clear{cp:.2f}", key="M50", z_p=0.0, pos="start", T_set=MP.T_SET_A, T_ch=25.0,
                       eps=EPS_POWDER, clear_plate=cp, group="clearance"))
    return cs


def suggested_power(steady, key):
    """>= 1.5x the worst Tier A steady power, in whole heaters of the module's size."""
    m = MP.MODULES[key]
    worst = max(r["P_heater_W"] for r in steady.values() if r["case"]["key"] == key and r["case"]["group"] == "base")
    n = math.ceil(1.5 * worst / m["heater_w"] - 1e-9)
    return worst, n, n * m["heater_w"]


def transient_specs(quick=False):
    sp = []
    keys = ["M50"] if quick else ["S25", "M50", "L75"]
    for key in keys:
        sp.append(dict(name=f"cool_{key}", key=key, z_p=-MP.BUILD_STROKE, T_ch=25.0, eps=EPS_POWDER, P_w=0.0,
                       T_init_from=f"{key}_end_ch25_e0.5_h2", t_end=6 * 3600.0, stop=MP.T_DOOR_OPEN))
        if not quick:
            m = MP.MODULES[key]
            sp.append(dict(name=f"heat_{key}", key=key, z_p=0.0, T_ch=25.0, eps=EPS_POWDER,
                           P_w=m["heaters"] * m["heater_w"], T_init=25.0, t_end=3 * 3600.0, stop=MP.T_SET_A))
    return sp


def min_clear_um(r):
    """Least plate-to-bore clearance (um) during a heat-up, up to the moment the plate centre reaches the set point."""
    t, c = np.array(r["t"]), np.array(r["clear_plate_mm"])
    tt = r["t_target_min"] * 60 if r.get("t_target_min") else t[-1]
    return 1000 * c[t <= tt + 1e-9].min()


def heaters_sentence(SG, h):
    short = [k for k in SG if SG[k]["installed_W"] < SG[k]["suggested_W"] - 1e-6]
    never = [f"{k} levels at {h[k]['T_centre_end']:.0f} °C" for k in SG if h.get(k) and not h[k]["t_target_min"]]
    txt = ("The heaters now in `module_params.py` give " + ", ".join(
        f"{k} {SG[k]['installed_W'] / SG[k]['worst_steady_W']:.1f}×" for k in ("S25", "M50", "L75") if k in SG) + " the worst steady power")
    txt += (f"; below the 1.5× margin: {', '.join(short)} (fit {', '.join(str(SG[k]['n_suggested']) + ' × ' + format(SG[k]['heater_w'], '.0f') + ' W' for k in short)})."
            if short else ", so all meet the 1.5× margin.")
    if never:
        txt += " At full power " + " and ".join(never) + " after 3 h."
    return txt


def clearance_sentence(st, hs):
    bad = [k for k in st if min(st[k]["clear_plate_hot_mm"] * 1000, min_clear_um(hs[k])) < 20]
    if not bad:
        return "That leaves ≥ 20 µm everywhere, so these clearances work."
    return ("Still too tight for " + ", ".join(bad) + ": add " + ", ".join(
        f"{k} ~{max(0, 30 - min(st[k]['clear_plate_hot_mm'] * 1000, min_clear_um(hs[k]))):.0f} µm" for k in bad) +
        " of cold clearance, or ramp-limit the heat-up so the bore keeps up.")


def narrative(S, TR, SG, LU):
    g = lambda k: S[k]  # noqa: E731
    st = {k: g(f"{k}_start_ch25_e0.5") for k in ("S25", "M50", "L75")}
    en = {k: g(f"{k}_end_ch25_e0.5") for k in ("S25", "M50", "L75")}
    m0 = st["M50"]
    share = lambda r: 100 * r["exit_W"]["radial_gaps"] / r["P_heater_W"]  # noqa: E731
    pg0, pg1 = g("M50_start_powdergaps"), g("M50_end_powdergaps")
    c05, c20 = g("M50_start_clear0.10"), g("M50_start_clear0.20")
    hot = [S[k] for k in S if S[k]["case"]["group"] == "base"]
    seal = max(r["T_seal_max"] for r in hot)
    orng = max(r["T_oring_max"] for r in hot)
    orng25 = max(r["T_oring_max"] for r in hot if r["case"]["T_ch"] == 25)
    gland = max(r["T_gland_max"] for r in hot)
    mag = max(r["T_rod_end"] for r in hot)
    spig = min(r["clear_spigot_hot_mm"] for r in S.values()) * 1000
    tb0, tb1 = g("M50_start_tierB"), g("M50_end_tierB")
    need = {k: MP.CLEAR["A"]["plate"] - st[k]["clear_plate_hot_mm"] + 0.03 for k in st}
    hs = {k: TR.get(f"heatS_{k}") or TR.get(f"heat_{k}") for k in st}
    h = {k: TR.get(f"heat_{k}") for k in st}
    never = [f"{k} levels at {h[k]['T_centre_end']:.0f} °C" for k in st if h[k] and not h[k]["t_target_min"]]
    out = ["## What this means for the design", "",
           f"1. **Build start is the worst case.** With the plate in the spigot (z_p 0) the set point takes "
           f"{st['S25']['P_heater_W']:.0f} / {st['M50']['P_heater_W']:.0f} / {st['L75']['P_heater_W']:.0f} W (S25 / M50 / L75), against "
           f"{en['S25']['P_heater_W']:.0f} / {en['M50']['P_heater_W']:.0f} / {en['L75']['P_heater_W']:.0f} W at the build end. "
           f"{min(share(st[k]) for k in st):.0f}–{max(share(st[k]) for k in st):.0f} % of it crosses the radial plate and block gaps into the "
           "bore. At the start that bore is the spigot, which the 0.03 mm fit and the flange tie to the floor, so most of the power ends up "
           f"in the floor (M50: {m0['sinks_W']['floor']:.0f} of {m0['P_heater_W']:.0f} W; the floor at the port only reaches "
           f"{m0['T_floor_port']:.0f} °C). " + heaters_sentence(SG, h),
           f"2. **The plate gap closes when hot.** The 6061 plate grows ~{23.6e-6 * 180 * 25.3 * 1000:.0f} µm (M50) to "
           f"~{23.6e-6 * 180 * 38 * 1000:.0f} µm (L75) on radius at 200 °C, while the 316L bore round it stays at "
           f"{st['M50']['T_bore_ring_mean']:.0f}–{st['L75']['T_bore_ring_mean']:.0f} °C at build start. With the cold clearances now in "
           "`module_params.py` (" + ", ".join(f"{k} {MP.MODULES[k]['plate_clear'] * 1000:.0f}" for k in st) + " µm), the hot gap at steady "
           "build start is " + " / ".join(f"{st[k]['clear_plate_hot_mm'] * 1000:.0f}" for k in st) + " µm (S25 / M50 / L75), and the "
           "least in a full-power heat-up, when the bore lags, is " + " / ".join(f"{min_clear_um(hs[k]):.0f}" for k in st) + " µm. "
           f"The gap also sets the leak: M50 at 0.10 / {MP.MODULES['M50']['plate_clear']:.2f} / 0.20 mm takes {c05['P_heater_W']:.0f} / "
           f"{m0['P_heater_W']:.0f} / {c20['P_heater_W']:.0f} W. " + clearance_sentence(st, hs) +
           " Close the gap against powder with a hot-side wiper at the plate rim.",
           f"3. **Powder in the gaps is the largest risk.** Filled with powder (k 0.2 against argon's ~0.025), the gaps make M50 need "
           f"{pg0['P_heater_W']:.0f} W at the start (block {pg0['T_block_max']:.0f} °C, past the {LIMITS['tco']:.0f} °C cutoff) and "
           f"{pg1['P_heater_W']:.0f} W at the end, where the coupling face reaches {pg1['T_rod_end']:.0f} °C (magnet limit 80) and the rod "
           f"gland {pg1['T_gland_max']:.0f} °C. At z_p 0 the plate gap opens onto the powder plane, so the wiper in point 2 is required, not optional.",
           f"4. **S25's heater block runs at its cutoff.** Most of its heat crosses the small Ø24.8 contact face (2000 W/m²K) to reach the "
           f"plate rim, so the block runs {st['S25']['T_block_max'] - MP.T_SET_A:.0f} °C above the set point: {st['S25']['T_block_max']:.0f} °C "
           f"at steady build start, against TCO_A = {LIMITS['tco']:.0f} °C, and {hs['S25']['T_block_at_target']:.0f} °C when the plate "
           f"reaches 200 °C at {hs['S25']['spec']['P_w']:.0f} W. "
           "Put graphite foil in the contact (aim for ≥ 5000 W/m²K) and ramp-limit the power. Also, S25's central cartridge and "
           "its single central Macor standoff occupy the same spot; use a Macor sleeve round the cartridge, or three small standoffs.",
           f"5. **Seals and the magnet pass in Tier A with clean (argon) gaps.** Worst over the 200 °C cases: bore seal {seal:.0f} °C "
           f"(limit 204), spigot O-ring {orng:.0f} °C ({orng25:.0f} with a 25 °C chamber; prefer ≤ 150), rod-gland O-rings "
           f"{gland:.0f} °C (≤ 200), coupling face {mag:.0f} °C (≤ 80). Build end is the hot case for the seal, gland and magnet, because "
           f"the head then sits 2 mm above the bottom flange. The magnet has {80 - mag:.0f} °C of margin, and loses it if powder fills the gaps (point 3). "
           "A 3–5 mm G10 or PEEK washer under the striker, or an SH-grade (150 °C) magnet, restores it. The 10 W/m²K coupling face is "
           "conservative: the 6061 Z arm under it is a better sink.",
           f"6. **The 0.03 mm spigot fit can bind.** The 316L spigot runs warmer than the 6061 port (it expands {ALPHA['SS'] * 1e6:.1f} against "
           f"{ALPHA['AL'] * 1e6:.1f} µm/m·K), and the hot fit falls to {spig:.0f} µm (with powder-filled gaps). Loosen it to ~0.10 mm radial, let "
           "the O-ring seal, and locate the module on the flange.",
           f"7. **Tier B (M50, 500 °C).** {tb0['P_heater_W']:.0f} W at the start ({tb0['sinks_W']['water_head'] + tb0['sinks_W']['water_flange']:.0f} W to water, "
           f"{tb0['sinks_W']['floor']:.0f} W to the floor) and {tb1['P_heater_W']:.0f} W at the end. Seals and O-rings ≤ "
           f"{max(tb0['T_seal_max'], tb1['T_seal_max'], tb0['T_oring_max'], tb1['T_oring_max'], tb0['T_gland_max'], tb1['T_gland_max']):.0f} °C "
           f"(bore seal at the build end: the tube beside the head runs hot), magnet ≤ {max(tb0['T_rod_end'], tb1['T_rod_end']):.0f} °C. But the "
           f"block reaches {tb0['T_block_max']:.0f} °C, too near 6061's ~580 °C solidus, so Tier B needs a steel or ceramic heater block. The "
           f"0.20 mm cold plate gap runs at {tb0['clear_plate_hot_mm'] * 1000:.0f} µm, so Tier B needs ≥ ~0.3 mm.",
           f"8. **Against the lumped estimate.** `requirements_budgets.py` puts the Ø50 loss at {LU['M50']['loss']:.0f} W, {LU['M50']['cyl']:.0f} W of "
           "it down a 60 mm cylinder wall assumed to be at plate temperature, and it has no plate-to-bore gap. The FEA agrees at the build end "
           f"({en['M50']['P_heater_W']:.0f} W; the wall beside the plate runs at ~{en['M50']['T_bore_ring_mean']:.0f} °C). At the build start, though, "
           f"the plate sits in a {MP.MODULES['M50']['spigot_wall']:.1f} mm-thick 316L spigot held near floor temperature, and the gap carries "
           f"~{m0['exit_W']['radial_gaps']:.0f} W across ~{MP.T_SET_A - m0['T_bore_ring_mean']:.0f} K. The FEA cool-downs are shorter than the lumped "
           f"{LU['S25']['cool_min']:.0f}–{LU['L75']['cool_min']:.0f} min for the same reason: the loss is larger.",
           f"9. **Chamber load.** {m0['into_chamber_W']:.0f} W (M50) to {st['L75']['into_chamber_W']:.0f} W (L75) go into the chamber at "
           f"build start, mostly through the floor. A 60 °C chamber cuts the M50 heater power by "
           f"{100 * (1 - g('M50_start_ch60_e0.5')['P_heater_W'] / m0['P_heater_W']):.0f} % but warms the spigot O-ring by "
           f"{g('M50_start_ch60_e0.5')['T_oring_max'] - m0['T_oring_max']:.0f} °C."]
    return "\n".join(out)


def write_report(data):
    """thermal.md from thermal.json (re-run with `report` to regenerate without solving)."""
    S, SG, LU = data["steady"], data["suggested"], data["lumped"]
    TR = {k: v for k, v in data["transient"].items() if "error" not in v}
    f0 = lambda v: "–" if v is None else f"{v:.0f}"  # noqa: E731

    def row(nm, label):
        r = S[nm]
        x, s = r["exit_W"], r["sinks_W"]
        tot = x["plate_top"] + x["radial_gaps"] + x["break"]
        return (f"| {label} | **{r['P_heater_W']:.0f}** | {r['T_plate_edge']:.0f} ({r['dT_centre_edge']:.1f}) | {r['T_block_max']:.0f} | "
                f"{r['T_seal_max']:.0f} | {r['T_oring_max']:.0f} | {r['T_gland_max']:.0f} | {r['T_rod_end']:.0f} | "
                f"{s['floor']:.0f} / {r['into_chamber_W']:.0f} | {100 * x['plate_top'] / tot:.0f} / {100 * x['radial_gaps'] / tot:.0f} / "
                f"{100 * x['break'] / tot:.0f} | {r['clear_plate_hot_mm'] * 1000:.0f} |")

    L = ["# Heated build modules: steady and transient thermal FEA (CalculiX, axisymmetric)", "",
         f"`analysis/thermal_module.py` builds an r–z model of each module from [`cad/module_params.py`](../../../cad/module_params.py) "
         f"(stack {data['params']['STACK']:.0f} mm: plate {data['params']['PLATE_T']:.0f}, heater block {data['params']['BLOCK_T']:.0f}, "
         f"break {data['params']['BREAK_T']:.0f}, head {data['params']['HEAD_T']:.0f}; rod {data['params']['ROD_L']:.0f} mm with its end hardware), "
         "meshes it with 8-node axisymmetric quads (CAX8) and solves it with ccx 2.21. For each steady case it finds, by a secant on "
         "heater power, the power that holds the **plate top centre at 200 °C**. Inputs: radial argon plate and 0.30 mm block "
         "gaps to the bore (cold radial plate clearance per size: " +
         ", ".join(f"{k} {m['plate_clear']:.2f} mm" for k, m in MP.MODULES.items()) + "); plate–block contact 2000 W/m²K; 8 mm argon break with smeared Macor posts and radiation through 2 shields; "
         "felt/PTFE bore seal on the head rim; 0.03 mm spigot fit plus an FKM O-ring; flange on the floor at 1500 W/m²K; floor edge "
         "(r = 120 mm) at the chamber temperature. Plate top: forced argon h 17 W/m²K (× (50/D)^0.5) plus radiation. Under the floor: "
         "5 W/m²K plus ε 0.3 to 25 °C. Coupling face: 10 W/m²K. Inside the cylinder below the head: adiabatic.", "",
         "## Tier A, 200 °C plate, chamber 25 °C, powder on the plate (ε 0.5)", "",
         "Temperatures in °C. Limits: felt/PTFE seal 204, FKM 200 (150 preferred), NdFeB magnet 80, block TCO "
         f"{LIMITS['tco']:.0f}. Loss split = share of heater power leaving the plate and block through the top / the radial gaps "
         "into the bore wall / the break into the head. Hot clearance = plate-to-bore radial clearance at temperature (µm, from "
         "the mean plate and bore-ring temperatures).", "",
         "| Module, position | Heater (W) | Plate edge (centre − edge) | Block max | Bore seal | Spigot O-ring | Rod-gland O-rings | "
         "Coupling face (magnet) | Floor / all into chamber (W) | Split top / gaps / break (%) | Hot clearance (µm) |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for key in ("S25", "M50", "L75"):
        for pos, lab in (("start", "build start (z_p 0)"), ("end", "build end (z_p −40)")):
            nm = f"{key}_{pos}_ch25_e0.5"
            if nm in S:
                L.append(row(nm, f"{key}, {lab}"))
    L += ["", "Heaters and transients (heat-up from 25 °C at full power with the plate at z_p 0; cool-down with the heaters off from the "
          "build-end steady state, to the 50 °C door interlock):", "",
          "| Module | Worst steady (W) | Installed now | ≥ 1.5 × worst, in whole heaters | Heat-up to 200 °C, installed | "
          "Heat-up, suggested | Block when the plate reaches 200 °C (suggested) | Least plate clearance in that heat-up (µm) | "
          "Cool-down to 50 °C |", "|---|---|---|---|---|---|---|---|---|"]
    for key in ("S25", "M50", "L75"):
        if key not in SG:
            continue
        sg, m = SG[key], MP.MODULES[key]
        h, hs, c = TR.get(f"heat_{key}"), TR.get(f"heatS_{key}"), TR.get(f"cool_{key}")
        ht = (f"{h['t_target_min']:.0f} min" if h and h["t_target_min"] else
              (f"never (levels at {h['T_centre_end']:.0f} °C)" if h else "–"))
        hst = (f"{hs['t_target_min']:.0f} min" if hs and hs["t_target_min"] else ("–" if not hs else f"never ({hs['T_centre_end']:.0f} °C)"))
        hx = hs or h
        L.append(f"| {key} | {sg['worst_steady_W']:.0f} | {m['heaters']} × {m['heater_w']:.0f} W = {sg['installed_W']:.0f} W | "
                 f"**{sg['n_suggested']} × {m['heater_w']:.0f} W = {sg['suggested_W']:.0f} W** | {ht} | {hst} | "
                 f"{f0(hx.get('T_block_at_target'))} °C | {min_clear_um(hx):.0f} | "
                 f"{f0(c['t_target_min']) + ' min' if c and c['t_target_min'] else '–'} |")
    # sensitivities
    L += ["", "## Sensitivities (heater power in W for 200 °C at the plate top centre)", "",
          "| Case | S25 start | S25 end | M50 start | M50 end | L75 start | L75 end |", "|---|---|---|---|---|---|---|"]
    for tag, lab in (("ch25_e0.5", "baseline: chamber 25 °C, powder ε 0.5"), ("ch60_e0.5", "chamber and floor edge at 60 °C"),
                     ("ch25_e0.1", "bare plate, ε 0.1 (start only)"), ("ch60_e0.1", "60 °C chamber, bare plate")):
        cells = []
        for key in ("S25", "M50", "L75"):
            for pos in ("start", "end"):
                r = S.get(f"{key}_{pos}_{tag}")
                cells.append(f"{r['P_heater_W']:.0f}" if r else "–")
        L.append(f"| {lab} | " + " | ".join(cells) + " |")
    pg = [S.get(f"M50_{p}_powdergaps") for p in ("start", "end")]
    if all(pg):
        L.append(f"| plate and block gaps full of powder (k 0.2), M50 | – | – | {pg[0]['P_heater_W']:.0f} | {pg[1]['P_heater_W']:.0f} | – | – |")
    for cp in (0.10, 0.20):
        r = S.get(f"M50_start_clear{cp:.2f}")
        if r:
            L.append(f"| plate radial gap {cp:.2f} mm instead of {MP.MODULES['M50']['plate_clear']:.2f} (M50) | – | – | "
                     f"{r['P_heater_W']:.0f} | – | – | – |")
    # tier B
    tb = [(p, S.get(f"M50_{p}_tierB")) for p in ("start", "end")]
    if all(r for _, r in tb):
        L += ["", "## Tier B reserve: M50 at 500 °C, 316L head with its underside held at 30 °C, 5 mm flange band at 30 °C", "",
              "| Position | Heater (W) | To water: head / flange (W) | Into floor (W) | Plate edge | Bore seal | Spigot O-ring | "
              "Rod-gland O-rings | Coupling face | Hot clearance (µm, 200 cold) |", "|---|---|---|---|---|---|---|---|---|---|"]
        for p, r in tb:
            s = r["sinks_W"]
            L.append(f"| {p} | **{r['P_heater_W']:.0f}** | {s['water_head']:.0f} / {s['water_flange']:.0f} | {s['floor']:.0f} | "
                     f"{r['T_plate_edge']:.0f} | {r['T_seal_max']:.0f} | {r['T_oring_max']:.0f} | {r['T_gland_max']:.0f} | "
                     f"{r['T_rod_end']:.0f} | {r['clear_plate_hot_mm'] * 1000:.0f} |")
    # lumped comparison
    L += ["", "## Against the lumped estimate in `requirements_budgets.py` (200 °C)", "",
          "| Module | Lumped: rad + conv + posts + cylinder = loss (W) | FEA start / end (W) | FEA: top / gaps / break, start (W) | "
          "Lumped cool-down | FEA cool-down |", "|---|---|---|---|---|---|"]
    for key in ("S25", "M50", "L75"):
        lu, a, b, c = LU[key], S.get(f"{key}_start_ch25_e0.5"), S.get(f"{key}_end_ch25_e0.5"), TR.get(f"cool_{key}")
        if not (a and b):
            continue
        x = a["exit_W"]
        L.append(f"| {key} | {lu['rad']:.0f} + {lu['conv']:.0f} + {lu['posts']:.0f} + {lu['cyl']:.0f} = {lu['loss']:.0f} | "
                 f"{a['P_heater_W']:.0f} / {b['P_heater_W']:.0f} | {x['plate_top']:.0f} / {x['radial_gaps']:.0f} / {x['break']:.0f} | "
                 f"{lu['cool_min']:.0f} min | {f0(c['t_target_min']) if c else '–'} min |")
    L += ["", "%%NARRATIVE%%", ""]
    # checks
    ms = {lab: S.get(f"M50_start_mesh_{lab}") for lab in ("coarse", "fine")}
    base = S.get("M50_start_ch25_e0.5")
    if base and all(ms.values()):
        L += ["## Mesh and checks", "",
              f"- Element size 1.0 mm in the module, growing to 4 mm at the floor edge; gaps and contact layers are one element across "
              f"({base['nodes']} nodes, {base['elements']} CAX8 for M50 at build start). M50 build-start power: 2 mm mesh "
              f"{ms['coarse']['P_heater_W']:.1f} W, 1 mm {base['P_heater_W']:.1f} W, 0.5 mm {ms['fine']['P_heater_W']:.1f} W "
              f"({100 * (ms['coarse']['P_heater_W'] / ms['fine']['P_heater_W'] - 1):+.1f} % and {100 * (base['P_heater_W'] / ms['fine']['P_heater_W'] - 1):+.1f} % against the finest). "
              "Transients use the 2 mm mesh and ccx's automatic steps (≤ 8 °C, ≤ 60–120 s).",
              f"- Energy balance: heater power against the sum of all sinks closes to "
              f"{max(abs(r['balance_err_pct']) for r in S.values()):.2f} % in every case. The exit split comes from gradients in the gap "
              f"elements and closes to {max(abs(r['exit_balance_err_pct']) for r in S.values() if r['case']['z_p'] == 0):.1f} % at build "
              "start; at build end the cake gradient at the plate's top corner is under-resolved, so the top share there is the remainder.",
              "- Units and ccx conventions checked on 1D cases (annulus conduction, film, radiation): " +
              ", ".join(f"{k} {v['err_pct']:+.2f} %" for k, v in data["sanity"].items()) +
              ". ccx reports CAX reaction heat for a 2° sector (×180)."]
    txt = "\n".join(L) + "\n"
    txt = txt.replace("%%NARRATIVE%%", narrative(S, TR, SG, LU))
    (OUT / "thermal.md").write_text(txt)


def _pool(fn, items):
    out = {}
    with cf.ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(fn, it): it["name"] for it in items}
        for f in cf.as_completed(futs):
            try:
                out[futs[f]] = f.result()
                print(f"  done {futs[f]}", flush=True)
            except Exception as exc:        # keep the other cases; the report shows the failure
                out[futs[f]] = dict(error=str(exc)[-400:])
                print(f"  FAILED {futs[f]}: {str(exc)[-200:]}", flush=True)
    return out


def main(argv):
    RUN.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    quick = "quick" in argv
    t0 = time.time()
    if "report" not in argv:
        san = sanity()
        print("sanity:", {k: round(v["err_pct"], 3) for k, v in san.items()})
        if "sanity" in argv:
            return
        cache = RUN / "steady_cache.json"
        if "resume" in argv and cache.exists():
            steady = json.loads(cache.read_text())
        else:
            steady = _pool(solve_steady, steady_cases(quick))
            cache.write_text(json.dumps(steady, default=float))
        steady = {k: v for k, v in steady.items() if "error" not in v}
        specs = transient_specs(quick)
        sugg = {}
        for key in sorted({r["case"]["key"] for r in steady.values()}):
            worst, n, pw = suggested_power(steady, key)
            m = MP.MODULES[key]
            sugg[key] = dict(worst_steady_W=worst, installed_W=m["heaters"] * m["heater_w"], n_suggested=n,
                             suggested_W=pw, heater_w=m["heater_w"])
            if not quick and abs(pw - m["heaters"] * m["heater_w"]) > 1e-6:
                specs.append(dict(name=f"heatS_{key}", key=key, z_p=0.0, T_ch=25.0, eps=EPS_POWDER, P_w=pw, T_init=25.0,
                                  t_end=3 * 3600.0, stop=MP.T_SET_A))
        trans = _pool(run_transient, specs)
        data = dict(sanity=san, steady=steady, transient=trans, suggested=sugg, lumped=lumped(), mesh_h0=H0,
                    params=dict(STACK=MP.STACK, PLATE_T=MP.PLATE_T, BLOCK_T=MP.BLOCK_T, BREAK_T=MP.BREAK_T,
                                HEAD_T=MP.HEAD_T, ROD_L=MP.ROD_L, BOT_FLANGE_T=MP.BOT_FLANGE_T, Z_P_MIN=MP.Z_P_MIN),
                    wall_s=round(time.time() - t0, 1))
        (OUT / "thermal.json").write_text(json.dumps(data, indent=1, default=float))
        print(f"wrote {OUT / 'thermal.json'} in {time.time() - t0:.0f} s")
    data = json.loads((OUT / "thermal.json").read_text())
    for key in ("S25", "M50", "L75"):
        nm = f"{key}_start_ch25_e0.5"
        if nm in data["steady"]:
            plot_map(nm, data["steady"][nm], OUT / f"thermal_map_{key}.png")
    plot_transients({k: v for k, v in data["transient"].items() if "error" not in v}, OUT / "thermal_transients.png")
    write_report(data)
    print(f"wrote {OUT / 'thermal.md'}")


if __name__ == "__main__":
    main(sys.argv[1:])
