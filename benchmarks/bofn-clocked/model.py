"""Models: a small exact GP in numpy, and the function network built from one GP per node.

GP: RBF kernel with one lengthscale per input (ARD), a signal variance, a learned nugget on top of the known
measurement variance of each point, and optionally a *group offset* term (tau^2 when two points share a group).
The group term is how the provenance experiments model another lab's offset or a campaign's calibration drift:
y = f(x) + b_group + noise, b_group ~ N(0, tau^2). Hyperparameters are maximum a posteriori under weak log-normal
priors, fitted with L-BFGS-B on the analytic gradient, and refitted only when a node's data has grown by a third
(otherwise the old hyperparameters are kept and only the Cholesky factor is recomputed).

Network: the nodes of truth.py, each a GP on its own inputs (design dims plus parents' outputs), sampled in
topological order with common random numbers, as bofn-prelim's `Network.samples` does (Astudillo & Frazier 2021).
Two outputs per design: the objective (strength minus mineral burden) and the log corrosion rate.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import cho_solve, solve_triangular
from scipy.optimize import minimize
from scipy.stats import norm

from truth import IMM_SIG, SIG_BAR, SIG_BUILD, SIG_COUPON, SIG_Q, burden


class GP:
    def __init__(self, X, y, noise, groups=None, hyper=None, prior_mean=0.5, prior_sd=0.3):
        X = np.asarray(X, float).reshape(len(y), -1) if len(y) else np.zeros((0, 1))
        self.X, self.n = X, len(y)
        self.groups = None if groups is None else np.asarray(groups)
        self.prior_mean, self.prior_sd = prior_mean, prior_sd
        if self.n == 0:
            self.hyper = hyper
            return
        y = np.asarray(y, float)
        self.ym = float(y.mean()) if self.n > 1 else prior_mean
        self.ys = max(float(y.std()), prior_sd * 0.5) if self.n > 2 else prior_sd
        self.Y = (y - self.ym) / self.ys
        self.N = np.asarray(noise, float) / self.ys ** 2
        d = X.shape[1]
        self.use_g = self.groups is not None and len(np.unique(self.groups)) > 1
        if hyper is None or len(hyper) != d + 2 + self.use_g:
            hyper = self.fit(d)
        self.hyper = hyper
        self._factor()

    # ------------------------------------------------------------ kernel and likelihood
    def _unpack(self, th, d):
        ls = np.exp(th[:d])
        sf2 = math.exp(th[d])
        nug = math.exp(th[d + 1])
        tau2 = math.exp(th[d + 2]) if self.use_g else 0.0
        return ls, sf2, nug, tau2

    def _K(self, th, grad=False):
        d = self.X.shape[1]
        ls, sf2, nug, tau2 = self._unpack(th, d)
        Z = self.X / ls
        sq = (Z * Z).sum(1)
        D2 = np.maximum(sq[:, None] + sq[None, :] - 2 * Z @ Z.T, 0)
        R = np.exp(-0.5 * D2)
        K = sf2 * R + np.diag(self.N + nug)
        G = None
        if self.use_g:
            G = (self.groups[:, None] == self.groups[None, :]).astype(float)
            K = K + tau2 * G
        if not grad:
            return K
        dK = []
        for k in range(d):
            diff = self.X[:, k][:, None] - self.X[:, k][None, :]
            dK.append(sf2 * R * diff ** 2 / ls[k] ** 2)
        dK.append(sf2 * R)
        dK.append(nug * np.eye(self.n))
        if self.use_g:
            dK.append(tau2 * G)
        return K, dK

    PRIOR = dict(ls=(math.log(0.5), 1.2), sf2=(0.0, 1.0), nug=(math.log(1e-3), 2.0), tau2=(math.log(0.05), 1.5))

    def _bounds(self, d):
        b = [(math.log(0.03), math.log(30.0))] * d + [(math.log(0.05), math.log(20.0)), (math.log(1e-6), math.log(0.3))]
        if self.use_g:
            b.append((math.log(1e-4), math.log(4.0)))
        return b

    def _prior(self, th, d):
        terms = [(th[:d], *self.PRIOR["ls"]), (th[d:d + 1], *self.PRIOR["sf2"]), (th[d + 1:d + 2], *self.PRIOR["nug"])]
        if self.use_g:
            terms.append((th[d + 2:d + 3], *self.PRIOR["tau2"]))
        val, grad = 0.0, []
        for v, m, s in terms:
            val += float((((v - m) / s) ** 2).sum() / 2)
            grad.append((v - m) / s ** 2)
        return val, np.concatenate(grad)

    def _nll(self, th, d):
        try:
            K, dK = self._K(th, grad=True)
            L = np.linalg.cholesky(K + 1e-9 * np.eye(self.n))
        except np.linalg.LinAlgError:
            return 1e10, np.zeros_like(th)
        alpha = cho_solve((L, True), self.Y)
        Kinv = cho_solve((L, True), np.eye(self.n))
        W = np.outer(alpha, alpha) - Kinv
        nll = 0.5 * self.Y @ alpha + np.log(np.diag(L)).sum()
        g = np.array([-0.5 * (W * dk).sum() for dk in dK])
        pv, pg = self._prior(th, d)
        return nll + pv, g + pg

    def fit(self, d):
        th0 = np.array([math.log(0.5)] * d + [0.0, math.log(1e-3)] + ([math.log(0.05)] if self.use_g else []))
        idx = None
        if self.n > 250:  # fit on a subset; predictions use every point
            idx = np.random.default_rng(self.n).choice(self.n, 250, replace=False)
            full = (self.X, self.Y, self.N, self.groups, self.n)
            self.X, self.Y, self.N = self.X[idx], self.Y[idx], self.N[idx]
            self.groups = None if self.groups is None else self.groups[idx]
            self.n = 250
        try:
            r = minimize(self._nll, th0, args=(d,), jac=True, method="L-BFGS-B", bounds=self._bounds(d),
                         options=dict(maxiter=40))
            th = r.x
        except Exception:
            th = th0
        if idx is not None:
            self.X, self.Y, self.N, self.groups, self.n = full
        return th

    def _factor(self):
        K = self._K(self.hyper)
        jitter = 1e-9
        while True:
            try:
                self.L = np.linalg.cholesky(K + jitter * np.eye(self.n))
                break
            except np.linalg.LinAlgError:
                jitter *= 10
        self.alpha = cho_solve((self.L, True), self.Y)
        d = self.X.shape[1]
        self.ls, self.sf2, self.nug, self.tau2 = self._unpack(self.hyper, d)
        self.Z = self.X / self.ls
        self.zsq = (self.Z * self.Z).sum(1)

    # ------------------------------------------------------------ prediction
    def kstar(self, Xs, gs=None):
        Zs = np.asarray(Xs, float) / self.ls
        D2 = np.maximum((Zs * Zs).sum(-1)[..., None] + self.zsq - 2 * Zs @ self.Z.T, 0)
        K = self.sf2 * np.exp(-0.5 * D2)
        if self.use_g:
            g = 0 if gs is None else gs
            K = K + self.tau2 * (self.groups == g)
        return K

    def predict(self, Xs, gs=None, return_V=False):
        """Posterior mean and variance (raw units, latent: without measurement noise) at Xs [..., d]."""
        Xs = np.asarray(Xs, float)
        if self.n == 0:
            shp = Xs.shape[:-1]
            m, v = np.full(shp, self.prior_mean), np.full(shp, self.prior_sd ** 2)
            return (m, v, None) if return_V else (m, v)
        Ks = self.kstar(Xs, gs)
        mean = self.ym + self.ys * (Ks @ self.alpha)
        V = solve_triangular(self.L, Ks.reshape(-1, self.n).T, lower=True).T.reshape(Ks.shape)
        prior_v = self.sf2 + (self.tau2 if self.use_g else 0.0)
        var = np.maximum(prior_v - (V * V).sum(-1), 1e-10) * self.ys ** 2
        return (mean, var, V) if return_V else (mean, var)

    def cross(self, Xs, Vs, Xz, Vz, gs=None):
        """Posterior covariance (raw units) between Xs [..., d] and candidates Xz [b, d] -> [..., b]."""
        Zs, Zz = np.asarray(Xs) / self.ls, np.asarray(Xz) / self.ls
        D2 = np.maximum((Zs * Zs).sum(-1)[..., None] + (Zz * Zz).sum(-1) - 2 * Zs @ Zz.T, 0)
        k = self.sf2 * np.exp(-0.5 * D2)
        if self.use_g:
            k = k + self.tau2  # candidates are own-group, own-group predictions
        return (k - Vs @ Vz.T) * self.ys ** 2


# --------------------------------------------------------------------------- the network
class Network:
    """One GP per node, built from the lab's records (and optional prior records from history or other labs).

    group_mode: None (ignore site/epoch labels), "site" (offset per site on rho and U), "epoch" (offset per
    campaign). Records are dicts produced by `records()`; prior records carry their own site/epoch labels.
    """

    def __init__(self, truth, comps, recs, group_mode=None, hyper=None, cur_group=0):
        self.truth = truth
        self.nc = truth.ncomp
        self.lam = truth.lam
        self.burden = truth.burden_x if hasattr(truth, "burden_x") else burden
        old = hyper or {}
        self.hyper = {}
        self.cur = cur_group

        def mk(name, X, y, noise, pm, ps, groups=None):
            th = None
            if name in old and old[name][0] is not None and len(y) <= old[name][1] * 4 / 3 + 6:
                th = old[name][0]
            g = GP(X, y, noise, groups=groups, hyper=th, prior_mean=pm, prior_sd=ps)
            self.hyper[name] = (g.hyper, old[name][1] if th is not None else len(y))
            return g

        C = np.array([v["c"] for v in comps.values()])
        self.gp_c = {n: mk(n, C, np.array([v[n] for v in comps.values()]), np.full(len(C), 1e-6), 0.4, 0.3)
                     for n in ("s", "f", "g")}

        def grp(rows):
            if group_mode is None:
                return None
            if group_mode == "site":
                return np.array([0 if r.get("site", "own") == "own" else 1 for r in rows])
            return np.array([int(r.get("epoch", cur_group)) for r in rows])

        rq, rr, ru, rc = recs["q"], recs["rho"], recs["U"], recs["corr"]
        self.gp_q = mk("q", np.array([[r["a"], r["g"], r["gas"]] for r in rq]).reshape(-1, 3),
                       np.array([r["y"] for r in rq]), np.full(len(rq), SIG_Q ** 2), 0.6, 0.3)
        self.ext = any(r.get("ext", 0) for r in rr)  # another lab's printer as its own machine (provenance kept)
        self.gp_rho = mk("rho", np.array([[r["P"], r["v"], r["f"], r["g"], r["q"], r["pt"], r["gas"]] + ([r.get("ext", 0.0)] if self.ext else [])
                                          for r in rr]).reshape(-1, 8 if self.ext else 7),
                         np.array([r["y"] for r in rr]), np.full(len(rr), SIG_BUILD ** 2 + SIG_COUPON ** 2), 0.4, 0.3,
                         grp(rr))
        self.gp_U = mk("U", np.array([[r["s"], r["rho"]] for r in ru]).reshape(-1, 2),
                       np.array([r["y"] for r in ru]), np.full(len(ru), SIG_BAR ** 2 + (0.8 * SIG_COUPON) ** 2), 0.4, 0.3,
                       grp(ru))
        self.gp_corr = mk("corr", np.array([list(r["c"]) + [r["rho"]] for r in rc]).reshape(-1, self.nc + 1),
                          np.array([r["y"] for r in rc]), np.array([r["noise"] for r in rc]), 0.7, 0.8)

    # ------------------------------------------------------------ sampling
    def comp_nodes(self, C):
        out = {}
        for n in ("s", "f", "g"):
            out[n] = self.gp_c[n].predict(C)
        return out

    def sample(self, X, gas, pt, eps, known=None):
        """Objective and ln corrosion-rate samples [m, S] at designs X [m, nc+3] (c, a, P, v).

        gas, pt: [m] route and machine indicators. eps: dict node -> [m, S] standard normals (common random numbers).
        known: optional dict with arrays [m] for s, f, g, q (measured or exact) that replace the GP's draws."""
        m, S = X.shape[0], eps["rho"].shape[1]
        nc = self.nc
        c = X[:, :nc]
        known = known or {}
        v = {}
        cn = self.comp_nodes(c)
        for n in ("s", "f", "g"):
            if n in known:
                v[n] = np.repeat(np.asarray(known[n], float)[:, None], S, 1)
            else:
                mu, var = cn[n]
                v[n] = mu[:, None] + np.sqrt(var)[:, None] * eps[n]
        if "q" in known:
            v["q"] = np.repeat(np.asarray(known["q"], float)[:, None], S, 1)
        else:
            inp = np.stack([np.repeat(X[:, nc][:, None], S, 1), v["g"], np.repeat(gas[:, None], S, 1)], -1)
            mu, var = self.gp_q.predict(inp)
            v["q"] = mu + np.sqrt(var) * eps["q"]
        inp = np.stack([np.repeat(X[:, nc + 1][:, None], S, 1), np.repeat(X[:, nc + 2][:, None], S, 1), v["f"], v["g"],
                        v["q"], np.repeat(pt[:, None], S, 1), np.repeat(gas[:, None], S, 1)]
                       + ([np.zeros((m, S))] if self.ext else []), -1)
        mu, var = self.gp_rho.predict(inp, self.cur)
        v["rho"] = mu + np.sqrt(var) * eps["rho"]
        mu, var = self.gp_U.predict(np.stack([v["s"], v["rho"]], -1), self.cur)
        v["U"] = mu + np.sqrt(var) * eps["U"]
        cin = np.concatenate([np.repeat(c[:, None, :], S, 1), v["rho"][..., None]], -1)
        mu, var = self.gp_corr.predict(cin)
        v["lnr"] = mu + np.sqrt(var) * eps["corr"]
        v["p_pass"] = norm.cdf((self.truth.ln_rmax - mu) / np.sqrt(var))  # smooth, so a small chance isn't rounded to 0
        obj = v["U"] - self.lam * self.burden(c)[:, None]
        return obj, v["lnr"], v

    def claim_value(self, obj, lnr):
        """Claimable value of each draw: the objective if the corrosion test would pass, else 0."""
        return np.where(lnr <= self.truth.ln_rmax, obj, 0.0)


