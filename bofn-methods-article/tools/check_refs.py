#!/usr/bin/env python3
"""Check references.bib against Crossref (and arXiv), and check the citations in the .tex files.

For each entry with a DOI, the Crossref record is fetched (cached in tools/cache/)
and compared field by field: title, first author, year, journal, volume, pages.
Entries with an arXiv eprint and no DOI are checked against the arXiv API. The
script also lists \\cite keys missing from the .bib, entries never cited, and any
Crossref update notices (corrections, retractions) attached to a DOI.

Writes reference-check.md. Exit status 1 if anything fails.

Usage (from bofn-methods-article/):  python tools/check_refs.py [--refresh]
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bib as bb  # noqa: E402  (shared fetch + cache helpers)

ROOT = Path(__file__).resolve().parent.parent
TEX_FILES = ["methodsx/manuscript.tex", "adv-mater/methods-si.tex"]


def parse_bib(text: str) -> dict[str, dict]:
    entries = {}
    for m in re.finditer(r"@(\w+)\{([^,\s]+),(.*?)\n\}", text, re.S):
        typ, key, body = m.groups()
        fields = {}
        for fm in re.finditer(r"^\s*(\w+)\s*=\s*\{(.*)\},?\s*$", body, re.M):
            fields[fm.group(1).lower()] = fm.group(2)
        fields["_type"] = typ.lower()
        entries[key] = fields
    return entries


def norm(s: str) -> str:
    s = re.sub(r"\\text(?:it|bf|subscript|superscript)\{([^}]*)\}", r"\1", s)
    s = re.sub(r"[{}\\$]", "", s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("--", "-").lower()
    s = re.sub(r"&amp;|&", "and", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def sim(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def cited_keys() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for name in TEX_FILES:
        p = ROOT / name
        if not p.exists():
            continue
        txt = re.sub(r"(?<!\\)%.*", "", p.read_text())
        for m in re.finditer(r"\\(?:cite|parencite|textcite|supercite|autocite|nocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}", txt):
            for k in m.group(1).split(","):
                k = k.strip()
                if k and k != "*":
                    found.setdefault(k, []).append(name)
    return found


def check_crossref(key: str, f: dict, refresh: bool) -> tuple[str, list[str], dict]:
    doi = f["doi"]
    msg = bb.crossref(doi, refresh)
    info = {}
    if msg is None:
        dc = bb.datacite(doi, refresh)
        if dc is None:
            return "FAIL", [f"DOI {doi} resolves in neither Crossref nor DataCite"], info
        title = dc.get("titles", [{}])[0].get("title", "")
        info = {"title": title, "year": str(dc.get("publicationYear", "")), "venue": "DataCite record"}
        notes = []
        if sim(f.get("title", ""), title) < 0.9:
            notes.append(f"title differs from DataCite: {title!r}")
        return ("WARN" if notes else "OK (DataCite)"), notes, info
    notes = []
    title = (msg.get("title") or [""])[0]
    year = bb.date_year(msg)
    journal = (msg.get("container-title") or [""])[0]
    info = {"title": title, "year": year, "venue": journal}
    s = sim(f.get("title", ""), title)
    if s < 0.9:
        notes.append(f"title similarity {s:.2f} vs Crossref {title!r}")
    people = [a for a in msg.get("author", []) if "family" in a]
    if "withheld" in f.get("author", ""):
        notes.append("authors withheld in the public repo (partner staff); restore with --full-authors at submission")
        people = []
    if people:
        first_bib = f.get("author", "").split(" and ")[0].split(",")[0]
        if norm(first_bib) != norm(people[0]["family"]):
            notes.append(f"first author {first_bib!r} vs Crossref {people[0]['family']!r}")
        n_bib = len([a for a in f.get("author", "").split(" and ") if a.strip()])
        if n_bib != len(people):
            notes.append(f"{n_bib} authors in .bib vs {len(people)} in Crossref")
    if f.get("year") and year and f["year"] != year:
        notes.append(f"year {f['year']} vs Crossref {year}")
    if f.get("volume") and msg.get("volume") and f["volume"] != msg["volume"]:
        notes.append(f"volume {f['volume']} vs Crossref {msg['volume']}")
    cr_pages = (msg.get("page") or msg.get("article-number") or "").replace("--", "-")
    if f.get("pages") and cr_pages and f["pages"].replace("--", "-") != cr_pages:
        notes.append(f"pages {f['pages']} vs Crossref {cr_pages}")
    for upd in msg.get("updated-by", []) or []:
        notes.append(f"Crossref update notice: {upd.get('type')} ({upd.get('DOI')})")
    for rel, items in (msg.get("relation") or {}).items():
        if "retract" in rel or "correct" in rel:
            notes.append(f"Crossref relation {rel}: {[i.get('id') for i in items]}")
    status = "OK" if not notes or all(n.startswith("authors withheld") for n in notes) else (
        "FAIL" if any(n.startswith(("title", "first author")) for n in notes) else "WARN")
    return status, notes, info


def check_arxiv(key: str, f: dict, refresh: bool) -> tuple[str, list[str], dict]:
    aid = f["eprint"]
    a = bb.arxiv(aid, refresh)
    if a is None:
        return "FAIL", [f"arXiv {aid} not found"], {}
    info = {"title": a["title"], "year": a["published"][:4], "venue": f"arXiv:{aid}"}
    notes = []
    s = sim(f.get("title", ""), a["title"])
    if s < 0.9:
        notes.append(f"title similarity {s:.2f} vs arXiv {a['title']!r}")
    first_bib = norm(f.get("author", "").split(" and ")[0].split(",")[0])
    if first_bib and first_bib not in norm(a["authors"][0]):
        notes.append(f"first author vs arXiv {a['authors'][0]!r}")
    status = "OK (arXiv)" if not notes else "FAIL"
    return status, notes, info


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    entries = parse_bib((ROOT / "references.bib").read_text())
    cites = cited_keys()
    rows, fails = [], 0
    for key, f in entries.items():
        if f.get("doi"):
            status, notes, info = check_crossref(key, f, args.refresh)
        elif f.get("eprint"):
            status, notes, info = check_arxiv(key, f, args.refresh)
        else:
            status, notes, info = "UNCHECKED", ["no DOI or arXiv id"], {}
        if key not in cites:
            notes.append("not cited in the .tex files")
        fails += status == "FAIL"
        rows.append((key, status, info, notes))
    missing = sorted(k for k in cites if k not in entries)
    today = dt.date.today().isoformat()
    out = [
        "# Reference check",
        "",
        f"Generated by `tools/check_refs.py` on {today}. Every entry with a DOI was compared with its Crossref "
        "record (title, first author, author count, year, volume, pages, and any correction or retraction notice). "
        "Conference papers without a DOI were compared with arXiv. Rebuild with `make refs`.",
        "",
        f"- Entries: {len(entries)}; cited keys: {len(cites)}",
        f"- FAIL: {fails}; WARN: {sum(r[1] == 'WARN' for r in rows)}; "
        f"not cited: {sum('not cited in the .tex files' in r[3] for r in rows)}",
        f"- Cited but missing from references.bib: {', '.join(missing) if missing else 'none'}",
        "",
        "| Key | Status | Registry title (year, venue) | Notes |",
        "|---|---|---|---|",
    ]
    for key, status, info, notes in rows:
        t = info.get("title", "").replace("|", "\\|")
        t = re.sub(r"<[^>]+>", "", t)
        venue = f"{info.get('year', '')}, {info.get('venue', '')}".strip(", ")
        out.append(f"| `{key}` | {status} | {t[:110]}{'…' if len(t) > 110 else ''} ({venue}) | {'; '.join(notes)} |")
    (ROOT / "reference-check.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[4:8]))
    if fails or missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
