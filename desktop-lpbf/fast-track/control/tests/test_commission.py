"""Commissioning routines on the simulated machine."""
import random

from ftctl import commission


def ready(rig):
    r = rig()
    r.sup.connect()
    r.sup.startup()
    return r


def test_focus_ladder_first_light(rig):
    r = ready(rig)
    e0 = r.w.energy_in_plate_J
    out = commission.focus_ladder(r.sup)
    assert [o["dz_mm"] for o in out] == [-1.0, -0.5, 0.0, 0.5, 1.0]
    assert all(o["P_W"] == 50.0 for o in out)
    assert all(abs(o["energy_J"] - 50.0 * 5.0 / 500.0) < 0.05 for o in out)    # 50 W x 10 ms per 5 mm line
    assert r.w.energy_in_plate_J > e0
    assert abs(r.m.piston.position() - r.cfg.motion.piston_build_start_mm) < 1e-6


def test_hot_piston_stall_margin(rig):
    r = ready(rig)
    res = commission.hot_piston_test(r.sup)
    assert res["strokes"] == 10 and res["spread_stroke_s"] < 0.1
    # load 23 N against 100 N: moves at 25 % current, stalls at 20 %
    assert res["lowest_current_that_moved"] == 0.25
    assert res["drag_upper_bound_N"] == 25.0 and res["margin"] == 4.0
    assert r.m.piston.run_current == 1.0


def test_dose_spread_cv(rig):
    r = ready(rig)
    rng = random.Random(3)
    res = commission.dose_spread_test(r.sup, lambda k: rng.gauss(0.095, 0.095 * 0.08))
    assert res["cycles"] == 20 and res["passed"] and res["cv"] < 0.15


def test_chain_proof_each_device_alone(rig):
    r = ready(rig)
    w = r.w
    attr = {"estop": "estop_ok", "key": "key_on", "lid": "lid_closed", "beam_tube": "tube_closed"}
    out = commission.chain_proof_test(r.sup, operate=lambda dev, opened: setattr(w, attr[dev], not opened))
    assert [o["opened_chain"] for o in out] == [True] * 4
    assert w.g9se
