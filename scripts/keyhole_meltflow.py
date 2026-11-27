"""Our own 3D steady-state melt-flow solver in the beam frame (PR #249, issue #235).

It adds Marangoni melt flow to the first-principles keyhole model (scripts/keyhole_first_principles.py), in the
spirit of the DebRoy group's convective weld-pool models and the AM module's steady-state mode: the top surface is
flat (no free-surface deformation) and the keyhole is a fixed cavity held at its wall temperature T_w.

Equations, in the frame of the beam (the plate moves at u_s = (-v, 0, 0)):

* continuity   div(rho u) = 0
* momentum     rho (u . grad) u = -grad p + div(mu grad u) - C (1 - f_l)^2 / (f_l^3 + eps) (u - u_s)
               (the Carman-Kozeny sink of the enthalpy-porosity method; f_l rises linearly from T_s to T_l)
* energy       rho u . grad H(T) = div(k(T) grad T), with H(T) the CALPHAD enthalpy (latent heat included)

Boundary conditions:
* top, z = 0 (z points down): w = 0 and the Marangoni shear mu du_t/dn = dsigma/dT grad_t T on the two tangential
  components; the beam enters as a Gaussian surface flux 2 A P / (pi r0^2) exp(-2 r^2 / r0^2) in conduction mode.
* y = 0 is a symmetry plane (half domain).
* front, rear, far side and bottom: the temperature of the analytic far field (a moving point source in the
  solid; the exact analytic field in the validation tests), and the plate velocity.
* keyhole mode: cells whose centres lie inside the keyhole (circular cross-sections of radius r(z) centred at
  x = xc(z), 0 <= z <= d) are held at T_w and blocked for flow. The keyhole wall is a free surface at uniform T,
  so it is shear-free and impermeable to the liquid (no Marangoni stress on it). The beam's power outside the
  keyhole opening enters as a surface flux.

Numerics: a finite-volume method on a non-uniform Cartesian grid, collocated, with Rhie-Chow face fluxes and
SIMPLEC pressure correction. Momentum and pressure correction are swept with line-by-line TDMA (numba) inside a
box that covers the liquid; the energy equation is assembled as a sparse matrix (power-law scheme, enthalpy
linearised about the last iterate) and solved with algebraic multigrid.

Usage (from the repo root):

    python scripts/keyhole_meltflow.py runs        # the three cases, Marangoni on and off -> first-principles/meltflow/
    python scripts/test_keyhole_meltflow.py        # validation

Requires numpy, scipy, numba, pyamg, pandas, matplotlib.
"""

from __future__ import annotations

import os

os.environ.setdefault("NUMBA_NUM_THREADS", "2")

import argparse  # noqa: E402
import dataclasses  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import pathlib  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numba as nb  # noqa: E402
import numpy as np  # noqa: E402
import pyamg  # noqa: E402
import scipy.sparse as sp  # noqa: E402
from scipy import special  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import keyhole_first_principles as kfp  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "arroyave-orchid-tools" / "keyhole-alternatives" / "first-principles" / "meltflow"
R_GAS = 8.314462618

# Liquid viscosity mu = mu_inf exp(E_A / R T): Kobatake, Schmitz & Brillo 2014 (J. Mater. Sci. 49, 3541,
# doi:10.1007/s10853-014-8072-z). Al: 0.281 mPa s and 12.3 kJ/mol; Al50Si50 (at%): 0.169 mPa s and 16.3 kJ/mol.
# AlSi10Mg and Al 5182 take the Al values; the blend (23.6 at% Si) is interpolated linearly in at%.
MU0_DEFAULT = 0.281e-3
E_MU_DEFAULT = 12.3e3
VISCOSITY = {"alsi10mg": (0.281e-3, 12.3e3), "blend": (0.228e-3, 14.2e3), "al5182": (0.281e-3, 12.3e3)}
DSIGMA_DT_DEFAULT = -1.27e-4  # N/m/K, Leitner et al. 2017
C_DARCY_DEFAULT = 1e9  # kg m^-3 s^-1
EPS_DARCY = 1e-3


# --------------------------------------------------------------------------------------------------------------
# grid
# --------------------------------------------------------------------------------------------------------------

def axis_faces(lo, hi, f_lo, f_hi, h_fine, h_cap, pool_lo, pool_hi, s1=0.08, s2=0.25):
    """Faces of a non-uniform 1D grid: cells of h_fine on [f_lo, f_hi], growing by s1 per unit distance (capped at
    h_cap) inside [pool_lo, pool_hi], then by s2 per unit distance outside it, out to [lo, hi]."""

    def h_at(x):
        d1 = max(f_lo - x, x - f_hi, 0.0)
        h = min(h_fine + s1 * d1, h_cap)
        d2 = max(pool_lo - x, x - pool_hi, 0.0)
        if d2 > 0:
            xe = pool_lo if x < pool_lo else pool_hi
            d1e = max(f_lo - xe, xe - f_hi, 0.0)
            h = min(h_fine + s1 * d1e, h_cap) + s2 * d2
        return h

    up = [f_hi]
    while up[-1] < hi - 1e-12:
        up.append(up[-1] + h_at(up[-1] + 0.5 * h_at(up[-1])))
    up[-1] = hi
    if len(up) > 2 and (up[-1] - up[-2]) < 0.5 * (up[-2] - up[-3]):
        up.pop(-2)
    n_mid = max(1, int(round((f_hi - f_lo) / h_fine)))
    mid = list(np.linspace(f_lo, f_hi, n_mid + 1))
    down = [f_lo]
    while down[-1] > lo + 1e-12:
        down.append(down[-1] - h_at(down[-1] - 0.5 * h_at(down[-1])))
    down[-1] = lo
    if len(down) > 2 and (down[-2] - down[-1]) < 0.5 * (down[-3] - down[-2]):
        down.pop(-2)
    faces = sorted(set(np.round(down[::-1][:-1] + mid + up[1:], 12)))
    return np.array(faces)


@dataclasses.dataclass
class Grid:
    xf: np.ndarray
    yf: np.ndarray
    zf: np.ndarray

    def __post_init__(self):
        self.xc = 0.5 * (self.xf[1:] + self.xf[:-1])
        self.yc = 0.5 * (self.yf[1:] + self.yf[:-1])
        self.zc = 0.5 * (self.zf[1:] + self.zf[:-1])
        self.dx, self.dy, self.dz = np.diff(self.xf), np.diff(self.yf), np.diff(self.zf)
        self.shape = (self.xc.size, self.yc.size, self.zc.size)
        self.V = self.dx[:, None, None] * self.dy[None, :, None] * self.dz[None, None, :]
        self.Ax = self.dy[:, None] * self.dz[None, :]  # (ny, nz)
        self.Ay = self.dx[:, None] * self.dz[None, :]  # (nx, nz)
        self.Az = self.dx[:, None] * self.dy[None, :]  # (nx, ny)

    @property
    def n(self):
        return int(np.prod(self.shape))


def make_grid(r0, x_rear, x_front, y_far, z_far, pool_x=(None, None), pool_y=None, pool_z=None, fine_x=None,
              fine_y=None, fine_z=None, h_fine=None, h_cap=None, hz_fine=None, s1=0.08, s2=0.25):
    """A grid fine (h_fine, default r0/8) around the beam and the keyhole, coarsening (to h_cap) over the pool and
    stretching fast beyond it."""
    h_fine = h_fine or r0 / 8
    hz_fine = hz_fine or h_fine
    h_cap = h_cap or 3 * h_fine
    fx = fine_x or (-1.5 * r0, 1.5 * r0)
    fy = fine_y or 1.5 * r0
    fz = fine_z or 1.5 * r0
    px = (pool_x[0] if pool_x[0] is not None else fx[0] - 10 * r0, pool_x[1] if pool_x[1] is not None else fx[1])
    py = pool_y or 6 * r0
    pz = pool_z or 6 * r0
    xf = axis_faces(x_rear, x_front, fx[0], fx[1], h_fine, h_cap, px[0], px[1], s1, s2)
    yf = axis_faces(0.0, y_far, 0.0, fy, h_fine, h_cap, 0.0, py, s1, s2)
    zf = axis_faces(0.0, z_far, 0.0, fz, hz_fine, h_cap, 0.0, pz, s1, s2)
    return Grid(xf, yf, zf)


# --------------------------------------------------------------------------------------------------------------
# properties
# --------------------------------------------------------------------------------------------------------------

@dataclasses.dataclass
class Props:
    """What the solver needs from a material. Built from keyhole_first_principles.Material, or constant."""
    rho: float
    T_s: float
    T_l: float
    H: object  # H(T), J/kg
    c: object  # dH/dT, J/kg/K (smoothed)
    k: object  # k(T), W/m/K
    mu0: float = MU0_DEFAULT
    E_mu: float = E_MU_DEFAULT
    dsigma_dT: float = DSIGMA_DT_DEFAULT
    C_darcy: float = C_DARCY_DEFAULT
    label: str = ""
    p_sat: object = None  # saturated vapour pressure p_sat(T), Pa (None: no evaporative cooling)
    M: float = 0.027  # molar mass of the vapour, kg/mol
    L_v: float = 0.0  # enthalpy of vaporisation, J/kg
    beta_back: float = 0.18  # back-condensed fraction (Knight 1979)

    def q_evap(self, T):
        """Evaporative heat loss (W/m^2): Hertz-Knudsen-Langmuir flux with 18 % back-condensation."""
        if self.p_sat is None:
            return np.zeros(np.shape(T))
        T = np.asarray(T, dtype=float)
        return self.L_v * (1 - self.beta_back) * self.p_sat(T) * np.sqrt(self.M / (2 * math.pi * R_GAS * T))

    def mu(self, T):
        Tm = np.maximum(T, self.T_s)
        return self.mu0 * np.exp(self.E_mu / (R_GAS * Tm))

    def f_l(self, T):
        return np.clip((T - self.T_s) / max(self.T_l - self.T_s, 1e-9), 0.0, 1.0)


