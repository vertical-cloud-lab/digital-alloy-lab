#!/usr/bin/env python3
"""Edison ANALYSIS: Draft §0 — Project Summary / Abstract (~250 words).

Drafts the Field 7 abstract for the FLAIME Genesis Mission proposal.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "abstract"
OUTPUT_FILE = "section0_abstract_draft.md"

QUERY = """You are drafting the Project Summary / Abstract (Field 7) for a DOE Genesis Mission Phase I proposal.

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency) — an autonomous closed-loop platform for discovering critical-mineral-lean aluminum alloys via AI-guided optimization.

CONSTRAINTS:
- ~250 words maximum
- Must cover: (1) vision/problem statement (U.S. critical mineral dependence for Mn, Cr, Zr), (2) AI advantage thesis (BOFN + pKGFN reduces experiments 10x vs conventional DOE), (3) critical minerals relevance (Al-Mn-Cr-Zr family), (4) expected outcomes (>=200 compositions screened, digital thread on AmSC), (5) TRL statement (enters Phase I at TRL 2, targets TRL 4 exit)
- Full project title: "FLAIME: Fast Learning AI for Mineral Efficiency — Autonomous Discovery of Critical-Mineral-Lean Alloys for Advanced Manufacturing"
- Topic 3B: AI-Enabled Materials Discovery and Engineering (AMMTO)
- PI: Sterling G. Baird, Brigham Young University
- Team: PI + 2 MS students + 10 UG researchers; subaward to Valimet (gas atomization)
- Budget: $750K for 9-month Phase I
- Discovery yield target: >=3%
- Throughput: up to 2 unique compositions/day, 6 days/week

Using the attached source documents (proposal plan, checklist, synthesis docs, metrics), draft a polished ~250-word abstract. Write in formal DOE proposal style — concise, quantitative, reviewer-ready. Do NOT use placeholder text. Output the abstract text only, ready to paste into LaTeX.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# §0 — Project Summary / Abstract (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
