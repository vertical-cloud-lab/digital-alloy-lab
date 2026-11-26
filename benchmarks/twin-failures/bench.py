"""Failed vs. abandoned atomizer runs in a simulated year of the vertical lab, both campaigns at once (DAL #274).

Runs the byu-vcl twin's round-3 engine (``Twin(mode="async")``, pinned in ``get_twin.sh``) with a failure regime from
``failures.py`` and, for both campaigns, round 3's time-aware BOFN with a failure-handling strategy from
``strategies.py``. The heuristic, random and GP-BO run as round 3 has them, for context.

    export TWIN_DIR=/tmp/byu-vcl/vertical-lab               # get_twin.sh puts it there
    python bench.py run main [twin ...]                      # -> results/<experiment>.jsonl (TWIN_WORKERS processes)
    python bench.py one STRATEGY [REGIME] [DAYS]             # one run, printed
    python bench.py list                                     # the experiments and their sizes

Runs are ordered seed by seed, so a run cut short still has every strategy on the same seeds.
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
TWIN_DIR = os.environ.get("TWIN_DIR", "/tmp/byu-vcl/vertical-lab")
sys.path.insert(0, TWIN_DIR)
sys.path.insert(0, str(HERE))
OUT = Path(os.environ.get("TWINFAIL_OUT", HERE / "results"))

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

STRATS_MAIN = ("bad_value", "drop", "abandon", "retry", "viability_x", "viability_node")
BASE = ("heuristic", "random", "gpbo")


def cfg(policy, seed, regime="lab", diag_acc=0.8, days=365, **kw):
    return dict(policy=policy, seed=seed, regime=regime, diag_acc=diag_acc, days=days, facility="vertical_lab",
                stock="stocked", crucible=225, reuse=True, scenario="historical", **kw)


def _seedwise(policies, seeds, **kw):
    return [cfg(p, s, **kw) for s in seeds for p in policies]


EXPERIMENTS = {
    "smoke": [cfg(p, 0, days=40) for p in ("bad_value", "drop", "retry", "viability_x", "viability_node", "oracle",
                                            "heuristic")],
    # the main benchmark: the lab's record (learning curve, damage), six strategies, seven seeds, paired (a BOFN year
    # with both campaigns took 13-19 min with four on the runner, so this is what fit in the job's six hours)
    "main": _seedwise(STRATS_MAIN, range(7), regime="lab"),
    # the cheap baselines on every regime, eight seeds
    "base": [cfg(p, s, regime=r) for s in range(8) for r in ("lab", "lab_region", "twin") for p in BASE],
    # the cheap references that fit: round 3's heuristic, random and GP-BO with round 3's own failure handling
    "base_lite": ([cfg(p, s, regime="lab") for s in range(5) for p in BASE] +
                  [cfg(p, s, regime="lab_region") for s in range(3) for p in ("heuristic", "random")]),
    # round 3's own failure law: does the ranking hold when failures are rare?
    "twin": _seedwise(("bad_value", "drop", "abandon", "viability_x", "viability_node"), range(6), regime="twin"),
    # the hidden region that won't atomize: when abandoning a composition is right
    "region": _seedwise(("bad_value", "drop", "abandon", "viability_x", "viability_node"), range(3),
                        regime="lab_region"),
    # what the diagnosis is worth: no diagnosis, the lab's (0.8), perfect
    "diag": _seedwise(("viability_node_nodiag", "oracle"), range(4), regime="lab"),
}


def run_id(c):
    return f"{c['policy']}_{c['regime']}_q{c['diag_acc']}_d{c['days']}_s{c['seed']}"


def _ledger_stats(camp):
    """Per campaign: runs and attempts by outcome and true cause, repeat failures, compositions given up."""
    L = camp.atom_ledger
    out = dict(runs=len(L), failed=sum(1 for e in L if not e["ok"]),
               failed_intrinsic=sum(1 for e in L if not e["ok"] and e["cause"] == "intrinsic"),
               failed_transient=sum(1 for e in L if not e["ok"] and e["cause"] == "transient"),
               misdiagnosed=sum(1 for e in L if not e["ok"] and e["diag"] != e["cause"]))
    ev = {}
    for e in L:
        g = ev.setdefault(e["event"], dict(design=e["design"], ok=0, n=0, causes=set()))
        g["n"] += 1
        g["ok"] += e["ok"]
        if not e["ok"]:
            g["causes"].add(e["cause"])
    by_d = {}
    for g in ev.values():
        d = by_d.setdefault(g["design"], dict(attempts=0, failed=0, made=0, causes=set()))
        d["attempts"] += 1
        d["failed"] += g["ok"] == 0
        d["made"] += g["ok"] > 0
        d["causes"] |= g["causes"]
    out.update(attempts=len(ev), failed_attempts=sum(1 for g in ev.values() if g["ok"] == 0),
               designs=len(by_d),
               # a composition whose attempts all failed, only ever from transient causes: given up on by chance
               given_up_transient=sum(1 for d in by_d.values() if d["made"] == 0 and d["causes"] == {"transient"}),
               given_up_intrinsic=sum(1 for d in by_d.values() if d["made"] == 0 and "intrinsic" in d["causes"]),
               # failed attempts after the composition's first failed attempt from its inputs
               repeat_intrinsic=sum(max(0, d["failed"] - 1) for d in by_d.values() if "intrinsic" in d["causes"]),
               retried_designs=sum(1 for d in by_d.values() if d["attempts"] > 1))
    return out


def run_one(c: dict) -> dict:
    import torch
    torch.set_num_threads(1)
    from twin import bench2 as B2
    from twin import campaign as C
    from twin import spaces as SP
    from twin.opt import policies3 as P3
    from twin.opt.gp import STATS

    import failures as F
    import strategies as ST
    t0 = time.time()
    bud = {"flaime_al": B2.BUDGET["flaime_al"], "onr_cu": B2.BUDGET["onr_cu"]}
    specs = {k: C.Spec(k, bud[k], B2.WIP[k], c["seed"], 1.0, crucible_cm3=c["crucible"], reuse=c["reuse"],
                       stock=c["stock"], cu_hidden=0.0, fidelity="fast") for k in bud}
    if c["policy"] in ST.FMODES:
        pols = {k: ST.make(c["policy"], k, c["seed"]) for k in specs}
    else:
        pols = {k: P3.make3(c["policy"], k, c["seed"], None) for k in specs}
    tw = C.Twin(specs, pols, scenario=c["scenario"], facility=c["facility"], seed=c["seed"],
                horizon_days=c["days"], mode="async")
    F.install(tw, c["regime"], seed=c["seed"], diag_acc=c["diag_acc"])
    s = tw.run()
    out = dict(cfg=c, seconds=round(time.time() - t0, 1), gp=dict(STATS), fail=F.summary(tw), campaigns={})
    for k in specs:
        cs = s[k]
        camp = tw.campaigns[k]
        refs = [{e: w.get(e, 0.0) for e in SP.SPACES[k].elements} for w in SP.REFERENCE[k].values()]
        for d in cs["demonstrated"]:
            comp = camp.designs[d["design"]]["composition"]
            d["ref"] = any(all(abs(comp.get(e, 0.0) - r[e]) < 0.06 for e in r) for r in refs)
        new = sorted([d for d in cs["demonstrated"] if not d["ref"]], key=lambda d: d["t_h"])
        best, curve_new = 0.0, []
        for d in new:
            best = max(best, d["u"])
            curve_new.append((round(d["t_h"] / 24.0, 3), round(d["spent"], 2), round(best, 4)))
        pol = pols[k]
        out["campaigns"][k] = dict(
            spent=round(cs["spent"], 2), budget=cs["budget"], best=cs["best"], best_new=best, curve_new=curve_new,
            n_demonstrated=cs["n_demonstrated"], n_new_demonstrated=len(new),
            n_new_alloys=len({d["design"] for d in new}), n_designs=cs["n_designs"], n_lots=cs["n_lots"],
            n_builds=cs["n_builds"], done=cs["done"], status=cs["status"], n_alloys_made=cs["n_alloys_made"],
            spend_by=cs["spend_by"], ledger=_ledger_stats(camp),
            fcounts=dict(getattr(pol, "fcounts", {}) or {}),
            policy_counts={kk: vv for kk, vv in (getattr(pol, "counts", {}) or {}).items()})
    f = next(iter(tw.facilities.values()))
    out["utilization"] = {k: round(x, 4) for k, x in f.utilization(tw.h).items()}
    out["atomizer_busy_h"] = round(f.res["atomizer"].busy_h, 1)
    out["atomizer_down_h"] = round(sum(min(b, tw.h) - a for a, b in f.res["atomizer"].down if a < tw.h), 1)
    return out


def _safe(c):
    try:
        return run_one(c)
    except Exception:
        import traceback
        return dict(cfg=c, error=traceback.format_exc()[-4000:])


def _jsonable(x):
    import numpy as np
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, set):
        return sorted(_jsonable(v) for v in x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x


def load(name):
    p = OUT / f"{name}.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def run(names, workers):
    OUT.mkdir(parents=True, exist_ok=True)
    todo = []
    for name in names:
        done = {run_id(r["cfg"]) for r in load(name)}
        mine = [c for c in EXPERIMENTS[name] if run_id(c) not in done]
        print(f"{name}: {len(mine)} runs to do ({len(done)} done)", flush=True)
        todo += [(name, c) for c in mine]
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        futs = {ex.submit(_safe, c): (name, c) for name, c in todo}
        for fut in as_completed(futs):
            name, c = futs[fut]
            res = fut.result()
            if "error" in res:
                with (OUT / f"{name}.errors.jsonl").open("a") as fh:
                    fh.write(json.dumps(_jsonable(res)) + "\n")
                print(f"  {name} {run_id(c)}: ERROR {res['error'].strip().splitlines()[-1]}", flush=True)
                continue
            with (OUT / f"{name}.jsonl").open("a") as fh:
                fh.write(json.dumps(_jsonable(res)) + "\n")
            a, u = res["campaigns"]["flaime_al"], res["campaigns"]["onr_cu"]
            print(f"  {name} {run_id(c)}: Al {a['best_new']:.3f} ({a['ledger']['failed']}/{a['ledger']['runs']} runs "
                  f"failed) Cu {u['best_new']:.3f} ({u['ledger']['failed']}/{u['ledger']['runs']}) down "
                  f"{res['fail']['down_days']:.0f} d; {res['seconds']:.0f} s, {time.time() - t0:.0f} s in", flush=True)


def main(argv):
    if not argv or argv[0] == "list":
        for k, v in EXPERIMENTS.items():
            print(k, len(v))
        return
    if argv[0] == "run":
        run(argv[1:] or ["main"], int(os.environ.get("TWIN_WORKERS", "4")))
        return
    if argv[0] == "one":
        c = cfg(argv[1], 0, regime=argv[2] if len(argv) > 2 else "lab", days=int(argv[3]) if len(argv) > 3 else 365)
        r = run_one(c)
        print(json.dumps(_jsonable({k: dict(best_new=v["best_new"], n_new=v["n_new_demonstrated"], ledger=v["ledger"],
                                            fcounts=v["fcounts"]) for k, v in r["campaigns"].items()}), indent=1))
        print(json.dumps(_jsonable(r["fail"])), r["seconds"], "s")
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
