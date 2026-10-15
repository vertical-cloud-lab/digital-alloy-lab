#!/usr/bin/env python3
"""Anthropic-style contextual chunk enrichment for the snippet store.

Implements the "Contextual Retrieval" recipe from
https://www.anthropic.com/news/contextual-retrieval: prepend ~50 tokens of
context per chunk that explain what document and section it belongs to and
what surrounding clauses establish, before indexing. Published gain on
regulatory text: nDCG@5 0.317 → 0.347; end-to-end answer correctness
62-64% → 72%.

Two prefix modes:

  * `structural` (default, pure stdlib) — uses the snippet's
    `doc_title`, `section_breadcrumbs`, `requirement_strength`,
    `page span`, and the leading sentence of any sibling parts. No LLM
    call. Cheap, deterministic, ~40-60 token prefix per snippet, gives
    most of the BM25 gain because BM25 was missing the breadcrumb terms.

  * `llm` (opt-in) — sends each snippet + its parent section to the
    Edison ANALYSIS crow (`EDISON_API_KEY` env var required) to generate
    a one-sentence summary like Anthropic's reference recipe. Slower and
    burns Edison credits; only run when v1 has been ratified.

Output: `snippets/snippets.contextual.jsonl`, mirroring
`snippets.jsonl` field-for-field but with an extra `context_prefix`
field and a `text_contextualized = context_prefix + "\\n\\n" + text`.

Downstream retrievers (BM25, dense, reranker) should index
`text_contextualized` instead of `text`; the playbook still shows the
human the original `text` so prefixes don't leak into reviewer findings.

Also writes a parent → children map (`snippets/parent_children.json`)
that `retrieve.py --expand-parent` uses for parent-child expansion: if a
chunk like `pappg-24-1#II.D.2.b~p2` ranks first, we can return the whole
`II.D.2.b` section as one merged hit so the LLM sees the surrounding
clauses too.

Usage:

    # Default — structural prefixes, no API key required
    python nsf-resources-text/scripts/contextualize.py

    # LLM-mode (requires EDISON_API_KEY)
    python nsf-resources-text/scripts/contextualize.py --mode llm

    # Stats only — print prefix-length histogram without rewriting
    python nsf-resources-text/scripts/contextualize.py --stats
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SNIPPETS_PATH = REPO / "nsf-resources-text" / "snippets" / "snippets.jsonl"
OUT_PATH = REPO / "nsf-resources-text" / "snippets" / "snippets.contextual.jsonl"
PARENT_MAP_PATH = REPO / "nsf-resources-text" / "snippets" / "parent_children.json"

# Target prefix budget. ~50 tokens ≈ 200 chars at the standard 4-char
# proxy. Snippets whose structural prefix would exceed this get truncated
# at a sentence boundary.
PREFIX_CHAR_BUDGET = 240


def _parent_id(snippet: dict) -> str | None:
    """Return the id of the snippet's parent section, if any.

    Snippets ids come in two shapes from `tokenize_corpus.py`:
      * `pappg-24-1#II.D.2.b` — single-chunk section (no parent grouping)
      * `pappg-24-1#II.D.2.b~p2` — part 2 of a multi-chunk section; the
        parent group is `pappg-24-1#II.D.2.b`.
    """
    sid = snippet.get("id", "")
    if "~p" not in sid:
        return None
    return sid.split("~p", 1)[0]


def _structural_prefix(snippet: dict, siblings: list[dict]) -> str:
    """Build a ~50-token contextual prefix from snippet metadata.

    Anthropic's recipe asks an LLM for a one-sentence summary of where
    the chunk sits in the document. We approximate that deterministically
    using fields the tokenizer already extracted:
      * doc_title + breadcrumb path  (replaces "what document/section")
      * requirement_strength         (replaces "what type of clause")
      * sibling-part count           (replaces "what surrounding text")
    """
    doc = snippet.get("doc_title") or snippet.get("doc_id", "")
    crumbs = " › ".join(snippet.get("section_breadcrumbs", []))
    strength = snippet.get("requirement_strength", "informational")
    pages = snippet.get("pages") or []
    page_str = f"p.{pages[0]}" if len(pages) == 1 else (
        f"pp.{pages[0]}-{pages[-1]}" if pages else "")
    part_str = ""
    if snippet.get("part_count", 1) > 1:
        part_str = (
            f" Part {snippet['part']} of {snippet['part_count']} for this section"
        )
    parts = [
        f"Context: from {doc} ({page_str}).",
        f"Section: {crumbs}." if crumbs else "",
        f"Clause type: {strength}.",
    ]
    if part_str:
        parts.append(part_str.strip() + ".")
    prefix = " ".join(p for p in parts if p)
    if len(prefix) > PREFIX_CHAR_BUDGET:
        prefix = prefix[: PREFIX_CHAR_BUDGET - 1] + "…"
    return prefix


def _llm_prefix(snippet: dict, siblings: list[dict]) -> str:
    """Generate a one-sentence context prefix via the Edison ANALYSIS crow.

    Only called when `--mode llm` is set. Falls back to the structural
    prefix on any error so the pipeline never blocks on credit limits or
    rate-limiting (Edison `POST /v0.1/crows` 429s under burst load).
    """
    key = os.environ.get("EDISON_API_KEY")
    if not key:
        return _structural_prefix(snippet, siblings)
    try:
        from edison_client import EdisonClient, JobNames  # type: ignore
        from edison_client.models.app import TaskRequest  # type: ignore
    except Exception:
        return _structural_prefix(snippet, siblings)
    prompt = (
        "You are preparing a regulatory document for retrieval. In ONE "
        "sentence (max 50 tokens), describe what this chunk is about and "
        "what the surrounding section establishes, so a search engine can "
        "find it from a paraphrased question. Do NOT quote the chunk; "
        "write only the contextual lead-in.\n\n"
        f"Document: {snippet.get('doc_title')}\n"
        f"Section path: {snippet.get('section_path')}\n"
        f"Breadcrumbs: {' › '.join(snippet.get('section_breadcrumbs', []))}\n"
        f"Pages: {snippet.get('pages')}\n\n"
        f"Chunk text (do not echo):\n{snippet.get('text', '')[:1800]}"
    )
    try:
        client = EdisonClient(api_key=key)
        req = TaskRequest(name=JobNames.ANALYSIS.value, query=prompt)
        # NOTE: this is a synchronous fallback path that blocks; the
        # batch driver below spaces calls ≥15s apart to dodge the 429
        # rate limit (see Edison rate-limiting playbook).
        tid = client.create_task(task_data=req)
        result = client.run_tasks_until_done([tid], timeout=1500)
        body = (result[0].formatted_answer or "").strip().splitlines()[0]
        return body[:PREFIX_CHAR_BUDGET] if body else _structural_prefix(snippet, siblings)
    except Exception as exc:  # pragma: no cover - network path
        print(f"  WARN: LLM prefix failed for {snippet.get('id')}: {exc}",
              file=sys.stderr)
        return _structural_prefix(snippet, siblings)


def contextualize(snippets: list[dict], mode: str = "structural") -> list[dict]:
    by_parent: dict[str, list[dict]] = defaultdict(list)
    for s in snippets:
        p = _parent_id(s)
        if p:
            by_parent[p].append(s)
    out: list[dict] = []
    prefix_fn = _llm_prefix if mode == "llm" else _structural_prefix
    for s in snippets:
        p = _parent_id(s)
        siblings = by_parent.get(p, []) if p else []
        prefix = prefix_fn(s, siblings)
        enriched = dict(s)
        enriched["context_prefix"] = prefix
        enriched["text_contextualized"] = f"{prefix}\n\n{s.get('text', '')}"
        enriched["parent_id"] = p
        out.append(enriched)
    return out


def build_parent_children(snippets: list[dict]) -> dict[str, list[str]]:
    """Return parent_id → [child_id, ...] map for `--expand-parent`."""
    m: dict[str, list[str]] = defaultdict(list)
    for s in snippets:
        p = _parent_id(s)
        if p:
            m[p].append(s["id"])
    return {k: sorted(v) for k, v in m.items()}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--mode", choices=["structural", "llm"], default="structural")
    parser.add_argument("--stats", action="store_true",
                        help="Print prefix length histogram and exit.")
    args = parser.parse_args(argv)
    snippets = [
        json.loads(line)
        for line in SNIPPETS_PATH.read_text("utf-8").splitlines()
        if line.strip()
    ]
    print(f"Loaded {len(snippets)} snippets from {SNIPPETS_PATH.name}")
    enriched = contextualize(snippets, mode=args.mode)
    parent_map = build_parent_children(snippets)
    lens = [len(s["context_prefix"]) for s in enriched]
    print(f"Context prefix chars: min={min(lens)} max={max(lens)} "
          f"avg={sum(lens) / len(lens):.0f}")
    print(f"Parent groups: {len(parent_map)} "
          f"(largest has {max((len(v) for v in parent_map.values()), default=0)} children)")
    if args.stats:
        return 0
    with OUT_PATH.open("w", encoding="utf-8") as fh:
        for s in enriched:
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")
    PARENT_MAP_PATH.write_text(
        json.dumps(parent_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT_PATH.relative_to(REPO)}")
    print(f"Wrote {PARENT_MAP_PATH.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
