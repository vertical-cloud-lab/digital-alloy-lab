#!/usr/bin/env python3
"""Re-measure the README's "CU-ZR, bytes of JSON per call" table of orchid-mcp against the local data.

Usage: /tmp/sbx/clean <venv>/bin/python -I orchid_mcp_readme_sizes.py --server <venv>/bin/orchid-mcp \
          --data-dir D --site-dir S --cache-dir C --out <results>/data/mcp_readme_sizes.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orchid_mcp_drive import Client  # noqa: E402

CALLS = [  # (README label, tool, args, README "after" bytes)
    ('get_system_data("CU-ZR")', "get_system_data", {"system": "CU-ZR"}, 23234),
    ('get_invariant_reactions("CU-ZR")', "get_invariant_reactions", {"system": "CU-ZR"}, 83218),
    ('get_phase_diagram("CU-ZR")', "get_phase_diagram", {"system": "CU-ZR"}, 38958),
    ('compare_to_dft("CU-ZR")', "compare_to_dft", {"system": "CU-ZR"}, 37597),
    ('get_formation_enthalpy("CuZr2")', "get_formation_enthalpy", {"formula": "CuZr2"}, 15140),
    ('search_systems(["Cu"])', "search_systems", {"elements": ["Cu"]}, 12135),
    ('list_tdb_files(["Cu","Zr"])', "list_tdb_files", {"elements": ["Cu", "Zr"]}, 10294),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    for k in ("--server", "--data-dir", "--site-dir", "--cache-dir", "--out"):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR") if k in os.environ}
    env.update({"ORCHID_DATA_DIR": a.data_dir, "ORCHID_SITE_DATA_DIR": a.site_dir, "ORCHID_OFFLINE": "1",
                "ORCHID_CACHE_DIR": a.cache_dir, "XDG_CACHE_HOME": a.cache_dir})
    cl = Client(shlex.split(a.server), env, Path(a.out).with_suffix(".stderr.log"))
    cl.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "sizes", "version": "0"}})
    cl.notify("notifications/initialized")
    rows = []
    for label, name, args, readme in CALLS:
        msg, dt, nb = cl.request("tools/call", {"name": name, "arguments": args})
        res = msg.get("result") or {}
        text = (res.get("content") or [{}])[0].get("text") or ""
        n = len(text.encode())
        rows.append({"call": label, "readme_bytes_after": readme, "measured_text_bytes": n,
                     "ratio": round(n / readme, 3), "envelope_bytes": nb, "ms": round(dt * 1000, 1),
                     "is_error": bool(res.get("isError"))})
        print(rows[-1], flush=True)
    cl.close()
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
