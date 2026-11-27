#!/usr/bin/env python3
"""Edison Scientific orchestration for FLAIME 15-element palette composition bounds.

Resolves vertical-cloud-lab/digital-alloy-lab-private element-palette bounds task.

Pipeline:
  Phase 1 (parallel LITERATURE queries):
    * 16 per-element upper-bound queries — Al + 15 alloying elements
      (Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn)
      Each asks for conservative + non-conservative upper bound + justification.
    * 1 lower-bound query (Al lower bound; others = 0 with simplex constraint).
    * 1 simultaneous all-bounds query (LITERATURE_HIGH).
  Phase 2 (ANALYSIS): finalized bounds table, with all phase-1 trajectory
    markdown files uploaded as context.
  Phase 3 (ANALYSIS): special multi-element constraints and edge cases,
    with phase-1 + phase-2 results uploaded.

All results are written to edison-trajectories/element-bounds/*.md so they
are durable, reviewable, and citable in the proposal.

Requires:
    pip install edison-client>=0.11.0
    EDISON_API_KEY environment variable set
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from edison_client import EdisonClient, JobNames, TaskRequest


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
EDISON_DIR = REPO_ROOT / "edison-trajectories"
OUTPUT_DIR = EDISON_DIR / "element-bounds"
PROPOSAL_DIR = REPO_ROOT / "genesis-mission-proposal"

# 15-element palette (non-Al) per .github/agents/proposal-consistency-checker.agent.md
NON_AL_ELEMENTS = [
    "Mn", "Cr", "Zr", "Mg", "Si", "Cu", "Ti", "Fe",
    "Ni", "Ce", "Sc", "Li", "Er", "Zn", "Sn",
]
ALL_ELEMENTS = ["Al"] + NON_AL_ELEMENTS

# Context shared with every prompt to anchor Edison in the FLAIME problem.
PROJECT_CONTEXT = """\
PROJECT CONTEXT — FLAIME (Fast Learning AI for Mineral Efficiency), DOE Genesis
Mission Phase I, Topic 3-B (AMMTO). The team is performing Bayesian Optimization
over Function Networks (BOFN/pKGFN) over a single joint search space:
(Al + 15 non-Al alloying elements) x atomization process x LPBF process.

The 15 non-Al element palette is:
  Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn.

Composition is parameterized as weight fractions that sum to 1.0; Al is the
matrix element. Down-selection is driven by CALPHAD (TCAl10 + AM Module),
Scheil solidification range, hot-cracking susceptibility, printability, and a
mineral-burden objective (USGS criticality / import reliance).

Anchor systems include Al-Mn-Cr-Zr and Al-Zr; the broader palette is intended
to enable AI-discovered sub-systems (ternary through ~9-component). All alloys
are Al-rich (Al typically >= 85 wt% for good LPBF processability and to remain
within the trustworthy region of TCAl10's binary/ternary Muggianu extrapolation).

We need element-by-element compositional BOUNDS (in weight percent, wt%) for
the BOFN / GA acquisition inner-solver search space.
"""


@dataclass
class QueryJob:
    key: str               # short identifier used in filenames + dict keys
    title: str             # human-readable title
    job_name: str          # JobNames value (LITERATURE or LITERATURE_HIGH)
    prompt: str            # full prompt text


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def build_per_element_prompt(element: str) -> str:
    if element == "Al":
        focus = (
            "Al is the matrix/solvent. Provide a CONSERVATIVE and "
            "NON-CONSERVATIVE LOWER bound on the Al weight fraction (since the "
            "alloy must remain Al-rich) AND any practical UPPER bound (e.g. "
            "essentially 1.0, or a slightly tighter value if a minimum amount "
            "of solute is required for printability/strengthening)."
        )
    else:
        focus = (
            f"{element} is one of 15 non-Al alloying elements. Provide a "
            "CONSERVATIVE upper bound (defensible from established LPBF Al "
            "alloy literature, e.g. published commercial / qualified AM "
            f"compositions) and a NON-CONSERVATIVE upper bound (defensible "
            f"but more aggressive — e.g. extending to the limit of TCAl10 "
            f"Al-rich validity, eutectic constraints, or known experimental "
            f"high-{element} LPBF studies)."
        )

    return PROJECT_CONTEXT + f"""

TASK — Element-specific bound: {element}
{focus}

Please return:
1. CONSERVATIVE bound (wt% of {element}) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of {element}) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for {element if element != 'Al' else 'common solutes'}).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
"""


def build_lower_bound_prompt() -> str:
    return PROJECT_CONTEXT + """

