#!/usr/bin/env python3
"""Compare regenerated orchid-bench PDFs/PNGs with the shipped ones beyond sha256: page text and 72-dpi renders."""
import json
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image

S = Path("/tmp/arroyave/src/orchid-calphad__orchid-bench/bench/docs")
W = Path("/tmp/arroyave/work/orchid-bench/bench/docs")
rows = []
for d in sorted(p.name for p in S.iterdir() if p.is_dir()):
    for f in ("vector.pdf", "image_only.pdf"):
        a, b = pymupdf.open(S / d / f), pymupdf.open(W / d / f)
        same_text = a.page_count == b.page_count and all(a[i].get_text() == b[i].get_text() for i in range(a.page_count))
        maxpix = 0
        for i in range(min(a.page_count, b.page_count)):
            pa, pb = a[i].get_pixmap(dpi=72), b[i].get_pixmap(dpi=72)
            xa = np.frombuffer(pa.samples, dtype=np.uint8).astype(int)
            xb = np.frombuffer(pb.samples, dtype=np.uint8).astype(int)
            maxpix = max(maxpix, int(np.abs(xa - xb).max()) if xa.shape == xb.shape else 999)
        ra, rb = (S / d / f).read_bytes(), (W / d / f).read_bytes()
        rows.append({"doc": d, "file": f, "pages": a.page_count, "same_text": same_text, "max_pixel_diff_72dpi": maxpix,
                     "size_shipped": len(ra), "size_regen": len(rb)})
png = "syn-CuZn-08Gie-v0/clean/page-4.png"
xa = np.asarray(Image.open(S / png)).astype(int); xb = np.asarray(Image.open(W / png)).astype(int)
res = {"pdfs": rows, "png_" + png: {"shape_equal": xa.shape == xb.shape,
                                    "n_pixels_differing": int((np.abs(xa - xb).reshape(xa.shape[0], xa.shape[1], -1).max(-1) > 0).sum()) if xa.shape == xb.shape else None,
                                    "max_abs_diff": int(np.abs(xa - xb).max()) if xa.shape == xb.shape else None}}
Path("/tmp/arroyave/results/orchid/data/orchid-bench-generate-pdfcompare.json").write_text(json.dumps(res, indent=1) + "\n")
print("pdfs:", len(rows), "same text:", sum(r["same_text"] for r in rows), "pixel-identical @72dpi:",
      sum(r["max_pixel_diff_72dpi"] == 0 for r in rows), "max pixel diff:", max(r["max_pixel_diff_72dpi"] for r in rows))
print("size deltas:", sorted({r["size_regen"] - r["size_shipped"] for r in rows})[:10])
print(res["png_" + png])
