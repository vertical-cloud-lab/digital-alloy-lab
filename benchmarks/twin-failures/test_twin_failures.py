"""Checks for the failure layer and the strategies (needs the twin: ``get_twin.sh``, then
``TWIN_DIR=/tmp/byu-vcl/vertical-lab python -m pytest -q test_twin_failures.py``)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, os.environ.get("TWIN_DIR", "/tmp/byu-vcl/vertical-lab"))
sys.path.insert(0, str(HERE))

import bench  # noqa: E402
import failures as F  # noqa: E402
import strategies as ST  # noqa: E402


def _twin(policy="heuristic", days=60, seed=0):
    from twin import bench2 as B2
    from twin import campaign as C
    from twin.opt import policies3 as P3
    specs = {k: C.Spec(k, B2.BUDGET[k], B2.WIP[k], seed, 1.0, stock="stocked") for k in B2.BUDGET}
    pols = {k: (ST.make(policy, k, seed) if policy in ST.FMODES else P3.make3(policy, k, seed, None)) for k in specs}
    return C.Twin(specs, pols, scenario="historical", facility="vertical_lab", seed=seed, horizon_days=days,
                  mode="async")


def test_learning_curve_fit():
    lc = F.fit_learning_curve()
    assert lc["n_transient"] == 6 and lc["n_used"] == 9
    assert 8.5 < lc["tau"] < 10.5 and lc["tau_lo"] < 4 and lc["tau_hi"] > 30
    R = F.REGIMES["lab"]
    assert 0.38 < F.transient_p(1, R) < 0.46           # the year's first run, after the ten logged
    assert abs(F.transient_p(200, R) - R["p_inf"]) < 1e-3
    assert F.transient_p(5, F.REGIMES["twin"]) == F.P_BASE_TWIN


def test_twin_regime_changes_no_outcome():
    """The 'twin' regime only labels causes: the year is the same as round 3's, run for run."""
    a = _twin()
    sa = a.run()
    b = _twin()
    F.install(b, "twin", seed=0, pre_w=None)
    sb = b.run()
    for k in ("flaime_al", "onr_cu"):
        assert sa[k]["curve"] == sb[k]["curve"]
        assert sa[k]["n_lots"] == sb[k]["n_lots"]
    st = b.fail_state
    assert st["fails"] == st["intrinsic"] + st["transient"]
    assert not st["damage"]


def test_ledger_is_released_with_the_lot():
    tw = _twin()
    F.install(tw, "lab", seed=0)
    tw.run()
    for k, camp in tw.campaigns.items():
        L = camp.atom_ledger
        assert L, k
        released = {e["event"] for e in L}
        n_runs = sum(len(camp._lot_truth[i]["runs"]) for i in released)
        assert n_runs == len(L)
        for e in L:
            assert e["ok"] == (e["cause"] is None)
            assert (e["diag"] is None) == e["ok"]
        # every lot in the policy's view is in the ledger once its results are back
        assert {i for i, Lt in camp.lots.items() if not Lt.get("gas")} <= {e["lot"] for e in L}


def test_diagnosis_accuracy():
    tw = _twin(days=120, seed=3)
    st = F.install(tw, "lab", seed=3, diag_acc=0.6)
    tw.run()
    fails = sum(s["fails"] for s in st["by_campaign"].values())
    mis = sum(s["misdiag"] for s in st["by_campaign"].values())
    assert fails >= 15
    assert 0.15 < mis / fails < 0.65                      # 0.4 expected


def test_no_powder_admitted_while_the_atomizer_is_repaired():
    tw = _twin(days=5)
    st = F.install(tw, "lab", seed=0)
    camp = tw.campaigns["flaime_al"]
    a = dict(kind="powder", design=dict(camp.policy.reference_seeds()[0]), runs=1)
    assert camp.gate_ok(a, 0.0)
    st["windows"].append((0.0, 24.0 * 10))
    camp.fac.res["atomizer"].down.append((0.0, 24.0 * 10))
    assert not camp.gate_ok(a, 0.0)


