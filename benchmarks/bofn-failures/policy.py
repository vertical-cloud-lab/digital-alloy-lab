"""Failure-aware BOFN on the aluminum and copper networks (issue #274).

One campaign = the source benchmark's best policy, BOFN with lot reuse (`eifn_reuse`: network
expected improvement per dollar over new designs and new prints/sessions on existing powder
lots), run against a truth in which stages can fail (`failmodel.py`). The strategies differ only
in what they do with a failed run, named for the Ax behaviour each mimics:

    drop            every failed run FAILED (Ax <= 1.2.3's complete_trial with a missing metric):
                    none of the run's data is fit, and the design may be suggested again.
    abandon         every failed run ABANDONED: none of its data is fit, and its design stays
                    pending for good (kriging believer at the posterior mean).
    partial         Ax >= 1.2.4: the run is COMPLETED with the metrics it has. Its completed
                    stages are fit; the design stays pending for the metrics it lacks.
    impute          "soft pushing": a failure labelled input-caused is recorded as the worst value
                    seen so far at the failed stage's output; a transient one is dropped.
    viab_x          Ax >= 1.3 with AddExecutionViability: transient -> FAILED, input-caused ->
                    ABANDONED (not fit, pending), and a GP on 0/1 labels over the design x
                    constrains P(viable) >= 0.8 once 3 runs are abandoned.
    viab_x_partial  as viab_x, plus fit_abandoned=True, which makes Ax fit the completed stages of
                    every run, FAILED and ABANDONED alike; an abandoned design stays pending for what
                    it lacks, and a FAILED run with data counts as viable (Ax labels every
                    non-ABANDONED training row 1). The best an Ax user can do today.
    keep            the completed stages are fit and nothing is pending: what Ax >= 1.2.4 does in
                    practice below 100 trials when a partly measured arm has any objective or
                    constraint metric (X_pending is the intersection over those metrics).
    viab_node       node-level ledger (the note's proposal): every completed stage is fit, nothing is
                    pending, and each stage with input-labelled failures gets a GP on 0/1 labels over
                    that stage's own inputs (design variables and parent outputs). An MC sample of the
                    network counts as an improvement only if every blocking stage on its path is
                    viable (0.8 bound, 3-failure trigger, as in Ax).
    viab_node_ec    viab_node, plus failures priced into the acquisition: EI times the chance of no
                    transient fault (per-stage rates from the ledger, Beta(1, 9) prior), divided by
                    the expected cost of a chain that stops at its first blocking failure.

`run(..., reuse=False)` is the full-pipeline policy (the source `eifn`): every decision is a new
design taken through every stage.

A run is "blocked" when a failure stops it before the objective is measured; the copper small-DED
step (Utah) is a side screen, so its failure doesn't block. CALPHAD is a simulation that never
fails, and its outputs are always kept. The shared seed data (CALPHAD on 32 compositions and five
full runs) is failure-free and sunk, exactly as in the source benchmarks; with the `nofail`
scenario every strategy reproduces the source `eifn_reuse` run action for action.
"""

from __future__ import annotations

import math
import time

import torch
from botorch.fit import fit_gpytorch_mll
from botorch.models import SingleTaskGP
from gpytorch.mlls import ExactMarginalLogLikelihood

from failmodel import Q_MIN, FailureModel

torch.set_default_dtype(torch.double)

STRATEGIES = ("drop", "abandon", "partial", "keep", "impute", "viab_x", "viab_x_partial", "viab_node", "viab_node_ec")
NODE_LEVEL = ("viab_node", "viab_node_ec")
VIABLE_BOUND = 0.8  # AddExecutionViability's feasibility threshold
MIN_ZEROS = 3  # its trigger: at least this many abandoned (input-labelled) runs
ETA = 1e-3  # BoTorch's default temperature for the sigmoid on outcome constraints
S_MC = 64
NEAR = 0.1  # an input-caused failure this close (in scaled x) to an earlier one counts as a repeat


# --------------------------------------------------------------------------- GP helpers
def condition_tinygp(gp, Xe, ye):
    """The vendored TinyGP conditioned on extra points, hyperparameters unchanged (kriging believer)."""
    new = object.__new__(type(gp))
    new.__dict__.update(gp.__dict__)
    X = torch.cat([gp.X, Xe])
    y = torch.cat([gp.y, ye])
    new.X, new.y = X, y
    new.Xs = X / gp.ls
    n = X.shape[0]
    K = gp._k(new.Xs, new.Xs)
    for jitter in (1e-8, 1e-6, 1e-4):
        try:
            L = torch.linalg.cholesky(K + (gp.noise + jitter) * torch.eye(n))
            break
        except RuntimeError:
            continue
    new.Linv = torch.linalg.solve_triangular(L, torch.eye(n), upper=False)
    Y = (y - gp.ym) / gp.ys
    new.alpha = new.Linv.T @ (new.Linv @ (Y - gp.const))
    return new


