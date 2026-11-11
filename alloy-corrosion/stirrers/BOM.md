# What to order: the copper corrosion setup with four stir modules

Ben asked on [#180](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/180) (2026-11-06)
for a BOM to start ordering now: the corrosion setup on the CubXL, with four of
[byu-vcl#269](https://github.com/vertical-cloud-lab/byu-vcl/pull/269)'s compact stir modules in a
column on the deck ([`README.md`](README.md)). As he asked, it leaves out the potentiostat (Dr.
Porter's EZstat-Pro is set up) and the 20 µL tips (enough for a few tests).

- **It covers the copper plan,** which Sterling put first on 22 October. The aluminium plan needs
  one more row (NaCl, below).
- **The corrosion rows come from [`../bom/bom.csv`](../bom/bom.csv),** with its IDs, links and
  prices. [`order_list.py`](order_list.py) reads them from there and adds the stirrer rows, so the
  two lists can't drift apart. It writes [`order-list.csv`](order-list.csv) and
  [`order-totals.json`](order-totals.json).
- **Prices were seen on 2026-10-19,** before shipping and tax. Amazon's change often, so check each
  at checkout. Several vendors block scripts, so their prices came from search snippets (the
  `link_check` column of `../bom/bom.csv` says which).

**Nothing in this list has been ordered.**

## Total

| | Cost |
| --- | --- |
| Corrosion setup: cell, deck, electrodes, chemicals, reference alloys, polishing film, tubes | **$2,025.53** |
| Four stir modules, beyond what ME order 13518 brought | **$47.26** ($40.27 if the 100 nF kit, ST4, is already ordered) |
| **To order now** | **$2,072.79**, plus three rows with no price yet (below) |

Of that, $261 is a placeholder for the leak-free reference (B19) until it's quoted, and $60 for
the sodium sulfide (B39) is an estimate. Still to price: the C95800 bar (B45, quote only), and the
drill rod (B10) and PTFE rod (B46), whose McMaster prices couldn't be read.

## 1. Order, by vendor

| ID | Item | Qty | Part number and link | Price, USD |
| --- | --- | --- | --- | --- |
| **Government Scientific Source** | | | | **328.00** |
| B38 | ASTM D1141 substitute ocean water **without** heavy metals, 4 L (Ricca 8363-1) | 1 | [8363-1](https://www.govsci.com/product-detail/Ricca--Chemical/8363-1/EA) | 135.00 |
| B41 | Nitric acid, TraceMetal grade, 500 mL | 1 | [A509P500](https://www.govsci.com/product-detail/Fisher--Scientific/A509P500/EA/) | 193.00 (hazmat shipping) |
| **OnlineMetals** | | | | **326.50** |
| B43 | C71500 (70/30 Cu–Ni) round bar, 1 in × 12 in | 1 | [mp-00059842](https://www.onlinemetals.com/en/buy/copper/1-inch-od-copper-nickel-round-bar-715/pid/mp-00059842) | 121.34 |
| B44 | C70600 (90/10 Cu–Ni) round bar, 1 in | 1 | [mp-00068387](https://www.onlinemetals.com/en/buy/copper-nickel-round-bar) | 205.16 |
| **PACE Technologies** | | | | **265.00** |
| B29 | Diamond lapping film, 0.1 µm, 12 in PSA, 3 per pack (copper's own, per the polishing SOP) | 1 | [PDAA-01P12](https://shop.metallographic.com/products/pdaa-01p12) | 265.00 |
| **Innovative Instruments** | | | | **261.00** |
| B19 | Leak-free Ag/AgCl reference, 2.0 mm OD, custom: 15.5 mm barrel with a bare silver-wire lead (16.6 mm at most) | 1 | [LF-2, custom length](https://www.2in.com/products/reference/reference.html) | 261.00 (budget; **ask for a quote**) |
| **Advent Research Materials** | | | | **216.00** |
| B21 | Platinum wire, 0.25 mm, 99.95 %, 0.2 m | 1 | [PT543404](https://www.advent-rm.com/en-gb/products/pure-metals/platinum/form/wire/line/pt5434) | 216.00 |
| **Ossila** | | | | **165.00** |
| B20 | Master reference, fritted Ag/AgCl, 6 mm glass body | 1 | [C2015B1](https://www.ossila.com/products/ag-agcl-reference-electrode) | 165.00 |
| **Fisher Scientific** | | | | **108.90** |
| B36 | 0.5 mL PP tubes with Safe-Lock caps, 500 (Eppendorf 022363611) | 1 | [05-402-18](https://www.fishersci.com/shop/products/snap-cap-microcentrifuge-safe-lock-tubes/p-194501) | 108.90 |
| **AquaPhoenix Scientific** | | | | **92.43** |
| B40 | CHEMets sulfide kit K-9510 (methylene blue, 0–1 and 1–10 mg/L, 30 tests) | 1 | [K-9510](https://catalog.aquaphoenixsci.com/products/testing-supplies/test-kits/k-9510-sulfide-total-soluble) | 92.43 |
| **Sigma-Aldrich** | | | | **60.00** |
| B39 | Sodium sulfide nonahydrate, ACS ≥ 98 %, 100 g | 1 | [208043-100G](https://www.sigmaaldrich.com/US/en/product/sigald/208043) | 60.00 (estimate) |
| **totalElement** | | | | **52.78** |
| B08 | NdFeB disc magnets, 4 × 2 mm, N52, 250 | 1 | [D4X2MMN52-250PK](https://totalelement.com/products/4mm-x-2mm-neodymium-rare-earth-permanent-disc-magnets-n52-250-pack) | 24.99 |
| B09 | Steel discs, 1 in × 1 mm, with 3M adhesive, 50 | 1 | [SP13M-50PK](https://totalelement.com/products/1-inch-steel-disc-with-3m-adhesive-blank-metal-strike-plates-50-pack) | 27.79 |
| **The O-Ring Store** | | | | **52.00** |
| B01 | FKM O-ring AS568-006 (2.90 ID × 1.78), FDA brown Viton 75, 100 | 1 | [FDABV75006](https://www.theoringstore.com/store/index.php?main_page=product_info&cPath=367_2040_2039&products_id=38308) | 9.00 |
| B02 | FKM O-ring AS568-008 (4.47 ID), 100 | 1 | [FDABV75008](https://www.theoringstore.com/store/index.php?main_page=product_info&cPath=367_2040_2039&products_id=38310) | 10.00 |
| B03 | FKM O-ring AS568-010 (6.07 ID), 100 | 1 | [FDABV75010](https://www.theoringstore.com/store/index.php?main_page=product_info&cPath=367_2040_2039&products_id=38312) | 13.00 |
| B04 | FKM O-ring AS568-013 (10.82 ID), 100, for the bench cell | 1 | [FDABV75013](https://www.theoringstore.com/store/index.php?main_page=product_info&cPath=367_2040_2039&products_id=38315) | 20.00 |
| **Amazon** (the stir modules) | | | | **47.26** |
| ST1 | Fan, Orion OD4010-12HSS, 40 × 40 × 10.5 mm, 12 V, 2-wire | 3 | [B00JJ402HY](https://www.amazon.com/dp/B00JJ402HY) | 22.29 |
| ST2 | Cable, 22 AWG, 4 conductors, stranded, 10 ft | 1 | [B0BVQ7ZNCQ](https://www.amazon.com/dp/B0BVQ7ZNCQ) | 7.99 |
| ST3 | Socket head screw kit, M3, 304 stainless, 6–30 mm, 540 pieces | 1 | [B0D4L6QRZB](https://www.amazon.com/dp/B0D4L6QRZB) | 9.99 |
| ST4 | Capacitor kit, 1206 chip, 16 values (the Hall sensor's 100 nF) | 1 | [B06XDHC93D](https://www.amazon.com/dp/B06XDHC93D) | 6.99 (**only if not ordered yet**) |
| **Digi-Key** | | | | **43.95** |
| B06 | Low-force spring pin for the electrode cap (Same Sky CPG-37-TH-TR) | 10 | [CPG-37-TH-TR](https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/CPG-37-TH-TR/25666017) | 8.21 |
| B11 | Copper foil tape 3M 1181, 1/4 in × 18 yd, conductive adhesive | 1 | [3M1181A-ND](https://www.digikey.com/en/products/detail/3m/1181-X-1-4/30708) | 33.93 |
| B26 | Dummy cell: 10 kΩ 0.1 % resistor and 1 µF film capacitor | 1 + 1 | [MFP-25BRD52-10K](https://www.digikey.com/en/products/detail/yageo/MFP-25BRD52-10K/2058797), [ECQ-E1105KF](https://www.digikey.com/en/products/detail/panasonic-industry/ECQ-E1105KF/56380) | 1.81 |
| **Adafruit** | | | | **22.35** |
| B07 | Pogo pins P75-B1, 10-pack | 2 | [2430](https://www.adafruit.com/product/2430) | 9.90 |
| B15 | Wire-wrap wire, 30 AWG, 200 m | 1 | [1446](https://www.adafruit.com/product/1446) | 7.50 |
| B16 | Silicone hookup wire, 26 AWG, 25 ft | 1 | [2517](https://www.adafruit.com/product/2517) | 4.95 |
| **ShowMeCables** | | | | **14.19** |
| B17 | Shielded cable, 4 × 24 AWG, foil and drain (Belden 9534), per foot | 3 ft | [Belden 9534](https://www.showmecables.com/belden-9534-4-conductors-24-awg-shielded-pvc-computer-cable-for-eia-rs-232) | 14.19 |
| **ChemicalStore (MiniScience)** | | | | **8.00** |
| B22 | Graphite rod, 10 × 100 mm (bench-cell counter) | 2 | [GR4BAR10X100](https://us.chemicalstore.com/carbon-electrode-graphite-rod-high-purity-density-and-conductivity-10-mm-x-100-mm) | 8.00 |
| **McMaster-Carr** | | | | **5.45** + 2 unread |
| B10 | Drill rod, 3 mm, O1 tool steel, 3 ft (or any 3 mm steel pin) | 1 | [88625K62](https://www.mcmaster.com/88625K62/) | not read |
| B14 | Socket head screws, M3 × 8, 18-8 stainless, 100 | 1 | [91292A112](https://www.mcmaster.com/91292A112/) | 5.45 |
| B46 | PTFE rod, 3/4 in, 1 ft (the S4 blank) | 1 | [8546K15](https://www.mcmaster.com/8546K15/) | not read |
| **Ace Hardware** | | | | **1.99** |
| B12 | Brass rod, 1/16 in × 12 in, 3-pack | 1 | [K&S 8162](https://www.acehardware.com/departments/hardware/metal-sheets-and-rods/brass-rods/5172754) | 1.99 |
| **Zoro** | | | | **1.99** |
| B47 | Drill #46 (2.06 mm), HSS jobber | 1 | [Chicago-Latrobe 45716](https://www.zoro.com/chicago-latrobe-135-degree-heavy-duty-jobber-length-drill-chicago-latrobe-150asp-steam-oxide-hss-rhsrhc-no-46-45716/i/G1828906/) | 1.99 |
| **Atlas Bronze** | | | | quote |
| B45 | C95800 nickel-aluminium bronze, continuous-cast bar about 1 in (ASTM B505); ask for the mill cert | 1 | [C95800](https://www.atlasbronze.com/C95800-Product-Sheet-s/473874.htm) | **quote** |

Notes on the order:

- **Start the long ones first:** the B19 quote (custom length; what to ask for is in
  [`../bom/README.md`](../bom/README.md#electrodes)), the B45 quote, and B41, which ships as hazmat.
- **B01–B04 can come from Filters4You instead** (checked 2026-11-11): their own-brand "Viton
  (FKM) 75A" in the same four sizes, $5.99 per 10-pack, against $52 for 100 of each here. Same
  size and hardness, but the compound isn't stated, so buy all four sizes from them, and the 25-pack
  ($8.99) of the -006 if each spot gets a fresh ring. They take orders by e-mail request, not a
  cart. Details in [`../bom/README.md`](../bom/README.md#o-rings-from-filters4you).
- **B17's length assumes the EZstat-Pro sits beside the deck's back edge.** Measure from the tray's
  back edge (x 222, y 260) to where the EZstat sits, and order that length. It is sold by the foot.
- **ST1:** stirrer B takes ME order 13518's second fan, so two are needed, for C and D, and the
  third is a spare. Amazon had only 4 on 2026-10-19; Digi-Key 1053-1205-ND is the same fan.
- **ST2:** about 1.5 m per stirrer, as byu-vcl#269 assumed. What's left of ME order 13518's pack
  covers one more stirrer and this pack two. Measure the route first, and buy two packs if it is
  longer than 1.5 m.
- **ST4:** the stirrer BOM's item 13 came after ME order 13518 went in. Skip this row if it has
  been ordered since.
- **Optional, for the stirrers:** the 12 × 3 mm PTFE bar
  ([Pioreactor SKU 2003](https://pioreactor.com/products/3-mm-ptfe-stir-bar), $1.68 each, four
  for $6.72). By byu-vcl#269's magnetics model it is pulled 44 % as hard as today's 15 × 6 mm bar,
  and it all but removes the Hall misreads. Try it if a stirrer stalls with the spacer in.
- **Aluminium:** add sodium chloride, ACS, 500 g ([Fisher S271-500](https://www.fishersci.com/shop/products/sodium-chloride-crystalline-certified-acs-fisher-chemical-6/S271500),
  B37, $83.65) when the aluminium shakedown runs.

## 2. Already on hand: count before ordering

**From ME order 13518 (the stirrer order)**, for four stirrers. One stirrer (A) is built, and a
second set of compact prints (from 2026-10-30) is unassembled.

| Stirrer BOM item | Four stirrers take | 13518 brought | Also covers |
| --- | --- | --- | --- |
| 2 Magnets, N52 1/4 × 1/16 in | 8, plus a spare for checking poles | 200 | |
| 3 PTFE stir bars, 15 × 6 mm | 4 | 10 | |
| 4 US1881 Hall latch | 4 | 20 | |
| 5 IRLZ44N MOSFET | 4 | 12 | |
| 6 1N5819 diode | 4 | 100 | |
| 7 Resistors: 100 Ω, 10 kΩ × 2 per stirrer | 12 | a 25-value kit | |
| 9 JST-XH 4-pin pairs with leads | 4 | 10 | **B18**: the tray's disconnect takes 2 more, so 6 of 10 |
| 10 Perfboard strips, 6 × 28 holes | 4 pieces (3 to a strip), plus one strip for the hub at the Uno | 20 | |
| 11 Heat-set inserts, M3 × 5.7 (ruthex) | 16 | 100 | **B13**: the same insert. The tray and bench cell take 12, so 28 of 100 |
| 12 M3 stainless kit | 16 × M3 × 20, 16 washers | 1 kit (15 × M3 × 20) | ST3 is the second kit |
| 1 Fan | 4 | 2 | A has one. The other goes in B; ST1 brings C and D's |
| 8 Cable, 10 ft | about 6 m | 1 pack | ST2 is the second |

**Other things the lab has** ([`../bom/README.md` §3](../bom/README.md#3-already-on-hand-borrowed-or-shared)):
- the EZstat-Pro and its Windows PC;
- 20 µL tips, for a few tests;
- the capper, the P20, the head camera and the Uno on the head;
- 20 mL VOA vials (six on the deck now: four stirred stocks, DI water and acid);
- Sylgard 184 and steel discs for the magnetic vial caps;
- cyanoacrylate, neutral-cure RTV, hot glue, heat shrink, solder;
- male–male jumper wires (capper BOM item 10) for the hub's leads into the Uno headers;
- DI water and a desiccator.

**Check the filament (B34).** The corrosion parts on A1 mini plates 1–4 come to 417 g of PLA
([`../bom/a1-mini/`](../bom/a1-mini/README.md)). The stir module's parts must be PETG, about 70 g
for the set below. Order a spool of either if less is left
([Bambu PETG HF](https://us.store.bambulab.com/products/petg-hf), $18.99).

## 3. Print

| What | Qty | File | Material |
| --- | --- | --- | --- |
| Corrosion parts: well lids, electrode caps and carriers, tray, shims, cup block, tube rack, tip rack 2, tip waste, vial caps, bench cell | plates 1–4 | [`../bom/a1-mini/`](../bom/a1-mini/README.md) (sliced, magnet pauses set) | PLA, as Ben asked on 2026-11-06 |
| Or, on the H2D: the same less the tip rack and vial caps, which the lab has | one plate | [`../bom/h2d/`](../bom/h2d/README.md) (sliced, magnet pauses set; 326 g) | PLA |
| Compact stirrer base (the 2026-11-04 one: cable notch in −X, no board stop) | **3**: B, C, D | byu-vcl [`stl/compact/base_compact.stl`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/stl/compact/base_compact.stl) | PETG |
| Compact vial holder | **2**: B, C. D reuses the 2026-10-30 holder | [`stl/compact/vial_holder_compact.stl`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/stl/compact/vial_holder_compact.stl) | PETG |
| Magnet carrier | **2**: B, C | [`stl/magnet_carrier.stl`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/stl/magnet_carrier.stl) | PETG, 100 % infill |
| Deck key, 0.05 mm press fit | **4**: B, C | [`stl/deck_key.stl`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/stl/deck_key.stl) | PETG |
| Spacer, Ø15 × 4.6 mm, under each vial | **4**, less any from byu-vcl#269's spacer print | [`stl/spacer/spacer_d15_h4.6_onshape.stl`](https://github.com/vertical-cloud-lab/byu-vcl/blob/bd46207/hardware/vial-stirrer-cubxl/stl/spacer/spacer_d15_h4.6_onshape.stl) | PETG |

Print the stirrer parts with byu-vcl `BUILD.md`'s settings: at least 4 walls, 30 % infill, the
carrier at 100 %, and 0.15 mm elephant-foot compensation. **Not PLA:** the Pioreactor's users report
PLA warping when the stirrer runs warm. The parts come to about 70 cm³. For scale, the 10-28
compact set (five parts, 28 cm³) took 27 g and 72 min on the A1 mini.

## 4. Left out on purpose

| Row | Why |
| --- | --- |
| B23–B25, B27, B28: potentiostat options | The EZstat-Pro is set up. **It has no EIS,** so step 5 of [`../copper/protocol.md` §4](../copper/protocol.md#4-sequence) is skipped and OCP runs for 30 min until a potentiostat with impedance arrives |
| B35: 20 µL tips | Enough for a few tests. A night takes at least 17 |
| B05, B18 (bought), B13 (bought) | B05 is only for the fallback O-ring cap. B13 and B18 come from ME order 13518 (section 2) |
| B30–B33 | Optional 1 µm diamond and colloidal-silica polish for copper |
| B37 | Aluminium only |
| B42 | Only if the ICP lab won't dilute into its own tubes. Ask first |
| B48 | Only if the lid's bridged counterbore ceiling comes out rough |
| An XIAO RP2040 per stirrer | Each stirrer would get its own USB, and could stir during a CubOS run. Not needed with the Uno; see the [build guide](BUILD.md#5-the-four-stirrer-firmware) |
