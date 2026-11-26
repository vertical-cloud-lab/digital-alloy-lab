"""Atomizer failure regimes for the byu-vcl twin, the per-run ledger a policy reads, and the lab's diagnosis of
each failure's cause (DAL #274).

The twin (byu-vcl PR 394, round 3, pinned in ``get_twin.sh``) draws an atomizer run's failure in
``twin/physics.py``: ``p_fail = 0.06 + 0.55 / (1 + exp((superheat - 70) / 14)) + 0.15 / (1 + exp(-(pour - 340) / 25))``
(+ wear above 1300 degC for copper). The 0.06 is chance; the rest comes from the run's inputs: the superheat the
campaign set over the liquidus it *believes*, so a CALPHAD error makes a cold melt, and the pour pressure. The twin
records only ``failed``. ``install()`` adds what DAL #274 needs on top, without changing the twin's code:

* a **cause** for every failed run: ``transient`` (equipment, set-up, consumables: outside the inputs; Ax's
  ``FAILED``) or ``intrinsic`` (the inputs: Ax's ``ABANDONED`` and a viability label of 0);
* the lab's **diagnosis** of that cause, right with probability ``diag_acc`` (``diag``);
* a **regime** for how often each happens (``REGIMES``), calibrated where the lab has a record;
* **damage**: a transient failure can damage the atomizer and stop it for days (both campaigns share it), during
  which no new powder is planned;
* a **ledger** of every run, released to the policy only when the lot's results come back (``view()['atom_ledger']``).

The policies in ``strategies.py`` decide what to do with that ledger.
"""
from __future__ import annotations

import math

import numpy as np

P_BASE_TWIN = 0.06            # twin/physics.py: the atomizer's chance failure rate at good settings
PRE_W = None                  # optional: hours a powder action may queue for its charge before the atomizer gate
RETRY_W = 72.0                # hours a queued rerun may wait for the atomizer's next free slot (strategy 'retry')

# ------------------------------------------------------------------------------------------- the lab's own record
# DAL PR 286 (atomizer-runs/runs.csv at 8320f13): every logged run of the rePOWDER, Oct 2 to Nov 13 2026, read for
# its cause. 'transient' = set-up, consumable or equipment (outside the alloy and the settings); 'inputs' = the run's
# settings; None = made powder. No failure in the log is attributed to the alloy: the same 630 bronze made powder on
# Oct 27 and Nov 10 and failed on Oct 28, Nov 5 and Nov 13.
LAB_RECORD = [
    ("2026-10-02", "Al 4047 in a 6063 cup", "transient", "set-up: melt shot out too fast, plate too far away"),
    ("2026-10-06", "Al 6063", "transient", "set-up: stream on the upper sonotrode, vibration started late"),
    ("2026-10-08", "Al rods", "inputs", "settings: too little amplitude for a carbon-fibre plate; melt froze on the tip"),
    ("2026-10-21", "Al 4047", "transient", "set-up: plate in the wrong place until corrected mid-pour"),
    ("2026-10-22", "Al 4047", None, "made powder, below target"),
    ("2026-10-27", "C63000", None, "about 91 % of the charge as powder"),
    ("2026-10-28", "C63000", "transient", "consumable: plate on its second use never started atomizing"),
    ("2026-11-05", "C63000", "transient", "equipment: induction generator tripped mid-pour"),
    ("2026-11-10", "C63000", None, "about 75 % of the charge"),
    ("2026-11-13", "C63000", "transient", "consumable: plate on its second use; hot shot burned the cup's seals "
                                          "and cracked its glass (DAL #269): the atomizer was down for over a week"),
]


def fit_learning_curve(p_inf=0.10, record=LAB_RECORD):
    """Maximum-likelihood time constant (runs) of p(n) = p_inf + (1 - p_inf) exp(-(n - 1) / tau) for the transient
    failures in the record (runs that failed from their inputs are left out), with a 95 % profile-likelihood interval.
    p_inf is assumed: ten runs can't estimate an asymptote."""
    obs = [(n, 1 if c == "transient" else 0) for n, (_, _, c, _) in enumerate(record, start=1) if c != "inputs"]

    def nll(tau):
        s = 0.0
        for n, o in obs:
            p = min(max(p_inf + (1 - p_inf) * math.exp(-(n - 1) / tau), 1e-9), 1 - 1e-9)
            s -= o * math.log(p) + (1 - o) * math.log(1 - p)
        return s
    taus = np.linspace(1.0, 200.0, 3981)
    v = np.array([nll(t) for t in taus])
    i = int(np.argmin(v))
    ok = taus[v - v[i] <= 1.92]
    return dict(p_inf=p_inf, tau=float(taus[i]), tau_lo=float(ok.min()), tau_hi=float(ok.max()),
                n_logged=len(record), n_transient=sum(o for _, o in obs), n_used=len(obs))


