"""Policies for the clocked lab. Each has `decide(lab, t) -> [action, ...]`, a ranked list the lab admits in order
as capacity, the admission window and money allow. Policies read only what the lab has measured (lot quality
readings, coupon density readings, bars, immersion readings), never the truth.

Automated (asynchronous) policies share one set of finishing rules (`finishing`): which coupons get bars, which get
replicates, which go into immersion and when an immersion is stopped. The rules use measured values only and depend
on the current claim, so finishing a part that could beat the claim always has value (the zero-KG trap of E4 can't
happen to them). The policies differ in what they make and print:

* `random`: random alloys and process settings.
* `tiered`: CALPHAD screen (predicted crack-free, ranked by strength net of minerals), then constrained EI on the
  shortlist with an objective-level GP; the shortlist moves down the screen's ranking when it stops paying (round 3's
  funnel).
* `gpbo`: constrained EI with one GP from the design to the measured objective and one to the corrosion readings
  (kriging believer by exclusion around designs in flight).
* `bofn`: the function network; constrained network EI per cost of the remaining path to a claim (round 3's BOFN).
* `pkgfn`: the same network; knowledge gradient of the next print (and of a new powder bundled with its first
  build) per its own cost, any composition allowed (CALPHAD first), candidates proposed by network EI (fast-pKGFN
  style), inner max over an incumbent-anchored set (bofn-prelim's estimator).
* `conv`: the conventional baselines' decision rule: tiered screening in rounds of four builds, decided at Monday
  meetings once the round's bars are back, three bars from each build's densest coupon, immersion without interim
  actions.
"""
from __future__ import annotations

import math
import warnings

import numpy as np
from scipy.stats import norm, qmc

warnings.filterwarnings("ignore", message="The balance properties of Sobol")

from model import GP, Network, eps_for, records
from truth import IMM_SIG, SIG_BAR, burden

F_SAFE, SCREEN_N, SCREEN_TOP = 0.25, 256, 4


def sobol(n, d, seed):
    return qmc.Sobol(d, scramble=True, seed=seed).random(n)


def gh(k):
    t, w = np.polynomial.hermite_e.hermegauss(k)
    return t, w / w.sum()


