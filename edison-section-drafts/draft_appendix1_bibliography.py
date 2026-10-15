#!/usr/bin/env python3
"""Edison ANALYSIS: Draft Appendix 1 — Bibliography & References Cited.

Generates a formatted BibTeX-ready reference list for the proposal.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "bibliography"
OUTPUT_FILE = "appendix1_bibliography_draft.md"

QUERY = """You are drafting Appendix 1 — Bibliography & References Cited for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

Generate a formatted reference list (~15-20 references) that MUST include:

REQUIRED (from template guidance):
- Abolhasani & Kumacheva 2023 (Nat. Synth.) — self-driving labs overview
- Stach et al. 2021 (Matter) — autonomous experimentation
- Hart et al. 2021 (Nat. Rev. Mater.) — BYU co-author, machine learning in materials
- Astudillo & Frazier 2019 (ICML) — BOFN (Bayesian Optimization of Function Networks)
- Khatamsaz et al. 2023 (npj Comput. Mater.) — cost-aware BO for alloys
- AMMT Roadmap 2025 (DOE AMMTO) — Additive Manufacturing roadmap
- Liang et al. 2025 (Sci. Adv.) — recent SDL/AM work

ADDITIONAL RECOMMENDED:
- Bukkapatnam 2023 (AMDM framework)
- Chawla et al. 2025 (cost-aware BO)
- Alvi et al. 2026 (npj) — recent materials/AI
- ISO 52902 (AM benchmark test artifacts)
- ASTM E8/E8M (tensile testing standard)
- ISO 52907 (AM powder characterization)
- Lo et al. 2024 — frugal twin review (PI co-author)
- SDL review paper (PI lead author on structural materials section)
- Sabanza Gil et al. 2025 (Nature Comp. Sci.) — CALPHAD+ML
- DOE Critical Materials Strategy 2023

Format each reference with: Authors, Year, Title, Journal/Publisher, DOI where available.
Output as a numbered list suitable for LaTeX \\bibitem entries.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# Appendix 1 — Bibliography (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