class ViabGP:
    """GP regression on 0/1 viability labels with a fitted noise level (what Ax fits for its
    viability metric), with cheap batched latent posteriors."""

    def __init__(self, Z, y):
        self.Z, self.y = Z, y
        self.ym = y.mean()
        self.ys = y.std().clamp_min(0.2)
        Y = ((y - self.ym) / self.ys).unsqueeze(-1)
        model = SingleTaskGP(Z, Y, outcome_transform=None)
        try:
            fit_gpytorch_mll(ExactMarginalLogLikelihood(model.likelihood, model))
        except Exception:
            pass
        self.ls = model.covar_module.lengthscale.detach().reshape(-1)
        self.const = model.mean_module.constant.detach().reshape(())
        self.noise = float(model.likelihood.noise.detach().reshape(-1)[0])
        self.Zs = Z / self.ls
        n = Z.shape[0]
        K = self._k(self.Zs, self.Zs) + (self.noise + 1e-8) * torch.eye(n)
        L = torch.linalg.cholesky(K)
        self.Linv = torch.linalg.solve_triangular(L, torch.eye(n), upper=False)
        self.alpha = self.Linv.T @ (self.Linv @ (Y.squeeze(-1) - self.const))

    @staticmethod
    def _k(A, B):
        d2 = (A * A).sum(-1, keepdim=True) - 2 * A @ B.T + (B * B).sum(-1)
        return torch.exp(-0.5 * d2.clamp_min(0))

    def sample(self, U, eps):
        """Latent samples in label units at inputs U [..., d] with base samples eps [...]."""
        Kx = self._k(U / self.ls, self.Zs)
        mean = self.const + Kx @ self.alpha
        V = Kx @ self.Linv.T
        var = (1.0 - (V * V).sum(-1)).clamp_min(1e-12)
        return (mean + var.sqrt() * eps) * self.ys + self.ym

    def prob(self, U):
        """P(latent >= VIABLE_BOUND) at inputs U [n, d] (for reporting)."""
        Kx = self._k(U / self.ls, self.Zs)
        mean = (self.const + Kx @ self.alpha) * self.ys + self.ym
        V = Kx @ self.Linv.T
        sd = (1.0 - (V * V).sum(-1)).clamp_min(1e-12).sqrt() * self.ys
        return torch.distributions.Normal(0.0, 1.0).cdf((mean - VIABLE_BOUND) / sd)


