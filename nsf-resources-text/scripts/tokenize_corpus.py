#!/usr/bin/env python3
"""Tokenize the NSF requirements corpus into Context7-style snippets.

Walks every markdown file under ``nsf-resources-text/`` and produces:

* ``snippets/snippets.jsonl`` — one JSON record per section/sub-section,
  with stable ``id``, breadcrumb ``section_path``, page span,
  ``requirement_strength`` (must/shall/should/may/informational) detected from
  the prose, source URL, char/token counts, and the section text.
* ``snippets/snippets.context7.md`` — the same chunks rendered in the
  Context7-style ``TITLE / DESCRIPTION / SOURCE / TEXT`` block format that
  many MCP doc-servers expose to LLMs.
* ``snippets/by-doc/<doc_id>.jsonl`` — per-document JSONL shards so an LLM
  can load only the document(s) it needs.
* ``snippets/index.md`` — human-readable index of all snippets with token
  counts, requirement strength, and a one-line title.
* ``llms.txt`` — root llmstxt.org-style index pointing at the snippet store
  and the largest source files.

Two grammars are supported:

1. **PAPPG-style outline** (single capital letter ``A.`` → arabic ``1.`` →
   lowercase ``a.`` → roman ``(i)`` markers each on their own line, with the
   section title on the following line). Used for ``pappg-24-1/*.md`` and
   ``pappg-24-1.md``.
2. **Markdown headings** (``# / ## / ### ...``). Used for everything else
   (GWSW workbook chapters, OSTP GSS guidance, GSS implementation plan,
   Federal Register notice).

Section text larger than ``MAX_CHUNK_TOKENS`` is split on paragraph
boundaries into ``part 1 / part N`` sub-snippets so each chunk fits in a
small RAG window. Page numbers are tracked from the
``<!-- page N -->`` markers emitted by the original pymupdf extraction.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import OrderedDict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "nsf-resources-text"
OUT = CORPUS / "snippets"
MANIFEST_PATH = CORPUS / "_manifest.json"

# Target chunk size. Sections larger than this are split on blank-line
# boundaries; sections smaller than the minimum are merged into the next one
# at the same heading level when possible.
MAX_CHUNK_TOKENS = 1200
MIN_CHUNK_TOKENS = 60
TOKENS_PER_CHAR = 1 / 4  # OpenAI heuristic, also used by the original manifest

# Source-of-record URLs (recorded in nsf-resources/SOURCES.md). We mirror the
# canonical retrieval URL into each snippet so the LLM can cite a stable
# location even when the user only loads the markdown.
SOURCE_URLS = {
    "pappg-24-1": "https://www.nsf.gov/pubs/policydocs/pappg24_1/pappg_full.pdf",
    "federal-register-2024-29244-gss":
        "https://www.federalregister.gov/documents/2024/12/13/2024-29244/"
        "guidance-for-implementing-the-gold-standard-of-science-in-the-conduct-of-scientific-research",
    "gold-standard-science-implementation-plan-2025":
        "https://www.whitehouse.gov/wp-content/uploads/2025/06/"
        "Gold-Standard-Science-Implementation-Plan.pdf",
    "ostp-gss-guidance-june-2025":
        "https://www.whitehouse.gov/wp-content/uploads/2025/06/OSTP-GSS-guidance.pdf",
}
GWSW_BASE = "https://www.grantcentral.com/workbooks/"

# Keywords used to label requirement strength. Order matters: stronger
# language wins (e.g. a paragraph that says both "must" and "may" is tagged
# "must"). "informational" is the default when no modal verb is present.
STRENGTH_PATTERNS: list[tuple[str, list[re.Pattern[str]]]] = [
    ("prohibited", [re.compile(r"\b(must not|shall not|may not|prohibited|will not be accepted|will be returned without review)\b", re.I)]),
    ("required",   [re.compile(r"\b(must|shall|is required|are required|required to)\b", re.I)]),
    ("recommended",[re.compile(r"\b(should|recommended|strongly recommended|expected to)\b", re.I)]),
    ("permitted",  [re.compile(r"\b(may|is permitted|are permitted|optional)\b", re.I)]),
]

# PAPPG outline markers, in nesting order.
OUTLINE_LEVELS = [
    # level name, regex matching the marker line, formatter for breadcrumb
    ("L1", re.compile(r"^([A-Z])\.\s*$"),         lambda m: m.group(1)),
    ("L2", re.compile(r"^(\d{1,2})\.\s*$"),       lambda m: m.group(1)),
    ("L3", re.compile(r"^([a-z])\.\s*$"),         lambda m: m.group(1)),
    ("L4", re.compile(r"^\(([ivxlcdm]+)\)\s*$"),  lambda m: f"({m.group(1)})"),
]
PAGE_MARKER = re.compile(r"<!--\s*page\s+(\d+)\s*-->", re.I)
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)


@dataclass
class Snippet:
    id: str
    doc_id: str
    doc_title: str
    section_path: str
    section_breadcrumbs: list[str]
    title: str
    text: str
    pages: list[int]
    source_pdf: str
    source_url: str
    requirement_strength: str
    requirement_phrases: list[str]
    char_count: int
    est_tokens: int
    # --- v2 schema additions (Edison feedback `660a4e59` + literature §8) ---
    # Human-readable citation label, e.g. "[NSF PAPPG 24-1 §II.D.2.b, p.49]".
    # Use this verbatim when citing the snippet in an LLM response.
    source_label: str = ""
    # Document version / revision identifier (e.g. "NSF 24-1 (effective May
    # 20, 2024)"). Helps the reviewer flag stale rules.
    version: str = ""
    # ISO date the source document took effect, when known.
    effective_date: str = ""
    # SHA-256 of the snippet text, for cache-busting and change detection.
    chunk_hash: str = ""
    # Cross-references parsed from the body ("see Chapter II.D.2.b" → [
    # {"raw": "Chapter II.D.2.b", "id": "pappg-24-1#II.D.2.b"}]). Unresolved
    # references keep an empty `id` so a downstream linter can flag them.
    cross_references: list[dict[str, str]] = field(default_factory=list)
    part: int = 1
    part_count: int = 1
    tags: list[str] = field(default_factory=list)


# Document-level metadata for the new schema fields. Date is the
# effective date as published in the document itself.
DOC_VERSIONS: dict[str, dict[str, str]] = {
    "pappg-24-1": {
        "version": "NSF 24-1",
        "effective_date": "2024-05-20",
        "label": "NSF PAPPG 24-1",
    },
    "federal-register-2024-29244-gss": {
        "version": "FR 2024-29244",
        "effective_date": "2024-12-13",
        "label": "Federal Register 2024-29244 (Gold-Standard Science)",
    },
    "gold-standard-science-implementation-plan-2025": {
        "version": "OSTP GSS Implementation Plan, June 2025",
        "effective_date": "2025-06-01",
        "label": "OSTP GSS Implementation Plan (June 2025)",
    },
    "ostp-gss-guidance-june-2025": {
        "version": "OSTP GSS Guidance, June 2025",
        "effective_date": "2025-06-01",
        "label": "OSTP GSS Guidance (June 2025)",
    },
}


def doc_meta(doc_id: str) -> dict[str, str]:
    """Return version / effective_date / label for a doc_id."""
    if doc_id in DOC_VERSIONS:
        return DOC_VERSIONS[doc_id]
    if doc_id.startswith("grant-writers-seminars-workshops/"):
        return {
            "version": "GWSW Workbook (2021-2025 chapters)",
            "effective_date": "",
            "label": "GWSW " + doc_id.split("/", 1)[1],
        }
    return {"version": "", "effective_date": "", "label": doc_id}


# Cross-reference detector. Matches phrases like:
#   "see Chapter II.D.2.b"           → ("Chapter", "II.D.2.b")
#   "as described in §II.D.2.b"      → ("§",       "II.D.2.b")
#   "in Section II.C.1"              → ("Section", "II.C.1")
# Conservative: requires either an explicit "Chapter"/"Section"/"§" anchor
# *or* a roman-numeral chapter prefix on the path.
XREF_RE = re.compile(
    r"\b(Chapter|Section|§)\s+"
    r"((?:[IVX]+|\d+)(?:\.[A-Za-z0-9]+(?:\.\([ivx]+\))?)*)",
    re.IGNORECASE,
)


def parse_cross_references(text: str, snippet_ids: set[str]) -> list[dict[str, str]]:
    """Find "see Chapter X.Y.Z" patterns and resolve them against known ids.

    Currently only resolves PAPPG references (the only doc with a stable
    `Chapter` outline). Other documents return entries with an empty `id`.
    """
    refs: list[dict[str, str]] = []
    seen: set[str] = set()
    for m in XREF_RE.finditer(text):
        path = m.group(2)
        # Normalise: "ii.d.2.b" -> "II.D.2.b"; trailing "(ii)" stays
        # lowercase per snippet id convention.
        parts = path.split(".")
        norm: list[str] = []
        for p in parts:
            if re.fullmatch(r"[ivx]+", p):
                norm.append(f"({p})")
            elif re.fullmatch(r"[IVX]+", p):
                norm.append(p)
            elif re.fullmatch(r"[A-Za-z]", p):
                norm.append(p.upper())
            else:
                norm.append(p)
        canonical = ".".join(norm)
        candidate = f"pappg-24-1#{canonical}"
        raw = f"{m.group(1)} {path}"
        key = (raw, candidate)
        if key in seen:
            continue
        seen.add(key)
        resolved_id = candidate if candidate in snippet_ids else ""
        refs.append({"raw": raw, "id": resolved_id})
    return refs


def parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    m = FRONTMATTER.match(raw)
    if not m:
        return {}, raw
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, raw[m.end():]


def estimate_tokens(text: str) -> int:
    return max(1, int(round(len(text) * TOKENS_PER_CHAR)))


def detect_strength(text: str) -> tuple[str, list[str]]:
    """Return (strength, list_of_matched_phrases) for a section body."""
    found_phrases: list[str] = []
    found_label = "informational"
    for label, patterns in STRENGTH_PATTERNS:
        for pat in patterns:
            for m in pat.finditer(text):
                found_phrases.append(m.group(0).lower())
            if found_label == "informational" and pat.search(text):
                found_label = label
    # Deduplicate while preserving order.
    seen: OrderedDict[str, None] = OrderedDict()
    for p in found_phrases:
        seen.setdefault(p, None)
    return found_label, list(seen.keys())[:6]


def split_long(text: str, max_tokens: int) -> list[str]:
    """Split *text* on blank-line paragraph boundaries into chunks <= max_tokens."""
    if estimate_tokens(text) <= max_tokens:
        return [text]
    paragraphs = re.split(r"\n\s*\n", text.strip())
    chunks: list[str] = []
    cur: list[str] = []
    cur_tokens = 0
    for p in paragraphs:
        pt = estimate_tokens(p)
        if pt > max_tokens and not cur:
            # Single oversize paragraph: hard-split on sentences.
            sentences = re.split(r"(?<=[.?!])\s+", p)
            buf: list[str] = []
            buf_tok = 0
            for s in sentences:
                st = estimate_tokens(s)
                if buf_tok + st > max_tokens and buf:
                    chunks.append(" ".join(buf))
                    buf, buf_tok = [s], st
                else:
                    buf.append(s)
                    buf_tok += st
            if buf:
                chunks.append(" ".join(buf))
            continue
        if cur_tokens + pt > max_tokens and cur:
            chunks.append("\n\n".join(cur))
            cur, cur_tokens = [p], pt
        else:
            cur.append(p)
            cur_tokens += pt
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


# ---------------------------------------------------------------------------
# PAPPG outline parser
# ---------------------------------------------------------------------------

def parse_pappg_outline(body: str) -> list[tuple[list[str], list[str], str, list[int]]]:
    """Yield (path_parts, breadcrumb_titles, body_text, pages) per section."""
    lines = body.splitlines()
    sections: list[dict] = []
    current_path: list[str] = []
    current_titles: list[str] = []
    current_body: list[str] = []
    current_pages: set[int] = set()
    last_page = 0
    i = 0

    def flush() -> None:
        if current_titles:
            sections.append({
                "path": list(current_path),
                "titles": list(current_titles),
                "body": "\n".join(current_body).strip(),
                "pages": sorted(current_pages),
            })

    while i < len(lines):
        line = lines[i]
        # Track page boundaries.
        pm = PAGE_MARKER.search(line)
        if pm:
            last_page = int(pm.group(1))
            current_pages.add(last_page)
            i += 1
            continue
        # Try to match an outline marker on its own line.
        matched_level = None
        for idx, (lvl, pat, fmt) in enumerate(OUTLINE_LEVELS):
            m = pat.match(line.strip())
            if m:
                matched_level = (idx, fmt(m))
                break
        if matched_level is not None and i + 1 < len(lines):
            # The next non-blank line is the section title.
            title_line = ""
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                title_line = lines[j].strip()
            # Heuristic: only treat as a section if the title line is short
            # (not a sentence) and not itself an outline marker.
            is_title = (
                title_line
                and len(title_line) < 160
                and not any(p.match(title_line) for _, p, _ in OUTLINE_LEVELS)
                and not title_line.endswith(",")
            )
            if is_title:
                flush()
                idx, marker = matched_level
                current_path = current_path[:idx] + [marker]
                current_titles = current_titles[:idx] + [f"{marker}. {title_line}"]
                current_body = []
                current_pages = set()
                if last_page:
                    current_pages.add(last_page)
                i = j + 1
                continue
        # Otherwise accumulate body content.
        if current_titles:
            current_body.append(line)
        i += 1
    flush()
    return [(s["path"], s["titles"], s["body"], s["pages"]) for s in sections]


# ---------------------------------------------------------------------------
# Markdown heading parser (for non-PAPPG docs)
# ---------------------------------------------------------------------------

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
# GWSW workbook chapters use ALL-CAPS lines (e.g. "PROPOSAL PREPARATION
# CHECKLIST") instead of markdown headings. Match a line that is at least
# 4 chars, all uppercase letters/digits/spaces/punctuation, with at least
# one letter and no leading lowercase. Excludes single-word YELLs and lines
# ending in colon (which are usually inline labels, not section headers).
ALLCAPS_HEADING = re.compile(
    r"^(?=.*[A-Z])(?!.*[a-z])([A-Z0-9][A-Z0-9 ,'\-&/().:]{3,80})\s*$"
)


def parse_markdown_headings(body: str) -> list[tuple[list[str], list[str], str, list[int]]]:
    """Section the document on markdown headings. Returns the same shape as
    parse_pappg_outline so the rest of the pipeline is uniform."""
    lines = body.splitlines()
    sections: list[dict] = []
    stack: list[tuple[int, str]] = []  # (level, title)
    current_body: list[str] = []
    current_pages: set[int] = set()
    last_page = 0

    def make_path() -> list[str]:
        return [t for _, t in stack]

    def make_section_path() -> list[str]:
        # Use a dotted numeric-ish path keyed on heading levels seen so far.
        # We keep just the title slug here; the breadcrumb carries hierarchy.
        return [slugify(t) for _, t in stack]

    def flush() -> None:
        if stack and current_body:
            sections.append({
                "path": make_section_path(),
                "titles": make_path(),
                "body": "\n".join(current_body).strip(),
                "pages": sorted(current_pages),
            })

    for line in lines:
        pm = PAGE_MARKER.search(line)
        if pm:
            last_page = int(pm.group(1))
            current_pages.add(last_page)
            continue
        h = HEADING.match(line)
        if h:
            flush()
            level = len(h.group(1))
            title = h.group(2).strip()
            # Pop deeper-or-equal levels off the stack.
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            current_body = []
            current_pages = set()
            if last_page:
                current_pages.add(last_page)
            continue
        # ALL-CAPS heading detection (GWSW workbook chapters). Treat as a
        # level-2 heading nested under the existing `# Title` (level-1).
        # Heuristic guards: line must be a standalone heading (no body text
        # accumulated since the last blank line on either side), and must
        # not look like an isolated word fragment from the middle of a
        # paragraph. We require the previous non-blank emitted body line
        # to be empty / absent so that mid-sentence ALL-CAPS noise does
        # not split paragraphs.
        stripped = line.rstrip()
        if (
            stack
            and ALLCAPS_HEADING.match(stripped)
            and len(stripped.split()) >= 2
            and (not current_body or not current_body[-1].strip())
        ):
            flush()
            title = stripped.strip(": ").title()
            # Keep the level-1 (`#`) doc title and add this as a level-2.
            while stack and stack[-1][0] >= 2:
                stack.pop()
            stack.append((2, title))
            current_body = []
            current_pages = set()
            if last_page:
                current_pages.add(last_page)
            continue
        current_body.append(line)
    flush()

    # If a doc has no headings, emit a single section.
    if not sections:
        sections = [{
            "path": ["body"],
            "titles": ["Body"],
            "body": body.strip(),
            "pages": sorted({int(m.group(1)) for m in PAGE_MARKER.finditer(body)}),
        }]
    return [(s["path"], s["titles"], s["body"], s["pages"]) for s in sections]


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"[-\s]+", "-", s)[:60] or "section"


def doc_slug(doc_id: str) -> str:
    """Filesystem-safe, collision-free slug for a doc_id (preserves full path)."""
    return re.sub(r"[^\w.-]+", "__", doc_id).strip("_") or "doc"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def doc_id_for(path: Path) -> str:
    rel = path.relative_to(CORPUS)
    parts = list(rel.with_suffix("").parts)
    if parts[0] == "pappg-24-1" and len(parts) > 1:
        # All chapter shards belong to the same logical document.
        return "pappg-24-1"
    return "/".join(parts)


def doc_title_for(path: Path, frontmatter: dict[str, str]) -> str:
    if frontmatter.get("part_of"):
        return frontmatter["part_of"]
    rel = path.relative_to(CORPUS).with_suffix("")
    return str(rel).replace("_", " ").replace("/", " — ")


def source_url_for(doc_id: str, source_pdf: str) -> str:
    if doc_id in SOURCE_URLS:
        return SOURCE_URLS[doc_id]
    if "grant-writers-seminars-workshops" in source_pdf:
        return GWSW_BASE
    return ""


def make_snippets(path: Path) -> Iterable[Snippet]:
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    doc_id = doc_id_for(path)
    doc_title = doc_title_for(path, fm)
    source_pdf = fm.get("source_pdf", "")
    source_url = source_url_for(doc_id, source_pdf)

    if doc_id == "pappg-24-1" and path.name != "00-front-matter.md":
        # PAPPG chapter shards: parse the outline. Front-matter is mostly TOC
        # so fall through to heading-based sectioning for it.
        chapter_slug = fm.get("chapter_slug", path.stem)
        chapter_roman = re.sub(r"^\d+-chapter-", "", chapter_slug).upper()
        if chapter_roman == chapter_slug.upper():
            chapter_roman = chapter_roman.replace("CHAPTER-", "")
        sections = parse_pappg_outline(body)
        prefix = chapter_roman
        chapter_title = f"Chapter {chapter_roman}"
    else:
        sections = parse_markdown_headings(body)
        prefix = ""
        chapter_title = ""

    if not sections:
        return

    for path_parts, breadcrumbs, sec_body, pages in sections:
        if not sec_body.strip():
            continue
        if prefix:
            section_path = ".".join([prefix] + path_parts)
            full_breadcrumbs = [chapter_title] + breadcrumbs
        else:
            section_path = "/".join(path_parts)
            full_breadcrumbs = breadcrumbs
        title = breadcrumbs[-1] if breadcrumbs else section_path
        chunks = split_long(sec_body, MAX_CHUNK_TOKENS)
        meta = doc_meta(doc_id)
        for idx, chunk in enumerate(chunks, 1):
            strength, phrases = detect_strength(chunk)
            sid = f"{doc_id}#{section_path}"
            if len(chunks) > 1:
                sid = f"{sid}~p{idx}"
            label_path = f"§{section_path}" if prefix else f"§{section_path}"
            page_part = f", p.{pages[0]}" if pages else ""
            source_label = f"[{meta['label']} {label_path}{page_part}]"
            chunk_text = chunk.strip()
            chunk_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()[:16]
            yield Snippet(
                id=sid,
                doc_id=doc_id,
                doc_title=doc_title,
                section_path=section_path,
                section_breadcrumbs=full_breadcrumbs,
                title=title,
                text=chunk_text,
                pages=pages,
                source_pdf=source_pdf,
                source_url=source_url,
                requirement_strength=strength,
                requirement_phrases=phrases,
                char_count=len(chunk),
                est_tokens=estimate_tokens(chunk),
                source_label=source_label,
                version=meta["version"],
                effective_date=meta["effective_date"],
                chunk_hash=f"sha256:{chunk_hash}",
                cross_references=[],  # second pass below resolves these
                part=idx,
                part_count=len(chunks),
            )


def write_outputs(snippets: list[Snippet]) -> None:
    OUT.mkdir(exist_ok=True)
    by_doc_dir = OUT / "by-doc"
    by_doc_dir.mkdir(exist_ok=True)

    # Global JSONL.
    with (OUT / "snippets.jsonl").open("w", encoding="utf-8") as f:
        for s in snippets:
            f.write(json.dumps(asdict(s), ensure_ascii=False) + "\n")

    # Per-doc JSONL shards.
    by_doc: dict[str, list[Snippet]] = {}
    for s in snippets:
        by_doc.setdefault(s.doc_id, []).append(s)
    for doc_id, items in by_doc.items():
        shard = by_doc_dir / f"{doc_slug(doc_id)}.jsonl"
        with shard.open("w", encoding="utf-8") as f:
            for s in items:
                f.write(json.dumps(asdict(s), ensure_ascii=False) + "\n")

    # Context7-style markdown rendering.
    lines = [
        "# nsf-resources-text — Context7-style snippets",
        "",
        "Auto-generated by `scripts/tokenize_corpus.py`. Each snippet below is a",
        "self-contained section with stable id, breadcrumb path, page span,",
        "detected requirement strength, and the canonical source URL.",
        "",
        f"**Total snippets:** {len(snippets):,}  ",
        f"**Total est. tokens:** {sum(s.est_tokens for s in snippets):,}",
        "",
        "---",
        "",
    ]
    for s in snippets:
        pages = (
            f"{s.source_pdf}#page={s.pages[0]}"
            if s.pages else s.source_pdf
        )
        page_span = (
            f"pp. {s.pages[0]}–{s.pages[-1]}" if len(s.pages) > 1
            else (f"p. {s.pages[0]}" if s.pages else "n/a")
        )
        lines.extend([
            f"## {s.id}",
            "",
            f"TITLE: {s.title}",
            f"CITATION: {s.source_label}",
            f"DOCUMENT: {s.doc_title}",
            f"VERSION: {s.version}"
            + (f"  (effective {s.effective_date})" if s.effective_date else ""),
            f"SECTION_PATH: {s.section_path}",
            f"BREADCRUMBS: {' › '.join(s.section_breadcrumbs)}",
            f"REQUIREMENT_STRENGTH: {s.requirement_strength}"
            + (f"  (matched: {', '.join(s.requirement_phrases)})" if s.requirement_phrases else ""),
            f"PAGES: {page_span}",
            f"SOURCE_PDF: {pages}",
            f"SOURCE_URL: {s.source_url}",
            f"PART: {s.part} of {s.part_count}",
            f"EST_TOKENS: {s.est_tokens}",
            f"CHUNK_HASH: {s.chunk_hash}",
            f"CROSS_REFERENCES: {', '.join(x['raw'] + ('→' + x['id'] if x['id'] else '') for x in s.cross_references) or '(none)'}",
            "",
            "TEXT:",
            "```",
            s.text,
            "```",
            "",
            "---",
            "",
        ])
    (OUT / "snippets.context7.md").write_text("\n".join(lines), encoding="utf-8")

    # Per-snippet index.
    idx_lines = [
        "# Snippet index",
        "",
        "| ID | strength | tokens | pages | title |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for s in snippets:
        page_span = (
            f"{s.pages[0]}–{s.pages[-1]}" if len(s.pages) > 1
            else (str(s.pages[0]) if s.pages else "—")
        )
        title = s.title.replace("|", "\\|")
        idx_lines.append(f"| `{s.id}` | {s.requirement_strength} | {s.est_tokens} | {page_span} | {title} |")
    (OUT / "index.md").write_text("\n".join(idx_lines), encoding="utf-8")

    # Aggregated metadata for the corpus.
    summary = {
        "n_snippets": len(snippets),
        "n_docs": len(by_doc),
        "total_est_tokens": sum(s.est_tokens for s in snippets),
        "by_strength": {
            label: sum(1 for s in snippets if s.requirement_strength == label)
            for label in ("prohibited", "required", "recommended", "permitted", "informational")
        },
        "by_doc": {
            doc_id: {
                "n_snippets": len(items),
                "est_tokens": sum(s.est_tokens for s in items),
            }
            for doc_id, items in sorted(by_doc.items())
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_llms_txt(snippets: list[Snippet]) -> None:
    """Emit a root llmstxt.org-style index for the corpus."""
    by_doc: dict[str, list[Snippet]] = {}
    for s in snippets:
        by_doc.setdefault(s.doc_id, []).append(s)

    lines = [
        "# digital-alloy-lab NSF requirements corpus",
        "",
        "> Tokenized corpus of NSF proposal-preparation requirements (PAPPG 24-1,",
        "> Gold-Standard-Science guidance, and Grant Writers' Seminars & Workshops",
        "> workbook chapters) chunked into Context7-style snippets so LLM mock",
        "> reviewers can cite specific provisions instead of grep'ing raw PDFs.",
        "",
        "## Snippet store",
        "",
        f"- [snippets.jsonl](nsf-resources-text/snippets/snippets.jsonl): one JSON record per section "
        f"(`{len(snippets):,}` snippets, ~{sum(s.est_tokens for s in snippets):,} est. tokens)",
        "- [snippets.context7.md](nsf-resources-text/snippets/snippets.context7.md): Context7 TITLE/DESCRIPTION/SOURCE/TEXT rendering",
        "- [index.md](nsf-resources-text/snippets/index.md): one-row-per-snippet table with strength + token count + pages",
        "- [summary.json](nsf-resources-text/snippets/summary.json): aggregated counts (snippets per doc, by requirement strength)",
        "- [by-doc/](nsf-resources-text/snippets/by-doc/): per-document JSONL shards",
        "",
        "## Per-document JSONL shards",
        "",
    ]
    for doc_id, items in sorted(by_doc.items()):
        title = items[0].doc_title or doc_id
        url = items[0].source_url
        url_part = f" — source: {url}" if url else ""
        lines.append(
            f"- [{doc_id}]({Path('nsf-resources-text/snippets/by-doc') / (doc_slug(doc_id) + '.jsonl')}): "
            f"{title} ({len(items)} snippets){url_part}"
        )
    lines += [
        "",
        "## Reading guides",
        "",
        "- [MOCK_REVIEWER_PLAYBOOK.md](nsf-resources-text/MOCK_REVIEWER_PLAYBOOK.md): system prompt + 5-criterion checklist that consumes these snippets",
        "- [INDEX.md](nsf-resources-text/INDEX.md): human-readable corpus overview",
        "- [SOURCES.md](nsf-resources/SOURCES.md): canonical retrieval URLs and copyright notice",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    # Skip the unsplit ``pappg-24-1.md`` because the per-chapter shards in
    # ``pappg-24-1/`` already cover the same content (and would otherwise be
    # indexed twice, doubling the token budget).
    md_files = sorted(p for p in CORPUS.rglob("*.md")
                      if p.name not in {"INDEX.md", "MOCK_REVIEWER_PLAYBOOK.md", "pappg-24-1.md"}
                      and "snippets" not in p.parts
                      and "examples" not in p.parts)
    snippets: list[Snippet] = []
    for path in md_files:
        try:
            snippets.extend(make_snippets(path))
        except Exception as exc:  # pragma: no cover - defensive
            print(f"WARN: failed to tokenize {path}: {exc}")
    # Filter out empty / trivially small snippets so the index isn't noisy.
    snippets = [s for s in snippets if s.est_tokens >= MIN_CHUNK_TOKENS or s.requirement_strength != "informational"]
    # Second pass: resolve cross-references now that we know the full id set.
    snippet_ids = {s.id for s in snippets}
    for s in snippets:
        s.cross_references = parse_cross_references(s.text, snippet_ids)
    write_outputs(snippets)
    write_llms_txt(snippets)
    n_xrefs = sum(len(s.cross_references) for s in snippets)
    n_resolved = sum(1 for s in snippets for x in s.cross_references if x["id"])
    print(f"Wrote {len(snippets):,} snippets across {len({s.doc_id for s in snippets})} documents "
          f"(~{sum(s.est_tokens for s in snippets):,} est. tokens) to {OUT}")
    print(f"Cross-references: {n_xrefs:,} found, {n_resolved:,} resolved to known ids")


if __name__ == "__main__":
    main()
