"""Re-fetch the sanitary-fitting, valve, gasket, filler-rod and metal-stock pages in vendor-lookups.csv.

    python bom/fetch_sanitary.py [url-substring]      # e.g. mcmaster.com/5237K47

Renders each page with fetch_render.py (headless Chrome via the SOCKS tunnel on 127.0.0.1:1080), three at a
time, and prints the lines that carry a listed part number and a price.
"""
import csv
import re
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
RENDER = [sys.executable, str(HERE / "fetch_render.py")]
PRICE = re.compile(r"\$\s?\d[\d,]*\.\d\d")
ITEMS = re.compile(r"ferrule|reducer|tri-?clamp|TC |gasket|butterfly|316L tube|304 tube|316L bar|304 bar|304 sheet|ER316L|spacer", re.I)
pages = defaultdict(set)
for r in csv.DictReader(open(HERE / "vendor-lookups.csv")):
    if (r["url"].startswith("http") and ITEMS.search(r["item"]) and "KF" not in r["item"]
            and (len(sys.argv) < 2 or sys.argv[1] in r["url"])):
        pages[r["url"]].add(r["part_number"].split(" ")[0])


def fetch(item):
    url, pns = item
    try:
        out = subprocess.run(RENDER + [url, "--wait", "8"], capture_output=True, text=True, timeout=150).stdout
    except subprocess.TimeoutExpired:
        return url, ["TIMEOUT"]
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    hits = [ln for ln in lines if any(pn and pn in ln for pn in pns) and (PRICE.search(ln) or re.search(r"\t\d+\.\d\d\b", ln))]
    if not hits:  # single-product pages: the price sits on its own line
        hits = [ln for ln in lines if PRICE.search(ln) and "minimum" not in ln.lower() and "shipping" not in ln.lower()][:3]
    return url, hits


with ThreadPoolExecutor(3) as ex:
    for url, hits in ex.map(fetch, sorted(pages.items())):
        print("==", url, "| parts:", ", ".join(sorted(pages[url])))
        for h in hits[:12]:
            print("   ", h[:220])