LC = fit_learning_curve()     # tau 9.6 runs (95 % 3.0-40.3) at p_inf 0.10: about 0.42 per run at the year's start

REGIMES = {
    # round 3 as it is: the twin's own draws; a failure's cause is attributed by the share of its law (chance 0.06)
    "twin": dict(kind="twin"),
    # the lab's record: transient failures on the learning curve fitted above, from run 11 on (the year starts
    # after the ten logged runs; both campaigns' runs count, as the operators and the SOP are shared); the input-
    # caused part of the twin's law unchanged; one transient failure in six damages the atomizer (Nov 13: the plate
    # never atomized, the hot shot reached the collection cup; the cold melt of Oct 8 froze on the plate and damaged
    # nothing), down for a lognormal time with a median of 14 days (assumed: parts come from AMAZEMET)
    "lab": dict(kind="lab", p_inf=LC["p_inf"], tau=LC["tau"], n0=len(LAB_RECORD),
                damage=dict(p=1 / 6, median_d=14.0, sigma=0.5)),
    # 'lab', learning at the slow end of the fit's interval
    "lab_slow": dict(kind="lab", p_inf=LC["p_inf"], tau=LC["tau_hi"], n0=len(LAB_RECORD),
                     damage=dict(p=1 / 6, median_d=14.0, sigma=0.5)),
    # 'lab' plus a hidden region of compositions that won't atomize (assumed physics, no CALPHAD node sees it; see
    # region_p): the case where abandoning a composition is right
    "lab_region": dict(kind="lab", p_inf=LC["p_inf"], tau=LC["tau"], n0=len(LAB_RECORD),
                       damage=dict(p=1 / 6, median_d=14.0, sigma=0.5), region=True),
}

# A hidden "won't atomize" region (assumed, stated as a stress test, not a claim about these alloys):
# * aluminium: Mg and Li, strong oxide formers, build a dross skin that clogs the nozzle and keeps the melt from
#   wetting the plate;
# * copper: the refractory additions (Cr, Nb, Ti) that don't dissolve fully at the atomizer's temperature and plug
#   the nozzle. NAB (Al 9.2, Fe 4.0) is left out of it on purpose: it atomized on Oct 27 and Nov 10.
# The thresholds are set by calibrate_region() so the region holds about a third of the best designs the oracle finds.
REGION = {
    "flaime_al": dict(w={"Mg": 1 / 4.0, "Li": 1 / 1.0}, s0=0.30, width=0.08, p_max=0.9),
    "onr_cu": dict(w={"Cr": 1 / 0.7, "Nb": 1 / 0.8, "Ti": 1 / 0.5}, s0=0.45, width=0.06, p_max=0.9),
}


def region_score(key, comp):
    R = REGION[key]
    return sum(comp.get(e, 0.0) * w for e, w in R["w"].items())


def region_p(key, comp):
    R = REGION[key]
    s = region_score(key, comp)
    return R["p_max"] / (1.0 + math.exp(-(s - R["s0"]) / R["width"]))


def transient_p(n_total, R):
    """Chance of a transient failure on the year's n_total-th run (1-based), both campaigns counted."""
    if R["kind"] == "twin":
        return P_BASE_TWIN
    n = R["n0"] + n_total
    return R["p_inf"] + (1 - R["p_inf"]) * math.exp(-(n - 1) / R["tau"])


def _usable(true_superheat_K):
    """physics.atomize's usable fraction of a run that did not fail."""
    sh = max(true_superheat_K, -50.0)
    return 0.91 * (1 - 0.25 / (1 + math.exp((sh - 90) / 15)))


