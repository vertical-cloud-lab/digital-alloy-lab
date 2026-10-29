"""Search federal award databases from the panel Pi's headed Chromium (PR #229).

Uses the Tab class in pi_browser.py, so every page loads in the Pi's own browser over the DevTools
tunnel described there. Each site is opened first and the pointer moves and scrolls on it before the
query runs. The NSF API is a GET, so it is loaded as a page; NIH RePORTER and USAspending take POSTs,
which are sent with fetch() from a tab on the API's own origin. Results go to /tmp/pi_grants/*.json,
with e-mail and phone fields dropped (NSF's coPDPI strings still embed co-PI e-mails, so don't commit raw dumps).

Keep to JSON APIs and light pages. On 29 Oct 2026 loading NASA TechPort froze the 1 GB Pi until it rebooted itself
(Tailscale ping and SSH timed out for ~10 minutes), and Chromium had to be relaunched afterwards. TechPort's API sends
all ~21,000 projects whatever the query, so screen it on the runner instead (scripts/federal_dump_screen.py).

DOE Office of Science's PAMS award search is an ASP.NET form that timed out from the runner, so it runs here: the
award number or abstract keyword is typed into the form, the status filter is set to All, and Search is clicked.
Each hit's public abstract names the DOE program manager (PM).

    python scripts/pi_grant_search.py nsf '"vat photopolymerization"' stereolithography ...
    python scripts/pi_grant_search.py nih '(stereolithography OR "digital light processing") AND metal'
    python scripts/pi_grant_search.py usaspending stereolithography "digital light processing" ...
    python scripts/pi_grant_search.py sbir "metal stereolithography" ...
    python scripts/pi_grant_search.py pams SC0016945 "abstract:digital light processing" ...
"""

import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pi_browser as pb  # noqa: E402

OUT = "/tmp/pi_grants"
PRIVATE = re.compile(r"email|phone|fax", re.I)


def strip_private(obj):
    if isinstance(obj, dict):
        return {k: strip_private(v) for k, v in obj.items() if not PRIVATE.search(k)}
    if isinstance(obj, list):
        return [strip_private(v) for v in obj]
    return obj


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def visit(tab, url):
    tab.goto(url)
    tab.wander(1)
    tab.scroll(500)


def nsf(tab, query):
    """Every NSF award whose title or abstract matches the query (quotes make a phrase)."""
    awards, offset = [], 0
    while True:
        url = ("https://api.nsf.gov/services/v1/awards.json?rpp=25&offset=%d&keyword=%s"
               % (offset, urllib.parse.quote(query)))
        tab.goto(url)
        d = json.loads(tab.js("document.body.innerText"))["response"]
        batch = d.get("award", [])
        awards += batch
        total = d.get("metadata", {}).get("totalCount", 0)
        if not batch or len(awards) >= min(total, 1000):
            break
        offset += 25
        pb.pause(0.8, 1.6)
    print(f"== NSF {query!r}: {len(awards)} of {total}")
    return strip_private(awards)


FETCH = """(async () => {
  const r = await fetch(%s, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: %s});
  return await r.text();
})()"""


def nih(tab, query):
    """NIH RePORTER projects matching an advanced text query over titles, terms and abstracts."""
    if "api.reporter.nih.gov" not in (tab.js("location.href") or ""):
        visit(tab, "https://reporter.nih.gov/")
        tab.goto("https://api.reporter.nih.gov/")  # same origin as the API, so fetch() needs no CORS
    rows, offset = [], 0
    while True:
        body = {"criteria": {"advanced_text_search": {"operator": "advanced", "search_field": "projecttitle,terms,abstracttext",
                                                       "search_text": query}},
                "offset": offset, "limit": 500}
        d = json.loads(tab.js(FETCH % (json.dumps("https://api.reporter.nih.gov/v2/projects/search"),
                                       json.dumps(json.dumps(body)))))
        rows += d.get("results", [])
        total = d.get("meta", {}).get("total", 0)
        if len(rows) >= min(total, 2000) or not d.get("results"):
            break
        offset += 500
    print(f"== NIH {query!r}: {len(rows)} of {total}")
    return strip_private(rows)


def usaspending(tab, query):
    """Grants and contracts on USAspending whose description matches the keyword."""
    if "usaspending.gov" not in (tab.js("location.href") or ""):
        visit(tab, "https://www.usaspending.gov/search")
    fields = ["Award ID", "Recipient Name", "Description", "Award Amount", "Awarding Agency",
              "Awarding Sub Agency", "Funding Sub Agency", "Start Date", "End Date", "Award Type",
              "generated_internal_id"]
    rows = []
    for group, codes in (("grants", ["02", "03", "04", "05"]), ("contracts", ["A", "B", "C", "D"])):
        page = 1
        while True:
            body = {"filters": {"keywords": [query], "award_type_codes": codes,
                                "time_period": [{"start_date": "2007-10-01", "end_date": "2026-09-30"}]},
                    "fields": fields, "page": page, "limit": 100, "sort": "Award Amount", "order": "desc"}
            d = json.loads(tab.js(FETCH % (json.dumps("https://api.usaspending.gov/api/v2/search/spending_by_award/"),
                                           json.dumps(json.dumps(body)))))
            for r in d.get("results", []):
                r["group"] = group
            rows += d.get("results", [])
            if not d.get("page_metadata", {}).get("hasNext") or page >= 5:
                break
            page += 1
    print(f"== USAspending {query!r}: {len(rows)}")
    return rows


