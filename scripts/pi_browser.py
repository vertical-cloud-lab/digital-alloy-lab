"""Drive the headed Chromium on the atomizer panel Pi for web lookups that block cloud runners.

The Pi's Chromium serves DevTools on its own 127.0.0.1:9222 (launch command in CLAUDE.md). Tunnel to it
first, then run this on the runner:

    ssh -f -N -o ExitOnForwardFailure=yes -L 9222:127.0.0.1:9222 "$PANEL_CAM_USERNAME@$PANEL_CAM_HOSTNAME"
    python scripts/pi_browser.py ebay "harris 9296" "9296-250-580"
    python scripts/pi_browser.py page https://weldingmart.com/products/...

Everything goes through a bare DevTools connection that sends only real input events: eased mouse
paths, clicks, per-key typing and wheel scrolls. It never calls Runtime.enable. Attached with
Playwright's connect_over_cdp, eBay served its "Something went wrong on our end" page on the first
search, but this approach got through. Images, fonts and video are blocked in the tab, because eBay
item pages with photos pushed the 1 GB Pi into swap and crashed Chromium. Results go to
/tmp/pi_browser/*.json and screenshots to /tmp/pi_browser/*.png.
"""

import base64
import json
import math
import os
import random
import re
import sys
import time
import urllib.request

import websocket  # pip install websocket-client

BASE = os.environ.get("PI_CDP", "http://127.0.0.1:9222")
OUT = "/tmp/pi_browser"
BLOCK = ("jpg", "jpeg", "png", "webp", "gif", "avif", "svg", "woff", "woff2", "ttf", "mp4", "webm")


def _http(path, method="GET"):
    with urllib.request.urlopen(urllib.request.Request(BASE + path, method=method), timeout=60) as r:
        body = r.read().decode()
    try:
        return json.loads(body)
    except ValueError:  # /json/activate and /json/close answer in plain text
        return body


def pause(a=0.3, b=0.9):
    time.sleep(random.uniform(a, b))


