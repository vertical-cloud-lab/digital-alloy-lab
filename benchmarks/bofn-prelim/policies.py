"""Sampling policies compared on the synthetic alloy network, all on equal $ budgets.

Every policy starts from the same data (CALPHAD on 32 compositions plus five
fully evaluated random designs) and is scored the way Buathong et al. (2024)
score them: the true objective of the design that maximizes the *network*
posterior mean fitted to that policy's data ("recommended alloy"), plus the
best objective among designs actually carried through tensile testing
("best validated alloy").
"""

from __future__ import annotations

import os
import time

import torch

import bofn_alloy
from bofn_alloy import (
    COMP,
    COSTS,
    D,
    IA,
    IPV,
    GROUPS,
    LAMBDA,
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
    normal_qmc,
    sobol,
)

N_CALPHAD0, N_FULL0 = 32, 5
SCREEN_N, SCREEN_TOP, F_SAFE = 256, 4, 0.25
NC = len(COMP)
S_REC = 64
S_ACQ = int(os.environ.get("BOFN_SACQ", 64))  # MC base samples inside pKGFN
N_CAND = int(os.environ.get("BOFN_NCAND", 16))  # candidates per stage scored by pKGFN each iteration


def initial_data(truth, seed):
    d = Data()
    lab = Lab(truth, d)
    for c in sobol(N_CALPHAD0, NC, seed=1000 + seed):
        lab.calphad(c)
    g = torch.Generator().manual_seed(2000 + seed)
    for x in torch.rand(N_FULL0, D, generator=g):
        lab.full_eval(x)
    d.spent = 0.0  # seed data is shared and sunk; budgets count new spend only
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
    return float(truth.objective(xr)), xr


class Recorder:
    def __init__(self, truth, d):
        self.truth, self.d = truth, d
        self.rows = []

    def __call__(self, net, it, action):
        if os.environ.get("BOFN_NO_REC"):  # skip the (noisy, slow) paper-protocol recommender
            rec, xr = float("nan"), torch.zeros(D)
        else:
            rec, xr = recommend(net, self.d, self.truth, it)
        best = max(v for _, v in self.d.full) if self.d.full else float("nan")
        # best printed alloy by the model (tensile-tested or not), scored by its true value
        Xb = torch.stack([design_of_build(self.d, j) for j in range(len(self.d.builds))])
        nub = net.mean(Xb, eps_for(Xb.shape[0], S_REC, 6))
        printed = float(self.truth.objective(Xb[nub.argmax()]))
        self.rows.append(
            {"spent": self.d.spent, "rec": rec, "best_validated": best, "rec_printed": printed,
             "action": action, "x_rec": [round(v, 4) for v in xr.tolist()]}
        )


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


def calphad_shortlist(d, lab, seed):
    """Stage 1 of tiered screening: simulate SCREEN_N compositions, keep the
    SCREEN_TOP strongest that CALPHAD predicts crack-free (freezing-range index
    below F_SAFE), net of the critical-mineral penalty."""
    for c in sobol(SCREEN_N, NC, seed=4000 + seed)[: SCREEN_N - N_CALPHAD0]:
        lab.calphad(c)
    comps = torch.tensor([list(k) for k in d.calphad])
    s = torch.tensor([v["s"] for v in d.calphad.values()])
    f = torch.tensor([v["f"] for v in d.calphad.values()])
    fom = s - LAMBDA * burden(torch.cat([comps, torch.zeros(len(comps), D - NC)], -1))
    fom = torch.where(f <= F_SAFE, fom, torch.full_like(fom, -9.0))
    return comps[fom.topk(SCREEN_TOP).indices]


