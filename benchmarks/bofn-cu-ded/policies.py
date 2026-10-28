"""Sampling policies compared on the synthetic copper/DED alloy network, all on equal $ budgets.

Every policy starts from the same data (CALPHAD on 32 compositions plus five
random designs carried through every stage, Utah included) and is scored by the
true objective of the best design deposited at Mines and carried through tensile
and immersion ("best alloy demonstrated"). Two secondary metrics: the printed
alloy the policy's own model ranks best (`rec_printed`) and, if BOFN_REC is set,
the paper's recommender (`rec`, the argmax of the network posterior mean).
"""

from __future__ import annotations

import hashlib
import os
import time

import torch

import bofn_alloy
from bofn_alloy import (
    COMP,
    COSTS,
    D,
    F_SAFE,
    FULL_COST,
    GROUPS,
    IA,
    IAL,
    IFE,
    IMN,
    INI,
    IPV,
    LAMBDA,
    M_FIRST,
    P_CAP,
    SPEC,
    AlloyTruth,
    Data,
    Lab,
    Network,
    TinyGP,
    burden,
    design_of_build,
    gauss_hermite,
    local_perturb,
    sig,
    sobol,
    transform,
)

N_CALPHAD0, N_FULL0 = 32, 5
SCREEN_N, SCREEN_TOP = 256, 4
RHO_GATE = 0.5  # the screening policies' Utah density gate ("small blocks reach the density target")
UTAH_SCAN = (0.25, 0.45, 0.65)  # the careful lab's Utah process scan: travel speeds at Utah's full (capped) power
UTAH_TRIES = len(UTAH_SCAN)  # a lot that misses the density gate at all three is retired
W_QUANTILE = 0.75  # the one-hour screen gate: immersion only for builds in the top quartile of screened builds
NEAR = {"A": 0.03, "M": 0.05, "I": 0.03}  # "just either side of each cutoff" for the audit
FUNNEL_K = (12, 6, 3, 3)  # fixed top-k at the CALPHAD, powder, Utah and screen gates
NI_FLOOR = 10 / 30  # corrosion-aware tiered variants: shortlist only compositions with at least 10 wt% Ni
TIERED_KINDS = ("tiered", "tiered_ni", "tiered_ni_ref")
NC = len(COMP)
S_REC = 64
# pKGFN Monte Carlo settings: the aluminum production run's (bofn-prelim, PR 86). The first copper
# sweep used lighter ones (32, 10, 256; 16 perturbations; 24 + 12 anchors); those runs are kept in
# quality/results-light/ and run_sweep.py refuses to mix them with these.
S_ACQ = int(os.environ.get("BOFN_SACQ", 64))  # MC base samples inside pKGFN
N_CAND = int(os.environ.get("BOFN_NCAND", 16))  # candidates per stage scored by pKGFN each iteration
N_POOL = int(os.environ.get("BOFN_NPOOL", 512))  # Sobol designs in the per-iteration pool
N_PERT = 24  # local perturbations around each of the 8 designs with the best posterior mean
N_ANCHOR = (32, 16)  # inner-max anchors: the best by posterior mean, the best by EI
N_INCUMBENT = 4  # the best validated designs, always in the inner-max set
REC = bool(os.environ.get("BOFN_REC"))  # the paper's (slow, noisy) recommender metric; off by default
TAIL = COSTS["S"] + COSTS["T"] + COSTS["K"] + COSTS["I"]  # $750 of tests after a Mines build
PKGFN_KINDS = ("pkgfn", "pkgfn_screen", "pkgfn_audit", "mines_only")
KG_HOOK = None  # quality/mc_noise.py sets this to re-score each KG with other base samples


def initial_data(truth, seed):
    d = Data()
    lab = Lab(truth, d)
    for c in sobol(N_CALPHAD0, NC, seed=1000 + seed):
        lab.calphad(c)
    g = torch.Generator().manual_seed(2000 + seed)
    for x in torch.rand(N_FULL0, D, generator=g):
        lab.full_eval(x)
    d.spent = 0.0  # seed data is shared and sunk; budgets count new spend only
    d.log = []  # and purchase counts are new purchases only
    return d, lab


def eps_for(m, S, seed):
    g = torch.Generator().manual_seed(seed)
    return {n: torch.randn(m, S, generator=g) for n in SPEC}


def recommend(net: Network, d: Data, truth: AlloyTruth, it: int):
    """True objective at argmax of the network posterior mean (paper's metric)."""
    g = torch.Generator().manual_seed(77 + it)
    pool = [sobol(1024, D, seed=it)]
    if d.full:
        pool.append(torch.stack([x for x, _ in d.full]))
    if d.builds:
        pool.append(torch.stack([design_of_build(d, j) for j in range(len(d.builds))]))
    P = torch.cat(pool)
    nu = net.mean(P, eps_for(P.shape[0], S_REC, 5))
    for _ in range(2):
        top = P[nu.topk(8).indices]
        Q = local_perturb(top, 32, 0.04, g)
        nq = net.mean(Q, eps_for(Q.shape[0], S_REC, 5))
        P, nu = torch.cat([P, Q]), torch.cat([nu, nq])
    xr = P[nu.argmax()]
    return float(truth.objective(xr.unsqueeze(0))[0]), xr


