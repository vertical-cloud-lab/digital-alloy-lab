"""The order list for the copper corrosion setup with four stir modules, minus what the lab has.

Asked for by Ben on #180 (2026-11-06): everything to order now to start the corrosion tests on
the CubXL with four of byu-vcl#269's compact stir modules on the deck. Left out, as he asked: the
potentiostat (Dr. Porter's EZstat-Pro is set up) and the 20 uL tips (enough for a few tests).

The corrosion rows are read from ../bom/bom.csv (prices seen 2026-10-19), so the two lists can't
drift apart. The stirrer rows are byu-vcl hardware/vial-stirrer-cubxl/BOM.md's, with its
prices (2026-10-19; item 13 on 2026-10-29), for what four stirrers need beyond ME order 13518.

    python order_list.py     # writes order-list.csv and order-totals.json, prints the tables
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOM = HERE.parent / "bom" / "bom.csv"

# Corrosion rows to order now, and why some aren't.
ORDER = ["B01", "B02", "B03", "B04", "B06", "B07", "B08", "B09", "B10", "B11", "B12", "B14", "B15", "B16",
         "B17", "B19", "B20", "B21", "B22", "B26", "B29", "B36", "B38", "B39", "B40", "B41", "B43", "B44",
         "B45", "B46", "B47"]
COVERED = {  # the stirrer order (ME 13518) already brought the same part
    "B13": "same insert as the stirrer BOM's item 11 (100 from ME order 13518): the cell takes 12, three more stirrers 12",
    "B18": "JST-XH 4-pin pairs come with the stirrer BOM's item 9 (10 pairs, ME order 13518): the tray takes 2, three more stirrers 3",
}
CHECK_STOCK = {"B34": "filament: about 0.42 kg of PLA for the corrosion plates (bom/a1-mini) and 0.1 kg of PETG for the stirrer parts"}
LEFT_OUT = {
    "B23": "potentiostat: the EZstat-Pro is set up", "B24": "potentiostat box", "B25": "potentiostat",
    "B27": "potentiostat", "B28": "potentiostat adapter", "B35": "tips: enough on hand for a few tests",
    "B05": "fallback O-ring cap only", "B30": "optional polish", "B31": "optional polish", "B32": "optional polish",
    "B33": "optional polish", "B37": "aluminium only: add it if the aluminium shakedown runs too",
    "B42": "only if the ICP lab won't dilute into its own tubes", "B48": "optional: only if the lid's bridged ceiling is rough",
}

# Stirrer rows: four compact stirrers need these beyond ME order 13518 (byu-vcl#269 README,
# "Four stirrers on one Uno"). One stirrer is built; 13518 had two fans and one 10 ft cable.
STIR = [
    {"id": "ST1", "item": "Fan, Orion OD4010-12HSS, 40 x 40 x 10.5 mm, 12 V, 2-wire", "qty": 3, "unit": 7.43,
     "vendor": "Amazon", "part": "B00JJ402HY", "url": "https://www.amazon.com/dp/B00JJ402HY",
     "notes": "two for stirrers C and D, one spare; only 4 were left on 2026-10-19, Digi-Key 1053-1205-ND is the same fan"},
    {"id": "ST2", "item": "Cable, 22 AWG, 4 conductors, stranded, 10 ft", "qty": 1, "unit": 7.99,
     "vendor": "Amazon", "part": "B0BVQ7ZNCQ", "url": "https://www.amazon.com/dp/B0BVQ7ZNCQ",
     "notes": "about 1.5 m per stirrer; with what is left of 13518's pack this covers B, C and D. Buy two if the route is longer"},
    {"id": "ST3", "item": "Socket head screw kit, M3, 304 stainless, 6-30 mm, 540 pcs", "qty": 1, "unit": 9.99,
     "vendor": "Amazon", "part": "B0D4L6QRZB", "url": "https://www.amazon.com/dp/B0D4L6QRZB",
     "notes": "four stirrers take 16 x M3 x 20 and the first kit has 15; stainless, because the magnets catch on steel"},
    {"id": "ST4", "item": "Capacitor kit, 1206 chip, 16 values (100 nF for the Hall sensor)", "qty": 1, "unit": 6.99,
     "vendor": "Amazon", "part": "B06XDHC93D", "url": "https://www.amazon.com/dp/B06XDHC93D",
     "notes": "only if the stirrer BOM's item 13 hasn't been ordered: it came after ME order 13518"},
]
STIR_OPTIONAL = [
    {"id": "ST5", "item": "PTFE stir bar 12 x 3 mm (Pioreactor SKU 2003)", "qty": 4, "unit": 1.68,
     "vendor": "Pioreactor", "part": "2003", "url": "https://pioreactor.com/products/3-mm-ptfe-stir-bar",
     "notes": "optional: pulled 44 % as hard as the 15 x 6 mm bar and all but removes the Hall misreads (byu-vcl#269 README)"},
]


def main():
    rows = {r["id"]: r for r in csv.DictReader(BOM.open())}
    out = []
    for i in ORDER:
        r = rows[i]
        price = float(r["ext_price_usd"]) if r["ext_price_usd"] else None
        out.append({"id": i, "group": r["group"], "item": r["item"], "qty": r["qty"], "vendor": r["vendor"],
                    "part": r["part_number"], "url": r["url"], "price_usd": price,
                    "status": r["status"], "for": "corrosion", "notes": r["notes"]})
    for s in STIR:
        out.append({"id": s["id"], "group": "stirrers", "item": s["item"], "qty": str(s["qty"]), "vendor": s["vendor"],
                    "part": s["part"], "url": s["url"], "price_usd": round(s["qty"] * s["unit"], 2),
                    "status": "to buy" if s["id"] != "ST4" else "to buy if not ordered", "for": "stirrers", "notes": s["notes"]})

    with (HERE / "order-list.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    priced = [r for r in out if r["price_usd"] is not None]
    by_vendor = defaultdict(float)
    for r in priced:
        by_vendor[r["vendor"]] += r["price_usd"]
    quotes = [f'{r["id"]} {r["item"][:50]}' for r in out if r["price_usd"] is None]
    totals = {
        "price_seen": "2026-10-19 (stirrer item 13: 2026-10-29); before shipping and tax",
        "rows": len(out),
        "priced_rows": len(priced),
        "unpriced_or_quote": quotes,
        "corrosion_usd": round(sum(r["price_usd"] for r in priced if r["for"] == "corrosion"), 2),
        "of_which_B19_reference_placeholder_usd": 261.0,
        "stirrers_usd": round(sum(r["price_usd"] for r in priced if r["for"] == "stirrers"), 2),
        "stirrers_without_ST4_usd": round(sum(r["price_usd"] for r in priced if r["for"] == "stirrers" and r["id"] != "ST4"), 2),
        "total_usd": round(sum(r["price_usd"] for r in priced), 2),
        "by_vendor_usd": {k: round(v, 2) for k, v in sorted(by_vendor.items(), key=lambda kv: -kv[1])},
        "optional_stirrer_usd": round(sum(s["qty"] * s["unit"] for s in STIR_OPTIONAL), 2),
        "covered_by_stirrer_order": COVERED,
        "check_stock": CHECK_STOCK,
        "left_out": LEFT_OUT,
    }
    (HERE / "order-totals.json").write_text(json.dumps(totals, indent=1) + "\n")
    print(json.dumps({k: v for k, v in totals.items() if k not in ("left_out",)}, indent=1))

    # markdown, by vendor, for BOM.md
    vend = defaultdict(list)
    for r in out:
        vend[r["vendor"]].append(r)
    order = sorted(vend, key=lambda v: -sum(r["price_usd"] or 0 for r in vend[v]))
    print()
    for v in order:
        sub = sum(r["price_usd"] or 0 for r in vend[v])
        print(f"| **{v}** | | | | **{sub:,.2f}** | |")
        for r in vend[v]:
            p = "quote" if r["price_usd"] is None and r["status"] == "quote" else ("not read" if r["price_usd"] is None else f'{r["price_usd"]:,.2f}')
            print(f'| {r["id"]} | {r["item"]} | {r["qty"]} | [{r["part"]}]({r["url"]}) | {p} | |')


if __name__ == "__main__":
    main()
