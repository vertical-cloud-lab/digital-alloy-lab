"""Screen NASA TechPort, ARPA-E and OSTI for metal vat-photopolymerization work, from the runner (PR #229).

These three answer the runner directly, so they don't need the Pi's browser:

- TechPort's project API ignores searchQuery and returns all ~21,000 projects (~115 MB) in one response. Loading that
  in the Pi's Chromium froze the 1 GB Pi on 29 Oct 2026, so fetch it here and screen it locally. Each project lists its
  NASA contacts (PI, project manager = technical monitor, program director and manager) with e-mails, which are dropped.
- ARPA-E's project search is a React page over /JSONAPI/custom/index/project, which takes filter[fulltext].
- OSTI's records API returns DOE-sponsored reports, articles and patents with their sponsor and contract numbers.

The terms are the ones scripts/sbir_metal_vpp_screen.py uses on SBIR.gov's award file. Hits are printed for reading
by hand; raw dumps stay in /tmp.

    python -I scripts/federal_dump_screen.py techport
    python -I scripts/federal_dump_screen.py arpae stereolithography photopolymer "digital light" hydrogel
    python -I scripts/federal_dump_screen.py osti 'stereolithography metal sintering' '"hydrogel infusion"'
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sbir_metal_vpp_screen import METAL, SINTER, VPP  # noqa: E402

OUT = "/tmp/federal_dumps"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)", "Accept": "application/json"}


def get(url, timeout=300):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return json.loads(r.read().decode())


def score(text):
    """0 unless the text pairs a photopolymerization term with a metal term; sintering terms count double."""
    vpp, metal = VPP.findall(text), METAL.findall(text)
    if not vpp or not metal:
        return 0
    return len({v.lower() for v in vpp}) + len({m.lower() for m in metal}) + 2 * len({s.lower() for s in SINTER.findall(text)})


def techport():
    path = f"{OUT}/techport_all.json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(get("https://techport.nasa.gov/api/projects/search?searchQuery=stereolithography", 600), f)
    projects = json.load(open(path))["results"]
    hits = []
    for p in projects:
        text = re.sub(r"<[^>]+>", " ", f"{p.get('title', '')}\n{p.get('description') or ''}\n{p.get('benefits') or ''}")
        if s := score(text):
            hits.append((s, p))
    print(f"== TechPort: {len(hits)} of {len(projects)} projects")
    for s, p in sorted(hits, key=lambda h: -h[0]):
        who = "; ".join(f"{c['project_contact_role']}: {c['full_name']}" for c in p.get("projectContacts") or [])
        prog = "; ".join(f"{c.get('program_contact_role') or c.get('role')}: {c.get('full_name')}"
                         for c in p.get("programContacts") or [])
        sup = [o.get("organization_name") for o in p.get("otherOrganizations") or []]
        print(f"[{s}] {p['projectId']} {p['startDate'][:7]}..{p['endDate'][:7]} {p['program'].get('acronym')} "
              f"| {(p.get('leadOrganization') or {}).get('organization_name')} (with {sup}) | {p['title']}\n"
              f"     {who} | {prog}")


def arpae(terms):
    for term in terms:
        url = ("https://arpa-e.energy.gov/JSONAPI/custom/index/project?page%5Boffset%5D=0&page%5Blimit%5D=50"
               "&filter%5Bfulltext%5D=" + urllib.parse.quote(term))
        d = get(url)
        print(f"== ARPA-E {term!r}: {d['meta']['count']['count']}")
        for x in d["data"]:
            f = x["attributes"]["fields"]
            print(f"   {x['attributes']['title'][:100]} | {f.get('award')} | {f.get('release_date')} | "
                  f"{[o['fields']['title'] for o in f.get('organization', [])]} | "
                  f"{[p['fields']['title'] for p in f.get('related_programs', [])]}")


def osti(queries):
    for q in queries:
        recs = get("https://www.osti.gov/api/v1/records?" + urllib.parse.urlencode({"q": q, "rows": 100}))
        hits = sorted(((score(f"{r.get('title', '')}\n{r.get('description', '')}"), r) for r in recs),
                      key=lambda h: -h[0])
        print(f"== OSTI {q!r}: {sum(1 for s, _ in hits if s)} of {len(recs)}")
        for s, r in hits:
            if s:
                print(f"   [{s}] {r['osti_id']} {r.get('publication_date', '')[:4]} {r.get('product_type')} | "
                      f"{r['title'][:110]} | {r.get('sponsor_orgs')} | {r.get('doe_contract_number')}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cmd, args = sys.argv[1], sys.argv[2:]
    {"techport": lambda a: techport(), "arpae": arpae, "osti": osti}[cmd](args)
