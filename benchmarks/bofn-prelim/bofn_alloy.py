"""Cost-aware Bayesian optimization of a synthetic alloy function network.

Preliminary benchmark for the MS&T26 talk (issue 83): does choosing *which
stage to run next* (pKGFN, Buathong et al. ICML 2024) beat tiered screening
and full-pipeline BO when stages cost $10 to $2,500 each?

Design vector x (all scaled to [0, 1]):
    x0 c1  main solute (Zn+Mg)        x4 a  ultrasonic atomization setting
    x1 c2  secondary solute (Cu)      x5 P  laser power
    x2 c3  Zr (grain refiner)         x6 v  scan speed
    x3 c4  Sc (refiner + strengthener, most critical)

Function network (one GP per node, outputs feed children):
    CALPHAD   (c)             -> s (strengthening phase), f (freezing range), g (primary nucleant)
    Atomize   (a, g)          -> q (powder quality)
    LPBF      (P, v, f, g, q) -> rho (printability / dense, crack-free fraction)
    Tensile   (s, rho)        -> U (strength)
    objective = U - LAMBDA * B(c), B = USGS-style critical-mineral burden (known)

The simulation-vs-experiment bias is `kappa`: how strongly the nucleant g
suppresses hot cracking in LPBF. A CALPHAD-only screen (freezing range below a
crack threshold) cannot see it, which is the documented behaviour of
Zr-inoculated 7075/6061 (Martin et al., Nature 2017). kappa = 0 makes the
screen's crack criterion exactly right.
"""

from __future__ import annotations

import math

import torch
from botorch.fit import fit_gpytorch_mll
from botorch.models import SingleTaskGP
from gpytorch.mlls import ExactMarginalLogLikelihood

torch.set_default_dtype(torch.double)

D = 7
COMP, IA, IPV = [0, 1, 2, 3], 4, [5, 6]
COSTS = {"C": 10.0, "A": 1500.0, "L": 2500.0, "T": 200.0}
FULL_COST = sum(COSTS.values())
LAMBDA = 0.3

# node -> (design dims, parent nodes); order is topological
SPEC = {
    "s": (COMP, []),
    "f": (COMP, []),
    "g": (COMP, []),
    "q": ([IA], ["g"]),
    "rho": (IPV, ["f", "g", "q"]),
    "U": ([], ["s", "rho"]),
}
ORDER = list(SPEC)
GROUPS = {"C": ["s", "f", "g"], "A": ["q"], "L": ["rho"], "T": ["U"]}
GROUP_OF = {n: g for g, ns in GROUPS.items() for n in ns}


def burden(x):
    """Critical-mineral burden of the composition (known, free to compute)."""
    return 0.15 * x[..., 0] + 0.1 * x[..., 1] + 0.2 * x[..., 2] + 1.0 * x[..., 3]


