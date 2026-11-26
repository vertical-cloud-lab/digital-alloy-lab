"""Run (network x scenario x strategy x seed) campaigns in parallel; one JSON per run, resumable.

    python run_sweep.py --net al --kappa 1 --scenario mixed --strategies all --seeds 0-19
    python run_sweep.py --plan plan.txt          # one "net kappa scenario strategies seeds" per line

Every run is its own process (the two networks share a module name), so a crash or a stuck run
only costs that run. Results go to results/<net>-k<kappa>/<scenario>/<strategy>_s<seed>.json.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
import warnings
from multiprocessing import get_context
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
ALL = ("nofail", "drop", "abandon", "partial", "keep", "impute", "viab_x", "viab_x_partial", "viab_node", "viab_node_ec")


def path_for(net, kappa, scenario, strategy, seed, out=OUT):
    """`net` may carry "+full" for the full-pipeline policy (no lot reuse): results/<net>-k<kappa>-full/..."""
    base, _, variant = net.partition("+")
    return Path(out) / (f"{base}-k{kappa:g}" + (f"-{variant}" if variant else "")) / scenario / f"{strategy}_s{seed}.json"


def one(job):
    net_name, kappa, scenario, strategy, seed, out = job
    path = path_for(net_name, kappa, scenario, strategy, seed, out)
    if path.exists():
        return str(path), 0.0, "exists"
    warnings.filterwarnings("ignore")
    import torch

    torch.set_num_threads(1)
    sys.path.insert(0, str(HERE))
    from netload import load
    from policy import run

    base, _, variant = net_name.partition("+")
    net = load(base)
    t0 = time.time()
    try:
        # the "nofail" reference keeps every result (any strategy gives the same run without failures)
        res = run(net, "partial" if strategy == "nofail" else strategy, "nofail" if strategy == "nofail" else scenario, kappa, seed,
                  reuse=variant != "full")
        res["variant"] = variant or "reuse"
        res["strategy"], res["scenario"] = strategy, scenario
    except Exception:
        return str(path), time.time() - t0, "ERROR " + traceback.format_exc()[-600:]
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(res))
    os.replace(tmp, path)
    return str(path), time.time() - t0, "ok"


def parse_seeds(s):
    lo, hi = (int(v) for v in s.split("-"))
    return range(lo, hi + 1)


def jobs_from(net, kappa, scenario, strategies, seeds, out):
    strats = ALL if strategies == ["all"] else strategies
    return [(net, kappa, scenario, st, s, out) for s in parse_seeds(seeds) for st in strats]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--net", help="al, cu-toy or cu-phys; add +full for the full-pipeline policy")
    ap.add_argument("--kappa", type=float, default=1.0)
    ap.add_argument("--scenario", default="mixed")
    ap.add_argument("--strategies", nargs="+", default=["all"])
    ap.add_argument("--seeds", default="0-19")
    ap.add_argument("--plan", help="file with one 'net kappa scenario seeds strategy...' per line, run in order")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    jobs = []
    if a.plan:
        for line in Path(a.plan).read_text().splitlines():
            line = line.split("#")[0].strip()
            if not line:
                continue
            net, kappa, scenario, seeds, *strategies = line.split()
            jobs += jobs_from(net, float(kappa), scenario, strategies, seeds, a.out)
    else:
        jobs = jobs_from(a.net, a.kappa, a.scenario, a.strategies, a.seeds, a.out)
    todo = [j for j in jobs if not path_for(*j[:5], out=j[5]).exists()]
    print(f"{time.strftime('%H:%M:%S')} {len(jobs)} runs, {len(todo)} to do", flush=True)
    ctx = get_context("spawn")
    with ctx.Pool(a.workers, maxtasksperchild=1) as pool:
        for path, wall, status in pool.imap(one, todo):
            print(f"{time.strftime('%H:%M:%S')} {path} {wall:.0f}s {status}", flush=True)


if __name__ == "__main__":
    main()