class Tab:
    """A new tab in the Pi's browser window, closed again on exit."""

    def __enter__(self):
        t = _http("/json/new?about:blank", "PUT")
        self.id, self.n = t["id"], 0
        _http(f"/json/activate/{self.id}")
        self.ws = websocket.create_connection(t["webSocketDebuggerUrl"], timeout=180, suppress_origin=True)
        self.call("Network.enable", maxTotalBufferSize=1_000_000, maxResourceBufferSize=200_000)
        self.call("Network.setBlockedURLs", urls=[f"*.{e}*" for e in BLOCK])
        self.x, self.y = random.uniform(300, 900), random.uniform(200, 600)
        return self

    def __exit__(self, *exc):
        try:
            self.ws.close()
        finally:
            _http(f"/json/close/{self.id}")

    def call(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def js(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"].get("text"))
        return r["result"].get("value")

    def wait_loaded(self, timeout=90, settle=(2.5, 4.0)):
        """Wait for a new document (the old one is marked first) to finish parsing."""
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                if self.js("window.__oldDoc === undefined && document.readyState !== 'loading'"):
                    break
            except Exception:
                pass
            time.sleep(0.7)
        pause(*settle)

    def goto(self, url):
        self.js("window.__oldDoc = 1")
        self.call("Page.navigate", url=url)
        self.wait_loaded()

    def move(self, x, y):
        """Move the pointer along an eased quadratic curve, like a hand would."""
        x0, y0 = self.x, self.y
        d = math.hypot(x - x0, y - y0)
        n = max(10, int(d / 22))
        cx = (x0 + x) / 2 + random.uniform(-0.25, 0.25) * d
        cy = (y0 + y) / 2 + random.uniform(-0.25, 0.25) * d
        for i in range(1, n + 1):
            t = i / n
            t = t * t * (3 - 2 * t)
            self.call("Input.dispatchMouseEvent", type="mouseMoved",
                      x=(1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x,
                      y=(1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y)
            time.sleep(random.uniform(0.004, 0.018))
        self.x, self.y = x, y

    def wander(self, k=2):
        for _ in range(k):
            self.move(random.uniform(200, 1100), random.uniform(150, 750))
            pause(0.1, 0.4)

    def click(self, sel, timeout=90):
        t0 = time.time()
        while time.time() - t0 < timeout:
            box = self.js(f"""(() => {{ const e = document.querySelector({json.dumps(sel)}); if (!e) return null;
                e.scrollIntoView({{block: 'center'}}); const r = e.getBoundingClientRect();
                return (r.width && r.height) ? [r.x, r.y, r.width, r.height] : null; }})()""")
            if box:
                break
            time.sleep(0.8)
        else:
            raise RuntimeError(f"nothing visible for {sel}")
        pause(0.2, 0.5)
        x = box[0] + box[2] * random.uniform(0.3, 0.7)
        y = box[1] + box[3] * random.uniform(0.35, 0.65)
        self.move(x, y)
        pause(0.08, 0.25)
        for typ in ("mousePressed", "mouseReleased"):
            self.call("Input.dispatchMouseEvent", type=typ, x=x, y=y, button="left", clickCount=1)
            time.sleep(random.uniform(0.05, 0.12))

    def key(self, key, code, vk, text=None, mods=0):
        kw = dict(key=key, code=code, windowsVirtualKeyCode=vk, nativeVirtualKeyCode=vk, modifiers=mods)
        self.call("Input.dispatchKeyEvent", type="keyDown" if text else "rawKeyDown", **kw,
                  **({"text": text} if text else {}))
        self.call("Input.dispatchKeyEvent", type="keyUp", **kw)

    def type(self, text):
        for ch in text:
            self.call("Input.dispatchKeyEvent", type="keyDown", text=ch, key=ch, unmodifiedText=ch)
            self.call("Input.dispatchKeyEvent", type="keyUp", key=ch)
            time.sleep(random.uniform(0.05, 0.16))

    def scroll(self, total=1400):
        done = 0
        while done < total:
            dy = random.randint(140, 340)
            self.call("Input.dispatchMouseEvent", type="mouseWheel", x=self.x, y=self.y, deltaX=0, deltaY=dy)
            done += dy
            time.sleep(random.uniform(0.12, 0.35))

    def shot(self, name):
        data = self.call("Page.captureScreenshot", format="png")["data"]
        with open(f"{OUT}/{name}.png", "wb") as f:
            f.write(base64.b64decode(data))


EBAY_RESULTS = r"""(() => {
  const items = [];
  for (const li of document.querySelectorAll('ul.srp-results > li, li.s-item, li.s-card')) {
    const a = li.querySelector('a[href*="/itm/"]');
    if (a) items.push({text: li.innerText.replace(/\n{2,}/g, '\n').slice(0, 900), href: a.href.split('?')[0]});
  }
  const h = document.querySelector('.srp-controls__count-heading');
  return {count: h ? h.innerText : null, title: document.title, items};
})()"""


def ebay(tab, query):
    """Type a query into eBay's search box and click Search, as a person would."""
    if "ebay.com" not in (tab.js("location.href") or ""):
        tab.goto("https://www.ebay.com/")
        tab.wander()
    tab.click("input#gh-ac")
    tab.key("a", "KeyA", 65, mods=2)
    tab.key("Backspace", "Backspace", 8)
    tab.type(query)
    pause(0.4, 0.9)
    tab.js("window.__oldDoc = 1")
    tab.click("#gh-search-btn, #gh-btn")
    tab.wait_loaded(settle=(3, 5))
    tab.scroll()
    res = tab.js(EBAY_RESULTS)
    print(f"== {query!r}: {res['count']} ({res['title'][:50]!r})")
    for it in res["items"]:
        line = " | ".join(s.strip() for s in it["text"].split("\n")
                          if s.strip() and s.strip() not in ("Opens in a new window or tab", "derosnopS"))
        if not re.search(r"shop on ebay", line, re.I):
            print(f"  {line[:300]}\n    {it['href']}")
    return res


def page(tab, url):
    tab.goto(url)
    tab.wander(1)
    tab.scroll(700)
    res = tab.js("({title: document.title, url: location.href, text: document.body ? document.body.innerText : ''})")
    print(f"== {res['title'][:90]}\n{res['url']}\n{res['text'][:3000]}")
    return res


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cmd, args = sys.argv[1], sys.argv[2:]
    with Tab() as tab:
        for i, arg in enumerate(args):
            tag = f"{cmd}-{re.sub(r'[^a-z0-9]+', '-', arg.lower()).strip('-')[:60]}"
            res = ebay(tab, arg) if cmd == "ebay" else page(tab, arg)
            with open(f"{OUT}/{tag}.json", "w") as f:
                json.dump(res, f, indent=1)
            tab.shot(tag)
            if i < len(args) - 1:
                pause(3, 6)
