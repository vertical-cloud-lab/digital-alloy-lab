# Completeness audit: every part in the model against the BOM (2026-11-22)

For [PR #266](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/266) (issue #260), in answer to Sterling's
question: "Have you been thorough in terms of both mechanical and electrical components? And optical of course".
This note covers the mechanical and whole-machine side. The electrical design and the optics audit are separate notes.
Nothing here has been built, quoted by a shop or reviewed by BYU's LSO or EHS.

## Short answer

**Before this audit, no.** The model's part list (`analysis/out/mass.json`, 223 parts) was checked part by part
against `bom.csv` and the part-number lists. At the start of the audit (bom.csv as committed in `cc1e0a1`):
- **87** parts were real parts with a vendor price and **26** were custom parts costed in a BOM line;
- **71** parts were in no bom.csv line at all, and **29** contradicted their BOM line;
- the BOM still described the tall model's welded box, 30 mm T-slot cabinet and ball-screw piston (G1, S9, M3), and
  the model tagged parts with lines that did not exist (D1, F3, F4, F5).

**Now**, with the electrical and optics workers' rows merged into bom.csv (07:02 UTC): 117 priced, 4 real but unpriced,
26 generic, 65 custom, **1 missing** and **9 inconsistent**. The BOM total goes from **$39,440 – $112,978** to
**$70,478 – $154,119**. $7,708 – $20,770 of the rise is line X1, the machining no line costed before; without X1 the
total is $62,770 – $133,349. Before the merge, this audit's own changes alone gave $58,132 – $144,632.

## How it was checked

[`analysis/audit/completeness.py`](analysis/audit/completeness.py) reads:
- the part list in `analysis/out/mass.json`;
- each part's own BOM tag and part number (`bom`, `mcm` in `cad/lpbf_low.py`), dumped to
  [`analysis/out/audit/model_tags.json`](analysis/out/audit/model_tags.json) from a snapshot of `97882b9` (the 12U-rack model; first run on `cc1e0a1`).

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
python desktop-lpbf/analysis/audit/completeness.py --tag bomonly                 # bom.csv and the repo's part lists only
python desktop-lpbf/analysis/audit/completeness.py desktop-lpbf/electrical-bom.csv desktop-lpbf/optics-bom.csv   # writes this note
python desktop-lpbf/analysis/audit/completeness.py --dump-tags SNAPSHOT_REPO     # re-dump the model's tags (CadQuery, ~25 s)
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
   - **Rack:** the model's rack is now 12U and 560 mm tall, for the electrical design's 4U drawer (the XS26 safety
     controller stands 129 mm off its rail). No 12U rack that low was priced: McMaster's 7648K62 cabinet is 10U
     ($609.03), its next size is 30 in. tall and its open racks start at 24U. S9 carries a $250-650 estimate.
5. **Optics (merged from `optics-bom.csv`):**
   - L6 is now the Thorlabs FTH160-1064 the model uses (it said f = 254 mm).
   - L3 now asks IPG for a ~3.2 mm beam: the 5 mm collimator the model still draws gives ~48 µm at f = 160 mm, not 75 µm.
     IPG's 2.5 mm collimator (~96 µm) is the fallback. Not priced.
   - The camera window becomes a plain window with a Thorlabs FESH0950 filter (M6), and the main window an Edmund 38-990
     (Ø50.8 × 9.53 mm, against 8 mm drawn).
6. **Electrical (merged from `analysis/out/electrical/bom_proposed_rows.csv`):**
   - No 2U scan/laser PC is chosen (C1 is the RTC6 card): the one part still in no line.
   - C6 is now the 4U drawer the model draws. The model still tags the UPS C6.
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
    - The hinge is labelled 1151A87 but drawn as custom knuckles, and the HSS blade still carries the 18-8 shim's
      part number (9011K104) in the model.
    - H1's 2317K275 shim is 0.13 mm thick, against the 0.3 mm shields the model draws.

## What changed in bom.csv

- **Rewritten for the low-profile model:**
  - G1 chamber: through-frame stock, floor, lid and door blanks, latches;
  - G2 dry scroll pump;
  - G7 Pirani, 316 relief and SAE-4 adapters; G8 seals from `seal-parts.csv`; G9 Vaisala DMT143;
  - M1 Ferrotec feedthrough; M2 ClearPath part number; M3 THK KR26 Z actuator; M4 roller feedthrough and overflow jar;
    M5 HSS blank; M6 Pi HQ camera (the lens is left to the optics audit, `optics-bom.csv` O20);
  - S9 rack, 20 mm guard frame and sliding door;
  - S7 the fixed Macurco OX-6 room O2 monitor that `safety-parts.csv` SP1 asks for, in place of the portable 18995T81;
  - G4 a note only: still no gas-tight blower;
  - B2 wipers and bore seals; R1 the KF-16 blank (estimate).
- **Added:** F3 levelling mounts, F4 MIC-6 base plates, F5 optics bridge, H3 module fan (`heat.md`), A3 pneumatics,
  D1 dock and umbilicals, D2 UPS, X1 machining.
- **Merged from the electrical design:** C1, C3, C4, C5, C6, S1, S2, S3, S4, H1, H2, A1 and A3, and new lines E1-E5
  (E5 is optional: $0 at the low end).
- **Merged from the optics audit:** L6, L7, A2 (AR-coated slides), T1, T2, M6 (plus the drawn LED bar the optics list
  leaves out, $20-60), F5 (focus shims and field-stop inserts) and a new T3 (calibration tools); text changes in L3, L4
  and L5.
- **Sources:** every fetched price is in [`analysis/audit/audit-prices.csv`](analysis/audit/audit-prices.csv), with its
  URL and UTC time. The prices were read on 2026-11-22 between 05:35 and 06:05 UTC; McMaster's and the plate distributor's through the lab tunnel.
  Estimates are marked "ESTIMATE" there and "estimate" in `price_basis`.
- **Stale rows left in place:** the tall model's rows in `mcmaster-parts.csv` still exist. These are the G1, S9 and M3
  rows, the 9572K33 V-ring, the 1165N11 cord and the 4277T52 nylon relief. Their lines now say they no longer apply.
  They show up in the reverse table below as rows with no model part.

## How the overlaps with the electrical and optics lists were settled (07:02 UTC)

Every item is counted once, in one bom.csv line:
- **UPS:** in D2 only. `electrical-bom.csv` E9-12 is the same Eaton at qty 0; its network card is optional in E5.
- **Pneumatics:** in A3 only, as the electrical worker's A3 row: this audit's SMC parts plus a pressure switch, a lockable
  dump valve and two D-M9B switches. The Mindman/NITRA set in E8 is not added.
- **Dock:** in D1 only. The low end is E7's HARTING Han-Modular frame and modules ($261.26) plus a $50 argon coupling
  estimate; the high end is a Stäubli CombiTac.
- **Vacuum gauge:** in G7 only (Vacuum Research 902377, $455). E9-11's Kurt J. Lesker 275i ($515) is the alternative.
- **Rack:** 12U in S9, as above.
- **Where a proposed row listed only its additions** (C1, S3, S4, H1, A1, A3), the line keeps its earlier candidate text in
  front of them, so the README table still names every part.