class Recorder:
    def __init__(self, truth, d):
        self.truth, self.d = truth, d
        self.rows = []

    def __call__(self, net, it, action):
        if REC:
            rec, xr = recommend(net, self.d, self.truth, it)
        else:
            rec, xr = float("nan"), torch.zeros(D)
        best = max(v for _, v in self.d.full) if self.d.full else float("nan")
        # best deposited alloy by the model (tested or not), scored by its true value
        Xb = torch.stack([design_of_build(self.d, j) for j in range(len(self.d.builds))])
        nub = net.mean(Xb, eps_for(Xb.shape[0], S_REC, 6))
        printed = float(self.truth.objective(Xb[nub.argmax()].unsqueeze(0))[0])
        self.rows.append(
            {"spent": self.d.spent, "rec": rec, "best_validated": best, "rec_printed": printed, "action": action, "x_rec": [round(v, 4) for v in xr.tolist()]}
        )


def w_gate(d: Data):
    """The one-hour screen's gate: the top quartile of every screened build so far (seed builds included)."""
    return float(torch.tensor(d.obs["w"][1]).quantile(W_QUANTILE))


def network_ei_pool(net, d, P, eps, best):
    smp = net.samples(P, eps)
    return (smp - best).clamp_min(0).mean(-1), smp.mean(-1)


# --------------------------------------------------------------------------- full-evaluation policies
def expected_improvement(gp, P, best):
    m, v = gp.post_std(P)
    mu, sd = m * gp.ys + gp.ym, v.sqrt() * gp.ys
    z = (mu - best) / sd
    nrm = torch.distributions.Normal(0.0, 1.0)
    return sd * (z * nrm.cdf(z) + nrm.log_prob(z).exp())


def calphad_shortlist(d, lab, seed, top=SCREEN_TOP, ni_floor=None):
    """Stage 1 of tiered screening: simulate SCREEN_N compositions, keep the `top`
    strongest that CALPHAD predicts crack-free (solidification index at or below
    F_SAFE), net of the critical-mineral penalty. On this network that shortlist is
    aluminum bronzes with 2 to 6 wt% Ni, which the 30-day immersion test fails.
    With `ni_floor` (the corrosion-aware variants) only compositions with at least that
    much nickel are eligible; when fewer than `top` of them pass the crack screen, the
    shortlist is topped up with the least crack-prone (lowest f) of the rest."""
    for c in sobol(SCREEN_N, NC, seed=4000 + seed)[: SCREEN_N - N_CALPHAD0]:
        lab.calphad(c)
    comps = torch.tensor([list(k) for k in d.calphad])
    s = torch.tensor([v["s"] for v in d.calphad.values()])
    f = torch.tensor([v["f"] for v in d.calphad.values()])
    fom = s - LAMBDA * burden(torch.cat([comps, torch.zeros(len(comps), D - NC)], -1))
    ok = f <= F_SAFE
    if ni_floor is not None:
        ok = ok & (comps[:, INI] >= ni_floor)
    fom = torch.where(ok, fom, torch.full_like(fom, -9.0))
    order = fom.argsort(descending=True)
    order = order[fom[order] > -9.0][:top]
    if ni_floor is not None and len(order) < top:
        rest = [i for i in f.argsort().tolist() if float(comps[i, INI]) >= ni_floor and i not in order.tolist()]
        order = torch.cat([order, torch.tensor(rest[: top - len(order)], dtype=torch.long)])
    return comps[order], comps, fom, f


def w_ref_9010(truth):
    """The one-hour screen reading of a dense 90-10 Cu-Ni (C70600) reference coupon: its densest deposit
    in this truth (the corrosion-aware lab screens one beside its builds and immerses what beats it)."""
    from bofn_alloy import REFERENCE

    apv = sobol(4096, 3, seed=1)
    X = torch.cat([torch.tensor(REFERENCE["C70600 (90-10 Cu-Ni)"]).expand(apv.shape[0], NC), apv], -1)
    out = truth.full(X)
    return float(out["w"][out["rho_m"].argmax()])


def lab_gp(rows):
    return TinyGP(torch.stack([x for x, _ in rows]), torch.tensor([y for _, y in rows]))


def lot_passed_utah(L):
    return any(r >= RHO_GATE for _, _, r in L["utah"])


def chain(lab, d, lot, pv, need_utah, rows, w_fixed=None):
    """The careful lab's chain on one lot at settings pv: Utah unless the lot already passed the
    density gate, then Mines, microscopy, tensile, the screen, and immersion if the screen passes
    (top quartile of screened builds, or with `w_fixed` the reading of a reference coupon).
    Appends the lab's own record (x, y) to rows, with a proxy value for a stopped chain.
    Returns the action label."""
    L = d.lots[lot]
    if need_utah:
        # the small step scans travel speed at Utah's full (capped) power, one setting per visit
        pu = [P_CAP, UTAH_SCAN[len(L["utah"]) % len(UTAH_SCAN)]]
        r = lab.utah(lot, pu)
        if r < RHO_GATE:
            xu = torch.cat([L["c"], torch.tensor([L["a"]] + pu)])
            rows.append((xu, -LAMBDA * float(burden(xu))))  # did not deposit dense: recorded as a failure
            return "utah-fail"
    if not any(B["lot"] == lot for B in d.builds):
        pv = list(max(L["utah"], key=lambda t: t[2])[:2])  # the first Mines build on a lot uses the setting that passed at Utah
    x = torch.cat([L["c"], torch.tensor([L["a"]] + [float(v) for v in pv])])
    b = lab.mines(lot, pv)
    lab.microscopy(b)
    U = lab.tensile(b)
    w = lab.screen(b)
    gate = w_gate(d) if w_fixed is None else w_fixed
    if w >= gate:
        lab.immersion(b)
        rows.append((x, d.builds[b]["J"]))
        return "full"
    rows.append((x, U * float(sig(torch.tensor((w - gate) / 0.05))) - LAMBDA * float(burden(x))))  # the screen stands in for immersion
    return "screen-fail"


