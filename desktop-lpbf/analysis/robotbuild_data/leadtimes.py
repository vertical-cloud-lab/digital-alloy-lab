"""Lead times for every bom.csv line, new and used, and the schedule they set (issue #260, PR #266, round 7, 2026-11-25).

days = calendar days from placing the order to having the part at BYU: the vendor's ship time + transit, + BYU's
purchase-order step when one vendor's order is $3,500 or more. Every row names its source; "estimate" marks this file's
own assumptions. Vendor statements are rows of leadtime-lookups.csv (read 2026-11-25; URL and fetch time on each).
Imported by build_hud.py.
"""
from __future__ import annotations

TRANSIT = dict(ground=(2, 5), freight=(3, 7), none=(0, 0))  # US parcel ground / LTL freight to Provo: estimates
PO_DAYS = (10, 14)  # capstone.byu.edu: "Allow ten days to two weeks PLUS shipping time for a large order to be placed
                    # through University Purchasing"; purchases over $3,500 need a PO (read 2026-11-25T05:45Z)
MCM = ("McMaster: '98% of items ship from stock, and most orders arrive same or next day'", 0, 1, "ground",
       "leadtime-lookups.csv MCM-shipping (mcmaster.com/info/delivery, 2026-11-25T05:39Z)", "vendor statement")


def EST(what, lo=0, hi=3):
    return (f"{what}: distributor stock (not checked)", lo, hi, "ground", "estimate", "estimate")


