"""Edison ANALYSIS query: spot-check our pKGFN port vs vertical-cloud-lab/partial_kgfn PR #2.

Submits an Edison ANALYSIS task with our `partial_kgfn/*.py` source, the driver
files, the upstream PR's `run_one_trial.py` snippets we manually fetched, and
the spot-check report `upstream-vlcl-pkgfn-pr2-spotcheck.md`.

Does NOT block-poll. Task ID is appended to
``edison-trajectories/pending-edison-tasks.json`` for next-session retrieval.

Per repo memory: gate submission with ``if __name__ == "__main__":`` so importing
this module from a poll/retry helper does not burn duplicate credits.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from edison_client import EdisonClient
from edison_client.models import RuntimeConfig, TaskRequest
from edison_client.models.app import JobNames

REPO = Path(__file__).resolve().parents[1]

FILES_TO_UPLOAD = [
    # Our spot-check report (the entrypoint for the analyst).
    "edison-trajectories/upstream-vlcl-pkgfn-pr2-spotcheck.md",
    # Our pKGFN port — the artefact under review.
    "benchmarks/partial_kgfn/partial_kgfn.py",
    "benchmarks/partial_kgfn/gp_network.py",
    "benchmarks/partial_kgfn/thompson_sampling.py",
    "benchmarks/partial_kgfn/manufacturing_problem.py",
    # The drivers that wire everything together.
    "benchmarks/bofn_pkgfn_demo.py",
    "benchmarks/bofn_actions_benchmark.py",
    # The latest cost-efficiency figure (post-noFb2) so the analyst sees the
    # current empirical regime.
    "benchmarks/figures/actions_hpc/pkgfn-noFb2-20260501T071019Z/best_so_far_traces_pkgfn_budget.png",
]

QUERY = """We have a working port of Buathong et al. (2024) p-KGFN at
``benchmarks/partial_kgfn/`` in ``vertical-cloud-lab/digital-alloy-lab-private``
(branch ``copilot/explore-llms-function-networks-bo``). It runs a 6-node
synthetic LPBF/CALPHAD DAG (``ExtendedManufacturingGPNetwork``) — distinct
from any of the 7 paper test networks.

A second, paper-faithful pKGFN reproduction of the *original* test networks
just landed at ``vertical-cloud-lab/partial_kgfn`` PR #2 (BOFN benchmark
workflow on top of the upstream paper code from ``frazier-lab/partial_kgfn``,
mirrored at ``vertical-cloud-lab/partial_kgfn/main`` @ a5996011). PR #2 only
adds a benchmark workflow + DAG visualizer; it does **not** modify the core
acquisition (``acquisition/partial_kgfn.py``) or model (``models/decoupled_gp_network.py``)
— so PR #2 effectively *is* the paper-faithful reference implementation we
should be mirroring.

We did two manual passes through both code-bases and produced
``upstream-vlcl-pkgfn-pr2-spotcheck.md`` (attached as the entrypoint).

**What we'd like you to do:**

1. **Independently re-derive the inconsistency table** by reading our
   ``benchmarks/partial_kgfn/partial_kgfn.py`` and comparing against the
   upstream file at
   <https://github.com/vertical-cloud-lab/partial_kgfn/blob/main/partial_kgfn/acquisition/partial_kgfn.py>
   (and similarly for ``gp_network.py``, ``thompson_sampling.py``, the
   driver code in
   <https://github.com/vertical-cloud-lab/partial_kgfn/blob/main/partial_kgfn/run_one_trial.py>
   `elif algo == "pKGFN":` block at ~line 701, and the helper
   functions ``generate_X_fantasies_candidates_RaLo`` /
   ``generate_X_fantasies_candidates_TS`` at the bottom of the same file).
   For each of the 5 passes (forward, pkgfn_step driver, GP network, TSFN,
   misc) **score each row of the spot-check table as
   confirmed / partially-confirmed / refuted, citing exact line numbers
   in both code-bases.**