def props_from_material(m: kfp.Material, smooth_K=15.0, evaporation=True, **kw) -> Props:
    """H is the CALPHAD enthalpy box-averaged over +/- smooth_K, and c its exact derivative, so the Newton
    linearisation of the advected enthalpy converges across the eutectic step (which the 5 K table makes a near
    jump). The averaging spreads the eutectic's latent heat over 2 smooth_K."""
    offs = np.linspace(-smooth_K, smooth_K, 31)

    def H(T):
        T = np.asarray(T, dtype=float)
        return np.trapezoid(m.H(T[..., None] + offs), offs, axis=-1) / (2 * smooth_K)

    def c(T):
        T = np.asarray(T, dtype=float)
        return (m.H(T + smooth_K) - m.H(T - smooth_K)) / (2 * smooth_K)

    def k(T):
        return m.k(T)

    ev = dict(p_sat=m.p_sat, M=m.M, L_v=m.L_v) if evaporation else {}
    return Props(rho=m.rho_s, T_s=m.T_s, T_l=m.T_l, H=H, c=c, k=k, label=m.name, **ev, **kw)


def props_constant(rho, c_p, k, T_s, T_l, **kw) -> Props:
    return Props(rho=rho, T_s=T_s, T_l=T_l, H=lambda T: c_p * np.asarray(T, dtype=float),
                 c=lambda T: np.full(np.shape(T), c_p, dtype=float), k=lambda T: np.full(np.shape(T), k, dtype=float),
                 label="constant", **kw)


# --------------------------------------------------------------------------------------------------------------
# heat input
# --------------------------------------------------------------------------------------------------------------

def gaussian_face_power(g: Grid, Q, r0):
    """Power of a Gaussian surface flux 2Q/(pi r0^2) exp(-2 r^2/r0^2) on each top face of the half domain (W)."""
    ex = special.erf(math.sqrt(2) * g.xf / r0)
    ey = special.erf(math.sqrt(2) * g.yf / r0)
    return Q / 4 * np.diff(ex)[:, None] * np.diff(ey)[None, :]


def wing_face_power(g: Grid, P_wings, r0, x_open, r_open, nsub=6):
    """The beam's power outside the keyhole opening (a circle at x_open, radius r_open) on the top faces, with the
    Gaussian's shape, normalised so the full-domain total is P_wings."""
    q = gaussian_face_power(g, 1.0, r0)
    frac = np.ones_like(q)
    near_i = np.where((g.xf[1:] > x_open - r_open) & (g.xf[:-1] < x_open + r_open))[0]
    near_j = np.where(g.yf[:-1] < r_open)[0]
    s = (np.arange(nsub) + 0.5) / nsub
    for i in near_i:
        xs = g.xf[i] + s * g.dx[i]
        for j in near_j:
            ys = g.yf[j] + s * g.dy[j]
            X, Y = np.meshgrid(xs, ys, indexing="ij")
            w = np.exp(-2 * (X ** 2 + Y ** 2) / r0 ** 2)
            out = ((X - x_open) ** 2 + Y ** 2) > r_open ** 2
            frac[i, j] = (w * out).sum() / w.sum()
    q = q * frac
    tot = q.sum()
    return q * (P_wings / 2) / tot if tot > 0 else q


# --------------------------------------------------------------------------------------------------------------
# keyhole geometry
# --------------------------------------------------------------------------------------------------------------

def keyhole_mask(g: Grid, keyhole):
    """Cells held at T_w. A cell counts if its centre lies within half a cell of the keyhole surface, so that the
    outermost T_w cell centres (where T = T_w is imposed) sit on the true surface on average, not half a cell inside
    it."""
    if keyhole is None:
        return np.zeros(g.shape, dtype=bool)
    zk = np.asarray(keyhole["z"], dtype=float)
    d = zk.max()
    X, Y, Z = np.meshgrid(g.xc, g.yc, g.zc, indexing="ij")
    hxy = 0.5 * np.sqrt(g.dx[:, None, None] * g.dy[None, :, None])
    hz = 0.5 * g.dz[None, None, :]
    r = np.interp(Z, zk, np.asarray(keyhole["r"], dtype=float))
    xc = np.interp(Z, zk, np.asarray(keyhole["xc"], dtype=float))
    return (Z <= d + hz) & ((X - xc) ** 2 + Y ** 2 <= (r + hxy) ** 2)


def cone_keyhole(a0, d, T_w, P_wings=0.0, n=60, tilt_xc_bottom=0.0):
    z = np.linspace(0, d, n)
    return dict(z=z, xc=tilt_xc_bottom * z / d, r=a0 * (1 - z / d), T_w=T_w, P_wings=P_wings, a0=a0)


# --------------------------------------------------------------------------------------------------------------
# energy equation (sparse, power-law, enthalpy linearised about T*)
# --------------------------------------------------------------------------------------------------------------

def _plaw_np(Pe):
    return np.maximum(0.0, 1.0 - 0.1 * np.abs(Pe)) ** 5


def assemble_energy(g: Grid, pr: Props, Ts, Fx, Fy, Fz, Tbc, q_top, kh, T_w):
    """Matrix and right-hand side for T. Tbc(x, y, z) gives the Dirichlet far-field temperature on the front, rear,
    far side and bottom. q_top is the power on each top face (half domain). Keyhole cells are held at T_w."""
    nx, ny, nz = g.shape
    idx = np.arange(g.n).reshape(g.shape)
    H = pr.H(Ts)
    c = pr.c(Ts)
    k = pr.k(Ts)
    Hc = H - c * Ts
    diag = np.zeros(g.shape)
    b = np.zeros(g.shape)
    rows, cols, vals = [], [], []
    khface = {}  # axis -> D across faces next to the keyhole, for the keyhole's heat

    def interior(axis):
        sl_L = [slice(None)] * 3
        sl_R = [slice(None)] * 3
        sl_L[axis] = slice(None, -1)
        sl_R[axis] = slice(1, None)
        sl_L, sl_R = tuple(sl_L), tuple(sl_R)
        f, cc = (g.xf, g.xc) if axis == 0 else (g.yf, g.yc) if axis == 1 else (g.zf, g.zc)
        shp = [1, 1, 1]
        shp[axis] = -1
        dl = (f[1:-1] - cc[:-1]).reshape(shp)
        dr = (cc[1:] - f[1:-1]).reshape(shp)
        if axis == 0:
            A, F = g.Ax[None, :, :], Fx[1:-1]
        elif axis == 1:
            A, F = g.Ay[:, None, :], Fy[:, 1:-1, :]
        else:
            A, F = g.Az[:, :, None], Fz[:, :, 1:-1]
        kL, kR = k[sl_L], k[sl_R]
        D = A / (dl / kL + dr / kR)
        cL, cR = c[sl_L], c[sl_R]
        HcL, HcR = Hc[sl_L], Hc[sl_R]
        Fp, Fm = np.maximum(F, 0.0), np.maximum(-F, 0.0)
        Pe = np.where(F > 0, Fp * cL, Fm * cR) / D
        Dp = D * _plaw_np(Pe)
        diag[sl_L] += Dp + cL * Fp
        diag[sl_R] += Dp + cR * Fm
        b[sl_L] += Fm * HcR - Fp * HcL
        b[sl_R] += Fp * HcL - Fm * HcR
        iL, iR = idx[sl_L], idx[sl_R]
        rows.extend([iL.ravel(), iR.ravel()])
        cols.extend([iR.ravel(), iL.ravel()])
        vals.extend([(-(Dp + cR * Fm)).ravel(), (-(Dp + cL * Fp)).ravel()])
        # faces between a keyhole cell and a liquid/solid cell: keep D for the keyhole's heat
        khL, khR = kh[sl_L], kh[sl_R]
        khface[axis] = (iL, iR, khL, khR, Dp, F)

    for ax in range(3):
        interior(ax)

    X, Y, Z = g.xc, g.yc, g.zc

    def dirichlet(sl, A, half, F_out, Tb):
        kP = k[sl]
        D = A * kP / half
        Fo = F_out
        Fp, Fm = np.maximum(Fo, 0.0), np.maximum(-Fo, 0.0)
        diag[sl] += D + c[sl] * Fp
        b[sl] += D * Tb + Fm * pr.H(Tb) - Fp * Hc[sl]

    # front (x max): inflow
    sl = (slice(nx - 1, nx), slice(None), slice(None))
    Tb = Tbc(np.full((1, ny, nz), g.xf[-1]), Y[None, :, None] + 0 * Z[None, None, :], Z[None, None, :] + 0 * Y[None, :, None])
    dirichlet(sl, g.Ax[None], (g.xf[-1] - g.xc[-1]), Fx[-1:], Tb)
    # rear (x min): outflow (outward flux = -Fx[0])
    sl = (slice(0, 1), slice(None), slice(None))
    Tb = Tbc(np.full((1, ny, nz), g.xf[0]), Y[None, :, None] + 0 * Z[None, None, :], Z[None, None, :] + 0 * Y[None, :, None])
    dirichlet(sl, g.Ax[None], (g.xc[0] - g.xf[0]), -Fx[:1], Tb)
    # far side (y max)
    sl = (slice(None), slice(ny - 1, ny), slice(None))
    Tb = Tbc(X[:, None, None] + 0 * Z[None, None, :], np.full((nx, 1, nz), g.yf[-1]), Z[None, None, :] + 0 * X[:, None, None])
    dirichlet(sl, g.Ay[:, None, :], (g.yf[-1] - g.yc[-1]), Fy[:, -1:, :], Tb)
    # bottom (z max)
    sl = (slice(None), slice(None), slice(nz - 1, nz))
    Tb = Tbc(X[:, None, None] + 0 * Y[None, :, None], Y[None, :, None] + 0 * X[:, None, None], np.full((nx, ny, 1), g.zf[-1]))
    dirichlet(sl, g.Az[:, :, None], (g.zf[-1] - g.zc[-1]), Fz[:, :, -1:], Tb)
    # top: surface heat input (symmetry plane and top are otherwise adiabatic, no flow through them)
    b[:, :, 0] += q_top
    if pr.p_sat is not None:
        # evaporative cooling, linearised about T*: q(T) ~ q* + q'* (T - T*)
        Tt = Ts[:, :, 0]
        q0 = pr.q_evap(Tt)
        dq = (pr.q_evap(Tt + 1.0) - pr.q_evap(Tt - 1.0)) / 2.0
        diag[:, :, 0] += dq * g.Az
        b[:, :, 0] += -(q0 - dq * Tt) * g.Az

    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    vals = np.concatenate(vals)
    khf = kh.ravel()
    if khf.any():
        # keyhole rows -> identity (scaled); couplings into keyhole cells -> right-hand side
        s = float(np.median(diag[~kh]))
        drop_row = khf[rows]
        to_rhs = (~drop_row) & khf[cols]
        bf = b.ravel()
        np.add.at(bf, rows[to_rhs], -vals[to_rhs] * T_w)
        keep = (~drop_row) & (~khf[cols])
        rows, cols, vals = rows[keep], cols[keep], vals[keep]
        df = diag.ravel()
        df[khf] = s
        bf[khf] = s * T_w
    A = sp.csr_matrix((np.concatenate([vals, diag.ravel()]),
                       (np.concatenate([rows, idx.ravel()]), np.concatenate([cols, idx.ravel()]))), shape=(g.n, g.n))
    return A, b.ravel(), khface