# --------------------------------------------------------------------------- lab with failures
class FailLab:
    """Runs stages through the vendored Lab, letting the failure model veto them, and keeps the
    node-level ledger. Observations of completed stages land in the vendored `Data.obs` as usual;
    ledger rows point at them, and each strategy decides which to fit."""

    def __init__(self, net, truth, d, lab, fm: FailureModel):
        self.net, self.truth, self.d, self.lab, self.fm = net, truth, d, lab, fm
        self.BA = net.BA
        self.cu = net.family == "cu"
        self.rows = []  # ledger: one dict per stage attempt
        self.trials = []  # one dict per decision (a chain of stages)
        self.unprintable = set()  # lots with too little usable powder (the lab measured q)
        self.n_seed = {n: len(d.obs[n][1]) for n in net.ORDER}

    # ---- bookkeeping
    def _snap(self):
        return {n: len(self.d.obs[n][1]) for n in self.net.ORDER}

    def _row(self, trial, stage, status, z=None, kind=None, label=None, cost=0.0, before=None, nodes=(), precondition=False):
        obs = []
        if before is not None:
            for n in nodes:
                obs += [(n, i) for i in range(before[n], len(self.d.obs[n][1]))]
        r = dict(trial=trial["id"], stage=stage, status=status, z=None if z is None else z.detach().clone(), kind=kind, label=label,
                 cost=cost, obs=obs, precondition=precondition)
        self.rows.append(r)
        trial["rows"].append(len(self.rows) - 1)
        if status == "FAILED" and stage in self.blocking_stages():
            trial["blocked"] = dict(stage=stage, kind=kind, label=label, precondition=precondition)
        return r

    def blocking_stages(self):
        return ("A", "M", "S", "T", "K", "I") if self.cu else ("A", "L", "T")

    def _pay(self, group, amount=None):
        before = self.d.spent
        self.lab._pay(group, amount) if self.cu else self.lab._pay(group)
        return self.d.spent - before

    def _calphad(self, c):
        return self.lab.calphad(c)

    def new_trial(self, x, kind, lot=None):
        t = dict(id=len(self.trials), x=x.detach().clone(), kind=kind, lot=lot, rows=[], blocked=None, complete=False, spent0=self.d.spent)
        self.trials.append(t)
        return t

    # ---- stages
    def atomize(self, t, c, a):
        self._calphad(c)
        status, kind, label = self.fm.attempt("A", {})
        cal = self.d.calphad[self.BA.comp_key(c)] if self.cu else self.lab.calphad(c)
        z = torch.tensor([float(a), float(c[3]), cal["f"]]) if self.cu else torch.tensor([float(a), cal["g"]])
        if status == "FAILED":
            cost = self._pay("A")
            self._row(t, "A", "FAILED", z=z, kind=kind, label=label, cost=cost)
            return None
        before = self._snap()
        s0 = self.d.spent
        lot = self.lab.atomize(c, a)
        self._row(t, "A", "COMPLETED", z=z, cost=self.d.spent - s0, before=before, nodes=["q"])
        if self.fm.inputs_on and self.d.lots[lot]["q"] < Q_MIN:
            self.unprintable.add(lot)
        t["lot"] = lot
        return lot

    def _precondition_fail(self, t, stage, z):
        self._row(t, stage, "FAILED", z=z, kind="input", label="input", cost=0.0, precondition=True)

    def print_al(self, t, lot, pv):
        L = self.d.lots[lot]
        cal = self.lab.calphad(L["c"])
        pv = [float(v) for v in pv]
        z = torch.tensor(pv + [cal["f"], cal["g"], L["q"]])  # the rho node's input
        if lot in self.unprintable:
            self._precondition_fail(t, "L", z)
            return None
        status, kind, label = self.fm.attempt("L", dict(P=pv[0], v=pv[1], f=cal["f"], g=cal["g"]))
        if status == "FAILED":
            cost = self._pay("L")
            self._row(t, "L", "FAILED", z=z, kind=kind, label=label, cost=cost)
            return None
        before = self._snap()
        s0 = self.d.spent
        b = self.lab.print_(lot, pv)
        self._row(t, "L", "COMPLETED", z=z, cost=self.d.spent - s0, before=before, nodes=["rho"])
        return b

    def tensile_al(self, t, b):
        B = self.d.builds[b]
        cal = self.lab.calphad(self.d.lots[B["lot"]]["c"])
        z = torch.tensor([cal["s"], B["rho"]])
        status, kind, label = self.fm.attempt("T", {})
        if status == "FAILED":
            cost = self._pay("T")
            self._row(t, "T", "FAILED", z=z, kind=kind, label=label, cost=cost)
            return False
        before = self._snap()
        s0 = self.d.spent
        self.lab.tensile(b)
        self._row(t, "T", "COMPLETED", z=z, cost=self.d.spent - s0, before=before, nodes=["U"])
        return True

    def utah(self, t, lot, pv):
        L, cal = self.lab._lot_inputs(lot)
        pv = [float(v) for v in pv]
        z = self.BA.transform("rho_u", torch.tensor(pv + [cal["f"], cal["g"], cal["h"], L["q"]]))
        if lot in self.unprintable:
            self._precondition_fail(t, "U", z)
            return None
        status, kind, label = self.fm.attempt("U", dict(P=pv[0], v=pv[1], f=cal["f"], g=cal["g"], h=cal["h"]))
        if status == "FAILED":
            cost = self._pay("U")
            self._row(t, "U", "FAILED", z=z, kind=kind, label=label, cost=cost)
            return None
        before = self._snap()
        s0 = self.d.spent
        r = self.lab.utah(lot, pv)
        self._row(t, "U", "COMPLETED", z=z, cost=self.d.spent - s0, before=before, nodes=["rho_u"])
        return r

    def mines(self, t, lot, pv):
        L, cal = self.lab._lot_inputs(lot)
        pv = [float(v) for v in pv]
        rho_u_in = self.lab.estimate_rho_u(lot, pv)
        z = torch.tensor(pv + [cal["f"], cal["g"], cal["h"], L["q"], float(rho_u_in)])  # the rho_m node's input
        if lot in self.unprintable:
            self._precondition_fail(t, "M", z)
            return None
        status, kind, label = self.fm.attempt("M", dict(P=pv[0], v=pv[1], f=cal["f"], g=cal["g"], h=cal["h"]))
        if status == "FAILED":
            cost = self.lab.mines_cost(lot)  # a failed session still uses the session (and the first one's scale-up)
            if L["sessions_left"] == 0:
                L["sessions_left"] = self.BA.SESSIONS_PER_LOT
            L["sessions_left"] -= 1
            paid = self._pay("M", cost)
            self._row(t, "M", "FAILED", z=z, kind=kind, label=label, cost=paid)
            return None
        before = self._snap()
        s0 = self.d.spent
        b = self.lab.mines(lot, pv, rho_u_in=rho_u_in)
        self._row(t, "M", "COMPLETED", z=z, cost=self.d.spent - s0, before=before, nodes=["rho_m"])
        return b

    def _simple_cu(self, t, stage, fn, b, node, zfun):
        z = zfun(b)
        status, kind, label = self.fm.attempt(stage, {})
        if status == "FAILED":
            cost = self._pay(stage)
            self._row(t, stage, "FAILED", z=z, kind=kind, label=label, cost=cost)
            return False
        before = self._snap()
        s0 = self.d.spent
        fn(b)
        self._row(t, stage, "COMPLETED", z=z, cost=self.d.spent - s0, before=before, nodes=[node])
        return True

    def tests_cu(self, t, b):
        """Microscopy, tensile, the one-hour screen and 30-day immersion on a Mines build."""
        BA, d = self.BA, self.d

        def zb(b_):
            B = d.builds[b_]
            c = d.lots[B["lot"]]["c"]
            return torch.tensor([float(c[BA.IAL]), float(c[BA.INI]), B["pv"][0], B["pv"][1], B["rho_m"]])

        def zt(b_):
            B = d.builds[b_]
            cal = self.lab.calphad(d.lots[B["lot"]]["c"])
            return torch.tensor([cal["s"], B["rho_m"], B["beta"]])

        def zw(b_):
            B = d.builds[b_]
            c = d.lots[B["lot"]]["c"]
            return torch.tensor([float(c[BA.INI]), float(c[BA.IAL]), float(c[BA.IFE]), B["rho_m"], B["beta"]])

        def zm(b_):
            B = d.builds[b_]
            c = d.lots[B["lot"]]["c"]
            return torch.tensor([float(c[BA.INI]), float(c[BA.IAL]), float(c[BA.IFE]), B["rho_m"], B["beta"], B["w"]])

        if not self._simple_cu(t, "S", self.lab.microscopy, b, "beta", zb):
            return False
        if not self._simple_cu(t, "T", self.lab.tensile, b, "U", zt):
            return False
        if not self._simple_cu(t, "K", self.lab.screen, b, "w", zw):
            return False
        return self._simple_cu(t, "I", self.lab.immersion, b, "m", zm)

    # ---- chains
    def run_new(self, x):
        net = self.net
        t = self.new_trial(x, "new")
        lot = self.atomize(t, x[net.COMP], x[net.IA])
        if lot is not None:
            if self.cu:
                self.utah(t, lot, x[net.IPV])  # a side screen: its failure doesn't stop the chain
                b = self.mines(t, lot, x[net.IPV])
                if b is not None:
                    t["complete"] = self.tests_cu(t, b)
            else:
                b = self.print_al(t, lot, x[net.IPV])
                if b is not None:
                    t["complete"] = self.tensile_al(t, b)
        t["cost"] = self.d.spent - t["spent0"]
        return t

    def run_reuse(self, x, lot):
        t = self.new_trial(x, "reuse", lot)
        pv = x[self.net.IPV]
        if self.cu:
            b = self.mines(t, lot, pv)
            if b is not None:
                t["complete"] = self.tests_cu(t, b)
        else:
            b = self.print_al(t, lot, pv)
            if b is not None:
                t["complete"] = self.tensile_al(t, b)
        t["cost"] = self.d.spent - t["spent0"]
        return t


