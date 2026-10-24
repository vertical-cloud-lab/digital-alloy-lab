"""Cost-aware Bayesian optimization of a synthetic copper/DED alloy function network.

Copper/DED version of `benchmarks/bofn-prelim/bofn_alloy.py` (the aluminum LPBF
network behind the MS&T26 preliminary results), built for the ONR YIP copper
proposal (issue 205). Same question: does choosing *which stage to run next*
(pKGFN, Buathong et al. ICML 2024) beat tiered screening and full-pipeline BO
when stages cost $10 to $3,100 each?

Design vector x (all scaled to [0, 1]; copper is the balance):
    x0 Ni  0-30 wt%        x4 a  ultrasonic atomizer setting
    x1 Al  0-9.5 wt%       x5 P  laser power (Utah's MX-Lab capped at 0.5)
    x2 Fe  0-4.5 wt%       x6 v  travel speed
    x3 Mn  0-4 wt%

Function network (one GP per node, outputs feed children), eight priced stages:
    C  CALPHAD + heat flow (c)              -> s strengthening potential, f solidification
                                               index, g nucleant fraction (Fe-rich kappa),
                                               h heat-flow (conductivity) index (added so the
                                               lack-of-fusion term is a function of node inputs)
    A  ultrasonic 0.5 kg lot (a, Mn, f)     -> q powder quality
    U  small DED, Utah (P<=0.5, v, f, g, h, q)      -> rho_u dense, crack-free index
    M  large DED, Mines (P, v, f, g, h, q, rho_u)   -> rho_m dense, crack-free fraction
    S  microscopy (Al, Ni, P, v, rho_m)     -> beta retained beta-prime index
    T  tensile (s, rho_m, beta)             -> U strength
    K  one-hour screen (Ni, Al, Fe, rho_m, beta)    -> w screen index
    I  30-day immersion (Ni, Al, Fe, rho_m, beta, w) -> m immersion index
    objective J = U * sigmoid((m - m_ref) / 0.05) - LAMBDA * B(c)
    B = 1.0 Ni + 0.3 Al + 0.2 Mn (known critical-mineral burden), m_ref = immersion
    index of dense 70-30 Cu-Ni (C71500) at its best settings.

`rho_u` is a model input of `rho_m` and `w` a model input of `m` so the GPs can learn
the small-step-to-large-step and screen-to-immersion transfers; the truth links each
pair only through shared parents (the truth ignores those two coordinates).

Two bias knobs: `kappa` (how much the Fe-rich kappa nucleant suppresses hot tearing,
which the Scheil crack index cannot see) and `eta` (how blind the one-hour screen is
to the selective attack of beta-prime that immersion finds, and to the slow-forming
film of low-nickel alloys). The constants below were tuned so the required properties
in README.md hold (checked by `check_truth.py`).
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
INI, IAL, IFE, IMN = 0, 1, 2, 3
P_CAP = 0.5  # Utah's MX-Lab laser power cap on the scaled axis (about 500 W of 1 kW)

# round all-in step costs (the project's own estimates; see README)
COSTS = {"C": 10.0, "A": 400.0, "U": 500.0, "M": 1500.0, "S": 100.0, "T": 200.0, "K": 50.0, "I": 400.0}
M_SCALE_UP = 1600.0  # the 2 kg scale-up lot, paid with the first Mines session on a lot
SESSIONS_PER_LOT = 4  # a scaled-up lot supports about four Mines sessions
M_FIRST = COSTS["M"] + M_SCALE_UP  # $3,100 for the first Mines session on a composition
FULL_COST = COSTS["C"] + COSTS["A"] + COSTS["U"] + M_FIRST + COSTS["S"] + COSTS["T"] + COSTS["K"] + COSTS["I"]  # $4,760
LAMBDA = 0.3
BURDEN_W = torch.tensor([1.0, 0.3, 0.0, 0.2])  # Ni, Al, Fe, Mn
GATE_SCALE = 0.05

# node -> (design dims, parent nodes); order is topological
SPEC = {
    "s": (COMP, []),
    "f": (COMP, []),
    "g": (COMP, []),
    "h": (COMP, []),
    "q": ([IA, IMN], ["f"]),
    "rho_u": (IPV, ["f", "g", "h", "q"]),
    "rho_m": (IPV, ["f", "g", "h", "q", "rho_u"]),
    "beta": ([IAL, INI] + IPV, ["rho_m"]),
    "U": ([], ["s", "rho_m", "beta"]),
    "w": ([INI, IAL, IFE], ["rho_m", "beta"]),
    "m": ([INI, IAL, IFE], ["rho_m", "beta", "w"]),
}
ORDER = list(SPEC)
GROUPS = {"C": ["s", "f", "g", "h"], "A": ["q"], "U": ["rho_u"], "M": ["rho_m"], "S": ["beta"], "T": ["U"], "K": ["w"], "I": ["m"]}
GROUP_OF = {n: g for g, ns in GROUPS.items() for n in ns}
STAGE_NAMES = {"C": "CALPHAD + heat flow", "A": "Atomize (0.5 kg)", "U": "Small DED (Utah)", "M": "Large DED (Mines)",
               "S": "Microscopy", "T": "Tensile", "K": "1-h screen", "I": "30-d immersion"}

# truth constants (tuned; see README "The truth functions and the optimum")
F_CRACK = 0.56  # crack onset on the effective solidification index
F_SAFE = 0.32  # the CALPHAD crack screen's threshold (conservative: 1% crack probability at kappa = 0)

# reference alloys (scaled levels): Ni, Al, Fe, Mn
REFERENCE = {
    "C71500 (70-30 Cu-Ni)": [1.0, 0.0, 0.15, 0.20],
    "C70600 (90-10 Cu-Ni)": [0.333, 0.0, 0.31, 0.20],
    "C95800 (NAB)": [0.15, 0.95, 0.90, 0.30],
}


def burden(x):
    """Critical-mineral burden of the composition (known, free to compute)."""
    return (x[..., :4] * BURDEN_W).sum(-1)


def transform(name, inp):
    """Per-node input transform: the Utah machine runs at min(P, P_CAP)."""
    if name == "rho_u":
        inp = inp.clone()
        inp[..., 0] = inp[..., 0].clamp(max=P_CAP)
    return inp


def sig(z):
    return torch.sigmoid(z)


# --------------------------------------------------------------------------- truth
class AlloyTruth:
    def __init__(self, kappa: float = 1.0, eta: float = 1.0, m_ref: float | None = None):
        self.kappa, self.eta = kappa, eta
        self.m_ref = M_REF if m_ref is None else m_ref

    def node(self, name, inp):
        """Evaluate one node on its own input vector (design dims + parent outputs)."""
        if name in ("s", "f", "g", "h"):
            ni, al, fe, mn = inp[..., 0], inp[..., 1], inp[..., 2], inp[..., 3]
            if name == "s":  # solid-solution Ni; kappa/beta from Al; the Ni-Al (kappa-III, NiAl) synergy
                return (1 - torch.exp(-(0.6 * ni + 0.9 * al + 3.0 * ni * al)) + 0.1 * fe + 0.05 * mn) / 1.15
            if name == "f":  # Cu-Ni wide, NAB narrow, the Ni-Al corner wide again (primary B2)
                return (0.65 * ni + 0.30 * mn - 0.35 * al + 2.5 * ni * al + 0.05 * fe).clamp(0, 1)
            if name == "g":  # Fe-rich primary kappa particles nucleate alpha and refine grains
                return (0.7 * fe.clamp(min=0) * (1 + 0.5 * al) + 0.15 * al * ni) / 1.2
            return 0.8 / (1 + 12 * ni + 4 * al + 2 * mn)  # h: conductivity index (drops steeply with the first few wt% of Ni or Al)
        if name == "q":
            a, mn, f = inp[..., 0], inp[..., 1], inp[..., 2]
            a_opt = 0.35 + 0.40 * f  # hotter melts need another setting; near the atomizer's limit the powder coarsens
            return torch.exp(-(((a - a_opt) / 0.28) ** 2)) * (1 - 0.35 * f**2) * (1 - 0.10 * mn)
        if name in ("rho_u", "rho_m"):
            P, v, f, g, h, q = (inp[..., i] for i in range(6))
            u = P - v - (0.05 + 0.25 * f)
            window = torch.exp(-((u / 0.2) ** 2)) * (1 - 0.35 * sig((P - 0.85) / 0.05))  # energy-density ridge, keyholing
            lof = sig((h - P) / 0.08)  # lack of fusion below a conductivity-set power threshold
            g = g.clamp(min=0)
            f_eff = f * (1 - self.kappa * 0.85 * g / (g + 0.12))
            crack = sig((f_eff - F_CRACK) / 0.05)
            rho = window * q.clamp(min=0) ** 0.3 * (1 - 0.75 * crack) * (1 - lof)
            if name == "rho_u":  # P already capped by `transform`; thin walls hide a little porosity
                rho = rho * (0.95 + 0.05 * q.clamp(min=0))
            return rho
        if name == "beta":
            al, ni, P, v = inp[..., 0], inp[..., 1], inp[..., 2], inp[..., 3]
            return al.clamp(min=0) ** 1.5 * (1 - 0.5 * ni) * sig((v - P + 0.2) / 0.15)  # retained beta-prime: Al, fast cooling
        if name == "U":
            s, rho_m, beta = inp[..., 0], inp[..., 1], inp[..., 2]
            return (0.25 + 0.75 * s) * rho_m * (1 + 0.15 * beta)
        if name in ("w", "m"):
            ni, al, fe, rho_m, beta = (inp[..., i] for i in range(5))
            film = 1 - torch.exp(-ni.clamp(min=0) / 0.15)  # the protective film saturates by 90-10
            fe_sol = 0.30 * fe.clamp(0, 0.4)  # iron in solution helps the film (why 90-10 carries 1.5% Fe)
            if name == "m":
                return (0.30 + 0.55 * film + 0.15 * al - 0.60 * al * beta + fe_sol - 0.15 * (fe - 0.5).clamp(min=0) - 0.30 * (1 - rho_m)).clamp(0, 1)
            # the one-hour screen: at eta = 1 it rates fresh films (Ni^0.7, Al's oxide) and is blind to beta-prime
            # attack and to slow-forming films; at eta = 0 it agrees with immersion up to its constants
            ni_term = self.eta * (0.4 * ni.clamp(min=0) ** 0.7 + 0.6 * film) + (1 - self.eta) * film
            return (0.35 + 0.50 * ni_term + 0.25 * al - 0.10 * (1 - rho_m) - (1 - self.eta) * (0.60 * al * beta - fe_sol)).clamp(0, 1)
        raise KeyError(name)

    def full(self, x):
        """All node outputs for designs x [..., D]."""
        out = {}
        for n in ORDER:
            inp = node_input(n, x, out)
            out[n] = self.node(n, inp)
        return out

    def objective(self, x, full=None):
        out = full or self.full(x)
        return objective_from(out["U"], out["m"], x, self.m_ref)


def objective_from(U, m, x, m_ref):
    return U * sig((m - m_ref) / GATE_SCALE) - LAMBDA * burden(x)


def _reference_m(kappa=1.0, eta=1.0):
    """Immersion index of C71500 deposited dense at its best (a, P, v), from the truth."""
    t = AlloyTruth(kappa, eta, m_ref=0.0)
    c = torch.tensor(REFERENCE["C71500 (70-30 Cu-Ni)"])
    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=0).draw(16384).double()
    X = torch.cat([c.expand(apv.shape[0], 4), apv], -1)
    out = t.full(X)
    j = out["rho_m"].argmax()
    return float(out["m"][j]), float(out["rho_m"][j]), X[j]




# --------------------------------------------------------------------------- GP
FIT_LOG = {"calls": 0, "failures": 0}  # per process; policies.run() resets it and stores it in the run JSON


class TinyGP:
    """Exact GP with BoTorch-fitted RBF hyperparameters and cheap batched posteriors."""

    def __init__(self, X, y, noise=1e-6):
        n, d = X.shape
        self.X, self.y = X, y
        self.ym = y.mean()
        # node outputs live on [0, 1]: keep a physical prior scale even when early
        # observations are all alike (e.g. every seed build cracked)
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

    def mean_raw(self, U):
        m, _ = self.post_std(U)
        return m * self.ys + self.ym

    def cov_std(self, U, VU, Z, VZ):
        """Posterior covariance between U [..., d] and candidates Z [b, d] -> [..., b]."""
        return self._k(U / self.ls, Z / self.ls) - VU @ VZ.T


def node_input(name, x, vals):
    """Input vector of `name` at designs x [..., D] given parent values; applies the node's transform."""
    dims, parents = SPEC[name]
    shape = torch.broadcast_shapes(*[vals[p].shape for p in parents]) if parents else x[..., 0].shape
    xs = x[..., dims].expand(*shape, len(dims)) if dims else None
    parts = ([xs] if xs is not None else []) + [vals[p].expand(shape).unsqueeze(-1) for p in parents]
    return transform(name, torch.cat(parts, -1))