def keyhole_heat(g: Grid, T, khface, T_w, H=None):
    """Full-domain power the keyhole wall delivers (W): the net energy leaving the T_w cells through their faces,
    by conduction D (T_w - T) and, where the material passes through them (flow off), by advected enthalpy."""
    Tf = T.ravel()
    Q = 0.0
    for ax, (iL, iR, khL, khR, Dp, F) in khface.items():
        m1 = khL & ~khR  # keyhole on the left: outward flux +F
        Q += float((Dp[m1] * (T_w - Tf[iR[m1]])).sum())
        m2 = khR & ~khL  # keyhole on the right: outward flux -F
        Q += float((Dp[m2] * (T_w - Tf[iL[m2]])).sum())
        if H is not None:
            F1, F2 = F[m1], -F[m2]
            Q += float(np.where(F1 > 0, F1 * H(T_w), F1 * H(Tf[iR[m1]])).sum())
            Q += float(np.where(F2 > 0, F2 * H(T_w), F2 * H(Tf[iL[m2]])).sum())
    return 2 * Q


def solve_energy(g, pr, T, Fx, Fy, Fz, Tbc, q_top, kh, T_w, tol=1e-9):
    """Classical (Ruge-Stueben) AMG with BiCGSTAB; smoothed aggregation if that fails."""
    import warnings
    A, b, khface = assemble_energy(g, pr, T, Fx, Fy, Fz, Tbc, q_top, kh, T_w)
    x0 = T.ravel().copy()
    bn = float(np.linalg.norm(b)) or 1.0
    for kind in ("rs", "sa"):
        res = []
        with warnings.catch_warnings(), np.errstate(all="ignore"):
            warnings.simplefilter("ignore")
            try:
                if kind == "rs":
                    ml = pyamg.ruge_stuben_solver(A, max_coarse=400)
                else:
                    ml = pyamg.smoothed_aggregation_solver(A, symmetry="nonsymmetric", max_coarse=400)
                x = ml.solve(b, x0=x0, tol=tol, accel="bicgstab", maxiter=300, residuals=res)
            except (ValueError, FloatingPointError, np.linalg.LinAlgError):
                continue
        if np.all(np.isfinite(x)) and float(np.linalg.norm(b - A @ x)) / bn < 1e-6:
            return x.reshape(g.shape), khface, len(res)
    raise RuntimeError("energy solve failed")


# --------------------------------------------------------------------------------------------------------------
# flow: numba kernels (collocated SIMPLEC, Rhie-Chow, line-by-line TDMA inside the flow box)
# --------------------------------------------------------------------------------------------------------------

@nb.njit(cache=True, inline="always")
def _plaw(F, D):
    """Patankar's power-law coefficient for the neighbour on the +side of a face with flux F (+ direction)."""
    if D <= 0.0:
        return max(-F, 0.0)
    t = 1.0 - 0.1 * abs(F) / D
    a = D * t ** 5 if t > 0.0 else 0.0
    return a + max(-F, 0.0)


@nb.njit(cache=True)
def mom_coeffs(i0, i1, j1, k1, xc, yc, zc, xf, yf, zf, mu, Fx, Fy, Fz, kh, aE, aW, aN, aS, aB, aT, aP):
    for i in range(i0, i1):
        dxi = xf[i + 1] - xf[i]
        for j in range(0, j1):
            dyj = yf[j + 1] - yf[j]
            for k in range(0, k1):
                dzk = zf[k + 1] - zf[k]
                if kh[i, j, k]:
                    aE[i, j, k] = aW[i, j, k] = aN[i, j, k] = aS[i, j, k] = aB[i, j, k] = aT[i, j, k] = 0.0
                    aP[i, j, k] = 0.0
                    continue
                m = mu[i, j, k]
                Ax = dyj * dzk
                Ay = dxi * dzk
                Az = dxi * dyj
                # east / west
                if kh[i + 1, j, k]:
                    ae = 0.0
                else:
                    ae = _plaw(Fx[i + 1, j, k], 0.5 * (m + mu[i + 1, j, k]) * Ax / (xc[i + 1] - xc[i]))
                if kh[i - 1, j, k]:
                    aw = 0.0
                else:
                    aw = _plaw(-Fx[i, j, k], 0.5 * (m + mu[i - 1, j, k]) * Ax / (xc[i] - xc[i - 1]))
                # north / south (south of j = 0 is the symmetry plane: per-component)
                if kh[i, j + 1, k]:
                    an = 0.0
                else:
                    an = _plaw(Fy[i, j + 1, k], 0.5 * (m + mu[i, j + 1, k]) * Ay / (yc[j + 1] - yc[j]))
                if j == 0 or kh[i, j - 1, k]:
                    as_ = 0.0
                else:
                    as_ = _plaw(-Fy[i, j, k], 0.5 * (m + mu[i, j - 1, k]) * Ay / (yc[j] - yc[j - 1]))
                # bottom (k+1) / top (k-1; above k = 0 is the free surface: per-component)
                if kh[i, j, k + 1]:
                    ab = 0.0
                else:
                    ab = _plaw(Fz[i, j, k + 1], 0.5 * (m + mu[i, j, k + 1]) * Az / (zc[k + 1] - zc[k]))
                if k == 0 or kh[i, j, k - 1]:
                    at = 0.0
                else:
                    at = _plaw(-Fz[i, j, k], 0.5 * (m + mu[i, j, k - 1]) * Az / (zc[k] - zc[k - 1]))
                aE[i, j, k], aW[i, j, k], aN[i, j, k], aS[i, j, k], aB[i, j, k], aT[i, j, k] = ae, aw, an, as_, ab, at
                dF = (Fx[i + 1, j, k] - Fx[i, j, k]) + (Fy[i, j + 1, k] - Fy[i, j, k]) + (Fz[i, j, k + 1] - Fz[i, j, k])
                aP[i, j, k] = ae + aw + an + as_ + ab + at + max(dF, 0.0)