def _fake_view(events, lots):
    """A view with only what FailNet3._book reads: the ledger and the lots."""
    led = []
    for ev in events:
        for j, ok in enumerate(ev["ok"]):
            led.append(dict(t=0.0, design=ev["design"], lot=ev["lot"], event=ev["event"], run=j, proc={}, ok=ok,
                            diag=None if ok else ev.get("diag", "transient"),
                            cause=None if ok else ev.get("cause", "transient"), n_event=len(ev["ok"]),
                            f_event=sum(1 for x in ev["ok"] if not x), y_event=0.0, into=ev.get("into", False)))
    return dict(atom_ledger=led, lots=lots, now_h=0.0)


@pytest.mark.parametrize("fmode,hidden,dead,retry_q", [
    ("bad_value", 0, 0, 0), ("drop", 1, 0, 0), ("abandon", 0, 1, 0), ("viability_x", 0, 1, 0),
    ("retry", 1, 0, 1), ("viability_node", 1, 0, 0), ("viability_node_nodiag", 0, 1, 0), ("oracle", 0, 1, 0)])
def test_first_failed_attempt(fmode, hidden, dead, retry_q):
    p = ST.FailNet3("flaime_al", 0, fmode=fmode)
    p.started.add(7)
    # diagnosed transient, truly intrinsic: viability_node trusts the diagnosis, the oracle doesn't
    v = _fake_view([dict(event=1, lot=1, design=7, ok=[False, False], diag="transient", cause="intrinsic")],
                   {1: dict(design=7)})
    p._book(v)
    assert len(p.hidden) == hidden and len(p.dead) == dead and len(p.retry_q) == retry_q
    assert (7 in p.started) == (hidden == 0)
    assert len(p._view(v)["lots"]) == 1 - hidden


def test_retry_then_abandon():
    p = ST.FailNet3("onr_cu", 0, fmode="retry")
    v = _fake_view([dict(event=1, lot=1, design=7, ok=[False])], {1: dict(design=7)})
    p._book(v)
    assert p.hidden == {1} and len(p.retry_q) == 1
    p.retry_q = []
    v = _fake_view([dict(event=1, lot=1, design=7, ok=[False]), dict(event=2, lot=2, design=7, ok=[False, False])],
                   {1: dict(design=7), 2: dict(design=7)})
    p._book(v)
    assert p.dead == {2} and not p.retry_q
    # a lot that made some powder is never a failed attempt
    v = _fake_view([dict(event=3, lot=3, design=8, ok=[False, True])], {3: dict(design=8)})
    p._book(v)
    assert 3 not in p.dead and 3 not in p.hidden


def test_viability_weight_follows_ax():
    """P(f >= 0.8) of a GP on 0/1, off until three zeros (Ax's defaults)."""
    p = ST.FailNet3("flaime_al", 0, fmode="viability_x")
    assert p.THR == 0.8 and p.MIN_ZERO == 3
    X = np.random.default_rng(0).random((12, p.space.dim))
    y = np.array([1.0] * 9 + [0.0] * 3)
    p.viab.fit(X, y)
    p._viab_on = True
    m, sd = p.viab.predict(X)
    w = 1.0 - __import__("scipy").stats.norm.cdf((0.8 - m) / sd)
    assert w[:9].mean() > w[9:].mean()


def test_bench_experiments_are_seedwise():
    main = bench.EXPERIMENTS["main"]
    assert [c["seed"] for c in main[:6]] == [0] * 6
    assert len({bench.run_id(c) for c in main}) == len(main)


def test_retry_waits_until_admitted():
    p = ST.FailNet3("flaime_al", 0, fmode="retry")
    v = _fake_view([dict(event=5, lot=5, design=9, ok=[False, False])], {5: dict(design=9)})
    p._book(v)
    assert len(p.retry_q) == 1 and p.retry_q[0]["key"] == 5
    p.admitted(dict(kind="powder", _retry_key=99))
    assert len(p.retry_q) == 1                            # not this retry
    p.admitted(dict(kind="powder", _retry_key=5, _did=9))
    assert not p.retry_q and p.fcounts["retries_run"] == 1 and 9 in p.started