M_REF, RHO_REF, X_REF = _reference_m()  # fixed across cells: a property of dense 70-30 Cu-Ni in the headline world


# --------------------------------------------------------------------------- data
class Data:
    """Per-node observations plus the physical inventory (powder lots, builds)."""

    def __init__(self):
        self.obs = {n: ([], []) for n in ORDER}
        self.calphad = {}  # composition tuple -> dict(s, f, g, h)
        self.lots = []  # dict(c, a, q, sessions_left, utah=[(P_u, v, rho_u)])
        self.builds = []  # dict(lot, pv, rho_u_in, rho_m, beta, U, w, m, J)
        self.full = []  # (x, objective) fully validated designs (tensile + immersion)
        self.spent = 0.0
        self.log = []  # (group, spent after)
        self.events = []  # audit trail: dict(kind, ...)

    def add(self, name, inp, val):
        self.obs[name][0].append(inp.detach().clone())
        self.obs[name][1].append(float(val))

    def tensors(self, name):
        X, y = self.obs[name]
        return torch.stack(X), torch.tensor(y)


def comp_key(c):
    return tuple(round(float(v), 6) for v in c)


class Lab:
    """Runs stages against the truth, enforcing upstream requirements and costs."""

    def __init__(self, truth: AlloyTruth, data: Data):
        self.t, self.d = truth, data
        self.net = None  # the policy's current network model, used to estimate rho_u for a Mines run without a matching Utah run

    def _pay(self, group, amount=None):
        self.d.spent += COSTS[group] if amount is None else amount
        self.d.log.append((group, self.d.spent))

    def calphad(self, c):
        key = comp_key(c)
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
        inp = torch.tensor([float(a), float(c[IMN]), cal["f"]])  # node q input order: (a, Mn, f)
        q = float(self.t.node("q", inp))
        self.d.add("q", inp, q)
        self.d.lots.append({"c": c.clone(), "a": float(a), "q": q, "sessions_left": 0, "utah": []})
        self._pay("A")
        return len(self.d.lots) - 1

    def _lot_inputs(self, lot):
        L = self.d.lots[lot]
        cal = self.calphad(L["c"])
        return L, cal

    def utah(self, lot, pv):
        L, cal = self._lot_inputs(lot)
        pv = [float(v) for v in pv]
        inp = transform("rho_u", torch.tensor(pv + [cal["f"], cal["g"], cal["h"], L["q"]]))
        rho_u = float(self.t.node("rho_u", inp))
        self.d.add("rho_u", inp, rho_u)
        L["utah"].append((float(inp[0]), pv[1], rho_u))
        self._pay("U")
        return rho_u

    def estimate_rho_u(self, lot, pv):
        """What the lab believes the small step would read at these settings: the measured value if
        Utah ran this lot at exactly these (capped) settings, else the current model's posterior mean."""
        L, cal = self._lot_inputs(lot)
        inp = transform("rho_u", torch.tensor([float(pv[0]), float(pv[1]), cal["f"], cal["g"], cal["h"], L["q"]]))
        for Pu, v, r in L["utah"]:
            if abs(Pu - float(inp[0])) < 1e-9 and abs(v - float(inp[1])) < 1e-9:
                return r
        if self.net is not None:
            return float(self.net.gp["rho_u"].mean_raw(inp.unsqueeze(0))[0])
        return float(sum(r for _, _, r in L["utah"]) / len(L["utah"])) if L["utah"] else 0.5

    def mines_cost(self, lot):
        return COSTS["M"] if self.d.lots[lot]["sessions_left"] > 0 else M_FIRST

    def mines(self, lot, pv, rho_u_in=None):
        L, cal = self._lot_inputs(lot)
        pv = [float(v) for v in pv]
        if rho_u_in is None:
            rho_u_in = self.estimate_rho_u(lot, pv)
        inp = torch.tensor(pv + [cal["f"], cal["g"], cal["h"], L["q"], float(rho_u_in)])
        rho_m = float(self.t.node("rho_m", inp))
        self.d.add("rho_m", inp, rho_m)
        cost = self.mines_cost(lot)
        if L["sessions_left"] == 0:
            L["sessions_left"] = SESSIONS_PER_LOT
        L["sessions_left"] -= 1
        self.d.builds.append({"lot": lot, "pv": pv, "rho_u_in": float(rho_u_in), "rho_m": rho_m, "beta": None, "U": None, "w": None, "m": None, "J": None})
        self._pay("M", cost)
        return len(self.d.builds) - 1

    def _build(self, build):
        B = self.d.builds[build]
        L, cal = self._lot_inputs(B["lot"])
        return B, L, cal

    def microscopy(self, build):
        B, L, cal = self._build(build)
        inp = torch.tensor([float(L["c"][IAL]), float(L["c"][INI]), B["pv"][0], B["pv"][1], B["rho_m"]])
        beta = float(self.t.node("beta", inp))
        self.d.add("beta", inp, beta)
        B["beta"] = beta
        self._pay("S")
        return beta

    def tensile(self, build):
        B, L, cal = self._build(build)
        assert B["beta"] is not None, "microscopy comes before tensile"
        inp = torch.tensor([cal["s"], B["rho_m"], B["beta"]])
        U = float(self.t.node("U", inp))
        self.d.add("U", inp, U)
        B["U"] = U
        self._pay("T")
        self._maybe_full(build)
        return U

    def screen(self, build):
        B, L, cal = self._build(build)
        assert B["beta"] is not None, "microscopy comes before the screen"
        inp = torch.tensor([float(L["c"][INI]), float(L["c"][IAL]), float(L["c"][IFE]), B["rho_m"], B["beta"]])
        w = float(self.t.node("w", inp))
        self.d.add("w", inp, w)
        B["w"] = w
        self._pay("K")
        return w

    def immersion(self, build):
        B, L, cal = self._build(build)
        assert B["w"] is not None, "the screen comes before immersion"
        inp = torch.tensor([float(L["c"][INI]), float(L["c"][IAL]), float(L["c"][IFE]), B["rho_m"], B["beta"], B["w"]])
        m = float(self.t.node("m", inp))
        self.d.add("m", inp, m)
        B["m"] = m
        self._pay("I")
        self._maybe_full(build)
        return m

    def _maybe_full(self, build):
        B = self.d.builds[build]
        if B["U"] is not None and B["m"] is not None and B["J"] is None:
            x = design_of_build(self.d, build)
            B["J"] = float(objective_from(torch.tensor(B["U"]), torch.tensor(B["m"]), x, self.t.m_ref))
            self.d.full.append((x, B["J"]))

    def full_eval(self, x, utah=True):
        """Every stage on one design (the full-pipeline policies)."""
        lot = self.atomize(x[COMP], x[IA])
        if utah:
            self.utah(lot, x[IPV])
        b = self.mines(lot, x[IPV])
        self.microscopy(b)
        self.tensile(b)
        self.screen(b)
        self.immersion(b)
        return b