def run_funnel_stages(lab, d, comps, fom, fvals, rows):
    """A fixed top-k funnel at every gate (CALPHAD, powder, Utah, screen); returns the finalist
    compositions and the record of what each gate kept and rejected."""
    k1, k2, k3, k4 = FUNNEL_K
    gates = []
    order = fom.argsort(descending=True).tolist()
    keep = [i for i in order if float(fom[i]) > -9.0][:k1]
    gates.append({"gate": "CALPHAD", "rule": f"top {k1} by s - 0.3 B with f <= {F_SAFE}", "kept": [comps[i].tolist() for i in keep],
                  "rejected": [comps[i].tolist() for i in order if i not in keep]})
    lots = [lab.atomize(comps[i], torch.tensor(0.5)) for i in keep]
    qs = sorted(lots, key=lambda l: -d.lots[l]["q"])
    keep2 = qs[:k2]
    gates.append({"gate": "powder", "rule": f"top {k2} of {len(lots)} lots by q (atomized at a = 0.5)", "kept": [d.lots[l]["c"].tolist() for l in keep2],
                  "rejected": [d.lots[l]["c"].tolist() for l in qs[k2:]]})
    best = {}
    for l in keep2:
        best[l] = max((lab.utah(l, [0.5, v]), v) for v in (0.25, 0.45, 0.65))
    us = sorted(keep2, key=lambda l: -best[l][0])
    keep3 = us[:k3]
    gates.append({"gate": "Utah", "rule": f"top {k3} of {len(keep2)} lots by the best of three small-DED settings", "kept": [d.lots[l]["c"].tolist() for l in keep3],
                  "rejected": [d.lots[l]["c"].tolist() for l in us[k3:]]})
    builds = []
    for l in keep3:
        v = best[l][1]
        for pv in ([0.5, v], [0.75, min(v + 0.25, 1.0)]):
            b = lab.mines(l, pv)
            lab.microscopy(b)
            lab.tensile(b)
            lab.screen(b)
            builds.append(b)
    ws = sorted(builds, key=lambda b: -d.builds[b]["w"])
    keep4 = ws[:k4]
    for b in builds:
        x = design_of_build(d, b)
        B = d.builds[b]
        if b in keep4:
            lab.immersion(b)
            rows.append((x, B["J"]))
        else:
            rows.append((x, B["U"] * float(sig(torch.tensor((B["w"] - d.builds[keep4[-1]]["w"]) / 0.05))) - LAMBDA * float(burden(x))))
    gates.append({"gate": "screen", "rule": f"top {k4} of {len(builds)} Mines builds by the one-hour screen go to immersion",
                  "kept": [design_of_build(d, b).tolist() for b in keep4], "rejected": [design_of_build(d, b).tolist() for b in ws[k4:]]})
    return torch.stack([d.lots[l]["c"] for l in keep3]), gates


