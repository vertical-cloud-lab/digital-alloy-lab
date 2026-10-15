#!/usr/bin/env python3
"""Edison ANALYSIS: Draft §4 — Milestones (~200 words + Table 1).

Drafts the milestone schedule and KPI go/no-go dashboard table.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "milestones"
OUTPUT_FILE = "section4_milestones_draft.md"

QUERY = """You are drafting §4 — Milestones in the Nine Months for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

WORD BUDGET: ~200 words of narrative text + Table 1 (KPI/go-no-go dashboard).

MILESTONE SCHEDULE:
- M1 (Month 1): BOFN DAG + CALPHAD screening pipeline operational, first candidates selected
- M2 (Month 2): First atomized powder batches characterized (PSD, SEM/EDS, flow)
- M3/G1 (Month 3): Go/No-Go G1 — >=50 compositions screened, surrogate RMSE < threshold
- M4/G2 (Month 5): Go/No-Go G2 — Closed-loop cycle demonstrated end-to-end
- M5/G3 (Month 7): Go/No-Go G3 — >=1 alloy meeting YS>=250 MPa, EL>=5%
- M6 (Month 9): Final deliverables: digital thread, Phase II readiness assessment

TABLE 1 — KPI/Go-No-Go Dashboard (5 KPIs):
| KPI | Threshold | Measurement | Triggered Optimizer Action |
Example KPIs: AI Acceleration Factor (>=3x), Discovery Yield (>=3%), Mineral-Burden Reduction (>=30%), Surrogate RMSE, Closed-Loop Throughput

Include brief narrative framing the 6-month DOE programmatic review point (M3-M5 demonstrate sufficient progress).

The table should be formatted as LaTeX (using booktabs) ready to paste into the template.

Using attached documents (especially project-metrics-v4-edison-refined.md and preliminary-results-roadmap.md), draft polished content. Formal, quantitative, reviewer-ready.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# §4 — Milestones (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
