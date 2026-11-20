"""Render vendor pages in Chrome through a SOCKS tunnel (ssh -D 127.0.0.1:1080 to a lab Pi) and save their visible text.
Usage: python fetch.py OUTDIR slug=url [slug=url ...]
"""
import sys, pathlib, time
from playwright.sync_api import sync_playwright

outdir = pathlib.Path(sys.argv[1]); outdir.mkdir(parents=True, exist_ok=True)
pairs = [a.split("=", 1) for a in sys.argv[2:]]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
                          proxy={"server": "socks5://127.0.0.1:1080"},
                          args=["--disable-blink-features=AutomationControlled"])
    ctx = b.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
                        viewport={"width": 1600, "height": 2400}, locale="en-US")
    for slug, url in pairs:
        page = ctx.new_page()
        try:
            r = page.goto(url, wait_until="domcontentloaded", timeout=45000)
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            time.sleep(2)
            txt = page.evaluate("document.body ? document.body.innerText : ''")
            (outdir / f"{slug}.txt").write_text(f"URL: {url}\nFINAL: {page.url}\nSTATUS: {r.status if r else None}\n\n{txt}")
            print(slug, r.status if r else None, len(txt))
        except Exception as e:
            print(slug, "ERR", type(e).__name__, str(e)[:120])
        finally:
            page.close()
    b.close()