def run_full_policy(kind, truth, seed, budget):
    d, lab = initial_data(truth, seed)
    rec = Recorder(truth, d)
    net = Network(d)
    lab.net = net
    rec(net, 0, "init")
    g = torch.Generator().manual_seed(3000 + seed)
    it = 0
    rows = list(d.full)  # the lab's own records for tiered screening and the funnel
    gates = None
    w_fixed = None
    if kind == "tiered_ni_ref":  # one screen of the reference coupon, then it is the gate
        w_fixed = w_ref_9010(truth)
        lab._pay("K")
    if kind in TIERED_KINDS + ("funnel",):
        shortlist, comps, fom, fvals = calphad_shortlist(d, lab, seed, ni_floor=NI_FLOOR if kind in ("tiered_ni", "tiered_ni_ref") else None)
        net = Network(d)
        lab.net = net
        it += 1
        rec(net, it, "C-screen")
        if kind == "funnel":
            shortlist, gates = run_funnel_stages(lab, d, comps, fom, fvals, rows)
            net = Network(d)
            lab.net = net
            it += 1
            rec(net, it, "funnel")
    reuse = kind in TIERED_KINDS + ("funnel", "eifn_reuse")
    cheapest = COSTS["M"] + TAIL if reuse else FULL_COST
    while d.spent + cheapest <= budget:
        it += 1
        left = budget - d.spent
        X = torch.stack([x for x, _ in d.full])
        y = torch.tensor([v for _, v in d.full])
        if kind == "eifn_reuse":
            # ablation: network EI per dollar over new designs and new Mines sessions on
            # existing lots (partial evaluation without KG's stage choice; every remaining stage runs)
            best = float(y.max())
            Pn = torch.cat([sobol(1024, D, seed=it + 50 * seed), local_perturb(X, 16, 0.05, g)])
            pools, lots = [Pn], [-1] * Pn.shape[0]
            costs = [torch.full((Pn.shape[0],), FULL_COST)]
            for i, L in enumerate(d.lots):
                pv = sobol(64, 2, seed=it + 50 * seed + i)
                pools.append(torch.cat([L["c"].expand(64, NC), torch.full((64, 1), L["a"]), pv], -1))
                costs.append(torch.full((64,), lab.mines_cost(i) + TAIL))
                lots += [i] * 64
            P, cost = torch.cat(pools), torch.cat(costs)
            ei, _ = network_ei_pool(net, d, P, eps_for(P.shape[0], 64, it), best)
            score = ei / cost
            score[cost > left] = -1.0
            j = int(score.argmax())
            if float(score[j]) < 0:
                break
            if lots[j] >= 0:
                b = lab.mines(lots[j], P[j, IPV])
                lab.microscopy(b)
                lab.tensile(b)
                lab.screen(b)
                lab.immersion(b)
            else:
                lab.full_eval(P[j])
            net = Network(d)
            lab.net = net
            rec(net, it, "reuse" if lots[j] >= 0 else "full")
            continue
        if reuse:
            # Stage 2, done the way a careful lab would: EI on its own records over the
            # shortlist only, reusing each lot (and its scale-up) across sessions.
            gp = lab_gp(rows)
            pools, costs, lots, needs = [], [], [], []
            for c in shortlist:
                for i, L in enumerate(d.lots):
                    if torch.allclose(L["c"], c):
                        if not lot_passed_utah(L) and len(L["utah"]) >= UTAH_TRIES:
                            continue  # retired: this powder does not deposit dense at Utah
                        pv = sobol(64, 2, seed=it + 50 * seed + i)
                        pools.append(torch.cat([c.expand(64, NC), torch.full((64, 1), L["a"]), pv], -1))
                        passed = lot_passed_utah(L)
                        costs.append(torch.full((64,), (0.0 if passed else COSTS["U"]) + lab.mines_cost(i) + TAIL))
                        lots += [i] * 64
                        needs += [not passed] * 64
                if kind in TIERED_KINDS:  # a new lot of a shortlisted composition
                    apv = sobol(128, 3, seed=it + 50 * seed)
                    pools.append(torch.cat([c.expand(128, NC), apv], -1))
                    costs.append(torch.full((128,), COSTS["A"] + COSTS["U"] + M_FIRST + TAIL))
                    lots += [-1] * 128
                    needs += [True] * 128
            if not pools:
                break
            P, cost = torch.cat(pools), torch.cat(costs)
            score = expected_improvement(gp, P, max(v for _, v in rows))
            score[cost > left] = -1.0
            j = int(score.argmax())
            if float(score[j]) < 0:
                break
            if lots[j] >= 0:
                action = chain(lab, d, lots[j], P[j, IPV], needs[j], rows, w_fixed)
            else:
                lot = lab.atomize(P[j, COMP], P[j, IA])
                action = chain(lab, d, lot, P[j, IPV], True, rows, w_fixed)
            net = Network(d)
            lab.net = net
            rec(net, it, action)
            continue
        if kind == "random":
            x = torch.rand(D, generator=g)
        elif kind == "ei":
            gp = TinyGP(X, y)
            P = torch.cat([sobol(2048, D, seed=it + 50 * seed), local_perturb(X[y.topk(min(5, len(y))).indices], 64, 0.05, g)])
            x = P[expected_improvement(gp, P, y.max()).argmax()]
        elif kind == "eifn":
            best = float(y.max())
            P = torch.cat([sobol(1024, D, seed=it + 50 * seed), local_perturb(X, 16, 0.05, g)])
            ei, _ = network_ei_pool(net, d, P, eps_for(P.shape[0], 64, it), best)
            Q = local_perturb(P[ei.topk(8).indices], 32, 0.03, g)
            eq, _ = network_ei_pool(net, d, Q, eps_for(Q.shape[0], 64, it), best)
            P, ei = torch.cat([P, Q]), torch.cat([ei, eq])
            x = P[ei.argmax()]
        else:
            raise KeyError(kind)
        lab.full_eval(x)
        net = Network(d)
        lab.net = net
        rec(net, it, "full")
    return rec.rows, d, {"gates": gates, "shortlist": shortlist.tolist() if kind in TIERED_KINDS else None, "w_fixed": w_fixed}


