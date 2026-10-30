#!/usr/bin/env python3
"""Export a part from a public Onshape document through the viewer's own Export dialog.

    pip install playwright   # uses the system Chrome; or `playwright install chromium` and drop CHROME
    python export_from_viewer.py URL OUTDIR STL    # binary STL, millimetres, "Fine"
    python export_from_viewer.py URL OUTDIR STEP   # STEP AP242, millimetres

URL is the Part Studio's link. Run once per Part Studio, as the part is found by its name in the
parts list ("Part 1").

Why this route: this repo has no Onshape API key. Anonymously, the REST API returns the
document, its element list and each Part Studio's feature list, but answers 401 to
everything that touches geometry (glTF, STL, tessellation, mass properties, translations).
The link share's permission set does include EXPORT, and the viewer's own Export dialog works
without signing in. So this opens the viewer in headless Chrome, right-clicks the part,
fills in the dialog and saves the download.
"""
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME = "/usr/bin/google-chrome"
PART = "Part 1"


def main() -> None:
    url, out, fmt = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True,
                                    args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        page = browser.new_context(viewport={"width": 1600, "height": 1000}, accept_downloads=True).new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=90_000)
        part = page.get_by_text(PART, exact=True).first
        part.wait_for(state="visible", timeout=90_000)
        time.sleep(8)  # let the model load before opening the menu
        part.click(button="right")
        time.sleep(2)
        items = page.get_by_text(re.compile(r"^\s*Export"))  # the first match is a hidden "Export tab…"
        next(items.nth(i) for i in range(items.count()) if items.nth(i).is_visible()).click()
        page.locator("#export-format-dropdown").select_option(label=fmt)
        time.sleep(2)
        if fmt == "STL":
            page.locator("select[ng-model='exportMode']:visible").select_option(label="Binary")
            page.locator("select[ng-model='currentUnits.length']:visible").select_option(label="Millimeter")
            page.locator("select[ng-model='exportResolution']:visible").first.select_option(label="Fine")
        elif fmt == "STEP":
            units = page.locator("#custom-step-units-checkbox")
            if units.is_visible() and not units.is_checked():
                units.check()
                page.locator("select[ng-model='options.stepExportUnit']:visible").select_option(label="Millimeter")
        page.locator("#export-options-dropdown").select_option(label="Download")
        with page.expect_download(timeout=180_000) as dl:
            page.locator("button.btn-primary[type=submit]:visible").click()
        dest = out / dl.value.suggested_filename
        dl.value.save_as(dest)
        print(dest, dest.stat().st_size, "bytes")
        browser.close()


if __name__ == "__main__":
    main()
