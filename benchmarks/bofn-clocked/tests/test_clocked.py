"""Checks for the clocked benchmark: the truth port, the calendars and capacity, money, the claim rule, the GP.

    cd benchmarks/bofn-clocked && python -m pytest -q tests
"""
import math
import os
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from lab import Lab, Station, ATOMIZER_SLOTS  # noqa: E402
from model import GP  # noqa: E402
from truth import Truth  # noqa: E402


def test_truth_matches_bofn_prelim():
    """The numpy port equals bofn-prelim's torch AlloyTruth (needs torch and botorch, as bofn-prelim does)."""
    torch = pytest.importorskip("torch")
    pytest.importorskip("botorch")
    sys.path.insert(0, str(HERE.parent / "bofn-prelim"))
    bofn_alloy = pytest.importorskip("bofn_alloy")
    X = np.random.default_rng(1).random((2000, 7))
    for k in (0.0, 0.5, 1.0):
        ours = Truth(k).design(X[:, :4], X[:, 4], X[:, 5], X[:, 6])[0]
        theirs = bofn_alloy.AlloyTruth(k).objective(torch.tensor(X)).numpy()
        assert np.abs(ours - theirs).max() < 1e-12


def test_atomizer_slots_give_16_runs_a_week():
    st = Station("atomizer", 1, "slots", slots=ATOMIZER_SLOTS)
    t, n = 0.0, 0
    while True:
        q = st.quote(t, 2.5, t)
        if q[0] >= 7.0:
            break
        st.commit(q, 2.5)
        t, n = q[1], n + 1
    assert n == 16


def test_partner_printer_lead_and_weekly_cap():
    st = Station("printer_pt", 1, "day", lead=7.0, per_period=(3, 7.0), turnaround=2.0)
    starts = []
    for _ in range(6):
        q = st.quote(0.0, 8.0, 0.0)
        st.commit(q, 8.0)
        starts.append(q[0])
    assert min(starts) >= 7.0  # booking lead
    weeks = [math.floor(s / 7) for s in starts]
    assert max(weeks.count(w) for w in set(weeks)) <= 3


def _lab(fac="vertical", budget=1e6):
    T = Truth(1.0)
    lab = Lab(T, fac, 0, budget, 365.0, {"T1": 0.0, "T2": 9.0})
    return lab, T


def test_money_and_results_flow():
    lab, T = _lab()
    assert lab.submit(dict(kind="powder", c=np.array([0.6, 0.45, 0.8, 0.0]), a=0.45, route="us"), 0.0)
    assert lab.spent == 1500 + 10  # a run plus the auto CALPHAD call
    t, _, kind, lot = lab.events[0]
    assert kind == "lot" and 1.0 <= t <= 2.0  # Monday 08:00 run, 2.5 h, a day of QC
    lab.apply(t, kind, lot)
    if lab.lots[0]["t_ready"] is None:  # this seed's run failed; nothing to print
        return
    assert lab.submit(dict(kind="print", lot=0, pv=[(0.35, 0.1)] * 6, machine="ih"), t)
    assert lab.spent == 1510 + 500


def test_budget_is_enforced():
    lab, _ = _lab(budget=1000.0)
    assert not lab.submit(dict(kind="powder", c=np.array([0.5, 0.5, 0.5, 0.0]), a=0.5, route="us"), 0.0)
    assert lab.spent == 0


def test_claim_needs_three_bars_and_a_passed_immersion():
    lab, T = _lab()
    c = np.array([0.3, 0.2, 0.1, 0.0])
    lab.calphad(c, pay=False)
    lab.lots.append(dict(id=0, c=c, key=lab.key(c), route="us", a=0.4, q_true=0.9, q_meas=0.9, uses_left=1,
                         t_ready=0.0, failed=False, t_order=0.0, epoch=0))
    lab.builds.append(dict(id=0, lot=0, machine="ih", coupons=[0], failed=False, t_done=0.0, epoch=0))
    lab.coupons.append(dict(id=0, build=0, lot=0, c=c, key=lab.key(c), a=0.4, route="us", machine="ih", P=0.3, v=0.12,
                            rho_actual=0.95, rho_meas=0.95, bars=[0.5, 0.5], bars_left=1, bars_pending=0, imm=None,
                            imm_read={}, imm_final=None, amp=1.0, epoch=0))
    lab._update_claim(1.0)
    assert lab.claim is None  # two bars, no immersion
    lab.coupons[0]["bars"].append(0.5)
    lab.coupons[0]["imm_final"] = T.ln_rmax + 0.1
    lab._update_claim(2.0)
    assert lab.claim is None  # failed corrosion
    lab.coupons[0]["imm_final"] = T.ln_rmax - 0.1
    lab._update_claim(3.0)
    assert lab.claim == 0 and "T1" in lab.hit


def test_stop_frees_the_vial():
    lab, _ = _lab()
    lab.coupons.append(dict(id=0, imm=dict(state="running", start=0.0, unit=3, t_end=30.0), imm_read={1: 2.0}))
    lab.stations["vials"].free_at[3] = 30.0
    assert lab.submit(dict(kind="stop", coupon=0), 1.0)
    assert lab.stations["vials"].free_at[3] == 1.0


def test_gp_gradient_and_group_offsets():
    rng = np.random.default_rng(0)
    X = rng.random((80, 3))
    y = np.sin(3 * X[:, 0]) + X[:, 1]
    grp = (rng.random(80) < 0.5).astype(int)
    g = GP(X, y + 0.3 * grp, np.full(80, 1e-3), groups=grp)
    th = g.hyper + 0.1
    f0, g0 = g._nll(th, 3)
    num = np.array([(g._nll(th + 1e-6 * np.eye(len(th))[i], 3)[0] - f0) / 1e-6 for i in range(len(th))])
    assert np.max(np.abs(num - g0)) < 1e-3
    m, _ = g.predict(X, 0)
    assert np.sqrt(np.mean((m - y) ** 2)) < 0.05  # the own group's function, offsets removed
