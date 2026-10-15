#!/usr/bin/env python3
"""Edison ANALYSIS: Draft §1 — Background and Introduction (~300 words + ~80-word overview paragraph).

Drafts the opening overview paragraph and Background section of the FLAIME proposal narrative.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "background"
OUTPUT_FILE = "section1_background_draft.md"

QUERY = """You are drafting §1 — Background and Introduction for a DOE Genesis Mission Phase I proposal (Topic 3B: AI-Enabled Materials Discovery, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

STRUCTURE (two parts):
1. **Overview paragraph (~80 words):** Opens the narrative immediately. Lead with the NATIONAL PROBLEM, not the acronym. Start with: "The U.S. depends on foreign sources for 100% of its manganese and the majority of its chromium and zirconium..." Then introduce FLAIME as the solution. This is the elevator pitch for merit reviewers.

2. **Background body (~300 words):** Must cover (prioritized):
   - MUST-HAVE (~200w): Critical minerals challenge (Mn 100% import-reliant, Cr/Zr on USGS list → AMMTO alignment). Lead with urgency: "A single supply disruption could idle U.S. additive manufacturing production." Quantified impact (347,000 kg Be/year, $250-400M/yr Be-Cu market, CMI Hub >$80M follow-on). DOE CMS pillar language (Pillar 2, 3, 5). Gap: no existing SDL integrates powder→LPBF→tensile in closed loop. All confirmed AM Al alloy deployments use LPBF (AlSi10Mg satellites, Scalmalloy telecom parts, AL250C engine) — validates FLAIME's LPBF focus.
   - HIGH (~100w): FLAIME's contribution (BOFN-guided autonomous platform with mineral-burden objective). Competitive sharpening: "Existing platforms either stop at powder synthesis (A-Lab) or optimize process parameters without closing the composition loop (ORNL Peregrine)." "Why now" signal: recent advances in cost-aware BO make this tractable.
   - MEDIUM (~50w): PI as human-in-the-loop SDL leader (frugal twin review, SDL review structural materials lead author). Brief Genesis Mission forward reference.

- Reference Fig. 2 (CALPHAD screening + SEM/EDS experimental evidence)
- Include Buy America compliance statement
- Data source: Thermo-Calc TCAL10/TCMG6 databases

Using the attached documents, draft polished prose ready for LaTeX. Formal DOE proposal style — concise, quantitative. Output the overview paragraph first, then the background body, clearly labeled.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# §1 — Background and Introduction (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