# line: dict(new=(text, ship_lo, ship_hi, transit, source, basis), used=(text, ship_lo, ship_hi, transit, source) or None,
#            po=True when that vendor's order is $3,500 or more (BYU purchase order), alt=a faster new option if any)
LT = {
    "L1": dict(new=("IPG: 10-12 weeks ARO; IPG says it is 'unlikely to deliver much faster'", 70, 84, "freight",
                    "quotes/ipg-ylr-500-u3-sm-ac.md (IPG budgetary quote, 2026-11-18)", "quote"),
               used=("eBay, US surplus dealer (M6860): ships the same day from El Paso by LTL freight; under $3,500 with "
                     "freight, so a PCard", 0, 1, "freight", "cost/used-options.csv (2026-11-20); cost-scenarios.md section 4"),
               po=True),
    "L2": dict(new=("not needed: the quoted IPG is forced-air cooled", 0, 0, "none", "bom.csv L2", "n/a"), used=None),
    "L3": dict(new=("ordered with the laser (IPG)", 70, 84, "freight", "quotes/ipg-ylr-500-u3-sm-ac.md", "quote"),
               used=("the used laser's own output optics, or the eBay IPG collimator (US)", 1, 3, "ground",
                     "cost/used-options.csv"), po=True),
    "L4": dict(new=("no catalogue shutter rated for >= 500 W CW: quote (IPG's beam shutter is quote only; nm Laser, "
                    "Optogama and Lasermet stop at 100-300 W)", None, None, "ground", "leadtime-lookups.csv L4-shutter",
                    "quote"), used=None),
    "L5": dict(new=("SCANLAB: quote only, no published lead time (an open-source build wiki quotes 8-10 weeks for galvos: "
                    "a proxy, not SCANLAB's figure)", None, None, "ground", "leadtime-lookups.csv L5-basiCube20", "quote"),
               used=("eBay, US dealer (hurrySCAN 25 with a 30-day warranty) or open-box intelliSCAN III 20", 1, 3, "ground",
                     "cost/used-options.csv"), po=True,
               alt=("Thorlabs QS20XY-Y1 ($5,893.56): 'Available: Today'", 0, 1, "ground",
                    "leadtime-lookups.csv L5-QS20XY (thorlabs.com via the lab Pi, 2026-11-25T05:45Z)")),
    "L6": dict(new=("Thorlabs: 'In Stock Overseas'; 'Transfers between locations typically take 3-4 weeks'", 21, 28,
                    "ground", "leadtime-lookups.csv L6-FTH160-1064 (thorlabs.com via the lab Pi, 2026-11-25T05:43Z)",
                    "vendor page"),
               used=("eBay, US (LINOS f = 254 mm, free returns)", 1, 3, "ground", "cost/used-options.csv"), po=True),
    "L7": dict(new=("Edmund 38-990: '5 In Stock' (UK and Canadian sites; the US site blocks automated reads)", 0, 1,
                    "ground", "leadtime-lookups.csv L7-edmund", "vendor page"), used=None),
    "C1": dict(new=("SCANLAB RTC6: quote only; no reseller lists a new card", None, None, "ground",
                    "leadtime-lookups.csv C1-RTC6", "quote"),
               used=("eBay, US (RTC5 PCIe): the listing gave delivery to Provo on Nov 23-25 when read on Nov 20", 3, 5,
                     "none", "cost-scenarios.md section 4"), po=True),
    "C2": dict(new=EST("Raspberry Pi 5"), used=None),
    "C3": dict(new=("Teknic ClearCore: 'Quantities up to 5 generally ship within 3 business days'", 0, 5, "ground",
                    "leadtime-lookups.csv M2-clearpath", "vendor page"), used=None),
    "C4": dict(new=EST("Mean Well and Phoenix DIN supplies"), used=None, po=True),
    "C5": dict(new=("AutomationDirect: all seven parts in stock (11 to 355 each); in-stock orders before 6 p.m. ET ship "
                    "the same day", 0, 1, "ground", "leadtime-lookups.csv C5-productivity1000", "vendor page"), used=None),
    "C6": dict(new=EST("4U drawer, Hammond box, DIN parts"), used=None),
    "M1": dict(new=("McMaster parts from stock; Ferrotec SFL-006-NN: no published lead time (Ferrotec: standard models "
                    "'may have inventory')", None, None, "ground", "leadtime-lookups.csv M4-ferrotec", "quote"), used=None),
    "M2": dict(new=("Teknic: 'Ships in: 3 Days' (the first 5 pieces)", 0, 5, "ground", "leadtime-lookups.csv M2-clearpath",
                    "vendor page"),
               used=("eBay open box (US)", 1, 3, "ground", "cost/used-options.csv")),
    "M3": dict(new=("Oriental Motor: 'Contact your local sales office'; THK Quick Ship: '2 days to 2 weeks depending on "
                    "current stock levels'; MISUMI: '23 Day(s) or more'", 2, 23, "ground",
                    "leadtime-lookups.csv M3-THK-KR26", "vendor page"), used=None),
    "M4": dict(new=("McMaster stepper from stock; Ferrotec SSL-005-NN: no published lead time", None, None, "ground",
                    "leadtime-lookups.csv M4-ferrotec", "quote"), used=None),
    "M5": dict(new=MCM, used=None, po=True),
    "M6": dict(new=EST("Pi HQ camera, lens, Thorlabs filter"), used=None),
    "G1": dict(new=("Midwest Steel & Aluminum: plate 'in stock available for immediate delivery' (no cutting time "
                    "stated; Speedy Metals: 1-2 days); McMaster plate from stock", 1, 7, "ground",
                    "leadtime-lookups.csv G1-midwest (search snippet)", "search snippet"), used=None),
    "G2": dict(new=("Marshall Scientific: 'Typically ships within Same Business Day', brand new", 0, 1, "ground",
                    "leadtime-lookups.csv G2-nXDS6i (marshallscientific.com via the lab Pi, 2026-11-25T05:44Z)",
                    "vendor page"),
               used=("eBay, US (Agilent IDP-3)", 1, 3, "ground", "cost/used-options.csv"), po=True),
    "G3": dict(new=MCM, used=None, po=True),
    "G4": dict(new=("no gas-tight blower of this size found: quote", None, None, "ground",
                    "bom.csv G4; leadtime-lookups.csv G4-blower", "quote"), used=None),
    "G5": dict(new=MCM, used=None, po=True),
    "G6": dict(new=("Instrumart (Ntron Microx): 'Usually ships in 6-8 weeks'", 42, 56, "ground",
                    "leadtime-lookups.csv G6-microx (2026-11-25T05:32Z)", "vendor page"),
               used=("eBay, US (Alpha Omega Series 3000 or Teledyne 3190) plus a new sensor cell (cell lead not checked)",
                     1, 3, "ground", "cost/used-options.csv"),
               alt=("SST OXY-FLEX-0-H: 6 in stock at Digi-Key (8 weeks after that); may be a percent-level sensor", 0, 1,
                    "ground", "leadtime-lookups.csv G6-oxyflex")),
    "G7": dict(new=("McMaster parts from stock; the Vacuum Research Pirani and MKS clamp not checked", 0, 3, "ground",
                    "leadtime-lookups.csv MCM-shipping + estimate", "estimate"), used=None, po=True),
    "G8": dict(new=MCM, used=None, po=True),
    "G9": dict(new=("Selectum (Vaisala): '2 Weeks Factory Lead Time'; made to order, non-returnable", 14, 14, "ground",
                    "leadtime-lookups.csv G9-DMT143", "vendor page"),
               used=("eBay, US (Atlas Copco open box or Michell refurbished)", 1, 3, "ground", "cost/used-options.csv")),
    "S1": dict(new=("Digi-Key: XS26-2 1 in stock, XS16si 38, XS2so 7; then 4 weeks", 0, 1, "ground",
                    "leadtime-lookups.csv S1-banner-XS26", "vendor page"), used=None, po=True),
    "S2": dict(new=("Digi-Key: IDEC HS5L-VC44M-G 3 in stock (then 16 weeks); HS6B-12B05 'not kept in stock', 27-week "
                    "manufacturer lead time", 189, 189, "ground", "leadtime-lookups.csv S2-idec", "vendor page"),
               used=None, po=True,
               alt=("a stocked guard-position switch in place of the HS6B (RS and Rapid hold UK stock; AutomationDirect "
                    "stocks IDEM interlocks): not chosen yet", 0, 3, "ground", "leadtime-lookups.csv S2-idec; estimate")),
    "S3": dict(new=EST("IDEC e-stops and enclosures"), used=None),
    "S4": dict(new=MCM, used=None, po=True),
    "S5": dict(new=("Thorlabs LW1P1/M: 'Available: Today'", 0, 1, "ground", "leadtime-lookups.csv S5-LW1P1", "vendor page"),
               used=None, po=True),
    "S6": dict(new=("Thorlabs LG1: 'Available: Today'", 0, 1, "ground", "leadtime-lookups.csv S6-LG1", "vendor page"),
               used=None, po=True),
    "S7": dict(new=("Macurco OX-6: not read (Kele and Macurco block automated reads)", None, None, "ground",
                    "leadtime-lookups.csv S7-macurco-OX6", "not found"), used=None),
    "S8": dict(new=MCM, used=None, po=True),
    "S9": dict(new=("McMaster T-slot and sheet from stock; the 12U rack is not chosen yet", 0, 3, "ground",
                    "leadtime-lookups.csv MCM-shipping + estimate", "estimate"), used=None, po=True),
    "F3": dict(new=MCM, used=None, po=True),
    "F4": dict(new=MCM, used=None, po=True),
    "F5": dict(new=MCM, used=None, po=True),
    "P1": dict(new=("McMaster 4083N14: page not readable by script; McMaster ships 98 % of items from stock", 0, 1,
                    "ground", "leadtime-lookups.csv P1-glovebox, MCM-shipping", "vendor statement"), used=None, po=True),
    "T1": dict(new=("Gentec-EO: 'CONTACT SALES' only, no lead time shown", None, None, "ground",
                    "leadtime-lookups.csv T1-gentec", "quote"),
               used=("eBay: Ophir L1500W head from China (7-20 days, estimate) + Nova II meter (US)", 7, 20, "none",
                     "cost/used-options.csv; the China leg is an estimate")),
    "T2": dict(new=("Thorlabs: DMSP1000 and NF1064-44 'Available: Today'; PDA36A2 shows 'Lead Time' (no date)", None,
                    None, "ground", "leadtime-lookups.csv T2-thorlabs (thorlabs.com via the lab Pi)", "vendor page"),
               used=None, po=True),
    "T3": dict(new=("Edmund 57-983: '20+ In Stock' (UK and Canadian sites); Thorlabs VRC2 not checked", 0, 3, "ground",
                    "leadtime-lookups.csv L7-edmund", "vendor page"), used=None),
    "H1": dict(new=("McMaster heaters and thermocouples from stock; Solid Sealing weld-ins: 'Get in touch to place an "
                    "order', no lead time published", None, None, "ground", "leadtime-lookups.csv H1-sst", "quote"),
               used=None, po=True),
    "H2": dict(new=("Digi-Key: Omron K8DT-TH1CD 0 in stock, one expected 03-Mar-2027, 19-week manufacturer lead time "
                    "(CN708: 6 in stock)", 98, 133, "ground", "leadtime-lookups.csv H2-K8DT, H2-CN708", "vendor page"),
               used=None, po=True,
               alt=("the 67F bimetal thermostat (Sensata-Airpax 67F050, $8.33, modules.md) or SOLO SL4848-RR-D ($143) "
                    "in place of the K8DT: stock not checked", 0, 3, "ground", "modules.md; electrical.md; estimate")),
    "H3": dict(new=MCM, used=None, po=True),
    "B1": dict(new=MCM, used=None, po=True),
    "B2": dict(new=MCM, used=None, po=True),
    "B3": dict(new=("MROSupply: 'typically shipped within 1 day' (search snippet; its site was down for maintenance on "
                    "2026-11-25); the SPC-HT pins have no distributor listing: ask SCHUNK", None, None, "ground",
                    "leadtime-lookups.csv B3-schunk", "search snippet"), used=None, po=True),
    "B4": dict(new=EST("SMC valve and fittings", 0, 5), used=None),
    "R1": dict(new=MCM, used=None, po=True),
    "A1": dict(new=("Digi-Key: Omron E3NX-FA41 5 in stock (+402 factory stock; 33 weeks after that); other sensors not "
                    "checked", 0, 1, "ground", "leadtime-lookups.csv A1-E3NX-FA41", "vendor page"), used=None, po=True),
    "A2": dict(new=("McMaster 5572N116 not readable by script (it rides on the McMaster order); Dynabrade 61470 at TA "
                    "Industrial: 'Est. Lead Time: 6 days'; the Edmund and Cloudray slides are a PCard order", 0, 6,
                    "ground", "leadtime-lookups.csv A2-dynabrade-61470, MCM-shipping", "vendor page"), used=None),
    "A3": dict(new=("SMC at Motion: 'In Stock / Factory Order' (read 2026-11-22)", 0, 5, "ground",
                    "analysis/audit/audit-prices.csv", "vendor page"), used=None),
    "D1": dict(new=("Digi-Key: HARTING docking frame 233 in stock, carrier 158 (then 4 weeks)", 0, 1, "ground",
                    "leadtime-lookups.csv D1-harting", "vendor page"), used=None, po=True),
    "D2": dict(new=("Eaton 5PX1500RTG2: CDW 'Item Backordered'; Digi-Key 0 in stock, one expected 15-Dec-2026 (2-week "
                    "lead)", 20, 27, "ground", "leadtime-lookups.csv D2-eaton-5px", "vendor page"),
               used=("eBay, US UPS refurbisher (APC SMX1500RM2U)", 1, 3, "ground", "cost/used-options.csv")),
    "FX": dict(new=MCM, used=None, po=True),
    "E1": dict(new=EST("Socomec disconnect, Eaton breakers, contactors", 0, 5), used=None, po=True),
    "E2": dict(new=EST("AutomationDirect switch", 0, 1), used=None),
    "E3": dict(new=EST("AutomationDirect and Turck sensors", 0, 5), used=None),
    "E4": dict(new=EST("bulk wire and straps"), used=None),
    "E5": dict(new=EST("optional meter, card, feedthrough", 0, 5), used=None),
    "X1": dict(new=("services: see FAB (in-house queue, or SendCutSend 2-5 production days + shipping)", 7, 15, "none",
                    "outsourcing.md section 4; leadtime-lookups.csv X1-sendcutsend", "vendor page"), used=None, po=True),
}
# Fabrication: outsourcing.md section 4 and its route table
FAB = dict(
    queue_split_wk=7.6, queue_all_wk=16.4, shop_h_per_wk=20.0, honing_wk=(3, 6), assembly_wk=(1, 1),
    note="outsourcing.md: 152 h in house on the recommended split (7.6 weeks) or 329 h for everything (16.4 weeks) at 20 "
         "shop hours a week (its assumption: one person half-time on the VF-4 and lathe); outsourced parts arrive in 1-2 "
         "weeks in parallel (SendCutSend: 2-5 production days + shipping; delivered 5-15 days out when quoted on "
         "2026-11-22); the module's honing loop (turn, weld, bore, ship out, hone, ship back) is 3-6 weeks (estimate), "
         "started first. Assembly and the leak check: about a week (estimate)",
)