def install(tw, regime="lab", seed=0, diag_acc=0.8, pre_w=PRE_W):
    """Put a failure regime, causes, diagnosis, damage and the ledger on a constructed ``twin.campaign.Twin``.
    ``pre_w=None`` keeps round 3's admission rule exactly (``_wrap_gate``)."""
    R = REGIMES[regime]
    frng = np.random.default_rng([int(seed), 274, 1])        # failure and damage draws
    drng = np.random.default_rng([int(seed), 274, 2])        # diagnosis draws
    state = dict(regime=regime, diag_acc=diag_acc, n=0, fails=0, intrinsic=0, transient=0, damage=[], windows=[],
                 overlap_h=0.0, gate_refused=0, gate_refused_pre=0, by_campaign={})
    for key, camp in tw.campaigns.items():
        state["by_campaign"][key] = dict(runs=0, fails=0, intrinsic=0, transient=0, misdiag=0)
        _wrap_route(camp)
        _wrap_gate(camp, state, pre_w)
        _wrap_atomize(camp, R, state, frng, drng, diag_acc)
        _wrap_release(camp)
        _wrap_view(camp)
    tw.fail_state = state
    return state


def _wrap_route(camp):
    orig = camp._route

    def _route(steps, ready_h, what, changeover=False, tag=None, handles=None):
        out = orig(steps, ready_h, what, changeover=changeover, tag=tag, handles=handles)
        if any(st == "atomizer" for st, _ in steps):
            camp._fail_last_t = out[0]
        return out
    camp._route = _route


def _wrap_gate(camp, state, pre_w=PRE_W):
    """One addition to round 3's admission rule for a powder action (``Campaign.gate_ok``), the same for every policy.

    * **Repairs.** ``queue_wait`` measures the wait against an idle station that also waits out a breakdown, so a
      repair doesn't count as waiting, and powder actions would queue up behind a two-week repair. While the atomizer
      is down from damage (this layer's windows only; the twin's own 36-hour breakdowns are left as round 3 has
      them), no new powder action is admitted: the lab waits for the repair before it plans more runs.
    * ``pre_w`` (off by default): also refuse a powder action whose charge would wait more than ``pre_w`` hours for
      other work at the shop or the doser. Round 3 lets those steps queue without limit. A 40-day test seemed to need
      it (578 aluminium runs booked, out to day 970), but that was the spending plan, which scales with the horizon
      and frees the whole budget by day 30 of a 40-day run; in a year it paces the money.
    """
    orig = camp.gate_ok

    def gate_ok(a, now_h):
        if a.get("_retry_key") is not None:
            # a rerun of a failed powder (strategy 'retry') books the atomizer's next free slot up to RETRY_W hours
            # out, the way an operator reruns an alloy next; round 3's 2-hour rule evaluates each action at the hour
            # its own charge is ready, so new designs kept taking the slots a queued rerun needed
            camp.GATE_W = RETRY_W
            try:
                ok0 = orig(a, now_h)
            finally:
                del camp.GATE_W
        else:
            ok0 = orig(a, now_h)
        if not ok0:
            return False
        if a.get("kind") != "powder":
            return True
        pre, st, h = camp.gate(a)
        t = now_h
        for s_, hh in pre:
            if pre_w is not None and camp.fac.queue_wait(s_, t, max(hh, 0.01), camp.key) > pre_w:
                state["gate_refused_pre"] += 1
                return False
            s0, d0, _ = camp.fac.res[s_].find(t, max(hh, 0.01), camp.key)
            t = s0 + d0
        if state["windows"]:
            t_end = t + h + camp.GATE_W
            if any(a0 < t_end and b0 > now_h for a0, b0 in state["windows"]):
                state["gate_refused"] += 1
                return False
        return True
    camp.gate_ok = gate_ok


