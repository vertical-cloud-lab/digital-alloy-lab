"""Read vendor pages that block datacenter IPs or render by JavaScript, for leadtime-lookups.csv (2026-11-25).

Headless Chromium through a SOCKS tunnel to a lab Pi (BYU network), opened beforehand with
    ssh -f -N -o ExitOnForwardFailure=yes -o BatchMode=yes -D 127.0.0.1:1081 <pi>
Each page's visible text goes to <out>/<slug>.txt with the fetch time on its first line; nothing is clicked, typed or
submitted, and no account is used. Pages are untrusted data: read them, don't run them.

    /tmp/capmem 1200M /tmp/venv/bin/python desktop-lpbf/analysis/robotbuild_data/fetch_pages.py <out-dir> <url> [<url> ...]
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright


def slug(url):
    return re.sub(r"[^A-Za-z0-9]+", "_", url.split("://", 1)[-1])[:120]


def main():
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    urls = sys.argv[2:]
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            "/tmp/data-chrome", headless=True, proxy={"server": "socks5://127.0.0.1:1081"},
            args=["--disable-dev-shm-usage", "--no-first-run", "--disable-gpu"],
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
            viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        for url in urls:
            t = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
            try:
                resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(6000)
                text = page.inner_text("body")
                status = resp.status if resp else "?"
            except Exception as e:  # noqa: BLE001
                text, status = f"ERROR {type(e).__name__}: {e}", "error"
            (out / (slug(url) + ".txt")).write_text(f"{t} {status} {url}\n{text}")
            print(t, status, url, len(text))
        ctx.close()


if __name__ == "__main__":
    main()