class Base:
    name = "base"
    model_based = False
    n_init = 4  # space-filling powders before a model takes over

    def __init__(self, seed, truth, group_mode=None, prior=None, cur_group=0, powder_route="us", lam=None,
                 comp_dims=None, refs=None, wip=None):
        self.seed, self.truth = seed, truth
        self.comp_dims = comp_dims  # E5: the composition dims a family's campaign may vary (others held at 0)
        self.refs = list(refs or [])  # E3b: (day, design) reference alloys re-made at those days
        self.ref_lots = {}
        if wip:
            self.WIP_LOTS, self.WIP_BUILDS = wip
        self.rng = np.random.default_rng(10_000 + seed)
        self.nc = truth.ncomp
        self.group_mode, self.prior, self.cur_group = group_mode, prior, cur_group
        self.powder_route = powder_route
        self.hyper = {}
        self.it = 0
        self.burden = truth.burden_x if hasattr(truth, "burden_x") else burden
        self.init_designs = self.mask(sobol(16, self.nc + 3, 900 + seed))
        self.n_started = 0

    def mask(self, P):
        if self.comp_dims is None:
            return P
        P = np.array(P, float)
        off = [j for j in range(self.nc) if j not in self.comp_dims]
        P[..., off] = 0.0
        return P

    def ref_actions(self, lab, t):
        """Reference alloys re-made at their scheduled days, printed at their own laser settings (E3b)."""
        acts = []
        for day, x in list(self.refs):
            if t >= day:
                self.refs.remove((day, x))
                acts.append(dict(kind="powder", c=np.asarray(x[: self.nc]), a=float(x[self.nc]), route=self.powder_route))
                self.ref_lots[lab.key(x[: self.nc])] = x
        for L in lab.lots:
            x = self.ref_lots.get(L["key"])
            if x is not None and L["t_ready"] is not None and L["uses_left"] > 0 and not any(
                    b["lot"] == L["id"] for b in lab.builds):
                pv = [(x[self.nc + 1] + dp, x[self.nc + 2] + dv) for dp, dv in
                      ((0, 0), (0.05, 0), (-0.05, 0), (0, 0.05), (0.05, 0.05), (-0.05, -0.05))]
                acts.append(dict(kind="print", lot=L["id"], pv=[(float(np.clip(a, 0, 1)), float(np.clip(b, 0, 1))) for a, b in pv],
                                 machine=("ih", "pt")))
        return acts

    # ------------------------------------------------------------ helpers
    def obj_meas(self, lab, cp):
        return lab.objective_meas(cp)

    def pending_comps(self, lab):
        """Compositions of lots in flight, or made but not yet printed: new designs keep away from them."""
        out = [lab.lots[i]["c"] for k, i, _ in lab.inflight if k == "powder"]
        for lot in lab.lots:
            if lot["t_ready"] is not None and lot["uses_left"] > 0 and not any(
                    lab.builds[b]["lot"] == lot["id"] for b in range(len(lab.builds))):
                out.append(lot["c"])
        return np.array(out).reshape(-1, self.nc)

    def ready_lots(self, lab):
        busy = {lab.builds[i]["lot"] for k, i, _ in lab.inflight if k == "print"}
        return [L for L in lab.lots if L["t_ready"] is not None and L["uses_left"] > 0 and L["id"] not in busy
                and L["key"] not in self.ref_lots]

    def machine_pref(self, lab, t):
        """The machine a build would go to now: in house if it can start within the window, else the partner."""
        for m in ("ih", "pt"):
            if lab.can_start(m, t):
                return m
        return None

    # ------------------------------------------------------------ shared finishing rules (measured values only)
    @staticmethod
    def corr_fails(lab, cp):
        """True once a coupon's immersion readings say it fails (P(pass) < 5 %) or its final reading failed."""
        if cp["imm_final"] is not None:
            return cp["imm_final"] > lab.truth.ln_rmax
        if not cp["imm_read"]:
            return False
        d = max(cp["imm_read"])
        return (cp["imm_read"][d] - lab.truth.ln_rmax) / IMM_SIG[d] > 1.645

    def finishing(self, lab, t, k_imm=6, near=0.05):
        """Shared, model-free finishing rules. Candidates: tested parts not failing corrosion, within `near` of the
        best such part and at or above the claim. The top ones get replicate bars and an immersion, in parallel."""
        acts = []
        inc = lab.claimed_value_meas()
        ok = [(self.obj_meas(lab, cp), cp) for cp in lab.coupons
              if cp["bars"] and not self.corr_fails(lab, cp) and not (cp["imm"] and cp["imm"]["state"] == "stopped")]
        best_ok = max((o for o, _ in ok), default=-math.inf)
        ref = max(inc if inc is not None else -math.inf, best_ok - near)
        # stops: the readings say it will fail, or it can no longer improve the claim
        for cp in lab.coupons:
            im = cp["imm"]
            if im is None or im["state"] != "running" or not cp["imm_read"]:
                continue
            hopeless = len(cp["bars"]) >= 3 and inc is not None and self.obj_meas(lab, cp) < inc - 0.01
            if self.corr_fails(lab, cp) or hopeless:
                acts.append(dict(kind="stop", coupon=cp["id"]))
        # first bar on the two densest coupons of every build that came back
        for b in lab.builds:
            if b.get("t_done") is None or b["failed"]:
                continue
            cps = sorted((lab.coupons[i] for i in b["coupons"]), key=lambda c: -c["rho_meas"])
            for j, cp in enumerate(cps[:2]):
                if not cp["bars"] and cp["bars_pending"] == 0 and cp["bars_left"] == 3 and (j == 0 or cp["rho_meas"] >= 0.5):
                    acts.append(dict(kind="bars", coupon=cp["id"], n=1))
        running = sum(1 for cp in lab.coupons if cp["imm"] is not None and cp["imm"]["state"] == "running")
        cands = [x for x in sorted(ok, key=lambda x: -x[0]) if x[0] >= ref][:k_imm]
        for o, cp in cands:
            if cp["bars_pending"] == 0 and len(cp["bars"]) < 3 and cp["bars_left"] > 0:
                acts.append(dict(kind="bars", coupon=cp["id"], n=3 - len(cp["bars"])))
            if cp["imm"] is None and running < 24:
                acts.append(dict(kind="imm", coupon=cp["id"]))
                running += 1
        return acts

    WIP_LOTS, WIP_BUILDS = 3, 4

    def unlearned(self, lab):
        """Lots made or in flight that nothing has been learned from yet, and builds whose first bar isn't back."""
        printed = {b["lot"] for b in lab.builds} | {L["id"] for L in lab.lots if L["key"] in self.ref_lots}
        inflight = {i for k, i, _ in lab.inflight if k == "powder"}
        lots = sum(1 for L in lab.lots if L["id"] not in printed and (L["id"] in inflight or L["t_ready"] is not None))
        builds = 0
        for b in lab.builds:
            if b.get("t_done") is None:
                builds += 1
            elif not b["failed"] and not any(lab.coupons[i]["bars"] for i in b["coupons"]):
                builds += 1
        return lots, builds

    def decide(self, lab, t):
        """Finishing first, then new prints and powders, each only while there is little unlearned work in
        flight (the same self-limits for every automated policy: a batch of about three powders and four builds)."""
        self.it += 1
        acts = self.ref_actions(lab, t) + self.finishing(lab, t)
        n_lots, n_builds = self.unlearned(lab)
        can_powder = lab.can_start(self.powder_route, t) and n_lots < self.WIP_LOTS
        mach = self.machine_pref(lab, t) if n_builds < self.WIP_BUILDS else None
        mach_any = self.machine_pref(lab, t)
        if not can_powder and mach is None and mach_any is None:
            return acts
        made = self.make(lab, t, can_powder, mach) if (can_powder or mach) else []
        return acts + self.first_builds(lab, made, mach_any) + made

    def first_builds(self, lab, made, mach):
        """Every powder gets at least one build: a ready lot nobody has printed is printed at the policy's own best
        settings for it (or space-filling ones), whatever its acquisition value, before anything new is made."""
        if mach is None:
            return []
        planned = {a["lot"] for a in made if a["kind"] == "print"}
        busy = {lab.builds[i]["lot"] for k, i, _ in lab.inflight if k == "print"}
        printed = {b["lot"] for b in lab.builds}
        out = []
        for L in self.ready_lots(lab):
            if L["id"] in printed or L["id"] in planned or L["id"] in busy:
                continue
            pv = getattr(self, "_pv_cache", {}).get(L["id"]) or self.default_pv(6, self.seed + L["id"])
            out.append(dict(kind="print", lot=L["id"], pv=pv, machine=(mach, "pt")))
        return out

    def init_powders(self, lab, k):
        out = []
        for _ in range(k):
            x = self.init_designs[self.n_started % len(self.init_designs)]
            self.n_started += 1
            out.append(dict(kind="powder", c=x[: self.nc], a=float(x[self.nc]), route=self.powder_route))
        return out

    def default_pv(self, k, seed):
        return [tuple(r) for r in sobol(8, 2, seed)[:k]]


