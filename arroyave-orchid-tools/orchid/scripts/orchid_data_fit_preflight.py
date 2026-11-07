#!/usr/bin/env python3
"""Build an ESPEI fitting selection for one binary from the ORCHID espei/ bundle and an SGTE TDB, for
orchid-data's own read-only preflight (espei/check_fit.py). Writes selection.json into --workdir only.

Usage:
  python -I orchid_data_fit_preflight.py --bundle <orchid-data>/espei --tdb <...>/AlCu-21Kro.tdb \
      --system AL-CU --folders experimental,invariants --workdir /tmp/arroyave/work/orchid-data-fitcheck/al-cu
then:
  python <orchid-data>/espei/check_fit.py --bundle <orchid-data>/espei --selection <workdir>/selection.json
"""
import argparse
import hashlib
import json
import os


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--tdb", required=True)
    ap.add_argument("--system", required=True)
    ap.add_argument("--folders", default="experimental,invariants")
    ap.add_argument("--workdir", required=True)
    a = ap.parse_args()
    folders = a.folders.split(",")
    idx = json.load(open(os.path.join(a.bundle, "index.json")))
    rows = [r for r in idx["datasets"] if r["system"] == a.system and r["folder"] in folders]
    sel = {"target": {"path": os.path.abspath(a.tdb), "sha256": sha(a.tdb)},
           "datasets": [{"path": r["path"], "sha256": sha(os.path.join(a.bundle, r["path"]))} for r in rows]}
    os.makedirs(a.workdir, exist_ok=True)
    out = os.path.join(a.workdir, "selection.json")
    json.dump(sel, open(out, "w"), indent=1)
    print(f"{out}: target {os.path.basename(a.tdb)}, {len(rows)} datasets from {folders}: "
          + ", ".join(r['path'] for r in rows))


if __name__ == "__main__":
    main()
