"""Bill of materials for options B (recommended) and A (interim), from the public catalogue lookups in
vendor-lookups.csv (fetched 2026-11-27). Writes ../BOM.md and bom_B.csv / bom_A.csv.

    python bom/make_bom.py

Prices are one unit as listed, before shipping, tax and cut fees. Each line names the lookup it came from
(vendor + part number in vendor-lookups.csv); lines marked "not priced" had no public price.
"""

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS = list(csv.DictReader(open(HERE / "vendor-lookups.csv")))


def price(vendor, pn):
    for r in ROWS:
        if r["vendor"].lower().startswith(vendor.lower()) and pn in r["part_number"]:
            try:
                return float(r["price_usd"]), r["url"], r["stock_or_lead_time"]
            except ValueError:
                return None, r["url"], r["stock_or_lead_time"]
    return None, "", ""


# (line, what, vendor, part number, qty, unit multiplier note, buy-qty factor for price)
B = [
    ("B1", "KF-50 x 2 in butt-weld stub, 304L, 19.05 mm (316L QF50-200-SSL not stocked)", "A&N", "4000126", 1, 1),
    ("B2", "3 x 2 in concentric butt-weld reducer, 316L, 0.065 wall, 101.6 long", "McMaster", "5237K471", 1, 1),
    ("B3", "3 in OD x 0.065 316 tube, 12 in (the pot's tube: 82.35 mm + facing)", "OnlineMetals", "4256", 1, 1),
    ("B4", "3-1/4 in 316 round bar, 1.5 in (end cap blank: 20 mm part + chuck + parting)", "Speedy", "p-2646", 1, 1.5),
    ("B5", "2-3/4 in OD x 0.065 304 tube, 12 in (liner, in the pot)", "McMaster", "11116N864", 1, 1),
    ("B6", "3 in 304 round bar, 1.5 in (catch puck Ø70 x 25, in the pot)", "Speedy", "p-1872", 1, 1.5),
    ("B7", "Over-pressure ring for the cone's KF-50 joint, 304L, 50 psig", "A&N", "4000076", 1, 1),
    ("B8", "Spare KF-50 centring ring, stainless + FKM", "MDC", "710003", 1, 1),
    ("B9", "KF-50 blank (closes the upper part's top for its hydro test)", "Duniway", "KF50-FB", 1, 1),
    ("B10", "KF-50 clamp, Al, wing nut (for B9)", "Duniway", "KF50-CP", 1, 1),
    ("B11", "Type K washer thermocouple, junction 900 C, 6 ft", "Auber", "TC-K-WS", 2, 1),

    ("B14", "2-channel type K meter with 2 alarm relays, 85-260 VAC", "Auber", "SYL-2813AC", 1, 1),
    ("B15", "Panel buzzer, 30-120 VAC", "McMaster", "56965T26", 1, 1),
    ("B16", "ER316L TIG rod 1/16 in, 1 lb", "McMaster", "7972A501", 1, 1),
    ("B17", "Leak-check fluid, Snoop 8 oz", "Keep Supply", "MS-SNOOP-8OZ", 1, 1),
]
B_NOT_PRICED = [
    ("B18", "6061-T6 flat bar 2-1/2 x 4-1/2 in, 5 in (weld fixture, 120 mm)", "shop stock or any metals supplier"),
    ("B19", "304 shim stock 0.025 in (0.64 mm), a 1 x 3 in strip (flange shim in the fixture)", "shop stock"),
    ("B12", "All-stainless worm clamps with a ~9 mm band, one for the 2 in stub, one for the 3 in end cap (the stub has "
            "12.6 mm of straight tube; McMaster 5415K's 12.7 mm band is too wide and its screw is zinc-plated)", "not priced"),
    ("B13", "3 in tri-clamp end cap with a 1/4 NPT port (test closure for both welded parts)", "sanitary catalogue, not priced"),
    ("B24", "3 in short weld ferrules (14WMP), 316L: one welded to the reducer, one to the pot's tube", "sanitary catalogue, not priced"),
    ("B25", "3 in tri-clamp, pressure-rated (the pot's joint)", "sanitary catalogue, not priced"),
    ("B26", "3 in tri-clamp gaskets, PTFE (260 C), x3: FEA peak 263 C only if all 816 g arrives as shot; FKM is "
            "fine to ~630 g", "sanitary catalogue, not priced"),
    ("B27", "3 in tri-clamp end cap, plain (carries the pot to the glovebox or bench under argon)", "sanitary catalogue, not priced"),
    ("B14b", "Test rig: 0-2 bar gauge, 1/4 NPT relief valve set ~1.5 bar, ball valve, hand pump or water line", "not priced"),
    ("B15b", "Meter wiring: enclosure, IEC cord, fuse holder, wire, two type K mini connectors", "not priced"),

    ("B21", "AMAZEMET cone shields", "should be in the lab (AMAZEMET: 'you should have the replacements')"),
    ("B22", "Stainless safety lanyard / wire rope with a clip, cup to frame, and an eye bolt on the frame "
            "(Edison: secondary restraint)", "shop stock"),
    ("B23", "Copper chill block for the KF flange during W1; two strap clamps for the fixture", "shop stock"),
]
A = [
    ("A1", "KF-50 full nipple, 160 mm, 304", "Duniway", "KF50-NP", 1, 1),
    ("A2", "KF-50 blank", "Duniway", "KF50-FB", 1, 1),
    ("A3", "KF-50 centring ring, stainless + FKM (bottom joint)", "MDC", "710003", 1, 1),
    ("A4", "KF-50 clamp, Al, wing nut (bottom joint)", "Duniway", "KF50-CP", 1, 1),
    ("A5", "Over-pressure rings (bottom joint and the cone's joint)", "A&N", "4000076", 2, 1),
    ("A6", "1-3/4 in OD x 0.049 304 tube, 1 ft (liner)", "McMaster", "11116N835", 1, 1),
    ("A7", "2 in 304 round bar, 2 in (puck)", "Speedy", "p-1866", 1, 2),
    ("A8", "Leak-check fluid, Snoop 8 oz", "Keep Supply", "MS-SNOOP-8OZ", 1, 1),
]