# --------------------------------------------------------------------------- random
class Random(Base):
    name = "random"

    def make(self, lab, t, can_powder, mach):
        acts = []
        if mach:
            for L in self.ready_lots(lab)[:2]:
                acts.append(dict(kind="print", lot=L["id"], pv=[tuple(self.rng.random(2)) for _ in range(6)],
                                 machine=(mach, "pt")))
        if can_powder:
            for _ in range(2):
                x = self.rng.random(self.nc + 3)
                acts.append(dict(kind="powder", c=x[: self.nc], a=float(x[self.nc]), route=self.powder_route))
        return acts


# --------------------------------------------------------------------------- objective-level models (GP-BO, tiered)
def design_feats(lab, cp):
    a = cp["a"] if cp["a"] is not None else 0.5
    return np.concatenate([cp["c"], [a, cp["P"], cp["v"], float(cp["machine"] == "pt"), float(cp["route"] == "gas")]])


class ObjModel:
    """GP-BO's model: one GP from design features to the measured objective, one to the latest immersion reading."""

    def __init__(self, lab, pol, prior_obj=None):
        X, y, nz = [], [], []
        Xc, yc, nzc = [], [], []
        for cp in lab.coupons:
            if cp["bars"]:
                X.append(design_feats(lab, cp))
                y.append(lab.objective_meas(cp))
                nz.append(SIG_BAR ** 2 / len(cp["bars"]) + 0.01 ** 2)
            if cp["imm_read"]:
                d = max(cp["imm_read"])
                Xc.append(design_feats(lab, cp))
                yc.append(cp["imm_read"][d])
                nzc.append(IMM_SIG[d] ** 2)
        if prior_obj:
            X = list(prior_obj["X"]) + X
            y = list(prior_obj["y"]) + y
            nz = list(prior_obj["noise"]) + nz
        d = pol.nc + 5
        self.gp = GP(np.array(X).reshape(-1, d), np.array(y), np.array(nz), hyper=pol.hyper.get("obj_h"),
                     prior_mean=0.2, prior_sd=0.2)
        self.gc = GP(np.array(Xc).reshape(-1, d), np.array(yc), np.array(nzc), hyper=pol.hyper.get("corr_h"),
                     prior_mean=0.7, prior_sd=0.8)
        for k, g, n in (("obj", self.gp, len(y)), ("corr", self.gc, len(yc))):
            old_n = pol.hyper.get(k + "_n", -99)
            if n > old_n * 4 / 3 + 6:
                pol.hyper[k + "_h"], pol.hyper[k + "_n"] = None, n  # refit next time
            else:
                pol.hyper[k + "_h"] = g.hyper
        self.ln_rmax = lab.truth.ln_rmax
        # de-noised incumbent: the GP's posterior mean at tested designs likely to pass corrosion (not the raw max)
        self.best = 0.0
        if len(y):
            Xa = np.array(X).reshape(-1, d)
            m, _ = self.gp.predict(Xa)
            mc, vc = self.gc.predict(Xa)
            ok = norm.cdf((self.ln_rmax - mc) / np.sqrt(vc + 1e-12)) >= 0.5
            if ok.any():
                self.best = float(m[ok].max())

    def cei(self, F):
        m, v = self.gp.predict(F)
        sd = np.sqrt(v + 1e-12)
        z = (m - self.best) / sd
        ei = sd * (z * norm.cdf(z) + norm.pdf(z))
        mc, vc = self.gc.predict(F)
        pf = norm.cdf((self.ln_rmax - mc) / np.sqrt(vc + 1e-12))
        return ei * pf, m


