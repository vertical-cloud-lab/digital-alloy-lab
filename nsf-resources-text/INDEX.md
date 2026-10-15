# nsf-resources-text — LLM-friendly index

Plain-text (markdown) extractions of every PDF in `nsf-resources/`, intended as
context for LLM-driven proposal review and drafting feedback. Token counts are
estimated as `chars / 4` (OpenAI heuristic).

**Total corpus:** 50 files, ~227,684 estimated tokens.

> ### 🔎 Looking for tokenized snippets?
> The raw markdown files below are PDF dumps and are not, on their own,
> particularly LLM-friendly. For Context7-style structured snippets — one
> JSON record per PAPPG section (`II.A.1`, `II.D.2.b`, …) with breadcrumb
> path, requirement strength (must / shall / should / may / informational),
> page span, source URL, and ~1,200-token chunks — see
> [`snippets/`](snippets/) (regenerate with
> `python scripts/tokenize_corpus.py`). A root [`../llms.txt`](../llms.txt)
> indexes the snippet store per the [llmstxt.org](https://llmstxt.org)
> convention.

For a structured prompt that turns this corpus into a usable mock-reviewer, see
[`MOCK_REVIEWER_PLAYBOOK.md`](MOCK_REVIEWER_PLAYBOOK.md).

A machine-readable manifest of all files (with paths, page counts, character
counts, and token estimates) is in [`_manifest.json`](_manifest.json).

## NSF PAPPG 24-1 — split by chapter

The full PAPPG (~189k tokens) is too large for most LLM contexts. It is split
into per-chapter files under `pappg-24-1/`. Load only the chapter(s) relevant
to the review task at hand.

| File | est. tokens | Title |
| --- | ---: | --- |
| `pappg-24-1/00-front-matter.md` | 25,316 | 00 front matter |
| `pappg-24-1/01-chapter-I.md` | 8,605 | 01 chapter I |
| `pappg-24-1/02-chapter-II.md` | 58,824 | 02 chapter II |
| `pappg-24-1/03-chapter-III.md` | 6,617 | 03 chapter III |
| `pappg-24-1/04-chapter-IV.md` | 3,862 | 04 chapter IV |
| `pappg-24-1/05-chapter-V.md` | 1,394 | 05 chapter V |
| `pappg-24-1/06-chapter-VI.md` | 3,658 | 06 chapter VI |
| `pappg-24-1/07-chapter-VII.md` | 11,347 | 07 chapter VII |
| `pappg-24-1/08-chapter-VIII.md` | 6,382 | 08 chapter VIII |
| `pappg-24-1/09-chapter-IX.md` | 8,785 | 09 chapter IX |
| `pappg-24-1/10-chapter-X.md` | 5,744 | 10 chapter X |
| `pappg-24-1/11-chapter-XI.md` | 23,202 | 11 chapter XI |
| `pappg-24-1/12-chapter-XII.md` | 25,232 | 12 chapter XII |

The unsplit single-file extraction is also retained at
`nsf-resources-text/pappg-24-1.md` (~189k tokens) for tools with very large
context windows or for grep-based searching.

## NSF Gold Standard Science (GSS) — supplements 26-200 / 26-202

| File | est. tokens | Title |
| --- | ---: | --- |
| `federal-register-2024-29244-gss.md` | 3,444 | federal register 2024 29244 gss |
| `gold-standard-science-implementation-plan-2025.md` | 3,272 | gold standard science implementation plan 2025 |
| `ostp-gss-guidance-june-2025.md` | 4,706 | ostp gss guidance june 2025 |

## Grant Writers' Seminars & Workshops (GWSW) — *Grant Application Writer's Workbook* sample chapters

### NSF workbook (most directly relevant)

| File | est. tokens | Chapter |
| --- | ---: | --- |
| `grant-writers-seminars-workshops/nsf/NSF-Budget-Justification.md` | 806 | NSF Budget Justification |
| `grant-writers-seminars-workshops/nsf/NSF-Learning-Milestones-for-Chapter-12.md` | 1,307 | NSF Learning Milestones for Chapter 12 |
| `grant-writers-seminars-workshops/nsf/OverviewTemplateMasterPlanNSF2021.md` | 676 | OverviewTemplateMasterPlanNSF2021 |
| `grant-writers-seminars-workshops/nsf/Pre-SubmissionReviewNSF2021.md` | 682 | Pre SubmissionReviewNSF2021 |
| `grant-writers-seminars-workshops/nsf/Principal-Changes-in-this-Edition.md` | 563 | Principal Changes in this Edition |
| `grant-writers-seminars-workshops/nsf/Table-of-Contents.md` | 614 | Table of Contents |

### NIH workbook (transferable: significance/innovation, rigor, key personnel framing)

| File | est. tokens | Chapter |
| --- | ---: | --- |
| `grant-writers-seminars-workshops/nih/Find-Program-Grant-Mechanism-2022.md` | 746 | Find Program Grant Mechanism 2022 |
| `grant-writers-seminars-workshops/nih/Learning-Milestones-Chapter-11.md` | 1,554 | Learning Milestones Chapter 11 |
| `grant-writers-seminars-workshops/nih/NIH25-Significance-Innovation-Subsections.md` | 681 | NIH25 Significance Innovation Subsections |
| `grant-writers-seminars-workshops/nih/NIH25-Table-of-Contents.md` | 801 | NIH25 Table of Contents |
| `grant-writers-seminars-workshops/nih/Preface-for-website.md` | 1,558 | Preface for website |
| `grant-writers-seminars-workshops/nih/Principle-Changes-in-this-Edition.md` | 824 | Principle Changes in this Edition |
| `grant-writers-seminars-workshops/nih/Rigor-of-Research-Design.md` | 850 | Rigor of Research Design |
| `grant-writers-seminars-workshops/nih/Senior-Key-Personnel.md` | 793 | Senior Key Personnel |

### USDA NIFA workbook (parallel reference for AFRI proposals)

| File | est. tokens | Chapter |
| --- | ---: | --- |
| `grant-writers-seminars-workshops/usda-nifa/USDABlueprintforProjectNarrative2021.md` | 719 | USDABlueprintforProjectNarrative2021 |
| `grant-writers-seminars-workshops/usda-nifa/USDABudgetJustification2021.md` | 872 | USDABudgetJustification2021 |
| `grant-writers-seminars-workshops/usda-nifa/USDAFacilitiesandOtherResources2021.md` | 1,000 | USDAFacilitiesandOtherResources2021 |
| `grant-writers-seminars-workshops/usda-nifa/USDAPrincipalChanges2021.md` | 515 | USDAPrincipalChanges2021 |
| `grant-writers-seminars-workshops/usda-nifa/USDAScoringandRanking2021.md` | 784 | USDAScoringandRanking2021 |
| `grant-writers-seminars-workshops/usda-nifa/USDASentenceStemsforOverview2021.md` | 767 | USDASentenceStemsforOverview2021 |
| `grant-writers-seminars-workshops/usda-nifa/USDATableofContents2021.md` | 553 | USDATableofContents2021 |

### Any-other-agency workbook (universals: abstract, overview, body)

| File | est. tokens | Chapter |
| --- | ---: | --- |
| `grant-writers-seminars-workshops/any-agency/BackgroundandNeedsAssessment.md` | 890 | BackgroundandNeedsAssessment |
| `grant-writers-seminars-workshops/any-agency/BeforeYouBegintoWrite.md` | 750 | BeforeYouBegintoWrite |
| `grant-writers-seminars-workshops/any-agency/DevelopmentofAbstract.md` | 849 | DevelopmentofAbstract |
| `grant-writers-seminars-workshops/any-agency/DevelopmentofOverviewSection.md` | 844 | DevelopmentofOverviewSection |
| `grant-writers-seminars-workshops/any-agency/TableofContents.md` | 396 | TableofContents |
| `grant-writers-seminars-workshops/any-agency/WritingtheBodyofYourProposal.md` | 918 | WritingtheBodyofYourProposal |

### Biomedical-publication workbook (introduction/discussion craft)

| File | est. tokens | Chapter |
| --- | ---: | --- |
| `grant-writers-seminars-workshops/biomedical-publication/Deciding-on-Co-Authors.md` | 737 | Deciding on Co Authors |
| `grant-writers-seminars-workshops/biomedical-publication/Deciding-on-a-Journal.md` | 824 | Deciding on a Journal |
| `grant-writers-seminars-workshops/biomedical-publication/Review-of-the-Manuscript.md` | 823 | Review of the Manuscript |
| `grant-writers-seminars-workshops/biomedical-publication/Table-of-Contents-BP.md` | 426 | Table of Contents BP |
| `grant-writers-seminars-workshops/biomedical-publication/The-Discussion.md` | 593 | The Discussion |
| `grant-writers-seminars-workshops/biomedical-publication/The-Introduction.md` | 761 | The Introduction |
| `grant-writers-seminars-workshops/biomedical-publication/What-When-to-Publish.md` | 818 | What When to Publish |

## Conventions

* Each `.md` file starts with a YAML frontmatter block: `source_pdf`, `pages`
  (where applicable), `chars`, `est_tokens`, plus PAPPG-specific fields.
* Page boundaries inside the body are marked with HTML comments
  `<!-- page N -->` so an LLM can cite "PAPPG p.42" precisely.
* Layout artefacts (headers/footers, footnote-then-body order, table cells
  reflowed into prose) are present — pymupdf's `text` extractor preserves
  reading order best-effort but is not perfect. When precision matters, fall
  back to the source PDF in `../nsf-resources/`.
* The PDFs themselves remain authoritative; the `.md` files are derived.
