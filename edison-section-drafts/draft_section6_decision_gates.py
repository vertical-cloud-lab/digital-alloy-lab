#!/usr/bin/env python3
"""Edison ANALYSIS: Draft §6 — Decision Gate Metrics (~180 words).

Drafts the decision gate metrics section with 3 quantitative go/no-go criteria.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "decision_gates"
OUTPUT_FILE = "section6_decision_gates_draft.md"

QUERY = """You are drafting §6 — Decision Gate Metrics for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

WORD BUDGET: ~180 words. Three quantitative Phase I go/no-go metrics:

1. **AI Acceleration Factor** (AF = n_baseline / n_BOFN): target >=3x vs. random baseline (conservative).
   Baseline structure: 4 baselines (B1=random, B2=expert DOE, B3=standard BO, B4=BOFN-mineral ablation) + BOFN as method under test. AF computed against each baseline independently.

2. **Discovery Yield** (compositions meeting all targets / total screened): target >=3% (PI-confirmed).

3. **Mineral-Burden Reduction** (critical mineral wt% vs. incumbent alloy): target >=30% reduction.

Also include:
- Scaling behavior statement: performance improves as CALPHAD database and experimental data grow
- AI Tool Disclosure statement (FOA requirement per FAQ): "This project uses AI tools including large language models for literature synthesis. All AI-generated content is reviewed and validated by the PI."

Using attached documents (especially project-metrics-v4-edison-refined.md and KPI review docs), draft polished prose for LaTeX. Formal, quantitative, reviewer-ready.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# §6 — Decision Gate Metrics (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