# --------------------------------------------------------------------------- strategy data rules
GATE_NODE = {"al": {"A": "q", "L": "rho"}, "cu": {"A": "q", "U": "rho_u", "M": "rho_m"}}
GATED = {"al": {"new": ("A", "L"), "reuse": ("L",)}, "cu": {"new": ("A", "M"), "reuse": ("M",)}}


class DataView:
    """What one strategy fits: `tensors(node)` like the vendored Data, built from the ledger."""

    def __init__(self, fl: FailLab, strategy: str):
        self.fl, self.strategy = fl, strategy
        net, d = fl.net, fl.d
        calphad_nodes = set(net.GROUPS["C"])
        keep = {n: set(range(fl.n_seed[n])) for n in net.ORDER}
        for n in calphad_nodes:  # CALPHAD is a simulation: every result is kept, whatever happened downstream
            keep[n] = set(range(len(d.obs[n][1])))
        self.imputed = {n: ([], []) for n in net.ORDER}
        self.pending = []  # (design x, nodes pending)
        self.vx = ([], [])  # viability over x: (designs, labels)
        stage_nodes = {r_stage: n for r_stage, n in GATE_NODE[net.family].items()}
        for t in fl.trials:
            rows = [fl.rows[i] for i in t["rows"]]
            blk = t["blocked"]
            observed = {n for r in rows for n, _ in r["obs"]}
            # fit_abandoned=True makes Ax fit every status, FAILED included, so viab_x_partial keeps everything
            discard = blk is not None and strategy in ("drop", "abandon", "viab_x")
            if not discard:
                for r in rows:
                    for n, i in r["obs"]:
                        keep[n].add(i)
            if blk is None:
                continue
            missing = [n for n in net.ORDER if n not in calphad_nodes and n not in observed]
            if strategy == "abandon":
                self.pending.append((t["x"], [n for n in net.ORDER if n not in calphad_nodes]))
            elif strategy == "partial":
                self.pending.append((t["x"], missing))
            elif strategy == "viab_x" and blk["label"] == "input":
                self.pending.append((t["x"], [n for n in net.ORDER if n not in calphad_nodes]))
            elif strategy == "viab_x_partial" and blk["label"] == "input":
                self.pending.append((t["x"], missing))
            if strategy in ("viab_x", "viab_x_partial") and blk["label"] == "input":
                self.vx[0].append(t["x"])
                self.vx[1].append(0.0)
            elif strategy == "viab_x_partial" and observed - calphad_nodes:
                # AddExecutionViability labels every non-ABANDONED row of the training data 1, and with
                # fit_abandoned=True a FAILED run's completed stages are in the training data
                self.vx[0].append(t["x"])
                self.vx[1].append(1.0)
        if strategy == "impute":
            # every input-labelled failed stage (blocking or not): its output at its inputs = worst seen
            for r in fl.rows:
                if r["status"] == "FAILED" and r["label"] == "input" and r["stage"] in stage_nodes:
                    n = stage_nodes[r["stage"]]
                    self.imputed[n][0].append(r["z"])
        self.keep = keep
        for n in net.ORDER:
            if self.imputed[n][0]:
                yk = torch.tensor([d.obs[n][1][i] for i in sorted(keep[n])])
                worst = float(yk.min())
                self.imputed[n] = (self.imputed[n][0], [worst] * len(self.imputed[n][0]))
        # viability over x: every completed run (seed runs included) is a 1
        if strategy in ("viab_x", "viab_x_partial"):
            for x, _ in d.full:
                self.vx[0].append(x)
                self.vx[1].append(1.0)
        # node-level viability: every completed attempt of a stage is a 1, every input-labelled failure a 0
        self.vnode = {}
        if strategy in NODE_LEVEL:
            for st, n in stage_nodes.items():
                Z = [d.obs[n][0][i] for i in range(len(d.obs[n][1]))]
                y = [1.0] * len(Z)
                zeros = [r["z"] for r in fl.rows if r["stage"] == st and r["status"] == "FAILED" and r["label"] == "input"]
                self.vnode[st] = (Z + zeros, y + [0.0] * len(zeros))

    def tensors(self, n):
        X, y = self.fl.d.obs[n]
        idx = sorted(self.keep[n])
        Xs = [X[i] for i in idx] + list(self.imputed[n][0])
        ys = [y[i] for i in idx] + list(self.imputed[n][1])
        return torch.stack(Xs), torch.tensor(ys)


