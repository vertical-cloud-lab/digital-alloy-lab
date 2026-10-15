# Tokenizing long requirements docs for LLMs — Edison literature query

High-effort Edison literature task spawned from PR review feedback on
[#11](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/11)
(comment 4384777152): *"send an Edison query asking about tokenization of
long requirements documents like this and how to best leverage LLMs for this.
I'm picturing similar to context7, but not necessarily for code packages."*

Companion to `../nsf-grant-best-practices/` (which tokenized the corpus); this
task surveys the **methodology** behind that pipeline so the lab can iterate
on it (and apply it to other long-form corpora — DOE FOAs, ASTM specs,
contracts, etc.).

## Task

| Field | Value |
| --- | --- |
| Job | `LITERATURE_HIGH` (`job-futurehouse-paperqa3-high`) |
| Task ID | `fc3988c8-1676-4bd6-9321-d75b1062cd70` |
| Submitted | 2026-05-06 |
| Submitter | copilot coding agent (PR #11 review feedback) |

## Prompt (eight themes)

> Provide a comprehensive, citation-rich literature review on best practices
> for tokenizing, chunking, indexing, and serving long, structured
> *requirements / policy / regulatory / standards* documents (examples: NSF
> PAPPG, NIH grants policy, DOE FOAs, FDA guidances, ISO/IEEE standards,
> ASTM specifications, building codes, legal statutes, RFCs, vendor
> compliance manuals) so that downstream large-language-model (LLM) workflows
> — proposal drafting, compliance checking, mock review, contract redlining,
> audit support — can consume them with minimal hallucination and maximal
> traceability. The user is explicitly inspired by services like Context7
> (https://context7.com), llms.txt (https://llmstxt.org), and the broader
> *docs-as-tools-for-LLMs* movement — but applied to *non-code* corpora
> (regulations, grant guides, scientific standards). Cover:
>
> 1. **Extraction pipelines** — PDF/HTML/DOCX → structured-markdown (pymupdf,
>    pdfplumber, marker, unstructured.io, Docling, Nougat, GROBID, Azure
>    Document Intelligence) on multi-column layouts, tables, footnotes,
>    section numbering.
> 2. **Chunking strategies** — fixed-size vs. recursive vs. semantic vs.
>    structure-aware (heading/section-anchored); empirical comparisons
>    (LangChain, LlamaIndex, Anthropic *contextual retrieval*,
>    late-chunking, ColBERT/ColPali).
> 3. **Token-budgeting and context-window engineering** — long-context models
>    (Claude 200k–1M, Gemini 2M, GPT-4.1) vs. RAG vs. tool calls vs. agentic
>    file-by-file iteration; cost/latency tradeoffs.
> 4. **Citation/traceability mechanisms** — page numbers, section anchors,
>    span offsets, hash-based content addressing, structured frontmatter; how
>    to make the LLM cite exact provisions reliably.
> 5. **`llms.txt` and "LLM-friendly docs" conventions** — what they specify,
>    who has adopted them (Anthropic, Vercel, Cloudflare, Stripe, Supabase),
>    what's missing, how the pattern extends to regulatory corpora.
> 6. **Context7 and similar code-doc tokenizers / MCP servers** (DeepWiki,
>    GitMCP, Cursor docs, Cline, Continue) — how they index, rank, and serve
>    docs; whether their approach generalizes to PDFs and policy docs.
> 7. **Empirical evaluations of LLM compliance/review on long policy
>    documents** — hallucination rates, evaluation harnesses (LegalBench,
>    ContractNLI, RAFT, FinanceBench, MTEB long-doc subsets, regulation-QA
>    benchmarks).
> 8. **Concrete recommended pipeline** for a private lab repo whose corpus is
>    ~200k–500k tokens of NSF/DOE/NIH policy + grant-writing guidance —
>    extraction tool, chunking strategy, frontmatter schema, retrieval setup
>    (BM25 vs. dense vs. hybrid; ColBERT/ColPali; reranker), serving layer
>    (raw markdown in git vs. MCP server vs. RAG endpoint), evaluation rubric.

For each theme: canonical sources, consensus best practices, most-cited
disagreements, concrete actionable rules. Full bibliographic detail + URLs.
Call out 2025–2026 advances (long-context RAG, ColPali/ColBERT-v2, contextual
retrieval, agentic chunking).

## Why this matters for this repo

The current pipeline (committed in this PR) uses pymupdf → markdown with
YAML frontmatter (`source_pdf`, `pages`, `chars`, `est_tokens`) and HTML page
markers, then a chapter-level split for the largest source (PAPPG 24-1). That
is a reasonable v1 but is essentially **structure-naïve chunking** + **raw
file serving**. The Edison synthesis is intended to inform v2 decisions:

* whether to swap pymupdf for Docling / marker / Nougat (better tables and
  reading order);
* whether to add semantic / late-chunking on top of the chapter split;
* whether to publish an `llms.txt` at the repo root pointing at
  `nsf-resources-text/INDEX.md` and `_manifest.json`;
* whether to stand up a small MCP server (Context7-style) over the corpus so
  Copilot/Claude can retrieve specific PAPPG sections on demand instead of
  always loading the full chapter; and
* what eval harness to use to measure whether the mock-reviewer playbook in
  `../../nsf-resources-text/MOCK_REVIEWER_PLAYBOOK.md` actually reduces
  hallucinated PAPPG citations.

## Retrieval

```python
from edison_client import EdisonClient
import os
c = EdisonClient(api_key=os.environ["EDISON_API_KEY"])
r = c.get_task(task_id="fc3988c8-1676-4bd6-9321-d75b1062cd70")
```

Plan ≥30 min before first poll (LITERATURE_HIGH typically 25–40+ min). Save
the synthesis to `result.md` here. Do not commit the raw JSON
(`edison-trajectories/*.json` is gitignored).

## Status

**Completed 2026-05-06 03:45 UTC.** Full result in
[`result.md`](result.md) (~26k chars). Theme-level synthesis below.

### Theme-level synthesis

1. **PDF→markdown extraction.** Docling (IBM, MIT) is the recommended
   primary tool for regulatory PDFs (best section/table recovery);
   pymupdf is fine for born-digital single-column docs (what we use);
   Nougat for math-heavy scientific appendices.
2. **Chunking.** *Structure-aware* chunking (the approach we use) wins
   on retrieval quality and cost vs. fixed-size, recursive, or purely
   semantic chunking; semantic chunking is "structurally blind" and
   worst on highly structured technical documents.
3. **Long-context vs. RAG vs. agentic.** "Lost in the middle"
   degradation makes pure 200k-context preload risky for
   compliance-checklist tasks; hybrid retrieval recommended.
4. **Citation/traceability.** Supports our snippet-id-with-page-deeplink
   approach.
5. **`llms.txt`.** Convention validated; ours follows the
   llmstxt.org structure.
6. **Context7 / DeepWiki / GitMCP.** Generalises to policy docs only
   if you add explicit deontic structure (modality / actor /
   condition); otherwise the snippets behave like documentation stubs
   rather than rules.
7. **Eval harnesses.** LegalBench, ContractNLI, FinanceBench validate
   the "regulatory compliance with citation" pattern but no
   NSF-specific harness exists yet.
8. **v2 pipeline recommendation.** Docling extraction → propositional
   chunking → LLM-assisted RFC 2119 extraction → BM25 + dense hybrid
   retrieval served via MCP.
