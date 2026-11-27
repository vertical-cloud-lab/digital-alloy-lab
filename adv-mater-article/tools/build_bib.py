#!/usr/bin/env python3
"""Build references.bib from tools/refs.tsv using Crossref (and DataCite/arXiv) metadata.

Every journal entry is generated from the registry record of its DOI, so author
lists, years, volumes and pages come from the publisher's deposit rather than
from memory. Conference papers without a Crossref DOI live in
references-manual.bib and are appended unchanged; check_refs.py checks those
against arXiv.

Usage (from adv-mater-article/):
    python tools/build_bib.py            # fetch (cached) and write references.bib
    python tools/build_bib.py --refresh  # ignore the cache
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = HERE / "cache"
UA = {"User-Agent": "refcheck/0.1"}  # generic on purpose: no names or e-mails

# ISO 4 / CASSI abbreviations, as Advanced Materials asks for abbreviated titles.
ABBREV = {
    "Nature": "Nature",
    "Progress in Materials Science": "Prog. Mater. Sci.",
    "Additive Manufacturing": "Addit. Manuf.",
    "International Materials Reviews": "Int. Mater. Rev.",
    "Acta Materialia": "Acta Mater.",
    "Physics Procedia": "Phys. Procedia",
    "Materials & Design": "Mater. Des.",
    "Advanced Materials": "Adv. Mater.",
    "Science Advances": "Sci. Adv.",
    "Environmental Science & Technology": "Environ. Sci. Technol.",
    "Materials": "Materials",
    "Johnson Matthey Technology Review": "Johnson Matthey Technol. Rev.",
    "Rapid Prototyping Journal": "Rapid Prototyp. J.",
    "Chemical Reviews": "Chem. Rev.",
    "Nature Synthesis": "Nat. Synth.",
    "Matter": "Matter",
    "Nature Communications": "Nat. Commun.",
    "Digital Discovery": "Digital Discovery",
    "Materials Science and Engineering: A": "Mater. Sci. Eng. A",
    "npj Advanced Manufacturing": "npj Adv. Manuf.",
    "Royal Society Open Science": "R. Soc. Open Sci.",
    "npj Computational Materials": "npj Comput. Mater.",
    "Nature Computational Science": "Nat. Comput. Sci.",
    "Calphad": "Calphad",
    "Journal of Open Research Software": "J. Open Res. Softw.",
    "Applied Materials Today": "Appl. Mater. Today",
    "Journal of Open Source Software": "J. Open Source Softw.",
    "Metallurgical and Materials Transactions A": "Metall. Mater. Trans. A",
    "JOM": "JOM",
    "Scripta Materialia": "Scr. Mater.",
    "Journal of Alloys and Compounds": "J. Alloys Compd.",
    "Powder Technology": "Powder Technol.",
    "Materials Today": "Mater. Today",
    "Nature Materials": "Nat. Mater.",
    "Science": "Science",
    "Advanced Functional Materials": "Adv. Funct. Mater.",
    "Advanced Science": "Adv. Sci.",
    "Advanced Intelligent Systems": "Adv. Intell. Syst.",
    "Journal of Materials Processing Technology": "J. Mater. Process. Technol.",
    "Corrosion Science": "Corros. Sci.",
    "Materials Characterization": "Mater. Charact.",
    "Integrating Materials and Manufacturing Innovation": "Integr. Mater. Manuf. Innov.",
}


def read_list(path: Path) -> list[tuple[str, str, str]]:
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            sys.exit(f"bad line in {path.name}: {line!r}")
        rows.append((parts[0].strip(), parts[1].strip(), parts[2].strip() if len(parts) > 2 else ""))
    keys = [r[0] for r in rows]
    dupes = {k for k in keys if keys.count(k) > 1}
    if dupes:
        sys.exit(f"duplicate keys: {sorted(dupes)}")
    return rows


def cached_get(url: str, name: str, refresh: bool, accept: str | None = None) -> tuple[int, str]:
    CACHE.mkdir(exist_ok=True)
    f = CACHE / name
    if f.exists() and not refresh:
        status, body = f.read_text().split("\n", 1)
        return int(status), body
    headers = dict(UA)
    if accept:
        headers["Accept"] = accept
    for attempt in range(4):
        try:
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 * (attempt + 1))
                continue
            f.write_text(f"{r.status_code}\n{r.text}")
            time.sleep(0.2)
            return r.status_code, r.text
        except requests.RequestException:
            time.sleep(2 * (attempt + 1))
    return 0, ""


def safe_name(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


def crossref(doi: str, refresh: bool) -> dict | None:
    st, body = cached_get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}",
                          f"crossref_{safe_name(doi)}.json", refresh)
    if st == 200:
        return json.loads(body)["message"]
    return None


def datacite(doi: str, refresh: bool) -> dict | None:
    st, body = cached_get(f"https://api.datacite.org/dois/{urllib.parse.quote(doi)}",
                          f"datacite_{safe_name(doi)}.json", refresh)
    if st == 200:
        return json.loads(body)["data"]["attributes"]
    return None


def arxiv(aid: str, refresh: bool) -> dict | None:
    st, body = cached_get(f"https://export.arxiv.org/api/query?id_list={aid}",
                          f"arxiv_{safe_name(aid)}.xml", refresh)
    if st != 200:
        return None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(body)
    e = root.find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        return None
    return {
        "title": " ".join(e.find("a:title", ns).text.split()),
        "authors": [" ".join(a.find("a:name", ns).text.split()) for a in e.findall("a:author", ns)],
        "published": e.find("a:published", ns).text[:10],
    }


TAGS = [
    (re.compile(r"<(?:jats:)?sub>(.*?)</(?:jats:)?sub>", re.S), r"\\textsubscript{\1}"),
    (re.compile(r"<(?:jats:)?sup>(.*?)</(?:jats:)?sup>", re.S), r"\\textsuperscript{\1}"),
    (re.compile(r"<(?:jats:)?i(?:talic)?>(.*?)</(?:jats:)?i(?:talic)?>", re.S), r"\\textit{\1}"),
]


def tex_text(s: str) -> str:
    """Make a Crossref string safe for pdflatex + biber."""
    s = html.unescape(s)
    s = s.replace("\u2010", "-").replace("\u2011", "-").replace("\u2012", "-")
    s = s.replace("\u2013", "--").replace("\u2014", "---").replace("\u2009", " ").replace("\u00a0", " ")
    s = s.replace("\u2018", "`").replace("\u2019", "'").replace("\u201c", "``").replace("\u201d", "''")
    for pat, rep in TAGS:
        s = pat.sub(lambda m, rep=rep: rep.replace(r"\1", m.group(1)), s)
    s = re.sub(r"</?[a-zA-Z:]+[^>]*>", "", s)  # any other markup
    s = re.sub(r"(?<!\\)([&%#_])", r"\\\1", s)
    return " ".join(s.split())


def date_year(msg: dict) -> str:
    for k in ("published-print", "published-online", "issued", "published"):
        dp = msg.get(k, {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            return str(dp[0][0])
    return ""


def authors_from_crossref(msg: dict) -> str:
    out = []
    people = [a for a in msg.get("author", []) if "family" in a]
    # Some report deposits (OSTI) mix institutions into the author list; keep
    # only the people when there are any.
    for a in (people or msg.get("author", [])):
        if "family" in a:
            given = a.get("given", "")
            out.append(f"{tex_text(a['family'])}, {tex_text(given)}" if given else tex_text(a["family"]))
        elif "name" in a:
            out.append("{" + tex_text(a["name"]) + "}")
    return " and ".join(out)


def journal_name(msg: dict) -> str:
    full = (msg.get("container-title") or [""])[0]
    full = html.unescape(full)
    if full in ABBREV:
        return ABBREV[full]
    short = (msg.get("short-container-title") or [""])[0]
    return tex_text(short or full)


def entry_from_crossref(key: str, doi: str, msg: dict) -> str:
    typ = msg.get("type", "")
    title = tex_text((msg.get("title") or [""])[0])
    f = {"author": authors_from_crossref(msg), "title": "{" + title + "}", "year": date_year(msg), "doi": doi}
    if typ == "journal-article":
        bibtype = "article"
        f["journaltitle"] = journal_name(msg)
        if msg.get("volume"):
            f["volume"] = msg["volume"]
        if msg.get("issue"):
            f["number"] = msg["issue"]
        pages = msg.get("page") or msg.get("article-number")
        if pages:
            f["pages"] = pages.replace("-", "--") if "--" not in pages else pages
    elif typ in ("report", "report-component", "monograph"):
        bibtype = "report"
        f["type"] = "Report"
        inst = msg.get("publisher", "")
        f["institution"] = tex_text(inst)
        if not f["author"] and inst:
            f["author"] = "{" + tex_text(inst) + "}"
    elif typ == "posted-content":
        bibtype = "online"
        f["pubstate"] = "prepublished"
        f["organization"] = tex_text(msg.get("institution", [{}])[0].get("name", msg.get("publisher", "")))
        f["url"] = msg.get("URL", f"https://doi.org/{doi}")
    elif typ == "proceedings-article":
        bibtype = "inproceedings"
        f["booktitle"] = tex_text((msg.get("container-title") or [""])[0])
        if msg.get("page"):
            f["pages"] = msg["page"].replace("-", "--")
    else:
        bibtype = "misc"
        f["howpublished"] = tex_text(msg.get("publisher", ""))
    body = ",\n".join(f"  {k:<12} = {{{v}}}" for k, v in f.items() if v)
    return f"@{bibtype}{{{key},\n{body},\n}}\n"


def entry_from_datacite(key: str, doi: str, a: dict) -> str:
    creators = []
    for c in a.get("creators", []):
        if c.get("familyName"):
            creators.append(f"{tex_text(c['familyName'])}, {tex_text(c.get('givenName', ''))}")
        else:
            creators.append("{" + tex_text(c.get("name", "")) + "}")
    title = tex_text(a.get("titles", [{}])[0].get("title", ""))
    f = {"author": " and ".join(creators), "title": "{" + title + "}", "year": str(a.get("publicationYear", "")),
         "doi": doi, "organization": tex_text(a.get("publisher") if isinstance(a.get("publisher"), str)
                                              else (a.get("publisher") or {}).get("name", ""))}
    body = ",\n".join(f"  {k:<12} = {{{v}}}" for k, v in f.items() if v)
    return f"@online{{{key},\n{body},\n}}\n"


def entry_from_arxiv(key: str, aid: str, a: dict) -> str:
    authors = []
    for n in a["authors"]:
        parts = n.split()
        authors.append(f"{tex_text(parts[-1])}, {tex_text(' '.join(parts[:-1]))}" if len(parts) > 1 else tex_text(n))
    f = {"author": " and ".join(authors), "title": "{" + tex_text(a["title"]) + "}",
         "year": a["published"][:4], "eprint": aid, "eprinttype": "arxiv", "pubstate": "prepublished"}
    body = ",\n".join(f"  {k:<12} = {{{v}}}" for k, v in f.items() if v)
    return f"@online{{{key},\n{body},\n}}\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    rows = read_list(HERE / "refs.tsv")
    out, problems = [], []
    for key, ident, _why in rows:
        if ident == "manual":
            continue
        kind, _, val = ident.partition(":")
        if kind == "doi":
            msg = crossref(val, args.refresh)
            if msg:
                out.append(entry_from_crossref(key, val, msg))
                continue
            dc = datacite(val, args.refresh)
            if dc:
                out.append(entry_from_datacite(key, val, dc))
                continue
            problems.append(f"{key}: DOI {val} not found in Crossref or DataCite")
        elif kind == "arxiv":
            a = arxiv(val, args.refresh)
            if a:
                out.append(entry_from_arxiv(key, val, a))
            else:
                problems.append(f"{key}: arXiv {val} not found")
        else:
            problems.append(f"{key}: unknown id {ident}")
    manual = (ROOT / "references-manual.bib").read_text()
    header = ("% GENERATED by tools/build_bib.py from tools/refs.tsv (Crossref/DataCite/arXiv metadata)\n"
              "% plus references-manual.bib. Edit those, not this file.\n\n")
    (ROOT / "references.bib").write_text(header + "\n".join(out) + "\n" + manual)
    print(f"wrote references.bib: {len(out)} generated + manual entries")
    for p in problems:
        print("PROBLEM:", p)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