def days_to_byu(entry, po):
    if entry is None or entry[1] is None:
        return None
    tr = TRANSIT[entry[3]]
    lo, hi = entry[1] + tr[0], entry[2] + tr[1]
    if po:
        lo, hi = lo + PO_DAYS[0], hi + PO_DAYS[1]
    return [lo, hi]


# Orders still at $3,500 or more on the used route: McMaster, Digi-Key (Banner, IDEC, Omron, HARTING, Mean Well),
# MROSupply (SCHUNK) and the services. Thorlabs drops under it once the lens is bought used; eBay buys go on a PCard.
PO_USED = {"M5", "G3", "G5", "G7", "G8", "S4", "S8", "S9", "F3", "F4", "F5", "P1", "H1", "H3", "B1", "B2", "R1", "FX",
           "S1", "S2", "H2", "A1", "D1", "C4", "E1", "B3", "X1"}
SHORT = {  # short HUD strings for the new route (the full text is in LT)
    "L1": "10-12 wk ARO", "L3": "with the laser", "L4": "quote (no >= 500 W catalogue part)",
    "L5": "quote; no published lead", "C1": "quote; no published lead", "L6": "3-4 wk (overseas stock)",
    "G6": "6-8 wk", "G9": "2 wk (made to order)", "G2": "ships same day", "G4": "quote; no gas-tight part found",
    "B3": "modules 1 d (snippet); pins: ask SCHUNK", "H1": "SST weld-ins: no published lead", "T1": "contact sales",
    "T2": "PDA36A2: no date shown", "S2": "27 wk (IDEC HS6B switch)", "H2": "19 wk (Omron K8DT; next 03-Mar-2027)",
    "D2": "backordered (~3-4 wk)", "M3": "2 d to 3 wk", "M1": "Ferrotec: quote", "M4": "Ferrotec: quote",
    "S7": "not read", "X1": "SendCutSend 5-15 d; shop queue 7.6-16.4 wk", "A1": "in stock (5); then 33 wk",
    "S1": "in stock (1); then 4 wk", "G1": "1-7 d", "C5": "in stock, ships same day", "M2": "ships in 3 d",
    "C3": "ships in 3 d", "L2": "not needed (air-cooled laser)",
    "B1": "stock same or next day; honing outside 3-6 wk (estimate)",
}
SHORT_USED = {"L1": "ships same day; ~1 wk freight", "T1": "1-3 wk (head from China)"}


