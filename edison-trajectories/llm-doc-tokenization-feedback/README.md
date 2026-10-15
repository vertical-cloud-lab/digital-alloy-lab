# Edison feedback on the Context7-style tokenization framework

## Task

- **Task ID:** `660a4e59-342b-49d0-95bf-4d61e2b2a3b2`
- **Job:** `JobNames.ANALYSIS` (`job-futurehouse-data-analysis-crow-high`)
- **Submitted:** 2026-05-06 03:24 UTC
- **Inputs (6 attachments uploaded via `client.upload_file(...)`):**
  - `01-snippet-schema.md` — `nsf-resources-text/snippets/README.md`
  - `02-mock-reviewer-playbook.md` — `nsf-resources-text/MOCK_REVIEWER_PLAYBOOK.md`
  - `03-corpus-summary.json` — `nsf-resources-text/snippets/summary.json`
  - `04-context7-sample.md` — first 200 lines of `nsf-resources-text/snippets/snippets.context7.md`
  - `05-snippets-sample.jsonl` — 3 example records from `nsf-resources-text/snippets/snippets.jsonl`
  - `06-tokenize_corpus.py` — the generator script
- **Submit script:** `/tmp/edison-fb/submit.py` (gated under `__main__`,
  idempotent via `task_id.txt` per repo memory)

## Prompt

Six-section opinionated critique requested (see `/tmp/edison-fb/00-PROMPT.md`):

1. Snippet granularity & chunking (≤1,200-token outline-anchored vs.
   semantic / late-chunking / propositional alternatives).
2. Schema completeness (deontic structure, cross-references, glossary,
   embedding vector field, parent/child links).
3. Requirement-strength labels (regex modal-verb robustness vs. RFC 2119
   / ISO/IEC Directives Part 2 / legal informatics deontic frames).
4. Serving model (file artefacts vs. MCP server vs. ColBERT/ColPali
   retriever vs. just preload-into-200k-context).
5. Evaluation (how to build an eval harness; suggest 5–10 hand-labelable
   items; analogues from LegalBench, ContractNLI, FinanceBench).
6. Three highest-ROI changes for tomorrow.

Self-critique included: regex strength labeller misses scope-limited
modals (verified by the dogfood example below — Finding 3 in
`nsf-resources-text/examples/review-output.md` required a hedge);
cross-references like "see Chapter IV.B" are not resolved; no eval set
exists.

## Status

**Completed 2026-05-06 03:45 UTC** (~21 min wall-clock from submission).
Full critique in [`result.md`](result.md).

### Top critiques flagged (and what we did about them in `1764da0` / `<this commit>`)

1. **"GWSW chapters are 1-snippet blobs."** Confirmed: the original
   markdown-heading parser only matched on `#`-prefixed lines, so GWSW
   workbook chapters (which use ALL-CAPS section headers like
   `PROPOSAL PREPARATION CHECKLIST`) yielded one snippet each.
   **Fix shipped:** added `ALLCAPS_HEADING` detection in
   `tokenize_corpus.py`. GWSW shards now have 2-5 snippets each
   (e.g. `nsf/Pre-SubmissionReviewNSF2021` went from 1 snippet to 3,
   correctly splitting *Proposal Preparation Checklist* and
   *Pre-Submission Review* sections).
2. **"Counts in `01-snippet-schema.md` (498 / 87 / 142 / 181 / 297) sum
   to 1,205 but `summary.json` shows 619."** Real bug — the README
   counts were carried over from a build that double-counted
   `pappg-24-1.md` against its per-chapter shards. **Fix shipped:**
   updated counts in `nsf-resources-text/snippets/README.md` to match
   the de-duplicated build (now 682 / 40 docs / ~210k tokens after the
   GWSW fix above).

### Top critiques deferred (with rationale)

3. **"Strip the regex labeller; use an LLM (gpt-4o-mini / Claude
   Haiku) to extract RFC 2119 modality + actor + condition."**
   Agreed in principle — would resolve the scope-limited-modal failure
   mode the dogfood example surfaced (Finding 3 in
   `nsf-resources-text/examples/review-output.md`). Deferred because
   it changes the dependency footprint (currently stdlib-only).
4. **"Implement an MCP server with hybrid BM25 + dense embeddings."**
   Agreed; called out as the v2 north star in
   `nsf-resources-text/snippets/README.md`. Deferred — out of scope
   for the snippet-store PR.
5. **"Add `effective_date` / `version` / `applies_to_condition` /
   `xrefs` fields."** Good idea; partially addressed today by the
   `source_url` field (which pins to the canonical 24-1 URL), but
   structured cross-references and conditional applicability remain
   future work.

### Edison sample eval items

The critique includes 5 hand-labelable eval items in the format
`Input -> Expected Citation -> Expected Verdict`. These are now the
seed for a future `examples/eval.jsonl` — see
`nsf-resources-text/examples/README.md` "What this demonstrates" for
how the dogfood example follows the same pattern.

## Result

See [`result.md`](result.md).

## See also

- `nsf-resources-text/examples/` — the dogfood worked example produced
  in parallel with this submission (synthetic broken NSF Project Summary
  reviewed against `pappg-24-1#II.D.2.b`, `II.C.1`, `II.D.2.d.(ii)`;
  6.5 / 7 defects caught with citations).
- `edison-trajectories/llm-doc-tokenization/` — the earlier
  `LITERATURE_HIGH` task on tokenization of long requirements documents
  in general (still pending; longer time horizon).