class GPBO(Base):
    name = "gpbo"
    model_based = True
    MIN_EI = 1e-4  # an action starts only if its EI is at least this (round 3's threshold for new designs)
    restrict = None  # tiered: list of allowed compositions

    def feats(self, X, pt, gas):
        m = X.shape[0]
        return np.concatenate([X, np.full((m, 1), pt), np.full((m, 1), gas)], 1)

    def make(self, lab, t, can_powder, mach):
        tested = sum(1 for cp in lab.coupons if cp["bars"])
        acts = []
        if tested < 3:  # not enough data for a model yet
            if mach:
                for L in self.ready_lots(lab)[:2]:
                    acts.append(dict(kind="print", lot=L["id"], pv=self.default_pv(6, self.seed + L["id"]),
                                     machine=(mach, "pt")))
            if can_powder and self.n_started < self.n_init:
                acts += self.init_powders(lab, 2)
            return acts
        M = ObjModel(lab, self)
        pt = float(mach == "pt")
        if mach:
            for L in self.ready_lots(lab)[:3]:
                a = L["a"] if L["a"] is not None else 0.5
                pv = sobol(128, 2, self.it * 7 + L["id"])
                X = np.concatenate([np.repeat(L["c"][None], 128, 0), np.full((128, 1), a), pv], 1)
                ei, _ = M.cei(self.feats(X, pt, float(L["route"] == "gas")))
                self._pv_cache = getattr(self, "_pv_cache", {})
                self._pv_cache[L["id"]] = self.pick_pv(pv, ei)
                acts.append((float(ei.max()), dict(kind="print", lot=L["id"], pv=self._pv_cache[L["id"]],
                                                   machine=(mach, "pt"))))
        if can_powder:
            P = self.pool(lab)
            if len(P):
                ei, _ = M.cei(self.feats(P, 0.0, 0.0))
                for j in self.diverse(P, ei, 2, self.pending_comps(lab)):
                    acts.append((float(ei[j]), dict(kind="powder", c=P[j, : self.nc], a=float(P[j, self.nc]),
                                                    route=self.powder_route)))
        live = [a for v, a in sorted(acts, key=lambda x: -x[0]) if v >= self.MIN_EI]
        if not live and acts and not lab.inflight:
            # the same last resort as the network policies: nothing worth it and nothing in flight
            self.zero_value = getattr(self, "zero_value", 0) + 1
            live = [max(acts, key=lambda x: x[0])[1]]
        return live

    def pick_pv(self, pv, score, k=6, min_d=0.06):
        chosen = []
        for j in np.argsort(-score):
            if all(np.linalg.norm(pv[j] - pv[i]) >= min_d for i in chosen):
                chosen.append(j)
            if len(chosen) == k:
                break
        return [tuple(pv[j]) for j in chosen]

    def diverse(self, P, score, k, avoid, min_d=0.08):
        out = []
        for j in np.argsort(-score):
            c = P[j, : self.nc]
            if len(avoid) and np.min(np.linalg.norm(avoid - c, axis=1)) < min_d:
                continue
            if any(np.linalg.norm(P[i, : self.nc] - c) < min_d for i in out):
                continue
            out.append(j)
            if len(out) == k:
                break
        return out

    def pool(self, lab):
        P = self.mask(sobol(512, self.nc + 3, self.it + 1000 * self.seed))
        tested = [cp for cp in lab.coupons if cp["bars"]]
        if tested:
            top = sorted(tested, key=lambda c: -lab.objective_meas(c))[:4]
            loc = []
            for cp in top:
                x = np.concatenate([cp["c"], [cp["a"] if cp["a"] is not None else 0.5, cp["P"], cp["v"]]])
                loc.append(self.mask(np.clip(x + 0.06 * self.rng.standard_normal((32, len(x))), 0, 1)))
            P = np.concatenate([P] + loc)
        return P


class Tiered(GPBO):
    """CALPHAD screen, then constrained EI on the shortlist; the shortlist moves down the screen's ranking."""

    name = "tiered"

    def ranking(self, lab):
        if not hasattr(self, "_rank"):
            comps = list(lab.comps.values())
            C = np.array([v["c"] for v in comps])
            s = np.array([v["s"] for v in comps])
            f = np.array([v["f"] for v in comps])
            fom = np.where(f <= F_SAFE, s - lab.truth.lam * self.burden(C), -9.0)
            order = np.argsort(-fom)
            self._rank = C[order[fom[order] > -9]]
            self.n_short = SCREEN_TOP
        return self._rank

    def shortlist(self, lab):
        return self.ranking(lab)[: self.n_short]

    def pool(self, lab):
        SL = self.shortlist(lab)
        apv = sobol(128, 3, self.it + 1000 * self.seed)
        return np.concatenate([np.concatenate([np.repeat(c[None], 128, 0), apv], 1) for c in SL])

    def init_powders(self, lab, k):
        SL = self.shortlist(lab)
        out = []
        for _ in range(k):
            c = SL[self.n_started % len(SL)]
            self.n_started += 1
            out.append(dict(kind="powder", c=c, a=0.5, route=self.powder_route))
        return out

    def diverse(self, P, score, k, avoid, min_d=0.08):
        # shortlisted compositions repeat: diversity is over (composition, atomizer setting)
        out = []
        for j in np.argsort(-score):
            if any(np.linalg.norm(P[i, : self.nc + 1] - P[j, : self.nc + 1]) < 0.05 for i in out):
                continue
            out.append(j)
            if len(out) == k:
                break
        return out

    def make(self, lab, t, can_powder, mach):
        acts = super().make(lab, t, can_powder, mach)
        # funnel: when nothing on the shortlist is worth a new powder, move four further down the ranking
        if can_powder and not any(a["kind"] == "powder" for a in acts) and sum(1 for cp in lab.coupons if cp["bars"]) >= 3:
            if self.n_short < len(self.ranking(lab)):
                self.n_short += SCREEN_TOP
        return acts


