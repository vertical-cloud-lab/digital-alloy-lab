"""3D quasi-steady melt-pool conduction in the beam's moving frame: finite volume, scipy sparse + AMG (issue #260; melt-pool.md).

What it solves (beam centre at the origin moving +x, so the material flows past at -v):
    div(k(T) grad T) + rho_m v dH/dx = 0,       H(T) = sensible + latent enthalpy (J/kg)
  - cell-centred finite volume on a tensor-product grid, uniform and fine over the melt pool (from an Eagar-Tsai estimate),
    geometrically stretched to 4-8 mm away; half domain y >= 0 (symmetry);
  - enthalpy is the unknown (Newton on T(H), which is Lipschitz, so the latent heat needs no smoothing: the "apparent heat
    capacity" dH/dT enters through the Jacobian); k(T) is lagged one iteration (Picard);
  - upwind advection of enthalpy; inflow face at T0 (x_max), outflow face (x_min) zero diffusive flux; bottom and far side at T0;
  - top surface: the Gaussian beam's absorbed flux A * 2P/(pi w^2) exp(-2 r^2/w^2), integrated exactly over each face, minus
    evaporation (Hertz-Knudsen-Langmuir, 0.82 net, latent heat of vaporisation of each element; props.Alloy.evap_heat_flux) and
    radiation (emissivity 0.2);
  - a powder layer (default 30 um) on top: mass flux phi*rho*v (packing phi 0.5) and k_powder 0.2 W/m K until the material at that
    (y, z) has melted upstream; bulk k(T) after;
  - liquid conductivity times a Marangoni factor f_M (default 2.5, swept 1-3), ramped by liquid fraction across the mushy zone.

It is a conduction model: no free surface, no vapour depression, no fluid flow. Where the scaling laws say a keyhole forms,
the depth it gives is the conduction depth, not the keyhole depth (melt-pool.md says which applies where).

Run:  OMP_NUM_THREADS=1 python fv3d.py case AlSi10Mg 320 1.1 --A 0.35       (one case, prints a summary)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass, field

import numpy as np
import scipy.sparse as sp
from scipy.special import erf

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import props as PR  # noqa: E402
import moving_source as MS  # noqa: E402


def stretched(lo, a, b, hi, h, r=1.18):
    """Face coordinates: uniform spacing h on [a, b], growing by ratio r outward to lo and hi."""
    n = max(1, int(round((b - a) / h)))
    mid = np.linspace(a, b, n + 1)
    left, d, x = [], h, a
    while x - lo > 1e-12:
        d *= r
        x = max(lo, x - d)
        if x - lo < 0.5 * d:
            x = lo
        left.append(x)
    right, d, x = [], h, b
    while hi - x > 1e-12:
        d *= r
        x = min(hi, x + d)
        if hi - x < 0.5 * d:
            x = hi
        right.append(x)
    return np.concatenate([left[::-1], mid, right])


@dataclass
class Case:
    alloy: str = "AlSi10Mg"
    P: float = 320.0             # W
    v: float = 1.1               # m/s
    d_spot: float = 96e-6        # 1/e^2 diameter, m
    A: float = 0.35              # absorptivity
    T0: float = 298.15           # preheat / substrate temperature, K
    f_M: float = 2.5             # Marangoni enhancement of liquid k
    t_layer: float = 30e-6       # powder layer, m (0 = bare plate)
    phi: float = 0.5             # powder packing
    k_powder: float = 0.2        # W/m K
    evap: bool = True
    f_vol: float = 1.0           # surface activity of Mg and Zn relative to the bulk (evaporation is supply-limited; see evap.py)
    eps: float = 0.2
    h: tuple = (5e-6, 4e-6, 3e-6)   # fine spacing dx, dy, dz
    tag: str = ""
    extra: dict = field(default_factory=dict)


class Solver:
    def __init__(self, c: Case):
        self.c = c
        self.al = PR.Alloy(c.alloy, k_liquid_factor=c.f_M)
        w = c.d_spot / 2
        self.w = w
        mp = self.al.mean_props(c.T0)
        rc = self.al.rho * mp["cp"]
        # Eagar-Tsai estimate of the mushy-zone extent (solidus isotherm) for the fine zone
        et = MS.pool_dims_et(c.A * c.P, c.v, rc, mp["alpha"], c.T0, w, self.al.T_sol)
        if et["L"] == 0:
            et = dict(x_front=1.5 * w, x_back=-2 * w, W=2 * w, D=w)
        self.et = et
        xb = min(-2.0 * w, 1.15 * et["x_back"]) - 3 * c.h[0]
        xf = max(1.5 * w, 1.15 * et["x_front"]) + 2 * c.h[0]
        yw = max(1.3 * w, 0.62 * et["W"]) + 2 * c.h[1]
        zd = max(c.t_layer + w, 1.1 * et["D"] + c.t_layer) + 2 * c.h[2]
        far = 6e-3 if c.v >= 0.5 else 9e-3
        self.xf = stretched(-1.6 * far, xb, xf, 0.7 * far, c.h[0])
        self.yf = stretched(0.0, 0.0, yw, far, c.h[1])
        zf = stretched(-far, -zd, 0.0, 0.0, c.h[2])
        # make a face at the bottom of the powder layer
        if c.t_layer > 0:
            j = np.argmin(np.abs(zf + c.t_layer))
            zf[j] = -c.t_layer
        self.zf = zf[::-1].copy()            # k = 0 at the top surface, increasing downward (z decreasing)
        self.xc = 0.5 * (self.xf[1:] + self.xf[:-1])
        self.yc = 0.5 * (self.yf[1:] + self.yf[:-1])
        self.zc = 0.5 * (self.zf[1:] + self.zf[:-1])
        self.dx, self.dy, self.dz = np.diff(self.xf), np.diff(self.yf), -np.diff(self.zf)
        self.nx, self.ny, self.nz = len(self.xc), len(self.yc), len(self.zc)
        self.N = self.nx * self.ny * self.nz
        self.layer = self.zc > -c.t_layer      # powder-layer cells (by z index)
        rho_m = np.where(self.layer, c.phi * self.al.rho, self.al.rho)
        self.rho_m = rho_m                    # mass density for the advective flux, per z index
        # laser flux on top faces (exact face integral of the Gaussian), W per face, half domain
        ex = erf(math.sqrt(2) * self.xf / w)
        ey = erf(math.sqrt(2) * self.yf / w)
        self.Qlaser = c.A * c.P / 4.0 * np.outer(np.diff(ex), np.diff(ey))     # (nx, ny), sums to A*P/2
        self.Atop = np.outer(self.dx, self.dy)
        self.idx = np.arange(self.N).reshape(self.nx, self.ny, self.nz)
        self.H0 = float(self.al.H(c.T0))

    # ------------------------------------------------------------------------------------------------------------ physics
    def k_field(self, T, update=True):
        """Bulk k(T); in the powder layer k_powder until the material at that (y, z) has melted upstream. The melted mask only
        grows once the iteration has settled (it_freeze), so cells can't toggle between powder and metal from one Newton step to
        the next."""
        c, al = self.c, self.al
        k = al.k(T)
        if c.t_layer > 0:
            Tl = T[:, :, self.layer]
            melted = np.maximum.accumulate(Tl[::-1, :, :], axis=0)[::-1] >= 0.5 * (al.T_sol + al.T_liq)
            if update:
                if getattr(self, "melted", None) is not None and getattr(self, "it", 0) >= 3:
                    melted = melted | self.melted
                self.melted = melted
            else:
                melted = self.melted
            kl = k[:, :, self.layer]
            kl = np.where(melted, kl, c.k_powder)
            k[:, :, self.layer] = kl
        return k

    def surf_loss(self, Ts):
        """Evaporation + radiation flux (W/m2) at surface temperature Ts, and its derivative."""
        c, al = self.c, self.al
        def q(T):
            out = c.eps * PR.SIGMA_SB * (T ** 4 - c.T0 ** 4)
            if c.evap:
                out = out + al.evap_heat_flux(T, f_vol=c.f_vol)
            return out
        q0 = q(Ts)
        dq = (q(Ts + 0.5) - q(Ts - 0.5)) / 1.0
        return q0, dq

    # ------------------------------------------------------------------------------------------------------------ assembly
    def assemble(self, h):
        c, al = self.c, self.al
        nx, ny, nz = self.nx, self.ny, self.nz
        T = al.T_of_H(h)
        tau = 1.0 / np.maximum(al.c_app(T), 1.0)
        k = self.k_field(T)
        F = np.zeros((nx, ny, nz))
        diag = np.zeros((nx, ny, nz))
        rows, cols, vals = [], [], []
        idx = self.idx

        def couple(K, sa, sb):
            # flux into a from b: K (T_b - T_a); contributes to both
            Ta, Tb = T[sa], T[sb]
            F[sa] += K * (Tb - Ta)
            F[sb] += K * (Ta - Tb)
            diag[sa] += K * tau[sa]
            diag[sb] += K * tau[sb]
            ia, ib = idx[sa].ravel(), idx[sb].ravel()
            Kr = K.ravel()
            rows.extend([ia, ib])
            cols.extend([ib, ia])
            vals.extend([-(Kr * tau[sb].ravel()), -(Kr * tau[sa].ravel())])

        dx, dy, dz = self.dx, self.dy, self.dz
        # x faces
        A_yz = np.outer(dy, dz)[None, :, :]
        Kx = A_yz / (0.5 * dx[:-1, None, None] / k[:-1] + 0.5 * dx[1:, None, None] / k[1:])
        couple(Kx, (slice(0, nx - 1),), (slice(1, nx),))
        # y faces
        A_xz = np.outer(dx, dz)[:, None, :]
        Ky = A_xz / (0.5 * dy[None, :-1, None] / k[:, :-1] + 0.5 * dy[None, 1:, None] / k[:, 1:])
        couple(Ky, (slice(None), slice(0, ny - 1)), (slice(None), slice(1, ny)))
        # z faces
        A_xy = np.outer(dx, dy)[:, :, None]
        Kz = A_xy / (0.5 * dz[None, None, :-1] / k[:, :, :-1] + 0.5 * dz[None, None, 1:] / k[:, :, 1:])
        couple(Kz, (slice(None), slice(None), slice(0, nz - 1)), (slice(None), slice(None), slice(1, nz)))
        # Dirichlet T0: x_max face (inflow), y_max, bottom
        for sl, K in (((nx - 1,), (np.outer(dy, dz)) / (0.5 * dx[-1] / k[-1])),
                      ((slice(None), ny - 1), (np.outer(dx, dz)) / (0.5 * dy[-1] / k[:, -1])),
                      ((slice(None), slice(None), nz - 1), (np.outer(dx, dy)) / (0.5 * dz[-1] / k[:, :, -1]))):
            F[sl] += K * (c.T0 - T[sl])
            diag[sl] += K * tau[sl]
        # advection: rho_m v A_x (h_E - h_P), h_E = H(T0) beyond x_max
        mflux = (self.rho_m[None, None, :] * c.v * A_yz)          # (1, ny, nz)
        hE = np.concatenate([h[1:], np.full((1, ny, nz), self.H0)], axis=0)
        F += mflux * (hE - h)
        diag += mflux * np.ones((nx, 1, 1))
        ia = idx[:-1].ravel()
        ib = idx[1:].ravel()
        rows.append(ia)
        cols.append(ib)
        vals.append(-(np.broadcast_to(mflux, (nx - 1, ny, nz)).ravel()))
        # top surface: laser in, evaporation and radiation out
        Ts = T[:, :, 0]
        q0, dq = self.surf_loss(Ts)
        F[:, :, 0] += self.Qlaser - self.Atop * q0
        diag[:, :, 0] += self.Atop * dq * tau[:, :, 0]
        rows.append(idx.ravel())
        cols.append(idx.ravel())
        vals.append(diag.ravel())
        Amat = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(self.N, self.N))
        return F, Amat, T, tau, k

    def initial(self):
        c, al = self.c, self.al
        mp = al.mean_props(c.T0)
        X, Y, Z = np.meshgrid(self.xc, self.yc, self.zc, indexing="ij")
        T = MS.eagar_tsai(X, Y, Z, c.A * c.P, c.v, al.rho * mp["cp"], mp["alpha"], c.T0, self.w, n=160)
        T = np.minimum(T, 0.9 * al.T_boil() + 0.1 * al.T_liq)
        return al.H(T)

    def solve(self, tol=0.5, maxit=60, verbose=True):
        import pyamg
        t0 = time.time()
        h = self.initial()
        hist = []
        ml = None
        omega = np.ones_like(h)
        dh_prev = np.zeros_like(h)
        for it in range(maxit):
            self.it = it
            F, Amat, T, tau, k = self.assemble(h)
            b = F.ravel()
            if ml is None or it % 4 == 0:
                ml = pyamg.ruge_stuben_solver(Amat.tocsr(), max_coarse=500)
            res = []
            dh = ml.solve(b, x0=np.zeros_like(b), tol=1e-7, accel="gmres", maxiter=60, residuals=res)
            dh = dh.reshape(h.shape)
            # per-cell damping: halve the step of any cell whose update changes sign (Newton cycling across the solidus or
            # liquidus kink), let it recover otherwise; then limit each cell's temperature change to +/-200 K
            flip = (np.sign(dh) != np.sign(dh_prev)) & (np.abs(tau * dh) > 1.0)
            omega = np.where(flip, np.maximum(0.5 * omega, 0.02), np.minimum(1.0, 1.3 * omega))
            h_new = h + omega * dh
            T_new = self.al.T_of_H(h_new)
            T_cl = np.clip(T_new, T - 200.0, T + 200.0)
            h_new = np.where(T_cl != T_new, self.al.H(T_cl), h_new)
            dT = self.al.T_of_H(h_new) - T
            m = float(np.max(np.abs(dT)))
            dh_prev = dh
            h = h_new
            hist.append(dict(it=it, dTmax=m, lin_res=float(res[-1] / max(res[0], 1e-30)) if res else None, Tmax=float(T.max())))
            if verbose:
                im = np.unravel_index(int(np.argmax(np.abs(dT))), dT.shape)
                print(f"  it {it:2d}  max|dT| {m:9.2f} K at {tuple(int(q) for q in im)} T={T[im]:7.1f}  Tmax {T.max():7.1f} K"
                      f"  lin {len(res)} its  {time.time() - t0:6.1f} s", flush=True)
            if m < tol:
                break
        self.h = h
        self.T = self.al.T_of_H(h)
        self.k = self.k_field(self.T, update=False)
        self.hist = hist
        self.seconds = time.time() - t0
        self.converged = hist[-1]["dTmax"] < tol
        return self.T

    # ------------------------------------------------------------------------------------------------------------ results
    def energy_balance(self):
        """Absorbed (full domain) vs evaporated + radiated + conducted out of the far boundaries + advected out (W)."""
        c, T = self.c, self.T
        q0, _ = self.surf_loss(T[:, :, 0])
        absorbed = 2 * self.Qlaser.sum()
        evap = 2 * float((self.Atop * (self.al.evap_heat_flux(T[:, :, 0], f_vol=c.f_vol) if c.evap else 0 * T[:, :, 0])).sum())
        rad = 2 * float((self.Atop * c.eps * PR.SIGMA_SB * (T[:, :, 0] ** 4 - c.T0 ** 4)).sum())
        A_yz = np.outer(self.dy, self.dz)
        adv_out = 2 * float((self.rho_m[None, :] * c.v * A_yz * (self.h[0] - self.H0)).sum())
        k = self.k
        cond = 2 * float((np.outer(self.dy, self.dz) / (0.5 * self.dx[-1] / k[-1]) * (T[-1] - c.T0)).sum()
                         + (np.outer(self.dx, self.dz) / (0.5 * self.dy[-1] / k[:, -1]) * (T[:, -1] - c.T0)).sum()
                         + (np.outer(self.dx, self.dy) / (0.5 * self.dz[-1] / k[:, :, -1]) * (T[:, :, -1] - c.T0)).sum())
        return dict(absorbed_W=absorbed, evaporation_W=evap, radiation_W=rad, advected_out_W=adv_out,
                    conducted_out_W=cond, balance_W=absorbed - evap - rad - adv_out - cond)

    def _cross(self, prof, coord, Tiso, side):
        """Interpolated coordinate where a profile crosses Tiso: side 'last' = the largest-coordinate crossing on the hot side."""
        above = prof >= Tiso
        if not above.any():
            return None
        ii = np.where(above)[0]
        if side == "max":
            i = ii[-1]
            if i + 1 >= len(prof):
                return coord[i]
            t = (prof[i] - Tiso) / (prof[i] - prof[i + 1])
            return coord[i] + t * (coord[i + 1] - coord[i])
        i = ii[0]
        if i == 0:
            return coord[0]
        t = (prof[i] - Tiso) / (prof[i] - prof[i - 1])
        return coord[i] + t * (coord[i - 1] - coord[i])

    def pool(self, Tiso=None):
        T = self.T
        Tiso = self.al.T_liq if Tiso is None else Tiso
        liq = T >= Tiso
        if not liq.any():
            return dict(L=0.0, W=0.0, D=0.0)
        # length along the top surface centreline row (and over all rows, the longest)
        L = 0.0
        x_back = x_front = None
        ii = np.argwhere(liq.any(axis=0))       # (j, k) rows with liquid
        for j, kk in ii:
            prof = T[:, j, kk]
            xa = self._cross(prof, self.xc, Tiso, "min")
            xb = self._cross(prof, self.xc, Tiso, "max")
            if xa is not None and xb - xa > L:
                L, x_back, x_front = xb - xa, xa, xb
        W = 0.0
        for i in np.where(liq[:, :, 0].any(axis=1))[0]:
            yy = self._cross(T[i, :, 0], self.yc, Tiso, "max")
            W = max(W, yy)
        D = 0.0
        for i in np.where(liq[:, 0, :].any(axis=1))[0]:
            zz = self._cross(T[i, 0, :], -self.zc, Tiso, "max")
            D = max(D, zz)
        # widest anywhere (sub-surface pools can be wider than at the top when the layer is powder)
        Wsub = 0.0
        for i, kk in np.argwhere(liq.any(axis=1)):
            yy = self._cross(T[i, :, kk], self.yc, Tiso, "max")
            Wsub = max(Wsub, yy)
        return dict(L=L, W=2 * W, W_any=2 * Wsub, D=D, x_back=x_back, x_front=x_front)

    def solidification(self):
        """Along each (y, z) row through the pool: where the rear of the pool crosses T_liq and T_sol; G, R, cooling rate and
        the time between the two crossings."""
        al, c, T = self.al, self.c, self.T
        gx, gy, gz = np.gradient(T, self.xc, self.yc, self.zc, edge_order=2)
        pts = []
        for j in range(self.ny):
            for kk in range(self.nz):
                prof = T[:, j, kk]
                if prof.max() < al.T_liq:
                    continue
                out = {}
                for name, Tiso in (("liq", al.T_liq), ("sol", al.T_sol)):
                    xa = self._cross(prof, self.xc, Tiso, "min")       # rear crossing
                    if xa is None:
                        break
                    i = int(np.clip(np.searchsorted(self.xc, xa) - 1, 0, self.nx - 2))
                    t = (xa - self.xc[i]) / (self.xc[i + 1] - self.xc[i])
                    g = [(1 - t) * gg[i, j, kk] + t * gg[i + 1, j, kk] for gg in (gx, gy, gz)]
                    G = math.sqrt(sum(q * q for q in g))
                    out[name] = dict(x=xa, G=G, R=c.v * g[0] / max(G, 1e-30), Tdot=c.v * g[0])
                if len(out) == 2:
                    pts.append(dict(y=float(self.yc[j]), z=float(self.zc[kk]), G=out["liq"]["G"], R=out["liq"]["R"],
                                    Tdot_liq=out["liq"]["Tdot"], Tdot_sol=out["sol"]["Tdot"], G_sol=out["sol"]["G"],
                                    t_sol=(out["liq"]["x"] - out["sol"]["x"]) / c.v,
                                    t_liquid=(self._cross(prof, self.xc, al.T_liq, "max") - out["liq"]["x"]) / c.v))
        return pts

    def surface_grid(self, xg, yg):
        """Top-cell temperatures interpolated to a regular (x, y) grid; y mirrored."""
        from scipy.interpolate import RegularGridInterpolator
        Ts = self.T[:, :, 0]
        yc = np.concatenate([-self.yc[::-1], self.yc])
        Tm = np.concatenate([Ts[:, ::-1], Ts], axis=1)
        f = RegularGridInterpolator((self.xc, yc), Tm, bounds_error=False, fill_value=self.c.T0)
        X, Y = np.meshgrid(xg, yg, indexing="ij")
        return f(np.stack([X.ravel(), Y.ravel()], axis=1)).reshape(X.shape)

    def summary(self):
        al, c = self.al, self.c
        Tsurf = self.T[:, :, 0]
        i, j = np.unravel_index(int(np.argmax(Tsurf)), Tsurf.shape)
        liq = self.pool(al.T_liq)
        mush = self.pool(al.T_sol)
        sol = self.solidification()
        out = dict(case=c.__dict__ | {"h": list(c.h)}, cells=self.N, seconds=round(self.seconds, 1), converged=self.converged,
                   iterations=len(self.hist), T_peak=float(Tsurf.max()), x_peak=float(self.xc[i]), T_boil_alloy=al.T_boil(),
                   T_liq=al.T_liq, T_sol=al.T_sol, liquid=liq, mushy=mush, energy=self.energy_balance())
        if sol:
            G = np.array([p["G"] for p in sol])
            R = np.array([p["R"] for p in sol])
            Td = np.array([p["Tdot_liq"] for p in sol])
            ts = np.array([p["t_sol"] for p in sol])
            tl = np.array([p["t_liquid"] for p in sol])
            # the surface centreline point and the deepest point
            cen = min(sol, key=lambda p: (p["y"], -p["z"]))
            deep = min(sol, key=lambda p: (p["z"]))
            out["solid"] = dict(n=len(sol), G_range=[float(G.min()), float(np.median(G)), float(G.max())],
                                R_range=[float(R.min()), float(np.median(R)), float(R.max())],
                                Tdot_range=[float(Td.min()), float(np.median(Td)), float(Td.max())],
                                t_sol_range=[float(ts.min()), float(np.median(ts)), float(ts.max())],
                                t_liquid_max=float(tl.max()), centre=cen, deepest=deep)
            self.sol_pts = sol
        return out


def run(c: Case, verbose=True):
    s = Solver(c)
    if verbose:
        print(f"{c.alloy} P={c.P} W v={c.v} m/s d={c.d_spot * 1e6:.0f} um A={c.A} T0={c.T0 - 273.15:.0f} C f_M={c.f_M} "
              f"layer={c.t_layer * 1e6:.0f} um: grid {s.nx} x {s.ny} x {s.nz} = {s.N} cells", flush=True)
    s.solve(verbose=verbose)
    return s, s.summary()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("alloy")
    ap.add_argument("P", type=float)
    ap.add_argument("v", type=float)
    ap.add_argument("--A", type=float, default=0.35)
    ap.add_argument("--d", type=float, default=96.0)
    ap.add_argument("--T0", type=float, default=25.0)
    ap.add_argument("--fM", type=float, default=2.5)
    ap.add_argument("--layer", type=float, default=30.0)
    ap.add_argument("--h", type=float, nargs=3, default=[5.0, 4.0, 3.0])
    ap.add_argument("--noevap", action="store_true")
    a = ap.parse_args()
    c = Case(alloy=a.alloy, P=a.P, v=a.v, A=a.A, d_spot=a.d * 1e-6, T0=a.T0 + 273.15, f_M=a.fM, t_layer=a.layer * 1e-6,
             h=tuple(x * 1e-6 for x in a.h), evap=not a.noevap)
    s, out = run(c)
    print(json.dumps({k: v for k, v in out.items() if k != "case"}, indent=1, default=float))


if __name__ == "__main__":
    main()