def recheck_days():
    """{line: (days_lo, days_hi, text)} from ebay-recheck.csv: eBay's own delivery window to Provo (84602) for the
    line's live used pick on 2026-11-25 (the low pick if it is still listed, else the high pick)."""
    import csv
    import pathlib
    f = pathlib.Path(__file__).resolve().parent / "ebay-recheck.csv"
    out = {}
    if not f.exists():
        return out
    rows = [r for r in csv.DictReader(open(f)) if r["status_2026_11_25"] == "still listed" and r["days_to_provo_low"]
            and r["pick"]]
    rows.sort(key=lambda r: 0 if "low" in r["pick"] else 1)
    for r in rows:
        line = r["replaces"].split(":")[0]
        if line not in out:
            out[line] = (int(r["days_to_provo_low"]), int(r["days_to_provo_high"]),
                         f"eBay ({r['item_as_listed'][:48]}): '{r['delivery_to_84602_as_listed']}' to Provo, read "
                         f"{r['fetched_utc']}; {r['returns_as_listed'].rstrip('.')}")
    return out


RECHECK = recheck_days()


def lead_rows(bom_rows):
    """{line: row} for every bom.csv line: the new and used routes' text, source and days to BYU."""
    out = {}
    for line, b in bom_rows.items():
        e = dict(LT.get(line, dict(new=EST(line), used=None)))
        if line in RECHECK and line != "L1" and e.get("used"):  # L1 ships by freight: no date on the listing
            lo, hi, txt = RECHECK[line]
            e["used"] = (txt, lo, hi, "none", "analysis/robotbuild_data/ebay-recheck.csv")
        po = bool(e.get("po"))
        po_u = line in PO_USED
        if line in SHORT:
            short = SHORT[line]
        elif e["new"] is MCM:
            short = "same or next day"
        else:
            d = days_to_byu(e["new"], False)
            short = (f"{d[0]}-{d[1]} d" if d and d[1] < 21 else f"{round(d[0] / 7)}-{round(d[1] / 7)} wk" if d else "TBD")
        used_days = days_to_byu(e["used"], False) if e.get("used") else None
        out[line] = dict(line=line, item=b["item"], po_new=po, po_used=po_u if not e.get("used") else False,
                         new_text=e["new"][0], new_source=e["new"][4], new_basis=e["new"][5],
                         days_new=days_to_byu(e["new"], po), days_new_vendor=days_to_byu(e["new"], False),
                         short_new=short + (" + BYU PO" if po else ""),
                         used_text=e["used"][0] if e.get("used") else "",
                         used_source=e["used"][4] if e.get("used") else "",
                         days_used=used_days,
                         # what the used route waits for on this line: the used listing, else the line bought new with
                         # the used route's purchase orders (and the stocked swap for S2 and H2)
                         days_used_route=(used_days if used_days else
                                          days_to_byu(e["alt"], po_u) if e.get("alt") and line in ("S2", "H2") else
                                          days_to_byu(e["new"], po_u)),
                         short_used=(SHORT_USED.get(line, (f"{used_days[0]} d" if used_days[0] == used_days[1] else f"{used_days[0]}-{used_days[1]} d") + " (used, US)") if used_days
                                     else ("stocked swap" if line in ("S2", "H2") else "same as new")),
                         alt_text=e["alt"][0] if e.get("alt") else "", alt_source=e["alt"][4] if e.get("alt") else "",
                         days_alt=days_to_byu(e["alt"], po) if e.get("alt") else None)
    return out


