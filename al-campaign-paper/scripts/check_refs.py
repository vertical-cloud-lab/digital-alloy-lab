#!/usr/bin/env python3
"""Check every reference in manuscript/references.bib against Crossref (or DataCite).

    python al-campaign-paper/scripts/check_refs.py

For each entry with a DOI it fetches the registered metadata and compares the title (similarity),
the year and the first author's family name. Entries without a DOI (datasheets, standards bodies,
web pages) are listed with their URL for a person to check. It also lists keys cited in main.tex
but missing from the .bib, and .bib entries that main.tex doesn't cite.

Writes manuscript/refs-check.csv and prints a summary. Exit code 1 if any DOI fails.
"""
from __future__ import annotations

import csv
import difflib
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests

PAPER = Path(__file__).resolve().parents[1]
MS = PAPER / "manuscript"
UA = {"User-Agent": "campaign-paper-refcheck/0.1 (generic client)"}


def parse_bib(text: str) -> list[dict]:
    entries = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        typ, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\},?\s*$", body, re.M | re.S):
            fields[fm.group(1).lower()] = fm.group(2)
        entries.append({"type": typ, "key": key, **fields})
    return entries


def norm(s: str) -> str:
    s = re.sub(r"\\[a-zA-Z]+|[{}$\\]", "", s or "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    # Standards: ignore "ASTM E8/E8M-24:" and a leading "standard", which registries drop.
    s = re.sub(r"^astm [a-z0-9 ]+? (?=standard|test|practice|reference|specification)", "", s)
    return re.sub(r"^standard ", "", s)


def fetch(doi: str) -> dict | None:
    for attempt in range(4):
        try:
            r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=40)
            if r.status_code == 200:
                m = r.json()["message"]
                return {"registry": "Crossref", "title": (m.get("title") or [""])[0],
                        "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                        "family": ((m.get("author") or [{}])[0]).get("family", ""),
                        "container": (m.get("container-title") or [""])[0]}
            if r.status_code == 404:
                break
        except requests.RequestException:
            pass
        time.sleep(2 + 3 * attempt)
    for attempt in range(3):
        try:
            r = requests.get(f"https://api.datacite.org/dois/{doi}", headers=UA, timeout=40)
            if r.status_code == 200:
                a = r.json()["data"]["attributes"]
                creators = a.get("creators") or [{}]
                return {"registry": "DataCite", "title": (a.get("titles") or [{}])[0].get("title", ""),
                        "year": a.get("publicationYear"), "family": creators[0].get("familyName", creators[0].get("name", "")),
                        "container": a.get("publisher", "")}
            if r.status_code == 404:
                break
        except requests.RequestException:
            pass
        time.sleep(2 + 3 * attempt)
    return None


def main() -> int:
    entries = parse_bib((MS / "references.bib").read_text(encoding="utf-8"))
    tex = (MS / "main.tex").read_text(encoding="utf-8")
    si = (MS / "si.tex").read_text(encoding="utf-8") if (MS / "si.tex").exists() else ""
    cited = set()
    for m in re.finditer(r"\\cite[tp]?\{([^}]+)\}", tex + si):
        cited.update(k.strip() for k in m.group(1).split(","))
    keys = {e["key"] for e in entries}
    rows, failures = [], 0
    for e in entries:
        doi = e.get("doi", "").strip()
        row = {"key": e["key"], "cited": e["key"] in cited, "doi": doi, "registry": "", "status": "",
               "title_similarity": "", "year_bib": e.get("year", ""), "year_registry": "",
               "first_author_bib": "", "first_author_registry": "", "registered_title": "", "url": e.get("url", "")}
        fam_bib = norm((e.get("author", "").split(" and ")[0]).split(",")[0])
        row["first_author_bib"] = fam_bib
        if not doi:
            row["status"] = "no DOI: check the URL by hand"
            rows.append(row)
            continue
        meta = fetch(doi)
        if meta is None:
            row["status"] = "FAIL: DOI not found"
            failures += 1
            rows.append(row)
            continue
        sim = difflib.SequenceMatcher(None, norm(e.get("title", "")), norm(meta["title"])).ratio()
        fam_reg = norm(meta["family"])
        year_ok = str(meta["year"]) == str(e.get("year", "")) or not e.get("year") or not meta["year"]
        auth_ok = (not fam_bib) or (not fam_reg) or fam_bib.split()[-1] in fam_reg or fam_reg.split()[-1] in fam_bib
        row.update(registry=meta["registry"], title_similarity=f"{sim:.2f}", year_registry=meta["year"],
                   first_author_registry=fam_reg, registered_title=meta["title"])
        if sim >= 0.9 and year_ok and auth_ok:
            row["status"] = "ok"
        elif sim >= 0.75:
            row["status"] = "check: " + ", ".join(x for x, ok in (("title", sim >= 0.9), ("year", year_ok), ("author", auth_ok)) if not ok)
        else:
            row["status"] = "FAIL: title mismatch"
            failures += 1
        rows.append(row)
        time.sleep(0.4)
    with open(MS / "refs-check.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    missing = sorted(cited - keys)
    uncited = sorted(keys - cited)
    n_ok = sum(r["status"] == "ok" for r in rows)
    print(f"{len(rows)} entries: {n_ok} ok, {failures} failed, "
          f"{sum(r['status'].startswith('check') for r in rows)} to check, "
          f"{sum(r['status'].startswith('no DOI') for r in rows)} without a DOI")
    for r in rows:
        if r["status"] != "ok":
            print(f"  {r['key']}: {r['status']} {r['doi'] or r['url']}")
    print("cited but missing from references.bib:", ", ".join(missing) or "none")
    print("in references.bib but not cited:", ", ".join(uncited) or "none")
    return 1 if failures or missing else 0


if __name__ == "__main__":
    sys.exit(main())