TASK — LOWER BOUND ANALYSIS
Aluminum is the matrix; the only element with a meaningful (nonzero) LOWER
bound is Al itself. All 15 non-Al elements technically have a lower bound of
0 wt% (they may be absent), with the simplex constraint
    Al_wt + sum_i(X_i_wt) = 1.0   for i in {Mn,Cr,Zr,Mg,Si,Cu,Ti,Fe,Ni,Ce,Sc,Li,Er,Zn,Sn}.

Please answer the following:

1. What is a defensible LOWER bound on the Al weight fraction (Al_min) for
   this BOFN search space, given that we want to remain (i) within the
   trustworthy region of TCAl10 and the AM Module, (ii) a meaningfully
   "Al alloy" by ASTM/wrought/AM convention, and (iii) reasonable for LPBF
   processability? Provide both a CONSERVATIVE Al_min (e.g. ~95 wt%) and a
   NON-CONSERVATIVE Al_min (e.g. as low as ~80–85 wt%) with justification.

2. Are there any non-Al elements that, when present, should themselves carry
   a nonzero LOWER bound — e.g. minimum Mg or Si if either is selected by
   the AI to ensure precipitation strengthening kicks in? Distinguish
   "global lower bound" (always > 0) from "conditional lower bound"
   (>0 only when the element is included).

3. How should the lower-bound Al_min interact with sparsity? FLAIME prefers
   k=3..8 active alloying elements per composition; what implications does
   this have for the per-element minimum nonzero concentration (e.g. a
   "detection / dosing floor" of ~0.05–0.1 wt% for ICP-MS / atomization
   crucible accuracy)?

Cite specific LPBF Al-alloy literature where possible. Express all numbers
in wt%.
"""


def build_simultaneous_prompt() -> str:
    elem_list = ", ".join(ALL_ELEMENTS)
    return PROJECT_CONTEXT + f"""

TASK — JOINT BOUNDS TABLE
Provide a single consolidated table of compositional bounds (in wt%) for
the entire FLAIME 15-element palette plus Al, in one go:
    {elem_list}

For EACH of the 16 elements include:
  * conservative lower bound (wt%) — Al only; 0 for the rest unless you
    argue otherwise
  * non-conservative lower bound (wt%)
  * conservative upper bound (wt%)
  * non-conservative upper bound (wt%)
  * primary failure mode setting the upper bound
  * key citation(s)

Use a markdown table. Then below the table, in a paragraph:

  (a) Reconcile the per-element upper bounds with the simplex constraint
      sum(wt%) = 100 — i.e. flag any bounds that, if all were saturated
      simultaneously, would produce an impossible (>100 wt%) composition.
  (b) Recommend any element-pair or element-group bounds (e.g.
      Cu + Li, Mg + Si, Sc + Zr, Fe + Si impurity sum) that are tighter
      than the marginal per-element bounds because of joint-failure modes
      (hot cracking, brittle intermetallics, eutectic depression,
      printability limits).
  (c) Suggest a default Al_min for the BOFN search space.

Be quantitative, cite peer-reviewed AM Al alloy literature, and use the
TCAl10 assessed-binary/ternary coverage as a guardrail for the
"non-conservative" bounds.
"""


def build_finalized_table_prompt() -> str:
    elem_list = ", ".join(ALL_ELEMENTS)
    return PROJECT_CONTEXT + f"""

TASK — FINALIZED BOUNDS TABLE (synthesis)

