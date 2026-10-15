"""Shared utilities for Edison Scientific section-drafting scripts.

Usage:
    from edison_utils import create_edison_client, upload_files, submit_and_poll, save_result

Requires:
    pip install edison-client>=0.11.0
    EDISON_API_KEY environment variable set
"""

import os
import sys
import time
import glob as glob_mod
import pathlib

from edison_client import EdisonClient, TaskRequest, JobNames


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PROPOSAL_DIR = REPO_ROOT / "genesis-mission-proposal"
EDISON_DIR = REPO_ROOT / "edison-trajectories"
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
BIOS_DIR = REPO_ROOT / "bios"
OUTPUT_DIR = pathlib.Path(__file__).resolve().parent / "results"


def create_edison_client() -> EdisonClient:
    """Create an authenticated Edison client."""
    api_key = os.environ.get("EDISON_API_KEY")
    if not api_key:
        print("ERROR: EDISON_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return EdisonClient(api_key=api_key)


def upload_files(client: EdisonClient, file_paths: list[str | pathlib.Path]) -> list[str]:
    """Upload files to Edison, returning list of data_entry IDs.

    Skips files that don't exist and prints warnings.
    """
    uploaded = []
    for fp in file_paths:
        fp = pathlib.Path(fp)
        if not fp.exists():
            print(f"  WARNING: skipping missing file: {fp}", file=sys.stderr)
            continue
        if fp.stat().st_size == 0:
            print(f"  WARNING: skipping empty file: {fp}", file=sys.stderr)
            continue
        # Skip binary files that Edison can't parse (images, PDFs over 50MB, etc.)
        suffix = fp.suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg"}:
            print(f"  INFO: skipping image file: {fp.name}", file=sys.stderr)
            continue
        try:
            fid = client.upload_file(str(fp))
            uploaded.append(fid)
            print(f"  Uploaded: {fp.name}")
        except Exception as e:
            print(f"  WARNING: failed to upload {fp.name}: {e}", file=sys.stderr)
    return uploaded


def submit_and_poll(
    client: EdisonClient,
    query: str,
    file_ids: list[str],
    poll_interval: int = 30,
    timeout: int = 900,
) -> str:
    """Submit an ANALYSIS task and poll until complete. Returns the answer text."""
    req = TaskRequest(name=JobNames.ANALYSIS, query=query)
    task_id = client.create_task(task_data=req, files=file_ids)
    print(f"  Task submitted: {task_id}")
    print(f"  Polling every {poll_interval}s (timeout {timeout}s)...")

    elapsed = 0
    while elapsed < timeout:
        time.sleep(poll_interval)
        elapsed += poll_interval
        task = client.get_task(task_id=task_id)
        status = task.status
        print(f"  [{elapsed}s] status={status}")
        if status == "success":
            return task.answer
        if status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"Edison task {task_id} failed with status={status}")
    raise TimeoutError(f"Edison task {task_id} timed out after {timeout}s")