# --------------------------------------------------------------------------- truth
class AlloyTruth:
    def __init__(self, kappa: float = 1.0):
        self.kappa = kappa

    def node(self, name, inp):
        """Evaluate one node on its own input vector (design dims + parent outputs)."""
        if name in ("s", "f", "g"):
            c1, c2, c3, c4 = inp[..., 0], inp[..., 1], inp[..., 2], inp[..., 3]
            if name == "s":
                return (1 - torch.exp(-(1.4 * c1 + 0.9 * c2 + 1.5 * c1 * c2)) + 0.1 * c3 + 0.3 * c4) / 1.2
            if name == "f":
                return 0.65 * c1 + 0.55 * c2 - 0.25 * c1 * c2 + 0.05 * c3 + 0.03 * c4
            return (0.6 * c3.clamp(min=0) ** 1.5 + 0.9 * c4.clamp(min=0) ** 1.2) * (1 + 0.2 * c1) / 1.8
        if name == "q":
            a, g = inp[..., 0], inp[..., 1]
            a_opt = 0.3 + 0.45 * g
            return torch.exp(-(((a - a_opt) / 0.28) ** 2)) * (0.9 + 0.1 * (1 - g))
        if name == "rho":
            P, v, f, g, q = inp[..., 0], inp[..., 1], inp[..., 2], inp[..., 3], inp[..., 4]
            # dense parts lie along a constant-energy-density ridge in (P, v) whose
            # offset grows with freezing range; very high power keyholes
            u = P - v - (0.05 + 0.25 * f)
            window = torch.exp(-((u / 0.2) ** 2)) * (1 - 0.35 * torch.sigmoid((P - 0.85) / 0.05))
            g = g.clamp(min=0)
            f_eff = f * (1 - self.kappa * 0.85 * g / (g + 0.12))
            crack = torch.sigmoid((f_eff - 0.38) / 0.05)
            return window * q.clamp(min=0) ** 0.3 * (1 - 0.75 * crack)
        if name == "U":
            s, rho = inp[..., 0], inp[..., 1]
            return (0.25 + 0.75 * s) * rho
        raise KeyError(name)

    def full(self, x):
        """All node outputs for designs x [..., D]."""
        out = {}
        for n in ORDER:
            dims, parents = SPEC[n]
            inp = torch.cat([x[..., dims]] + [out[p].unsqueeze(-1) for p in parents], -1)
            out[n] = self.node(n, inp)
        return out

    def objective(self, x):
        return self.full(x)["U"] - LAMBDA * burden(x)


# --------------------------------------------------------------------------- GP
FIT_LOG = {"calls": 0, "failures": 0}  # per process; policies.run() resets it and stores it in the run JSON


class TinyGP:
    """Exact GP with BoTorch-fitted RBF hyperparameters and cheap batched posteriors."""

    def __init__(self, X, y, noise=1e-6):
        n, d = X.shape
        self.X, self.y = X, y
        self.ym = y.mean()
        # node outputs live on [0, 1]: keep a physical prior scale even when early
        # observations are all alike (e.g. every random print cracked)
        self.ys = y.std().clamp_min(0.25) if n > 1 else torch.tensor(0.25)
        Y = ((y - self.ym) / self.ys).unsqueeze(-1)
        model = SingleTaskGP(X, Y, train_Yvar=torch.full_like(Y, noise), outcome_transform=None)
        FIT_LOG["calls"] += 1
        try:
            fit_gpytorch_mll(ExactMarginalLogLikelihood(model.likelihood, model))
        except Exception:  # keep the prior/partially fitted hyperparameters, but count it
            FIT_LOG["failures"] += 1
        self.ls = model.covar_module.lengthscale.detach().reshape(-1)
        self.const = model.mean_module.constant.detach().reshape(())
        self.noise = noise
        self.Xs = X / self.ls
        K = self._k(self.Xs, self.Xs) + (noise + 1e-8) * torch.eye(n)
        L = torch.linalg.cholesky(K)
        self.Linv = torch.linalg.solve_triangular(L, torch.eye(n), upper=False)
        self.alpha = self.Linv.T @ (self.Linv @ (Y.squeeze(-1) - self.const))

    @staticmethod
    def _k(A, B):
        d2 = (A * A).sum(-1, keepdim=True) - 2 * A @ B.T + (B * B).sum(-1)
        return torch.exp(-0.5 * d2.clamp_min(0))

    def post_std(self, U, return_V=False):
        """Posterior mean/var in standardized units for raw inputs U [..., d]."""
        Kx = self._k(U / self.ls, self.Xs)
        mean = self.const + Kx @ self.alpha
        V = Kx @ self.Linv.T
        var = (1.0 - (V * V).sum(-1)).clamp_min(1e-12)
        return (mean, var, V) if return_V else (mean, var)

    def cov_std(self, U, VU, Z, VZ):
        """Posterior covariance between U [..., d] and candidates Z [b, d] -> [..., b]."""
        return self._k(U / self.ls, Z / self.ls) - VU @ VZ.T


def node_input(name, x, vals):
    dims, parents = SPEC[name]
    shape = torch.broadcast_shapes(*[vals[p].shape for p in parents]) if parents else x[..., 0].shape
    xs = x[..., dims].expand(*shape, len(dims)) if dims else None
    parts = ([xs] if xs is not None else []) + [vals[p].expand(shape).unsqueeze(-1) for p in parents]
    return torch.cat(parts, -1)


