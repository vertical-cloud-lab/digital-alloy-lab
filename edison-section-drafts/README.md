# Edison Section Draft Scripts

Modular scripts for drafting each section/component of the FLAIME Genesis Mission proposal using Edison Scientific's ANALYSIS API. Each script can be run independently or all can be run in parallel.

## Setup

```bash
pip install edison-client>=0.11.0
export EDISON_API_KEY="your-api-key"
```

## Usage

### Run all sections in parallel (~10-15 min wall time)
```bash
python run_all_parallel.py
```

### Run specific sections
```bash
python run_all_parallel.py --scripts draft_section1_background draft_section3_methods
```

### Run a single section
```bash
python draft_section1_background.py
```

### Dry run (list scripts without executing)
```bash
python run_all_parallel.py --dry-run
```

### Control concurrency
```bash
python run_all_parallel.py --max-workers 4  # Default: 6
```

## Scripts (13 total)

| Script | Section | Word Target |
|--------|---------|-------------|
| `draft_section0_abstract.py` | §0 — Project Summary / Abstract | ~250w |
| `draft_title_page.py` | DOE Title Page | Structured fields |
| `draft_section1_background.py` | §1 — Background and Introduction | ~80w overview + ~300w body |
| `draft_section2_objectives.py` | §2 — Project Objectives | ~250w |
| `draft_section3_methods.py` | §3 — Proposed Research and Methods | ~400w |
| `draft_section4_milestones.py` | §4 — Milestones in the Nine Months | ~200w + Table 1 |
| `draft_section5_data_sources.py` | §5 — Data Sources and Models | ~160w |
| `draft_section6_decision_gates.py` | §6 — Decision Gate Metrics | ~180w |
| `draft_appendix1_bibliography.py` | Appendix 1 — Bibliography | ~15-20 refs |
| `draft_appendix2_facilities.py` | Appendix 2 — Facilities & Resources | ~250w |
| `draft_appendix4_dmsp.py` | Appendix 4 — DMSP | ~300w |
| `draft_appendix5_synergistic.py` | Appendix 5 — Synergistic Activities | 5 activities |
| `draft_budget_justification.py` | Budget Justification | ~500w |

## Output

Results are saved to `results/` directory as Markdown files. Each file contains the Edison-drafted content ready for review and integration into the LaTeX template.

## Architecture

- `edison_utils.py` — Shared utilities (Edison client, file upload, polling, context file management)
- Each `draft_*.py` — Self-contained script with section-specific query and source file list
- `run_all_parallel.py` — Parallel runner using ThreadPoolExecutor

Each script:
1. Uploads core context files (proposal plan, checklist, LaTeX template, synthesis docs)
2. Uploads section-specific source documents
3. Submits an Edison ANALYSIS task with a detailed drafting prompt
4. Polls until completion (~8-12 min per task)
5. Saves the result to `results/`
