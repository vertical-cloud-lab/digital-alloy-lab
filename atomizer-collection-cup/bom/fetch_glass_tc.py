"""Re-fetch the main glass / seal / thermocouple / meter / leak-fluid pages and print the price lines.

usage: python bom/fetch_glass_tc.py   (playwright + the SOCKS tunnel on 127.0.0.1:1080)
Shells out to fetch_render.py next to this file; TGP's paged table is read with Playwright directly.
"""
import os, re, subprocess, sys, time
from pathlib import Path

RENDER = [sys.executable, str(Path(__file__).with_name("fetch_render.py"))]
PAGES = [  # (url, regex for the lines worth printing)
    ("https://mtixtl.com/products/qztube-100d-650", r"Regular price|\$\d|stock"),
    ("https://mtixtl.com/products/hqt100", r"Regular price|\$\d|stock"),
    ("https://www.waleapparatus.com/product/clear-fused-quartz-tubing", r"CFQ(9\d|10\d)X"),
    ("https://www.waleapparatus.com/product/heavy-wall-corning-pyrex-glass-tubing", r"BH-400C"),
    ("https://www.waleapparatus.com/product/standard-wall-corning-pyrex-glass-tubing", r"BS-100C"),
    ("https://www.mcmaster.com/products/borosilicate-glass-tubing/", r"1176K29"),
    ("https://www.mcmaster.com/products/o-ring-cord/chemical-resistant-viton-fluoroelastomer-cord-stock~~/", r"96515K1(29|31)|94245K63[245]"),
    ("https://www.mcmaster.com/products/o-ring-cord/high-temperature-silicone-cord-stock~~/", r"96505K(24|106)|1187N(18|21)"),
    ("https://www.mcmaster.com/products/o-rings/dash-number~344/", r"9464K466"),
    ("https://www.mcmaster.com/products/o-rings/dash-number~345/", r"9464K467"),
    ("https://www.mcmaster.com/products/silicone-o-rings/high-temperature-silicone-o-rings~~/dash-number~344/", r"9186N363|\$\d"),
    ("https://www.mcmaster.com/products/viton-rubber-sheets/", r"86075K(24|34)"),
    ("https://www.globaloring.com/shop/?filter_group=o-rings&size=344&filter_material=viton-fkm&qs_unit=inch", r"V75344\s"),
    ("https://www.globaloring.com/shop/?filter_group=o-rings&size=344&filter_material=silicone&qs_unit=inch", r"S70344\s"),
    ("https://www.auberins.com/index.php?main_page=product_info&cPath=20_3&products_id=307", r"Starting at|temperature|insulation"),
    ("https://www.auberins.com/index.php?main_page=product_info&cPath=17&products_id=587", r"Starting at"),
    ("https://www.dwyeromega.com/en-us/heavy-duty-bolt-on-thermocouple-with-ss-washer-housing-armor-cable/WT-HD/p/WTK-HD-72-S", r"/ each|Process Temperature|In Stock"),
    ("https://www.mcmaster.com/products/pipe-clamp-thermocouples/high-temperature-thermocouples-for-air-and-surfaces~~/", r"3859K44"),
    ("https://www.mcmaster.com/products/pipe-clamp-thermocouples/thermocouples-for-pipe-tube-and-hose~~/", r"37045K532"),
    ("https://www.mcmaster.com/products/worm-drive-hose-clamps/worm-drive-clamps~~/", r"5415K(18|23)|5413K(57|62)"),
    ("https://www.mcmaster.com/products/panel-mount-buzzers/", r"56965T2[36]"),
    ("https://www.keepsupply.com/ms-snoop-8oz-swagelok-snoop-liquid-leak-detector-8-oz-236-ml-bottle", r"Web Price|\$\d|Stock"),
    ("https://trutechtools.com/Big-Blu-Brush-on-Microleak-Detector", r"PRICE|MSRP|In Stock"),
    ("https://www.mcmaster.com/products/leak-detectors/gas-leak-detectors-2~/", r"10875T22|1012T22"),
]


def tgp_rows():
    """TGP tubing table is paged client-side: show 100 rows/page, walk pages, keep ~100 mm OD rows."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None, headless=True,
                              args=["--disable-blink-features=AutomationControlled"],
                              proxy={"server": "socks5://127.0.0.1:1080"})
        ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        pg = b.new_context(user_agent=ua, viewport={"width": 1400, "height": 1000}).new_page()
        pg.goto("https://technicalglass.com/product-pages/fused-quartz-tubing/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)
        for _ in range(3):
            pg.mouse.wheel(0, 3000); time.sleep(0.8)
        for s in pg.query_selector_all("select"):
            if "100" in [o.get_attribute("value") for o in s.query_selector_all("option")]:
                s.select_option("100"); time.sleep(2); break
        for _ in range(5):
            for line in "\n".join(t.inner_text() for t in pg.query_selector_all("table")).splitlines():
                if re.match(r"^(8[5-9]|9\d|10\d)(\.\d+)?x", line):
                    print("  ", line)
            nxt = pg.query_selector("a.paginate_button.next:not(.disabled), button.dt-paging-button.next:not(.disabled)")
            if not nxt:
                break
            nxt.click(); time.sleep(2.5)
        b.close()


if __name__ == "__main__":
    print("== https://technicalglass.com/product-pages/fused-quartz-tubing/")
    try:
        tgp_rows()
    except Exception as e:
        print("   TGP error:", e)
    for url, pat in PAGES:
        print("==", url)
        try:
            out = subprocess.run(RENDER + [url, "--wait", "8"], capture_output=True, text=True, timeout=150).stdout
        except subprocess.TimeoutExpired:
            print("   timeout"); continue
        hits = [l.strip() for l in out.splitlines() if re.search(pat, l)]
        print("\n".join("   " + h[:220] for h in hits[:8]) or "   (no match - page changed or blocked)")
    sys.exit(0)
