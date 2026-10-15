#!/usr/bin/env python3
"""Edison ANALYSIS: Draft §2 — Project Objectives (~250 words).

Drafts the objectives section with quantitative targets and commercialization content.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "objectives"
OUTPUT_FILE = "section2_objectives_draft.md"

QUERY = """You are drafting §2 — Project Objectives for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

WORD BUDGET: ~250 words total. Structure with explicit priority tiers:

MUST-HAVE (~70w): 5 quantitative objectives as a numbered list, FRONT-LOADED immediately after section header:
  O1: Demonstrate closed-loop BOFN/pKGFN platform for autonomous alloy screening
  O2: Screen >=200 Al-alloy compositions computationally via CALPHAD + mineral-burden objective
  O3: Validate >=200 compositions experimentally through the MVS pipeline (2 compositions/day, 6 days/week, 9 months; ~468 theoretical max, >=200 accounts for ramp-up)
  O4: Achieve discovery yield >=3% (overall yield; complementary metric: >=20% Tier 1 pass rate among fully tested compositions)
  O5: Demonstrate AI acceleration factor >=3x vs. random baseline

MUST-HAVE (~30w): TRL advancement: TRL 2 (BOFN DAG + CALPHAD designed) → TRL 4 Phase I (closed-loop validated on real Al alloys) → TRL 6 Phase II (system in relevant environment with industry-scale powders)

MUST-HAVE (~15w): Scope statement: "Phase I focuses exclusively on Al alloys processed by LPBF, with Cu-Cr-Zr as a stretch demonstration"

HIGH (~40w): Market sizing ($250-400M/yr Be-Cu replacement) + industry pathway (Valimet → Fehrmann Materials GmbH)

HIGH (~25w): IP strategy: "FLAIME platform open-source; Month-6 internal review to assess selective IP for top compositions"

HIGH (~15w): Integrating sentence after O1-O5 linking dual mandate of Topic 3B

MEDIUM (~25w): Phase II vision — ONE vivid example: "Phase II will extend FLAIME to AMMTO priority alloys (e.g., 316H for nuclear structural applications)"

MEDIUM (~20w): Technology transfer sentence

Using attached documents, draft polished prose for LaTeX. Formal, quantitative, reviewer-ready.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# §2 — Project Objectives (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
