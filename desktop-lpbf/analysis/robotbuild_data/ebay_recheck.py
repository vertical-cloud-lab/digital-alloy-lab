"""Re-read the used picks' eBay item pages (2026-11-25): still listed, price, estimated delivery to Provo, returns.

eBay serves its error page to automated navigation, so (as in PR 270's sourcing/scripts) the URL is typed into a headed
Chrome's address bar with xdotool and the page text is read over raw CDP (Runtime.evaluate only). Chrome runs on its own
virtual display, its traffic through the lab Pi's SOCKS tunnel (BYU network, so delivery estimates are for Provo).
Nothing is clicked, no account is used and no seller is contacted. Page text is untrusted data.

    Xvfb :95 -screen 0 1280x900x24 &
    DISPLAY=:95 google-chrome --proxy-server=socks5://127.0.0.1:1081 --user-data-dir=/tmp/data-chrome-ebay \
        --remote-debugging-port=9333 --no-first-run --window-size=1280,900 about:blank &
    /tmp/venv/bin/python desktop-lpbf/analysis/robotbuild_data/ebay_recheck.py <out.json> <item-id> ...
"""
from __future__ import annotations

import datetime as dt
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.request

import websocket

DISPLAY = os.environ.get("EBAY_DISPLAY", ":95")
PORT = int(os.environ.get("EBAY_CDP_PORT", "9333"))
JS = r"""() => {
  const t = s => { const e = document.querySelector(s); return e ? e.innerText.trim() : null; };
  const body = (document.body.innerText || '');
  const grab = re => { const m = body.match(re); return m ? m[0].slice(0, 300) : null; };
  return {title_tag: document.title, url: location.href, h1: t('h1'),
          price: t('.x-price-primary') || t('[data-testid="x-price-primary"]'),
          condition: t('.x-item-condition-text') || t('[data-testid="x-item-condition"]'),
          delivery: grab(/(Estimated delivery|Delivery)[^\n]{0,200}/),
          shipping: grab(/Shipping:?[^\n]{0,200}/),
          returns: grab(/Returns:?[^\n]{0,200}/),
          located: grab(/Located in:?[^\n]{0,120}/),
          ended: grab(/(This listing (was ended|has ended|sold)|no longer available|Bidding has ended|The item you selected is unavailable)[^\n]{0,200}/),
          available: grab(/\d+ available[^\n]{0,80}/), sold: grab(/\d+ sold[^\n]{0,40}/),
          body: body.slice(0, 6000)};
}"""


def x(*args):
    subprocess.run(["xdotool", *args], env=dict(os.environ, DISPLAY=DISPLAY), check=False)


def nav(url, wait):
    wid = subprocess.run(["xdotool", "search", "--onlyvisible", "--class", "google-chrome"], capture_output=True,
                         text=True, env=dict(os.environ, DISPLAY=DISPLAY)).stdout.split()
    if wid:
        x("windowactivate", "--sync", wid[0])
    x("mousemove", "--sync", str(500 + random.randint(0, 200)), str(350 + random.randint(0, 200)))
    x("key", "--clearmodifiers", "ctrl+l")
    time.sleep(0.4)
    p = subprocess.Popen(["xdotool", "type", "--delay", "25", "--file", "-"], stdin=subprocess.PIPE,
                         env=dict(os.environ, DISPLAY=DISPLAY))
    p.communicate(url.encode())
    x("key", "Return")
    time.sleep(wait)
    for _ in range(3):
        x("click", "5")
        time.sleep(random.uniform(0.2, 0.6))


def read():
    tabs = [t for t in json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list")) if t.get("type") == "page"]
    ws = websocket.create_connection(tabs[0]["webSocketDebuggerUrl"], timeout=60, suppress_origin=True)
    ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                        "params": {"expression": f"({JS})()", "returnByValue": True, "awaitPromise": True}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == 1:
            break
    ws.close()
    return m.get("result", {}).get("result", {}).get("value") or {}


def main():
    out = sys.argv[1]
    res = {}
    for iid in sys.argv[2:]:
        nav(f"https://www.ebay.com/itm/{iid}", random.uniform(7, 9))
        d = read()
        d["fetched_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        res[iid] = d
        print(iid, "|", (d.get("title_tag") or "")[:60], "|", d.get("price"), "|", (d.get("delivery") or "")[:80], "|",
              (d.get("ended") or "")[:60], flush=True)
        json.dump(res, open(out, "w"), indent=1)
        time.sleep(random.uniform(3, 6))


if __name__ == "__main__":
    main()
