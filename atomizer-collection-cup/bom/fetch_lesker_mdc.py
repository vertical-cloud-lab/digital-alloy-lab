"""Re-fetch the KF-50 rows priced from Kurt J. Lesker and MDC Precision (public catalogue pages, no login).

    python bom/fetch_lesker_mdc.py            # Lesker tables (plain HTTP) + MDC part pages (headless Chrome)
    python bom/fetch_lesker_mdc.py --lesker   # Lesker only (no browser needed)

Lesker's ordering tables are in the page HTML; MDC's site is client-rendered, so its part pages need
Playwright (pip install playwright beautifulsoup4 lxml; it uses the system Chrome). Prints one line per
KF-50 row: part number, the table's columns, price. Compare against vendor-lookups.csv.
"""
import re
import subprocess
import sys
import time

import requests
from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"}
LESKER = "https://www.lesker.com/newweb/flanges/"
LESKER_PAGES = [
    "flanges_kf_weld.cfm?pgid=weld3",            # short weld stubs QF50-200-SS / -SSL / -SST
    "flanges_kf_weld.cfm?pgid=weld2",            # short weld flange QF50-200-SF
    "flanges_kf_blank.cfm?pgid=flange1",         # blank QF50-200-SB
    "fittings_kf_nipples.cfm?pgid=full1",        # full nipples QF50-200-N / -NL
    "hardware_kf_centeringrings.cfm?pgid=ss",    # QF50-200-SRV
    "hardware_kf_centeringrings.cfm?pgid=al",    # QF50-200-ARV
    "hardware_kf_centeringrings.cfm?pgid=outerring-oring",  # QF50-200-SCV (captured O-ring, outer ring)
    "hardware_kf_orings.cfm?pgid=0",             # O-V330, O-S330, O-K330
    "hardware_over_pressure_rings.cfm?pgid=0",   # QF50-200-OPR
    "hardware-kf-wingnut-clamp-ss.cfm?pgid=0",   # QF50-200-SSC
    "hardware_kf_clamps_machined.cfm?pgid=al2",  # QF50-200-C (cast Al)
    "hardware_kf_clamps_chain.cfm?pgid=al",      # QF50-200-CCL
    "hardware-kf-toggle-clamp.cfm?pgid=0",       # QF50-200-TCL
    "https://www.lesker.com/newweb/valves/rough-vacuum-ball-valves.cfm?pgid=manual",  # BVR0200MVQF
]
MDC = "https://www.mdcprecision.com/parts/"
MDC_PARTS = [
    "half-nipple-nw50-short-weld-stub-w2tube", "iso-kf-flange-nw50-2-weld", "iso-kf-flange-nw50-blank",
    "nipple-nw50-w2-tube", "hinged-clamp-nw50-1-per-pack",
    "centering-ring-standard-nw50-dn50kf-fkm-elastomer-stainless-steel-1-per-pack-includes-one-elastomer-gasket-seal",
    "centering-ring-standard-nw50-dn50kf-fkm-elastomer-aluminum-eumetric-pn-7710016",
    "centering-ring-standard-nw50-dn50kf-silicone-stainless-steel-eumetric-pn-7710024",
    "o-ring-replacement-iso-kf-kwik-flange-nw50-fkm-elastomer", "o-ring-replacement-iso-kf-kwik-flange-nw50-silicone",
]


def lesker():
    for p in LESKER_PAGES:
        url = p if p.startswith("http") else LESKER + p
        s = BeautifulSoup(requests.get(url, headers=UA, timeout=40).text, "lxml")
        for tab in s.find_all("table"):
            if not tab.find(attrs={"data-partno": True}):
                continue
            rows = tab.find_all("tr")
            head = [c.get_text(" ", strip=True) for c in rows[0].find_all(["th", "td"])]
            for tr in rows[1:]:
                cells = [re.sub(r"\s+", " ", c.get_text(" ")).strip() for c in tr.find_all(["th", "td"])]
                if len(cells) == len(head) and re.search(r"KF ?50 \(2\.95", " ".join(cells)):
                    d = dict(zip(head, cells))
                    keep = {k: v for k, v in d.items() if v and k not in ("More Info", "Drawing", "VacuCAD SM", "Add To Cart", "Accessories")}
                    print("Lesker", url.split("/")[-1], "|", " | ".join(f"{k}: {v}" for k, v in keep.items()))
            break  # first table is in inches; the second repeats it in mm


def mdc():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True)
        pg = b.new_page(user_agent=UA["User-Agent"])
        for slug in MDC_PARTS:
            pg.goto(MDC + slug, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)
            t = pg.inner_text("body")
            pn = re.search(r"Part Number: (\S+)", t)
            ref = re.search(r"Reference: (\S+)", t)
            price = re.search(r"Price: (\$[\d,.]+ / \w+)", t)
            avail = re.search(r"(Available[^\n]*|Out of stock[^\n]*|Available to Quote)", t)
            print("MDC", pn and pn.group(1), ref and ref.group(1), price and price.group(1), "|", avail and avail.group(1), "|", slug)
        b.close()


if __name__ == "__main__":
    print(subprocess.run(["date", "-u", "+%FT%H:%MZ"], capture_output=True, text=True).stdout.strip())
    lesker()
    if "--lesker" not in sys.argv:
        mdc()
