"""Render one page in headless Chrome and print its visible text (used by the other fetch_*.py scripts).

    python bom/fetch_render.py URL [--direct] [--wait S] [--html OUT.html]

By default it goes out through a SOCKS proxy on 127.0.0.1:1080 (an SSH tunnel to a lab machine), because
some vendors (McMaster-Carr, Technical Glass Products) block datacenter IPs; --direct skips the proxy.
Needs `pip install playwright`; uses the system Chrome if there is one, else `playwright install chromium`.
"""
import argparse
import os
import sys
import time

from playwright.sync_api import sync_playwright

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--direct", action="store_true")
    ap.add_argument("--wait", type=float, default=6.0)
    ap.add_argument("--html")
    a = ap.parse_args()
    with sync_playwright() as p:
        kw = dict(headless=True, args=["--disable-blink-features=AutomationControlled"])
        if os.path.exists("/usr/bin/google-chrome"):
            kw["executable_path"] = "/usr/bin/google-chrome"
        if not a.direct:
            kw["proxy"] = {"server": "socks5://127.0.0.1:1080"}
        b = p.chromium.launch(**kw)
        pg = b.new_context(user_agent=UA, viewport={"width": 1400, "height": 1000}, locale="en-US").new_page()
        try:
            pg.goto(a.url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:  # noqa: BLE001 - print and still dump what loaded
            print("GOTO-ERROR", e, file=sys.stderr)
        time.sleep(a.wait)
        try:
            pg.wait_for_load_state("networkidle", timeout=15000)
        except Exception:  # noqa: BLE001
            pass
        if a.html:
            open(a.html, "w").write(pg.content())
        print("URL:", pg.url)
        print("TITLE:", pg.title())
        print(pg.inner_text("body"))
        b.close()


if __name__ == "__main__":
    main()
