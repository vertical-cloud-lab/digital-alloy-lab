"""Write robot-build/route-quotes.csv: the live instant quotes of 2026-11-25 (round 7, manufacturing-route.md).

The quotes were read in headed Chromium through the lab Pi's SOCKS tunnel (BYU network), with no account, no login and
nothing ordered or put in a cart:
  - JLC3DP (jlc3dp.com/3d-printing-quote), 05:35-05:41 UTC: the frame and the one-piece body (frame + floor plate fused),
    exported by export_chamber.py, in SLM 316L, SLM "Aluminum 6061", SLM Ti TC4 and BJ-316L;
  - JLCCNC (jlccnc.com/cnc-machining-quote), 05:41-05:47 UTC (frame, floor, lid, door, with spec variants) and
    06:00-06:17 UTC (all 64 machined pieces of export_parts.py, default spec, one at a time);
  - Craftcloud and PCBWay: tried, not priced (see the rows).
The bulk JLCCNC prices were parsed from the page text (/tmp/route/jlccnc_items.json, file names shortened to p##_... because
JLCCNC dropped uploads with long names; /tmp/route/short/map.json maps them back). Those /tmp files are not committed; this
script is kept so the CSV can be rebuilt from them in the same session.

Run: python3 desktop-lpbf/analysis/route/quotes_csv.py
"""
import csv
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[2] / "robot-build" / "route-quotes.csv"
ITEMS = pathlib.Path("/tmp/route/jlccnc_items.json")
MAP = pathlib.Path("/tmp/route/short/map.json")
PARTS = pathlib.Path("/tmp/route/allparts/parts.csv")
SHOT = "robot-build/img/"

FIELDS = ["service", "part", "file", "as_quoted", "qty", "usd_each", "lead_time", "fetched_utc", "screenshot", "note"]
MANUAL = [
    # service, part, file, as quoted, qty, usd, lead, utc, screenshot, note
    ("JLC3DP", "Process chamber body (through-frame), 312 x 222 x 123.9 mm, 1594.8 cm3", "frame.step",
     "SLM 316L, no surface finish", 1, 2833.47, "standard build 3 days; UPS Express Saver DDP 2-4 business days, $180.40 (18.87 kg)",
     "2026-11-25T05:37Z", SHOT + "route-quote-jlc3dp-frame-316l.png",
     "'The final price is subject to review'; Ra 3.2-12 um and +/-0.3 mm (<=100 mm) or +/-0.4 % as stated by JLC3DP"),
    ("JLC3DP", "Process chamber body (through-frame)", "frame.step", "SLM Aluminum 6061 (JLC3DP's new SLM aluminium)", 1, 1716.66,
     "standard build (days not shown in the dialog)", "2026-11-25T05:36Z", SHOT + "route-quote-jlc3dp-frame-al.png",
     "price in the spec dialog; JLC3DP states 172 W/m.K, 15 % elongation, service <= 150 C"),
    ("JLC3DP", "Process chamber body (through-frame)", "frame.step", "SLM Titanium TC4", 1, 3471.39, "not shown",
     "2026-11-25T05:37Z", "", "for scale only"),
    ("JLC3DP", "One-piece body: frame + floor plate fused, 312 x 222 x 140 mm, 2725.17 cm3", "body_one_piece.step",
     "SLM 316L, no surface finish", 1, 4826.37, "standard build 3 days; both bodies together ship for $453.13 (50.91 kg)",
     "2026-11-25T05:40Z", SHOT + "route-quote-jlc3dp-both-316l.png", "price subject to review"),
    ("JLC3DP", "One-piece body: frame + floor plate fused", "body_one_piece.step", "SLM Aluminum 6061", 1, 2916.58,
     "not shown", "2026-11-25T05:39Z", SHOT + "route-quote-jlc3dp-body-al.png", "price in the spec dialog"),
    ("JLC3DP", "One-piece body", "body_one_piece.step", "BJ-316L (binder jet)", 1, None, "-", "2026-11-25T05:39Z", "",
     "not offered: 'Max 100x100x100mm'"),
    ("JLCCNC", "Process chamber body (through-frame)", "frame.step", "6061, any finish", 1, None,
     "manual quote 'in 2-4 hours' after an order is submitted (needs an account)", "2026-11-25T05:41Z",
     SHOT + "route-quote-jlccnc-frame-manual.png", "no instant price"),
    ("JLCCNC", "Chamber floor plate", "floor.step", "6061, no finish, ISO 2768-m", 1, 83.68, "standard 6 days + UPS DDP 2-4 business days",
     "2026-11-25T05:44Z", SHOT + "route-quote-jlccnc-chamber.png", "default spec (bead blast + natural anodize): $92.16"),
    ("JLCCNC", "Chamber lid", "lid.step", "6061, no finish, ISO 2768-m", 1, 64.99, "standard 6 days + UPS DDP 2-4 business days",
     "2026-11-25T05:44Z", SHOT + "route-quote-jlccnc-chamber.png", "default spec: $74.16"),
    ("JLCCNC", "Chamber lid", "lid.step", "6061, no finish, tightest tolerance +/-0.05 mm", 1, 73.30, "as above", "2026-11-25T05:46Z", "",
     "threads 'Yes' asks for a drawing upload; the earlier run (outsourcing.md) found threads add ~25 %"),
    ("JLCCNC", "Chamber door", "door.step", "6061, no finish, ISO 2768-m", 1, 33.74, "standard 6 days + UPS DDP 2-4 business days",
     "2026-11-25T05:44Z", SHOT + "route-quote-jlccnc-chamber.png", "default spec: $37.83"),
    ("Craftcloud", "frame", "frame.stl", "-", 1, None, "-", "2026-11-25T05:44Z", "",
     "not priced: the upload opens a settings dialog whose 'Confirm & continue' accepts Craftcloud's Terms of Use; closing it "
     "cancels the upload. Not accepted on the lab's behalf (as on 2026-11-22)"),
    ("PCBWay", "frame", "frame.step", "3D printing, stainless", 1, None, "-", "2026-11-25T05:46Z", "",
     "not priced: the 3D-printing form is a request for quote ('RFQ', Submit Request accepts the terms)"),
]