2. **Catch anything we missed.** Specifically scan for:
   - Anywhere our port silently drops an upstream argument (we already found
     `inner_sampler` — are there others?).
   - Anywhere the BoTorch >=0.13 migration changed semantics, not just the
     API surface (e.g. `Standardize` v0 vs v1 behaviour, `fit_gpytorch_mll`
     vs `fit_gpytorch_model` convergence criteria, `MultivariateNormalNetwork`
     `rsample_from_base_samples` shape contract).
   - Discrete-acquisition optimisation: upstream uses
     `optimize_discrete_acqf_for_function_network`; we use `pkgfn(raw_cands)`
     and `argmax`. Is the upstream `parent_bounds` projection step doing
     something we'd be silently wrong without?
   - Cost accounting in
     `benchmarks/bofn_actions_benchmark.py` vs the upstream BO loop in
     `run_one_trial.py:407-426` (KGFN/pKGFN cost-update branch).

3. **Quantify which fixes matter most.** Given the empirical state
   (final ranking at $1,720 cost cap, n=20 seeds: TSFN 17.489 ± 0.261,
   HighFidOnly 17.353, Random 17.246, Sobol 17.228, pKGFN 17.191 ± 0.604,
   true_max=18.02, init=15.21), and assuming the synthetic DAG itself is
   adequate, **rank the fixes by expected lift on pKGFN's mean** at fixed
   wall-clock budget. The current candidates we identified, in priority
   order, are:
     a. Wire `inner_sampler` through `forward()` (currently dropped).
     b. Anchor `X_fantasies_candidates` on the incumbent (`generate_X_fantasies_candidates_RaLo`
        + optionally `_TS`), instead of 200 global Sobol points.
     c. Drop `num_fantasies` from 32/64 → 8 (paper default) once (b) lands.
     d. Add a continuous L-BFGS refinement pass after the discrete argmax
        (mini version of `optimize_discrete_acqf_for_function_network`).
     e. Implement `impose_assump` (only fantasize child if parents observed).

   Suggest a different priority order or new fixes if warranted.

4. **Try to actually run a 2-3 iter smoke** of our `bofn_pkgfn_demo.py`
   (`python benchmarks/bofn_pkgfn_demo.py`) if you can install
   ``botorch>=0.17 torch>=2.10 gpytorch matplotlib numpy``. If install
   fails, that's fine — just analyse statically.

Be precise with line numbers in BOTH code-bases (ours and upstream). The
goal is to give the team a concrete, prioritised, line-number-cited list of
the smallest set of changes most likely to bring our pKGFN curve above TSFN
on the next ORC re-sweep.
"""


def main() -> None:
    api_key = os.environ.get("EDISON_API_KEY")
    if not api_key:
        sys.exit("EDISON_API_KEY not set")

    client = EdisonClient(api_key=api_key)

    uris: list[str] = []
    for rel in FILES_TO_UPLOAD:
        p = REPO / rel
        if not p.exists():
            print(f"  [skip] missing: {p}")
            continue
        uri = client.upload_file(file_path=str(p))
        print(f"  uploaded {rel}  -> {uri}")
        uris.append(uri)
    print(f"Uploaded {len(uris)} files")

    task_id = client.create_task(
        task_data=TaskRequest(
            name=JobNames.ANALYSIS,
            query=QUERY,
            runtime_config=RuntimeConfig(),
        ),
        files=uris,
    )
    task_id = str(task_id) if task_id else None
    print(f"Submitted Edison ANALYSIS task: {task_id}")

    pending_path = REPO / "edison-trajectories" / "pending-edison-tasks.json"
    data = (
        json.loads(pending_path.read_text())
        if pending_path.exists()
        else {"tasks": []}
    )
    data.setdefault("tasks", []).append(
        {
            "purpose": "spot-check vs vertical-cloud-lab/partial_kgfn PR #2 (paper-faithful)",
            "addresses_comment": 4403214937,
            "job_name": "ANALYSIS",
            "task_id": task_id,
            "status": "pending",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "attached_files": FILES_TO_UPLOAD,
            "spotcheck_doc": "edison-trajectories/upstream-vlcl-pkgfn-pr2-spotcheck.md",
        }
    )
    data["last_submitted_at"] = datetime.now(timezone.utc).isoformat()
    pending_path.write_text(json.dumps(data, indent=2))
    print(f"Recorded in {pending_path}")


if __name__ == "__main__":
    main()
