#!/usr/bin/env python3
"""Edison ANALYSIS: Draft Budget Justification narrative.

Drafts the budget justification text for the SF-424 R&R Budget form.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "budget"
OUTPUT_FILE = "budget_justification_draft.md"

QUERY = """You are drafting the Budget Justification narrative for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

TOTAL BUDGET: $750K for 9-month Phase I

BUDGET BREAKDOWN:
| Category | Direct | Total (w/ F&A) |
|----------|--------|----------------|
| Personnel (PI + 2 MS + 10 UGs) | ~$330K | ~$393K |
| Materials & Supplies | ~$80K | ~$95K |
| Travel | ~$15K | ~$18K |
| Subaward: Valimet (gas atomization) | [partner amount removed] | [partner amount removed] |
| Other Direct (software, services) | ~$50K | ~$60K |
| Indirect (F&A) | — | ~$154K |

KEY POINTS:
- Personnel: PI, 2 MS students (full-time research), 10 UGs at $30/hr operating in shifts for 6-day/week lab coverage
- AMAZEMET and Thermo-Calc are BYU direct costs (equipment supplies, software licenses) — NOT subawards
- Valimet is the ONLY subaward (gas atomization services for comparison with ultrasonic)
- F&A rate: BYU's negotiated rate (typically ~50% MTDC)
- Budget mechanism: AMAZEMET costs = consumables + maintenance; TC costs = license upgrade (TCAL10 + AM Module)
- Travel: 1 trip to DOE review, 1 conference (MRS or TMS)

Draft a clear, line-item-justified budget narrative suitable for the SF-424 budget justification. Each category should explain WHY the cost is necessary and HOW it supports the technical objectives. ~500 words. Formal DOE style.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# Budget Justification (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