SBIR_RESULTS = r"""(() => {
  const out = [];
  for (const a of document.querySelectorAll('h4 a[href*="/awards/"]')) {
    const card = a.closest('div') ? a.closest('div').parentElement : a.parentElement;
    out.push({title: a.innerText.trim(), href: a.href, text: (card ? card.innerText : '').slice(0, 900)});
  }
  const m = document.body.innerText.match(/Showing \d+-\d+ of (\d+) results/);
  return {total: m ? +m[1] : 0, items: out};
})()"""


def sbir(tab, query):
    """SBIR.gov's own award search, typed into the Keywords box and paged through."""
    visit(tab, "https://www.sbir.gov/awards")
    tab.click("input[name='keywords'], input#edit-keywords")
    tab.type(query)
    pb.pause(0.4, 0.9)
    tab.js("window.__oldDoc = 1")
    tab.key("Enter", "Enter", 13, text="\r")
    tab.wait_loaded(settle=(3, 5))
    tab.scroll(1500)
    res = tab.js(SBIR_RESULTS)
    items, page = res["items"], 0
    while len(items) < min(res["total"], 100):
        page += 1
        tab.goto(tab.js("location.href").split("&page=")[0] + f"&page={page}")
        more = tab.js(SBIR_RESULTS)["items"]
        if not more:
            break
        items += more
    print(f"== SBIR.gov {query!r}: {len(items)} of {res['total']}")
    return items


def sbir_award(tab, url):
    """One SBIR.gov award page: agency, branch, contract, PI and abstract."""
    visit(tab, url)
    return {"url": url, "text": tab.js("document.querySelector('main') ? document.querySelector('main').innerText"
                                       " : document.body.innerText")[:6000]}


PAMS = "https://pamspublic.science.energy.gov/WebPAMSExternal/Interface/Awards/AwardSearchExternal.aspx"
PAMS_ROWS = r"""(() => Array.from(document.querySelectorAll('table tr')).map(tr => {
  const tds = Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim().replace(/\s+/g, ' '));
  const a = Array.from(tr.querySelectorAll('a')).find(a => /View Abstract/.test(a.innerText));
  const m = a && a.href.match(/OpenPopupWithMenuBar\("([^"]+)"/);
  return {cells: tds, abstract: m ? decodeURIComponent(m[1]) : null};
}).filter(r => r.cells.length >= 5 && /DE-[A-Z]{2}\d{7}/.test(r.cells.join(' '))))()"""


def pams(tab, query):
    """PAMS awards by award number, or by abstract keyword with an "abstract:" prefix; PM read from each abstract."""
    field = "txtAbstractKeyword" if query.startswith("abstract:") else "txtAwardNumber"
    value = query.split(":", 1)[1] if query.startswith("abstract:") else query
    visit(tab, PAMS)
    tab.click(f"#ctl00_MainContent_pnlSearch_{field}")
    tab.type(value)
    pb.pause(0.3, 0.7)
    tab.js("""(() => { const s = document.querySelector('#ctl00_MainContent_pnlSearch_ddAwardStatus');
        s.value = '0'; s.dispatchEvent(new Event('change', {bubbles: true})); })()""")  # status: All
    tab.js("window.__oldDoc = 1")
    tab.click("#btnSearch")
    tab.wait_loaded(settle=(3, 5))
    rows = tab.js(PAMS_ROWS)
    for r in rows:
        if r["abstract"]:
            tab.goto(urllib.parse.urljoin(PAMS, r["abstract"]))
            text = tab.js("document.body.innerText")
            r["pm"] = (re.search(r"PM: (.+)", text) or [None, None])[1]
            r["abstract_text"] = text[:4000]
    print(f"== PAMS {query!r}: {len(rows)}")
    for r in rows:
        print("   " + " | ".join(r["cells"][1:5]) + f" | PM: {r.get('pm')}")
    return rows


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cmd, args = sys.argv[1], sys.argv[2:]
    fn = {"nsf": nsf, "nih": nih, "usaspending": usaspending, "sbir": sbir, "sbir-award": sbir_award, "pams": pams}[cmd]
    with pb.Tab() as tab:
        if cmd == "nsf":
            visit(tab, "https://www.nsf.gov/awardsearch/")
        for i, arg in enumerate(args):
            res = fn(tab, arg)
            with open(f"{OUT}/{cmd}-{slug(arg)}.json", "w") as f:
                json.dump(res, f, indent=1)
            if i < len(args) - 1:
                pb.pause(2, 4)
