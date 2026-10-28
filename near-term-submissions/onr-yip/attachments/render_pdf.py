"""Render an HTML file to a Letter PDF with 1-inch margins through headless Chromium.

    /tmp/venv/bin/python render_pdf.py src/field10-facilities.html field10-facilities.pdf
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

CSS = """
@page { size: Letter; margin: 1in; }
body { font-family: "Times New Roman", "Liberation Serif", "Nimbus Roman", serif; font-size: 12pt; line-height: 1.25; margin: 0; }
h1 { font-size: 12pt; text-align: center; margin: 0 0 2pt 0; }
p.sub { text-align: center; margin: 0 0 10pt 0; }
h2 { font-size: 12pt; margin: 10pt 0 2pt 0; }
p { margin: 0 0 6pt 0; text-align: justify; }
ul { margin: 0 0 6pt 0; padding-left: 18pt; } li { margin-bottom: 2pt; text-align: justify; }
table { border-collapse: collapse; width: calc(100% - 2pt); font-size: 11pt; margin: 4pt 1pt 8pt 1pt; }  /* collapsed outer borders straddle the box edge; at 100% Chromium clips the right rule */
th, td { border: 0.75pt solid #444; padding: 2pt 4pt; vertical-align: top; }
th { background: #eee; }
tr { break-inside: avoid; page-break-inside: avoid; } thead { display: table-header-group; } td.n, th.n { text-align: right; white-space: nowrap; }
.small { font-size: 10.5pt; }
a { overflow-wrap: anywhere; }
figure { margin: 2pt 0 8pt 0; break-inside: avoid; page-break-inside: avoid; }
figure .row { display: flex; justify-content: center; align-items: flex-end; gap: 6pt; }
figure .row div { text-align: center; }
figure img { display: block; height: var(--h, 1.8in); width: auto; border: 0.5pt solid #888; }
figure .lab { font-size: 10pt; margin-top: 1pt; }
figcaption { font-size: 10.5pt; line-height: 1.2; text-align: justify; margin-top: 3pt; }
"""

def main(src, dst):
    src = Path(src).resolve()
    html = src.read_text()
    if "<style>" not in html:
        html = html.replace("<head>", f"<head><style>{CSS}</style>", 1) if "<head>" in html else f"<html><head><style>{CSS}</style></head><body>{html}</body></html>"
    # Load from a file next to the source so relative image paths (src/img/...) resolve.
    tmp = src.with_name(f".{src.stem}.render.html")
    tmp.write_text(html)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(tmp.as_uri(), wait_until="load")
            pg.pdf(path=dst, format="Letter", margin={"top": "1in", "bottom": "1in", "left": "1in", "right": "1in"},
                   print_background=True, prefer_css_page_size=True)
            b.close()
    finally:
        tmp.unlink(missing_ok=True)
    print("wrote", dst)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
