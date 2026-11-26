"""Why does bofn-prelim's pKGFN fall behind tiered screening when the screen is right (kappa = 0)?

Runs bofn-prelim's own `policies.run_pkgfn` unchanged, with three probes added from outside:

* every call to `Network.kg` is logged (the best KG of each stage at each iteration), so we can see whether the
  knowledge gradient of finishing a part (tensile, "T") is ever exactly zero, which is the failure byu-vcl's round-3
  port found (an incumbent of 0 and a never-negative utility make KG of finishing exactly 0);
* after every purchase, the *restricted ceiling*: the best true objective over every design whose composition has
  been simulated (bofn-prelim's pKGFN may only atomize simulated compositions), with the atomizer setting and laser
  settings at their best, found on a grid;
* the same for the composition nearest the optimum.

Variant `--calphad0 256` gives pKGFN the 256 CALPHAD compositions that tiered screening simulates (and charges it
for the 224 extra calls, as tiered pays for them), which tests the explanation without changing pKGFN's logic.

Usage (needs torch and botorch, as bofn-prelim does):
    python diagnose.py <path to benchmarks/bofn-prelim> <kappa> <seed> <out.json> [--calphad0 N] [--kind pkgfn_la]

`--kind pkgfn_la` runs bofn-prelim's own lookahead variant (a new powder is also valued by what printing it would
reveal), still restricted to simulated compositions, which separates the two explanations.
"""
from __future__ import annotations

import json
import os
import sys
import time

os.environ.setdefault("BOFN_NO_REC", "1")
PRELIM = os.path.abspath(sys.argv[1])
sys.path.insert(0, PRELIM)

import torch  # noqa: E402

import bofn_alloy  # noqa: E402
import policies  # noqa: E402

KAPPA, SEED, OUT = float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
CAL0 = int(sys.argv[sys.argv.index("--calphad0") + 1]) if "--calphad0" in sys.argv else policies.N_CALPHAD0
KIND = sys.argv[sys.argv.index("--kind") + 1] if "--kind" in sys.argv else "pkgfn"  # pkgfn | pkgfn_la | pkgfn_free
OPT = {1.0: 0.693739, 0.5: 0.530736, 0.0: 0.484755}[KAPPA]  # bofn-prelim README / analyze.optimum
OPT_C = {0.0: [0.28, 0.19, 0.0, 0.0], 0.5: [0.35, 0.27, 1.0, 0.0], 1.0: [0.65, 0.60, 1.0, 0.0]}[KAPPA]

truth = bofn_alloy.AlloyTruth(KAPPA)
A_GRID = torch.linspace(0, 1, 201)
PV = torch.cartesian_prod(torch.linspace(0, 1, 101), torch.linspace(0, 1, 101))


def best_over_process(c):
    """Best true objective for composition c [4] over (a, P, v): q is maximised over a first (rho rises with q)."""
    s, f, g = (float(truth.node(n, c)) for n in ("s", "f", "g"))
    q = truth.node("q", torch.stack([A_GRID, torch.full_like(A_GRID, g)], -1)).max()
    inp = torch.cat([PV, torch.tensor([[f, g, float(q)]]).expand(PV.shape[0], 3)], -1)
    rho = truth.node("rho", inp).max()
    U = (0.25 + 0.75 * s) * rho
    return float(U - bofn_alloy.LAMBDA * bofn_alloy.burden(torch.cat([c, torch.zeros(3)])))


_ceil_cache = {}


def ceiling(d):
    best, best_c = -9.0, None
    for k in d.calphad:
        if k not in _ceil_cache:
            _ceil_cache[k] = best_over_process(torch.tensor(k))
        if _ceil_cache[k] > best:
            best, best_c = _ceil_cache[k], k
    return best, best_c


KG_CALLS = []
_kg = bofn_alloy.Network.kg


def kg_logged(self, group, Z, Xi, eps, w, ww, chunk=4):
    out = _kg(self, group, Z, Xi, eps, w, ww, chunk)
    KG_CALLS.append((group, out.detach().clone()))
    return out


bofn_alloy.Network.kg = kg_logged

_init = policies.initial_data


def initial_data(truth_, seed):
    d, lab = _init(truth_, seed)
    if CAL0 != 32:
        # extra CALPHAD compositions, paid for (tiered screening pays for its 224 extra calls the same way)
        for c in bofn_alloy.sobol(CAL0, policies.NC, seed=4000 + seed)[: CAL0 - policies.N_CALPHAD0]:
            lab.calphad(c)
    return d, lab


policies.initial_data = initial_data
policies.N_CALPHAD0 = 32  # the shared seed set is unchanged; extra compositions come from tiered's own Sobol stream

ITER = []
_rec_call = policies.Recorder.__call__


def rec_logged(self, net, it, action):
    _rec_call(self, net, it, action)
    d = self.d
    cbest, ckey = ceiling(d)
    kg_by = {}
    for grp, v in KG_CALLS:
        kg_by[grp] = max(kg_by.get(grp, 0.0), float(v.max()) if v.numel() else 0.0)
    nT = sum(int(v.numel()) for g, v in KG_CALLS if g == "T")
    zT = sum(int((v <= 1e-12).sum()) for g, v in KG_CALLS if g == "T")
    dist = min(float(torch.tensor(k).sub(torch.tensor(OPT_C)).norm()) for k in d.calphad)
    ITER.append(dict(it=it, action=action, spent=d.spent, best_validated=self.rows[-1]["best_validated"] / OPT,
                     ceiling=cbest / OPT, ceiling_comp=[round(x, 3) for x in ckey] if ckey else None,
                     n_comps=len(d.calphad), nearest_to_opt=dist, kg_max=kg_by, kg_T_scored=nT, kg_T_zero=zT,
                     fallback=bool(self.rows[-1].get("fallback", False))))
    KG_CALLS.clear()


policies.Recorder.__call__ = rec_logged


t0 = time.time()
out = policies.run(KIND, KAPPA, SEED, 100_000)
# the fallback flag is written into rows after the recorder call; copy it over
for r, row in zip(ITER, out["rows"]):
    r["fallback"] = bool(row.get("fallback", False))
json.dump(dict(kind=KIND, kappa=KAPPA, seed=SEED, calphad0=CAL0, seconds=round(time.time() - t0, 1), counts=out["counts"],
               final_best_validated=out["rows"][-1]["best_validated"] / OPT, iters=ITER,
               actions=[r["action"] for r in out["rows"]]), open(OUT, "w"))
print(f"{KIND} kappa={KAPPA} seed={SEED} calphad0={CAL0}: best {100 * out['rows'][-1]['best_validated'] / OPT:.1f}% "
      f"ceiling {100 * ITER[-1]['ceiling']:.1f}% counts {out['counts']} {time.time() - t0:.0f}s", flush=True)
