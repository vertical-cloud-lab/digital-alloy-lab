"""Run eBay searches through the headed Chrome: navigate by typed URL (xdotool), extract over raw CDP.
usage: batch.py OUTDIR QUERYFILE   (QUERYFILE lines: query|live or query|sold)"""
import json, pathlib, random, re, subprocess, sys, time, urllib.parse, datetime
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
here = pathlib.Path(__file__).parent
for line in open(sys.argv[2]):
    line = line.strip()
    if not line or line.startswith("#"): continue
    q, mode = line.rsplit("|", 1)
    slug = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")
    dest = out / f"{slug}-{mode}.json"
    if dest.exists(): continue
    params = {"_nkw": q, "_sacat": "0", "_ipg": "120"}
    if mode == "sold": params.update({"LH_Sold": "1", "LH_Complete": "1"})
    url = "https://www.ebay.com/sch/i.html?" + urllib.parse.urlencode(params)
    subprocess.run([str(here / "xnav.sh"), url, str(round(random.uniform(6, 9), 1))], check=False)
    r = subprocess.run([sys.executable, "-P", str(here / "cdp_eval.py"), str(here / "ebay_extract.js")], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        d.update(query=q, mode=mode, search_url=url, fetched_utc=datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%MZ"))
        d["cards"] = [c for c in d["cards"] if c["item_id"] and c["item_id"] != "123456"]
        dest.write_text(json.dumps(d, indent=1))
        n = sum(1 for c in d["cards"] if not c["after_fewer_words"])
        print(f"{q!r} [{mode}] {d['title'][:40]!r} heading={d['heading']!r} exact={n} total={len(d['cards'])}", flush=True)
        if "Error" in d["title"] or "Pardon" in d["title"]:
            print("BLOCKED; stopping", flush=True); break
    except Exception as e:
        print(f"{q!r} [{mode}] ERR {e} {r.stderr[:200]}", flush=True)
    time.sleep(random.uniform(2, 5))