@nb.njit(cache=True)
def cell_gradient(i0, i1, j1, k1, xc, yc, zc, xf, yf, zf, p, kh, Gx, Gy, Gz):
    """Cell-centre gradient of p from linearly interpolated face values; zero-gradient at walls, the keyhole, the
    box edge, the top surface and the symmetry plane."""
    for i in range(i0, i1):
        for j in range(0, j1):
            for k in range(0, k1):
                if kh[i, j, k]:
                    Gx[i, j, k] = Gy[i, j, k] = Gz[i, j, k] = 0.0
                    continue
                pP = p[i, j, k]
                # x
                if i + 1 < i1 and not kh[i + 1, j, k]:
                    w = (xf[i + 1] - xc[i]) / (xc[i + 1] - xc[i])
                    pe = (1 - w) * pP + w * p[i + 1, j, k]
                else:
                    pe = pP
                if i - 1 >= i0 and not kh[i - 1, j, k]:
                    w = (xf[i] - xc[i - 1]) / (xc[i] - xc[i - 1])
                    pw = (1 - w) * p[i - 1, j, k] + w * pP
                else:
                    pw = pP
                Gx[i, j, k] = (pe - pw) / (xf[i + 1] - xf[i])
                # y
                if j + 1 < j1 and not kh[i, j + 1, k]:
                    w = (yf[j + 1] - yc[j]) / (yc[j + 1] - yc[j])
                    pn = (1 - w) * pP + w * p[i, j + 1, k]
                else:
                    pn = pP
                if j - 1 >= 0 and not kh[i, j - 1, k]:
                    w = (yf[j] - yc[j - 1]) / (yc[j] - yc[j - 1])
                    ps = (1 - w) * p[i, j - 1, k] + w * pP
                else:
                    ps = pP
                Gy[i, j, k] = (pn - ps) / (yf[j + 1] - yf[j])
                # z
                if k + 1 < k1 and not kh[i, j, k + 1]:
                    w = (zf[k + 1] - zc[k]) / (zc[k + 1] - zc[k])
                    pb = (1 - w) * pP + w * p[i, j, k + 1]
                else:
                    pb = pP
                if k - 1 >= 0 and not kh[i, j, k - 1]:
                    w = (zf[k] - zc[k - 1]) / (zc[k] - zc[k - 1])
                    pt = (1 - w) * p[i, j, k - 1] + w * pP
                else:
                    pt = pP
                Gz[i, j, k] = (pb - pt) / (zf[k + 1] - zf[k])


@nb.njit(cache=True)
def build_component(comp, i0, i1, j1, k1, xc, yc, zc, xf, yf, zf, mu, aE, aW, aN, aS, aB, aT, aP, darcy, kh, phi,
                    target, G, tau, alpha, ape_out, b_out, dRC, dC):
    """Diagonal and source for component comp (0 = u, 1 = v, 2 = w), with Darcy sink, pressure gradient, Marangoni
    shear (top cells), symmetry and top-wall conditions, and under-relaxation. Also d = V/aP for Rhie-Chow and the
    SIMPLEC d = V/(aP - sum a_nb)."""
    for i in range(i0, i1):
        dxi = xf[i + 1] - xf[i]
        for j in range(0, j1):
            dyj = yf[j + 1] - yf[j]
            for k in range(0, k1):
                dzk = zf[k + 1] - zf[k]
                V = dxi * dyj * dzk
                if kh[i, j, k]:
                    ape_out[i, j, k] = 1e30
                    b_out[i, j, k] = 0.0
                    dRC[i, j, k] = 0.0
                    dC[i, j, k] = 0.0
                    phi[i, j, k] = 0.0
                    continue
                snb = aP[i, j, k]
                ap = snb + darcy[i, j, k] * V
                bb = darcy[i, j, k] * V * target - V * G[i, j, k]
                if k == 0:
                    if comp == 2:
                        ap += mu[i, j, k] * dxi * dyj / (zc[0] - zf[0])  # w = 0 at the surface
                    else:
                        bb += tau[i, j] * dxi * dyj  # Marangoni shear on u, v
                if j == 0 and comp == 1:
                    ap += mu[i, j, k] * dxi * dzk / (yc[0] - yf[0])  # v = 0 on the symmetry plane
                ape = max(ap, 1e-300) / alpha
                ape_out[i, j, k] = ape
                b_out[i, j, k] = bb + (1 - alpha) * ape * phi[i, j, k]
                dRC[i, j, k] = V / ape
                dC[i, j, k] = V / max(ape - snb, 1e-300)


@nb.njit(cache=True, parallel=True)
def tdma_x(i0, i1, j1, k1, ap, aE, aW, aN, aS, aB, aT, b, phi):
    n = i1 - i0
    ny = phi.shape[1]
    for j in nb.prange(0, j1):
        P = np.empty(n)
        Q = np.empty(n)
        for k in range(0, k1):
            for m in range(n):
                i = i0 + m
                r = b[i, j, k] + aB[i, j, k] * phi[i, j, k + 1]
                if j + 1 < ny:
                    r += aN[i, j, k] * phi[i, j + 1, k]
                if j > 0:
                    r += aS[i, j, k] * phi[i, j - 1, k]
                if k > 0:
                    r += aT[i, j, k] * phi[i, j, k - 1]
                be = aE[i, j, k]
                cw = aW[i, j, k]
                if m == 0:
                    r += cw * phi[i - 1, j, k]
                    cw = 0.0
                if m == n - 1:
                    r += be * phi[i + 1, j, k]
                    be = 0.0
                if m > 0:
                    den = ap[i, j, k] - cw * P[m - 1]
                    Q[m] = (r + cw * Q[m - 1]) / den
                else:
                    den = ap[i, j, k]
                    Q[m] = r / den
                P[m] = be / den
            for m in range(n - 1, -1, -1):
                i = i0 + m
                if m == n - 1:
                    phi[i, j, k] = Q[m]
                else:
                    phi[i, j, k] = P[m] * phi[i + 1, j, k] + Q[m]


@nb.njit(cache=True, parallel=True)
def tdma_y(i0, i1, j1, k1, ap, aE, aW, aN, aS, aB, aT, b, phi):
    n = j1
    ny = phi.shape[1]
    for i in nb.prange(i0, i1):
        P = np.empty(n)
        Q = np.empty(n)
        for k in range(0, k1):
            for m in range(n):
                j = m
                r = b[i, j, k] + aE[i, j, k] * phi[i + 1, j, k] + aW[i, j, k] * phi[i - 1, j, k] \
                    + aB[i, j, k] * phi[i, j, k + 1]
                if k > 0:
                    r += aT[i, j, k] * phi[i, j, k - 1]
                be = aN[i, j, k]
                cw = aS[i, j, k]
                if m == 0:
                    cw = 0.0
                if m == n - 1:
                    if j + 1 < ny:
                        r += be * phi[i, j + 1, k]
                    be = 0.0
                if m > 0:
                    den = ap[i, j, k] - cw * P[m - 1]
                    Q[m] = (r + cw * Q[m - 1]) / den
                else:
                    den = ap[i, j, k]
                    Q[m] = r / den
                P[m] = be / den
            for m in range(n - 1, -1, -1):
                j = m
                if m == n - 1:
                    phi[i, j, k] = Q[m]
                else:
                    phi[i, j, k] = P[m] * phi[i, j + 1, k] + Q[m]


@nb.njit(cache=True, parallel=True)
def tdma_z(i0, i1, j1, k1, ap, aE, aW, aN, aS, aB, aT, b, phi):
    n = k1
    ny = phi.shape[1]
    for i in nb.prange(i0, i1):
        P = np.empty(n)
        Q = np.empty(n)
        for j in range(0, j1):
            for m in range(n):
                k = m
                r = b[i, j, k] + aE[i, j, k] * phi[i + 1, j, k] + aW[i, j, k] * phi[i - 1, j, k]
                if j + 1 < ny:
                    r += aN[i, j, k] * phi[i, j + 1, k]
                if j > 0:
                    r += aS[i, j, k] * phi[i, j - 1, k]
                be = aB[i, j, k]
                cw = aT[i, j, k]
                if m == 0:
                    cw = 0.0
                if m == n - 1:
                    r += be * phi[i, j, k + 1]
                    be = 0.0
                if m > 0:
                    den = ap[i, j, k] - cw * P[m - 1]
                    Q[m] = (r + cw * Q[m - 1]) / den
                else:
                    den = ap[i, j, k]
                    Q[m] = r / den
                P[m] = be / den
            for m in range(n - 1, -1, -1):
                k = m
                if m == n - 1:
                    phi[i, j, k] = Q[m]
                else:
                    phi[i, j, k] = P[m] * phi[i, j, k + 1] + Q[m]


