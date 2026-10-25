"""Two independent Edison Analysis reviews of this benchmark (code; analysis), as for bofn-prelim.

    python edison/edison_review.py settings          # write edison/settings.md
    python edison/edison_review.py submit code       # upload files, submit, record the task id in edison/tasks.json
    python edison/edison_review.py submit analysis
    python edison/edison_review.py wait              # foreground: poll every task until done, then fetch
    python edison/edison_review.py fetch             # save transcripts and outputs under edison/results/

The API key is read from EDISON_PLATFORM_API_KEY and never printed.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
TASKS = HERE / "tasks.json"
OUT = HERE / "results"
UPLOAD = Path("/tmp/edison-upload-cu")
FILES = {
    "code-review": ["bofn_alloy.py", "policies.py", "run_sweep.py", "check_truth.py", "analyze.py", "plot.py", "README.md", "truth_tables.md", "edison/settings.md"],
    "analysis-review": ["README.md", "tables.md", "analyze.py", "plot.py", "bofn_alloy.py", "policies.py", "truth_tables.md", "truth_tables.json", "edison/settings.md",
                        "bofn_cu_best_vs_spend_k1_partial_vs_full.png"],
}
BRIEF = {"code-review": HERE / "brief-code.md", "analysis-review": HERE / "brief-analysis.md"}
DONE = {"success", "fail", "failed", "cancelled", "error"}


def client():
    from edison_client import EdisonClient

    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def settings():
    import botorch
    import gpytorch
    import torch

    sys.path.insert(0, str(ROOT))
    import policies as PO
    from bofn_alloy import COSTS, F_CRACK, F_SAFE, FULL_COST, GATE_SCALE, LAMBDA, M_FIRST, M_REF, M_SCALE_UP, P_CAP, SESSIONS_PER_LOT

    tt = json.loads((ROOT / "truth_tables.json").read_text())
    runs = sorted((ROOT / "results").glob("k*/*.json"))
    L = ["# Settings of the uploaded runs", "",
         f"- Python {platform.python_version()}, torch {torch.__version__}, botorch {botorch.__version__}, gpytorch {gpytorch.__version__}; CPU only, one thread per run.",
         f"- pKGFN Monte Carlo: S_ACQ = {PO.S_ACQ} base samples, N_CAND = {PO.N_CAND} candidates per stage, N_POOL = {PO.N_POOL} Sobol designs per iteration; "
         f"10 Gauss-Hermite nodes for one-output stages, a 2-point product rule (16 points) for the four CALPHAD outputs. Environment variables BOFN_SACQ, BOFN_NCAND, BOFN_NPOOL, BOFN_REC were unset (defaults).",
         f"- Seed data per seed: CALPHAD on {PO.N_CALPHAD0} Sobol compositions plus {PO.N_FULL0} random designs through every stage; spend counted from zero afterwards. Budget $100,000 of new spend.",
         f"- Costs (USD): {json.dumps(COSTS)}; the first Mines session on a lot adds the ${M_SCALE_UP:,.0f} 2 kg scale-up (${M_FIRST:,.0f} in all); a scaled-up lot supports {SESSIONS_PER_LOT} sessions; a full chain on a new composition is ${FULL_COST:,.0f}.",
         f"- Truth constants: crack onset F_CRACK = {F_CRACK}, CALPHAD screen F_SAFE = {F_SAFE}, Utah power cap {P_CAP}, immersion gate scale {GATE_SCALE}, lambda = {LAMBDA}, m_ref = {M_REF:.6f}.",
         f"- Screening policies: Utah density gate rho_u >= {PO.RHO_GATE}; one-hour screen gate = the {PO.W_QUANTILE:.0%} quantile of every w observed so far; tiered shortlist: top {PO.SCREEN_TOP} of {PO.SCREEN_N} compositions; funnel k = {PO.FUNNEL_K}; audit near-cutoff margins {PO.NEAR}.",
         "- Required properties of the truth (from the specification; checked by check_truth.py, results in truth_tables.md): (1) at (kappa, eta) = (1, 1) the optimum fails the CALPHAD crack screen or ranks below the top quartile of dense candidates on the one-hour screen, so tiered screening cannot reach it; at (0, 0) the screens keep at least 85% of the optimum; (2) C71500 passes immersion by definition (m_ref), C95800 (NAB) is stronger and, deposited fast and cool, carries beta-prime and fails immersion, C70600 is weaker, uses less nickel and passes; (3) the optimum is a ridge in (P, v), not a point; (4) copper-rich compositions (low Ni and Al) cannot fuse at Utah's power cap but can at Mines.",
         "- True optima per (kappa, eta) cell, by multi-start local search from the best of 400,000 random designs (truth_tables.json): "
         + "; ".join(f"({r['kappa']:g}, {r['eta']:g}): J* = {r['optimum']:.6f} at x = {r['x_opt']}" for r in tt) + ".",
         f"- Runs uploaded: {len(runs)} JSON files in results.zip, as results/k<kappa>e<eta>/<policy>_s<seed>.json.", ""]
    (HERE / "settings.md").write_text("\n".join(L))
    print("\n".join(L))


def submit(name):
    from edison_client import JobNames, TaskRequest

    UPLOAD.mkdir(parents=True, exist_ok=True)
    zpath = UPLOAD / "results.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted((ROOT / "results").glob("k*/*.json")):
            z.write(p, p.relative_to(ROOT))
    c = client()
    uploads = []
    for f in FILES[name] + [str(zpath)]:
        p = Path(f) if Path(f).is_absolute() else ROOT / f
        entry = c.upload_file(str(p))
        uploads.append({"file": p.name, "entry_id": str(entry)})
        print("uploaded", p.name, flush=True)
    req = TaskRequest(name=JobNames.ANALYSIS, query=BRIEF[name].read_text())
    task_id = c.create_task(task_data=req, files=[u["entry_id"] for u in uploads])
    tasks = json.loads(TASKS.read_text()) if TASKS.exists() else {}
    tasks[name] = {"task_id": str(task_id), "job": "ANALYSIS", "uploads": uploads, "submitted": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "brief": f"benchmarks/bofn-cu-ded/edison/{BRIEF[name].name}", "runs_uploaded": len(list((ROOT / "results").glob("k*/*.json")))}
    TASKS.write_text(json.dumps(tasks, indent=1))
    print(name, "task", task_id, flush=True)


def wait(max_minutes=float(os.environ.get("EDISON_WAIT_MIN", 45)), every=240):
    c = client()
    tasks = json.loads(TASKS.read_text())
    t0 = time.time()
    while True:
        status = {}
        for name, t in tasks.items():
            status[name] = str(c.get_task(task_id=t["task_id"]).status)
        print(time.strftime("%H:%M:%S"), status, flush=True)
        if all(s in DONE for s in status.values()) or time.time() - t0 > max_minutes * 60:
            break
        time.sleep(every)
    fetch()


def fetch():
    c = client()
    tasks = json.loads(TASKS.read_text())
    OUT.mkdir(exist_ok=True)
    for name, t in tasks.items():
        task = c.get_task(task_id=t["task_id"], verbose=True)
        d = task.model_dump(mode="json") if hasattr(task, "model_dump") else json.loads(task.json())
        status = str(d.get("status"))
        t["status"] = status
        if status not in DONE:
            print(name, "still", status)
            continue
        (OUT / f"{name}.json").write_text(json.dumps(d, indent=1))
        state = (d.get("environment_frame") or {}).get("state") or {}
        answer = (state.get("state") or {}).get("answer") or ""
        if answer:
            (OUT / f"{name}.md").write_text(answer)
        for o in (state.get("info") or {}).get("output_data") or []:
            fn = o.get("filename", "")
            if fn.endswith((".md", ".ipynb", ".csv", ".txt", ".json", ".py")):
                try:
                    got = c.fetch_data_from_storage(o["entry_id"])
                    if isinstance(got, Path):
                        data = got.read_bytes()
                    elif isinstance(got, list) and got and isinstance(got[0], Path):
                        data = got[0].read_bytes()
                    elif hasattr(got, "content"):
                        data = got.content if isinstance(got.content, bytes) else str(got.content).encode()
                    else:
                        data = str(got).encode()
                    (OUT / f"{name}-{fn}").write_bytes(data)
                    print(name, "saved", fn)
                except Exception as e:  # keep going; the transcript JSON holds the answer
                    print(name, "could not fetch", fn, type(e).__name__)
        print(name, status, "saved")
    TASKS.write_text(json.dumps(tasks, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "settings":
        settings()
    elif cmd == "submit":
        submit(sys.argv[2] if sys.argv[2].endswith("-review") else f"{sys.argv[2]}-review")
    elif cmd == "wait":
        wait()
    elif cmd == "fetch":
        fetch()