Attached are the markdown trajectories from a batch of LITERATURE-mode
Edison queries that asked, separately and jointly, for upper / lower
compositional bounds on each of the 16 elements:
    {elem_list}

Synthesize ALL of the attached trajectories (per-element upper-bound
queries, the lower-bound query, and the joint simultaneous-bounds query)
into ONE finalized markdown bounds table that the FLAIME team can drop
directly into the BOFN search-space definition. The table must contain,
for each element, exactly these columns:

| Element | Lower bound (wt%) | Recommended upper bound (wt%) | Conservative upper (wt%) | Non-conservative upper (wt%) | Primary failure mode setting upper bound | Notes / caveats | Key citations |

Conventions:
  * Recommended upper bound = the bound the FLAIME team should USE in the
    BOFN search space (justify the choice between conservative and
    non-conservative based on TCAl10 coverage, dosing accuracy of the
    AMAZEMET rePOWDER induction crucible, and the project's k=3..8 sparsity
    pattern).
  * Lower bound is 0 wt% for non-Al elements unless the synthesis
    determines a defensible nonzero floor (e.g. dosing detection limit ~0.05
    wt% if present at all).
  * Al lower bound: pick a single Al_min and justify it.

Below the table:
  1. State the chosen Al_min in wt% and explain.
  2. Note any per-element cases where the conservative and non-conservative
    estimates from the LITERATURE queries disagreed substantially, and how
    you resolved it.
  3. Flag any elements where Edison's LITERATURE responses had thin or
    contradictory evidence — these are candidates for follow-up CALPHAD or
    experimental verification in Activity 1 / Activity 2.

Output: a single, copy-pasteable markdown section.
"""


def build_constraints_prompt() -> str:
    return PROJECT_CONTEXT + """

TASK — SPECIAL MULTI-ELEMENT CONSTRAINTS AND EDGE CASES

Attached are: (a) the 16 per-element bound trajectories, (b) the Al
lower-bound trajectory, (c) the joint simultaneous-bounds trajectory, and
(d) the finalized bounds table you previously synthesized.

The marginal (per-element) bounds are not enough for a safe BOFN search
space. We also need MULTI-ELEMENT constraints — sums or ratios of specific
element subsets that must stay within a bound — and edge cases that the
GA / pKGFN inner solver should respect.

Please produce a markdown section titled "Multi-Element Constraints &
Edge Cases" with at least the following content, drawing only on the
attached trajectories and on standard Al-alloy / LPBF literature:

1. SIMPLEX & SPARSITY
   * Required: sum of all weight fractions = 1 (Al + 15 = 1).
   * Sparsity prior: k = 3..8 nonzero non-Al elements per composition;
     state how this should be enforced (hard or soft constraint).
   * Dosing floor for any included element (wt%).

2. SUM CONSTRAINTS — list each as
       sum(subset) <= X wt%   (or >=, or a band)
   covering at minimum:
     * Total non-Al solute (1 - Al)
     * Cu + Li (Al-Cu-Li hot-cracking + density / ductility)
     * Mg + Si (Mg2Si precipitation balance, beta-prime)
     * Mg + Zn (+ Cu) for 7xxx-style hot tearing
     * Sc + Zr (L1_2 dispersoid forming pair; near-stoichiometric ratio)
     * Fe + Si (residual / impurity sum that controls beta-AlFeSi)
     * Ce + Mn (eutectic / dispersoid co-additions reported in AM Al-Ce
       and Al-Mn-Sc-Zr literature)
     * Any other group your synthesis identifies

3. RATIO / STOICHIOMETRY CONSTRAINTS
   * Sc:Zr atomic-ratio guidance for Al3(Sc,Zr) L1_2.
   * Mg:Si atomic-ratio for Mg2Si.
   * Cu:Mg ratio for S-phase / theta'.

4. TCAl10 COVERAGE GUARDRAILS
   * Element pairs with NO assessed Al-X-Y ternary should have tighter
     marginal bounds when both are simultaneously > some threshold.
   * State explicitly which pairs from the 15-element palette are
     "Muggianu-extrapolation only" and recommend a joint-cap.

