#!/usr/bin/env python3
"""Re-run orchid-bench's text_regex baseline on the vector PDFs only (no Tesseract needed) and compare with the
shipped outputs/text_regex/vector/*.json byte-for-byte. Mirrors baselines/text_regex.py main() for rendering=vector."""
import hashlib
import json
import sys
from pathlib import Path

WORK = Path("/tmp/arroyave/work/orchid-bench/bench")
SRC = Path("/tmp/arroyave/src/orchid-calphad__orchid-bench/bench")
sys.path.insert(0, str(WORK))
import pdfplumber  # noqa: E402
from common import DOCS, TRUTH, load_json, write_json  # noqa: E402
from baselines.text_regex import extract  # noqa: E402

out = Path("/tmp/arroyave/work/bench_scratch/text_regex_vector")
same = n = 0
for tf in sorted(TRUTH.glob("*.json")):
    doc = load_json(tf)["doc_id"]
    with pdfplumber.open(DOCS / doc / "vector.pdf") as pdf:
        txt = "\n".join(p.extract_text() or "" for p in pdf.pages)
    p = out / "vector" / f"{doc}.json"
    write_json(p, {"doc_id": doc, "rendering": "vector", "extractor": "text_regex",
                   "status": {"text": "ran: pdf_text_layer"}, "text_values": extract(txt)})
    n += 1
    same += hashlib.sha256(p.read_bytes()).hexdigest() == hashlib.sha256((SRC / "outputs/text_regex/vector" / f"{doc}.json").read_bytes()).hexdigest()
print(json.dumps({"vector_docs": n, "byte_identical": same}))
