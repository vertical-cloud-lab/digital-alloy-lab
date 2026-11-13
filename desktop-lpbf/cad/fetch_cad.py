"""Fetch vendor CAD (McMaster native CAD download; Thorlabs 'CAD PDF' drawings) through the lab-Pi tunnel.
Usage: python cadbatch.py OUTDIR MANIFEST.csv mcm:PN ... tl:PN ...
Files are saved to OUTDIR (keep it outside the repo); the manifest records source URL, size and sha256."""
import sys, time, pathlib, hashlib, csv, datetime
from playwright.sync_api import sync_playwright
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rows = []
def rec(vendor, pn, kind, url, path):
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    rows.append([vendor, pn, kind, path.name, path.stat().st_size, h, url, datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%MZ")])
    print(vendor, pn, kind, path.name, path.stat().st_size)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True, proxy={"server": "socks5://127.0.0.1:1080"}, args=["--disable-blink-features=AutomationControlled"])
    ctx = b.new_context(accept_downloads=True, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
    for spec in sys.argv[3:]:
        kind, pn = spec.split(":", 1)
        pg = ctx.new_page()
        try:
            if kind == "mcm":
                pg.goto(f"https://www.mcmaster.com/{pn}/", wait_until="domcontentloaded", timeout=45000)
                try: pg.wait_for_load_state("networkidle", timeout=15000)
                except Exception: pass
                with pg.expect_download(timeout=30000) as dl:
                    pg.get_by_text("Download", exact=True).first.click()
                d = dl.value; dest = out / d.suggested_filename; d.save_as(dest)
                rec("McMaster-Carr", pn, "native CAD (SolidWorks part; Onshape imports it)", d.url.split("?")[0], dest)
            else:
                pg.goto(f"https://www.thorlabs.com/item/{pn}", wait_until="domcontentloaded", timeout=45000)
                try: pg.wait_for_load_state("networkidle", timeout=15000)
                except Exception: pass
                with ctx.expect_page(timeout=20000) as newp:
                    pg.get_by_text("CAD PDF", exact=True).first.click()
                url = newp.value.url; newp.value.close()
                r = ctx.request.get(url, timeout=30000)
                dest = out / (pn.replace("/", "_") + "_" + url.split("/")[-1].split("?")[0]); dest.write_bytes(r.body())
                rec("Thorlabs", pn, "dimensioned drawing (PDF)", url.split("?")[0], dest)
        except Exception as e:
            print(spec, "FAIL", type(e).__name__, str(e).splitlines()[0][:120])
        finally:
            pg.close()
    b.close()
with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f); w.writerow(["vendor", "part_number", "kind", "file", "bytes", "sha256", "source_url", "fetched_utc"]); w.writerows(rows)
