"""Check every DOI in a folder of Edison reports against Crossref (PR #249, issue #235).

For each distinct DOI in the reports' markdown, it records how the report cites it (the text just before the
DOI on its line), what Crossref (or DataCite, for data and theses) says it is, and a first-pass verdict:
"title matches the citation" if most of the registered title's words are in the citing text, else "first author
matches the citation", else "check by hand"; "not found" if neither registry knows the DOI. The verdict is a
screen, not proof; the rows marked "check by hand" are read by hand.

    python scripts/edison_doi_check.py edison-trajectories/keyhole-first-principles doi-check.csv
"""
import csv
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\]\|,;\"'>]+")
STOP = {"the", "of", "and", "in", "a", "an", "for", "on", "by", "to", "with", "at", "from", "during", "its"}


def clean(doi):
    doi = doi.replace("\\_", "_").rstrip(".").rstrip("*")
    while doi.endswith(")") and doi.count(")") > doi.count("("):
        doi = doi[:-1]
    return doi.rstrip(".")


def datacite(doi):
    url = "https://api.datacite.org/dois/" + urllib.parse.quote(doi)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "doi-check"}), timeout=30) as r:
            a = json.load(r)["data"]["attributes"]
        cr = (a.get("creators") or [{}])[0]
        return {"author": [{"family": cr.get("familyName") or cr.get("name", "")}],
                "issued": {"date-parts": [[a.get("publicationYear")]]},
                "container-title": [a.get("publisher", "") if isinstance(a.get("publisher"), str) else ""],
                "title": [(a.get("titles") or [{}])[0].get("title", "")], "_source": "DataCite"}
    except Exception:
        return None


def title_match(title, ctx):
    words = [w for w in re.findall(r"[a-z0-9]+", title.lower()) if w not in STOP][:8]
    if not words:
        return False
    c = ctx.lower()
    return sum(w in c for w in words) / len(words) >= 0.6


def crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "doi-check (research script)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["message"]
    except Exception:
        return None


def main(folder, out_name):
    folder = pathlib.Path(folder)
    seen = {}
    # Reports first, artifacts after: a report line names the authors, an artifact table cell often only a key.
    for f in sorted(folder.glob("*.md"), key=lambda f: (f.name.endswith("-artifacts.md"), f.name)):
        for line in f.read_text().splitlines():
            for m in DOI_RE.finditer(line):
                doi = clean(m.group(0))
                ctx = re.sub(r"\s+", " ", line[max(0, m.start() - 320):m.start()]).strip()
                d = seen.setdefault(doi.lower(), {"doi": doi, "cited_as": ctx, "files": set()})
                d["files"].add(f.name)
    rows = []
    for key, d in sorted(seen.items()):
        msg = crossref(d["doi"]) or datacite(d["doi"])
        time.sleep(0.2)
        if msg is None:
            rows.append({"doi": d["doi"], "cited_as": d["cited_as"][-160:], "crossref": "", "verdict": "not found",
                         "files": " ".join(sorted(d["files"]))})
            continue
        au = (msg.get("author") or [{}])[0].get("family", "")
        yr = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
        jn = (msg.get("container-title") or [""])[0]
        ti = (msg.get("title") or [""])[0]
        if title_match(ti, d["cited_as"]):
            verdict = "title matches the citation"
        elif au and au.lower() in d["cited_as"].lower():
            verdict = "first author matches the citation"
        else:
            verdict = "check by hand"
        rows.append({"doi": d["doi"], "cited_as": d["cited_as"][-160:], "crossref": f"{au} {yr}, {jn}: {ti}"[:240],
                     "verdict": verdict + (" (DataCite)" if msg.get("_source") == "DataCite" else ""),
                     "files": " ".join(sorted(d["files"]))})
    with open(folder / out_name, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["doi", "cited_as", "crossref", "verdict", "files"])
        w.writeheader()
        w.writerows(rows)
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print(len(rows), "DOIs:", counts)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
