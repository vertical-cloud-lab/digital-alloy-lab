# EAGER mock-reviewer evaluation — Edison ANALYSIS + LITERATURE_HIGH

Spawned from PR #11 review feedback
([comment 4501651864](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/11#issuecomment-4501651864)):
*"how did this do? Send to edison analysis for feedback on how it did. In
parallel, send a high-effort literature query describing the results
you're seeing so far with this simple test and the general framework and
ask for advice/recommendations on how to improve this."*

Two tasks submitted in parallel.

## Tasks

| Field | ANALYSIS | LITERATURE_HIGH |
| --- | --- | --- |
| Job | `job-futurehouse-data-analysis-crow-high` | `job-futurehouse-paperqa3-high` |
| Task ID | `0427297c-0593-4d99-bdbf-aa912e98e184` | `ab6be84e-a426-4bdf-9365-c9266be7c2cd` |
| Submitted | 2026-05-20 ~18:58 UTC | 2026-05-20 ~18:58 UTC |
| Submitter | copilot coding agent (PR #11) | copilot coding agent (PR #11) |

## ANALYSIS — how did the framework do?

Uploaded files (5):

1. `nsf-resources-text/MOCK_REVIEWER_PLAYBOOK.md` — the system prompt the framework runs.
2. `eager-concept-outline-current.tex` — current state on `copilot/discuss-vertical-cloud-lab-idea` after the PI applied the 3 findings.
3. `nsf-resources-text/examples/eager-vcl-concept-outline.txt` — the rendered prose of the *earlier* revision that was the input to the mock review.
4. `nsf-resources-text/examples/review-output-eager.md` — the 1 Major + 2 Minor + 15/18 checklist mock review the framework produced.
5. `nsf-resources-text/examples/README-eager.md` — walkthrough of the three `retrieve.py` invocations.

Prompt asks for honest feedback on five axes:
A. quality of the review (false positives / false negatives);
B. quality of snippet retrieval (right anchors? missed sections?);
C. did the PI's rewrites actually resolve each finding;
D. systematic framework-level weaknesses from this one example;
E. likely PO outcome on the post-fix outline.

## LITERATURE_HIGH — how to improve the framework

Self-contained prompt (no uploads) describing the framework's current state
(619 structure-aware snippets, BM25 baseline R@5=0.867, modal-verb regex
for requirement-strength, single-LLM mock-reviewer playbook) and the
single-worked-example signal. Asks for 2024–2026 citation-rich
recommendations on eight axes: hybrid retrieval beyond BM25, chunking /
contextual retrieval, deontic / requirement-frame extraction, eval
harnesses (Ragas / TruLens / ARES / LLM-as-judge), mock-reviewer prompt
patterns, MCP serving, sample-size-of-one validation risk, and a
prioritized top-3 next-step list.

## Retrieval

```python
from edison_client import EdisonClient
import os
c = EdisonClient(api_key=os.environ["EDISON_API_KEY"])
analysis = c.get_task(task_id="0427297c-0593-4d99-bdbf-aa912e98e184")
lit = c.get_task(task_id="ab6be84e-a426-4bdf-9365-c9266be7c2cd")
```

ANALYSIS first poll ≥20 min; LITERATURE_HIGH first poll ≥21 min (per repo
memory of typical 20–21 min completion). Append syntheses to
`result-analysis.md` and `result-literature.md` once available. Raw JSON
is gitignored (`edison-trajectories/*.json`).

## Status

**Completed 2026-05-20.** ANALYSIS returned ~7.5k chars; LITERATURE_HIGH
returned ~23k chars. Full text in
[`result-analysis.md`](result-analysis.md) and
[`result-literature.md`](result-literature.md). Headline findings below.

### ANALYSIS — verdict on the EAGER run

* **Real wins.** Finding 1 (§II.F.3 preliminary-data exclusion) is a
  high-value, well-grounded flag. Budget-arithmetic check is genuinely
  useful.
* **One false positive.** Finding 3 (explicit IM/BI labels) is bloat at
  the concept-outline stage; the LLM itself noted §I.D.1 *permits*
  rather than requires it, but flagged it anyway.
* **Three false negatives the framework missed.**
  1. `\usepackage[margin=0.7in]{geometry}` violates PAPPG §II.C.2's
     1-inch margin rule (fatal at full-proposal stage).
  2. The post-fix draft claims "first scientific deployment of an
     electrified-tray VLM" while citing a *prior* electrified-tray VLM
     feasibility study (Baird 2025) — an overclaim a human would catch.
  3. Suggesting `CISE/IIS Robust Intelligence` as a tertiary unit is
     actually *bad* advice — that program explicitly does not fund
     applications of RI to existing domains. The framework hallucinated
     a program fit it cannot verify without RAG into NSF directorate
     pages.
* **Dogfooding-loop failure (the "Yes, dear" problem).** Edison
  verified that the PI's later "Trim back to 2 pages" commit
  **silently reverted Findings 1, 2, and 3** — line 28 is back to a
  single unit, line 64 is back to "Year~2 measures the backbone under
  realistic loads" (the original flagged framing), and the explicit
  IM/BI labels are gone. My PR #11 reply asserting the fixes were
  applied was wrong. The framework needs a programmatic re-check step.
* **Snippet-store gap.** BM25 on §I.D.1 + §II.F.3 missed the global
  formatting rules in §II.C.2 and the cap-raise to $400K in NSF Policy
  Supplement 26-200 (Dec 2025). Per-retrieval results need a
  universal "base compliance" snippet always injected.
* **PO verdict on post-fix draft.** Most likely outcome: *request more
  info / decline-with-feedback*, because Year-2 still reads as
  preliminary-data collection.

### LITERATURE_HIGH — recommendations (cited)

Eight-theme synthesis; top-three prioritized recommendations:

| # | Recommendation | Lift | Effort | Top citation |
| - | --- | --- | --- | --- |
| 1 | **BM25 → BM25 + BGE-M3 (or NV-Embed-v2) + bge-reranker-v2 hybrid.** Directly targets Hit@1 = 0.600. | +0.07 Recall@10, +0.08 MAP@10 on regulatory corpora; reranker further +30–45% nDCG@10 | 3–7 days | rayo2025ahybridapproach pp 2-3; alshehri2026neuralrerankingfor pp 17-20; lee2025nvembedimprovedtechniques pp 6-8 |
| 2 | **Anthropic-style contextual chunk enrichment + parent-child expansion** — keep current chunks, add ~50 tokens of LLM-generated context per snippet, return parent section when a child is retrieved. | nDCG@5 0.317 vs 0.309 (contextual vs late chunking); 62–64% → 72% answer correctness | 2–5 days | merola2025reconstructingcontext pp 9-15; junior2603adaptivechunkingoptimizing pp 8-9 |
| 3 | **Build a real eval harness** — expand to 50–100 stratified queries (LLM-generated + human review, ARES-style PPI), add RAGChecker / Deepchecks claim-level faithfulness scoring, plus adversarial red-team cases. | Largest reduction in FP/FN; protection against overfitting to current 15-query + 1-example signal | 5–10 days | saadfalcon2024aresanautomated pp 3-5; ru2024ragcheckerafinegrained pp 7-8; gerner2026deepchecksevaluatingretrievalaugmented pp 11-15 |

Other themes covered in [`result-literature.md`](result-literature.md):
deontic / requirement-frame extraction beyond modal-verb regex; mock-
reviewer playbook patterns (multi-agent debate, refusal-on-no-evidence,
JSON-schema output); MCP-server serving for non-code corpora; sample-
size-of-one validation risk and stratification guidance.