5. ATOMIZATION / OXIDATION EDGE CASES
   * Elements that are problematic for ultrasonic atomization in an Al
     induction crucible (Li, Mg high-vapor pressure; Ce/Sc/Er high cost
     and oxide-skin issues; Ti losses to Al3Ti primaries; Zr losses to
     Al3Zr primaries above the peritectic).

6. PRINTABILITY EDGE CASES
   * Compositions with predicted freezing range > some threshold should
     be discarded or flagged.
   * Compositions where the conservative upper bound on a heavy critical
     element (Sc, Er, Ce) is exceeded should incur a mineral-burden
     penalty as well as a printability one.

7. RECOMMENDATIONS
   * 3-5 specific actionable changes to the BOFN search-space definition.
   * Any constraints that should be implemented as PENALTIES in the
     pKGFN acquisition rather than as hard bounds.

Be concise, quantitative, and cite where possible.
"""


# ---------------------------------------------------------------------------
# Edison helpers
# ---------------------------------------------------------------------------

def make_client() -> EdisonClient:
    api_key = os.environ.get("EDISON_API_KEY")
    if not api_key:
        sys.stderr.write("ERROR: EDISON_API_KEY not set\n")
        sys.exit(1)
    return EdisonClient(api_key=api_key)


def submit(client: EdisonClient, job: QueryJob, file_ids: list[str] | None = None,
           max_attempts: int = 8, base_delay: float = 5.0) -> str:
    """Submit a task with backoff on 429/transient errors; return task_id."""
    job_name = getattr(JobNames, job.job_name)
    req = TaskRequest(name=job_name, query=job.prompt)
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            if file_ids:
                return client.create_task(task_data=req, files=file_ids)
            return client.create_task(task_data=req)
        except Exception as e:  # includes tenacity.RetryError wrapping 429s
            last_exc = e
            wait = base_delay * (2 ** (attempt - 1))
            print(f"  submit retry {attempt}/{max_attempts} for {job.key} after error: {e!r}; sleeping {wait:.0f}s",
                  flush=True)
            time.sleep(wait)
    raise RuntimeError(f"submit failed for {job.key} after {max_attempts} attempts: {last_exc!r}")


def poll_until_done(
    client: EdisonClient,
    task_id: str,
    label: str,
    poll_interval: int = 30,
    timeout: int = 1800,
) -> str | None:
    """Poll until success/failure; return answer text or None on failure."""
    elapsed = 0
    while elapsed < timeout:
        time.sleep(poll_interval)
        elapsed += poll_interval
        try:
            task = client.get_task(task_id=task_id)
            status = task.status
        except Exception as e:
            print(f"  [{label}] poll error at {elapsed}s: {e}", flush=True)
            continue
        print(f"  [{label}] {elapsed}s status={status}", flush=True)
        if status == "success":
            return getattr(task, "formatted_answer", None) or task.answer or ""
        if status in ("failed", "error", "cancelled"):
            print(f"  [{label}] task ended with status={status}", flush=True)
            return None
    print(f"  [{label}] TIMED OUT after {timeout}s (task_id={task_id})", flush=True)
    return None


def write_result(key: str, title: str, task_id: str, prompt: str, answer: str | None) -> pathlib.Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{key}.md"
    parts = [f"# {title}", "", f"*Edison task: `{task_id}`*", ""]
    if answer is None:
        parts += ["**Status:** task did not complete in this run.", ""]
    parts += ["## Answer", "", answer or "_(no answer)_", ""]
    parts += ["---", "", "## Prompt", "", "```", prompt.rstrip(), "```", ""]
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def upload_files(client: EdisonClient, paths: list[pathlib.Path]) -> list[str]:
    ids: list[str] = []
    for p in paths:
        if not p.exists() or p.stat().st_size == 0:
            print(f"  upload skip (missing/empty): {p}", flush=True)
            continue
        try:
            fid = client.upload_file(str(p))
            ids.append(fid)
            print(f"  uploaded: {p.name}", flush=True)
        except Exception as e:
            print(f"  upload failed {p.name}: {e}", flush=True)
    return ids


# ---------------------------------------------------------------------------
# Phase orchestration
# ---------------------------------------------------------------------------

def build_phase1_jobs() -> list[QueryJob]:
    jobs: list[QueryJob] = []
    for el in ALL_ELEMENTS:
        jobs.append(QueryJob(
            key=f"01_per_element_{el}",
            title=f"Phase 1 — Per-element bound: {el}",
            job_name="LITERATURE",
            prompt=build_per_element_prompt(el),
        ))
    jobs.append(QueryJob(
        key="01_lower_bound",
        title="Phase 1 — Lower-bound query (Al-rich constraint)",
        job_name="LITERATURE",
        prompt=build_lower_bound_prompt(),
    ))
    jobs.append(QueryJob(
        key="01_simultaneous_all_bounds",
        title="Phase 1 — Simultaneous all-element bounds (LITERATURE_HIGH)",
        job_name="LITERATURE_HIGH",
        prompt=build_simultaneous_prompt(),
    ))
    return jobs


def run_phase1(client: EdisonClient, jobs: list[QueryJob], max_workers: int) -> dict[str, dict]:
    """Submit all phase-1 jobs, then concurrently poll. Save results.

    Returns a dict keyed by job.key with {task_id, answer, path}.
    """
    print(f"\n=== Phase 1: submitting {len(jobs)} LITERATURE queries ===", flush=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    state_path = OUTPUT_DIR / "_submitted.json"
    state: dict[str, str] = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text())
            print(f"  loaded {len(state)} prior task IDs from {state_path}", flush=True)
        except Exception as e:
            print(f"  WARN: could not read {state_path}: {e}", flush=True)

    submitted: list[tuple[QueryJob, str]] = []
    for job in jobs:
        if job.key in state and state[job.key]:
            task_id = state[job.key]
            print(f"  resumed {job.key}: task_id={task_id} (from state file)", flush=True)
        else:
            task_id = submit(client, job)
            state[job.key] = task_id
            state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
            print(f"  submitted {job.key}: task_id={task_id} ({job.job_name})", flush=True)
            time.sleep(3.0)  # gentle pacing to avoid 429 burst limits
        submitted.append((job, task_id))

    results: dict[str, dict] = {}

    def _poll(job: QueryJob, task_id: str):
        # LITERATURE_HIGH may take ~15min per the cookbook custom instruction.
        timeout = 2700 if job.job_name == "LITERATURE_HIGH" else 1500
        first_wait = 600 if job.job_name == "LITERATURE_HIGH" else 300
        time.sleep(first_wait)  # avoid hammering early
        ans = poll_until_done(
            client, task_id, label=job.key, poll_interval=60, timeout=timeout - first_wait
        )
        path = write_result(job.key, job.title, task_id, job.prompt, ans)
        return job.key, {"task_id": task_id, "answer": ans, "path": str(path.relative_to(REPO_ROOT))}

    print(f"\n=== Phase 1: polling {len(submitted)} tasks (max_workers={max_workers}) ===", flush=True)
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_poll, job, tid): job.key for job, tid in submitted}
        for fut in as_completed(futures):
            try:
                key, info = fut.result()
            except Exception as e:
                key = futures[fut]
                print(f"  [{key}] poll thread crashed: {e}", flush=True)
                results[key] = {"task_id": None, "answer": None, "path": None}
                continue
            results[key] = info
            print(f"  saved {info['path']}", flush=True)

    # Persist machine-readable index
    index_path = OUTPUT_DIR / "_phase1_index.json"
    index_path.write_text(
        json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "answer"} for k, v in results.items()}, indent=2),
        encoding="utf-8",
    )
    print(f"  wrote index: {index_path}", flush=True)
    return results


def _load_state() -> dict:
    sp = OUTPUT_DIR / "_submitted.json"
    if sp.exists():
        try:
            return json.loads(sp.read_text())
        except Exception:
            return {}
    return {}


def _save_state(state: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "_submitted.json").write_text(json.dumps(state, indent=2), encoding="utf-8")


def run_phase2(client: EdisonClient, phase1_paths: list[pathlib.Path]) -> tuple[str, pathlib.Path]:
    print("\n=== Phase 2: ANALYSIS (finalized bounds table) ===", flush=True)
    job = QueryJob(
        key="02_finalized_bounds_table",
        title="Phase 2 — Finalized bounds table (Edison ANALYSIS)",
        job_name="ANALYSIS",
        prompt=build_finalized_table_prompt(),
    )
    state = _load_state()
    task_id = state.get(job.key)
    if task_id:
        print(f"  resumed {job.key}: task_id={task_id} (from state file)", flush=True)
    else:
        file_ids = upload_files(client, phase1_paths)
        task_id = submit(client, job, file_ids=file_ids)
        state[job.key] = task_id
        _save_state(state)
        print(f"  submitted {job.key}: task_id={task_id}", flush=True)
        time.sleep(60)
    ans = poll_until_done(client, task_id, label=job.key, poll_interval=45, timeout=3600)
    path = write_result(job.key, job.title, task_id, job.prompt, ans)
    print(f"  saved {path}", flush=True)
    return task_id, path


def run_phase3(client: EdisonClient, prior_paths: list[pathlib.Path]) -> pathlib.Path:
    print("\n=== Phase 3: ANALYSIS (multi-element constraints) ===", flush=True)
    job = QueryJob(
        key="03_multi_element_constraints",
        title="Phase 3 — Multi-element constraints & edge cases (Edison ANALYSIS)",
        job_name="ANALYSIS",
        prompt=build_constraints_prompt(),
    )
    state = _load_state()
    task_id = state.get(job.key)
    if task_id:
        print(f"  resumed {job.key}: task_id={task_id} (from state file)", flush=True)
    else:
        file_ids = upload_files(client, prior_paths)
        task_id = submit(client, job, file_ids=file_ids)
        state[job.key] = task_id
        _save_state(state)
        print(f"  submitted {job.key}: task_id={task_id}", flush=True)
        time.sleep(60)
    ans = poll_until_done(client, task_id, label=job.key, poll_interval=45, timeout=3600)
    path = write_result(job.key, job.title, task_id, job.prompt, ans)
    print(f"  saved {path}", flush=True)
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phases", default="1,2,3",
        help="Comma-separated phases to run (default: 1,2,3).",
    )
    parser.add_argument(
        "--max-workers", type=int, default=18,
        help="Max concurrent phase-1 polling threads (default: 18).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the prompts that would be sent and exit without contacting Edison.",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    phases = {int(p) for p in args.phases.split(",") if p.strip()}

    if args.dry_run:
        for job in build_phase1_jobs():
            print(f"--- {job.key} ({job.job_name}) ---")
            print(job.prompt)
        print(f"--- 02_finalized_bounds_table (ANALYSIS) ---")
        print(build_finalized_table_prompt())
        print(f"--- 03_multi_element_constraints (ANALYSIS) ---")
        print(build_constraints_prompt())
        return 0

    client = make_client()

    phase1_paths: list[pathlib.Path] = []
    if 1 in phases:
        results = run_phase1(client, build_phase1_jobs(), args.max_workers)
        phase1_paths = [REPO_ROOT / r["path"] for r in results.values() if r.get("path")]
    else:
        phase1_paths = sorted(OUTPUT_DIR.glob("01_*.md"))
        print(f"Phase 1 skipped; using {len(phase1_paths)} existing files.", flush=True)

    phase2_path: pathlib.Path | None = None
    if 2 in phases:
        _, phase2_path = run_phase2(client, phase1_paths)
    else:
        candidate = OUTPUT_DIR / "02_finalized_bounds_table.md"
        phase2_path = candidate if candidate.exists() else None

    if 3 in phases:
        prior = list(phase1_paths)
        if phase2_path:
            prior.append(phase2_path)
        run_phase3(client, prior)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
