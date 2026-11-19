"""Open eBay item pages in the headed Chrome (typed URL via xdotool), extract over raw CDP, then fetch the
seller description iframe through the Pi tunnel with curl. usage: items.py OUTDIR ITEM_ID ..."""
import json, pathlib, random, subprocess, sys, time, datetime
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
here = pathlib.Path(__file__).parent
for iid in sys.argv[2:]:
    dest = out / f"{iid}.json"
    if dest.exists(): continue
    subprocess.run([str(here / "xnav.sh"), f"https://www.ebay.com/itm/{iid}", str(round(random.uniform(6, 8), 1))])
    r = subprocess.run([sys.executable, "-P", str(here / "cdp_eval.py"), str(here / "item_extract.js")], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except Exception as e:
        print(iid, "ERR", e, r.stderr[:200], flush=True); continue
    d["fetched_utc"] = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%MZ")
    if d.get("desc_src"):
        c = subprocess.run(["curl", "-s", "--max-time", "30", "--socks5-hostname", "127.0.0.1:1080", "-A",
                            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36",
                            d["desc_src"]], capture_output=True, text=True)
        import re, html
        t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", c.stdout)
        t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))
        d["description"] = re.sub(r"\s+", " ", t).strip()[:6000]
    dest.write_text(json.dumps(d, indent=1))
    print(iid, "|", d.get("title_tag", "")[:70], "|", d.get("price"), "|", d.get("condition"), "| desc", len(d.get("description", "") or ""), flush=True)
    time.sleep(random.uniform(2, 5))