# --------------------------------------------------------------------------- the network policies
class BOFN(GPBO):
    name = "bofn"
    S = 32
    MIN_EI = 1e-4

    def network(self, lab):
        net = Network(lab.truth, lab.comps, records(lab, self.prior), self.group_mode, self.hyper, self.cur_group)
        self.hyper = net.hyper
        return net

    def incumbent(self, lab, net):
        """Best tested part, de-noised: the strength node's posterior mean at its measured density, minus the burden,
        over tested parts that passed corrosion or that the corrosion node expects to pass (P >= 0.5). The raw
        maximum of single-bar readings would be biased high (the winner's curse) and make every EI vanish."""
        rows = [cp for cp in lab.coupons if cp["bars"] and not self.corr_fails(lab, cp)]
        if not rows:
            return 0.0
        s_ = np.array([lab.comps[cp["key"]]["s"] for cp in rows])
        r_ = np.array([cp["rho_meas"] for cp in rows])
        C = np.array([cp["c"] for cp in rows])
        mu_u, _ = net.gp_U.predict(np.stack([s_, r_], -1), net.cur)
        obj = mu_u - net.lam * net.burden(C)
        mc, vc = net.gp_corr.predict(np.concatenate([C, r_[:, None]], 1))
        pp = norm.cdf((lab.truth.ln_rmax - mc) / np.sqrt(vc))
        pp = np.where([cp["imm_final"] is not None for cp in rows], 1.0, pp)
        ok = pp >= 0.5
        return float(obj[ok].max()) if ok.any() else 0.0

    def path_cost(self, lab, stage, mach):
        r = lab.routes
        tail = r["bars"]["cost_per"] * 3 + r["imm"]["cost"]
        build = r[mach]["cost"] if mach in r else r["pt"]["cost"]
        if stage == "build":
            return build + tail
        return r[self.powder_route]["cost"] + 10 + build + tail

    def lot_known(self, lab, L, m):
        cal = lab.comps[L["key"]]
        return dict(s=np.full(m, cal["s"]), f=np.full(m, cal["f"]), g=np.full(m, cal["g"]), q=np.full(m, L["q_meas"]))

    def ei(self, net, X, gas, pt, inc, seed, known=None):
        """Constrained network EI in normal form (round 3's choice): the objective draws' mean and spread give the
        EI, times the mean probability that the corrosion test passes. Unlike the EI of 32 raw draws, it is never
        rounded to exactly 0 when the chance is small. Also returns the expected claim value."""
        eps = eps_for(X.shape[0], self.S, seed)
        obj, lnr, v = net.sample(X, np.full(X.shape[0], gas), np.full(X.shape[0], pt), eps, known)
        m, sd = obj.mean(1), np.maximum(obj.std(1), 1e-6)
        pf = v["p_pass"].mean(1)
        z = (m - inc) / sd
        ei = pf * (sd * norm.pdf(z) + (m - inc) * norm.cdf(z))
        return np.maximum(ei, 0.0), (obj * v["p_pass"]).mean(1), (obj, lnr, v)

    def make(self, lab, t, can_powder, mach):
        if sum(1 for cp in lab.coupons if cp["rho_meas"] is not None) < 12:
            acts = []
            if mach:
                for L in self.ready_lots(lab)[:2]:
                    acts.append(dict(kind="print", lot=L["id"], pv=self.default_pv(6, self.seed + L["id"]),
                                     machine=(mach, "pt")))
            if can_powder and self.n_started < self.n_init:
                acts += self.init_powders(lab, 2)
            return acts
        net = self.network(lab)
        inc = self.incumbent(lab, net)
        scored = []
        pt = float(mach == "pt")
        if mach:
            for L in self.ready_lots(lab)[:4]:
                a = L["a"] if L["a"] is not None else 0.5
                pv = np.concatenate([sobol(96, 2, self.it * 7 + L["id"]), self.local_pv(lab, L)])
                X = np.concatenate([np.repeat(L["c"][None], len(pv), 0), np.full((len(pv), 1), a), pv], 1)
                ei, mu, _ = self.ei(net, X, float(L["route"] == "gas"), pt, inc, self.it, self.lot_known(lab, L, len(pv)))
                score = self.build_score(net, lab, L, X, ei, mu, pt, inc)
                self._pv_cache = getattr(self, "_pv_cache", {})
                self._pv_cache[L["id"]] = self.pick_pv(pv, ei + 1e-6 * mu)
                scored.append((score / self.own_cost(lab, "build", mach),
                               dict(kind="print", lot=L["id"], pv=self._pv_cache[L["id"]], machine=(mach, "pt")),
                               float(ei.max()) / self.path_cost(lab, "build", mach), float(ei.max()), float(mu.max())))
        if can_powder:
            P = self.pool(lab)
            ei, mu, _ = self.ei(net, P, 0.0, 0.0, inc, self.it + 1)
            for j in self.powder_choice(net, lab, P, ei, mu, inc):
                scored.append((self.powder_score(net, lab, P, j, ei, mu, inc) / self.own_cost(lab, "powder", "ih"),
                               dict(kind="powder", c=P[j, : self.nc], a=float(P[j, self.nc]), route=self.powder_route),
                               float(ei[j]) / self.path_cost(lab, "powder", "ih"), float(ei[j]), float(mu[j])))
        if not scored:
            return []
        # an action starts only if its EI is at least 1e-4 (round 3's threshold for new designs)
        live = [x for x in scored if x[3] >= self.MIN_EI]
        if self.name == "pkgfn":
            if live and max(x[0] for x in live) > 1e-9:
                self.kg_used = getattr(self, "kg_used", 0) + 1
                live = [x for x in live if x[0] > 1e-9]
            else:  # every KG is flat: EI per cost of the remaining path decides (bofn-prelim's and round 3's fallback)
                self.kg_flat = getattr(self, "kg_flat", 0) + 1
                live = [(x[2],) + x[1:] for x in live]
        if not live and not lab.inflight:
            # nothing is worth its cost by the model and nothing is in flight: rather than end the campaign with money
            # left, make the single candidate with the best expected claim value; counted, as it means the model is stuck
            self.zero_value = getattr(self, "zero_value", 0) + 1
            return [max(scored, key=lambda x: x[4])[1]]
        return [x[1] for x in sorted(live, key=lambda x: -x[0])]

    def own_cost(self, lab, stage, mach):
        """BOFN's denominator is the cost of the remaining path to a claim; pKGFN's (below) the step's own cost."""
        return self.path_cost(lab, stage, mach)

    def build_score(self, net, lab, L, X, ei, mu, pt, inc):
        return float(ei.max())

    def powder_choice(self, net, lab, P, ei, mu, inc):
        return self.diverse(P, ei + 1e-6 * mu, 2, self.pending_comps(lab))

    def powder_score(self, net, lab, P, j, ei, mu, inc):
        return float(ei[j])

    def local_pv(self, lab, L):
        cps = [cp for cp in lab.coupons if cp["key"] == L["key"] and cp["rho_meas"] is not None]
        if not cps:
            return np.zeros((0, 2))
        best = max(cps, key=lambda c: c["rho_meas"])
        return np.clip(np.array([best["P"], best["v"]]) + 0.05 * self.rng.standard_normal((32, 2)), 0, 1)