def main():
    rows = [dict(zip(FIELDS, r)) for r in MANUAL]
    if ITEMS.exists() and MAP.exists():
        items = json.loads(ITEMS.read_text())
        short = json.loads(MAP.read_text())
        parts = {r["file"]: r for r in csv.DictReader(PARTS.open())} if PARTS.exists() else {}
        # the six uploaded under their long names show truncated names; match them by volume
        by_vol = {round(float(r["volume_cm3"]), 1): r for r in parts.values() if r["kind"] == "stock"}
        for it in items:
            f = short.get(it["name"])
            if f is None:
                p = by_vol.get(round(it["vol_mm3"] / 1000.0, 1))
                f = p["file"] if p else it["name"]
            p = parts.get(f, {})
            price = it["price"]
            rows.append(dict(service="JLCCNC (bulk, default spec)", part=p.get("part", f)[:110], file=f + ".step",
                             as_quoted="6061-T6 (default for every piece, 316L and 416 included), bead blast + natural anodize, "
                                       "ISO 2768-m, standard appearance, no threads",
                             qty=int(p.get("qty_per_machine", 1) or 1),
                             usd_each=None if price == "manual" else price,
                             lead_time="standard 7 days (all 64 together: $2,437.49; economic 12 days $2,249.48; expedited 3 days "
                                       "$3,747.92); UPS DDP 2-4 business days, $746.51 for 83.87 kg",
                             fetched_utc="2026-11-25T06:17Z", screenshot=SHOT + "route-quote-jlccnc-all.png",
                             note=("manual quote" if price == "manual" else "price per piece at quantity 1 (the qty column is per machine; "
                                   "quantity breaks not applied)") + f"; envelope {' x '.join(str(d) for d in it['dims'])} mm, "
                                   f"{it['vol_mm3'] / 1000:.1f} cm3"))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print("wrote", OUT, len(rows), "rows")


if __name__ == "__main__":
    main()