def fit_viability(Z, y):
    y = torch.tensor(y)
    if int((y == 0).sum()) < MIN_ZEROS or int((y == 1).sum()) < 1:
        return None
    return ViabGP(torch.stack(list(Z)), y)


class Model:
    """The strategy's network (vendored Network on its DataView), pending points and viability GPs."""

    def __init__(self, fl: FailLab, strategy: str):
        self.fl, self.strategy = fl, strategy
        net = fl.net
        self.view = DataView(fl, strategy)
        self.network = net.BA.Network(self.view)
        self.n_pending = len(self.view.pending)
        if self.view.pending:
            self._condition_pending()
        self.vx = fit_viability(*self.view.vx) if strategy in ("viab_x", "viab_x_partial") else None
        self.vnode = {}
        if strategy in NODE_LEVEL:
            for st, (Z, y) in self.view.vnode.items():
                gp = fit_viability(Z, y)
                if gp is not None:
                    self.vnode[st] = gp

    def _mean_path(self, X):
        """Posterior-mean node values and node inputs along the network at designs X [p, D]."""
        BA, net = self.fl.BA, self.fl.net
        vals, inps = {}, {}
        for n in net.ORDER:
            dims, parents = net.SPEC[n]
            if parents:
                inp = BA.node_input(n, X, vals)
            else:
                inp = X[..., dims]
                if hasattr(BA, "transform"):
                    inp = BA.transform(n, inp)
            gp = self.network.gp[n]
            m, _ = gp.post_std(inp)
            vals[n] = m * gp.ys + gp.ym
            inps[n] = inp
        return vals, inps

    def _condition_pending(self):
        net = self.fl.net
        Xp = torch.stack([x for x, _ in self.view.pending])
        vals, inps = self._mean_path(Xp)
        for n in net.ORDER:
            rows = [i for i, (_, nodes) in enumerate(self.view.pending) if n in nodes]
            if rows:
                idx = torch.tensor(rows)
                self.network.gp[n] = condition_tinygp(self.network.gp[n], inps[n][idx], vals[n][idx])


