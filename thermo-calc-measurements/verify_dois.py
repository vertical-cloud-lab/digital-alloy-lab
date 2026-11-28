#!/usr/bin/env python3
"""Check every DOI cited in this folder against Crossref (DataCite for Zenodo DOIs).

Sources scanned: README.md, sops/*.md, analysis/*.py and the Edison references
(edison/*/references.txt). For Edison references the title Edison gave is compared with the
registered title (word-overlap score), because #249 found many Edison DOIs pointing at the wrong
paper. Writes doi-check.csv with one row per (source, DOI).

    python verify_dois.py          # needs network access to api.crossref.org / api.datacite.org

Columns: doi, source, status (ok / title_mismatch / not_found), registered_title, year, first_author,
container, cited_title, overlap. "ok" for a README/SOP DOI means it resolves; the claim it backs was
checked by reading the paper's abstract or text where possible (see README, section Verification).
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).parent
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s,;\"'<>\]]+")
UA = {"User-Agent": "digital-alloy-lab-doi-check/0.1"}


def clean(doi: str) -> str:
    doi = doi.rstrip(".")
    while doi.endswith(")") and doi.count(")") > doi.count("("):
        doi = doi[:-1].rstrip(".")
    return doi


def lookup(doi: str) -> dict | None:
    for base in ("https://api.crossref.org/works/", "https://api.datacite.org/dois/"):
        try:
            with urllib.request.urlopen(urllib.request.Request(base + urllib.parse.quote(doi), headers=UA),
                                        timeout=30) as r:
                m = json.load(r)
        except Exception:
            continue
        if "message" in m:   # Crossref
            m = m["message"]
            return {"title": (m.get("title") or [""])[0],
                    "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                    "first_author": (m.get("author") or [{}])[0].get("family", ""),
                    "container": (m.get("container-title") or [""])[0], "registry": "crossref"}
        a = m.get("data", {}).get("attributes", {})   # DataCite
        return {"title": (a.get("titles") or [{}])[0].get("title", ""), "year": a.get("publicationYear"),
                "first_author": ((a.get("creators") or [{}])[0].get("familyName") or ""),
                "container": a.get("publisher", ""), "registry": "datacite"}
    return None


def words(s: str) -> set[str]:
    s = re.sub(r"<[^>]+>", " ", s.lower())
    return {w for w in re.findall(r"[a-z0-9]+", s) if len(w) > 3}


def edison_refs():
    """(doi, cited_title, source) from Edison's numbered reference lists."""
    out = []
    for f in sorted((HERE / "edison").glob("*/references.txt")):
        for line in f.read_text().splitlines():
            m = DOI_RE.search(line)
            if not m:
                continue
            cited = line.split("):", 1)[-1].split("URL:")[0].strip()   # authors. title. journal, year
            out.append((clean(m.group(0)), cited, f"edison/{f.parent.name}"))
    return out


def own_refs():
    out = []
    for f in [HERE / "README.md", *sorted((HERE / "sops").glob("*.md")), *sorted((HERE / "analysis").glob("*.py"))]:
        if f.exists():
            for m in DOI_RE.finditer(f.read_text()):
                out.append((clean(m.group(0)), "", str(f.relative_to(HERE))))
    return out


def main():
    rows, cache = [], {}
    seen = set()
    for doi, cited, src in own_refs() + edison_refs():
        if (doi, src) in seen:
            continue
        seen.add((doi, src))
        if doi not in cache:
            cache[doi] = lookup(doi)
            time.sleep(0.2)
        meta = cache[doi]
        if meta is None:
            rows.append({"doi": doi, "source": src, "status": "not_found", "cited_title": cited})
            continue
        ov = ""
        status = "ok"
        if cited:
            # share of the registered title's words that appear in Edison's reference text
            a, b = words(cited), words(meta["title"])
            ov = round(len(a & b) / max(1, len(b)), 2) if b else 0.0
            status = "ok" if ov >= 0.75 else "title_mismatch"
        rows.append({"doi": doi, "source": src, "status": status, "registered_title": meta["title"],
                     "year": meta["year"], "first_author": meta["first_author"], "container": meta["container"],
                     "cited_title": cited, "overlap": ov})
    cols = ["doi", "source", "status", "registered_title", "year", "first_author", "container", "cited_title", "overlap"]
    with open(HERE / "doi-check.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    c = Counter((r["source"].split("/")[0], r["status"]) for r in rows)
    for k, v in sorted(c.items()):
        print(k, v)


if __name__ == "__main__":
    main()