def save_result(filename: str, content: str) -> pathlib.Path:
    """Save Edison result to the results/ directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / filename
    out_path.write_text(content, encoding="utf-8")
    print(f"  Result saved: {out_path}")
    return out_path


def get_core_context_files() -> list[pathlib.Path]:
    """Return the set of core context files that every section script should attach.

    These provide the overall proposal structure, plan, checklist, and template
    so Edison has full context regardless of which section is being drafted.
    """
    core = [
        PROPOSAL_DIR / "proposal-population-plan.md",
        PROPOSAL_DIR / "proposal-checklist.md",
        PROPOSAL_DIR / "flaime-genesis-proposal.tex",
        EDISON_DIR / "edison-3b-deepdive-synthesis.md",
        EDISON_DIR / "project-metrics-v4-edison-refined.md",
        EDISON_DIR / "preliminary-results-roadmap.md",
    ]
    return [f for f in core if f.exists()]


def get_section_specific_files(section_key: str) -> list[pathlib.Path]:
    """Return section-specific source files based on the section key.

    Section keys match the proposal plan's section identifiers.
    """
    files_map: dict[str, list[pathlib.Path]] = {
        "abstract": [
            EDISON_DIR / "ai-advantage-statement.md",
            EDISON_DIR / "edison-3b-deepdive-synthesis.md",
            EDISON_DIR / "project-metrics-v4-edison-refined.md",
        ],
        "title_page": [
            EDISON_DIR / "budget-breakdown-phase1.md",
            EDISON_DIR / "team-skill-chart.md",
            EDISON_DIR / "budget-assessment-official-requirements.md",
        ],
        "background": [
            EDISON_DIR / "edison-3b-deepdive-synthesis.md",
            EDISON_DIR / "materials_criticality_databases.md",
            EDISON_DIR / "literature_alloy_discovery.md",
            EDISON_DIR / "literature_lpbf_alloys.md",
            EDISON_DIR / "calphad_alloy_design.md",
            EDISON_DIR / "pareto-am-al-alloys" / "downstream_applications.md",
            EDISON_DIR / "pareto-am-al-alloys" / "pareto_front_analysis.md",
        ],
        "objectives": [
            EDISON_DIR / "ai-advantage-statement.md",
            EDISON_DIR / "project-metrics-v4-edison-refined.md",
            EDISON_DIR / "edison-kpi1-discovery_yield-review.md",
            EDISON_DIR / "edison-kpi3-acceleration-review.md",
            EDISON_DIR / "edison-kpi4-throughput-review.md",
            EDISON_DIR / "edison-kpi5-mineral_burden-review.md",
        ],
        "methods": [
            EDISON_DIR / "calphad_alloy_design.md",
            EDISON_DIR / "high-throughput-calphad.md",
            EDISON_DIR / "bofn-edison-review1.md",
            EDISON_DIR / "bofn-edison-review2.md",
            EDISON_DIR / "am-scaleup-test-structures.md",
            EDISON_DIR / "alloy_databases_3b_review.md",
            EDISON_DIR / "thermocalc_3b_calphad_strategy_full.md",
        ],
        "milestones": [
            EDISON_DIR / "project-metrics-v4-edison-refined.md",
            EDISON_DIR / "preliminary-results-roadmap.md",
            EDISON_DIR / "edison-kpi1-discovery_yield-review.md",
            EDISON_DIR / "edison-kpi2-cmdri-review.md",
            EDISON_DIR / "edison-kpi3-acceleration-review.md",
            EDISON_DIR / "edison-kpi4-throughput-review.md",
        ],
        "data_sources": [
            EDISON_DIR / "alloy_databases_overview.md",
            EDISON_DIR / "thermocalc_discussion_analysis.md",
            EDISON_DIR / "high-throughput-calphad.md",
            EDISON_DIR / "calphad_licensing.md",
        ],
        "decision_gates": [
            EDISON_DIR / "project-metrics-v4-edison-refined.md",
            EDISON_DIR / "ai-advantage-statement.md",
            EDISON_DIR / "edison-kpi1-discovery_yield-review.md",
            EDISON_DIR / "edison-kpi3-acceleration-review.md",
            EDISON_DIR / "edison-kpi5-mineral_burden-review.md",
        ],
        "bibliography": [
            EDISON_DIR / "bofn-edison-review1.md",
            EDISON_DIR / "literature_alloy_discovery.md",
            EDISON_DIR / "literature_lpbf_alloys.md",
            EDISON_DIR / "literature_lpbf_powders.md",
        ],
        "facilities": [
            EDISON_DIR / "am-scaleup-test-structures.md",
            EDISON_DIR / "calphad_hpc.md",
            EDISON_DIR / "companies_powder_atomization.md",
        ],
        "synergistic": [
            BIOS_DIR / "baird-CV.pdf",
            EDISON_DIR / "self_driving_labs.md",
            EDISON_DIR / "publication_strategy.md",
        ],
        "budget": [
            EDISON_DIR / "budget-breakdown-phase1.md",
            EDISON_DIR / "budget-assessment-official-requirements.md",
            EDISON_DIR / "team-skill-chart.md",
        ],
    }
    return [f for f in files_map.get(section_key, []) if f.exists()]