def node_samples(fl: FailLab, network, x, eps):
    """The vendored Network.samples, also returning every node's samples: [m, S] each."""
    BA, net = fl.BA, fl.net
    vals = {}
    xe = x.unsqueeze(-2)
    for n in net.ORDER:
        inp = BA.node_input(n, xe, vals) if net.SPEC[n][1] else x[..., net.SPEC[n][0]].unsqueeze(-2)
        vals[n] = network._sample(n, inp, eps[n])
    if fl.cu:
        obj = vals["U"] * BA.sig((vals["m"] - network.m_ref) / BA.GATE_SCALE) - BA.LAMBDA * BA.burden(x).unsqueeze(-1)
    else:
        obj = vals["U"] - BA.LAMBDA * BA.burden(x).unsqueeze(-1)
    return vals, obj


def gated_ei(fl: FailLab, model: Model, P, is_new, eps, best, it, chunk=8192, want_gates=False):
    """Network EI with the strategy's viability gates; is_new [m] marks new-design chains.
    With want_gates, also return each gated stage's mean gate per candidate (its P(viable))."""
    BA, net = fl.BA, fl.net
    out = []
    gmean = {}
    for i0 in range(0, P.shape[0], chunk):
        x = P[i0 : i0 + chunk]
        nw = is_new[i0 : i0 + chunk]
        e = {n: v[i0 : i0 + chunk] for n, v in eps.items()}
        vals, obj = node_samples(fl, model.network, x, e)
        w = torch.ones_like(obj)
        if model.vx is not None:
            v = model.vx.sample(x.unsqueeze(-2), e["_vx"])
            w = w * torch.sigmoid((v - VIABLE_BOUND) / ETA)
        if model.vnode:
            xe = x.unsqueeze(-2)
            for st, gp in model.vnode.items():
                node = GATE_NODE[net.family][st]
                if node == "q":
                    dims, parents = net.SPEC["q"]
                    z = BA.node_input("q", xe, vals) if parents else x[..., dims].unsqueeze(-2)
                    z = z.expand(-1, obj.shape[-1], -1) if z.shape[-2] == 1 else z
                else:
                    z = BA.node_input(node, xe, vals)
                v = gp.sample(z, e["_v" + st])
                gate = torch.sigmoid((v - VIABLE_BOUND) / ETA)
                if st == "A":  # only a new design is atomized; a reprint uses an existing lot
                    gate = torch.where(nw.unsqueeze(-1), gate, torch.ones_like(gate))
                if st in GATED[net.family]["new"] or st in GATED[net.family]["reuse"]:
                    w = w * gate
                    gmean.setdefault(st, []).append(gate.mean(-1))
        out.append(((obj - best).clamp_min(0) * w).mean(-1))
    if want_gates:
        return torch.cat(out), {st: torch.cat(v) for st, v in gmean.items()}
    return torch.cat(out)


def transient_rates(fl: FailLab):
    """Per-stage transient failure rate from the ledger: Beta(1, 9) prior (mean 0.1), labels as recorded."""
    out = {}
    for st in "AULMSTKI":
        n = sum(1 for r in fl.rows if r["stage"] == st and not r["precondition"])
        k = sum(1 for r in fl.rows if r["stage"] == st and r["status"] == "FAILED" and r["label"] == "transient")
        out[st] = (k + 1.0) / (n + 10.0)
    return out


