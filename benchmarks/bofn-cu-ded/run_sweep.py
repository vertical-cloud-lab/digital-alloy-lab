"""Run (policy x cell x seed) jobs in parallel; one JSON per job, resumable.

    python run_sweep.py --cells 1,1 --seeds 0-19 --kinds pkgfn eifn eifn_reuse tiered ei random

A cell is (kappa, eta). Results go to results/k<kappa>e<eta>/<kind>_s<seed>.json.
"""

import argparse
import json
import os
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

OUT = Path(__file__).parent / "results"
SLOW = ("pkgfn", "pkgfn_screen", "pkgfn_audit", "mines_only")


def cell_dir(kappa, eta):
    return f"k{kappa:g}e{eta:g}"


LEGACY = {"TRUTH": "toy"}  # runs stored before a setting existed had its default


def mismatch(stored, settings, budget):
    """The settings (and budget) a stored run differs in, as text; empty if it can be resumed."""
    have = stored.get("settings", {})
    diff = [f"{k}: {have.get(k, LEGACY.get(k, 'missing'))} vs {v}" for k, v in settings.items() if have.get(k, LEGACY.get(k)) != v]
    if float(stored.get("budget", -1)) != float(budget):
        diff.append(f"budget: {stored.get('budget')} vs {budget}")
    return "; ".join(diff)


def code_hash():
    """sha256 of the code a run used (stored with the run, for provenance)."""
    import hashlib

    h = hashlib.sha256()
    for f in ("bofn_alloy.py", "policies.py", "truth_phys.py"):
        fp = Path(__file__).parent / f
        if fp.exists():
            h.update(fp.read_bytes())
    return h.hexdigest()


def job(args):
    kind, kappa, eta, seed, budget, out = args
    warnings.filterwarnings("ignore")
    import torch

    torch.set_num_threads(1)
    from policies import run

    from policies import settings_for

    path = Path(out) / cell_dir(kappa, eta) / f"{kind}_s{seed}.json"
    if path.exists():
        # resume only a run stored with the same budget and settings (Edison F9: a stale file with other
        # Monte Carlo settings, budget or truth used to be reused silently)
        stored = json.loads(path.read_text())
        diff = mismatch(stored, settings_for(kind), budget)
        if diff:
            return f"REFUSED {path}: stored with other settings ({diff}); move it away to re-run", -1.0
        return str(path), 0.0
    t0 = time.time()
    res = run(kind, kappa, eta, seed, budget)
    res["wall_s"] = time.time() - t0
    res["code_sha256"] = code_hash()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(res))
    return str(path), res["wall_s"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", nargs="+", default=["1,1"], help="kappa,eta pairs")
    ap.add_argument("--seeds", default="0-19")
    ap.add_argument("--kinds", nargs="+", default=["pkgfn", "eifn", "eifn_reuse", "tiered", "ei", "random"])
    ap.add_argument("--budget", type=float, default=100_000)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", default=str(OUT), help="results folder (default results/; use another folder for convergence checks)")
    a = ap.parse_args()
    lo, hi = (int(v) for v in a.seeds.split("-"))
    cells = [tuple(float(v) for v in c.split(",")) for c in a.cells]
    jobs = [(k, kap, eta, s, a.budget, a.out) for (kap, eta) in cells for s in range(lo, hi + 1) for k in a.kinds]
    jobs.sort(key=lambda j: j[0] not in SLOW)  # the pKGFN runs first, so the fast ones fill the last cores
    refused = 0
    with Pool(a.workers) as pool:
        for path, wall in pool.imap_unordered(job, jobs):
            refused += wall < 0
            print(f"{time.strftime('%H:%M:%S')} {path} {max(wall, 0):.0f}s", flush=True)
    if refused:
        raise SystemExit(f"{refused} stored run(s) have other settings; nothing was overwritten")


if __name__ == "__main__":
    main()
