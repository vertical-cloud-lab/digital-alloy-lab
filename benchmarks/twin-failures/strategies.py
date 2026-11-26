"""Failure-handling strategies for round 3's time-aware BOFN (``twin/opt/net3.py``, ``Net3``), in Ax's terms (DAL #274).

Every strategy is the same optimizer, on the same engine, capacity and money; only what it does with a failed atomizer
run changes. A *run* is one pour of the atomizer; an *attempt* is one powder action (a lot, or a top-up of one), made
of one or more runs. An attempt that made no powder is a failed attempt.

==================  ===========================================  ==============================  ==========================
strategy            the failed run's data                        the design afterwards           new designs weighted by
==================  ===========================================  ==============================  ==========================
``bad_value``       0 yield in the atomize node (round 3 as is)  Al: never again; Cu: topped up  P(yield > 3 %) (round 3)
                                                                 again and again (round 3 as is)
``drop``            none (Ax <= 1.2.3 ``FAILED``)                may come back, no memory        P(yield > 3 %), successes
``abandon``         none (Ax ``ABANDONED``)                      pending for good                P(yield > 3 %), successes
``retry``           none                                         one rerun at the same settings, P(yield > 3 %), successes
                                                                 then abandoned
``viability_x``     a 0/1 GP over the design per attempt; Ax     pending for good                P(f(x) >= 0.8) once 3
                    1.3's ``AddExecutionViability``                                              attempts failed
``viability_node``  a 0/1 GP over the atomize node's inputs      diagnosed transient: back, like P(f(x_node) >= 0.8) once
                    (composition, CALPHAD, settings) per run;    ``FAILED``; diagnosed           3 runs labelled 0
                    diagnosed-transient runs left out            intrinsic: abandoned
``viability_node_nodiag``  as above, every failure labelled 0    abandoned                       as above
``oracle``          as ``viability_node`` with the true cause    as ``viability_node``           as above
==================  ===========================================  ==============================  ==========================

The viability weight multiplies a new design's (and a copper blend's atomizing) acquisition value, the
outcome-constraint form BoTorch uses for Ax's ``execution_viable >= 0.8``. It also picks the atomizer settings: the
best of 64 by the yield node's mean + half a standard deviation, times the weight. Round 3's ``bad_value`` keeps its
own rule (P(yield > 3 %) for choosing which new designs to list, nothing on the final score).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.stats import norm

from twin.opt import net3 as N3
from twin.opt.gp import Node

FMODES = ("bad_value", "drop", "abandon", "retry", "viability_x", "viability_node", "viability_node_nodiag", "oracle")
VIAB = ("viability_x", "viability_node", "viability_node_nodiag", "oracle")


class FailNet3(N3.Net3):
    """Round 3's BOFN (time-aware EI per bottleneck-hour) with a failure-handling strategy."""
    THR = 0.8                 # Ax's feasibility_threshold
    MIN_ZERO = 3              # Ax's min_abandoned_trials

    def __init__(self, key, seed=0, crucible=None, fmode="bad_value"):
        super().__init__(key, seed, crucible)
        assert fmode in FMODES, fmode
        self.fmode = fmode
        self.viab = Node("gp", 4, max_n=400, seed=seed) if fmode in VIAB else None
        self._viab_n = -1
        self._viab_on = False
        self.hidden, self.dead = set(), set()          # lot ids: forgotten (FAILED) / no more powder (ABANDONED)
        self.fail_attempts = {}                        # design id -> failed attempts so far
        self.retry_q = []                              # retry: (design id, settings, runs, copper blend promote)
        self._seen_ev = set()
        self._set_cache = {}
        self.fcounts = dict(attempts=0, failed_attempts=0, hidden=0, dead=0, retries=0, viab_fits=0,
                            viab_active_at_h=None, topups_blocked=0)

    # ---------------------------------------------------------------------------------------------- the ledger
    def _events(self, v):
        ev = {}
        for e in v.get("atom_ledger", ()):
            g = ev.setdefault(e["event"], dict(event=e["event"], design=e["design"], lot=e["lot"], proc=e["proc"],
                                               n=e["n_event"], f=e["f_event"], y=e["y_event"], into=e["into"],
                                               runs=[]))
            g["runs"].append(e)
        return ev

    def _label(self, e):
        """The cause a strategy acts on for a failed run: the lab's diagnosis, the truth (oracle) or 'intrinsic'."""
        if self.fmode == "oracle":
            return e["cause"]
        if self.fmode == "viability_node":
            return e["diag"]
        return "intrinsic"

    def _book(self, v):
        """New attempts since the last call: hide (FAILED), kill (ABANDONED) or queue a retry, by strategy."""
        for eid, g in sorted(self._events(v).items()):
            if eid in self._seen_ev:
                continue
            self._seen_ev.add(eid)
            self.fcounts["attempts"] += 1
            if g["n"] - g["f"] > 0:
                continue
            did, lot = g["design"], g["lot"]
            self.fcounts["failed_attempts"] += 1
            k = self.fail_attempts[did] = self.fail_attempts.get(did, 0) + 1
            fm = self.fmode
            if fm == "bad_value":
                continue
            if fm in ("viability_node", "oracle"):
                transient = all(self._label(e) == "transient" for e in g["runs"] if not e["ok"])
                fm = "drop" if transient else "abandon"
            elif fm in ("viability_x", "viability_node_nodiag"):
                fm = "abandon"
            if fm == "retry":
                if k == 1:
                    self.fcounts["retries"] += 1
                    if not g["into"]:
                        self._forget(v, lot, did)
                        self.retry_q.append(dict(did=did, proc=g["proc"], runs=g["n"]))
                    continue                          # a failed top-up: one more top-up is allowed
                fm = "abandon"
            if fm == "drop":
                if not g["into"]:
                    self._forget(v, lot, did)
            elif fm == "abandon":
                self.dead.add(lot)
                self.fcounts["dead"] += 1

    def _forget(self, v, lot, did):
        self.hidden.add(lot)
        self.fcounts["hidden"] += 1
        self.started.discard(did)
        if getattr(self, "blend_state", {}).get(did) == "promoted":
            self.blend_state.pop(did, None)
        self._simc_clear(did)

    def _simc_clear(self, did):
        self._set_cache = {k: x for k, x in self._set_cache.items() if k[0] != did}

    def _view(self, v):
        """The view with forgotten lots taken out, so the rest of the policy treats their designs as never made."""
        if not self.hidden:
            return v
        w = dict(v)
        w["lots"] = {k: L for k, L in v["lots"].items() if k not in self.hidden}
        return w

    # ---------------------------------------------------------------------------------------------- the data
    def datasets(self, v):
        D = super().datasets(v)
        if self.fmode == "bad_value":
            return D
        X, Y = [], []
        for g in self._events(v).values():
            ok = g["n"] - g["f"]
            if ok <= 0 or g["y"] is None or self.sim_of(v, g["design"]) is None:
                continue
            dsg = dict(v["design_inputs"][g["design"]], **g["proc"])
            X.append(self.atom_x(v, g["design"], dsg))
            Y.append(float(g["y"]) * g["n"] / ok)       # in-cut yield per charge that made powder
        D["atomize"] = (X, [Y])
        return D

    def _viab_rows(self, v):
        X, y = [], []
        if self.fmode == "viability_x":
            for g in self._events(v).values():
                dsg = dict(v["design_inputs"][g["design"]], **g["proc"])
                X.append(self.space.encode(dsg))
                y.append(1.0 if g["n"] - g["f"] > 0 else 0.0)
        else:
            for e in v.get("atom_ledger", ()):
                if self.sim_of(v, e["design"]) is None:
                    continue
                if not e["ok"] and self._label(e) == "transient":
                    continue                              # FAILED: says nothing about the inputs
                dsg = dict(v["design_inputs"][e["design"]], **e["proc"])
                X.append(self.atom_x(v, e["design"], dsg))
                y.append(1.0 if e["ok"] else 0.0)
        return X, y

    def fit(self, v):
        super().fit(v)
        if self.viab is None:
            return
        X, y = self._viab_rows(v)
        if len(y) == self._viab_n:
            return
        self._viab_n = len(y)
        zeros = sum(1 for t in y if t == 0.0)
        self._viab_on = zeros >= self.MIN_ZERO
        if self._viab_on:
            self.viab.fit(np.array(X), np.array(y))
            self.fcounts["viab_fits"] += 1
            if self.fcounts["viab_active_at_h"] is None:
                self.fcounts["viab_active_at_h"] = round(float(v["now_h"]), 1)
            self._set_cache = {}

    def _w(self, v, did, dsg_list):
        """P(f >= 0.8) of the viability GP at each of a design's candidate settings (1 while inactive)."""
        if self.viab is None or not self._viab_on or not self.viab.ready():
            return np.ones(len(dsg_list))
        if self.fmode == "viability_x":
            X = np.array([self.space.encode(d) for d in dsg_list])
        else:
            if self.sim_of(v, did) is None:
                return np.ones(len(dsg_list))
            X = np.array([self.atom_x(v, did, d) for d in dsg_list])
        m, sd = self.viab.predict(X)
        return 1.0 - norm.cdf((self.THR - m) / np.maximum(sd, 1e-6))

    # ---------------------------------------------------------------------------------------------- settings
    def atomizer_settings(self, v, did, design):
        if self.fmode not in VIAB:
            return super().atomizer_settings(v, did, design)
        ck = (did, self._viab_n, self._fitted_at.get("atomize"))
        if ck in self._set_cache:
            return dict(self._set_cache[ck][0])
        trial = [dict(design)]
        for _ in range(63):
            d = dict(design)
            for var in self.space.process[:3]:
                d[var.name] = float(var.from_unit(self.gen.random()))
            trial.append(d)
        w = self._w(v, did, trial)
        if self.ready("atomize") and self.sim_of(v, did) is not None:
            X = np.array([self.atom_x(v, did, d) for d in trial])
            mu, sd = self.nodes["atomize"][0].predict(X)
            s = np.maximum(mu + 0.5 * sd, 1e-3) * w
        else:
            s = w
        j = int(np.argmax(s))
        self._set_cache[ck] = (dict(trial[j]), float(w[j]))
        return dict(trial[j])

    def _w_at(self, v, did):
        """The weight at the settings the policy would use for this design."""
        if self.fmode not in VIAB:
            return None
        dsg = self.atomizer_settings(v, did, dict(v["design_inputs"][did]))
        return float(self._w(v, did, [dsg])[0])

    def _p_powder(self, v, dids):
        p = super()._p_powder(v, dids)
        if self.fmode in VIAB:
            p = p * np.array([self._w_at(v, d) for d in dids])
        return p

    # ---------------------------------------------------------------------------------------------- decisions
    def propose(self, v, n):
        self._book(v)
        return super().propose(self._view(v), n)

    def _candidates(self, v, P):
        C = super()._candidates(v, P)
        if self.dead:                                     # no more powder for abandoned lots
            keep = []
            for c in C:
                a0 = c["acts"][0] if c.get("acts") else {}
                if a0.get("kind") == "powder" and a0.get("into") in self.dead:
                    self.fcounts["topups_blocked"] += 1
                    continue
                keep.append(c)
            C = keep
        if self.retry_q:
            R = []
            for r in self.retry_q:
                dsg = dict(v["design_inputs"][r["did"]], **r["proc"])
                a = self.powder_action(dsg, runs=r["runs"], v=v)
                a["_did"] = r["did"]
                if not self.al:
                    a["_promote"] = r["did"]
                R.append(dict(what="retry a failed powder at the same settings", acts=[a], always=True,
                              did=r["did"]))
            self.retry_q = []
            C = R + C
        return C

    def _cands_new(self, v, P, pi, best_kb):
        out = super()._cands_new(v, P, pi, best_kb)
        if self.fmode in VIAB:
            for c in out:
                if c.get("did") is not None:
                    c["w_fail"] = self._w_at(v, c["did"])
        return out

    def _cands_cu(self, v, P, pi, best):
        C = super()._cands_cu(v, P, pi, best)
        if self.fmode in VIAB:
            for c in C:
                a0 = c["acts"][0] if c.get("acts") else {}
                if a0.get("kind") == "powder" and not a0.get("into") and a0.get("_did") is not None:
                    c["w_fail"] = self._w_at(v, a0["_did"])
        return C

    def _score(self, C, best_kb):
        super()._score(C, best_kb)
        for c in C:
            w = c.get("w_fail")
            if w is not None and c.get("value") is not None:
                c["value"] = c["value"] * w


def make(fmode, key, seed, crucible=None):
    p = FailNet3(key, seed, crucible, fmode=fmode)
    p.name, p.acq, p.denom = f"bofn3_{fmode}", "ei", "time"
    return p