def expected_cost_and_success(fl: FailLab, is_new, gates, cost_new, cost_reuse_by_lot, lots):
    """For viab_node_ec: E[cost] of each candidate's chain when it stops at the first blocking
    failure, and its probability of finishing, from the transient rates and the viability gates."""
    C = fl.net.COSTS
    p = transient_rates(fl)
    m = is_new.shape[0]
    one = torch.ones(m)
    vg = {st: gates.get(st, one) for st in ("A", "L", "M")}
    if fl.cu:
        tail_ok = (1 - p["T"]) * (1 - p["I"])
        pm = (1 - p["M"]) * vg["M"]
        # after Mines: microscopy (never fails), tensile, the screen (never fails), immersion
        tail_cost = C["S"] + C["T"] + (1 - p["T"]) * (C["K"] + C["I"])
        reuse_cost = torch.tensor([cost_reuse_by_lot.get(l, 0.0) for l in lots])  # Mines session (first or repeat)
        pa = (1 - p["A"]) * vg["A"]
        first_mines = cost_new - (C["C"] + C["A"] + C["U"] + C["S"] + C["T"] + C["K"] + C["I"])
        e_new = C["C"] + C["A"] + pa * (C["U"] + first_mines + pm * tail_cost)
        e_reuse = reuse_cost + pm * tail_cost
        succ = torch.where(is_new, pa * pm * tail_ok, pm * tail_ok)
    else:
        pl = (1 - p["L"]) * vg["L"]
        pa = (1 - p["A"]) * vg["A"]
        e_new = C["C"] + C["A"] + pa * (C["L"] + pl * C["T"])
        e_reuse = C["L"] + pl * C["T"]
        succ = torch.where(is_new, pa * pl * (1 - p["T"]), pl * (1 - p["T"]))
    ecost = torch.where(is_new, e_new * one, e_reuse * one)
    # the transient part of success scales EI; the viability part is already inside the gated EI
    tr_ok = torch.where(is_new, ((1 - p["A"]) * ((1 - p["M"]) * tail_ok if fl.cu else (1 - p["L"]) * (1 - p["T"]))) * one,
                        (((1 - p["M"]) * tail_ok) if fl.cu else (1 - p["L"]) * (1 - p["T"])) * one)
    return ecost, tr_ok, succ


# --------------------------------------------------------------------------- the campaign
def run(net, strategy: str, scenario: str, kappa: float, seed: int, budget: float = 100_000.0, eta: float = 1.0, verbose: bool = False, reuse: bool = True):
    BA, POL = net.BA, net.POL
    truth = net.truth(kappa, eta)
    torch.manual_seed(seed)
    BA.FIT_LOG.update(calls=0, failures=0)
    d, lab = POL.initial_data(truth, seed)
    fm = FailureModel(net.family, scenario, seed, kappa, f_crack=getattr(BA, "F_CRACK", 0.56), p_cap=getattr(BA, "P_CAP", 0.5))
    fl = FailLab(net, truth, d, lab, fm)
    g = torch.Generator().manual_seed(3000 + seed)
    NC, D, COSTS = len(net.COMP), net.D, net.COSTS
    if fl.cu:
        full_cost = BA.FULL_COST
        tail = COSTS["S"] + COSTS["T"] + COSTS["K"] + COSTS["I"]
        cheapest = COSTS["M"] + tail
    else:
        full_cost = COSTS["C"] + COSTS["A"] + COSTS["L"] + COSTS["T"]
        cheapest = COSTS["L"] + COSTS["T"]
    if not reuse:  # full-pipeline BOFN (the source `eifn`): every decision is a new design through every stage
        cheapest = full_cost
    curve = [dict(spent=0.0, best=max(v for _, v in d.full), action="init")]
    it = 0
    t0 = time.time()
    n_viab_active = 0
    while d.spent + cheapest <= budget:
        it += 1
        left = budget - d.spent
        model = Model(fl, strategy)
        if fl.cu:
            lab.net = model.network
        n_viab_active += int(model.vx is not None or bool(model.vnode))
        X = torch.stack([x for x, _ in d.full])
        y = torch.tensor([v for _, v in d.full])
        best = float(y.max())
        Pn = net.feasible(torch.cat([BA.sobol(1024, D, seed=it + 50 * seed), BA.local_perturb(X, 16, 0.05, g)]))
        pools, lots = [Pn], [-1] * Pn.shape[0]
        costs = [torch.full((Pn.shape[0],), full_cost)]
        for i, L in enumerate(d.lots if reuse else []):
            pv = BA.sobol(64, 2, seed=it + 50 * seed + i)  # drawn for every lot, as in the source, so pools stay aligned
            if i in fl.unprintable:
                continue
            pools.append(torch.cat([L["c"].expand(64, NC), torch.full((64, 1), L["a"]), pv], -1))
            costs.append(torch.full((64,), (lab.mines_cost(i) + tail) if fl.cu else (COSTS["L"] + COSTS["T"])))
            lots += [i] * 64
        P, cost = torch.cat(pools), torch.cat(costs)
        is_new = torch.tensor([l < 0 for l in lots])
        eps = POL.eps_for(P.shape[0], S_MC, it)
        gv = torch.Generator().manual_seed(900_000 + 1000 * seed + it)
        eps["_vx"] = torch.randn(P.shape[0], S_MC, generator=gv)
        for st in ("A", "L", "U", "M"):
            eps["_v" + st] = torch.randn(P.shape[0], S_MC, generator=gv)
        if strategy == "viab_node_ec":
            ei, gates = gated_ei(fl, model, P, is_new, eps, best, it, want_gates=True)
            reuse_cost = {i: lab.mines_cost(i) for i in range(len(d.lots))} if fl.cu else {}
            ecost, tr_ok, _ = expected_cost_and_success(fl, is_new, gates, full_cost, reuse_cost, lots)
            score = ei * tr_ok / ecost
        else:
            ei = gated_ei(fl, model, P, is_new, eps, best, it)
            score = ei / cost
        score[cost > left] = -1.0
        j = int(score.argmax())
        if float(score[j]) < 0:
            break
        x = P[j]
        t = fl.run_reuse(x, lots[j]) if lots[j] >= 0 else fl.run_new(x)
        blk = t["blocked"]
        curve.append(dict(spent=d.spent, best=max(v for _, v in d.full), action=t["kind"], complete=t["complete"],
                          fail=None if blk is None else f"{blk['stage']}:{blk['kind']}:{blk['label']}" + (":pre" if blk["precondition"] else ""),
                          ei=float(ei[j]), pend=model.n_pending))
        if verbose:
            c = curve[-1]
            print(f"it {it:3d} {c['action']:5s} {str(c['fail']):22s} spent {d.spent:8.0f} best {c['best']:.3f} pend {model.n_pending} {time.time() - t0:.0f}s", flush=True)
    return summarize(net, fl, truth, strategy, scenario, kappa, eta, seed, budget, curve, it, n_viab_active, time.time() - t0)


