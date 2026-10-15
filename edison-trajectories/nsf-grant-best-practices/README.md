# NSF grant-writing best practices — Edison literature query

High-effort Edison literature task supporting issue #11 (and #10).

## Task

| Field | Value |
| --- | --- |
| Job | `LITERATURE_HIGH` (`job-futurehouse-paperqa3-high`) |
| Task ID | `aef69217-645d-4581-96e7-2c922544c2d2` |
| Submitted | 2026-05-06 |
| Submitter | copilot coding agent (issue resolution) |

Note on credits: per repo convention, `LITERATURE_HIGH` is the costlier deep variant
of the literature search (vs. the 1-credit base `LITERATURE`). High effort was
explicitly requested in the issue.

## Prompt

> Provide a comprehensive, citation-rich literature review of best practices and
> official requirements for writing competitive U.S. National Science Foundation
> (NSF) grant proposals, with particular emphasis on (1) the NSF Proposal & Award
> Policies & Procedures Guide (PAPPG, current edition NSF 24-1, plus 2026
> supplements 26-200/26-202 / Gold Standard Science), (2) the two NSF Merit Review
> Criteria (Intellectual Merit and Broader Impacts), (3) EAGER (EArly-concept Grants
> for Exploratory Research) mechanism guidance and successful EAGER proposal
> characteristics, (4) the curriculum, principles, and published advice from Grant
> Writers' Seminars & Workshops (GWSW) — especially Russell & Morrison's "Grant
> Application Writer's Workbook" — covering hypothesis-driven framing, the
> "specific aims" page, reviewer-centric writing, and pitfalls, (5) other widely
> cited NSF / federal grant-writing best-practice resources (Robert Porter, NSF
> program-officer talks, ProfHacker, Inside Higher Ed, IRIS, NCURA, etc.), and
> (6) empirical studies of what predicts NSF funding success (proposal length, PI
> demographics, prior funding, collaboration structure, broader-impacts framing,
> etc.). Organize the review by these six themes; for each, list the canonical
> primary sources, the consensus best practices, the most-cited disagreements, and
> concrete actionable rules for a PI preparing an NSF proposal in 2026. Cite
> everything with full bibliographic detail and direct URLs where possible.

## Retrieval

Edison `LITERATURE_HIGH` tasks typically take 25-40+ minutes (often longer for the
high-effort variant). To retrieve:

```python
from edison_client import EdisonClient
import os
c = EdisonClient(api_key=os.environ["EDISON_API_KEY"])
r = c.get_task(task_id="aef69217-645d-4581-96e7-2c922544c2d2")
```

When the task completes, save the returned synthesis to `result.md` in this
directory (do not commit the raw JSON — see `.gitignore` rule
`edison-trajectories/*.json`).

## Status

**Completed 2026-05-06 03:45 UTC.** Full result in
[`result.md`](result.md) (~39k chars; six-theme matrix with concrete
actionable rules + citations).

### One-line takeaways per theme

1. **PAPPG requirements.** Build to the official structure first
   (1-page Project Summary with explicit Overview/IM/BI; 15-page
   Project Description; URLs may not carry substantive content).
2. **Merit Review Criteria.** Make IM and BI parallel and concrete:
   each needs goals + activities + feasibility + assessment.
3. **EAGER.** Talk to the program officer first; justify mechanism fit
   on page 1; keep scope small and proof-of-concept-like.
4. **GWSW / Russell & Morrison.** Even for NSF, draft a "specific
   aims"-style opening (problem → gap → idea → 2-4 aims → approach →
   payoff); replace generic verbs with testable aims.
5. **Other best-practice resources.** Write for impatient mixed-expertise
   reviewers; contact PO early with a 1-page concept; use internal
   red-team review.
6. **Empirical predictors.** Modest evidence that confident, promotional
   language helps; structural factors (collaborations, panel service,
   resubmission) matter more than wordsmithing.
