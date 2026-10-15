# Reusable Agent Prompt — “Regulatory-Corpus Mock-Reviewer Framework”

> Drop this whole file into a new repository's `prompts/` directory (or paste
> it into the issue body) and assign it to a capable coding agent (Copilot
> Workspace, Claude Code, Cursor, Aider, etc.). The agent should treat it as
> the project brief and produce a self-contained, dogfooded toolkit for
> compliance-checking any long-form draft against a stack of regulatory or
> policy PDFs.
>
> Originally distilled from
> [`vertical-cloud-lab/digital-alloy-lab-private` PR #11](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/11),
> which built it for NSF PAPPG 24-1 + Gold-Standard-Science + GWSW grant-writing
> material and then re-used it on the
> [vertical-cloud-lab EAGER concept outline (PR #10)](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/10).

---

## 1. Goal

Build a small, **pure-stdlib-by-default** toolkit that lets an LLM (or a human
reviewer) answer the question *"does this draft comply with §X of <regulator>'s
policy?"* with citations down to the section and PDF page, **without** dumping
the whole corpus into the prompt window.

Three deliverables, in this order:

1. A **tokenized snippet store** — every section of every PDF chunked into ≤
   ~1,200 token records with stable ids, breadcrumbs, page-deep-link URLs,
   and a `requirement_strength` label (`prohibited` / `required` /
   `recommended` / `permitted` / `informational`).
2. A **retrieval CLI + library** the agent (or a human) can call to surface
   the 3–5 governing snippets for any free-text question, with optional
   filters by document and requirement strength.
3. A **mock-reviewer playbook + worked example** — a Markdown prompt that
   tells an LLM how to use (1) and (2) to produce reviewer-style findings on
   a given draft, plus one fully-worked end-to-end example committed to the
   repo.

A small **evaluation harness** (≥15 hand-labelled query → snippet-id pairs,
Recall@5 / MRR / Hit@1) is required so the retrieval quality is a measurable
number, not a vibe.

---

## 2. Inspirations and prior art (read these first)

The agent **must** fetch and skim at least these before designing the
schema, because the conventions below are intentionally aligned with them:

- **Context7** — code-doc tokenization with `TITLE / DESCRIPTION / SOURCE /
  TEXT` blocks: <https://context7.com> and the
  [context7-mcp server](https://github.com/upstash/context7).
- **`llms.txt` spec** — root-level pointer file: <https://llmstxt.org>.
- **Anthropic *Contextual Retrieval*** — prepend ~50 tokens of LLM-generated
  context to every chunk, giving a ~35–67% reduction in retrieval failures:
  <https://www.anthropic.com/news/contextual-retrieval>.
- **BM25 (Okapi)** — Robertson & Zaragoza, *The Probabilistic Relevance
  Framework: BM25 and Beyond*:
  <https://www.staff.city.ac.uk/~sb317/papers/foundations_bm25_review.pdf>.
- **BGE-M3** — dense + sparse + multi-vector embedding model:
  <https://github.com/FlagOpen/FlagEmbedding/tree/master/research/BGE_M3>
  (paper: <https://arxiv.org/abs/2402.03216>).
- **bge-reranker-v2-m3** — cross-encoder reranker:
  <https://huggingface.co/BAAI/bge-reranker-v2-m3>.
- **NV-Embed-v2** — alternative SOTA dense embedder (MTEB leader, May 2024):
  <https://huggingface.co/nvidia/NV-Embed-v2>.
- **RAGChecker** — claim-level retrieval/generation faithfulness:
  <https://github.com/amazon-science/RAGChecker>.
- **ARES** — automated RAG evaluation with PPI confidence intervals:
  <https://github.com/stanford-futuredata/ARES>.
- **DeepEval** — pytest-style LLM eval suite incl. faithfulness, contextual
  precision/recall: <https://github.com/confident-ai/deepeval>.
- **Model Context Protocol** — for the optional Phase 2 MCP server:
  <https://modelcontextprotocol.io>.

Optional but valuable comparators:

- **Docling** (IBM) for higher-fidelity PDF→Markdown:
  <https://github.com/DS4SD/docling>.
- **DeepWiki** and **GitMCP** as related “tokenize-and-serve” systems.
- **LegalBench** / **ContractNLI** / **FinanceBench** for off-the-shelf
  regulatory-text retrieval benchmarks worth replicating the methodology of.

---

## 3. Input the user must hand the agent

When invoking, the user provides:

- A *target regulator* and one or more **source PDFs** (or URLs) — e.g.
  `NSF PAPPG 24-1`, `21 CFR Part 11`, `FAR Part 31`, `MITRE ATT&CK`,
  `ASTM E3166`. PDFs go in a sibling directory, e.g. `<regulator>-resources/`.
- A *draft document* to be reviewed (a `.tex`, `.md`, `.txt`, or `.pdf`).
- Optional: a *project context* paragraph (what the project does, why it
  needs the review). This unblocks domain-specific reviewer findings.

If none of these are provided, the agent stops and asks for them rather
than fabricating a corpus.

---

## 4. Required deliverables

The agent should produce **all** of the following in a single PR, in the
order listed, with each step **committed and dogfooded** before moving on.

### 4.1 PDF → text extraction

- Use `pymupdf` (a.k.a. `fitz`) as the default extractor — pure-Python,
  no system deps, layout-preserving enough for policy PDFs.
- Emit one `.md` per PDF into `<regulator>-resources-text/`. Mark page
  boundaries with `<!-- page N -->` HTML comments so downstream chunking
  can recover page spans.
- If reviewers later complain about table/figure handling, swap to
  **Docling** behind the same script interface.

### 4.2 Structure-aware tokenizer

Write `scripts/tokenize_corpus.py` that:

- Parses the document's outline grammar (for NSF/legal text that is usually
  `Chapter II → A. → 1. → a. → (i)`; for FR notices it's heading-rule based).
- Detects ALL-CAPS headings, numbered headings, and Markdown `#`/`##`
  headings; falls back to top-level chunking if no structure is present.
- Splits into ≤ ~1,200-token chunks (use `tiktoken` if available, else
  `len(text)/4` as the conservative est-token proxy).
- **Detects requirement strength** with a modal-verb regex per chunk and
  records every matched phrase as evidence:
  - `prohibited` — `must not`, `may not`, `shall not`, `prohibited`.
  - `required` — `must`, `shall`, `required`, `mandatory`, `is required`.
  - `recommended` — `should`, `recommended`, `expected to`.
  - `permitted` — `may`, `can`, `is permitted`, `optional`.
  - `informational` — none of the above.

Emit a record per chunk with **at least** these fields (the v2 schema):

```json
{
  "id": "pappg-24-1#II.D.2.b",
  "doc_id": "pappg-24-1",
  "doc_title": "PAPPG 24-1 (NSF 24-1)",
  "section_path": "II.D.2.b",
  "section_breadcrumbs": ["Chapter II", "D. Proposal Contents", ...],
  "title": "b. Project Summary",
  "text": "Each proposal must contain ...",
  "pages": [49],
  "source_pdf": "<regulator>-resources/<doc>.pdf",
  "source_url": "https://.../doc.pdf#page=49",
  "requirement_strength": "required",
  "requirement_phrases": ["must", "should"],
  "char_count": 985,
  "est_tokens": 246,
  "source_label": "[NSF PAPPG 24-1 §II.D.2.b, p.49]",
  "version": "NSF 24-1",
  "effective_date": "2024-05-20",
  "chunk_hash": "sha256:d431b2729c31aab6",
  "cross_references": []
}
```

Outputs:

- `snippets/snippets.jsonl` — canonical store
- `snippets/snippets.context7.md` — same records as Context7-style blocks
  (`TITLE / DOCUMENT / SECTION_PATH / BREADCRUMBS / REQUIREMENT_STRENGTH
  / PAGES / SOURCE_PDF / SOURCE_URL / TEXT`)
- `snippets/by-doc/<doc>.jsonl` — per-document shards (LLM can request only
  what it needs)
- `snippets/index.md` + `snippets/summary.json` — counts by doc and strength
- A root `llms.txt` per <https://llmstxt.org> pointing at all of the above

### 4.3 Retrieval CLI + library

`scripts/retrieve.py` — pure-stdlib Okapi BM25 (k1=1.5, b=0.75) over the
`snippets.jsonl` store. Required behaviour:

- `python scripts/retrieve.py "query string"` — top-k citation-formatted hits
- `--doc pappg-24-1`, `--strength required` filters
- `--show-text` to preview snippet body
- `--json` for machine output
- Importable as a library: `from retrieve import RetrievalIndex`
- **No dependencies beyond the stdlib** (rank_bm25, sklearn, torch all
  forbidden in the default path — they go in `retrieve_hybrid.py` instead)
- The keep-list is intentional: regulatory text relies on terms like
  *must*, *shall*, *section* that look like stopwords but carry meaning;
  keep the stoplist to ~30 truly content-free function words.

### 4.4 Eval harness

`scripts/run_eval.py` against `eval/eval_set.jsonl`. v1 = ≥ 15 hand-labelled
`{query, expected_id, also_acceptable?, tag}` items spanning ≥ 10 distinct
compliance topics (page limits, formatting, biosketch, merit review, etc.).
Reports Recall@k, MRR, Hit@1, and a **per-tag Recall** breakdown so you can
see which compliance topics retrieve poorly. v2 target = 50–100 stratified
items with adversarial/refusal cases (see §6 below).

### 4.5 Mock-reviewer playbook

`MOCK_REVIEWER_PLAYBOOK.md` — the LLM prompt itself. Structure:

1. **Role** — *"You are a panel reviewer for `<regulator>`."*
2. **Inputs** — link to the snippet store, the draft, the project context.
3. **Procedure** — for each section of the draft, retrieve the 3–5
   governing snippets via `retrieve.py`, then check the draft against the
   `prohibited` / `required` / `recommended` clauses one at a time.
4. **Output format** — `Major / Minor / Nit` findings, each with: the
   exact rule violated (with `[Regulator §X, p.N]` citation), the offending
   line/quote from the draft, and a concrete suggested fix.
5. **Refusal rule** — *"If no governing snippet is retrieved at confidence
   > threshold, output `INSUFFICIENT EVIDENCE — would need: <what>` rather
   than guessing."* Critical to prevent hallucinated rule citations.

### 4.6 Two worked examples (dogfooding)

Commit at least **two** `examples/*.md` walkthroughs that run the framework
against real draft material — one on a deliberately-broken seed draft to
prove the framework catches violations, one on a real in-flight document
(an actual concept outline, abstract, or section). The second example
proves the framework generalizes across document types without code changes.

Each example file includes: the input draft, the 3 retrieval queries used,
the retrieval output, and the resulting Major / Minor / Nit findings.

### 4.7 External self-evaluation

After the worked example, submit it to an *independent* LLM for critique —
in this repo we used [Edison Scientific](https://edisonscientific.gitbook.io/edison-cookbook/edison-client)
(`JobNames.ANALYSIS` for figure/typography-aware critique, then
`JobNames.LITERATURE_HIGH` for a citation-grounded improvement roadmap).
Commit the prompt + result under `edison-trajectories/<eval-name>/`.
This is what catches false positives (your tool flagged something benign),
false negatives (your tool missed real violations), and "the dogfooding
loop silently reverted the prior fix" failure modes — none of which the
framework can self-diagnose.

---

## 5. v2 improvements (do these once v1 is dogfooded)

In priority order (these are the same three the Edison literature pass
recommended, with citations):

### 5.1 Hybrid retrieval + cross-encoder reranker (3–7 days)

- **BM25** (you already have) +
- **BGE-M3** dense (or NV-Embed-v2) via
  [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) or
  [sentence-transformers](https://www.sbert.net/) +
- **bge-reranker-v2-m3** cross-encoder rerank on the union top-50.
- Combine with **Reciprocal Rank Fusion** (k=60): see
  <https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf>.
- Published gain on regulatory corpora: +0.07 Recall@10, +0.08 MAP@10,
  +30–45 % nDCG@10 from the reranker alone.
- Keep the same `RetrievalIndex` interface so the playbook and CLI don't
  change. Put it in `retrieve_hybrid.py` so the stdlib `retrieve.py` keeps
  working in CI.

### 5.2 Anthropic-style contextual chunks + parent-child expansion (2–5 days)

- For each chunk, prepend ~50 tokens of LLM-generated context that says
  what document and section the chunk belongs to and what the surrounding
  paragraph claims (Anthropic recipe:
  <https://www.anthropic.com/news/contextual-retrieval>).
- Optionally also store the parent section's id and **expand** on retrieval
  — if a `partN` child snippet hits, return the full parent section in the
  context instead of just the child. Useful when chunks split mid-clause.
- Reported gains: nDCG@5 0.317 → 0.347 on regulatory text, end-to-end
  answer correctness 62–64 % → 72 %.

### 5.3 Real eval harness (5–10 days)

- Grow `eval_set.jsonl` from 15 → 50–100 items, stratified by `requirement_strength`
  and by `doc_id`. Use an LLM to draft candidate queries from each snippet,
  then human-review every accepted item.
- Add **adversarial / refusal cases** — queries about facts that are *not*
  in the corpus (e.g., a CFR section the regulator doesn't enforce); the
  expected answer is `REFUSE` and a passing system declines rather than
  retrieving something plausible-but-wrong.
- Add **claim-level faithfulness** scoring via
  [RAGChecker](https://github.com/amazon-science/RAGChecker),
  [ARES](https://github.com/stanford-futuredata/ARES), or a lightweight
  sentinel-phrase check (does the top-1 snippet contain the rule's
  controlling verb + noun?).

### 5.4 Optional Phase 2

- **MCP stdio server** wrapping `retrieve.py` so the snippet store shows up
  as a tool in Claude Desktop / Cursor (`modelcontextprotocol/servers`
  pattern: <https://github.com/modelcontextprotocol/servers>).
- **LLM-extracted deontic frames** to replace the modal-verb regex —
  classify each clause as `(actor, modality, action, condition)` so the
  reviewer can ask *"what must the PI do before X?"*.
- **Docling** extraction swap for tables and figures.

---

## 6. Failure modes the agent must avoid

These were caught in the dogfooding pass — don't re-make them:

- **"Tokenized" = pymupdf-dumped Markdown**. No. Tokenized means
  Context7-style structured records with stable ids, breadcrumbs, page
  spans, deep-link source URLs, and a requirement-strength label. The
  Markdown dump is an *intermediate*, not a deliverable.
- **The dogfooding loop has no programmatic re-check.** If the framework
  flags a finding and the PI then "trims to 2 pages" and silently reverts
  the fix, the agent's previous PR comment claiming the fix is live is
  wrong. Either re-run the mock review on every commit to the draft (CI),
  or stop asserting fix-applied without a fresh retrieval pass.
- **Hallucinated unit-fit / cross-reference / preliminary-data claims.**
  The mock reviewer must cite a retrieved snippet for every finding, or
  output `INSUFFICIENT EVIDENCE`. Adding the refusal rule to the playbook
  is what prevents the *"CISE/IIS Robust Intelligence is the right
  tertiary unit"*-style fabrications.
- **Sample size of one.** A single worked example is anecdote. Ship at
  least two, on materially different document types (concept outline vs.
  full proposal vs. project summary), or any retrieval-quality claim is
  unsupported.
- **Mixing eval set provenance.** Don't let the LLM that generates the
  eval queries also be the LLM whose retrieval you're scoring; have a
  human accept every eval item before it counts.

---

## 7. Acceptance criteria for the agent's PR

- All seven deliverables in §4 exist and are committed.
- `python scripts/run_eval.py` reports numeric Recall@5, MRR, Hit@1.
- At least two `examples/*.md` walkthroughs, each citing real
  `retrieve.py` invocations (paste the commands and outputs).
- `MOCK_REVIEWER_PLAYBOOK.md` contains the refusal rule from §6.
- An `edison-trajectories/<name>/` (or equivalent) directory with the
  prompt + result of an external LLM critiquing the framework, including
  at least one false positive and one false negative the framework had
  not surfaced itself.
- A short `prompts/<this-prompt>.md` copy of *this* file in the new
  repository so the chain stays reusable.

---

## 8. References (machine-fetchable)

The agent should `web_fetch` (or equivalent) each of these and cite back
to them in the PR description:

```
https://context7.com
https://llmstxt.org
https://www.anthropic.com/news/contextual-retrieval
https://github.com/FlagOpen/FlagEmbedding/tree/master/research/BGE_M3
https://huggingface.co/BAAI/bge-reranker-v2-m3
https://huggingface.co/nvidia/NV-Embed-v2
https://arxiv.org/abs/2402.03216
https://www.staff.city.ac.uk/~sb317/papers/foundations_bm25_review.pdf
https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
https://github.com/amazon-science/RAGChecker
https://github.com/stanford-futuredata/ARES
https://github.com/confident-ai/deepeval
https://modelcontextprotocol.io
https://github.com/modelcontextprotocol/servers
https://github.com/DS4SD/docling
https://github.com/upstash/context7
https://edisonscientific.gitbook.io/edison-cookbook/edison-client
```