def run_full_policy(kind, truth, seed, budget):
    d, lab = initial_data(truth, seed)
    rec = Recorder(truth, d)
    net = Network(d)
    rec(net, 0, "init")
    g = torch.Generator().manual_seed(3000 + seed)
    it = 0
    if kind.startswith("tiered"):
        shortlist = calphad_shortlist(d, lab, seed)
        net = Network(d)
        it += 1
        rec(net, it, "C-screen")
    reuse = kind in ("tiered", "tiered_pu", "eifn_reuse")
    cheapest = COSTS["L"] + COSTS["T"] if reuse else COSTS["A"] + COSTS["L"] + COSTS["T"] + COSTS["C"]
    while d.spent + cheapest <= budget:
        it += 1
        X = torch.stack([x for x, _ in d.full])
        y = torch.tensor([v for _, v in d.full])
        if kind == "eifn_reuse":
            # ablation: network EI per dollar over new designs and reprints of
            # existing powders (partial evaluation without KG's stage choice)
            best = float(y.max())
            Pn = torch.cat([sobol(1024, D, seed=it + 50 * seed), local_perturb(X, 16, 0.05, g)])
            pools, lots = [Pn], [-1] * Pn.shape[0]
            costs = [torch.full((Pn.shape[0],), COSTS["C"] + COSTS["A"] + COSTS["L"] + COSTS["T"])]
            for i, L in enumerate(d.lots):
                pv = sobol(64, 2, seed=it + 50 * seed + i)
                pools.append(torch.cat([L["c"].expand(64, NC), torch.full((64, 1), L["a"]), pv], -1))
                costs.append(torch.full((64,), COSTS["L"] + COSTS["T"]))
                lots += [i] * 64
            P, cost = torch.cat(pools), torch.cat(costs)
            ei, _ = network_ei_pool(net, d, P, eps_for(P.shape[0], 64, it), best)
            score = ei / cost
            score[cost > budget - d.spent] = -1.0
            j = int(score.argmax())
            if float(score[j]) < 0:  # nothing affordable (e.g. no lot to reuse and no room for a new pipeline)
                break
            if lots[j] >= 0:
                lab.tensile(lab.print_(lots[j], P[j, IPV]))
            else:
                lab.full_eval(P[j])
            net = Network(d)
            rec(net, it, "reuse" if lots[j] >= 0 else "full")
            continue
        if reuse:
            # Stage 2, done the way a careful lab would: BO on the shortlist only,
            # reusing each powder lot across LPBF trials ("tiered_pu": EI per dollar).
            gp = TinyGP(X, y)
            pools, costs, lots = [], [], []
            for c in shortlist:
                for i, L in enumerate(d.lots):
                    if torch.allclose(L["c"], c):
                        pv = sobol(64, 2, seed=it + 50 * seed + i)
                        pools.append(torch.cat([c.expand(64, NC), torch.full((64, 1), L["a"]), pv], -1))
                        costs.append(torch.full((64,), COSTS["L"] + COSTS["T"]))
                        lots += [i] * 64
                apv = sobol(128, 3, seed=it + 50 * seed)
                pools.append(torch.cat([c.expand(128, NC), apv], -1))
                costs.append(torch.full((128,), COSTS["A"] + COSTS["L"] + COSTS["T"]))
                lots += [-1] * 128
            P, cost = torch.cat(pools), torch.cat(costs)
            score = expected_improvement(gp, P, y.max()) / (cost if kind == "tiered_pu" else 1.0)
            score[cost > budget - d.spent] = -1.0
            j = int(score.argmax())
            if float(score[j]) < 0:  # only new $4,200 pipelines left and they do not fit
                break
            if lots[j] >= 0:
                lab.tensile(lab.print_(lots[j], P[j, IPV]))
            else:
                lab.full_eval(P[j])
            net = Network(d)
            rec(net, it, "reuse" if lots[j] >= 0 else "full")
            continue
        if kind == "random":
            x = torch.rand(D, generator=g)
        elif kind in ("ei", "tiered_naive"):
            gp = TinyGP(X, y)
            if kind == "ei":
                P = torch.cat([sobol(2048, D, seed=it + 50 * seed), local_perturb(X[y.topk(min(5, len(y))).indices], 64, 0.05, g)])
            else:
                apv = sobol(256, 3, seed=it + 50 * seed)
                P = torch.cat([torch.cat([c.expand(256, NC), apv], -1) for c in shortlist])
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
        rec(net, it, "full")
    return rec.rows, d