def eps_for(m, S, seed, nodes=("s", "f", "g", "q", "rho", "U", "corr")):
    rng = np.random.default_rng(seed)
    return {n: rng.standard_normal((m, S)) for n in nodes}


# --------------------------------------------------------------------------- records from the lab
def records(lab, extra=None):
    """Node-level records of everything the lab has measured (plus `extra`: prior records)."""
    R = {"q": [], "rho": [], "U": [], "corr": []}
    site = getattr(lab, "site", "own")
    for lot in lab.lots:
        if lot["q_meas"] is None:
            continue
        cal = lab.comps[lot["key"]]
        R["q"].append(dict(a=lot["a"] if lot["a"] is not None else 0.5, g=cal["g"], gas=float(lot["route"] == "gas"),
                           y=lot["q_meas"], site=site, epoch=lot["epoch"]))
    for cp in lab.coupons:
        if cp["rho_meas"] is None:
            continue
        lot = lab.lots[cp["lot"]]
        cal = lab.comps[cp["key"]]
        R["rho"].append(dict(P=cp["P"], v=cp["v"], f=cal["f"], g=cal["g"], q=lot["q_meas"], pt=float(cp["machine"] == "pt"),
                             gas=float(cp["route"] == "gas"), y=cp["rho_meas"], site=site, epoch=cp["epoch"]))
        for u in cp["bars"]:
            R["U"].append(dict(s=cal["s"], rho=cp["rho_meas"], y=u, site=site, epoch=cp["epoch"]))
        if cp["imm_read"]:
            d = max(cp["imm_read"])
            R["corr"].append(dict(c=cp["c"], rho=cp["rho_meas"], y=cp["imm_read"][d], noise=IMM_SIG[d] ** 2))
    if extra:
        for k in R:
            R[k] = list(extra.get(k, [])) + R[k]
    return R