def table(lines):
    out, total = [], 0.0
    for line, what, vendor, pn, qty, factor in lines:
        p, url, stock = price(vendor, pn)
        ext = None if p is None else p * qty * factor
        total += ext or 0.0
        out.append(dict(line=line, item=what, vendor=vendor, part_number=pn, qty=qty,
                        unit_usd="" if p is None else f"{p * factor:.2f}", ext_usd="" if ext is None else f"{ext:.2f}",
                        stock=stock, url=url))
    return out, total


def main():
    tb, totb = table(B)
    ta, tota = table(A)
    for name, rows in (("bom_B.csv", tb), ("bom_A.csv", ta)):
        with open(HERE / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    md = ["# Bill of materials\n",
          "Public catalogue prices fetched 2026-11-27, one unit as listed, before shipping, tax and cut fees.",
          "Generated by `bom/make_bom.py` from `bom/vendor-lookups.csv`; alternatives, stock levels and the KF",
          "overpressure ratings are in `bom/README.md`.\n",
          f"## B: welded 316L cup (recommended), ${totb:.2f} priced\n",
          "| Line | Item | Vendor | Part no. | Qty | Unit (USD) | Ext. (USD) | Stock / lead |",
          "|---|---|---|---|---:|---:|---:|---|"]
    for r in tb:
        md.append(f"| {r['line']} | {r['item']} | {r['vendor']} | [{r['part_number']}]({r['url']}) | {r['qty']} | "
                  f"{r['unit_usd']} | {r['ext_usd']} | {r['stock'][:40]} |")
    for line, what, note in B_NOT_PRICED:
        md.append(f"| {line} | {what} | {note} | | | | | |")
    md += [f"| | **Total priced** | | | | | **{totb:.2f}** | |\n",
           f"## A: catalogue cup (interim, small charges only), ${tota:.2f}\n",
           "| Line | Item | Vendor | Part no. | Qty | Unit (USD) | Ext. (USD) | Stock / lead |",
           "|---|---|---|---|---:|---:|---:|---|"]
    for r in ta:
        md.append(f"| {r['line']} | {r['item']} | {r['vendor']} | [{r['part_number']}]({r['url']}) | {r['qty']} | "
                  f"{r['unit_usd']} | {r['ext_usd']} | {r['stock'][:40]} |")
    md += [f"| | **Total** | | | | | **{tota:.2f}** | |\n",
           "## Shop equipment and tooling assumed (optional, usually in the shop)\n",
           "| For | Equipment / tools |", "|---|---|",
           "| Turning (end cap, puck, liner, tube ends) | CNC or manual lathe, 3-jaw chuck with soft jaws, a tube spider; "
           "CNMG 432 and VNMG 331 inserts, a 16 mm boring bar (CCMT), a 3 mm parting blade, a 25 mm drill |",
           "| Milling (fixture) | 3-axis mill or router that takes a 245 x 114 x 64 mm block; 50 mm face mill, 12 mm "
           "3-flute carbide end mill (36 mm flute), 1/2 in 90 deg chamfer mill, 6 mm end mill, 10 mm spot drill, "
           "5.0 mm drill, M6 x 1.0 tap |",
           "| Welding | TIG (pulsed DCEN, 5-60 A) with argon, a second argon line and tape or plugs for the back-purge, "
           "stainless-only brushes, pickling gel, a borescope to look at the inside of W2 and W3 |",
           "| Testing | water and the B13/B14b rig for the 1.2 bar hydro test of each welded part; an argon regulator "
           "to +0.3 bar for the soap test; the atomizer's own pump and gauge for the rate-of-rise test |",
           "\nOptional extras priced in `bom/README.md` but left out of B: an isolation valve (not needed: the "
           "pot is capped with B27 after removal) and a separate vacuum gauge for bench rate-of-rise tests."]
    (HERE.parent / "BOM.md").write_text("\n".join(md) + "\n")
    print(f"B {totb:.2f}  A {tota:.2f}")


if __name__ == "__main__":
    main()