def summarize(net, fl, truth, strategy, scenario, kappa, eta, seed, budget, curve, iters, n_viab_active, wall):
    stages = sorted({r["stage"] for r in fl.rows})
    att = {s: sum(1 for r in fl.rows if r["stage"] == s and not r["precondition"]) for s in stages}
    fails = {}
    for r in fl.rows:
        if r["status"] == "FAILED":
            key = f"{r['stage']}:{r['kind']}" + (":pre" if r["precondition"] else "")
            fails[key] = fails.get(key, 0) + 1
    spent_failed = sum(r["cost"] for r in fl.rows if r["status"] == "FAILED")
    spent_blocked = sum(t["cost"] for t in fl.trials if t["blocked"] is not None)
    # repeated input-caused failures (true kind), within NEAR of an earlier one in x
    inp = [fl.trials[r["trial"]]["x"] for r in fl.rows if r["status"] == "FAILED" and r["kind"] == "input"]
    repeats = 0
    for k in range(1, len(inp)):
        if torch.cdist(inp[k][None], torch.stack(inp[:k])).min() < NEAR:
            repeats += 1
    mislabels = sum(1 for r in fl.rows if r["status"] == "FAILED" and r["kind"] != r["label"])
    best_x = max(fl.d.full, key=lambda t: t[1])[0]
    return {
        "net": net.name, "strategy": strategy, "scenario": scenario, "kappa": kappa, "eta": eta, "seed": seed, "budget": budget,
        "curve": curve, "iters": iters, "wall_s": wall,
        "trials": len(fl.trials), "trials_new": sum(1 for t in fl.trials if t["kind"] == "new"),
        "trials_complete": sum(1 for t in fl.trials if t["complete"]),
        "trials_blocked": sum(1 for t in fl.trials if t["blocked"] is not None),
        "attempts": att, "failures": fails, "mislabels": mislabels,
        "spent_on_failed_stages": spent_failed, "spent_on_blocked_runs": spent_blocked,
        "input_failures": len(inp), "repeat_input_failures": repeats,
        "iters_with_viability_active": n_viab_active,
        "final_best": curve[-1]["best"], "best_x": [round(float(v), 4) for v in best_x],
        "gp_fits": dict(fl.BA.FIT_LOG),
    }