@nb.njit(cache=True)
def rhie_chow(i0, i1, j1, k1, xc, yc, zc, xf, yf, zf, rho, us, u, v, w, p, Gx, Gy, Gz, dU, dV, dW, kh, Fx, Fy, Fz):
    """Face mass fluxes in the flow box from Rhie-Chow interpolation. Faces on the box edge carry the plate's flux;
    faces next to the keyhole, on the top surface and on the symmetry plane carry none."""
    # x faces i0 .. i1 (face i is between cells i-1 and i)
    for i in range(i0, i1 + 1):
        for j in range(0, j1):
            A = (yf[j + 1] - yf[j])
            for k in range(0, k1):
                Af = A * (zf[k + 1] - zf[k])
                if kh[i - 1, j, k] or kh[i, j, k]:
                    Fx[i, j, k] = 0.0
                elif i == i0 or i == i1:
                    Fx[i, j, k] = rho * us * Af
                else:
                    wR = (xf[i] - xc[i - 1]) / (xc[i] - xc[i - 1])
                    wL = 1 - wR
                    ub = wL * u[i - 1, j, k] + wR * u[i, j, k]
                    db = wL * dU[i - 1, j, k] + wR * dU[i, j, k]
                    gb = wL * Gx[i - 1, j, k] + wR * Gx[i, j, k]
                    Fx[i, j, k] = rho * Af * (ub + db * (gb - (p[i, j, k] - p[i - 1, j, k]) / (xc[i] - xc[i - 1])))
    # y faces 0 .. j1 (face j between cells j-1 and j); face 0 is the symmetry plane
    for i in range(i0, i1):
        dxi = xf[i + 1] - xf[i]
        for j in range(0, j1 + 1):
            for k in range(0, k1):
                Af = dxi * (zf[k + 1] - zf[k])
                if j == 0:
                    Fy[i, j, k] = 0.0
                elif kh[i, j - 1, k] or (j < Fy.shape[1] - 1 and kh[i, j, k]):
                    Fy[i, j, k] = 0.0
                elif j == j1:
                    Fy[i, j, k] = 0.0  # plate moves in x only
                else:
                    wR = (yf[j] - yc[j - 1]) / (yc[j] - yc[j - 1])
                    wL = 1 - wR
                    vb = wL * v[i, j - 1, k] + wR * v[i, j, k]
                    db = wL * dV[i, j - 1, k] + wR * dV[i, j, k]
                    gb = wL * Gy[i, j - 1, k] + wR * Gy[i, j, k]
                    Fy[i, j, k] = rho * Af * (vb + db * (gb - (p[i, j, k] - p[i, j - 1, k]) / (yc[j] - yc[j - 1])))
    # z faces 0 .. k1; face 0 is the top surface
    for i in range(i0, i1):
        dxi = xf[i + 1] - xf[i]
        for j in range(0, j1):
            Af = dxi * (yf[j + 1] - yf[j])
            for k in range(0, k1 + 1):
                if k == 0 or k == k1:
                    Fz[i, j, k] = 0.0
                elif kh[i, j, k - 1] or kh[i, j, k]:
                    Fz[i, j, k] = 0.0
                else:
                    wR = (zf[k] - zc[k - 1]) / (zc[k] - zc[k - 1])
                    wL = 1 - wR
                    wb = wL * w[i, j, k - 1] + wR * w[i, j, k]
                    db = wL * dW[i, j, k - 1] + wR * dW[i, j, k]
                    gb = wL * Gz[i, j, k - 1] + wR * Gz[i, j, k]
                    Fz[i, j, k] = rho * Af * (wb + db * (gb - (p[i, j, k] - p[i, j, k - 1]) / (zc[k] - zc[k - 1])))


@nb.njit(cache=True)
def pcorr_coeffs(i0, i1, j1, k1, xc, yc, zc, xf, yf, zf, rho, dU, dV, dW, kh, Fx, Fy, Fz,
                 aE, aW, aN, aS, aB, aT, aP, b):
    """SIMPLEC pressure-correction coefficients and the mass imbalance (b = inflow - outflow)."""
    tot = 0.0
    for i in range(i0, i1):
        dxi = xf[i + 1] - xf[i]
        for j in range(0, j1):
            dyj = yf[j + 1] - yf[j]
            for k in range(0, k1):
                dzk = zf[k + 1] - zf[k]
                aE[i, j, k] = aW[i, j, k] = aN[i, j, k] = aS[i, j, k] = aB[i, j, k] = aT[i, j, k] = 0.0
                if kh[i, j, k]:
                    aP[i, j, k] = 1.0
                    b[i, j, k] = 0.0
                    continue
                Ax, Ay, Az = dyj * dzk, dxi * dzk, dxi * dyj
                if i + 1 < i1 and not kh[i + 1, j, k]:
                    wR = (xf[i + 1] - xc[i]) / (xc[i + 1] - xc[i])
                    aE[i, j, k] = rho * Ax * ((1 - wR) * dU[i, j, k] + wR * dU[i + 1, j, k]) / (xc[i + 1] - xc[i])
                if i - 1 >= i0 and not kh[i - 1, j, k]:
                    wR = (xf[i] - xc[i - 1]) / (xc[i] - xc[i - 1])
                    aW[i, j, k] = rho * Ax * ((1 - wR) * dU[i - 1, j, k] + wR * dU[i, j, k]) / (xc[i] - xc[i - 1])
                if j + 1 < j1 and not kh[i, j + 1, k]:
                    wR = (yf[j + 1] - yc[j]) / (yc[j + 1] - yc[j])
                    aN[i, j, k] = rho * Ay * ((1 - wR) * dV[i, j, k] + wR * dV[i, j + 1, k]) / (yc[j + 1] - yc[j])
                if j - 1 >= 0 and not kh[i, j - 1, k]:
                    wR = (yf[j] - yc[j - 1]) / (yc[j] - yc[j - 1])
                    aS[i, j, k] = rho * Ay * ((1 - wR) * dV[i, j - 1, k] + wR * dV[i, j, k]) / (yc[j] - yc[j - 1])
                if k + 1 < k1 and not kh[i, j, k + 1]:
                    wR = (zf[k + 1] - zc[k]) / (zc[k + 1] - zc[k])
                    aB[i, j, k] = rho * Az * ((1 - wR) * dW[i, j, k] + wR * dW[i, j, k + 1]) / (zc[k + 1] - zc[k])
                if k - 1 >= 0 and not kh[i, j, k - 1]:
                    wR = (zf[k] - zc[k - 1]) / (zc[k] - zc[k - 1])
                    aT[i, j, k] = rho * Az * ((1 - wR) * dW[i, j, k - 1] + wR * dW[i, j, k]) / (zc[k] - zc[k - 1])
                s = aE[i, j, k] + aW[i, j, k] + aN[i, j, k] + aS[i, j, k] + aB[i, j, k] + aT[i, j, k]
                aP[i, j, k] = s + 1e-12 * (s + 1e-30) + 1e-300
                mout = (Fx[i + 1, j, k] - Fx[i, j, k]) + (Fy[i, j + 1, k] - Fy[i, j, k]) + (Fz[i, j, k + 1] - Fz[i, j, k])
                b[i, j, k] = -mout
                tot += abs(mout)
    return tot


@nb.njit(cache=True)
def pcorr_apply(i0, i1, j1, k1, xc, yc, zc, xf, yf, zf, rho, dU, dV, dW, kh, pp, Fx, Fy, Fz):
    """Correct the interior face fluxes of the box with the pressure correction pp."""
    for i in range(i0 + 1, i1):
        for j in range(0, j1):
            for k in range(0, k1):
                if kh[i - 1, j, k] or kh[i, j, k]:
                    continue
                Af = (yf[j + 1] - yf[j]) * (zf[k + 1] - zf[k])
                wR = (xf[i] - xc[i - 1]) / (xc[i] - xc[i - 1])
                d = (1 - wR) * dU[i - 1, j, k] + wR * dU[i, j, k]
                Fx[i, j, k] -= rho * Af * d * (pp[i, j, k] - pp[i - 1, j, k]) / (xc[i] - xc[i - 1])
    for i in range(i0, i1):
        for j in range(1, j1):
            for k in range(0, k1):
                if kh[i, j - 1, k] or kh[i, j, k]:
                    continue
                Af = (xf[i + 1] - xf[i]) * (zf[k + 1] - zf[k])
                wR = (yf[j] - yc[j - 1]) / (yc[j] - yc[j - 1])
                d = (1 - wR) * dV[i, j - 1, k] + wR * dV[i, j, k]
                Fy[i, j, k] -= rho * Af * d * (pp[i, j, k] - pp[i, j - 1, k]) / (yc[j] - yc[j - 1])
    for i in range(i0, i1):
        for j in range(0, j1):
            for k in range(1, k1):
                if kh[i, j, k - 1] or kh[i, j, k]:
                    continue
                Af = (xf[i + 1] - xf[i]) * (yf[j + 1] - yf[j])
                wR = (zf[k] - zc[k - 1]) / (zc[k] - zc[k - 1])
                d = (1 - wR) * dW[i, j, k - 1] + wR * dW[i, j, k]
                Fz[i, j, k] -= rho * Af * d * (pp[i, j, k] - pp[i, j, k - 1]) / (zc[k] - zc[k - 1])


# --------------------------------------------------------------------------------------------------------------
# the coupled solve
# --------------------------------------------------------------------------------------------------------------

@dataclasses.dataclass
class FlowState:
    u: np.ndarray
    v: np.ndarray
    w: np.ndarray
    p: np.ndarray
    Fx: np.ndarray
    Fy: np.ndarray
    Fz: np.ndarray


def plate_state(g: Grid, rho, v_scan):
    nx, ny, nz = g.shape
    u = np.full(g.shape, -v_scan)
    Fx = np.empty((nx + 1, ny, nz))
    Fx[:] = rho * (-v_scan) * g.Ax[None, :, :]
    return FlowState(u=u, v=np.zeros(g.shape), w=np.zeros(g.shape), p=np.zeros(g.shape), Fx=Fx,
                     Fy=np.zeros((nx, ny + 1, nz)), Fz=np.zeros((nx, ny, nz + 1)))


def marangoni_stress(g: Grid, T, pr: Props):
    Ts = T[:, :, 0]
    dTdx = np.zeros_like(Ts)
    dTdx[1:-1] = (Ts[2:] - Ts[:-2]) / (g.xc[2:] - g.xc[:-2])[:, None]
    dTdy = np.zeros_like(Ts)
    dTdy[:, 1:-1] = (Ts[:, 2:] - Ts[:, :-2]) / (g.yc[2:] - g.yc[:-2])[None, :]
    dTdy[:, 0] = (Ts[:, 1] - Ts[:, 0]) / (g.yc[1] + g.yc[0])  # mirror across the symmetry plane
    liquid = Ts > pr.T_s
    return pr.dsigma_dT * dTdx * liquid, pr.dsigma_dT * dTdy * liquid


