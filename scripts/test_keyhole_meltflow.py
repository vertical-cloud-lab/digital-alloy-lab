"""Checks of scripts/keyhole_meltflow.py, our 3D steady-state melt-flow solver (PR #249).

1. Flow off, conduction mode, constant properties: the pool matches the exact moving Gaussian source
   (keyhole_first_principles.gaussian_field + pool_dimensions) to within 5 %.
2. Flow off, keyhole mode, a straight cone at T_w: the heat the wall delivers is within 15 % of the collocation
   in keyhole_first_principles.keyhole_conduction (sum of q), and the pool depth within 10 %.
3. The global energy balance closes to within 2 % (flow off and on).
4. Marangoni flow on, dsigma/dT < 0: the surface flows outward from the hot spot, and the peak surface speed is of
   the order of the boundary-layer scaling (|dsigma/dT| dT)^(2/3) / (rho mu L)^(1/3).
5. Grid check on the AlSi10Mg render point with flow on: pool sizes change by less than 10 % between h = r0/6 and
   h = r0/8.

Run from the repo root: python scripts/test_keyhole_meltflow.py   (about 4 minutes on 2 cores)
"""

from __future__ import annotations

import os

os.environ.setdefault("NUMBA_NUM_THREADS", "2")

import math  # noqa: E402
import pathlib  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import keyhole_first_principles as kfp  # noqa: E402
import keyhole_meltflow as mf  # noqa: E402

RESULTS = {}


def _field_bc(fun, T0):
    """Dirichlet far field from an analytic field fun(x, y, z) -> theta, evaluated in chunks."""
    def Tbc(x, y, z):
        sh = np.broadcast(x, y, z).shape
        X, Y, Z = (np.broadcast_to(a, sh).ravel() for a in (x, y, z))
        out = np.empty(X.size)
        for s in range(0, X.size, 4000):
            out[s:s + 4000] = fun(X[s:s + 4000], Y[s:s + 4000], Z[s:s + 4000])
        return T0 + out.reshape(sh)
    return Tbc


RHO, CP, K = 2600.0, 1000.0, 100.0
KAPPA = K / (RHO * CP)
T0 = 400.0


def test_flow_off_conduction_matches_analytic():
    P, A, r0, v = 250.0, 0.3, 40e-6, 0.9
    Q = A * P
    pr = mf.props_constant(RHO, CP, K, T_s=900.0, T_l=950.0)
    fun = lambda x, y, z: kfp.gaussian_field(x, y, z, Q, r0, K, KAPPA, v)  # noqa: E731
    g = mf.grid_for(r0, pool_D=120e-6, pool_W=250e-6, pool_L_rear=500e-6, far=0.8e-3)
    case = mf.Case(label="t1", props=pr, P=P, v=v, r0=r0, T0=T0, A=A, grid=g, Tbc=_field_bc(fun, T0))
    out, T, st, kh = mf.solve_case(case, flow=False)
    worst = 0.0
    for tag, Tiso in (("liquidus", 950.0), ("solidus", 900.0)):
        D, W, L, _ = kfp.pool_dimensions(fun, Tiso - T0, r0)
        for name, ref in (("depth", D), ("width", W), ("length", L)):
            got = out[f"pool_{name}_{tag}_um"] * 1e-6
            worst = max(worst, abs(got / ref - 1))
    RESULTS["1_conduction_worst_rel_err"] = worst
    RESULTS["3_energy_balance_flow_off_conduction"] = out["energy_balance_rel_err"]
    assert worst < 0.05, worst
    assert abs(out["energy_balance_rel_err"]) < 0.02


def test_flow_off_keyhole_heat_matches_collocation():
    r0, v = 40e-6, 0.9
    a0, d, T_w = 40e-6, 150e-6, 2800.0
    pr = mf.props_constant(RHO, CP, K, T_s=900.0, T_l=950.0)
    th = kfp.Thermal(k=K, kappa=KAPPA, rho_c=RHO * CP, theta_w=T_w - T0, theta_l=950 - T0, theta_s=900 - T0, T_w=T_w)
    empty = (np.zeros(0), np.zeros(0), np.zeros(0))
    zs, q = kfp.keyhole_conduction(a0, d, th, v, empty)
    fun = lambda x, y, z: kfp.point_source_field(x, y, z, zs, q, K, KAPPA, v)  # noqa: E731
    g = mf.grid_for(r0, pool_D=250e-6, pool_W=300e-6, pool_L_rear=500e-6, keyhole_d=d, far=0.8e-3)
    case = mf.Case(label="t2", props=pr, P=0.0, v=v, r0=r0, T0=T0, A=0.0, grid=g, Tbc=_field_bc(fun, T0),
                   keyhole=mf.cone_keyhole(a0, d, T_w))
    out, T, st, kh = mf.solve_case(case, flow=False)
    ratio = out["Q_keyhole_W"] / float(q.sum())
    D, W, L, _ = kfp.pool_dimensions(fun, 950.0 - T0, r0)
    RESULTS["2_keyhole_heat_cfd_over_collocation"] = ratio
    RESULTS["2_pool_depth_cfd_over_analytic"] = out["pool_depth_liquidus_um"] * 1e-6 / D
    RESULTS["3_energy_balance_flow_off_keyhole"] = out["energy_balance_rel_err"]
    assert abs(ratio - 1) < 0.15, ratio
    assert abs(out["pool_depth_liquidus_um"] * 1e-6 / D - 1) < 0.10
    assert abs(out["energy_balance_rel_err"]) < 0.02


