#!/usr/bin/env python3
"""Per-document orchid-bench scores (from the re-scored outputs) for the Al- and Cu-containing synthetic papers."""
import csv
import json
from pathlib import Path

RS = Path("/tmp/arroyave/work/bench_scratch/rescore")
EXT = ["ai_gemini", "tables_pdfplumber", "camelot_stream", "vector_route", "assessed_pd", "text_regex"]
rows = []
for e in EXT:
    s = json.loads((RS / f"{e}.json").read_text())
    for doc, per in sorted(s["per_document"].items()):
        sysname = doc.split("-")[1]
        if not any(x in sysname for x in ("Al", "Cu")):
            continue
        for rend, d in per.items():
            ir, pdg, tx = d.get("invariant_rows") or {}, d.get("phase_diagram") or {}, d.get("text") or {}
            rows.append({"extractor": e, "doc": doc, "rendering": rend,
                         "inv_rows_matched": ir.get("matched"), "inv_rows_true": ir.get("rows_true"),
                         "pd_boundary_recall@0.01": (pdg.get("boundary") or {}).get("recall@0.01"),
                         "pd_field_recall": (pdg.get("fields") or {}).get("recall"),
                         "pd_field_precision": (pdg.get("fields") or {}).get("precision"),
                         "pd_invariant_recall": (pdg.get("invariants") or {}).get("recall"),
                         "text_recall": tx.get("recall"), "text_precision": tx.get("precision")})
out = Path("/tmp/arroyave/results/orchid/data/orchid-bench-alcu-per-doc.csv")
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    for r in rows:
        w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
print(len(rows), "rows ->", out)
for r in rows:
    if r["doc"] in ("syn-AlCu-02Mie-v0", "syn-CuNi-87Jan-v0", "syn-AlSi-12Tan-v0") and r["rendering"] in ("vector", "degraded_raster") \
            and r["extractor"] in ("ai_gemini", "vector_route", "tables_pdfplumber"):
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