# --------------------------------------------------------------------------- pKGFN
def run_pkgfn(truth, seed, budget, verbose=False, utah=True, screens=False, audit=False):
    """pKGFN over the eight stages. `utah=False` removes the small-DED stage (`mines_only`).
    `screens=True` makes it trust the screens (no atomizing a composition the CALPHAD crack
    screen rejects, no Mines session on a lot that has not passed the Utah density gate, no
    immersion on a build the one-hour screen stops); `audit=True` lets about one in ten stopped
    candidates go on anyway, plus those just either side of each cutoff (Advance 5)."""
    d, lab = initial_data(truth, seed)
    rec = Recorder(truth, d)
    net = Network(d)
    lab.net = net
    rec(net, 0, "init")
    g = torch.Generator().manual_seed(5000 + seed)
    gh_t, gh_w = gauss_hermite(10)
    w1 = gh_t.unsqueeze(-1)
    # 4-output CALPHAD fantasy: 2-point Gauss-Hermite product rule
    pm = torch.tensor([-1.0, 1.0])
    w4 = torch.cartesian_prod(pm, pm, pm, pm)
    ww4 = torch.full((16,), 1 / 16)
    it = 0
    events = []

    def passes(kind_, key, value, cutoff, above=True):
        """May a candidate go on past this screen? Returns (allowed, how)."""
        ok = value >= cutoff if above else value <= cutoff
        if not screens:
            return True, "pass" if ok else "nogate"
        if ok:
            return True, "pass"
        if audit:
            if abs(value - cutoff) < NEAR[kind_]:
                return True, "near"
            if int(hashlib.md5(f"{seed}:{kind_}:{key}".encode()).hexdigest(), 16) % 10 == 0:
                return True, "audit"
        return False, "stopped"

    while d.spent + COSTS["C"] <= budget:
        it += 1
        t0 = time.time()
        left = budget - d.spent
        # ---- pool and anchoring set
        Xv = torch.stack([x for x, _ in d.full])
        P = torch.cat([sobol(N_POOL, D, seed=it + 100 * seed), local_perturb(Xv, 8, 0.05, g)])
        nuP = net.mean(P, eps_for(P.shape[0], S_ACQ, 10_000 + it))
        Q = local_perturb(P[nuP.topk(8).indices], N_PERT, 0.03, g)
        nuQ = net.mean(Q, eps_for(Q.shape[0], S_ACQ, 20_000 + it))
        P, nuP = torch.cat([P, Q]), torch.cat([nuP, nuQ])
        smpP = net.samples(P, eps_for(P.shape[0], S_ACQ, 30_000 + it))
        # candidates are ranked by network EI over the best alloy demonstrated so far, as in EIFN. (The
        # aluminum version measured EI from the best posterior mean. On this network that is a pure-copper
        # design whose immersion gate is shut, so every EI came out zero and one seed stopped after $4,750.)
        yv = torch.tensor([v for _, v in d.full])
        inc = yv.max()
        eiP = (smpP - inc).clamp_min(0).mean(-1)
        # the inner max is anchored on the incumbent: the best validated designs themselves (not only
        # perturbations of them), the posterior-mean maximizer of the pool, and the best by EI (Edison F2)
        anchors = [Xv[yv.topk(min(N_INCUMBENT, len(yv))).indices], P[nuP.topk(N_ANCHOR[0]).indices], P[eiP.topk(N_ANCHOR[1]).indices]]
        cands, ei_of, smp_of, meta, costs = {}, {}, {}, {}, {}
        # ---- CALPHAD candidates: compositions of promising designs, plus space filling
        cx = torch.cat([P[eiP.topk(N_CAND - 4).indices], P[nuP.topk(4).indices]])
        cx = torch.cat([cx, torch.cat([sobol(4, NC, seed=it + 7 * seed), cx[:4, NC:]], -1)])
        cands["C"] = (cx[:, COMP], cx)
        ei_of["C"] = eiP.topk(N_CAND - 4).values.tolist() + [0.0] * 8
        # ---- atomization candidates: simulated compositions, best (a, P, v) for each
        keys = list(d.calphad)
        comps = torch.tensor([list(k) for k in keys])
        fa = torch.tensor([d.calphad[k]["f"] for k in keys])
        apv = sobol(48, 3, seed=it + 11 * seed)
        PA = torch.cat([comps.unsqueeze(1).expand(-1, 48, -1), apv.unsqueeze(0).expand(len(comps), -1, -1)], -1)
        sA = net.samples(PA.reshape(-1, D), eps_for(PA.shape[0] * 48, S_ACQ, 40_000 + it))
        eiA = (sA - inc).clamp_min(0).mean(-1).reshape(len(comps), 48)
        mA = sA.mean(-1).reshape(len(comps), 48)
        best_apv = (eiA + 1e-9 * mA).argmax(1)  # the posterior mean breaks ties when EI is zero
        score = eiA.gather(1, best_apv[:, None]).squeeze(1)
        allowed = torch.tensor([passes("A", k, float(fa[i]), F_SAFE, above=False)[0] for i, k in enumerate(keys)])
        rank = torch.where(allowed, score + 1e-9 * mA.gather(1, best_apv[:, None]).squeeze(1), torch.full_like(score, -float("inf")))
        keep = rank.topk(min(N_CAND, int(allowed.sum()))).indices
        if len(keep):
            xa = PA[keep, best_apv[keep]]
            za = torch.stack([xa[:, IA], xa[:, IMN], fa[keep]], -1)
            cands["A"] = (za, xa)
            ei_of["A"] = score[keep].tolist()
            smp_of["A"] = sA.reshape(len(comps), 48, -1)[keep, best_apv[keep]]
        # ---- small-DED (Utah) and large-DED (Mines) candidates: existing lots, promising (P, v) for each
        if d.lots:
            pv = sobol(32, 2, seed=it + 13 * seed)
            xsU, zU, lotU, xsM, zM, lotM, cM = [], [], [], [], [], [], []
            for i, L in enumerate(d.lots):
                cal = lab.calphad(L["c"])
                xs = torch.cat([L["c"].expand(32, NC), torch.full((32, 1), L["a"]), pv], -1)
                base = torch.cat([pv, torch.tensor([[cal["f"], cal["g"], cal["h"], L["q"]]]).expand(32, 4)], -1)
                if utah:
                    xsU.append(xs)
                    zU.append(transform("rho_u", base))
                    lotU += [i] * 32
                allowed_m = True
                if screens and utah:
                    best_u = max((r for _, _, r in L["utah"]), default=None)
                    allowed_m = best_u is not None and passes("M", i, best_u, RHO_GATE)[0]  # the careful lab runs the small step first
                if allowed_m:
                    rhat = net.gp["rho_u"].mean_raw(transform("rho_u", base))
                    xsM.append(xs)
                    zM.append(torch.cat([base, rhat.unsqueeze(-1)], -1))
                    lotM += [i] * 32
                    cM.append(torch.full((32,), lab.mines_cost(i)))
            for grp, xs_, z_, lots_, c_, sd in (("U", xsU, zU, lotU, None, 50_000), ("M", xsM, zM, lotM, cM, 51_000)):
                if not xs_:
                    continue
                Xg, Zg = torch.cat(xs_), torch.cat(z_)
                sG = net.samples(Xg, eps_for(Xg.shape[0], S_ACQ, sd + it))
                eiG = (sG - inc).clamp_min(0).mean(-1)
                # the posterior mean breaks ties for the ranking only: the fallback's positive-EI test
                # must see the raw EI (Edison F4; the tie-break once sent all-zero-EI cases down the EI branch)
                keep = (eiG + 1e-9 * sG.mean(-1)).topk(min(N_CAND, Xg.shape[0])).indices
                cands[grp] = (Zg[keep], Xg[keep])
                ei_of[grp] = eiG[keep].tolist()
                smp_of[grp] = sG[keep]
                meta[grp] = [lots_[k] for k in keep.tolist()]
                if c_ is not None:
                    costs[grp] = torch.cat(c_)[keep]
        # ---- test candidates: Mines builds at the next stage they have not had
        gate = w_gate(d)

        def build_cands(grp, cond, zfun, sd):
            idx = [j for j, B in enumerate(d.builds) if cond(j, B)]
            if not idx:
                return
            Z = torch.stack([zfun(j) for j in idx])
            Xb = torch.stack([design_of_build(d, j) for j in idx])
            sB = net.samples(Xb, eps_for(len(idx), S_ACQ, sd + it))
            e = (sB - inc).clamp_min(0).mean(-1)
            keep = (e + 1e-9 * sB.mean(-1)).topk(min(N_CAND, len(idx))).indices
            cands[grp] = (Z[keep], Xb[keep])
            ei_of[grp] = e[keep].tolist()
            smp_of[grp] = sB[keep]
            meta[grp] = [idx[k] for k in keep.tolist()]

        def binfo(j):
            B = d.builds[j]
            L = d.lots[B["lot"]]
            return B, L, lab.calphad(L["c"])

        def z_beta(j):
            B, L, cal = binfo(j)
            return torch.tensor([float(L["c"][IAL]), float(L["c"][INI]), B["pv"][0], B["pv"][1], B["rho_m"]])

        def z_U(j):
            B, L, cal = binfo(j)
            return torch.tensor([cal["s"], B["rho_m"], B["beta"]])

        def z_corr(j, with_w=False):
            B, L, cal = binfo(j)
            return torch.tensor([float(L["c"][INI]), float(L["c"][IAL]), float(L["c"][IFE]), B["rho_m"], B["beta"]] + ([B["w"]] if with_w else []))

        build_cands("S", lambda j, B: B["beta"] is None, z_beta, 55_000)
        build_cands("T", lambda j, B: B["beta"] is not None and B["U"] is None, z_U, 56_000)
        build_cands("K", lambda j, B: B["beta"] is not None and B["w"] is None, lambda j: z_corr(j), 57_000)
        build_cands("I", lambda j, B: B["w"] is not None and B["m"] is None and passes("I", j, B["w"], gate)[0], lambda j: z_corr(j, True), 58_000)
        # ---- test bundles: one-step KG cannot see that microscopy's value is to unlock the tensile test and
        # the screen, nor that the screen's is to unlock immersion. After a Mines build the policy therefore
        # also prices the bundles S+T, S+K+I and K+I, each valued by the knowledge gradient of its last stage
        # with the intermediate outputs plugged in at their posterior means (the aluminum version's lookahead).
        kg_group = {"S+T": "T", "S+K+I": "I", "K+I": "I"}

        def z_U_hat(j):
            B, L, cal = binfo(j)
            beta_hat = float(net.gp["beta"].mean_raw(z_beta(j).unsqueeze(0))[0])
            return torch.tensor([cal["s"], B["rho_m"], beta_hat])

        def z_m_hat(j, beta_known):
            B, L, cal = binfo(j)
            beta = B["beta"] if beta_known else float(net.gp["beta"].mean_raw(z_beta(j).unsqueeze(0))[0])
            zc = torch.tensor([float(L["c"][INI]), float(L["c"][IAL]), float(L["c"][IFE]), B["rho_m"], beta])
            w_hat = float(net.gp["w"].mean_raw(zc.unsqueeze(0))[0])
            return torch.cat([zc, torch.tensor([w_hat])])

        build_cands("S+T", lambda j, B: B["beta"] is None, z_U_hat, 59_000)
        build_cands("S+K+I", lambda j, B: B["beta"] is None, lambda j: z_m_hat(j, False), 59_500)
        build_cands("K+I", lambda j, B: B["beta"] is not None and B["w"] is None, lambda j: z_m_hat(j, True), 59_800)
        for key, c in (("S+T", COSTS["S"] + COSTS["T"]), ("S+K+I", COSTS["S"] + COSTS["K"] + COSTS["I"]), ("K+I", COSTS["K"] + COSTS["I"])):
            if key in cands:
                costs[key] = torch.full((cands[key][0].shape[0],), c)
        # ---- shared inner-max set (anchored on the incumbent) and CRN base samples; duplicates removed,
        # so a build that is a candidate for several tests gets one Monte Carlo estimate, not several (F2)
        Xi = torch.unique(torch.cat(anchors + [v[1] for v in cands.values()]), dim=0)
        eps = eps_for(Xi.shape[0], S_ACQ, 60_000 + it)
        best = (None, -1.0, None)
        kg_log = {}

        def cost_of(grp, Z):
            return costs[grp] if grp in costs else torch.full((Z.shape[0],), COSTS[grp])

        for grp, (Z, Xz) in cands.items():
            cv = cost_of(grp, Z)
            if float(cv.min()) > left:
                continue
            w, ww = (w4, ww4) if grp == "C" else (w1, gh_w)
            kg = net.kg(kg_group.get(grp, grp), Z, Xi, eps, w, ww).clamp_min(0)
            if KG_HOOK is not None:
                KG_HOOK(it, grp, net, kg_group.get(grp, grp), Z, Xi, eps, w, ww, cv, kg)
            ratio = kg / cv
            ratio[cv > left] = -1.0
            j = int(ratio.argmax())
            kg_log[grp] = float(kg[j])
            if float(ratio[j]) > best[1]:
                best = (grp, float(ratio[j]), j)
        grp, ratio, j = best

        def to_validation(k, i, c):
            """This purchase plus the cheapest remaining path to a validated build (tensile and immersion)."""
            if k == "A":
                return c + (COSTS["U"] if screens and utah else 0.0) + M_FIRST + TAIL
            if k == "U":
                return c + lab.mines_cost(meta["U"][i]) + TAIL
            if k == "M":
                return c + TAIL
            B = d.builds[meta[k][i]]
            done = set(k.split("+"))
            rest = (COSTS["S"] if B["beta"] is None and "S" not in done else 0.0) + (COSTS["T"] if B["U"] is None and "T" not in done else 0.0)
            if B["m"] is None and "I" not in done:
                rest += COSTS["I"] + (COSTS["K"] if B["w"] is None and "K" not in done else 0.0)
            return c + rest

        if grp is None or ratio < 1e-10:
            # KG is flat (no single result can move the incumbent on this discretization): fall back
            # to network EI on the same candidates, as fast-pKGFN does to propose candidates, per
            # dollar of the cheapest path to a validated build. (Dividing by the next stage's cost
            # alone, as the aluminum version did, made the copper runs buy lot after lot and Utah
            # session after session, since a design's EI only pays off once it is tested.)
            fb = []
            for k in ("A", "U", "M", "S", "T", "K", "I", "S+T", "S+K+I", "K+I"):
                if k not in cands:
                    continue
                cv = cost_of(k, cands[k][0])
                for i, e in enumerate(ei_of[k][: len(cands[k][0])]):
                    if float(cv[i]) <= left:
                        fb.append((e / to_validation(k, i, float(cv[i])), float(smp_of[k][i].max()), k, i))
            if not fb:
                break
            pos = [t for t in fb if t[0] > 0]
            # when no candidate has positive EI either, buy the one with the most optimistic posterior
            # sample, so the policy never stops with money left
            _, _, grp, j = max(pos) if pos else max(fb, key=lambda t: t[1])
            kg_log["fallback"] = grp if pos else grp + " (optimistic)"
            kg_log["fallback_branch"] = "ei" if pos else "optimistic"
        Z, Xz = cands[grp]
        if grp == "C":
            lab.calphad(Z[j])
            changed = GROUPS["C"]
        elif grp == "A":
            lab.atomize(Xz[j, COMP], Xz[j, IA])
            changed = ["q"]
        elif grp == "U":
            lab.utah(meta["U"][j], Xz[j, IPV])
            changed = ["rho_u"]
        elif grp == "M":
            lab.mines(meta["M"][j], Xz[j, IPV], rho_u_in=float(Z[j, -1]))
            changed = ["rho_m"]
        elif grp == "S":
            lab.microscopy(meta["S"][j])
            changed = ["beta"]
        elif grp == "T":
            lab.tensile(meta["T"][j])
            changed = ["U"]
        elif grp == "K":
            lab.screen(meta["K"][j])
            changed = ["w"]
        elif grp == "I":
            b = meta["I"][j]
            B = d.builds[b]
            how = passes("I", b, B["w"], gate)[1]
            lab.immersion(b)
            events.append({"it": it, "build": b, "w": B["w"], "gate": gate, "screen_pass": B["w"] >= gate, "how": how, "m": B["m"], "immersion_pass": B["m"] >= truth.m_ref})
            changed = ["m"]
        else:  # a test bundle; a trusting variant still checks the screen's gate before immersion
            b = meta[grp][j]
            B = d.builds[b]
            changed = []
            if "S" in grp.split("+"):
                lab.microscopy(b)
                changed.append("beta")
            if grp == "S+T":
                lab.tensile(b)
                changed.append("U")
            else:
                lab.screen(b)
                changed.append("w")
                gate = w_gate(d)
                ok, how = passes("I", b, B["w"], gate)
                if ok:
                    lab.immersion(b)
                    events.append({"it": it, "build": b, "w": B["w"], "gate": gate, "screen_pass": B["w"] >= gate, "how": how + "-bundle", "m": B["m"], "immersion_pass": B["m"] >= truth.m_ref})
                    changed.append("m")
        net.refit(d, changed)
        lab.net = net
        rec(net, it, grp)
        rec.rows[-1]["fallback"] = "fallback" in kg_log  # True when KG was flat and EI per dollar chose the purchase
        if "fallback" in kg_log:
            rec.rows[-1]["fallback_branch"] = kg_log["fallback_branch"]  # "ei" (EI per dollar) or "optimistic" (every EI zero)
        rec.rows[-1]["n_inner"] = int(Xi.shape[0])
        if verbose:
            r = rec.rows[-1]
            print(f"it {it:3d} {grp} spent ${d.spent:8.0f} best_val {r['best_validated']:.3f} printed {r['rec_printed']:.3f} KG {{{', '.join(f'{k}: {v:.2e}' if isinstance(v, float) else f'{k}: {v}' for k, v in kg_log.items())}}} {time.time() - t0:.1f}s", flush=True)
    return rec.rows, d, {"events": events}


