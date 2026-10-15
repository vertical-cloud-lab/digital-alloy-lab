#!/usr/bin/env python3
"""Edison ANALYSIS: Draft Appendix 5 — Synergistic Activities.

Drafts the 5 synergistic activities for PI biosketch (<=1 page).
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "synergistic"
OUTPUT_FILE = "appendix5_synergistic_draft.md"

QUERY = """You are drafting Appendix 5 — Synergistic Activities for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PI: Sterling G. Baird, Brigham Young University

CONSTRAINT: <=5 activities, <=1 page total. Each activity ~3-4 sentences.

ACTIVITY 1: SDL Leadership & Community Building
- npj Computational Materials Guest Editor for "Self-driving Labs for Chemistry and Materials Science" collection (2024-present)
- Chemical Reviews SDL review lead author (structural materials section)
- Frugal Twin review lead author (Lo et al. 2024)
- AC BO Hackathon solo organizer (120 participants, 62 orgs, 14 countries)
- MRS Fall 2025 presentation: "Autonomous Vertical Cloud Lab for Additively Manufactured Aerospace Alloys"

ACTIVITY 2: Open-Source Software & Community Infrastructure
- 17,000+ open-source code contributions (15K commits, 1.5K issues, 913 PRs)
- Honegumi tutorial framework (JOSS 2025)
- Meta BoTorch Technical Consultant (Nov 2024–Jan 2025, letter of support)
- xtal2png (JOSS 2022)
- 350+ SDL kits deployed worldwide

ACTIVITY 3: Training & Workforce Development
- ~5,000 person-hours of SDL training to ~700 individuals across ~62 organizations
- Built AC Dev Lab from scratch ($600K, 500 line items, 24 months)
- 200+ hours course content
- Supervised 12 staff + 8 students

ACTIVITY 4: Standardization & Open Science
- POSE (Pathways to Open Source Ecosystems) PI for materials informatics toolchain
- Acceleration Consortium community standards contributor
- FAIR data practices: schema.org metadata templates for SDL datasets
- GCMAC presenter (2024, 2025)
- NSF TIP Directorate Review Panelist (2026)
- IEC/ISO materials data working groups

ACTIVITY 5: Open Data Impact & Domain Expertise
- MPTS-52 dataset heavily reused by crystal structure generative AI community
- Matbench-genmetrics benchmarking framework (JOSS 2024)
- Fehrmann Materials GmbH contract ($34K, ML for Al alloys)
- Zenodo/Figshare deposits with documented reuse metrics

Draft polished prose suitable for a DOE biosketch appendix. Professional, achievement-focused, quantitative.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# Appendix 5 — Synergistic Activities (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