# --------------------------------------------------------------------------- data
class Data:
    """Per-node observations plus the physical inventory (powder lots, builds)."""

    def __init__(self):
        self.obs = {n: ([], []) for n in ORDER}
        self.calphad = {}  # composition tuple -> dict(s, f, g)
        self.lots = []  # dict(c, a, q)
        self.builds = []  # dict(lot, pv, rho, tested, U)
        self.full = []  # (x, objective) fully validated designs
        self.spent = 0.0
        self.log = []  # (group, spent after)

    def add(self, name, inp, val):
        self.obs[name][0].append(inp.detach().clone())
        self.obs[name][1].append(float(val))

    def tensors(self, name):
        X, y = self.obs[name]
        return torch.stack(X), torch.tensor(y)


class Lab:
    """Runs stages against the truth, enforcing upstream requirements and costs."""

    def __init__(self, truth: AlloyTruth, data: Data):
        self.t, self.d = truth, data

    def _pay(self, group):
        self.d.spent += COSTS[group]
        self.d.log.append((group, self.d.spent))

    def calphad(self, c):
        key = tuple(round(float(v), 6) for v in c)
        if key in self.d.calphad:
            return self.d.calphad[key]
        out = {n: float(self.t.node(n, c)) for n in GROUPS["C"]}
        for n, v in out.items():
            self.d.add(n, c, v)
        self.d.calphad[key] = out
        self._pay("C")
        return out

    def atomize(self, c, a):
        cal = self.calphad(c)
        inp = torch.tensor([float(a), cal["g"]])  # node q input order: (a, g)
        q = float(self.t.node("q", inp))
        self.d.add("q", inp, q)
        self.d.lots.append({"c": c.clone(), "a": float(a), "q": q})
        self._pay("A")
        return len(self.d.lots) - 1

    def print_(self, lot, pv):
        L = self.d.lots[lot]
        cal = self.calphad(L["c"])
        pv = [float(v) for v in pv]
        inp = torch.tensor(pv + [cal["f"], cal["g"], L["q"]])
        rho = float(self.t.node("rho", inp))
        self.d.add("rho", inp, rho)
        self.d.builds.append({"lot": lot, "pv": pv, "rho": rho, "tested": False})
        self._pay("L")
        return len(self.d.builds) - 1

    def tensile(self, build):
        B = self.d.builds[build]
        L = self.d.lots[B["lot"]]
        cal = self.calphad(L["c"])
        inp = torch.tensor([cal["s"], B["rho"]])
        U = float(self.t.node("U", inp))
        self.d.add("U", inp, U)
        B["tested"], B["U"] = True, U
        x = torch.cat([L["c"], torch.tensor([L["a"]] + B["pv"])])
        self.d.full.append((x, U - LAMBDA * float(burden(x))))
        self._pay("T")

    def full_eval(self, x):
        lot = self.atomize(x[COMP], x[IA])
        b = self.print_(lot, x[IPV])
        self.tensile(b)


def design_of_build(d: Data, j):
    B = d.builds[j]
    L = d.lots[B["lot"]]
    return torch.cat([L["c"], torch.tensor([L["a"]] + B["pv"])])