def flow_box(g: Grid, T, pr: Props, kh, old=None, margin=3):
    hot = (T >= pr.T_s - 30.0) | kh
    if not hot.any():
        return None
    ii, jj, kk = np.where(hot)
    nx, ny, nz = g.shape
    i0 = max(1, ii.min() - margin)
    i1 = min(nx - 1, ii.max() + margin + 1)
    j1 = min(ny - 1, jj.max() + margin + 1)
    k1 = min(nz - 1, kk.max() + margin + 1)
    if old is not None:
        i0, i1, j1, k1 = min(i0, old[0]), max(i1, old[1]), max(j1, old[2]), max(k1, old[3])
    return (int(i0), int(i1), int(j1), int(k1))


@dataclasses.dataclass
class Case:
    label: str
    props: Props
    P: float  # laser power, W
    v: float  # scan speed, m/s
    r0: float  # 1/e^2 radius, m
    T0: float
    A: float = 0.0  # absorbed fraction (conduction mode)
    keyhole: dict | None = None
    grid: Grid | None = None
    Tbc: object = None  # far-field temperature function; default: moving point source in the solid
    Q_far: float | None = None  # power for the default far field


def far_field_point_source(pr: Props, T0, T_s, v):
    Tg = np.linspace(T0, T_s - 1.0, 200)
    k_ff = float(np.trapezoid(pr.k(Tg), Tg) / (Tg[-1] - Tg[0]))
    c_ff = float((pr.H(T_s - 1.0) - pr.H(T0)) / (T_s - 1.0 - T0))
    kappa = k_ff / (pr.rho * c_ff)

    def make(Q):
        def Tbc(x, y, z):
            R = np.maximum(np.sqrt(x * x + y * y + z * z), 1e-9)
            return T0 + Q / (2 * math.pi * k_ff * R) * np.exp(-v * (R + x) / (2 * kappa))
        return Tbc
    return make, k_ff, kappa


def solve_case(case: Case, flow=True, n_outer=60, n_inner=25, alpha_u=0.5, alpha_p=0.8, alpha_T=0.6,
               p_passes=6, tolT=0.5, tol_pool=0.003, verbose=False, log=print):
    """Steady state for one case. flow=False holds the velocity at the plate's (conduction with advection only)."""
    t0 = time.time()
    g, pr = case.grid, case.props
    nx, ny, nz = g.shape
    rho = pr.rho
    kh = keyhole_mask(g, case.keyhole)
    T_w = float(case.keyhole["T_w"]) if case.keyhole is not None else 0.0
    if case.keyhole is None:
        q_top = gaussian_face_power(g, case.A * case.P, case.r0)
    else:
        kk = case.keyhole
        q_top = wing_face_power(g, kk.get("P_wings", 0.0), case.r0, float(kk["xc"][0]), float(kk["r"][0]))
        q_top[kh[:, :, 0]] = 0.0
    if case.Tbc is not None:
        Tbc = case.Tbc
        make_ff = None
    else:
        make_ff, _, _ = far_field_point_source(pr, case.T0, pr.T_s, case.v)
        Q_far = case.Q_far if case.Q_far is not None else (case.A * case.P if case.keyhole is None else None)
        if Q_far is None:
            Q_far = 0.5 * case.P  # first guess, updated from the keyhole's heat
        Tbc = make_ff(Q_far)
    st = plate_state(g, rho, case.v)
    T = np.full(g.shape, case.T0)
    T[kh] = T_w
    hist = []
    # 1) flow-off solution (velocity = plate's); a few passes for the enthalpy linearisation and far field
    for it in range(8):
        Tn, khface, nres = solve_energy(g, pr, T, st.Fx, st.Fy, st.Fz, Tbc, q_top, kh, T_w)
        dT = float(np.abs(Tn - T).max())
        T = T + (Tn - T) * (1.0 if it < 2 else alpha_T)
        if case.keyhole is not None and case.Tbc is None:
            Qk = keyhole_heat(g, T, khface, T_w, pr.H)
            Tbc = make_ff(Qk + float(case.keyhole.get("P_wings", 0.0)))
        if verbose:
            log(f"  energy-only pass {it}: max dT {dT:.2f} K, krylov its {nres}")
        if dT < tolT and it >= 2:
            break
    out = {"flow": bool(flow)}
    if flow:
        aE, aW, aN, aS, aB, aT, aP = (np.zeros(g.shape) for _ in range(7))
        ape, bb, dRC_u, dC_u, dRC_v, dC_v, dRC_w, dC_w = (np.zeros(g.shape) for _ in range(8))
        Gx, Gy, Gz = np.zeros(g.shape), np.zeros(g.shape), np.zeros(g.shape)
        pa = [np.zeros(g.shape) for _ in range(8)]
        pp = np.zeros(g.shape)
        box = None
        args_geo = (g.xc, g.yc, g.zc, g.xf, g.yf, g.zf)
        for outer in range(n_outer):
            mu = pr.mu(T)
            fl = pr.f_l(T)
            darcy = pr.C_darcy * (1 - fl) ** 2 / (fl ** 3 + EPS_DARCY)
            taux, tauy = marangoni_stress(g, T, pr)
            box = flow_box(g, T, pr, kh, box)
            if box is None:
                break
            i0, i1, j1, k1 = box
            for inner in range(n_inner):
                mom_coeffs(i0, i1, j1, k1, *args_geo, mu, st.Fx, st.Fy, st.Fz, kh, aE, aW, aN, aS, aB, aT, aP)
                cell_gradient(i0, i1, j1, k1, *args_geo, st.p, kh, Gx, Gy, Gz)
                for comp, phi, target, G, tau, dRC, dC in (
                        (0, st.u, -case.v, Gx, taux, dRC_u, dC_u), (1, st.v, 0.0, Gy, tauy, dRC_v, dC_v),
                        (2, st.w, 0.0, Gz, taux, dRC_w, dC_w)):
                    build_component(comp, i0, i1, j1, k1, *args_geo, mu, aE, aW, aN, aS, aB, aT, aP, darcy, kh, phi,
                                    target, G, tau, alpha_u, ape, bb, dRC, dC)
                    for _ in range(2):
                        tdma_x(i0, i1, j1, k1, ape, aE, aW, aN, aS, aB, aT, bb, phi)
                        tdma_z(i0, i1, j1, k1, ape, aE, aW, aN, aS, aB, aT, bb, phi)
                        tdma_y(i0, i1, j1, k1, ape, aE, aW, aN, aS, aB, aT, bb, phi)
                rhie_chow(i0, i1, j1, k1, *args_geo, rho, -case.v, st.u, st.v, st.w, st.p, Gx, Gy, Gz,
                          dRC_u, dRC_v, dRC_w, kh, st.Fx, st.Fy, st.Fz)
                mres = pcorr_coeffs(i0, i1, j1, k1, *args_geo, rho, dC_u, dC_v, dC_w, kh, st.Fx, st.Fy, st.Fz,
                                    *pa)
                pp[:] = 0.0
                for _ in range(p_passes):
                    tdma_x(i0, i1, j1, k1, pa[6], pa[0], pa[1], pa[2], pa[3], pa[4], pa[5], pa[7], pp)
                    tdma_z(i0, i1, j1, k1, pa[6], pa[0], pa[1], pa[2], pa[3], pa[4], pa[5], pa[7], pp)
                    tdma_y(i0, i1, j1, k1, pa[6], pa[0], pa[1], pa[2], pa[3], pa[4], pa[5], pa[7], pp)
                pcorr_apply(i0, i1, j1, k1, *args_geo, rho, dC_u, dC_v, dC_w, kh, pp, st.Fx, st.Fy, st.Fz)
                cell_gradient(i0, i1, j1, k1, *args_geo, pp, kh, Gx, Gy, Gz)
                bsl = (slice(i0, i1), slice(0, j1), slice(0, k1))
                st.u[bsl] -= dC_u[bsl] * Gx[bsl]
                st.v[bsl] -= dC_v[bsl] * Gy[bsl]
                st.w[bsl] -= dC_w[bsl] * Gz[bsl]
                st.p[bsl] += alpha_p * pp[bsl]
            # energy with the new fluxes
            Tn, khface, nres = solve_energy(g, pr, T, st.Fx, st.Fy, st.Fz, Tbc, q_top, kh, T_w)
            dTa = np.abs(Tn - T)
            dT = float(dTa.max())
            iw = np.unravel_index(int(np.argmax(dTa)), dTa.shape)
            T = T + alpha_T * (Tn - T)
            if case.keyhole is not None and case.Tbc is None:
                Qk = keyhole_heat(g, T, khface, T_w, pr.H)
                Tbc = make_ff(Qk + float(case.keyhole.get("P_wings", 0.0)))
            m_ref = rho * case.v * (g.yf[j1] * g.zf[k1])
            umax = float(np.sqrt((st.u[:, :, 0] + case.v) ** 2 + st.v[:, :, 0] ** 2).max())
            dims = np.array(pool_dims(g, T, pr.T_l)[:3])
            hist.append({"outer": outer, "dT_max_K": dT, "mass_residual_rel": mres / max(m_ref, 1e-30),
                         "u_surface_max_rel_m_s": umax, "box": list(box),
                         "pool_liquidus_DWL_um": [round(float(q) * 1e6, 2) for q in dims]})
            if verbose:
                log(f"  outer {outer}: box {box}, max dT {dT:.2f} K at {tuple(int(q) for q in iw)} T={T[iw]:.0f}, "
                    f"mass res {mres / m_ref:.2e}, "
                    f"max surface speed {umax:.3f} m/s, krylov {nres}")
            # converged when T has settled everywhere, or when the pool's size has stopped changing (a few cells at
            # the melting front can keep a +/-10 K limit cycle between the flow and the energy solve)
            if outer >= 4 and mres / m_ref < 1e-3:
                prev = [np.array(h["pool_liquidus_DWL_um"]) for h in hist[-4:-1]]
                cur = np.array(hist[-1]["pool_liquidus_DWL_um"])
                steady = len(prev) == 3 and all(np.all(np.abs(cur - q) <= tol_pool * np.maximum(cur, 1.0)) for q in prev)
                if dT < tolT or steady:
                    break
    # final: energy balance and outputs
    A_, b_, khface = assemble_energy(g, pr, T, st.Fx, st.Fy, st.Fz, Tbc, q_top, kh, T_w)
    out.update(pool_metrics(g, T, pr))
    out.update(energy_balance(g, pr, T, st, Tbc, q_top, kh, T_w, khface))
    surf = np.sqrt((st.u[:, :, 0] + case.v) ** 2 + st.v[:, :, 0] ** 2)
    out["u_surface_max_rel_m_s"] = float(surf[~kh[:, :, 0]].max())  # speed relative to the plate
    out["u_max_rel_m_s"] = float(np.sqrt((st.u + case.v) ** 2 + st.v ** 2 + st.w ** 2)[~kh].max())
    out["T_peak_K"] = float(T[~kh].max())
    out["grid_cells"] = g.n
    out["grid_shape"] = list(g.shape)
    out["h_min_um"] = [round(float(g.dx.min()) * 1e6, 2), round(float(g.dy.min()) * 1e6, 2), round(float(g.dz.min()) * 1e6, 2)]
    out["runtime_s"] = round(time.time() - t0, 1)
    out["outer_iterations"] = len(hist)
    out["history"] = hist
    return out, T, st, kh