class PKGFN(BOFN):
    """Knowledge gradient of the next print (or new powder + its first build) per its own cost."""

    name = "pkgfn"
    S_KG, F_KG, N_ANCHOR = 16, 8, 32

    def make(self, lab, t, can_powder, mach):
        self._anchor = None
        return super().make(lab, t, can_powder, mach)

    def anchors(self, net, lab):
        if self._anchor is None:
            P = self.pool(lab)
            _, mu, _ = self.ei(net, P, 0.0, 0.0, 0.0, self.it + 3)
            self._anchor = P[np.argsort(-mu)[: self.N_ANCHOR]]
        return self._anchor

    def kg(self, net, lab, X, z_known, gas, pt):
        """KG of one build: the joint density readings of its coupons at designs X [k, nc+3] (one lot, so the same
        composition, atomizer setting, f, g and q), fantasized jointly (F quasi-random draws of the k readings) and
        carried through the strength and corrosion nodes; inner max over the anchors and X (bofn-prelim's estimator,
        so the estimate is never negative)."""
        Xi = np.concatenate([self.anchors(net, lab), X])
        m, S, k = Xi.shape[0], self.S_KG, X.shape[0]
        eps = eps_for(m, S, 77 + self.it)
        gasv, ptv = np.zeros(m), np.zeros(m)
        gasv[-k:], ptv[-k:] = gas, pt
        _, _, v = net.sample(Xi, gasv, ptv, eps, None)
        nc = self.nc
        gp = net.gp_rho
        if gp.n == 0:
            return 0.0
        inp = np.stack([np.repeat(Xi[:, nc + 1][:, None], S, 1), np.repeat(Xi[:, nc + 2][:, None], S, 1), v["f"], v["g"],
                        v["q"], np.repeat(ptv[:, None], S, 1), np.repeat(gasv[:, None], S, 1)]
                       + ([np.zeros((m, S))] if net.ext else []), -1)
        mu, var, V = gp.predict(inp, net.cur, return_V=True)
        Z = np.array([[x[nc + 1], x[nc + 2], z_known["f"], z_known["g"], z_known["q"], pt, gas] + ([0.0] if net.ext else [])
                      for x in X])
        _, _, Vz = gp.predict(Z, net.cur, return_V=True)
        Kzz = gp.cross(Z, Vz, Z, Vz) + (0.015 ** 2 * 2) * np.eye(k)
        Lz = np.linalg.cholesky(Kzz + 1e-10 * np.eye(k))
        C = gp.cross(inp, V, Z, Vz)  # [m, S, k]
        A = np.linalg.solve(Lz, C.reshape(-1, k).T).T.reshape(m, S, k)  # shift of the fantasy = A @ w
        vplus = np.maximum(var - (A * A).sum(-1), 1e-12)
        W = self.fant_w(k)
        burden_i = net.lam * net.burden(Xi[:, :nc])[:, None]
        nus = []
        for w in W:
            rho = mu + A @ w + np.sqrt(vplus) * eps["rho"]
            mu_u, var_u = net.gp_U.predict(np.stack([v["s"], rho], -1), net.cur)
            U = mu_u + np.sqrt(var_u) * eps["U"]
            cin = np.concatenate([np.repeat(Xi[:, None, :nc], S, 1), rho[..., None]], -1)
            mc, vc = net.gp_corr.predict(cin)
            pp = norm.cdf((lab.truth.ln_rmax - mc) / np.sqrt(vc))
            nus.append(((U - burden_i) * pp).mean(1))
        nus = np.array(nus)  # [F, m]
        return float(nus.max(1).mean() - nus.mean(0).max())

    def fant_w(self, k):
        if not hasattr(self, "_W") or self._W.shape[1] != k:
            u = qmc.Sobol(k, scramble=True, seed=5).random(self.F_KG)
            W = norm.ppf(np.clip(u, 1e-6, 1 - 1e-6))
            self._W = (W - W.mean(0)) / W.std(0).clip(1e-9)  # moment-matched, so the fantasies average to the mean
        return self._W

    def own_cost(self, lab, stage, mach):
        r = lab.routes
        build = r[mach]["cost"] if mach in r else r["pt"]["cost"]
        return build if stage == "build" else r[self.powder_route]["cost"] + 10 + build

    def build_score(self, net, lab, L, X, ei, mu, pt, inc):
        cal = lab.comps[L["key"]]
        pv = self.pick_pv(X[:, self.nc + 1:], ei + 1e-6 * mu)
        Xb = np.array([np.concatenate([L["c"], [L["a"] if L["a"] is not None else 0.5], p]) for p in pv])
        return self.kg(net, lab, Xb, dict(f=cal["f"], g=cal["g"], q=L["q_meas"]), float(L["route"] == "gas"), pt)

    def powder_choice(self, net, lab, P, ei, mu, inc):
        # KG decides among the four best candidates by network EI per cost (fast-pKGFN proposes this way)
        return self.diverse(P, ei + 1e-6 * mu, 4, self.pending_comps(lab))

    def powder_score(self, net, lab, P, j, ei, mu, inc):
        """A new powder valued with its first build (bundle lookahead): q at its posterior mean, six coupons around
        the candidate's own laser setting."""
        x = P[j]
        cn = net.comp_nodes(x[None, : self.nc])
        g = float(cn["g"][0][0])
        mq, _ = net.gp_q.predict(np.array([[x[self.nc], g, 0.0]]))
        offs = np.array([[0, 0], [0.08, 0], [-0.08, 0], [0, 0.08], [0.08, 0.08], [-0.08, -0.08]])
        Xb = np.array([np.concatenate([x[: self.nc + 1], np.clip(x[self.nc + 1:] + o, 0, 1)]) for o in offs])
        return self.kg(net, lab, Xb, dict(f=float(cn["f"][0][0]), g=g, q=float(mq[0])), 0.0, 0.0)