def schedule(leads, bom_rows):
    """Weeks from go to 'all bought parts in hand' and to 'assembled', for three routes, with what sets each."""
    stock = leads["F4"]["days_new"]  # McMaster stock (on a PO) gates the start of machining
    out = {}
    for name, use_used, swaps in (("new", False, False), ("new_with_swaps", False, True), ("used", True, True)):
        worst, unknown = [], []
        for line, r in leads.items():
            if line in ("X1", "L3"):  # X1 is the fabrication path; L3 rides on the laser order
                continue
            if use_used:
                d = r["days_used_route"]
            else:
                d = r["days_alt"] if (swaps and r["days_alt"] and line in ("S2", "H2")) else r["days_new"]
            if d is None:
                unknown.append(line)
                continue
            worst.append((d[1], d[0], line))
        worst.sort(reverse=True)
        hi, lo, line = worst[0]
        parts = [round(lo / 7, 1), round(hi / 7, 1)]
        fab_split = [round(stock[0] / 7 + FAB["queue_split_wk"], 1), round(stock[1] / 7 + FAB["queue_split_wk"], 1)]
        fab_all = [round(stock[0] / 7 + FAB["queue_all_wk"], 1), round(stock[1] / 7 + FAB["queue_all_wk"], 1)]
        a = FAB["assembly_wk"]
        out[name] = dict(
            parts_in_hand_wk=parts, set_by=line, set_by_item=bom_rows[line]["item"],
            next=[dict(line=l2, item=bom_rows[l2]["item"], wk=[round(x / 7, 1), round(y / 7, 1)]) for y, x, l2 in worst[1:7]],
            unknown=unknown, fabrication_split_wk=fab_split, fabrication_all_in_house_wk=fab_all,
            critical_split=f"purchases ({line})" if parts[1] > fab_split[1] else "fabrication (recommended split)",
            critical_all_in_house=f"purchases ({line})" if parts[1] > fab_all[1] else "fabrication (all in house)",
            ready_split_wk=[round(max(parts[0], fab_split[0]) + a[0], 1), round(max(parts[1], fab_split[1]) + a[1], 1)],
            ready_all_in_house_wk=[round(max(parts[0], fab_all[0]) + a[0], 1), round(max(parts[1], fab_all[1]) + a[1], 1)])
    return dict(routes=out, fab=FAB, po_days=PO_DAYS, transit=TRANSIT,
                assumptions="'new' buys every line new as chosen in bom.csv; 'new_with_swaps' swaps the two long-lead "
                            "switches (S2's HS6B-12B05, H2's K8DT-TH1CD) for stocked parts; 'used' also takes the used "
                            "picks. Lines with no stated lead time are listed in 'unknown' and left out of the maximum. "
                            "Machining starts when the McMaster stock arrives (PO + delivery). Assembly and the leak "
                            "check add about a week (estimate).")