def test_marangoni_outward_and_scaling():
    P, A, r0, v = 200.0, 0.3, 40e-6, 0.5
    Q = A * P
    mu0 = 1.0e-3
    pr = mf.props_constant(RHO, CP, K, T_s=900.0, T_l=950.0, mu0=mu0, E_mu=0.0, dsigma_dT=-1.27e-4)
    fun = lambda x, y, z: kfp.gaussian_field(x, y, z, Q, r0, K, KAPPA, v)  # noqa: E731
    g = mf.grid_for(r0, pool_D=150e-6, pool_W=300e-6, pool_L_rear=600e-6, far=0.8e-3)
    case = mf.Case(label="t4", props=pr, P=P, v=v, r0=r0, T0=T0, A=A, grid=g, Tbc=_field_bc(fun, T0))
    out, T, st, kh = mf.solve_case(case, flow=True)
    Ts = T[:, :, 0]
    ih, jh = np.unravel_index(int(np.argmax(Ts)), Ts.shape)
    X, Y = np.meshgrid(g.xc, g.yc, indexing="ij")
    dx, dy = X - g.xc[ih], Y - g.yc[jh]
    r = np.sqrt(dx ** 2 + dy ** 2)
    ur, uy = st.u[:, :, 0] + v, st.v[:, :, 0]
    liquid = (Ts > pr.T_l) & (r > 0.5 * r0)
    radial = (ur * dx + uy * dy) / np.maximum(r, 1e-12)
    frac_out = float((radial[liquid] > 0).mean())
    lateral_out = float((uy[liquid & (Y > 5e-6)] > 0).mean())
    half_width = out["pool_width_liquidus_um"] * 1e-6 / 2
    dT = out["T_peak_K"] - pr.T_l
    scale = (abs(pr.dsigma_dT) * dT) ** (2 / 3) / (RHO * mu0 * half_width) ** (1 / 3)
    ratio = out["u_surface_max_rel_m_s"] / scale
    RESULTS["4_surface_points_flowing_outward"] = frac_out
    RESULTS["4_lateral_velocity_outward_fraction"] = lateral_out
    RESULTS["4_peak_surface_speed_m_s"] = out["u_surface_max_rel_m_s"]
    RESULTS["4_scaling_speed_m_s"] = scale
    RESULTS["3_energy_balance_flow_on"] = out["energy_balance_rel_err"]
    RESULTS["4_pool_width_flow_on_over_analytic"] = out["pool_width_liquidus_um"] * 1e-6 / kfp.pool_dimensions(
        fun, 950.0 - T0, r0)[1]
    assert frac_out > 0.9, frac_out
    assert lateral_out > 0.9, lateral_out
    assert 0.2 < ratio < 5.0, ratio
    assert abs(out["energy_balance_rel_err"]) < 0.02


def test_grid_check_alsi10mg_render():
    dims = {}
    for frac in (6.0, 8.0):
        case = mf.build_cases(h_fine_frac=frac)[0]
        out, T, st, kh = mf.solve_case(case, flow=True)
        dims[frac] = np.array([out["pool_depth_liquidus_um"], out["pool_width_liquidus_um"],
                               out["pool_length_liquidus_um"]])
        RESULTS[f"5_alsi10mg_flow_on_h_r0_over_{int(frac)}_DWL_um"] = [round(float(q), 1) for q in dims[frac]]
    rel = np.abs(dims[6.0] / dims[8.0] - 1)
    RESULTS["5_max_rel_change"] = float(rel.max())
    assert rel.max() < 0.10, rel


if __name__ == "__main__":
    t0 = time.time()
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t = time.time()
            try:
                fn()
                print(f"PASS {name} ({time.time() - t:.0f} s)", flush=True)
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name}: {e}", flush=True)
    for k, v in RESULTS.items():
        print(f"  {k}: {v if not isinstance(v, float) else round(v, 4)}")
    print(f"{'all passed' if not failed else f'{failed} failed'} in {time.time() - t0:.0f} s")
    sys.exit(1 if failed else 0)
