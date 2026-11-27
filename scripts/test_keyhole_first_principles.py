"""Checks of the first-principles keyhole model's pieces against exact or published results (PR #249).

    python scripts/test_keyhole_first_principles.py      (or: pytest scripts/test_keyhole_first_principles.py)
"""
import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import keyhole_first_principles as fp  # noqa: E402


def test_drude_matches_laserbeamfoam_flat_absorptance():
    # laserbeamFoam's flat-surface Drude-Fresnel values for liquid Al: 0.141 (40 uOhm cm) and 0.196 (65 uOhm cm).
    ne = 3 * 2375 * fp.N_A / 0.02698
    a40 = float(fp.fresnel_absorptance(fp.drude_index(40e-8, ne), 1.0))
    a65 = float(fp.fresnel_absorptance(fp.drude_index(65e-8, ne), 1.0))
    assert abs(a40 - 0.141) < 0.01 and abs(a65 - 0.196) < 0.01, (a40, a65)


def test_drude_fit_reproduces_krishnan():
    k = fp.KRISHNAN_AL
    wp2, g = fp.drude_from_nk(k["n"], k["k"], k["lam"])
    N = fp.drude_index_params(wp2, g, k["lam"])
    assert abs(N.real - 0.91) < 1e-6 and abs(N.imag - 6.33) < 1e-6, N


def test_fresnel_limits():
    N = complex(3.0, 8.0)
    a0 = float(fp.fresnel_absorptance(N, 1.0))
    assert abs(a0 - 4 * 3.0 / ((3.0 + 1) ** 2 + 8.0 ** 2)) < 1e-12
    assert float(fp.fresnel_absorptance(N, 0.0)) < 1e-9  # grazing incidence reflects everything


def test_gaussian_source_far_field_is_rosenthal():
    k, kappa, v, Q, r0 = 100.0, 4e-5, 0.5, 50.0, 40e-6
    x, y, z = -600e-6, 150e-6, 100e-6
    R = math.sqrt(x * x + y * y + z * z)
    ros = Q / (2 * math.pi * k * R) * math.exp(-v * (R + x) / (2 * kappa))
    g = float(fp.gaussian_field(np.array([x]), y, z, Q, r0, k, kappa, v)[0])
    assert abs(g / ros - 1) < 0.02, (g, ros)


def test_flat_keyhole_absorbs_like_a_flat_surface():
    N = fp.drude_index(55e-8, 3 * 2300 * fp.N_A / 0.02698)
    a, sf, _, _ = fp.trace_keyhole(1.0, 1e-3, N, n_rays=20000)
    assert abs((a + sf) - float(fp.fresnel_absorptance(N, 1.0))) < 0.01


def test_deep_cone_traps_light():
    N = fp.drude_index(55e-8, 3 * 2300 * fp.N_A / 0.02698)
    shallow = sum(fp.trace_keyhole(1.0, 1.0, N, n_rays=20000)[:2])
    deep = sum(fp.trace_keyhole(1.0, 20.0, N, n_rays=20000)[:2])
    assert 0.25 < shallow < deep < 1.0, (shallow, deep)


def test_lankalapalli_worked_example():
    # Lankalapalli et al. 1996, Sec. 2.5: mild steel, k 0.6 W/cm/C, alpha 0.05 cm^2/s, 4500 W, 2 cm/s,
    # a = 0.0635 cm (Pe0 = 1.27), T_V 2730 C -> conical depth 0.465 cm.
    d = fp.lankalapalli_depth(4500.0, 0.02, 0.000635, 60.0, 5e-6, 2730.0 - 25.0)
    assert abs(d / 0.00465 - 1) < 0.01, d


def test_collocation_close_to_lankalapalli_for_a_deep_cone():
    # Our 3D collocation (axis point sources, adiabatic top) against Lankalapalli's 2D slices for a deep cone.
    # It comes out 34 % higher: the axis sources hold only the mean wall temperature, like Kaplan's line source
    # (12 % above the exact 2D cylinder at Pe = 1.27), and the tip also conducts downwards in 3D.
    th = fp.Thermal(k=60.0, kappa=5e-6, rho_c=60.0 / 5e-6, theta_w=2705.0, theta_l=1000.0, theta_s=900.0, T_w=2730.0)
    a0, d, v = 0.000635, 0.00465, 0.02
    zs, q = fp.keyhole_conduction(a0, d, th, v, (np.zeros(0), np.zeros(0), np.zeros(0)))
    P_lank = 4500.0
    assert 1.0 < q.sum() / P_lank < 1.45, q.sum()


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except AssertionError as e:
                fails += 1
                print("FAIL", name, e)
    sys.exit(1 if fails else 0)
