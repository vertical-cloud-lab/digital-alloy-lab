#!/usr/bin/env python3
"""Thermal lensing of the cover slide, the chamber window and the f-theta at 500 W (issue #260).

Two models:
  1. analytic central curvature of a thin plate heated by a Gaussian beam (heat flows radially to a cool rim):
        dioptric power D0 = chi * P_abs / (pi * k * w^2),   chi = dn/dT + (n - 1)(1 + nu) alpha
     (mech.md E used P_abs dn/dT / (2 pi k w^2), the uniform-heating form, and dz = f^2 D with f = 160 mm);
  2. a numerical axisymmetric steady-state conduction solve (finite volumes, r-z) of the real disc, with the absorbed
     power in a thin layer at the fouled face (or spread through the bulk), rim held at the mount temperature, faces
     losing heat by radiation + natural convection in argon; the optical path difference is integrated through the
     thickness and the Gaussian-weighted best-fit defocus gives the effective lens power D_eff.
The focus moves toward the lens by dz = h^2 D / (1 + h D) for an element h (air-equivalent) above the focus.

Writes analysis/out/optics/thermal_lens.json / .md / .png. Units SI inside the solver, mm and W in the tables.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "optics"
OUT.mkdir(parents=True, exist_ok=True)

# fused silica (Corning 7980 data sheet: k 1.38 W/mK, dn/dT 9.6e-6 /K near 1 um as used in mech.md, alpha 0.52e-6 /K,
# nu 0.16, rho 2201 kg/m3, c 740 J/kgK); n at 1070 nm from Malitson (beam_path.py)
FS = dict(k=1.38, dndT=9.6e-6, alpha=0.52e-6, nu=0.16, n=1.4496, rho=2201.0, c=740.0)
FS["chi"] = FS["dndT"] + (FS["n"] - 1) * (1 + FS["nu"]) * FS["alpha"]
# N-BK7 (Schott data sheet: k 1.114, dn/dT abs ~2.4e-6 at 1060 nm, alpha 7.1e-6, nu 0.206, n 1.507): a marking-lens glass
BK7 = dict(k=1.114, dndT=2.4e-6, alpha=7.1e-6, nu=0.206, n=1.507)
BK7["chi"] = BK7["dndT"] + (BK7["n"] - 1) * (1 + BK7["nu"]) * BK7["alpha"]

P = 500.0
SIGMA = 5.670e-8


def beam_w(D_coll_mm: float, h_air_mm: float) -> float:
    """1/e2 radius (m) of the converging beam h (air-equivalent) above the focus, f = 160 mm (far from focus)."""
    return D_coll_mm / 2 * h_air_mm / 160.0 * 1e-3


def solve_disc(R_m, t_m, w_m, P_abs, where="bottom", rim="fixed", h_face=10.0, mat=FS, nr=160, nz=24):
    """Axisymmetric steady conduction. Returns r (m), OPD(r) (m), T rise at centre and rim (K).
    where: 'bottom' / 'top' (absorbing film in the first cell layer at that face) or 'bulk' (uniform through t).
    rim: 'fixed' (rim at the mount temperature) or 'insulated' (all heat leaves through the faces)."""
    k = mat["k"]
    dr, dz = R_m / nr, t_m / nz
    rc = (np.arange(nr) + 0.5) * dr
    N = nr * nz
    idx = lambda i, j: j * nr + i
    rows, cols, vals = [], [], []
    b = np.zeros(N)
    # absorbed power density
    q_r = P_abs * 2 / (math.pi * w_m ** 2) * np.exp(-2 * rc ** 2 / w_m ** 2)      # W/m2 (surface flux equivalent)
    for j in range(nz):
        for i in range(nr):
            p = idx(i, j)
            V = 2 * math.pi * rc[i] * dr * dz
            diag = 0.0
            # radial faces
            for di in (-1, 1):
                ii = i + di
                rf = rc[i] + di * dr / 2
                A = 2 * math.pi * rf * dz
                if 0 <= ii < nr:
                    g = k * A / dr
                    rows.append(p); cols.append(idx(ii, j)); vals.append(-g); diag += g
                elif ii == nr and rim == "fixed":
                    g = k * A / (dr / 2)
                    diag += g          # T_rim = 0
            # axial faces
            for dj in (-1, 1):
                jj = j + dj
                A = 2 * math.pi * rc[i] * dr
                if 0 <= jj < nz:
                    g = k * A / dz
                    rows.append(p); cols.append(idx(i, jj)); vals.append(-g); diag += g
                else:
                    g = 1.0 / (1.0 / (h_face * A) + (dz / 2) / (k * A))
                    diag += g
            rows.append(p); cols.append(p); vals.append(diag)
            # source
            Aface = 2 * math.pi * rc[i] * dr
            if where == "bulk":
                b[p] += q_r[i] * Aface / nz
            elif (where == "bottom" and j == 0) or (where == "top" and j == nz - 1):
                b[p] += q_r[i] * Aface
    A = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))
    T = spla.spsolve(A.tocsc(), b).reshape(nz, nr)
    # optical path: chi * integral of T over the thickness
    opd = mat["chi"] * T.sum(axis=0) * dz
    return rc, opd, float(T[:, 0].mean()), float(T[:, -1].mean()), float(T.max())


def fit_defocus(r, opd, w):
    """Gaussian-intensity-weighted least-squares fit OPD ~ a + b r^2; D_eff = -2 b (1/m)."""
    wt = np.exp(-2 * r ** 2 / w ** 2) * r
    X = np.vstack([np.ones_like(r), r ** 2]).T
    W = np.diag(wt)
    a, bb = np.linalg.lstsq(np.sqrt(W) @ X, np.sqrt(W) @ opd, rcond=None)[0]
    resid = opd - (a + bb * r ** 2)
    rms = math.sqrt(float((wt * resid ** 2).sum() / wt.sum()))
    return -2 * bb, rms


def focus_shift(h_m, D):
    return h_m ** 2 * D / (1 + h_m * D)


def zr_mm(D_coll):
    d = 4 * 1.1 * 1.070e-3 * 160 / (math.pi * D_coll)
    return math.pi * (d / 2) ** 2 / (1.1 * 1.070e-3)


ELEMENTS = {
    # name: (R of the disc to the rim contact, thickness, air-equivalent height above focus, fouled face)
    "cover slide (Ø50.8 x 3, rim on the drawer)": (23.0e-3, 3.0e-3, 0.126, "bottom"),
    "window (Ø50.8 x 8, O-ring seat Ø44.9)": (22.45e-3, 8.0e-3, 0.147, "bottom"),
}
ABS = {"clean, uncoated (bulk 20 ppm/cm + 2 x 5 ppm surfaces)": None,
       "clean, AR both faces (2 x 30 ppm + bulk)": None,
       "light film 0.05 %": 5e-4, "fogged 0.5 %": 5e-3, "sooted 2 %": 2e-2}

res = dict(material=dict(fused_silica=FS, NBK7=BK7), cases=[], lens=[], check=[])

for D_coll in (5.0, 3.2):
    zR = zr_mm(D_coll)
    for ename, (Rm, tm, h, face) in ELEMENTS.items():
        w = beam_w(D_coll, h * 1e3)
        for aname, a in ABS.items():
            if a is None:
                bulk = 20e-6 * tm * 100          # 20 ppm/cm
                surf = 2 * 30e-6 if "AR" in aname else 2 * 5e-6
                a_tot, where = bulk + surf, "bulk"
            else:
                a_tot, where = a, face
            Pabs = a_tot * P
            r, opd, Tc, Trim, Tmax = solve_disc(Rm, tm, w, Pabs, where=where)
            D_eff, rms = fit_defocus(r, opd, w)
            D0 = FS["chi"] * Pabs / (math.pi * FS["k"] * w ** 2)
            dz_eff = focus_shift(h, D_eff) * 1e3
            dz0 = focus_shift(h, D0) * 1e3
            # insulated-rim variant (all heat out through the faces): same curvature, hotter disc
            _, opd_i, Tc_i, _, _ = solve_disc(Rm, tm, w, Pabs, where=where, rim="insulated")
            D_i, _ = fit_defocus(r, opd_i, w)
            res["cases"].append(dict(D_coll_mm=D_coll, element=ename, absorption=aname, a_tot=a_tot, P_abs_W=Pabs, w_mm=w * 1e3,
                                     T_centre_K=Tc, T_rim_K=Trim, T_max_K=Tmax, T_centre_insulated_K=Tc_i,
                                     D_eff_per_m=D_eff, D_central_per_m=D0, D_eff_insulated=D_i, wavefront_rms_resid_nm=rms * 1e9,
                                     dz_mm=dz_eff, dz_central_mm=dz0, x_zR=dz_eff / zR, zR_mm=zR))
    # the f-theta itself: total absorption of all elements, equivalent single plate in the collimated beam at H' (h = f)
    for mat_name, mat in (("fused silica", FS), ("N-BK7-type glass", BK7)):
        for a_tot in (2e-4, 5e-4, 1e-3, 3e-3):
            w = D_coll / 2 * 1e-3
            Pabs = a_tot * P
            r, opd, Tc, Trim, Tmax = solve_disc(37.5e-3, 20e-3, w, Pabs, where="bulk", mat=mat)
            D_eff, rms = fit_defocus(r, opd, w)
            dz = 0.160 ** 2 * D_eff / (1 + 0.160 * D_eff) * 1e3
            res["lens"].append(dict(D_coll_mm=D_coll, material=mat_name, a_tot=a_tot, P_abs_W=Pabs, T_centre_K=Tc, D_eff_per_m=D_eff,
                                    dz_mm=dz, x_zR=dz / zR, zR_mm=zR))

# reproduce mech.md E's 500 W / 0.5 % row with its own formula, and with this one at the model's real slide height
w_mech = 3.2e-3 / 2 * (0.145 / 0.1825)
D_mech = 2.5 * 9.6e-6 / (2 * math.pi * 1.38 * w_mech ** 2)
res["check"] = dict(mech_md_formula_dz_mm=0.160 ** 2 * D_mech * 1e3,
                    note="mech.md: w = 1.27 mm, D = P dn/dT/(2 pi k w^2), dz = f^2 D: 43.8 mm. Here: the slide is at z 126 "
                         "(not 145), the central-curvature power is 2x, and dz = h^2 D/(1 + h D) for an element h above focus.")

# time constants (fused silica): local (beam radius) and whole disc
kappa = FS["k"] / (FS["rho"] * FS["c"])
res["time_constants_s"] = dict(local_w2mm=(2e-3) ** 2 / (4 * kappa), disc_R23mm=(23e-3) ** 2 / (5.78 * kappa))

(OUT / "thermal_lens.json").write_text(json.dumps(res, indent=1))

L = ["# Thermal lensing at 500 W (`analysis/optics/thermal_lens.py`)", "",
     f"Fused silica: k {FS['k']} W/m·K, dn/dT {FS['dndT']:.2e} /K, χ = dn/dT + (n−1)(1+ν)α = {FS['chi']:.3e} /K. "
     f"N-BK7-type glass χ = {BK7['chi']:.2e} /K, k {BK7['k']}. Static beam (worst case: a small coupon near the field centre). "
     "Focus moves toward the lens by Δz = h²D/(1 + hD).", "",
     "| Collimator D | Element | Absorption | P_abs (W) | Beam w (mm) | ΔT centre, rim fixed / insulated rim (K) | D_eff (1/m) | Central-curvature D0 (1/m) | Focus shift (mm) | × z_R |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for c in res["cases"]:
    L.append(f"| {c['D_coll_mm']} mm | {c['element']} | {c['absorption']} | {c['P_abs_W']:.3g} | {c['w_mm']:.2f} | {c['T_centre_K']:.2g} / {c['T_centre_insulated_K']:.2g} | "
             f"{c['D_eff_per_m']:.3g} | {c['D_central_per_m']:.3g} | **{c['dz_mm']:.2g}** | {c['x_zR']:.2g} |")
L += ["", "f-theta lens heated by its own absorption (all elements lumped, beam at its collimated size, at H' 160 mm above focus):", "",
      "| Collimator D | Material | Total absorption | P_abs (W) | D_eff (1/m) | Focus shift (mm) | × z_R |", "|---|---|---|---|---|---|---|"]
for c in res["lens"]:
    L.append(f"| {c['D_coll_mm']} mm | {c['material']} | {100*c['a_tot']:.2f} % | {c['P_abs_W']:.2g} | {c['D_eff_per_m']:.3g} | **{c['dz_mm']:.2g}** | {c['x_zR']:.2g} |")
L += ["", f"Check against mech.md E (500 W, 0.5 %): its formula gives {res['check']['mech_md_formula_dz_mm']:.1f} mm. {res['check']['note']}", "",
      f"Time constants: local (w = 2 mm) {res['time_constants_s']['local_w2mm']:.1f} s; whole slide {res['time_constants_s']['disc_R23mm']:.0f} s."]
(OUT / "thermal_lens.md").write_text("\n".join(L) + "\n")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
    aa = np.logspace(-5, -1.5, 30)
    for D_coll, col in ((5.0, "#2a78d6"), (3.2, "#eb6834")):
        w = beam_w(D_coll, 126.0)
        dz = []
        for a in aa:
            r, opd, *_ = solve_disc(23e-3, 3e-3, w, a * P, where="bottom", nr=100, nz=12)
            De, _ = fit_defocus(r, opd, w)
            dz.append(focus_shift(0.126, De) * 1e3)
        ax.loglog(aa * 100, dz, color=col, lw=2, label=f"cover slide, D = {D_coll} mm beam")
        ax.annotate(f"D {D_coll} mm", (aa[-1] * 100, dz[-1]), xytext=(-40, 4), textcoords="offset points", fontsize=7, color="#52514e")
        z_r = zr_mm(D_coll)
        ax.axhline(z_r, color=col, ls=":", lw=1)
        ax.text(1.2e-3, z_r * 1.08, f"z_R {z_r:.1f} mm (D {D_coll} mm)", fontsize=7, color="#52514e")
        ax.axhline(z_r * math.sqrt(1.1 ** 2 - 1), color=col, ls="--", lw=0.8)
    ax.set_xlabel("absorption in the fouled face (%)")
    ax.set_ylabel("focus shift toward the lens at 500 W (mm)")
    ax.grid(alpha=0.25, which="both", lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=7, frameon=False)
    ax.set_title("Cover-slide thermal lens (static beam); dashed: ±10 % spot growth", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "thermal_lens.png")
except Exception as e:
    print("figure skipped:", e)

print((OUT / "thermal_lens.md").read_text())