# Cheap parts whose stock sets or threatens the schedule (leadtime-lookups.csv, Digi-Key and vendor pages, 2026-11-25)
LEAD_RISKS = [
    dict(line="S2", part="IDEC HS6B-12B05 guard-position switch", usd=123.45,
         stated="Digi-Key: 'not kept in stock'; Manufacturer Standard Lead Time 27 Weeks",
         action="swap for a stocked guard-position switch before ordering (the longest lead in bom.csv as chosen)"),
    dict(line="H2", part="Omron K8DT-TH1CD plate-temperature relay (door channel)", usd=240.25,
         stated="Digi-Key: In-Stock 0; 1 expected 03-Mar-2027; Manufacturer Standard Lead Time 19 Weeks",
         action="use the 67F bimetal thermostat (modules.md, $8.33) or SOLO SL4848-RR-D ($143), or order on day one"),
    dict(line="A1", part="Omron E3NX-FA41 fibre amplifier", usd=353.03,
         stated="Digi-Key: In-Stock 5; Factory Stock 402; Manufacturer Standard Lead Time 33 Weeks",
         action="order now while stock lasts"),
    dict(line="S2", part="IDEC HS5L-VC44M-G guard lock", usd=254.19,
         stated="Digi-Key: In-Stock 3; Manufacturer Standard Lead Time 16 Weeks", action="order now while stock lasts"),
    dict(line="H2", part="DwyerOmega CN708 limit controller", usd=212.78,
         stated="Digi-Key: In-Stock 6; Manufacturer Standard Lead Time 12 Weeks", action="order now while stock lasts"),
    dict(line="S1", part="Banner XS26-2 safety controller", usd=1093.01,
         stated="Digi-Key: In-Stock 1; Manufacturer Standard Lead Time 4 Weeks", action="order now; 4 weeks if missed"),
    dict(line="D2", part="Eaton 5PX1500RTG2 UPS", usd=1137.99,
         stated="CDW: 'Item Backordered'; Digi-Key: In-Stock 0, 1 expected 15-Dec-2026",
         action="or a refurbished APC SMX1500RM2U ($449.99, eBay) or the Vertiv GXT5 (in stock at one reseller, snippet)"),
    dict(line="G6", part="Ntron Microx trace O2 analyzer", usd=2091.0, stated="Instrumart: 'Usually ships in 6-8 weeks'",
         action="order early, or a used Teledyne 3190 / Alpha Omega 3000 with a new cell"),
    dict(line="L6", part="Thorlabs FTH160-1064 f-theta lens and windows", usd=1255.84,
         stated="Thorlabs: 'In Stock Overseas'; transfers typically take 3-4 weeks", action="order early"),
    dict(line="G9", part="Vaisala DMT143 dew-point transmitter", usd=2281.70,
         stated="Selectum: '2 Weeks Factory Lead Time'; made to order, non-returnable and non-cancelable",
         action="fix the configuration before ordering"),
]