def _wrap_atomize(camp, R, state, frng, drng, diag_acc):
    truth = camp.truth
    orig = truth.atomize
    key = camp.key
    S = state["by_campaign"][key]

    def atomize(comp, proc, set_TL_C, rng):
        r = orig(comp, proc, set_TL_C, rng)                # the twin's own run (and its draws, so streams stay put)
        state["n"] += 1
        S["runs"] += 1
        p_twin = min(float(r.get("p_fail", P_BASE_TWIN)), 0.95)
        p_in = max(p_twin - P_BASE_TWIN, 0.0)               # the part of the twin's law that comes from the inputs
        if R["kind"] == "twin":
            failed = bool(r["failed"])
            cause = None
            if failed:
                cause = "intrinsic" if frng.random() < p_in / max(p_twin, 1e-9) else "transient"
        else:
            p_reg = region_p(key, comp) if R.get("region") else 0.0
            p_int = 1.0 - (1.0 - min(p_in, 0.95)) * (1.0 - p_reg)
            p_tr = transient_p(state["n"], R)
            i_fail = frng.random() < p_int
            t_fail = frng.random() < p_tr
            failed = i_fail or t_fail
            cause = "intrinsic" if i_fail else ("transient" if t_fail else None)
            if failed:
                r["usable_frac"] = 0.0
            elif r["failed"]:
                r["usable_frac"] = _usable(r["true_superheat_K"])
            r["failed"] = failed
            r["p_transient"] = p_tr
            r["p_intrinsic"] = p_int
            dmg = R.get("damage")
            if cause == "transient" and dmg and frng.random() < dmg["p"]:
                d_h = 24.0 * dmg["median_d"] * math.exp(frng.normal(0.0, dmg["sigma"]))
                t0 = float(getattr(camp, "_fail_last_t", 0.0))
                res = camp.fac.res["atomizer"]
                # bookings already made inside the window still run (counted, so the approximation is visible)
                state["overlap_h"] += sum(max(0.0, min(e, t0 + d_h) - max(s, t0)) for s, e, *_ in res.jobs if e > t0)
                res.down.append((t0, t0 + d_h))
                state["windows"].append((t0, t0 + d_h))
                state["damage"].append(dict(campaign=key, t_h=round(t0, 2), days=round(d_h / 24.0, 2)))
        r["cause"] = cause
        if failed:
            state["fails"] += 1
            S["fails"] += 1
            state[cause] += 1
            S[cause] += 1
            right = drng.random() < diag_acc
            r["diag"] = cause if right else ("transient" if cause == "intrinsic" else "intrinsic")
            S["misdiag"] += 0 if right else 1
        return r
    truth.atomize = atomize


def _wrap_release(camp):
    """When a lot's results come back, its runs go into the ledger the policy sees: settings, made powder or not,
    and the lab's diagnosis of a failure. ``cause`` (the truth) is there for the oracle strategy and the analysis;
    the other strategies never read it."""
    orig = camp.release
    camp.atom_ledger = []

    def release(t_h, p):
        if p.get("type") == "lot" and not p.get("gas"):
            lt = camp._lot_truth.get(p["id"]) or {}
            m = p["measured"]
            y = (m.get("yield") or {}).get("cut_yield_frac")
            into = p.get("into")
            target = into if (into in camp.lots and camp.lots[into]["design"] == p["design"]) else p["id"]
            for j, r in enumerate(lt.get("runs", [])):
                failed = bool(r.get("failed"))
                cause = r.get("cause") if failed else None
                if failed and cause is None:          # the 400 cm3 crucible's longer pour (charge_plan's p_fail_add)
                    cause = "intrinsic"
                diag = r.get("diag") if failed else None
                if failed and diag is None:
                    diag = cause
                camp.atom_ledger.append(dict(t=round(t_h, 3), design=p["design"], lot=target, event=p["id"],
                                             run=j, proc=dict(p.get("proc") or {}), ok=not failed, diag=diag,
                                             cause=cause, n_event=int(m.get("runs", 0)),
                                             f_event=int(m.get("failed_runs", 0)), y_event=y,
                                             into=target != p["id"]))
        return orig(t_h, p)
    camp.release = release


def _wrap_view(camp):
    orig = camp.view

    def view(now_h):
        v = orig(now_h)
        v["atom_ledger"] = camp.atom_ledger
        return v
    camp.view = view


def summary(tw):
    """What the regime did in one run (for the results line)."""
    st = tw.fail_state
    out = {k: st[k] for k in ("regime", "diag_acc", "n", "fails", "intrinsic", "transient", "damage", "gate_refused",
                              "gate_refused_pre")}
    out["overlap_h"] = round(st["overlap_h"], 2)
    out["by_campaign"] = st["by_campaign"]
    out["down_days"] = round(sum(d["days"] for d in st["damage"]), 2)
    return out