def settings_for(kind):
    """What a stored run must match to be resumed (run_sweep.py, Edison F9): the truth and screens for
    every policy, and the Monte Carlo settings for the pKGFN-type ones (the others do not use them)."""
    s = {"TRUTH": bofn_alloy.TRUTH, "S_REC": S_REC, "REC": REC, "RHO_GATE": RHO_GATE, "W_QUANTILE": W_QUANTILE, "F_SAFE": F_SAFE}
    if kind in ("tiered_ni", "tiered_ni_ref"):
        s.update(NI_FLOOR=NI_FLOOR)
    if kind in PKGFN_KINDS:
        s.update(S_ACQ=S_ACQ, N_CAND=N_CAND, N_POOL=N_POOL, N_PERT=N_PERT, N_ANCHOR=list(N_ANCHOR), N_INCUMBENT=N_INCUMBENT, FIXES=["F2", "F4"])
    return s


def run(kind, kappa, eta, seed, budget, verbose=False):
    truth = AlloyTruth(kappa, eta)
    torch.manual_seed(seed)
    bofn_alloy.FIT_LOG.update(calls=0, failures=0)
    if kind in PKGFN_KINDS:
        rows, d, extra = run_pkgfn(truth, seed, budget, verbose=verbose, utah=kind != "mines_only", screens=kind in ("pkgfn_screen", "pkgfn_audit"), audit=kind == "pkgfn_audit")
    else:
        rows, d, extra = run_full_policy(kind, truth, seed, budget)
    counts = {grp: sum(1 for g_, _ in d.log if g_ == grp) for grp in COSTS}
    settings = settings_for(kind)
    builds = []
    for j, B in enumerate(d.builds):
        L = d.lots[B["lot"]]
        builds.append({"c": [round(float(v), 4) for v in L["c"]], "a": L["a"], "pv": B["pv"], "q": L["q"], "rho_u_in": B["rho_u_in"], "rho_m": B["rho_m"],
                       "beta": B["beta"], "U": B["U"], "w": B["w"], "m": B["m"], "J": B["J"]})
    lots = [{"c": [round(float(v), 4) for v in L["c"]], "a": L["a"], "q": L["q"], "utah": L["utah"], "sessions_left": L["sessions_left"]} for L in d.lots]
    out = {"kind": kind, "kappa": kappa, "eta": eta, "seed": seed, "budget": budget, "m_ref": truth.m_ref, "rows": rows, "counts": counts, "settings": settings,
           "gp_fits": dict(bofn_alloy.FIT_LOG), "builds": builds, "lots": lots, "w_gate_final": w_gate(d)}
    if extra.get("events") is not None:
        out["events"] = extra["events"]
    if extra.get("shortlist") is not None:
        out["shortlist"] = extra["shortlist"]
    if extra.get("w_fixed") is not None:
        out["w_ref_9010"] = extra["w_fixed"]
    if extra.get("gates") is not None:
        # false rejections per gate, judged by the truth after the fact: a rejected composition
        # (or build) whose best achievable objective beats what the funnel finally demonstrated
        final = max(v for _, v in d.full)
        apv = sobol(4096, 3, seed=9)
        gates = []
        for gt in extra["gates"]:
            rej = []
            for x in gt["rejected"]:
                if len(x) == NC:
                    Xr = torch.cat([torch.tensor(x).expand(apv.shape[0], NC), apv], -1)
                    pot = float(truth.objective(Xr).max())
                else:
                    pot = float(truth.objective(torch.tensor(x).unsqueeze(0))[0])
                rej.append(pot)
            gates.append({"gate": gt["gate"], "rule": gt["rule"], "n_kept": len(gt["kept"]), "n_rejected": len(gt["rejected"]), "rejected_potential": rej,
                          "false_rejections": int(sum(p > final for p in rej)), "best_rejected_potential": max(rej) if rej else None})
        out["gates"] = gates
        out["final_best_validated"] = final
    return out
