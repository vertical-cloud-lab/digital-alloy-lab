"""Re-fetch the main KF-50 price pages and print the price lines.

usage: python bom/fetch_kf_mcmaster.py
McMaster: renders each part page with fetch_render.py (headless Chrome through the SOCKS tunnel on 127.0.0.1:1080).
Duniway: plain GET through the same tunnel (requests[socks]).
A&N (ancorp.com) sits behind a JS challenge and Ideal Vacuum/Agilent return 403, so they are not scripted here.
"""
import html, re, subprocess, sys
from pathlib import Path
import requests

MC_PARTS = ["4518K38", "4518K43", "4518K877", "4518K878", "4518K61", "4518K65", "5777N15", "4518K771",
            "4518K69", "4518K74", "4518K78", "4518K968", "4518K895", "5786N27", "3634N1"]
DU_URL = "https://www.duniway.com/catalog/hardware/kf%C2%AE-flangesfittings"
PROXY = {"http": "socks5h://127.0.0.1:1080", "https": "socks5h://127.0.0.1:1080"}
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

def mcmaster(part):
    out = subprocess.run([sys.executable, str(Path(__file__).with_name("fetch_render.py")), f"https://www.mcmaster.com/{part}/", "--wait", "7"],
                         capture_output=True, text=True, timeout=180).stdout
    title = re.search(r"^TITLE: (.*)$", out, re.M)
    price = re.search(r"\$[\d,]+\.\d\d each", out)
    ship = re.search(r"Delivers [^\n]+", out)
    pres = re.search(r"Maximum Pressure @ Temperature\s*\n\s*([^\n]*\S)", out)
    print(f"{part}\t{price.group(0) if price else 'no price'}\t{ship.group(0) if ship else ''}\t"
          f"pressure: {pres.group(1) if pres else '-'}\t{title.group(1)[:90] if title else ''}", flush=True)

def duniway():
    h = requests.get(DU_URL, proxies=PROXY, headers={"User-Agent": UA}, timeout=60).text
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    t = re.sub(r"(\|\s*)+", "|", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "|", h)))
    for m in re.finditer(r"\|(KF50-[A-Z0-9/]+)\|([^|]+)\|(\$[\d,.]+|INQUIRE)", t):
        print("\t".join(html.unescape(x).strip() for x in m.groups()))

if __name__ == "__main__":
    for p in MC_PARTS:
        mcmaster(p)
    duniway()
