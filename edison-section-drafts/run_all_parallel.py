#!/usr/bin/env python3
"""Run all Edison section-drafting scripts in parallel.

Usage:
    python run_all_parallel.py              # Run all 13 scripts
    python run_all_parallel.py --dry-run    # List scripts without running
    python run_all_parallel.py --max-workers 4  # Limit concurrency

Each script submits an Edison ANALYSIS task and polls for results.
Tasks run concurrently (Edison handles parallelism server-side).
Results are saved to edison-section-drafts/results/*.md

Requires:
    pip install edison-client>=0.11.0
    EDISON_API_KEY environment variable set
"""

import argparse
import importlib
import pathlib
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent

# All section draft scripts in execution order (order doesn't matter for parallel)
DRAFT_SCRIPTS = [
    "draft_section0_abstract",
    "draft_title_page",
    "draft_section1_background",
    "draft_section2_objectives",
    "draft_section3_methods",
    "draft_section4_milestones",
    "draft_section5_data_sources",
    "draft_section6_decision_gates",
    "draft_appendix1_bibliography",
    "draft_appendix2_facilities",
    "draft_appendix4_dmsp",
    "draft_appendix5_synergistic",
    "draft_budget_justification",
]


def run_script(script_name: str) -> tuple[str, float, str | None]:
    """Run a single draft script. Returns (script_name, elapsed_seconds, error_or_None)."""
    start = time.time()
    try:
        print(f"\n{'='*60}")
        print(f"STARTING: {script_name}")
        print(f"{'='*60}")
        # Add scripts dir to path and import
        if str(SCRIPTS_DIR) not in sys.path:
            sys.path.insert(0, str(SCRIPTS_DIR))
        mod = importlib.import_module(script_name)
        mod.main()
        elapsed = time.time() - start
        print(f"\n✓ COMPLETED: {script_name} ({elapsed:.0f}s)")
        return (script_name, elapsed, None)
    except Exception as e:
        elapsed = time.time() - start
        error_msg = f"{type(e).__name__}: {e}"
        print(f"\n✗ FAILED: {script_name} ({elapsed:.0f}s) — {error_msg}")
        return (script_name, elapsed, error_msg)


def main():
    parser = argparse.ArgumentParser(description="Run Edison section drafts in parallel")
    parser.add_argument("--dry-run", action="store_true", help="List scripts without running")
    parser.add_argument("--max-workers", type=int, default=6,
                        help="Max concurrent Edison tasks (default: 6)")
    parser.add_argument("--scripts", nargs="*", help="Specific scripts to run (default: all)")
    args = parser.parse_args()

    scripts = args.scripts if args.scripts else DRAFT_SCRIPTS

    if args.dry_run:
        print(f"Would run {len(scripts)} scripts with max_workers={args.max_workers}:")
        for s in scripts:
            print(f"  - {s}.py")
        return

    print(f"Running {len(scripts)} Edison section drafts with max_workers={args.max_workers}")
    print(f"Results will be saved to: {SCRIPTS_DIR / 'results'}/")
    print()

    overall_start = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {executor.submit(run_script, s): s for s in scripts}
        for future in as_completed(futures):
            results.append(future.result())

    overall_elapsed = time.time() - overall_start

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY — {len(results)} scripts in {overall_elapsed:.0f}s")
    print(f"{'='*60}")

    succeeded = [r for r in results if r[2] is None]
    failed = [r for r in results if r[2] is not None]

    for name, elapsed, _ in sorted(succeeded, key=lambda x: x[0]):
        print(f"  ✓ {name:40s} {elapsed:6.0f}s")

    if failed:
        print(f"\n  FAILURES ({len(failed)}):")
        for name, elapsed, err in sorted(failed, key=lambda x: x[0]):
            print(f"  ✗ {name:40s} {elapsed:6.0f}s — {err}")

    print(f"\n  Total: {len(succeeded)}/{len(results)} succeeded")
    print(f"  Wall time: {overall_elapsed:.0f}s")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
