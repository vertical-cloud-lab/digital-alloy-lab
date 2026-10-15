#!/usr/bin/env python3
"""Edison ANALYSIS: Draft DOE Title Page content.

Drafts the title page fields including Senior/Key Personnel table and partnership structure.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "title_page"
OUTPUT_FILE = "title_page_draft.md"

QUERY = """You are drafting the DOE Title Page content for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

Draft the following fields:

1. **Full Project Title:** "FLAIME: Fast Learning AI for Mineral Efficiency — Autonomous Discovery of Critical-Mineral-Lean Alloys for Advanced Manufacturing"

2. **Challenge and Focus Area:** Topic 3, Focus Area B: AI-Enabled Materials Discovery and Engineering (AMMTO)

3. **Senior/Key Personnel Table:**
| Institution | Role | Senior/Key Personnel |
|-------------|------|---------------------|
| BYU (Lead) | Prime | S. G. Baird (PI); 2 MS students, 10 UG researchers |
| Valimet, Inc. (Stockton, CA) | Subawardee | [Contact TBD] — gas atomization services |
| AMAZEMET (Białystok, Poland) | Collaborator | [Contact TBD] — ultrasonic atomization technology |
| Thermo-Calc Software (Stockholm/Pittsburgh) | Collaborator | Thermo-Calc's account manager — CALPHAD/AM Module support |

4. **2-of-3 Team Composition (FOA §II.E):**
   - BYU: Institution of Higher Education (Category 3) ✓
   - Valimet: Industry (Category 2) ✓
   - Ames National Lab: DOE Lab connection via letter of support (Category 1 — advisory, not formal team member)

5. **Budget Summary:**
   - Total: $750,000
   - Period: 9 months (Phase I)
   - Cost Share: Not required per FOA

6. **PI Information:**
   - Sterling G. Baird, Ph.D.
   - Assistant Professor, Department of Materials Science & Engineering
   - Brigham Young University, Provo, UT 84602

Format as structured content ready for the LaTeX template fields. Formal DOE style.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# DOE Title Page (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