# --------------------------------------------------------------------------- pKGFN
def run_pkgfn(truth, seed, budget, verbose=False, lookahead=False, free_comp=False):
    """pKGFN; with lookahead=True, new powders are also valued by what printing
    them would reveal (atomize + print as one $4,000 move, q plugged in at its
    posterior mean), which one-step KG otherwise cannot see."""
    d, lab = initial_data(truth, seed)
    rec = Recorder(truth, d)
    net = Network(d)
    rec(net, 0, "init")
    g = torch.Generator().manual_seed(5000 + seed)
    gh_t, gh_w = gauss_hermite(10)
    w1 = gh_t.unsqueeze(-1)
    # 3-output CALPHAD fantasy: 2-point Gauss-Hermite product rule
    pm = torch.tensor([-1.0, 1.0])
    w3 = torch.cartesian_prod(pm, pm, pm)
    ww3 = torch.full((8,), 1 / 8)
    it = 0
    min_cost = min(COSTS.values())
    while d.spent + min_cost <= budget:
        it += 1
        t0 = time.time()
        left = budget - d.spent
        # ---- pool and anchoring set
        Xv = torch.stack([x for x, _ in d.full])
        P = torch.cat([sobol(512, D, seed=it + 100 * seed), local_perturb(Xv, 8, 0.05, g)])
        epsP = eps_for(P.shape[0], S_ACQ, 10_000 + it)
        smp = net.samples(P, epsP)
        nuP = smp.mean(-1)
        inc = nuP.max()
        Q = local_perturb(P[nuP.topk(8).indices], 24, 0.03, g)
        nuQ = net.mean(Q, eps_for(Q.shape[0], S_ACQ, 20_000 + it))
        P, nuP = torch.cat([P, Q]), torch.cat([nuP, nuQ])
        smpP = net.samples(P, eps_for(P.shape[0], S_ACQ, 30_000 + it))
        inc = smpP.mean(-1).max()
        eiP = (smpP - inc).clamp_min(0).mean(-1)
        anchors = [P[nuP.topk(32).indices], P[eiP.topk(16).indices]]
        cands = {}
        # ---- CALPHAD candidates: compositions of promising designs, plus space filling
        cx = torch.cat([P[eiP.topk(N_CAND - 4).indices], P[nuP.topk(4).indices]])
        cx = torch.cat([cx, torch.cat([sobol(4, NC, seed=it + 7 * seed), cx[:4, NC:]], -1)])
        cands["C"] = (cx[:, COMP], cx)
        ei_of = {"C": eiP.topk(N_CAND - 4).values.tolist() + [0.0] * 8}
        # ---- atomization candidates: simulated compositions, best (a, P, v) for each
        comps = torch.tensor([list(k) for k in d.calphad])
        gvals = torch.tensor([v["g"] for v in d.calphad.values()])
        apv = sobol(48, 3, seed=it + 11 * seed)
        PA = torch.cat([comps.unsqueeze(1).expand(-1, 48, -1), apv.unsqueeze(0).expand(len(comps), -1, -1)], -1)
        sA = net.samples(PA.reshape(-1, D), eps_for(PA.shape[0] * 48, S_ACQ, 40_000 + it))
        eiA = (sA - inc).clamp_min(0).mean(-1).reshape(len(comps), 48)
        best_apv = eiA.argmax(1)
        score = eiA.max(1).values
        keep = score.topk(min(N_CAND, len(comps))).indices
        xa = PA[keep, best_apv[keep]]
        za = torch.stack([xa[:, IA], gvals[keep]], -1)
        fa = torch.tensor([v["f"] for v in d.calphad.values()])[keep]
        ga, sa_ = gvals[keep], score[keep]
        if free_comp:
            # also allow alloys never simulated: CALPHAD runs automatically
            # before melting ($10), and its outputs enter KG at their GP means
            xn = torch.cat([P[eiP.topk(N_CAND).indices], P[nuP.topk(4).indices]])

            def gmean(n, X):
                m_, _ = net.gp[n].post_std(X[:, COMP])
                return m_ * net.gp[n].ys + net.gp[n].ym

            xa = torch.cat([xa, xn])
            fa = torch.cat([fa, gmean("f", xn)])
            ga = torch.cat([ga, gmean("g", xn)])
            sa_ = torch.cat([sa_, torch.cat([eiP.topk(N_CAND).values, eiP[nuP.topk(4).indices]])])
            za = torch.stack([xa[:, IA], ga], -1)
        cands["A"] = (za, xa)
        ei_of["A"] = sa_.tolist()
        if lookahead:
            mq, _ = net.gp["q"].post_std(za)
            qhat = mq * net.gp["q"].ys + net.gp["q"].ym
            z_virt = torch.cat([xa[:, IPV], fa.unsqueeze(-1), ga.unsqueeze(-1), qhat.unsqueeze(-1)], -1)
        # ---- LPBF candidates: existing powder lots, promising (P, v) for each
        if d.lots:
            pv = sobol(32, 2, seed=it + 13 * seed)
            rows, xs = [], []
            for i, L in enumerate(d.lots):
                cal = lab.calphad(L["c"])
                xs.append(torch.cat([L["c"].expand(32, NC), torch.full((32, 1), L["a"]), pv], -1))
                rows.append(torch.cat([pv, torch.tensor([[cal["f"], cal["g"], L["q"]]]).expand(32, 3)], -1))
            XL, ZL = torch.cat(xs), torch.cat(rows)
            sL = net.samples(XL, eps_for(XL.shape[0], S_ACQ, 50_000 + it))
            eiL = (sL - inc).clamp_min(0).mean(-1) + 1e-9 * sL.mean(-1)
            keep = eiL.topk(min(N_CAND, XL.shape[0])).indices
            cands["L"] = (ZL[keep], XL[keep])
            ei_of["L"] = eiL[keep].tolist()
        # ---- tensile candidates: untested builds
        untested = [j for j, B in enumerate(d.builds) if not B["tested"]]
        if untested:
            ZT, XT = [], []
            for j in untested:
                B = d.builds[j]
                cal = lab.calphad(d.lots[B["lot"]]["c"])
                ZT.append(torch.tensor([cal["s"], B["rho"]]))
                XT.append(design_of_build(d, j))
            cands["T"] = (torch.stack(ZT), torch.stack(XT))
            sT = net.samples(cands["T"][1], eps_for(len(untested), S_ACQ, 55_000 + it))
            ei_of["T"] = (sT - inc).clamp_min(0).mean(-1).tolist()
        # ---- shared inner-max set (anchored on the incumbent) and CRN base samples
        Xi = torch.cat(anchors + [v[1] for v in cands.values()])
        eps = eps_for(Xi.shape[0], S_ACQ, 60_000 + it)
        best = (None, -1.0, None)
        kg_log = {}

        def cost_of(grp, Xz):
            """Per-candidate cost; a never-simulated alloy also pays its $10 CALPHAD call."""
            c = torch.full((Xz.shape[0],), COSTS[grp])
            if grp == "A":
                c += torch.tensor([COSTS["C"] if tuple(round(float(v), 6) for v in x[COMP]) not in d.calphad else 0.0 for x in Xz])
            return c

        if lookahead:
            cv = cost_of("A", xa) + COSTS["L"]
            kv = net.kg("L", z_virt, Xi, eps, w1, gh_w).clamp_min(0) / cv
            kv[cv > left] = -1.0
            jv = int(kv.argmax())
            if float(kv[jv]) >= 0:
                kg_log["A+L"] = float(kv[jv]) * float(cv[jv])
                best = ("A", float(kv[jv]), jv)
        for grp, (Z, Xz) in cands.items():
            cv = cost_of(grp, Xz)
            if float(cv.min()) > left:
                continue
            w, ww = (w3, ww3) if grp == "C" else (w1, gh_w)
            kg = net.kg(grp, Z, Xi, eps, w, ww).clamp_min(0)
            ratio = kg / cv
            ratio[cv > left] = -1.0
            j = int(ratio.argmax())
            kg_log[grp] = float(kg[j])
            if float(ratio[j]) > best[1]:
                best = (grp, float(ratio[j]), j)
        grp, ratio, j = best
        if grp is None or ratio < 1e-10:
            # KG is flat (no single result can move the incumbent on this
            # discretization): fall back to network EI per dollar on the same
            # candidates, as fast-pKGFN does to propose candidates
            fb = [(e / float(c), k, i) for k in ("A", "L", "T") if k in cands for (i, e), c in zip(enumerate(ei_of.get(k, [])[: len(cands[k][0])]), cost_of(k, cands[k][1])) if float(c) <= left]
            fb = [t for t in fb if t[0] > 0]
            if not fb:
                break
            _, grp, j = max(fb)
            kg_log["fallback"] = grp
        Z, Xz = cands[grp]
        if grp == "C":
            lab.calphad(Z[j])
            changed = GROUPS["C"]
        elif grp == "A":
            new_alloy = tuple(round(float(v), 6) for v in Xz[j, COMP]) not in d.calphad
            lab.atomize(Xz[j, COMP], Xz[j, IA])
            changed = (GROUPS["C"] if new_alloy else []) + ["q"]
        elif grp == "L":
            # map the chosen design back to its lot
            xj = Xz[j]
            lot = next(i for i, L in enumerate(d.lots) if torch.allclose(L["c"], xj[COMP]) and abs(L["a"] - float(xj[IA])) < 1e-9)
            lab.print_(lot, xj[IPV])
            changed = ["rho"]
        else:
            lab.tensile(untested[j])
            changed = ["U"]
        net.refit(d, changed)
        rec(net, it, grp)
        rec.rows[-1]["fallback"] = "fallback" in kg_log  # True when KG was flat and EI per dollar chose the purchase
        if verbose:
            r = rec.rows[-1]
            print(f"it {it:3d} {grp} spent ${d.spent:8.0f} rec {r['rec']:.3f} best_val {r['best_validated']:.3f} KG {kg_log} {time.time() - t0:.1f}s", flush=True)
    return rec.rows, d


def run(kind, kappa, seed, budget):
    truth = AlloyTruth(kappa)
    torch.manual_seed(seed)
    bofn_alloy.FIT_LOG.update(calls=0, failures=0)
    if kind in ("pkgfn", "pkgfn_la", "pkgfn_free"):
        rows, d = run_pkgfn(truth, seed, budget, lookahead=kind != "pkgfn", free_comp=kind == "pkgfn_free")
    else:
        rows, d = run_full_policy(kind, truth, seed, budget)
    counts = {grp: sum(1 for g, _ in d.log if g == grp) for grp in COSTS}
    settings = {"S_ACQ": S_ACQ, "N_CAND": N_CAND, "S_REC": S_REC}
    return {"kind": kind, "kappa": kappa, "seed": seed, "budget": budget, "rows": rows, "counts": counts, "settings": settings, "gp_fits": dict(bofn_alloy.FIT_LOG)}
