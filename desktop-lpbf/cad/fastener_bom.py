"""Fastener bill of materials from the model's joint table (joints.py), for one machine with all three build modules.

Builds the machine with the M50 module (every machine-side joint) and the S25 and L75 modules (their own joints only),
counts every McMaster part, and writes desktop-lpbf/fasteners.csv: joint, part number, description, quantity, the pack it
is sold in, packs to buy, line cost, URL and fetch time. Prices are McMaster list prices read through the lab Pi.

Run:  python desktop-lpbf/cad/fastener_bom.py
"""
from __future__ import annotations

import csv
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fasteners as FS  # noqa: E402
import joints as J  # noqa: E402
import lpbf_low as M  # noqa: E402

MODULE_KEYS = ("module_flange", "stack_", "gland_", "handle_", "rod_", "striker_", "res_lid")   # joints that come with each module
                                                                                                # (and its reservoir: the lid screws)


def pack_qty(sold_as):
    m = re.search(r"(\d[\d,]*)", str(sold_as or "1"))
    return int(m.group(1).replace(",", "")) if m and "pack" in str(sold_as) else 1


def main():
    count, where = {}, {}
    for mod in ("M50", "S25", "L75"):
        M.build(module=mod)
        for key, n_pn_items in [(k, r) for k, r in J.REGISTRY.items()]:
            if mod != "M50" and not key.startswith(MODULE_KEYS):
                continue
            if mod != "M50" and key == "module_flange":
                pass                                  # every module carries its own captive screws and retainers
            r = n_pn_items
            for pn, items in [(r["pn"], r["items"])] + r["extra"]:
                count[pn] = count.get(pn, 0) + len(items)
                where.setdefault(pn, set()).add(key.replace("_M50", "").replace("_S25", "").replace("_L75", ""))
    rows, total = [], 0.0
    for pn in sorted(count, key=lambda p: (FS.CATALOG[p]["kind"], FS.CATALOG[p].get("d", 0), FS.CATALOG[p].get("L", 0))):
        c = FS.CATALOG[pn]
        q = count[pn]
        pk = pack_qty(c.get("sold_as"))
        packs = math.ceil(q / pk)
        price = float(c.get("price_usd") or 0.0)
        line = packs * price
        total += line
        rows.append([", ".join(sorted(where[pn])), pn, c.get("desc", ""), q, c.get("sold_as", ""), f"{price:.2f}", packs, f"{line:.2f}",
                     c.get("url", ""), c.get("fetched_utc", "")])
    out = HERE.parent / "fasteners.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["joints", "part_number", "description_as_listed", "qty_per_machine", "sold_as", "price_per_pack_usd", "packs",
                    "line_usd", "url", "fetched_utc"])
        w.writerows(rows)
    print(f"wrote {out.name}: {len(rows)} part numbers, {sum(count.values())} pieces, ${total:,.2f}")
    return total


if __name__ == "__main__":
    main()
