"""Evaluate a JS expression in the active Chrome tab over raw CDP (Runtime.evaluate only; no Runtime.enable,
no Playwright), print the JSON result. usage: cdp_eval.py JSFILE [OUTFILE]"""
import json, sys, urllib.request, websocket
tabs = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9222/json/list")) if t.get("type") == "page"]
ws = websocket.create_connection(tabs[0]["webSocketDebuggerUrl"], timeout=60, suppress_origin=True)
expr = open(sys.argv[1]).read()
ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": f"({expr})()", "returnByValue": True, "awaitPromise": True}}))
while True:
    m = json.loads(ws.recv())
    if m.get("id") == 1: break
ws.close()
val = m.get("result", {}).get("result", {}).get("value")
s = json.dumps(val, indent=1)
if len(sys.argv) > 2: open(sys.argv[2], "w").write(s)
else: print(s)
