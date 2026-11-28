"""SendCutSend instant quote, step by step, in headed Chrome through the lab's SOCKS tunnel (no account, nothing typed, nothing
put in a cart): upload one DXF, then do the given steps in order, saving a screenshot and the page text after each.
Steps: a visible text to click; "xy:X,Y" to click a point of the 1600 x 1200 window; "hover:X,Y"; "wait:N"; "shot".
Usage: xvfb-run -a /tmp/venv/bin/python scs_quote.py OUTDIR file.dxf STEP ...
The run of 2026-11-25 (prices in analysis/out/monitoring/fab/quotes/sendcutsend_quotes.csv) used, for 6061-T6 1/4 in.:
  "xy:1003,631" (the MM units button) "xy:1530,1162" (CONFIRM) "wait:4" "Metals" "Aluminum" "6061 T6 Aluminum"
  '.250" (6.3 MM)' "wait:8"      and '.187" (4.7 MM)' for 3/16 in.; the price shows after the thickness.
The run of 2026-11-27 used the same steps (the page had not moved), then "hover:1302,634" (1/4 in.) or "hover:1302,558"
(3/16 in.) over the thickness's warning icon to read its tooltip."""
import pathlib
import sys
import time

from playwright.sync_api import sync_playwright

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
f = sys.argv[2]
steps = sys.argv[3:]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=False,
                          proxy={"server": "socks5://127.0.0.1:1080"},
                          args=["--disable-blink-features=AutomationControlled", "--window-size=1600,1200"])
    ctx = b.new_context(viewport={"width": 1600, "height": 1200}, locale="en-US",
                        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
    page = ctx.new_page()
    page.goto("https://app.sendcutsend.com/customer#/quote", wait_until="domcontentloaded", timeout=60000)
    time.sleep(8)
    page.query_selector_all("input[type=file]")[0].set_input_files([f])
    time.sleep(12)
    for i, st in enumerate(steps):
        try:
            if st.startswith("wait:"):
                time.sleep(float(st[5:]))
            elif st == "shot":
                pass
            elif st.startswith("xy:"):
                x, y = (float(v) for v in st[3:].split(","))
                page.mouse.click(x, y)
            elif st.startswith("hover:"):   # e.g. over a thickness's warning icon, to read its tooltip
                x, y = (float(v) for v in st[6:].split(","))
                page.mouse.move(x, y)
            elif st.startswith("css:"):
                page.locator(st[4:]).first.click(timeout=15000)
            else:
                page.get_by_text(st, exact=True).first.click(timeout=15000)
            time.sleep(4)
        except Exception as e:  # noqa: BLE001
            print("step", i, st, "failed:", type(e).__name__, str(e)[:160])
        page.screenshot(path=str(out / f"s{i:02d}.png"))
        (out / f"s{i:02d}.txt").write_text(page.evaluate("document.body ? document.body.innerText : ''"))
        print("step", i, st, "ok")
    b.close()
