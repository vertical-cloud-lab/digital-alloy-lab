#!/usr/bin/env python3
"""Read-only integrity checks of an orchid-data checkout's Parquet release.

1. parquet/MANIFEST.json: row counts and file SHA-256 of the 7 tables; SHA-256 of the 9 listed inputs
   (the phase-diagrams/sgte/*.json input is the SHA-256 of the 'sha256  basename' lines, newline-terminated).
2. Counts stated in DATASET_CARD.md compared with the Parquet tables and the JSONL dump.
3. Why the Al-Si literature values are not accepted (gate failure codes).

Usage: python -I orchid_data_integrity.py --data /path/to/orchid-data
"""
import argparse
import collections
import glob
import gzip
import hashlib
import json
import os
import re

import pandas as pd
import pyarrow.parquet as pq


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    D = ap.parse_args().data.rstrip("/") + "/"

    print("== 1. parquet/MANIFEST.json")
    m = json.load(open(D + "parquet/MANIFEST.json"))
    print("release:", m.get("release"))
    for name, t in m["tables"].items():
        f = D + "parquet/" + t["file"]
        rows = pq.ParquetFile(f).metadata.num_rows
        print(f"  {name:26s} rows {rows:>6} (manifest {t['rows']:>6}) file_sha256 {'OK' if sha(f) == t['file_sha256'] else 'MISMATCH'}")
    for path, h in m["inputs"].items():
        if "*" in path:
            files = sorted(glob.glob(D + path.split(" ")[0]))
            s = "\n".join(f"{sha(f)}  {os.path.basename(f)}" for f in files) + "\n"
            ok = hashlib.sha256(s.encode()).hexdigest() == h
            print(f"  input {path}: {len(files)} files, {'OK' if ok else 'MISMATCH'}")
        else:
            print(f"  input {path}: {'OK' if sha(D + path) == h else 'MISMATCH'}")

    print("\n== 2. DATASET_CARD.md counts vs data")
    card = open(D + "DATASET_CARD.md", encoding="utf-8").read()
    lv = pd.read_parquet(D + "parquet/literature_values.parquet",
                         columns=["id", "system", "accepted", "evidence_class", "paper_id", "gate_failures", "property"])
    n_jsonl = 0
    acc_jsonl = collections.Counter()
    with gzip.open(D + "literature/orchid-literature.jsonl.gz", "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            n_jsonl += 1
            acc_jsonl[bool(r.get("flags", {}).get("extraction_accepted"))] += 1
    claims = {
        "values (card: 'There are N values')": (re.search(r"There are ([\d,]+) values", card), len(lv)),
        "accepted (card: 'N values are accepted')": (re.search(r"([\d,]+) values are accepted", card), int(lv.accepted.sum())),
        "papers (card: 'values from N papers')": (re.search(r"values from ([\d,]+)\s+papers", card), lv.paper_id.nunique()),
        "systems (card: 'covering N chemical systems')": (re.search(r"covering ([\d,]+) chemical systems", card), lv.system.nunique()),
    }
    for ec in ("experimental", "model", "dft", "unspecified"):
        claims[f"evidence_class={ec}"] = (re.search(rf"`{ec}` \(([\d,]+)", card), int((lv.evidence_class == ec).sum()))
    for k, (mt, actual) in claims.items():
        stated = int(mt.group(1).replace(",", "")) if mt else None
        print(f"  {k:48s} card {stated!s:>7}  parquet {actual:>7}  {'same' if stated == actual else 'DIFFERENT'}")
    print(f"  JSONL dump: {n_jsonl} rows, flags.extraction_accepted true {acc_jsonl[True]} / false {acc_jsonl[False]}")

    print("\n== 3. Al-Si literature values: acceptance")
    s = lv[lv.system == "AL-SI"]
    codes = collections.Counter(g.get("code") if isinstance(g, dict) else g for x in s.gate_failures for g in x)
    print(f"  {len(s)} values, accepted {int(s.accepted.sum())}; properties {s.property.value_counts().to_dict()}; "
          f"gate failure codes {dict(codes)}")


if __name__ == "__main__":
    main()