def pool_metrics(g: Grid, T, pr: Props):
    res = {}
    for tag, Tiso in (("liquidus", pr.T_l), ("solidus", pr.T_s)):
        D, W, L, Dmax = pool_dims(g, T, Tiso)
        res[f"pool_depth_{tag}_um"] = D * 1e6
        res[f"pool_width_{tag}_um"] = W * 1e6
        res[f"pool_length_{tag}_um"] = L * 1e6
        res[f"pool_depth_max_{tag}_um"] = Dmax * 1e6
    return res


def _crossing(coords, vals, iso):
    """Last position (from the start) where vals stays >= iso before dropping below it, interpolated."""
    above = vals >= iso
    if not above[0]:
        return 0.0
    k = np.argmin(above) if not above.all() else above.size
    if k >= above.size:
        return coords[-1]
    a, b = vals[k - 1], vals[k]
    return coords[k - 1] + (a - iso) / (a - b) * (coords[k] - coords[k - 1])


def pool_dims(g: Grid, T, Tiso):
    """Depth (on the centre plane), width (at the surface) and length (surface centre line), as pool_dimensions in
    keyhole_first_principles; plus the deepest point anywhere."""
    zc = np.concatenate([[0.0], g.zc])
    yc = np.concatenate([[0.0], g.yc])
    depth = 0.0
    Tc = T[:, 0, :]
    for i in range(g.shape[0]):
        col = np.concatenate([[Tc[i, 0]], Tc[i]])
        depth = max(depth, _crossing(zc, col, Tiso))
    dmax = 0.0
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            if T[i, j, 0] >= Tiso:
                col = np.concatenate([[T[i, j, 0]], T[i, j]])
                dmax = max(dmax, _crossing(zc, col, Tiso))
    half = 0.0
    for i in range(g.shape[0]):
        row = np.concatenate([[T[i, 0, 0]], T[i, :, 0]])
        half = max(half, _crossing(yc, row, Tiso))
    line = T[:, 0, 0]
    if line.max() < Tiso:
        return depth, 2 * half, 0.0, dmax
    ih = int(np.argmax(line))
    xf = _crossing(g.xc[ih:], line[ih:], Tiso)
    xr = _crossing(g.xc[ih::-1], line[ih::-1], Tiso)
    return depth, 2 * half, xf - xr, dmax


def energy_balance(g: Grid, pr: Props, T, st: FlowState, Tbc, q_top, kh, T_w, khface):
    """Full-domain powers: heat in (surface + keyhole) against heat out (conduction and enthalpy through the
    boundaries)."""
    nx, ny, nz = g.shape
    k = pr.k(T)
    H = pr.H(T)
    Q_in_surface = 2 * float(q_top[~kh[:, :, 0]].sum())
    Q_kh = keyhole_heat(g, T, khface, T_w, pr.H) if kh.any() else 0.0
    out = 0.0
    X, Y, Z = g.xc, g.yc, g.zc
    # front (x max)
    Tb = Tbc(np.full((ny, nz), g.xf[-1]), Y[:, None] + 0 * Z[None, :], Z[None, :] + 0 * Y[:, None])
    F = st.Fx[-1]
    out += float((k[-1] * g.Ax / (g.xf[-1] - g.xc[-1]) * (T[-1] - Tb)).sum())
    out += float((np.where(F > 0, F * H[-1], F * pr.H(Tb))).sum())
    # rear (x min): outward flux -Fx[0]
    Tb = Tbc(np.full((ny, nz), g.xf[0]), Y[:, None] + 0 * Z[None, :], Z[None, :] + 0 * Y[:, None])
    F = -st.Fx[0]
    out += float((k[0] * g.Ax / (g.xc[0] - g.xf[0]) * (T[0] - Tb)).sum())
    out += float((np.where(F > 0, F * H[0], F * pr.H(Tb))).sum())
    # far side
    Tb = Tbc(X[:, None] + 0 * Z[None, :], np.full((nx, nz), g.yf[-1]), Z[None, :] + 0 * X[:, None])
    out += float((k[:, -1, :] * g.Ay / (g.yf[-1] - g.yc[-1]) * (T[:, -1, :] - Tb)).sum())
    # bottom
    Tb = Tbc(X[:, None] + 0 * Y[None, :], Y[None, :] + 0 * X[:, None], np.full((nx, ny), g.zf[-1]))
    out += float((k[:, :, -1] * g.Az / (g.zf[-1] - g.zc[-1]) * (T[:, :, -1] - Tb)).sum())
    Q_evap = float((pr.q_evap(T[:, :, 0]) * g.Az)[~kh[:, :, 0]].sum())
    out = 2 * (out + Q_evap)
    Q_in = Q_in_surface + Q_kh
    return {"Q_in_surface_W": Q_in_surface, "Q_keyhole_W": Q_kh, "Q_out_W": out, "Q_evap_surface_W": 2 * Q_evap,
            "energy_balance_rel_err": (out - Q_in) / max(Q_in, 1e-12)}


# --------------------------------------------------------------------------------------------------------------
# cases
# --------------------------------------------------------------------------------------------------------------

def grid_for(r0, pool_D, pool_W, pool_L_rear, keyhole_d=0.0, h_fine=None, h_cap=None, far=2.5e-3, hz_fine=None):
    """A grid sized from an estimate of the pool (with flow the pool can grow, so the 'pool' zone is generous)."""
    h_fine = h_fine or r0 / 8
    fz = max(1.5 * r0, keyhole_d + 0.5 * r0)
    return make_grid(r0, x_rear=-(1.8 * pool_L_rear + far), x_front=2.5 * r0 + 0.6 * far,
                     y_far=1.4 * pool_W / 2 + far, z_far=1.5 * pool_D + far,
                     pool_x=(-1.8 * pool_L_rear, 2.0 * r0), pool_y=1.4 * pool_W / 2, pool_z=1.5 * pool_D,
                     fine_x=(-2.0 * r0, 1.5 * r0), fine_y=1.6 * r0, fine_z=fz, h_fine=h_fine, h_cap=h_cap,
                     hz_fine=hz_fine)


