# Worked example #1 — dogfooding the framework on a deliberately broken Project Summary

> See also: [worked example #2](README-eager.md) — running the framework
> on a real, intended-to-be-sent 1-page EAGER concept outline for
> [issue #9](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/issues/9).

This is an end-to-end demonstration of the
[`MOCK_REVIEWER_PLAYBOOK`](../MOCK_REVIEWER_PLAYBOOK.md) running over the
[Context7-style snippet store](../snippets/) on a **synthetic, deliberately
flawed** NSF Project Summary. The point is not the draft (which is throwaway)
but to show:

1. how few snippets you need to load (3 total, ~520 tokens) to give an LLM
   precise, citable review feedback on a Project Summary;
2. what the structured output looks like when each finding is grounded in a
   specific snippet id (e.g. `pappg-24-1#II.D.2.b`); and
3. that the requirement-strength labels (`required` / `prohibited` /
   `recommended`) line up with the actual modal verbs in the source PDF.

> Why a synthetic NSF draft when the actual proposal in this repo is a DOE
> Genesis Mission application? Because the corpus is NSF-targeted (PAPPG
> 24-1). A real test of the framework needs a draft against the same
> regulatory regime as the snippets — not a regime mismatch.

## Step 1 — Pick the test draft

A 5-paragraph, ~530-word, deliberately broken NSF "Project Summary" for a
made-up materials-discovery program. Built-in defects (so we can score the
review):

| # | Defect | PAPPG provision violated |
| --- | --- | --- |
| D1 | Missing the explicit "overview" subsection | `pappg-24-1#II.D.2.b` |
| D2 | Missing the explicit "intellectual merit" subsection | `pappg-24-1#II.D.2.b` |
| D3 | Missing the explicit "broader impacts" subsection | `pappg-24-1#II.D.2.b` |
| D4 | Reads like an abstract of the full proposal (PAPPG forbids that) | `pappg-24-1#II.D.2.b` |
| D5 | Embeds a URL inside the narrative (not allowed in Project Description per II.D.2.d.(ii); commonly mis-applied to Project Summary) | `pappg-24-1#II.D.2.d.(ii)` |
| D6 | Self-numbers pages (PAPPG says don't, Research.gov auto-paginates) | `pappg-24-1#II.C.1` |
| D7 | At ~530 words on the assumption of a 1.05-page set, would exceed the 1-page limit at typical 11pt single-spacing | `pappg-24-1#II.D.2.b` |

Draft is in [`dummy-project-summary.txt`](dummy-project-summary.txt).

## Step 2 — Pick the snippets to load (via retrieval)

Per the [Tier-1 spot-check mode](../MOCK_REVIEWER_PLAYBOOK.md) of the
playbook, for a Project Summary review we load **only** the snippets that
govern this single proposal section, not all of Chapter II. Use the
BM25 retriever to surface them with one focused query per rule family
(broad multi-topic queries dilute the BM25 signal — see *Caveats* in
`review-output.md`):

```bash
$ python nsf-resources-text/scripts/retrieve.py \
    "project summary overview intellectual merit broader impacts" \
    --doc pappg-24-1 --top-k 1
# 1  score=30.65  [NSF PAPPG 24-1 §II.D.2.b, p.49]   (required,    239t)

$ python nsf-resources-text/scripts/retrieve.py \
    "URLs not permitted in proposal" --doc pappg-24-1 --top-k 1
# 1  score= 9.82  [NSF PAPPG 24-1 §II.D.2.d.(ii), p.50] (prohibited, 222t)

$ python nsf-resources-text/scripts/retrieve.py \
    "page numbering pagination Research.gov" --doc pappg-24-1 --top-k 1
# 1  score=24.93  [NSF PAPPG 24-1 §II.C.1, p.42]    (recommended,  57t)
```

Three snippets, ~518 tokens total (vs. 58,824 for the whole Chapter II,
~110× smaller). Equivalent library form for an agent that wants the
records inline:

```python
import sys
sys.path.append('nsf-resources-text/scripts')
from retrieve import RetrievalIndex
idx = RetrievalIndex.load_default()
context = []
for q in [
    "project summary overview intellectual merit broader impacts",
    "URLs not permitted in proposal",
    "page numbering pagination Research.gov",
]:
    context.extend(h.snippet for h in idx.search(q, doc_id="pappg-24-1", top_k=1))
```

## Step 3 — Run the review

Apply the playbook's system prompt ([§2 of MOCK_REVIEWER_PLAYBOOK.md](../MOCK_REVIEWER_PLAYBOOK.md))
to the snippets above + the dummy draft. The structured output the
framework produces is in [`review-output.md`](review-output.md). Cite
each finding with the snippet's `source_label` field verbatim, e.g.
`[NSF PAPPG 24-1 §II.D.2.b, p.49]`.

## Step 4 — Score it

The framework caught **6 of 7** built-in defects, with correct snippet
citations and quoted evidence. See [`review-output.md`](review-output.md) §
"Scoring" for the breakdown.

## What this demonstrates

- **Token efficiency.** 518 tokens of regulatory context (vs. 59k for an
  unsharded Chapter II, vs. 228k for the whole corpus) is enough to cover
  every PAPPG provision a Project Summary touches.
- **Citation discipline.** Because every snippet ships with its `id`,
  `section_breadcrumbs`, `pages`, and `requirement_phrases`, the review
  output can quote back the exact source phrase that justifies each
  finding — no "PAPPG says somewhere that...".
- **Strength labels are useful, not decorative.** The `prohibited` /
  `required` / `recommended` tags map directly onto severity in the
  review output: a `required` violation is a Major finding, a `recommended`
  one is Minor.
- **Failure modes the dogfood test surfaced.** See the *Caveats* section
  of `review-output.md` — the 1-page-limit defect (D7) is hard to detect
  from prose alone because it's a layout property; this is the kind of
  thing a v2 should pair with a length-counter / layout linter.

## Reproducing

```bash
# Re-generate snippets if any source markdown changes:
python nsf-resources-text/scripts/tokenize_corpus.py

# Then load the 3 snippets above into your model of choice with the
# system prompt from MOCK_REVIEWER_PLAYBOOK.md and the draft from
# dummy-project-summary.txt. The expected output is review-output.md.
```