class BOFNConfirm(BOFN):
    """BOFN plus the move to production powder (E2b): a gas-atomized lot of the best candidate, printed on the
    partner's machine, finished by the shared rules. `confirm` = "after": order once the alloy is claimed (30-day
    immersion passed); "early": order as soon as a candidate has three bars at the top of the field and an interim
    immersion reading (day 7 or later) that passes with 80 % probability. Discovery stops once there is a claim and a
    production lot on order (otherwise it keeps spending while the lot is out for 51 days)."""

    name = "bofn_confirm"
    confirm = "after"

    def decide(self, lab, t):
        acts = super().decide(lab, t)
        return self.confirm_actions(lab, t) + acts

    def candidate(self, lab):
        if self.confirm == "after":
            return lab.coupons[lab.claim] if lab.claim is not None else None
        ok = [cp for cp in lab.coupons if len(cp["bars"]) >= 3 and cp["route"] == "us" and not self.corr_fails(lab, cp)]
        if not ok:
            return None
        top = max(ok, key=lambda c: lab.objective_meas(c))
        days = [d for d in top["imm_read"] if d >= 7]
        if not days:
            return None
        d = max(days)
        p_pass = norm.cdf((lab.truth.ln_rmax - top["imm_read"][d]) / IMM_SIG[d])
        return top if p_pass >= 0.8 else None

    def gas_alive(self, lab):
        """Gas-atomized lots the lab has accepted that are in flight or came back usable."""
        inflight = {i for k, i, _ in lab.inflight if k == "powder"}
        return [L for L in lab.lots if L["route"] == "gas" and (L["id"] in inflight or L["t_ready"] is not None)]

    def confirm_actions(self, lab, t):
        cp = self.candidate(lab)
        if cp is None:
            return []
        alive = self.gas_alive(lab)
        n_orders = sum(1 for L in lab.lots if L["route"] == "gas")
        inflight = {i for k, i, _ in lab.inflight if k == "powder"}
        if cp["key"] in {L["key"] for L in alive} or n_orders >= 3 or any(L["id"] in inflight for L in alive):
            return []
        # proposed every decision until the lab accepts it (the supplier takes one run a month)
        return [dict(kind="powder", c=cp["c"], a=0.5, route="gas")]

    def ready_lots(self, lab):
        # gas lots are printed on the partner's machine (the second site of the validation network)
        return [L for L in super().ready_lots(lab) if L["route"] != "gas"]

    def make(self, lab, t, can_powder, mach):
        # once an alloy is claimed and its production lot is on order, discovery stops: the money goes to confirming
        acts = [] if (lab.claim is not None and self.gas_alive(lab)) else super().make(lab, t, can_powder, mach)
        if not lab.can_start("pt", t):
            return acts
        busy = {lab.builds[i]["lot"] for k, i, _ in lab.inflight if k == "print"}
        gas = [L for L in lab.lots if L["route"] == "gas" and L["t_ready"] is not None and L["id"] not in busy]
        if not gas or sum(1 for cp in lab.coupons if cp["rho_meas"] is not None) < 12:
            return acts
        net = self.network(lab)
        for L in gas:
            done = [cp for cp in lab.coupons if cp["lot"] == L["id"] and cp["rho_meas"] is not None]
            if any(lab.claimable(cp) for cp in done) or len([b for b in lab.builds if b["lot"] == L["id"]]) >= 4:
                continue
            pv = np.concatenate([sobol(96, 2, self.it * 11 + L["id"]), self.local_pv(lab, L)])
            X = np.concatenate([np.repeat(L["c"][None], len(pv), 0), np.full((len(pv), 1), 0.5), pv], 1)
            known = self.lot_known(lab, L, len(pv))
            ei, mu, _ = self.ei(net, X, 1.0, 1.0, 0.0, self.it, known)
            # value the confirmation build by its posterior mean (the alloy is already chosen), not EI over the claim
            acts.insert(0, dict(kind="print", lot=L["id"], pv=self.pick_pv(pv, mu), machine=("pt",)))
        return acts

    def finishing(self, lab, t, k_imm=6, near=0.05):
        acts = super().finishing(lab, t, k_imm, near)
        # confirmation coupons are judged against each other, not against the claim: they stop only when their
        # own readings fail
        acts = [a for a in acts if not (a["kind"] == "stop" and lab.coupons[a["coupon"]]["route"] == "gas"
                                        and not self.corr_fails(lab, lab.coupons[a["coupon"]]))]
        gas = [(lab.objective_meas(cp), cp) for cp in lab.coupons if cp["route"] == "gas" and cp["bars"]
               and not self.corr_fails(lab, cp)]
        if gas:
            best = max(o for o, _ in gas)
            for o, cp in sorted(gas, key=lambda x: -x[0])[:3]:
                if o < best - near:
                    break
                if cp["bars_pending"] == 0 and len(cp["bars"]) < 3 and cp["bars_left"] > 0:
                    acts.append(dict(kind="bars", coupon=cp["id"], n=3 - len(cp["bars"])))
                if cp["imm"] is None:
                    acts.append(dict(kind="imm", coupon=cp["id"]))
        return acts