# --------------------------------------------------------------------------- network model
class Network:
    def __init__(self, data: Data):
        self.gp = {n: TinyGP(*data.tensors(n)) for n in ORDER}

    def refit(self, data: Data, names):
        for n in names:
            self.gp[n] = TinyGP(*data.tensors(n))

    def _sample(self, n, inp, eps):
        gp = self.gp[n]
        m, v = gp.post_std(inp)
        return (m + v.sqrt() * eps) * gp.ys + gp.ym

    def samples(self, x, eps):
        """Objective samples at designs x [m, D] with base samples eps[node] [m, S] -> [m, S]."""
        vals = {}
        xe = x.unsqueeze(-2)  # [m, 1, D]
        for n in ORDER:
            inp = node_input(n, xe, vals) if SPEC[n][1] else x[..., SPEC[n][0]].unsqueeze(-2)
            vals[n] = self._sample(n, inp, eps[n])
        return vals["U"] - LAMBDA * burden(x).unsqueeze(-1)

    def mean(self, x, eps):
        return self.samples(x, eps).mean(-1)

    def kg(self, group, Z, Xi, eps, w, ww, chunk=4):
        """pKGFN value of evaluating `group` at candidate node inputs Z [b, d] (Buathong et al. 2024).

        Discrete inner max over the shared, incumbent-anchored design set Xi [m, D];
        fantasies w [nf, r] with weights ww [nf]; common random numbers eps.
        """
        nodes = GROUPS[group]
        out = []
        for i in range(0, Z.shape[0], chunk):
            Zc = Z[i : i + chunk]
            b = Zc.shape[0]
            vals = {}
            xe = Xi.unsqueeze(-2)  # [m, 1, D]
            for n in ORDER:
                gp = self.gp[n]
                if SPEC[n][1]:
                    inp = node_input(n, xe, vals)
                else:
                    inp = Xi[..., SPEC[n][0]].unsqueeze(-2).expand(-1, eps[n].shape[-1], -1)
                if n in nodes:
                    r = nodes.index(n)
                    mu, var, VU = gp.post_std(inp, return_V=True)  # [..., m, S]
                    mz, vz, VZ = gp.post_std(Zc, return_V=True)  # [b]
                    cov = gp.cov_std(inp, VU, Zc, VZ)  # [..., m, S, b]
                    cov = cov.movedim(-1, 0)  # [b, ..., m, S]
                    sz = (vz + gp.noise).sqrt().view(b, *([1] * (cov.dim() - 1)))
                    # broadcast fantasy dim: result [b, nf, ..., m, S]
                    shift = (cov / sz).unsqueeze(1) * w[:, r].view(1, -1, *([1] * (cov.dim() - 1)))
                    vplus = (var.unsqueeze(0) - (cov / sz) ** 2).clamp_min(1e-12).unsqueeze(1)
                    if mu.dim() > 2:  # already carries [b, nf] from an upstream group node
                        mu_b = mu
                    else:
                        mu_b = mu.view(1, 1, *mu.shape)
                    vals[n] = (mu_b + shift + vplus.sqrt() * eps[n]) * gp.ys + gp.ym
                else:
                    mu, var = gp.post_std(inp)
                    vals[n] = (mu + var.sqrt() * eps[n]) * gp.ys + gp.ym
            obj = vals["U"] - LAMBDA * burden(Xi).unsqueeze(-1)
            obj = obj.expand(b, w.shape[0], *obj.shape[-2:]) if obj.dim() == 4 else obj
            nu = obj.mean(-1)  # [b, nf, m]
            best = nu.max(-1).values  # [b, nf]
            # current value from the same fantasy-averaged estimator, so KG >= 0
            # by Jensen and the MC error largely cancels between the two terms
            base = (nu * ww.view(1, -1, 1)).sum(1).max(-1).values  # [b]
            out.append((best * ww).sum(-1) - base)
        return torch.cat(out)


def sobol(n, d, seed):
    eng = torch.quasirandom.SobolEngine(d, scramble=True, seed=seed)
    return eng.draw(n).double()


def normal_qmc(shape, seed):
    m, s = shape
    u = sobol(s, m, seed).T.clamp(1e-6, 1 - 1e-6)  # [m, s]
    return torch.distributions.Normal(0.0, 1.0).icdf(u)


def gauss_hermite(k):
    import numpy as np

    t, w = np.polynomial.hermite_e.hermegauss(k)
    return torch.tensor(t), torch.tensor(w / w.sum())


def local_perturb(x, n, scale, gen):
    pts = x.unsqueeze(1) + scale * torch.randn(x.shape[0], n, x.shape[-1], generator=gen)
    return pts.reshape(-1, x.shape[-1]).clamp(0, 1)
