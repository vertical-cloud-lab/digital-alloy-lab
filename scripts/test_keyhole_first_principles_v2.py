"""Checks of the first-principles keyhole model's version 2 against exact or published results (PR #249).

    python scripts/test_keyhole_first_principles_v2.py
"""

from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import keyhole_first_principles as fp  # noqa: E402
import keyhole_first_principles_v2 as v2  # noqa: E402
import keyhole_fp_powder as pw  # noqa: E402
import keyhole_fp_shaped as sh  # noqa: E402


def test_shaped_tracer_reproduces_cone_tracer():
    """The general ray tracer, given a straight cone, absorbs what version 1's cone tracer does, and conserves
    the beam's energy."""
    m = fp.alloy_material("blend")
    N = fp.optical_index(m, m.T_boil())
    for a0, d in [(1.0, 0.5), (1.0, 5.0), (0.8, 4.0)]:
        a, sf, _, h = fp.trace_keyhole(a0, d, N, n_rays=40000, seed=3)
        z = np.linspace(0, d, 41)
        Qd, Qr, surf, out, hits = sh.trace_shaped(z, np.zeros_like(z), a0 * (1 - z / d), N.real, N.imag, 40000, 5, 4,
                                                  400, 1e-7)
        assert abs(Qd.sum() + Qr.sum() - a) < 0.01, (a0, d, Qd.sum() + Qr.sum(), a)
        assert abs(Qd.sum() + Qr.sum() + surf + out - 1.0) < 1e-9
        assert abs(hits - h) < 0.1


def test_janaf_vapour_pressure_is_one_bar_at_the_boiling_point():
    for el, j in v2.JANAF.items():
        assert abs(float(v2.p_pure(el, j["T_b"])) / 1e5 - 1.0) < 1e-9, el
    # Mg is far more volatile than Al at the keyhole wall
    assert float(v2.p_pure("Mg", 2800.0)) > 100 * float(v2.p_pure("Al", 2800.0))


def test_mg_depletion_limits():
    """With no Mg in the vapour the wall is Al-controlled; Mg can only lower the wall temperature, and the wall
    keeps less Mg than the bulk."""
    for key in ("alsi10mg", "al5182"):
        r0, a0, v = 40e-6, 40e-6, 0.8
        out = {}
        for use_mg in (False, True):
            al = v2.make_alloy(key, use_mg=use_mg)
            ws = al.vap.wall(a0, 0.5 * a0, math.pi * a0 * math.sqrt(a0 ** 2 + (3 * a0) ** 2), v,
                             lambda T, Mv: v2.vapour_outflow(a0, al.m.sigma, T, Mv))
            out[use_mg] = ws
        assert out[True]["T_w"] <= out[False]["T_w"] + 1e-6
        assert 0.0 < out[True]["x_mg_surface"] < out[True]["x_mg_bulk"]


def test_powder_limits():
    """Black particles on a black substrate absorb everything; a layer far thinner than one particle absorbs like
    its substrate; a thick layer of perfect mirrors absorbs nothing."""
    beta = pw.extinction(0.5, 1.0)
    a, _, _ = pw.powder_mc(1.3, 10.0, 1.3, 10.0, 1.0, 1.0, 2.0, beta, 20000, 1)
    assert abs(a - 1.0) < 1e-9
    a, _, sub = pw.powder_mc(1.3, 10.0, 1.3, 10.0, 0.0, 0.3, 1e-4, beta, 20000, 1)
    assert abs(a - 0.3) < 0.02 and abs(sub - a) < 1e-12
    a, _, _ = pw.powder_mc(1.3, 10.0, 1.3, 10.0, 0.0, 0.0, 20.0, beta, 20000, 1)
    assert a < 1e-12


def test_cone_roots_reproduce_version_1():
    """With version 1's material and a single stable root, the root scan lands on version 1's depth."""
    key = "blend"
    a = fp.ALLOYS[key]
    m = fp.alloy_material(key)
    tab = fp.ray_table(m)
    r0, a0, T0 = a["r0"], a["r0"], a["T0"]
    T_w = fp.wall_temperature(m, a0)
    th = fp.thermal_state(m, T0, T_w)
    Q_e = fp.evaporation_power(m, a0, T_w)
    f = v2.cone_balance(375.0, 0.4, r0, a0, th, Q_e, tab, a["A_am"])
    roots = v2.cone_roots(f, a0, r0, n=120)
    r1 = fp.solve_point(m, 375.0, 0.4, r0, T0, tab, A_override=a["A_am"], want_pool=False)
    assert abs(roots["shallow"] * 1e6 - r1.d_um) < 0.02 * r1.d_um, (roots, r1.d_um)


def test_kaplan_tilt_leans_back_and_steepens_with_power():
    """The front wall leans back (tip behind the opening's centre) and stands steeper at higher intensity."""
    m = fp.alloy_material("alsi10mg")
    N = fp.optical_index(m, m.T_boil())
    th = fp.thermal_state(m, 423.15, fp.wall_temperature(m, 40e-6))
    t_lo = sh.kaplan_tip(250.0, 40e-6, 40e-6, 150e-6, 0.0, N, th, 0.9)
    t_hi = sh.kaplan_tip(400.0, 40e-6, 40e-6, 150e-6, 0.0, N, th, 0.9)
    ang = lambda t: math.degrees(math.atan2(40e-6 - t, 150e-6))  # noqa: E731
    assert t_lo < 40e-6 and ang(t_hi) < ang(t_lo)


if __name__ == "__main__":
    n = 0
    for name, f in list(globals().items()):
        if name.startswith("test_") and callable(f):
            f()
            n += 1
            print("PASS", name)
    print(n, "passed")