def build_cases(h_fine_frac=8.0, mu0=None, E_mu=None, dsigma_dT=DSIGMA_DT_DEFAULT, C_darcy=C_DARCY_DEFAULT,
                materials=None, evaporation=True):
    """The three runs. materials may map 'alsi10mg', 'blend' and 'al5182' to Material objects (e.g. with a sourced
    k(T)); by default they come from keyhole_first_principles. mu0/E_mu override the sourced viscosities."""
    materials = materials or {}

    def kw_for(key):
        m0, e0 = VISCOSITY[key]
        return dict(mu0=mu0 if mu0 is not None else m0, E_mu=E_mu if E_mu is not None else e0,
                    dsigma_dT=dsigma_dT, C_darcy=C_darcy, evaporation=evaporation)

    cases = []
    # 1) AlSi10Mg 250 W 0.9 m/s, conduction, A = AM module's
    a = kfp.ALLOYS["alsi10mg"]
    m = materials.get("alsi10mg") or kfp.alloy_material("alsi10mg")
    pr = props_from_material(m, **kw_for("alsi10mg"))
    r0 = a["r0"]
    g = grid_for(r0, pool_D=150e-6, pool_W=300e-6, pool_L_rear=700e-6, h_fine=r0 / h_fine_frac)
    cases.append(Case(label="alsi10mg-250W-0.9-conduction-A_am", props=pr, P=250.0, v=0.9, r0=r0, T0=a["T0"],
                      A=a["A_am"], grid=g))
    # 2) blend 375 W 0.4 m/s, keyhole (cone at the AM module's A)
    a = kfp.ALLOYS["blend"]
    m = materials.get("blend") or kfp.alloy_material("blend")
    tab = kfp.ray_table(m, "cone")
    res = kfp.solve_point(m, 375.0, 0.4, a["r0"], a["T0"], tab, A_override=a["A_am"], hatch=a["hatch"])
    s, gg = res.d_um / res.a0_um, res.a0_um * 1e-6 / a["r0"]
    A_kh, A_sf, _, _ = tab(s, gg)
    scale = a["A_am"] / (A_kh + A_sf)
    P_w = A_sf * scale * 375.0
    kh = cone_keyhole(res.a0_um * 1e-6, res.d_um * 1e-6, res.T_w, P_wings=P_w)
    pr = props_from_material(m, **kw_for("blend"))
    r0 = a["r0"]
    g = grid_for(r0, pool_D=400e-6, pool_W=550e-6, pool_L_rear=1500e-6, keyhole_d=res.d_um * 1e-6,
                 h_fine=r0 / h_fine_frac)
    cases.append(Case(label="blend-375W-0.4-keyhole-cone-A_am", props=pr, P=375.0, v=0.4, r0=r0, T0=a["T0"],
                      A=a["A_am"], keyhole=kh, grid=g))
    cases[-1].analytic = dataclasses.asdict(res)
    # 3) NIST AM-Bench 2022 Al 5182, keyhole (cone at the measured A = 0.43)
    amb = kfp.AMB2022
    m = materials.get("al5182") or kfp.al5182_material()
    tab = kfp.ray_table(m, "cone")
    res = kfp.solve_point(m, amb["P"], amb["v"], amb["r0"], amb["T0"], tab, A_override=amb["A_keyhole"])
    s, gg = res.d_um / res.a0_um, res.a0_um * 1e-6 / amb["r0"]
    A_kh, A_sf, _, _ = tab(s, gg)
    scale = amb["A_keyhole"] / (A_kh + A_sf)
    P_w = A_sf * scale * amb["P"]
    kh = cone_keyhole(res.a0_um * 1e-6, res.d_um * 1e-6, res.T_w, P_wings=P_w)
    pr = props_from_material(m, **kw_for("al5182"))
    r0 = amb["r0"]
    g = grid_for(r0, pool_D=200e-6, pool_W=420e-6, pool_L_rear=900e-6, keyhole_d=res.d_um * 1e-6,
                 h_fine=r0 / h_fine_frac)
    cases.append(Case(label="al5182-473W-0.7-keyhole-cone-A_measured", props=pr, P=amb["P"], v=amb["v"], r0=r0,
                      T0=amb["T0"], A=amb["A_keyhole"], keyhole=kh, grid=g))
    cases[-1].analytic = dataclasses.asdict(res)
    return cases


def _row(case, out):
    keep = ["flow", "pool_depth_liquidus_um", "pool_width_liquidus_um", "pool_length_liquidus_um",
            "pool_depth_solidus_um", "pool_width_solidus_um", "pool_length_solidus_um", "pool_depth_max_liquidus_um",
            "u_surface_max_rel_m_s", "u_max_rel_m_s", "T_peak_K", "Q_in_surface_W", "Q_keyhole_W", "Q_out_W",
            "energy_balance_rel_err", "grid_cells", "outer_iterations", "runtime_s"]
    r = {"case": case.label, "P_W": case.P, "v_m_s": case.v, "r0_um": case.r0 * 1e6, "A": case.A}
    if case.keyhole is not None:
        r.update({"keyhole_a0_um": case.keyhole["a0"] * 1e6, "keyhole_depth_um": float(np.max(case.keyhole["z"])) * 1e6,
                  "T_w_K": case.keyhole["T_w"], "P_wings_W": case.keyhole["P_wings"]})
    r.update({k: out[k] for k in keep if k in out})
    return r


def run_all(out_dir=OUT_DIR, log=print, only=None, **kw):
    import pandas as pd
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, full = [], {}
    fields = {}
    for case in build_cases(**kw):
        if only and only not in case.label:
            continue
        log(f"{case.label}: grid {case.grid.shape} = {case.grid.n} cells")
        for flow in (False, True):
            out, T, st, kh = solve_case(case, flow=flow, verbose=True, log=log)
            r = _row(case, out)
            rows.append(r)
            full[f"{case.label}|flow={flow}"] = {**r, "history": out["history"],
                                                  "analytic": getattr(case, "analytic", None)}
            log(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}))
            if flow:
                fields[case.label] = (case, T, st, kh)
    pd.DataFrame(rows).to_csv(out_dir / "meltflow-runs.csv", index=False, float_format="%.5g")
    (out_dir / "meltflow-runs.json").write_text(json.dumps({"params": {
        "viscosity_mu_inf_Pa_s_E_J_mol": {k: list(v) for k, v in VISCOSITY.items()},
        "viscosity_source": "Kobatake, Schmitz & Brillo 2014, J. Mater. Sci. 49, 3541 (doi:10.1007/s10853-014-8072-z)",
        "mu0_override_Pa_s": kw.get("mu0"), "E_mu_override_J_mol": kw.get("E_mu"),
        "dsigma_dT_N_m_K": kw.get("dsigma_dT", DSIGMA_DT_DEFAULT), "C_darcy": kw.get("C_darcy", C_DARCY_DEFAULT),
        "eps_darcy": EPS_DARCY}, "runs": full}, indent=1, default=float) + "\n")
    for label, (case, T, st, kh) in fields.items():
        if "blend" in label:
            figure(case, T, st, kh, out_dir / "meltflow-blend-375W-section.png")
    return rows


def figure(case, T, st, kh, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    g, pr = case.grid, case.props
    sel_x = (g.xc > -2.2e-3) & (g.xc < 0.4e-3)
    sel_y = g.yc < 0.5e-3
    sel_z = g.zc < 0.6e-3
    fig, axes = plt.subplots(2, 1, figsize=(10, 7.5), constrained_layout=True)
    ax = axes[0]
    X, Y = np.meshgrid(g.xc[sel_x] * 1e3, g.yc[sel_y] * 1e3, indexing="ij")
    Ts = T[np.ix_(sel_x, sel_y, [0])][:, :, 0]
    cs = ax.contourf(X, Y, Ts, levels=30, cmap="inferno")
    ax.contour(X, Y, Ts, levels=[pr.T_s, pr.T_l], colors=["#9ecae1", "white"], linewidths=1.2)
    U = st.u[np.ix_(sel_x, sel_y, [0])][:, :, 0] + case.v
    Vv = st.v[np.ix_(sel_x, sel_y, [0])][:, :, 0]
    sk = (slice(None, None, 3), slice(None, None, 2))
    ax.quiver(X[sk], Y[sk], U[sk], Vv[sk], color="#2a78d6", scale=60, width=0.0016)
    ax.set_aspect("equal")
    ax.set_title(f"{case.label}: top surface, T (K) and velocity relative to the plate", fontsize=9)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    fig.colorbar(cs, ax=ax, shrink=0.8)
    ax = axes[1]
    X, Z = np.meshgrid(g.xc[sel_x] * 1e3, g.zc[sel_z] * 1e3, indexing="ij")
    Tc = T[np.ix_(sel_x, [0], sel_z)][:, 0, :]
    cs = ax.contourf(X, Z, Tc, levels=30, cmap="inferno")
    ax.contour(X, Z, Tc, levels=[pr.T_s, pr.T_l], colors=["#9ecae1", "white"], linewidths=1.2)
    U = st.u[np.ix_(sel_x, [0], sel_z)][:, 0, :] + case.v
    W = st.w[np.ix_(sel_x, [0], sel_z)][:, 0, :]
    sk = (slice(None, None, 3), slice(None, None, 2))
    ax.quiver(X[sk], Z[sk], U[sk], -W[sk], color="#2a78d6", scale=60, width=0.0016)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_title("centre plane y = 0 (white: liquidus, blue: solidus)", fontsize=9)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    fig.colorbar(cs, ax=ax, shrink=0.8)
    fig.savefig(path, dpi=130)
    plt.close(fig)


def run_sensitivity(out_dir=OUT_DIR, log=print, case_key="alsi10mg"):
    """The Carman-Kozeny constant C, one decade each way, on one case with flow on."""
    import pandas as pd
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for C in (1e8, 1e9, 1e10):
        case = [c for c in build_cases(C_darcy=C) if case_key in c.label][0]
        out, T, st, kh = solve_case(case, flow=True)
        r = {"C_darcy": C, **_row(case, out)}
        rows.append(r)
        log(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}))
    pd.DataFrame(rows).to_csv(out_dir / f"meltflow-darcy-sensitivity-{case_key}.csv", index=False, float_format="%.5g")
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["runs", "sensitivity"])
    ap.add_argument("--only", default=None)
    ap.add_argument("--h-fine-frac", type=float, default=8.0)
    ap.add_argument("--case", default="alsi10mg")
    ap.add_argument("--out", type=pathlib.Path, default=OUT_DIR)
    a = ap.parse_args()
    if a.cmd == "sensitivity":
        run_sensitivity(a.out, case_key=a.case)
        return
    run_all(a.out, only=a.only, h_fine_frac=a.h_fine_frac)


if __name__ == "__main__":
    main()