class BOFNConfirmEarly(BOFNConfirm):
    name = "bofn_confirm_early"
    confirm = "early"


# --------------------------------------------------------------------------- conventional rounds
class Conv(Tiered):
    """Tiered screening in rounds: 4 builds a round, decided on Mondays after the round's bars are back."""

    name = "conv"
    ROUND = 4

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.round_items = []  # builds or lots of the current round still to come back
        self.want = []  # designs of the current round waiting for their lot

    def lot_for(self, lab, x):
        """The lot for design x: ('ready', lot), ('waiting', lot) or (None, None) if there is none or it failed."""
        key = lab.key(x[: self.nc])
        inflight = {i for k, i, _ in lab.inflight if k == "powder"}
        for L in lab.lots:
            if L["key"] != key or (L["a"] is not None and abs(L["a"] - x[self.nc]) > 0.05):
                continue
            if L["t_ready"] is not None and L["uses_left"] > 0:
                return "ready", L
            if L["id"] in inflight:
                return "waiting", L
        return None, None

    def decide(self, lab, t):
        self.it += 1
        acts = self.conv_finishing(lab, t)
        # prints for this round's designs whose lot has arrived; reorder a lot that came back unusable
        still = []
        for x in self.want:
            state, L = self.lot_for(lab, x)
            if state == "ready":
                acts.append(dict(kind="print", lot=L["id"], pv=self.round_pv(lab, L, x), machine="pt"))
            elif state == "waiting":
                still.append(x)
            else:
                acts.append(dict(kind="powder", c=x[: self.nc], a=float(x[self.nc]), route=self.powder_route))
                still.append(x)
        self.want = still
        busy = any(k in ("powder", "print", "bars") for k, _, _ in lab.inflight) or self.want
        untested = any(not lab.builds[cp["build"]]["failed"] and cp["rho_meas"] is not None and not cp["bars"]
                       and cp["bars_pending"] == 0 and cp["id"] in self._top_ids(lab) for cp in lab.coupons)
        if busy or untested or any(a["kind"] in ("bars", "print", "powder") for a in acts):
            return acts
        return acts + self.plan_round(lab, t)

    def _top_ids(self, lab):
        out = set()
        for b in lab.builds:
            if b.get("t_done") is not None and not b["failed"]:
                out.add(max(b["coupons"], key=lambda i: lab.coupons[i]["rho_meas"]))
        return out

    def conv_finishing(self, lab, t):
        acts = []
        inc = lab.claimed_value_meas()
        for i in self._top_ids(lab):
            cp = lab.coupons[i]
            if not cp["bars"] and cp["bars_pending"] == 0 and cp["bars_left"] == 3:
                acts.append(dict(kind="bars", coupon=i, n=3))
            elif cp["bars"] and cp["imm"] is None and cp["bars_pending"] == 0:
                o = lab.objective_meas(cp)
                if inc is None or o >= inc - 0.01:
                    acts.append(dict(kind="imm", coupon=i))
        return acts

    def round_pv(self, lab, L, x):
        tested = [cp for cp in lab.coupons if cp["key"] == L["key"] and cp["rho_meas"] is not None]
        if not tested:  # a first build: a small process DOE around the chosen setting
            base = np.array([x[self.nc + 1], x[self.nc + 2]])
            pts = [base] + [np.clip(base + d, 0, 1) for d in ([0.1, 0], [-0.1, 0], [0, 0.1], [0, -0.1], [0.1, 0.1])]
            return [tuple(p) for p in pts]
        M = ObjModel(lab, self)
        a = L["a"] if L["a"] is not None else 0.5
        pv = sobol(128, 2, self.it * 7 + L["id"])
        X = np.concatenate([np.repeat(L["c"][None], 128, 0), np.full((128, 1), a), pv], 1)
        ei, _ = M.cei(self.feats(X, 1.0, float(L["route"] == "gas")))
        return self.pick_pv(pv, ei)

    def plan_round(self, lab, t):
        acts = []
        tested = sum(1 for cp in lab.coupons if cp["bars"])
        SL = self.shortlist(lab)
        if tested < 3:
            designs = [np.concatenate([c, [0.5, 0.35, 0.1]]) for c in SL[: self.ROUND]]
        else:
            M = ObjModel(lab, self)
            P = self.pool(lab)
            gas = float(self.powder_route == "custom")
            ei, _ = M.cei(self.feats(P, 1.0, gas))
            idx = self.diverse(P, ei, self.ROUND, np.zeros((0, self.nc)))
            designs = [P[j] for j in idx]
            if float(ei[idx].max()) < 1e-4 and self.n_short < len(self.ranking(lab)):
                self.n_short += SCREEN_TOP
        for x in designs:
            state, L = self.lot_for(lab, x)
            if state == "ready":
                acts.append(dict(kind="print", lot=L["id"], pv=self.round_pv(lab, L, x), machine="pt"))
            else:
                if state is None:
                    acts.append(dict(kind="powder", c=x[: self.nc], a=float(x[self.nc]), route=self.powder_route))
                self.want.append(x)
        return acts


POLICIES = {"random": Random, "tiered": Tiered, "gpbo": GPBO, "bofn": BOFN, "pkgfn": PKGFN, "conv": Conv,
            "bofn_confirm": BOFNConfirm, "bofn_confirm_early": BOFNConfirmEarly}
