# Worked example #2 — EAGER concept outline (issue #9 / PR #10, vertical-cloud-lab)

The first [worked example](README.md) ran the framework on a
deliberately-broken NSF Project Summary to show the framework finding
known defects. This second example runs it on the **real, 2-page EAGER
concept outline** drafted on
[PR #10](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/10)
(`copilot/discuss-vertical-cloud-lab-idea`,
[`eager-concept-outline.tex`](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/blob/copilot/discuss-vertical-cloud-lab-idea/eager-concept-outline.tex)
at commit cb59e56) for [issue #9](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/issues/9) —
the vertical-cloud-lab pitch of a vertical-lift module + UR5e arm as
the integration backbone for a 50-printer asynchronous Bambu A1 Mini
print farm, intended to be sent to a cognizant ENG/CMMI Program Officer
as a pre-submission inquiry.

The point of this run is to test whether the framework adds value on a
**different document type** (concept outline vs. project summary) where
the **defects are not pre-planted** — i.e., as a real pre-submission
sanity check on a draft that is already in good shape.

## Step 1 — The draft

The source-of-truth draft is the `.tex` (with compiled PDF) on PR #10.
[`eager-vcl-concept-outline.txt`](eager-vcl-concept-outline.txt) is the
prose extracted from that `.tex` (figures, table, and LaTeX layout
commands stripped) so the snippet-store reviewer has a clean text
input. Word counts and numbers are preserved.

The draft is 2 pages at 11 pt with two figures and a budget table, has
a single primary unit (ENG/CMMI Advanced Manufacturing), four
quantitative Year-1 go/no-go gates, a $279K two-year budget under the
$300K EAGER cap, and prior feasibility data from the PI's earlier work
at U. Toronto's Acceleration Consortium.

## Step 2 — Pick the snippets via retrieval

Three focused BM25 queries surface the three governing rule snippets:

```bash
$ python nsf-resources-text/scripts/retrieve.py \
    "EAGER concept outline program officer concurrence required eight pages" \
    --doc pappg-24-1 --top-k 1
# 1  score=26.45  [NSF PAPPG 24-1 §II.F.3, p.84]   (required,   902t)

$ python nsf-resources-text/scripts/retrieve.py \
    "concept outline required content title PI keywords narrative description" \
    --doc pappg-24-1 --top-k 1
# 1  score=29.44  [NSF PAPPG 24-1 §I.D.1, p.31]    (prohibited, 730t)

$ python nsf-resources-text/scripts/retrieve.py \
    "merit review criteria intellectual merit broader impacts" \
    --doc pappg-24-1 --top-k 1
# 1  score=30.74  [NSF PAPPG 24-1 §III.A.2, p.110] (required,   401t)
```

Total context: ~2,033 tokens of regulatory text (vs. 207k for the whole
corpus, ~100× smaller). The retriever found the right §I.D.1 *Concept
Outlines* snippet from a query that paraphrases its content rather than
matching its title literally — useful regression signal for the eval
harness.

## Step 3 — Run the review

Apply the [`MOCK_REVIEWER_PLAYBOOK`](../MOCK_REVIEWER_PLAYBOOK.md) §2
system prompt to the snippets above + the draft. Output is in
[`review-output-eager.md`](review-output-eager.md).

## Step 4 — Score

| Type | Count |
| --- | ---: |
| Required elements satisfied | 15 of 18 |
| Critical violations (return without review) | 0 |
| Major findings (must fix before sending) | 1 |
| Minor reframes (should fix) | 2 |

The one Major finding is real: the Year-2 measurement-campaign paragraph
could be misread as preliminary-data collection (a §II.F.3 EAGER
exclusion). The suggested ~25-word reframe at the top of Year 2
("stress-tests the *hypothesis* under load, not the print farm itself")
re-anchors the campaigns on the central transformative claim.

The two Minors are also useful but lower-stakes: list 2-3 candidate NSF
units instead of one (§I.D.1 says "unit(s)") to give the recipient PO
a clean redirect path; and add an explicit IM/BI sentence (permissive
at concept-outline stage per §I.D.1's *may*; required for the eventual
full proposal per §III.A.2).

## What this demonstrates about the framework

- **Generalizes across document types.** Same retriever + same
  playbook handle a Project Summary (worked example #1) and a 2-page
  concept outline (this run) with no code changes.
- **Calibrated severity.** Worked example #1 (synthetic, deliberately
  broken) found 6 Majors. This run (real, well-prepared draft) found
  1 Major + 2 Minors. The framework reports findings at whatever
  severity the draft actually warrants.
- **Useful before, not after.** The right time to run this is
  *before* emailing the PO, when reframing 25 words is cheap. After
  the PO email, the cost of a "this looks like preliminary-data
  collection, please re-scope" reply is a multi-week round-trip.
- **Limits surfaced honestly.** The framework cannot check
  funding-opportunity-specific length limits (live in DCLs and
  program solicitations, not PAPPG), cannot verify the current
  cognizant NSF unit (could have moved in a reorg), and cannot
  fact-check cited literature. The review-output explicitly flags
  these as v2 work.

## Reproducing

```bash
# Re-run the retrieval to confirm the same 3 snippets surface:
python nsf-resources-text/scripts/retrieve.py \
    "EAGER concept outline program officer concurrence required eight pages" \
    --doc pappg-24-1 --top-k 1
python nsf-resources-text/scripts/retrieve.py \
    "concept outline required content title PI keywords narrative description" \
    --doc pappg-24-1 --top-k 1
python nsf-resources-text/scripts/retrieve.py \
    "merit review criteria intellectual merit broader impacts" \
    --doc pappg-24-1 --top-k 1

# Then load those 3 snippets + eager-vcl-concept-outline.txt into your
# model of choice with the MOCK_REVIEWER_PLAYBOOK.md system prompt;
# the expected output is review-output-eager.md.
```
