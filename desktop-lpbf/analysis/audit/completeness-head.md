# Completeness audit: every part in the model against the BOM (2026-11-22)

For [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to Sterling's
question: "Have you been thorough in terms of both mechanical and electrical components? And optical of course".
This note covers the mechanical and whole-machine side. The electrical design and the optics audit are separate notes.
Nothing here has been built, quoted by a shop or reviewed by BYU's LSO or EHS.

## Short answer

**Before this audit, no.** The model's part list (`analysis/out/mass.json`, 223 parts) was checked part by part
against `bom.csv` and the part-number lists. At the start of the audit (bom.csv as committed in `cc1e0a1`):
- **87** parts were real parts with a vendor price and **26** were custom parts costed in a BOM line;
- **70** parts were in no bom.csv line at all, and **29** contradicted their BOM line;
- the BOM still described the tall model's welded box, 30 mm T-slot cabinet and ball-screw piston (G1, S9, M3), and
  the model tagged parts with lines that did not exist (D1, F3, F4, F5).

**Now:** 117 priced, 4 real but unpriced, 22 generic, 65 custom, **2 missing** and **12 inconsistent**. The BOM total
goes from **$39,440 – $112,978** to **$58,132 – $144,632**. $7,708 – $20,770 of the rise is line X1, the machining no
line costed before. Without X1 the total is $50,424 – $123,862.

## How it was checked

[`analysis/audit/completeness.py`](analysis/audit/completeness.py) reads:
- the part list in `analysis/out/mass.json`;
- each part's own BOM tag and part number (`bom`, `mcm` in `cad/lpbf_low.py`), dumped to
  [`analysis/out/audit/model_tags.json`](analysis/out/audit/model_tags.json) from a snapshot of `cc1e0a1`.

It maps every part to a bom.csv line and to rows of `mcmaster-parts.csv`, `fasteners.csv`, `seal-parts.csv`,
`vendor-parts.csv`, `safety-parts.csv`, `robot-tooling.csv`, `assembly-tooling.csv`, `options-*.csv`,
`plate-materials.csv`, `vendor-lookups.csv` and this audit's [`analysis/audit/audit-prices.csv`](analysis/audit/audit-prices.csv).
- **By part number** where the name or tag has one (McMaster `\d{4,5}[A-Z]\d{1,4}`, AS568 dash numbers `2-xxx`, vendor
  part numbers).
- **By an explicit table** in the script for the rest. Each entry names the line and a keyword that the line's text must
  contain, so a stale line fails the check.
- **Model-vs-BOM rules** flag a part as inconsistent when the model and its line (or another analysis) disagree.
- **Custom parts** come from `analysis/out/machining/hours.csv` (48 machined parts) and the sheet parts of
  `cad/render_build.kind()`.

Any CSV named on the command line is read as an extra purchase list. That is how `electrical-bom.csv` and
`optics-bom.csv` are folded in when they exist. Re-run:

```bash
python desktop-lpbf/analysis/audit/completeness.py --bom desktop-lpbf/analysis/out/audit/bom_before.csv --no-audit-prices --tag before
python desktop-lpbf/analysis/audit/completeness.py [desktop-lpbf/electrical-bom.csv desktop-lpbf/optics-bom.csv]
python desktop-lpbf/analysis/audit/completeness.py --dump-tags SNAPSHOT_REPO   # re-dump the model's tags (CadQuery, ~25 s)
```

## The gaps that matter most

1. **No gas-tight recirculation blower exists in the BOM (G4).**
   - The CFD needs 140-200 L/min at 1.5-3 kPa through a sealed loop (`gas-flow.md`).
   - G4 is still a $300-1,500 estimate. The model's envelope is labelled ~100 L/min, which is the pre-CFD figure.
   - This is the one purchase the gas loop cannot work without.
2. **Machining was not costed.** Of the 249.5 h in `hours.csv`, 177.7 h belonged to parts that no line costed: the
   chamber group, base plates, optics bridge, recoater and Z parts, and the robot hardware.
   - X1 now carries them, plus 15-30 h for the sheet parts, at an **assumed** $40-100/h. No shop has quoted.
   - The build modules, metering base, blade holder and reservoir lids are left out of X1: their lines already carry
     machining.
3. **The vacuum pump changes price class.**
   - The model draws a 26 kg dry scroll. G2 had priced the $587.53 McMaster 4396K21 rotary-vane pump.
   - G2 is now an Edwards nXDS6i ($5,977.85, Marshall Scientific; 26.2 kg, 0.02 mbar) or an Agilent IDP-3 ($3,979 list,
     search snippet).
   - `analysis/out/tray/tray_budget.md` still uses the 4396K21's 7 A at 115 V.
4. **Three decisions are still open in the model.**
   - **Cooling:** chilled-water lines run to a laser that IPG quotes as air-cooled (`heat.md` says decide first).
   - **UPS:** the model draws an Eaton 5PX1500RTG2 ($1,137.99) but the tray budget sizes a Vertiv GXT5LI-1500
     ($2,706.99). D2 lists both.
   - **Rack:** the model's 11U rack, 515 mm tall, has no catalogue match. McMaster's 7648K62 cabinet is 10U and
     495 mm tall ($609.03). Its next size is 30 in. tall, and its open racks start at 24U. So either the 3U DIN drawer
     becomes 2U or the rack is a custom frame.
5. **For the optics audit:**
   - L6 still specifies f = 254 mm, while the model uses the Thorlabs FTH160-1064 (f = 160 mm).
   - The IPG 5 mm collimator in the model and L3 gives ~48 µm at f = 160 mm, not 75 µm. `low-profile.md` §2 calls for a
     ~3.2 mm beam.
   - The camera window (Ø1 in., 1070 nm blocking coating) is in no line.
   - The Ø2 in. × 8 mm main window has no part number: L7 names a Ø1 in. WG41050-C.
6. **For the electrical design:**
   - No 2U scan/laser PC is chosen (C1 is the RTC6 card).
   - C6 is a NEMA wall box, but the model draws a 3U DIN-rail drawer.
   - The model tags the UPS C6.
   - A1's load cell is 3 kg; the model's label says 2 kg.
7. **Vacuum feedthroughs and connectors have no price.**
   - The two Ferrotec magnetic-fluid feedthroughs (SFL-006-NN on the recoater, SSL-005-NN on the roller) have no
     published price. They are estimated at $500-1,500 and $400-1,000, against Rigaku's $921.57 alternative.
   - The drawn LEMO 1B rod-end connector fails the seal spec (`seal-parts.csv`).
8. **Chamber stock.** McMaster sells no 6061 plate thicker than 4 in. Midwest Steel & Aluminum cuts the 5-1/2 x 9.5 x
   15 in. 6061-T651 frame blank for $590.89 (read 2026-11-22), so G1 now names a distributor for it.
9. **Small parts with no catalogue match:**
   - the drawer's quarter-turn latches (`seals.md`);
   - a 316 SS 0.5 psi relief with an FKM seat (McMaster's stainless reliefs start at 25 psi);
   - an SAE-4 adapter for the 3861N11 transmitter;
   - KF-25 adapters for the HEPA housing's 1/2 NPSC ports and for the blower;
   - two shaft couplings, Dowty-type bonded washers and 1 mm FKM sheet;
   - the CombiTac tray half (no public price; D1 estimates $1,500-5,000).
10. **Smaller fit notes:**
    - The optics posts are drawn 60 × 60 × 5 mm. McMaster's nearest is 2-1/2 × 1/4 in. (6546K31).
    - THK's KR26 rail is nominally 26 mm wide, against the 46 × 28 mm Z envelope.
    - The SMC door actuator weighs 0.60 kg, against the 0.3 kg the model assumes.
    - The hinge is labelled 1151A87 but drawn as custom knuckles.
    - H1's 2317K275 shim is 0.13 mm thick, against the 0.3 mm shields the model draws.

## What changed in bom.csv

- **Rewritten for the low-profile model:**
  - G1 chamber: through-frame stock, floor, lid and door blanks, latches;
  - G2 dry scroll pump;
  - G7 Pirani, 316 relief and SAE-4 adapters; G8 seals from `seal-parts.csv`; G9 Vaisala DMT143;
  - M1 Ferrotec feedthrough; M2 ClearPath part number; M3 THK KR26 Z actuator; M4 roller feedthrough and overflow jar;
    M5 HSS blank; M6 Pi HQ camera and 16 mm lens (Adafruit);
  - S9 rack, 20 mm guard frame and sliding door;
  - S7 the fixed Macurco OX-6 room O2 monitor that `safety-parts.csv` SP1 asks for, in place of the portable 18995T81;
  - G4 a note only: still no gas-tight blower;
  - B2 wipers and bore seals; R1 the KF-16 blank (estimate).
- **Added:** F3 levelling mounts, F4 MIC-6 base plates, F5 optics bridge, H3 module fan (`heat.md`), A3 pneumatics,
  D1 dock and umbilicals, D2 UPS, X1 machining.
- **Not touched:** C1-C6, S1-S4, H2, A1, L1-L7, S5, S6, T1 and T2, which are the electrical and optics lines.
- **Sources:** every fetched price is in [`analysis/audit/audit-prices.csv`](analysis/audit/audit-prices.csv), with its
  URL and UTC time. The prices were read on 2026-11-22 between 05:35 and 05:56 UTC, McMaster's through the lab tunnel.
  Estimates are marked "ESTIMATE" there and "estimate" in `price_basis`.
- **Stale rows left in place:** the tall model's rows in `mcmaster-parts.csv` still exist. These are the G1, S9 and M3
  rows, the 9572K33 V-ring, the 1165N11 cord and the 4277T52 nylon relief. Their lines now say they no longer apply.
  They show up in the reverse table below as rows with no model part.