def design_of_build(d: Data, j):
    B = d.builds[j]
    L = d.lots[B["lot"]]
    return torch.cat([L["c"], torch.tensor([L["a"]] + B["pv"])])


# --------------------------------------------------------------------------- network model
class Network:
    def __init__(self, data: Data, m_ref: float | None = None):
        self.m_ref = M_REF if m_ref is None else m_ref
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
        return vals["U"] * sig((vals["m"] - self.m_ref) / GATE_SCALE) - LAMBDA * burden(x).unsqueeze(-1)

    def mean(self, x, eps):
        return self.samples(x, eps).mean(-1)

    def kg(self, group, Z, Xi, eps, w, ww, chunk=4):
        """pKGFN value of evaluating `group` at candidate node inputs Z [b, d] (Buathong et al. 2024).

        Discrete inner max over the shared, incumbent-anchored design set Xi [m, D];
        fantasies w [nf, r] with weights ww [nf]; common random numbers eps.
        """
        nodes = GROUPS[group]
        out = []
        m_, S_ = Xi.shape[0], eps[ORDER[0]].shape[-1]
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
            obj = vals["U"] * sig((vals["m"] - self.m_ref) / GATE_SCALE) - LAMBDA * burden(Xi).unsqueeze(-1)
            if obj.dim() == 2:  # the fantasized node does not reach the objective (cannot happen: every node is upstream of U or m)
                obj = obj.expand(b, w.shape[0], m_, S_)
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
