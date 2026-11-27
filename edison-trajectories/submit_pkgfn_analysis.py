"""Fire an Edison ANALYSIS task asking why pKGFN underperforms on the 6-node
benchmark, with the benchmark code, composite figure, raw results zip, the
new node-correlation figure, and the latest manuscript attached.

Does NOT wait. Task ID is appended to
``edison-trajectories/pending-edison-tasks.json`` for next-session retrieval.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from edison_client import EdisonClient
from edison_client.models import TaskRequest, RuntimeConfig
from edison_client.models.app import JobNames

REPO = Path(__file__).resolve().parents[1]

FILES_TO_UPLOAD = [
    # Benchmark code (so the analyst can inspect the implementation).
    "benchmarks/bofn_actions_benchmark.py",
    "benchmarks/partial_kgfn/manufacturing_problem.py",
    "benchmarks/partial_kgfn/gp_network.py",
    "benchmarks/bofn_pkgfn_demo.py",
    "benchmarks/bofn_node_correlations.py",
    # Composite result figure + summary + raw per-seed JSONs (zipped).
    "benchmarks/figures/actions_full/bofn_actions_cost_efficiency.png",
    "benchmarks/figures/actions_full/bofn_actions_summary.json",
    "benchmarks/results/actions_full/bofn-combined-24736409107.zip",
    # Node correlation grid (R² matrix + figure).
    "benchmarks/figures/node_correlations.png",
    "benchmarks/figures/node_correlations.json",
    # Latest manuscript (PR #58 draft living in the repo root).
    "main (2).pdf",
]

QUERY = """We ran a cost-matched BOFN benchmark comparing 7 algorithms on a
6-node DAG ExtendedManufacturingGPNetwork (y0..y5; full pipeline cost $120;
per-node costs [5,10,10,45,20,30]; noise_std=0.05 i.i.d. Gaussian;
$2,400 budget ≈ 20 full pipelines; 20 seeds; init 9 full Sobol evals;
true-max of noiseless y5 over 16,384 Sobol points is 1.297).

Results (mean±std over 20 seeds of posterior mean on 200-Sobol grid of y5):

| Algorithm   | Final mean | ± std  | Avg iters |
|-------------|-----------:|-------:|----------:|
| TSFN        | 1.177      | 0.062  | 11.0      |
| HighFidOnly | 1.150      | 0.114  | 11.0      |
| pKGFN       | 1.043      | 0.130  | 44.0      |
| Sobol       | 1.004      | 0.103  | 11.0      |
| Random      | 1.000      | 0.130  | 11.0      |
| LowFidOnly  | 0.894      | 0.162  | 264.0     |
| Node2Only   | 0.894      | 0.161  | 132.0     |

Questions we'd like you to explore:

1. **Why is pKGFN underperforming?** In the original Astudillo & Frazier
   BOFN papers and the Buathong et al. p-KGFN (NeurIPS 2024) paper, pKGFN
   should dominate TSFN at equal cost because it can cheaply probe the
   root CALPHAD node. On our 6-node extended problem pKGFN trails TSFN
   (1.043 vs 1.177) and even HighFidOnly (1.150), despite using 4× more
   acquisition iterations. Please inspect the pKGFN implementation in
   `benchmarks/bofn_actions_benchmark.py` (the `pkgfn_step` call inside
   the main loop) and `benchmarks/bofn_pkgfn_demo.py` / `partial_kgfn/*`.
   What could be wrong? Possibilities to evaluate:
     - Fantasy sample size too small; bias in the inner KG optimization.
     - Poor parent-GP fits for downstream nodes when we only ever probe
       roots (does pKGFN ever pick intermediate/terminal nodes here?).
     - Node-selection logic — are we properly normalising KG value by
       node cost? Are costs $5/$10/$10/$45/$20/$30 consistent with how
       pKGFN weights them?
     - Numerical issues with the Matheron-path synthetic ground truth.
     - Bounds / parent_bounds mismatch between node 4 (active x4, parent
       y3) and node 5 (parents y3, y4) — see
       `manufacturing_problem.py:180-196`.

2. **Is it the problem, not the algorithm?** The node_correlations.png /
   .json show that y4→y5 has R²=0.90 (highly linear) and y0→y1 is 0.76,
   but y1→y3 and y3→y4 are only ~0.2. Does this pattern (strong terminal
   linearity + noisy intermediates) systematically favor HighFidOnly over
   per-node decomposition? Is this representative of the real LPBF
   pipeline the manuscript describes, or an artefact of the Matheron
   synthesis? Suggest a more discriminating synthetic problem.

3. **std-dev is large** (±0.13 for pKGFN, ±0.16 for LowFidOnly). Is this
   seed noise, measurement noise (σ=0.05) exploding through the 6-node
   composition, or under-optimization of acquisition? Recommend concrete
   diagnostics and, if needed, variance-reduction steps (paired CRNs,
   more init points, averaging posterior means over more MC samples).

4. **Manuscript alignment.** Does the proposed FLAIME workflow
   (`main (2).pdf`) still hold if pKGFN isn't reliably better than a
   vanilla GP-EI on y5 in this regime? Any concrete claim in Activity 1
   that should be softened, or any alternative algorithm (e.g. EIFN with
   node-MTMT kernel, multi-fidelity KG over the true fidelity hierarchy)
   we should surface?

Please be precise about which lines of code or which panels of
node_correlations.png support each recommendation."""


def main() -> None:
    api_key = os.environ.get("EDISON_API_KEY")
    if not api_key:
        sys.exit("EDISON_API_KEY not set")

    client = EdisonClient(api_key=api_key)

    uris = []
    for rel in FILES_TO_UPLOAD:
        p = REPO / rel
        if not p.exists():
            print(f"  [skip] missing: {p}")
            continue
        uri = client.upload_file(file_path=str(p))
        print(f"  uploaded {rel}  -> {uri}")
        uris.append(uri)
    print(f"Uploaded {len(uris)} files")

    task = client.create_task(
        task_data=TaskRequest(
            name=JobNames.ANALYSIS,
            query=QUERY,
            runtime_config=RuntimeConfig(),
        ),
        files=uris,
    )
    # create_task returns a trajectory_id string.
    task_id = str(task) if task else None
    print(f"Submitted Edison ANALYSIS task: {task_id}")

    # Persist task ID for next-session retrieval.
    pending_path = REPO / "edison-trajectories" / "pending-edison-tasks.json"
    data = json.loads(pending_path.read_text()) if pending_path.exists() else {"tasks": []}
    data.setdefault("tasks", []).append(
        {
            "purpose": "pkgfn-underperformance-analysis",
            "addresses_comment": 4291093320,
            "job_name": "ANALYSIS",
            "task_id": task_id,
            "status": "pending",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "attached_files": FILES_TO_UPLOAD,
        }
    )
    data["last_submitted_at"] = datetime.now(timezone.utc).isoformat()
    pending_path.write_text(json.dumps(data, indent=2))
    print(f"Recorded in {pending_path}")


if __name__ == "__main__":
    main()
