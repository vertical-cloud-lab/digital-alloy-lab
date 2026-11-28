<!-- Collected 2026-11-19 by a research subagent of the Claude session on PR #266 (issue #260), for hot-swap.md. Every number has its source; (SE) marks a figure seen only in a search-engine extract. -->
# Hot-swappable interfaces for the desktop LPBF: published facts (collected 2026-11-19)

Scope: facts for choosing how the build plate (Ø25/50/75 × 10 mm 6061 on a 200–225 °C block, argon, 20–63 µm Al powder, robot swap every
build), build module (2–4 kg 316L, flange ≤ 60–85 °C, swapped per campaign), reservoir, blade holder, overflow jar and cover-slide drawer are
held. No repo file was edited.

Conventions:
- Every number is the **vendor's claim** unless marked *measured* (a paper's experiment).
- **(SE)** = seen only in a search-engine extract of the cited page; I could not open that page (blocked, 403/404/410, or the text wasn't in
  the rendered page). Everything not marked (SE) was read on the rendered page or PDF text.
- "Not found" = looked, found no published number. Percentages in brackets are my arithmetic.
- Sections 4 (magnets) and 5, 7, 8 (kinematic couplings, screwdriving, standards) were collected by two parallel research passes and checked
  for sources; their own conventions ("read off chart", "snippet only" = SE) are kept.

## 1. Commercial LPBF build-plate and build-cylinder fastening

| Machine | How the plate / cylinder is held and exchanged | Exchange: manual or automated | Numbers | Source |
|---|---|---|---|---|
| Additive Industries MetalFAB (MetalFAB1, G2) | Plates move between modules (build cores, storage, heat treatment, removal). Plate clamping mechanism: **not found** | **Robotic plate exchange** ("a robotic system can move the print plates to a changeover module and add a new plate") | 8-plate storage; some users run unattended "for up to a week" | [Fabbaloo](https://www.fabbaloo.com/news/exploring-the-automation-and-modular-design-of-additive-industries-metal-3d-printer-system); [3DPrint.com](https://3dprint.com/134808/additive-industries-beta/) (SE: "automated build plate handling and storage for up to eight powder-filled printing beds") |
| EOS M 290 | Plate fixation: **not found** in public docs (EOS sells e.g. DirectBase S22, 252 × 252 × 22 mm steel platforms) | manual | build volume 250 × 250 × 325 mm incl. platform | [EOS store](https://store.eos.info/collections/all?page=2) (SE for S22 size) |
| EOS M 300-4 | "different automation options"; data sheet said to list clamping modules in three models for post-processing integration (SE; not visible on the rendered data sheet) | automation-ready | 300 × 300 × 400 mm | [EOS M 300-4 data sheet](https://www.eos.info/en-us/metal-solutions/metal-printers/data-sheets/sds-eos-m-300-4) |
| EOS M 400-4 + Grenzebach DualSetupStation EOS Edition | "Two exchangeable frames consecutively operating within a single machine" | **automated**: "Automatic job initiation 24/7", "No operator interaction needed" | laser-off to laser-on < 30 min; compressed air max 6 bar; status 07/2024 | [EOS-hosted datasheet PDF](https://eos.info/03_system-related-assets/periphery-products/peripherie_m/Grenzebach_DualSetupStation_EOS_Edition_Datasheet.pdf) |
| EOS "digital factory" (concept line) | "a robot removes the build plate with the parts on it from the set-up station and transports it, under protective gas, to a furnace", then to optical measurement and a saw | **robotic** downstream | – | [Metal AM article](https://www.metal-am.com/articles/eos-developing-metal-3d-printing-for-a-truly-digital-factory/) |
| TRUMPF TruPrint 3000 | "quickly interchangeable build and powder supply cylinder"; brochure: "Zero-point clamping system for fast set up. The ideal basis for downstream processes such as sawing, milling or grinding" (SE) | cylinder exchange "parallel to production" (SE) | Ø300 × 400 mm; standard preheat 200 °C (500 °C option per one brochure, SE) | [TRUMPF product page](https://trumpf.com/en_US/products/machines-systems/additive-production-systems/truprint-3000) (SE); [tech data sheet](https://pdf.directindustry.com/pdf/trumpf-maquinaria-sa/technical-data-sheet-truprint-3000/216245-965774.html) (200 °C read) |
| Nikon SLM 500 | exchangeable build cylinder; cylinder goes to the Part Removal Station (PRS) to cool and depowder (SE). Plate fastening: **not found** | cylinder exchange | "less than an hour turn-around" | [Nikon SLM 500](https://nikon-slm-solutions.com/slm-systems/slm500/) |
| Nikon SLM MACHX (2025–26) | optional cylinder exchange; next cylinder preheated outside the chamber; layer monitoring "automatically levels the build platform"; interchangeable build-plate packages | semi-automated; "interfaces for automated material handling" | 25-min changeover; plate packages 80–200 °C and 200–450 °C | [Metal AM](https://www.metal-am.com/nikon-slm-solutions-introduces-new-machx-range-at-formnext/) |
| 3D Systems DMP Flex 350 | **System 3R Delphin TableTop Chuck** in the build chamber; drawbars give zero-point clamping; "A protective cover keeps screws clean"; AMCarrier (273 × 273 mm, 16 pin-and-groove positions) carries BuildPal plates 63 mm square to 273 mm; "patented elastic solution" lets the plate deform during the build | manual set-up "within one minute"; pallet handling downstream | – | [Metal AM / System 3R](https://www.metal-am.com/articles/system-3r-bridging-critical-gaps-in-the-additive-manufacturing-workflow-to-enable-serial-production/) |
| 3D Systems / GF DMP Factory 500 | Removable Print Module (RPM) with System 3R referencing and clamping integrated; Parking Module stores RPMs inert | module transport between stations | 500 × 500 × 500 mm | [Metal AM](https://www.metal-am.com/3d-systems-and-gf-machining-solutions-launch-dmp-factory-500/) (SE); System 3R article above (read) |
| System 3R's statement of the problem | "the absence of tooling necessitates manual build plate attachment and levelling. Dismantling the build plate can also be tricky because of the unscrewing operation inside a powder environment" | – | – | System 3R article above |
| DMG MORI LASERTEC SLM ("pucks") | parts printed on round pucks resting in the build plate; the puck is then the chuck feature on a lathe | **robot** loads pucks into the CNC lathe | 16 spine implants: post-processing > 6 h → 1 h 20 min (80 %) | [AM Media](https://www.additivemanufacturing.media/articles/dmg-mori-build-plate-pucks-cut-postprocessing-time-by-80) |
| DMG MORI LASERTEC 30 Dual SLM (user: tool maker Neher) | **4 × SCHUNK VERO-S NSE-HT mini 88-20** + one NE-HT mini 36 centring unit as "thermal zero point" via a central pin; spring-locked, air only to open | manual loading; same interface on the mill and CMM | powder bed heated to 200 °C; one module 3 years in service; SCHUNK: ~10-year life | [SCHUNK blue journal](https://bluejournal.schunk.com/en/01-23/reliable-clamping-in-heat-and-dust/) |
| Matsuura Lumex (hybrid LPBF + milling) | **AMF K5.3** zero-point modules: five under the base plate, clamping pins screwed to the plate | – | modules see "up to 150 °C and more" under a 30 mm plate | [Industrial Production](https://www.industrial-production.de/handling-technology/voltage-for-hybrid-production.htm) |
| KASTOwin amc (plate band saw) | AMF zero-point modules hold the base plate; the saw swivels it head-down to cut parts off | automated saw | – | [AMF blog](https://en.industryarena.com/amf-andreas-maier/blog/zero-point-clamping-technology-is-unavoidable-in-additive-manufacturing--11319.html) |
| Velo3D Sapphire / XC | build module swapped; plate fixation **not found** | "changeovers between build are done autonomously within 15 minutes" | two-piece plates 25 + 50 mm on XC (SE) | [TCT](https://www.tctmagazine.com/velo3d-high-volume-metal-3d-printing-system/) |
| One Click Metal MPRINT (BOLDseries) | interchangeable build modules (Standard, Lab, Heating) with "identical mechanical and electrical interfaces"; machine identifies the module automatically. Starter package lists "substrate plates … bayonet lock" (SE) | manual module swap | 150 × 150 × 150 mm (Lab 78 × 53 × 90); plate preheat ≤ 200 °C | [Metal AM](https://www.metal-am.com/one-click-metal-introduces-interchangeable-build-modules-for-its-boldseries-metal-additive-manufacturing/); [filament2print](https://filament2print.com/en/metal-dmls/2684-mprint-one-click-metal-lpbf-metal-3d-printer.html); [Javelin](https://www.javelin-tech.com/3d/?p=72207) (SE, bayonet) |
| Renishaw RenAM 500 | **not found** (user guide H-5800-3693 not opened) | – | 250 × 250 × 350 mm | [Renishaw resource centre](https://renishaw.com/resourcecentre/en/details/RenAM-500-series-additive-manufacturing-system--140422?lang=en) |
| Farsoon, Xact Metal XM200G | **not found** (XM300G said to have an "interchangeable build platform", SE) | – | – | [Metal AM on XM300G](https://www.metal-am.com/?p=88468) (SE) |
| Aconity MIDI / MIDI+ | interchangeable process chamber (SE); plate fixation **not found** | – | preheat to 800 °C, 1200 °C (induction) on MIDI; 1000 °C on MIDI+ (SE) | [3Dnatives](https://www.3dnatives.com/en/aconity3d-metal-modular-3d-printers-191220194/) (SE) |
| Patents: magnets for LPBF plates | Blue Origin US 12365133 B2: electro-permanent chuck for build plates ("significantly easier … than with fasteners"; corner fasteners make "no go" zones). GE US 11465245 B2: magnets plus recesses against rotation | – | no commercial machine found | [US12365133B2](https://patents.google.com/patent/US12365133B2/en); [US11465245B2](https://patents.google.com/patent/US11465245B2/en) |

Pattern: where a vendor documents a quick plate interface, it is a **zero-point system** (System 3R on 3D Systems, SCHUNK on DMG MORI, AMF on
Matsuura and KASTO, TRUMPF), sometimes **pucks or pallets** carried through post-processing. High-throughput machines automate at the level of
the **whole cylinder or frame** (Nikon SLM, TRUMPF, EOS + Grenzebach, Velo3D), and Additive Industries moves plates with a robot. Plain
screwed plates are the default otherwise, and System 3R names unscrewing in powder as the problem.

## 2. Zero-point clamping systems (smallest modules)

| Product | Size | Locking / fail-safe | Release | Pull-in (clamping) force | Holding / retention | Repeatability | Temperature limit | Cleaning, seat check | Mass | Price | Robot loading | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SCHUNK VERO-S NSE mini 90 (ID 435100) | Ø90 × 20 mm | spring-loaded, form-fit, self-locking; "full pull-down force is maintained even in the event of a pressure drop" | pneumatic 6 bar | 0.5 kN; 1.5 kN with turbo | not stated | < 0.005 mm | not stated | "dynamic pressure monitoring of the clamping slide position 'opened'" | 1.0 kg | not listed | "Can be used in automated applications" | [schunk.com p/435100](https://schunk.com/us/en/p/000000000000435100); [NSE mini page](https://schunk.com/se/en/workpiece-clamping-technology/quick-change-pallet-systems/quick-change-pallet-system-for-easy-milling-applications/single-modules-nse-mini-90/c/PGR_4059) |
| SCHUNK NSE-M mini 90 (ID 435140), manual | Ø90 × 20 | mechanical | key, 10 N·m | 1000 N | – | < 0.005 mm | – | – | 1 kg | **$1,430** (MRO Supply) | – | [MRO Supply](https://www.mrosupply.com/machining/6171221_435140_schunk/) |
| SCHUNK NSE mini 90-25 (ID 1319696, discontinued; NSE3 mini 90-25 replaces it) | Ø90 | spring-loaded, sealed | 6 bar | 1.5 kN; 6 kN turbo | – | < 0.005 mm | – | slide monitoring | 1.3 kg | – | "also used for automated loading of machines" | [schunk.com p/1319696](https://schunk.com/de/en/workpiece-clamping-technology/quick-change-pallet-systems/quick-change-pallet-system-for-easy-milling-applications/single-modules-nse-mini-90/nse-mini-90-25/p/000000000001319696) |
| SCHUNK NSE-E mini 90 (electromechanical) | Ø90, pin Ø20 | form-fit, self-retaining; full force kept on power failure | 24 V BLDC, ~30 W while locking/unlocking | 1.5 kN (SE) | – | < 0.005 mm | – | inductive slide monitoring | 1.7 kg (SE) | – | yes | [schunk.com NSE-E mini 90](https://schunk.com/sg/en/werkstueckspanntechnik/intelligente-spannsysteme/elektromechanische-nullpunktspannsysteme/nse-e-mini-90/c/PGR_3990) |
| **SCHUNK NSE-AM mini 78-20** (AM, 2019) | Ø78, 20 mm above table | spring force, form-fit, self-locking; substrate stays clamped on pressure drop | 6 bar | 1.5 kN (turbo, standard) | – | < 0.005 mm | **max operating 200 °C**; "suitable for … inert gas atmosphere" | fully sealed; insertion radii | – | – | for SLS/SLM set-up; same interface as NSE mini 90-25 on machine tools | [Industry USA](https://www.magazine-industry-usa.com/news/21351-clamping-module-minimizes-set-up-times-in-3d-printing) |
| **SCHUNK NSE-HT mini 88-20** (ID 1419192; V1 1460874) | Ø88 (× Ø73 × 20, SE) | spring assembly, self-locking; air only to open | 6 bar | 0.5 kN; 2.5 kN turbo | – | < 0.005 mm | **max actuation temperature 200 °C**. Manual (SE, PDF 403): above 200 °C (to 520 °C) the clamping-pin screw's holding force drops; replace pin screws after a cycle > 200 °C; 12.9 screws only. NE-HT centring unit (no pull-down) to 500 °C (SE) | "completely sealed"; "remains unaffected by the finest dusts … and even continuous immersion baths"; "suitable for operation with inert gas" | 1.0 kg | – | – | [p/1460874](https://schunk.com/us/en/p/000000000001460874); [NSE-HT mini page](https://schunk.com/at/en/workpiece-clamping-technology/quick-change-pallet-systems/quick-change-pallet-system-for-easy-milling-applications/individual-modules-nse-ht-mini/c/PGR_4819); [blue journal](https://bluejournal.schunk.com/en/01-23/reliable-clamping-in-heat-and-dust/) |
| SCHUNK statement | "While conventional quick-change pallet systems can be used up to 60 degrees Celsius, this clamping system withstands the high temperatures of the steel powder melting process" | | | | | | | | | | | [blue journal](https://bluejournal.schunk.com/en/01-23/reliable-clamping-in-heat-and-dust/) |
| **AMF K5.3** (AM built-in) | – | spring force; lines can be disconnected | pneumatic ≥ 5 bar | 1.5 kN | 13 kN | – | "seals and media" for ≥ 150 °C at the module | – | – | – | – | [Industrial Production](https://www.industrial-production.de/handling-technology/voltage-for-hybrid-production.htm) |
| **AMF K10.3 / K20.3** (AM built-in) | – | spring force | pneumatic from 4.5 bar | 10 / 17 kN | 25 / 55 kN | – | "temperature-resistant" (hardened surfaces, special seals; 150 °C+ in the clamp) | optional blow-out for chips; "support control" (seat check) for automated processes | – | – | "basis for placement by robots" | [AMF blog](https://en.industryarena.com/amf-andreas-maier/blog/zero-point-clamping-technology-is-unavoidable-in-additive-manufacturing--11319.html) |
| AMF substrate-plate clamping system | segmented substrate plate on zero-point pull studs, "without screws" | – | – | – | – | < 5 µm | – | – | – | – | "Can be automated through standardized interface" | [amf.de](https://www.amf.de/en_us/clamping-systems/additive-manufacturing) |
| **STARK.easyclick D085** (Roemheld group) | Ø85 × 19 mm | "click & hold": pallet clicks in, held by spring "without energy input" | 4 bar (Tornado 5.5–6), max 8; 8 cm³ air, hand pump suffices; 0.1 s | 5,000 N ("load up to which the zero point … is guaranteed") | 10,000 N (zero point lost but still held); lateral 2,500 N | < 0.01 mm | **+10 to +80 °C (NBR); +10 to +150 °C (FKM, "ET")** | seat check and blow-out optional | 0.62 kg | – | "particularly suitable for use as a robot gripper"; radial pre-positioning ±0.4 mm, "loading device must be compliant"; maintenance every 250,000 cycles | [STARK catalogue WM-020-338-03-en (Carr Lane-hosted)](https://www.carrlane.com/Portals/0/Media/e89c4c29-6e4d-4f1d-929f-f1624b55509c.pdf) |
| Zimmer SPN062 (standard) | small (062) | spring assembly | 6–7 bar (E6) / 4–7 bar (E4) | 2.0 / 1.0 kN; PLUS connection 5.0 / 2.5 kN | "holding force max. M8" | 0.005 mm | **−10 to +70 °C** | air cleaning: no; venting filter, sealing | 0.39 kg | – | – | [Zimmer SPN062 datasheet](https://www.zimmer-group.com/fileadmin/pim/MER/GD/PG/MER_GD_PG_SPN062E6SD-B__SEN__APD__V1.pdf) |
| LANG Quick-Point 52 / 96 | grids 52 / 96 mm, stud Ø16 (52) | mechanical, tightening screw (pneumatic for LANG automation on request) | manual | up to 14 kN (depends on plate) | – | 0.005 mm | – | plates not stainless | – | – | pneumatic versions for LANG's automation | [LANG FAQ](https://lang-technik.de/en/service/faq/zero-point-clamping-system) |
| EROWA ITS Chuck 50 RSA (ER-008186) | base plate 10 × 55.5 × 85 | spring clamping, pneumatic opening | 6 bar | 2,800 N | – | < 0.002 mm | not stated | optional cleaning-air line; "suited for submerged operation", corrosion-resistant | – | – | "Suitable for automated use" | [EROWA](https://www.erowa.com/en/products/chuck-50-rsa/pd/008186) |
| EROWA ITS 50 Compact CombiChuck | – | – | 6 bar | 3,000 N; 5,000 N reclamped (SE) | – | < 0.002 mm (SE) | – | – | – | – | – | [EROWA](https://www.erowa.com/en/products/clamping-systems/edm-its/its-50-compact-combichuck-p1424) (SE) |
| System 3R Macro / MacroNano / MacroMagnum | – | – | pneumatic or manual (5 N·m Macro, 12 N·m MacroMagnum) | Macro 6,000 N (SE); MacroMagnum 16,000 N | – | Macro 0.002 mm; MacroNano 0.001 mm (SE) | – | "Automatic air-blast cleaning" (MacroMagnum) | – | – | for automatic changing (SE) | [DirectIndustry / System 3R](https://directindustry.com/prod/system-3r/product-6177-239952.html) |
| Jergens Ball Lock | shank + receiver bushing | 3 balls driven into a tapered groove (screw-actuated, manual) | – | – | up to 20,000 lb (9,000 kg) per shank (SE) | ±0.0005 in (±0.013 mm) with two liner bushings and holes at ±0.0002 in (SE) | – | – | – | – | – | [Jergens FAQ](https://www.jergensinc.com/en/knowledge-center/ball-lock-knowledge-center/faq) (SE) |
| Vektek KP10 / KP20 | – | – | pneumatic 8–12 bar (SE) | 8 / 17 kN (SE) | – | < 0.005 mm (SE) | – | – | – | – | – | [Vektek](https://vektek.com/zero-point-systems/zp-pm/) (SE) |
| Röhm | **not found** | | | | | | | | | | | |

Definitions (STARK): clamping force = load up to which the zero point is guaranteed; retention force = maximum overload at which the nipple is
still held though the zero point has been lost. Zero-point systems are vendor-specific: no ISO/DIN/VDI interface standard was found (see §8).

## 3. Robotic tool changers

| Product | Locking mechanism | Behaviour on air loss | Locking force | Payload | Static moment | Repeatability | Temperature | Mass | Source |
|---|---|---|---|---|---|---|---|---|---|
| ATI QC-11 | piston drives hardened balls along a multi-tapered cam: 1st taper pick-up ("No-Touch Locking"), 2nd locked, 3rd reverse taper = fail-safe | "In the event lock air pressure is removed, the balls are trapped by the cam"; "eliminates the need for a spring" | 240 lbf (1,100 N) at 80 psi (5.5 bar) | 35 lb (16 kg) suggested | X/Y 180 lbf-in (20.3 N·m), Z 110 lbf-in (12.4 N·m) on the web page; catalogue gives 220 / 300 lbf-in. Dynamic = 3 × static; test failure at 10–12 × X/Y static | 0.0004 in (0.010 mm), "based on million-cycle testing" | Buna-N seals, −20 to 150 °F (−29 to 66 °C) | 0.54 lb coupled (0.24 kg) | [ATI QC-11](https://www.ati-ia.com/Products/toolchanger/QC.aspx?ID=QC-11); [QC catalogue PDF](https://www.ati-ia.com/Library/documents/ati_qc_cat.pdf) |
| ATI QC-5 | same | same | 160 lbf (690 N) | 18 lb (8.2 kg) | 110 lbf-in (12 N·m) X/Y | – | same | – | catalogue above |
| SCHUNK SWS-011 | piston and balls; "fail-safe reverse taper" | "can only be separated from one another in the self-locking status if" the piston gets unlock air pressure (catalogue) | 1,100 N | 16 kg (recommended handling weight) | – | 0.015 mm | **5–60 °C** ambient | master 0.13 kg, adapter 0.09 kg; Ø50 | [SCHUNK SWS catalogue section PDF](https://d16vz4puxlsxm1.cloudfront.net/asset/076200133045-Prod/document_6vmj4tqbah0tp7o3edf4ggma69/SWS%20Catalog%20section.pdf) |
| SCHUNK SWS-001 | same | same | 170 N | 1.4 kg | – | 0.01 mm | 5–60 °C | 0.03 + 0.02 kg | same |
| SCHUNK SWS-011 capture window | – | – | – | – | – | max XY offset ±1 mm, angle ±2°, max gap when locking 1.5 mm; 4.5–6.9 bar | – | – | same |
| Stäubli MPS 015 / MPS 025 | guiding column + cross-shaped guiding surfaces; locking balls into an internal collar | "yes, by compression spring" | connection force 4 / 6 kN; lateral 2 / 3 kN | 10 / 20 kg | 15 / 34 N·m (dynamic 52 / 119) | ±0.0015 mm | **0–50 °C** | robot side 0.26 / 0.4 kg; tool side 0.14 / 0.18 kg; ISO 9409-1-31.5-4-M5 / -40-4-M6; safety PL d, Cat. 3 | [Stäubli MPS 015–055 brochure](https://staubli.com/content/dam/fcs/brochures/products/mps/01-small-payload/tool-changer-MPS-015-025-035-055-staubli-en.pdf) |
| OnRobot Quick Changer | locking springs, "redundant locking mechanism"; **manual** release by an operator | not stated | – | 25 kg (older v1.0.2 manual: 10 kg, SE) | permissible force 400 N, torque 40 N·m (datasheet v1.7, SE) | ±0.02 mm | not stated | 200 g; IP67; ISO 9409-1-50-4-M6 (SE); **5,000 tool-change operating cycles**; change < 5 s | [OnRobot](https://onrobot.com/en/products/quick-changer) |
| Zimmer WWR (WWR40F-B, WWR100F-B, WWR160L-B) | spring accumulator + self-locking mechanical transmission | "the tool is held securely during a pressure loss" | not stated (WWR100F-B joining 120 N, release 75 N) | WWR40F-B 20 kg | – | Z 0.01, X/Y 0.02 mm | not found | B10d 5,000,000 cycles (WWR160L-B) | [Zimmer WWR100F-B](https://zimmer-group.com/en/technologies-components/components/handling-technology/tool-changer/pneumatic/series-wwr/products/wwr100f-b) (all SE) |

Pattern: every automatic changer locks with **balls on a taper or collar, driven by air, held mechanically on air loss** (reverse taper or
spring), with a capture window of about ±1 mm and ±2°. None is rated above 50–66 °C, which is set by their elastomer seals and electronics.
The OnRobot unit is a manual changer for cobots (5,000 cycles), not an automatic one.

## 4. Magnets (electro-permanent, fail-safe, plain; materials; strike plates; contamination)

All numbers are vendor claims unless marked otherwise. "Read off chart" means I read the value from a vendor graph (about ±5 % of full scale).
"Not found" means I looked and could not find a published number. Percentages in brackets are my own arithmetic on the vendor numbers.

### 4.1 Switchable permanent-magnet (electro-permanent and motor-switched) grippers / workholding

| Product | Mechanism | Force (condition) | Shear / payload | Power-loss behaviour | Temp. limit | Mass, other | Price | Source |
|---|---|---|---|---|---|---|---|---|
| Magswitch PPe30 (81401683) | Electrically actuated switchable permanent magnet. Magswitch says E-Series units "are not electromagnets nor are they electropermanent magnets (EPMs)"; off state "reducing magnetism to zero" so ferrous particles fall off | Max breakaway 536.0 N on 200 × 200 mm SAE 1018 sheet, 63 µin finish, flat pole shoes, no gap. By sheet thickness: 0.5 mm 64.4 N; 1 mm 172.3; 1.9 mm 305.1; 3 mm 466.3; 4.76 mm 525.2; 10 mm 534.3; 25 mm 536.0 N. By air gap, thick target, read off chart: 0.2 mm ≈310 N (58 %); 0.3 mm ≈285 N (53 %); 0.5 mm ≈210 N (39 %); 1.0 mm ≈133 N (25 %) | Max shear 117.6 N (22 % of breakaway). "Not safe lifting forces" | "a magnet that won't let go if power is lost" | Operating −15 to 80 °C. "Do not expose the magnet to temperatures above 80 °C … will permanently degrade the magnet" | 1.18 kg; 24 V DC, 2 A peak; actuation 350 ms on/off; warns debris and air gaps reduce force | "Request pricing" (not listed) | [spec sheet PDF](https://downloads.magswitch.com/products/81401683-PPe30-Spec-Sheet-1101911.pdf); [press article](https://www.therobotreport.com/intelligent-magnetic-gripping-revolutionizes-ferrous-automation-applications/) |
| Magswitch E50 / PPe50 | as above (E50 has variable field output 0–100 %) | Max breakaway 2066 N (210.7 kgf). E50 EU by thickness, SAE 1018: 0.5 mm 14.6 kgf; 1 mm 37.8; 2 mm 70.1; 3 mm 110.5; 4 mm 153.4; 5 mm 182.9; 6 mm 194.5; 7 mm 202.7; 12.7 mm 210.5; 50 mm 210.7 kgf (±5 %) | Max shear 716 N (35 %). Magswitch recommends safe working load = max force / 5 | holds on power loss (PPe50 page, same wording) | E50: ambient −10 to +40 °C operating | 2.95–3.4 kg; 24 V, 2–3 A peak | not listed | [PPe50 page](https://magswitch.com/products/plug-and-play-ppe-e50-81401665); [E50 EU PDF](https://downloads.magswitch.com/products/1101409.pdf); [E50 PDF](https://downloads.magswitch.com/products/1101336.pdf) |
| OnRobot MG10 | Permanent magnets switched by an integrated electric BLDC motor (datasheet: "Motor: Integrated, electric BLDC"; "gripping time (including brake activation)") | Pulling force 300 N; 10 force steps; full force needs ≥ 65.4 × 65.4 mm workpiece and all four fingers in contact. Payload (3 g) vs thickness, read off chart: 0.5 mm 3.5 kg; 1 mm 6; 1.5 mm 8; 2 mm 9.4; ≥ 2.5 mm 10 kg. Payload vs air gap: 0 → 10 kg; 0.25 mm ≈4.7 kg; 0.5 mm ≈2.6 kg (26 %); 1 mm ≈1.4 kg (14 %); 2 mm ≈0.9 kg | 10 kg parallel; 3.4 kg perpendicular to ground; "perpendicular … 28 % of the maximum" | "Hold workpiece if power is lost? Yes" | Operating 5–50 °C; storage 0–55 °C | 0.8 kg; IP67; 300 ms; 24 V; Ø71 × 80.2 mm; warranty 3 y or 3,000,000 cycles | not listed | [datasheet v1.5](https://onrobot.com/storage/datasheets/mg10/datasheet_mg10_v1.5_en.pdf); [product page](https://onrobot.com/en/products/mg10) |
| SCHUNK EMH-RP 036-B | Electro-permanent: "short current pulse" reverses the permanent magnets' polarity ("Aktivierungszeit … Umpolung der Permanentmagnete") | Holding force 530 N on 6.08 cm² magnet area (test plate not stated) | Payload 8.5 kg with the magnet face horizontal, 3.5 kg with it vertical | Remains in its selected state on power failure or E-stop | Ambient 5–50 °C; module heats +10 K at 5 activations/min, +25 K at 15/min | 1.0 kg; IP52; 300 ms; 24 V, 3.1 A; 64 × 64 × 128 mm. "Designed mainly for clean to lightly soiled environments" | login required | [product page (DE)](https://schunk.com/at/de/greiftechnik/magnetgreifer/emh/emh-rp-036-b/p/000000000001351485); [series page](https://schunk.com/dk_en/gripping-systems/series/emh/) |
| Kendrion HMG (cobot gripper) | Built on Kendrion GTN permanent electro holding magnets; "no moving parts" | "Power-free holding with up to 700 N" | not found | Fail-safe: holds on power failure | not found | ISO 9409-1-50-4-M6 flange | not listed | [Kendrion flyer](https://www.kendrion.com/fileadmin/user_upload/Downloads/Brochures_and_Flyers/Electromagnets_Actuators/Solution-examples/Magnetic-gripper-robot-tool-EN.pdf) |
| Goudsmit HGE-SQ E-Gripper | "Bi-stable electro-permanent magnetic gripper" | Forces on website, not in manual (not found). Advised loads use safety factor 3 per EN 13155 | Max acceleration 20 m/s² with friction ring | Bi-stable (holds without power) | Ambient 5–40 °C; ambient > 30 °C or part at 40–80 °C reduces force; > 4 cycles/min heats the magnet system; temperature sensors built in | Coil insulation class B; IP40; 24 V, 6 A peak for 350 ms; duty 12 on + 12 off per min | not listed | [user manual](https://www.goudsmitmagnetics.com/uploads/pdf/en_GMSD_IM_HGE_4223.pdf) |
| Zubax FluxGrip (FG40) | Solid-state EPM, zero power in either state | not found on the reference manual's landing page | not found | stays in state (EPM) | not found | not found | not found | [FluxGrip manual](https://fluxgrip.zubax.com/) |

**Material factor (force relative to low-carbon steel = 100 %).** Goudsmit HGE manual: C15/C45 80–90 %; tool steel 70–80 %; ferritic/martensitic stainless "like AISI430" 60–75 %;
cast iron 45–50 %; nickel 30–50 %; AISI 304 1–3 %; **austenitic AISI 316 0 %; brass, aluminium, copper 0 %**
([manual](https://www.goudsmitmagnetics.com/uploads/pdf/en_GMSD_IM_HGE_4223.pdf)). SCHUNK EMH: Fe 360 100 %, 10-C15 90 %, tool/case-hardening/sectional steels 70–80 %,
magnetic stainless 65 %, cast iron 50 % ([series page](https://schunk.com/dk_en/gripping-systems/series/emh/)).

### 4.2 Holding magnets: fail-safe "permanent electro" (power to release) vs plain electromagnets (power to hold)

| Product | Type | Size | Holding force (condition) | Duty cycle, power | Coil thermal class | On power loss | Source |
|---|---|---|---|---|---|---|---|
| Kendrion PEM2525A (No. 1266251) | Permanent holding magnet, coil cancels field to release | Ø25 × 25 mm, M6 | 140 N (counter-plate not stated) | 24 V DC, 15 % ED, 9.6 W | E (120 °C); IP00 | holds | [datasheet PDF](https://www.kendrion.com/fileadmin/user_upload/Product_Finder/Solenoid_Technology/Solenoids_DS_EW/Datasheets/Permanent-Haftmagnet-1266251-DB.PDF) |
| Kendrion D35 (01030004) | Permanent electro holding magnet | Ø35 | 160 N | 24 V, 25 % ED, 4.6 W | E 120; IP65 (device) | "holds loads even in the event of a power failure and only needs to be energized briefly to release" | [page](https://www.kendrion.com/en/productfinder/group/product/holding-magnets/01030004); [PDF](https://www.kendrion.com/fileadmin/user_upload/Product_Finder/Solenoid_Technology/Solenoids_DS_EW/Datasheets/Permanent-Haftmagnet-01030004-DB.PDF) |
| Kendrion D55 (01050002) | Permanent electro holding magnet | Ø55 | 420 N | 24 V, 25 % ED, 8.9 W | E 120 | holds | [page](https://www.kendrion.com/en/productfinder/group/product/holding-magnets/01050002) |
| Kendrion GTB040 | Plain DC electro holding magnet | Ø40 × 25.5 mm | 475 N | 24 V, **100 % ED**, 0.21 A, 5.1 W | B (130 °C); IP65 | "When the supply voltage is switched off, the workpiece … falls off" | [page](https://www.kendrion.com/en/productfinder/group/product/holding-magnets/gtb040100001); [PDF](https://www.kendrion.com/fileadmin/user_upload/Product_Finder/Solenoid_Technology/Solenoids_DS_EW/Datasheets/Elektro-Haftmagnet-GTB040.100001-DB.PDF) |
| Magnet-Schultz G MH X (plain, S1 100 %) | Plain DC holding magnet with armature | Ø25 / 40 / 50 (armature 3 / 5 / 6 mm thick) | **Force vs air gap (stroke), N:** Ø25: 0 mm 135; 0.1 mm 36.3 (27 %); 0.16 mm 18.2; 0.25 mm 9.8 (7 %); 0.4 mm 3.5; 1.0 mm 0.9. Ø40: 470; 275 (59 %); 157; 80 (17 %); 30; 6.2. Ø50: 720; 569 (79 %); 373; 216 (30 %); 93; 18. Measured on blank 9SMn28, plane ground, roughness ≤ 15 µm, at 90 % rated voltage, ±10 %; "if the specimen thickness is small, the magnetic force is reduced"; galvanized poles −10 % | 3.2 / 5.6 / 6.5 W; temperature rise Δυ = 60 K at reference 35 °C | F (insulation materials) | drops; "a retention force of about 5 % of the magnetic force remains" after switch-off | [catalogue (distributor-hosted)](https://astat.pl/pliki/Komponenty_automatyki_przemyslowej/Elektromagnesy_mocujace/karta-katalogowa-GMH_GZZ.pdf) |

**Air gap on a large-pole electro-permanent chuck** (Eclipse workholding brochure, read off chart, mild steel): 0 mm 1.00; 0.2 mm ≈0.88; 0.5 mm ≈0.62; 0.7 mm ≈0.50;
1.0 mm ≈0.41 of full force. Tool steel starts at 0.60, cast iron at 0.50 at zero gap ([brochure p. 8](https://www.eclipsemagnetics.com/site/assets/files/2396/magnetic_workholding_brochure.pdf)).
Pattern across sources: the smaller the pole pitch, the faster force falls with gap (Ø25 pot magnet loses 73 % at 0.1 mm; a chuck loses 12 % at 0.2 mm), but the thinner the
steel needed to saturate it.

**Counter-plate (strike plate) thickness to reach full force:** OnRobot MG10 ≈2.5 mm; Magswitch PPe30 98 % at 4.76 mm; E50 ≈96 % at 7 mm, 100 % at 12.7 mm; Goudsmit rates pot
magnets on 5 mm ground St37 ([Goudsmit flat pot page](https://www.goudsmitmagnetics.com/en-us/products/mounting-magnets/flat-pot-magnets)); Magnet-Schultz specifies 3 / 5 / 6 mm
armatures for Ø25 / 40 / 50 (sources as above).

### 4.3 Permanent-magnet materials: temperature

| Material / grade | Max operating temp. | Rev. temp. coeff. of Br | of Hci | Curie | Source |
|---|---|---|---|---|---|
| NdFeB N / M / H / SH / UH / EH / AH (≈30–38 MGOe) | 80 / 100 / 120 / 150 / 180 / 200 / 230 °C (N38AH 220 °C) | −0.12 %/°C | −0.70 %/°C | — | [Adams chart](https://www.adamsmagnetic.com/wp-content/uploads/ADAMS-Materials-Chart-of-Properties-7-25.pdf) |
| NdFeB high-energy grades | derated: N40EH 190; N42UH 170; N45SH 140; N45UH 160; N48H 110; N48SH 130; N54, N56 60 °C | " | " | — | same |
| NdFeB sintered (40 MGOe), Arnold | — | −0.11 %/°C | −0.60 (−0.45 to −0.65 by grade) | 310 °C | [Arnold TN 0303](https://www.arnoldmagnetics.com/wp-content/uploads/2017/10/TN_0303_rev_150715.pdf) |
| SmCo 1:5 | 250 °C | −0.040 to −0.045 | −0.30 (Adams); −0.40 (Arnold) | 700 °C | Adams; Arnold |
| Sm2Co17 | 300 °C (Hci ≥ 18 kOe); 350 °C (Hci ≥ 25 kOe) | −0.020 to −0.035 (Adams); −0.03 (Arnold) | −0.20 | 800 °C | Adams; Arnold; [Eclipse SmCo sheet](https://www.eclipsemagnetics.com/site/assets/files/19544/eclipsemagnetics_smco_datasheet.pdf) ("H versions … up to +350 °C") |
| AlNiCo cast / sintered | 550 / 450 °C | −0.02 | +0.01 | 860–900 °C | Adams; Arnold |
| Ferrite (ceramic 1–8) | 399 °C (Adams); 350 °C (Alliance) | −0.18 to −0.20 | +0.2 to +0.5 (Adams); +0.27 (Arnold) | 450 °C | Adams; Arnold; [Alliance table](https://www.allianceorg.com/pdfs/PhysicalPropertiesofMagnets.pdf) |

- **The rating depends on the load line.** Adams: "Maximum operating temperatures are for a magnet geometry with a corresponding Operating Slope of 1" (permeance coefficient 1).
  Arnold TN 0303: designers use Hk with the coefficient of coercivity to set the maximum temperature; the coefficients are averages over 20 to about 120 °C and are not linear;
  "above 180 °C the material of choice is SmCo. NdFeB has a superior price/performance ratio below about 120 °C"; 120–180 °C "poses a challenge".
- **Pot (cup) magnets as sold:** Goudsmit NdFeB pot magnets up to 80 °C (lose 15–20 % at 80 °C, reversible); SmCo up to 200 °C (15–20 %); ferrite up to 200 °C (30–40 %)
  ([Goudsmit](https://www.goudsmitmagnetics.com/en-us/products/mounting-magnets/flat-pot-magnets)). Eclipse SmCo bi-pole deep pot: up to 200 °C, Ø6–32 mm, 8–600 N, H6 brass
  shell for press fit ([Eclipse](https://www.eclipsemagnetics.com/en-us/products/magnetic-tools-and-standard-magnets/samarium-cobalt-deep-pot/)). AlNiCo pot magnet with a rating: not found.
- **The design's existing Z-coupling magnet, McMaster 5679K95** (NdFeB in zinc-plated steel case, Ø25 × 7 mm, 44 lbf max pull, M4): **maximum 175 °F (79 °C)**; pull rated
  "on direct contact with rust-free, unpainted iron" ([McMaster](https://www.mcmaster.com/5679K95/)).

### 4.4 Coil insulation (electromagnets)

- Thermal classes seen on holding-magnet datasheets: E = 120 °C (Kendrion PEM2525A, D35, D55), B = 130 °C (Kendrion GTB040; Goudsmit HGE), F (Magnet-Schultz G MH; sources above).
  A coil maker citing DIN VDE 0580: class F coil max 155 °C (wire 180 °C), class H coil max 180 °C (wire 200 °C)
  ([Bondioli & Pavesi, via search, PDF not opened](https://bondioli-pavesi.com//download/pdf/398SCV0063A00.pdf)). The IEC 60085 table itself was not opened; the class letters and
  limits above (E 120, B 130, F 155, H 180 °C) are as the vendors state them.
- Duty cycle matters: fail-safe types are rated 15–25 % ED (they only need current to release); plain types hold at 100 % ED and self-heat (Magnet-Schultz Δυ = 60 K above a
  35 °C reference). Switching heats EPM grippers too (SCHUNK +10 K at 5/min, +25 K at 15/min).
- Hot-rated switchable magnetic clamping does exist, but only as mould-clamping platens: Roemheld R-MAG 210 "proven performance at temperatures up to 240 °C", R-MAG-R
  "operating temperature up to 230 °C", both electro-permanent, "complete safety in the case of a power failure", with monitoring of "magnetic force, mold position, and platen
  temperature" ([Roemheld](https://roemheld-usa.com/en/products/applications/Magnetic%20Clamping%20Systems%20for%20Rubber%20Molding)); Magna IM 120 / 150 / 180 °C variants with a
  standard temperature sensor ([brochure](https://cdn.shopify.com/s/files/1/0670/2340/5359/files/09_MAGNA_INJECTION_MOLD.pdf)); EAS Pressmag SP100 100 °C, SP150 150 °C (stainless
  mesh seals, "easy-to-clean, perfectly flat all steel surface") ([brochure](https://easchangesystems.com/wp-content/uploads/EASC6031-Brochure-Pressmag_UK-LR.pdf)). These are
  large platens; no small hot-rated module was found.

### 4.5 Strike plates: which steels are magnetic

| Material | Magnetic behaviour | Source |
|---|---|---|
| Annealed austenitic stainless (304, 316) | DC permeability 1.003–1.005 at 200 Oe ("essentially nonmagnetic"); cold work can raise it via deformation martensite, less so in higher-Ni grades | [Carpenter](https://www.carpentertechnology.com/blog/magnetic-properties-of-stainless-steels) |
| 316 / 6061 as a gripper target | 0 % of low-carbon-steel force | [Goudsmit manual](https://www.goudsmitmagnetics.com/uploads/pdf/en_GMSD_IM_HGE_4223.pdf) |
| 430 (process-annealed, measured) | Bs = 1.51 T; 430FR softest of ten grades: µmax 960, Hc 265 A/m, Br 0.49 T. Bs falls about linearly with Cr content; as-received samples were magnetically harder than ASM Handbook values | Oxley et al., J. Magn. Magn. Mater. 321 (2009) 2107–2114, [doi:10.1016/j.jmmm.2009.01.002](https://doi.org/10.1016/j.jmmm.2009.01.002) ([author copy](https://www.holycross.edu/document/stainlesssteelspaper)) (independent measurement) |
| 410 / 416 (martensitic) | ferromagnetic; can become permanently magnetized when hardened; coercivity rises with hardness | [Carpenter](https://www.carpentertechnology.com/blog/magnetic-properties-of-stainless-steels) |
| 430 as a gripper target | 60–75 % (Goudsmit), 65 % (SCHUNK) of low-carbon steel | sources in 4.1 |

### 4.6 Contamination, powder and magnetic build plates

- Every gripper source names debris as an air gap: Magswitch ("Debris or contamination on the target surface", "Ensure all surfaces are clean and free of debris … Any air gaps will
  reduce the magnet's hold force"); Goudsmit ("rough surfaces, rust and dirt lead to an air gap and reduce the holding force"); SCHUNK EMH (designed for clean to lightly soiled
  environments; life may be shorter otherwise). Sources in 4.1.
- Grinding-chuck practice (distributor manuals found by search, not opened): remove burrs and chips; brush, and never use compressed air on swarf
  ([Grizzly T1227 manual](https://www.manualslib.com/manual/1477734/Grizzly-T1227.html?page=6)); resurface the chuck face to restore flatness.
- Off-state residual: a plain electromagnet keeps about 5 % of its force after switch-off (Magnet-Schultz, above), so it holds onto ferrous fines; Magswitch claims zero field in the
  off state so ferrous particles fall off (press article above).
- **Measured holding-force loss from a layer of fine powder: not found.** The 20–63 µm Al powder is non-magnetic, so it is not attracted; it only matters if it is trapped in the
  joint, where it acts as a 20–63 µm gap (compare the Ø25 data: −73 % at 0.1 mm). A ferromagnetic powder (17-4PH, maraging steel, Fe) would also be attracted to the poles. I found
  no source on magnetic workholding inside a metal-powder bed.
- **LPBF build plates held by magnets: no commercial machine found.** Patents: Blue Origin, US 12365133 B2 (priority 2017-08-31): an electro-permanent magnetic chuck
  "releasably supports the build platform"; "the magnet used to attach the build plates is electro-permanent"; current "is only needed to switch the magnet between off and on";
  adding and removing plates "is significantly easier with a magnetic chuck than with fasteners", and corner fasteners create "no go" zones
  ([Google Patents](https://patents.google.com/patent/US12365133B2/en)). GE, US 11465245 B2 (priority 2019-01-30): permanent or electro-magnets pull fixtures onto a mounting plate in
  a powder-bed machine; an electromagnet alone "may not provide proper alignment", so recesses prevent rotation ([Google Patents](https://patents.google.com/patent/US11465245B2/en)).
- FDM (polymer) printers use magnetic beds holding spring-steel sheets; Prusa describes "high Curie temperature magnets" in the MK52 bed, according to search results
  ([Prusa help](https://help.prusa3d.com/article/flexible-steel-sheets_2195), not opened); a numeric temperature rating was not found.

### Key facts (magnets)

1. **No switchable magnetic gripper or clamp module of robot size is rated anywhere near a 200–225 °C plate.** Published ambient limits: SCHUNK EMH 50 °C, OnRobot MG10 50 °C,
   Goudsmit HGE 40 °C, Magswitch E50 40 °C, PPe30 80 °C (permanent damage above 80 °C). Only large mould-clamping platens are rated hot (Roemheld 230–240 °C, Magna IM 180 °C).
2. **Magnet material at 200–225 °C:** NdFeB only in EH/AH grades (200–230 °C at permeance coefficient 1, less in a low-permeance circuit, and Br drops about 0.12 %/°C, i.e. roughly
   21–24 % at 200–225 °C from 23 °C; Arnold notes the coefficient is an average over 20–120 °C, so this is an extrapolation). Sm2Co17 (300–350 °C) or AlNiCo (450–550 °C) give margin. Off-the-shelf SmCo pot magnets are rated only to 200 °C (Eclipse, Goudsmit).
3. **The magnet already in the design (5679K95) is rated 79 °C.** Check what temperature the Z-arm coupling reaches under a 200–225 °C module.
4. **Coils:** holding-magnet coils are class E/B/F (120/130/155 °C); class H is 180 °C. A coil near a 225 °C block would need a 200/220 °C insulation system or must be kept away
   from the heat.
5. **Air gap kills small magnets.** A Ø25 holding magnet keeps 27 % of its force at 0.1 mm and 7 % at 0.25 mm (Magnet-Schultz). The larger-pole PPe30 keeps 58 % at 0.2 mm and 39 % at
   0.5 mm, and an EPM chuck keeps 88 % at 0.2 mm. Powder grains of 20–63 µm sit in the range that costs tens of percent for a small magnet, so a magnet joint in the powder zone
   needs a wipe/blow-off and a seat check.
6. **Aluminium 6061 and 316L give zero magnetic force.** They need a ferritic strike plate (430 or 416 gives 60–75 % of mild-steel force; Bs of 430 is 1.51 T, measured) thick
   enough to saturate: about 2.5 mm (MG10) to 5 mm (PPe30) to 7–13 mm (E50), scaling with pole pitch.
7. **Magnets are weak in shear.** PPe30 shear is 22 % of breakaway, E50 35 %, SCHUNK EMH 3.5 kg vertical vs 8.5 kg horizontal. A magnet should only pull the part down; dowels, a
   spigot or a kinematic seat must take lateral load and torque (GE's patent adds recesses for the same reason).
8. **Fail-safe behaviour:** electro-permanent and switchable-PM devices (SCHUNK EMH, OnRobot MG10, Magswitch, Kendrion PEM/HMG, Goudsmit HGE, Roemheld) keep holding on power loss.
   Plain electromagnets drop the part (Kendrion GTB040) and keep about 5 % residual. Fail-safe holding magnets need current only to release (15–25 % ED).
9. **Vendor safety factors on magnetic holding:** Magswitch 5:1; Goudsmit 3 (EN 13155); OnRobot payloads quoted at 3 g.
10. **Precedent:** an electro-permanent chuck for LPBF build plates appears in patents (Blue Origin, GE), not in any commercial LPBF machine found.

(Sections 5, 7, 8: "snippet only" = seen only in a search-engine extract, same as (SE).)

## 5. Kinematic couplings

### 5a. Papers (measured unless noted)

| Source | Mechanism | Preload | Repeatability | Conditions / temperature | Cost | URL |
|---|---|---|---|---|---|---|
| Slocum 2010, review, Int J Mach Tools Manuf 50(4):310–327, DOI 10.1016/j.ijmachtools.2009.10.006 | 3-2-1 fixturing (point contacts against 3+2+1 points) | not stated | "on the order of 3–5 microns" in practice | general statement | – | [MIT open copy](https://web.mit.edu/course/2/2.70/Reading%20Materials/Kinematic%20coupling%20review%20article.pdf), [DSpace](https://dspace.mit.edu/handle/1721.1/69013) |
| same | steel ball / steel groove, 3-groove | 80 % of allowable Hertz stress | sub-µm at first, then worse each cycle, to about 10 µm after several hundred cycles; fret marks at the contacts | room-temperature lab test. Review: plain (non-stainless) steel "should only be used for low-cycle applications" because of fretting | – | same |
| same | Si₃N₄ ball / steel groove | 80 % of allowable | 50 nm over a few dozen cycles; after wear-in it approaches the groove surface finish (burnishing seen) | polished, corrosion-resistant (ideally ceramic) surfaces give sub-µm "with little or no wear-in" | – | same |
| same | canoe balls (large-radius contact), 300 mm coupling, grinding fixture | not stated | 50 nm; axial stiffness > 200 N/µm | – | – | same |
| same, Hertz examples at 1.3 GPa peak contact pressure, E = 193 GPa (stainless) | 25 mm half-sphere on 25 mm cylinders / in a vee / 25 mm × R125 crowned cone in vee / 250 mm half-sphere in vee | Fmax per contact 111 N / 229 N / 1106 N / 16 160 N | vertical deflection 3.2 / 4.7 / 11 / 47 µm; contact ellipse 0.425×0.269 / 0.488×0.488 / 2.695×0.603 / 4.878×4.878 mm | design guidance (calculated, not measured) | – | same |
| same | how to preload | heavy duty: bolts through the centre of each ball compressing springs; light instruments: magnets; vertical couplings: a clamp or gravity on a mass | Hertz deflection ∝ F^(2/3), so preload sets stiffness; preload "must be high, repeatable, and must NOT deform the rest of the structure" | – | – | same |
| same | sheet-metal / spring-steel vees, flat faces then seat | vertical preload | "tens of microns", "very good for a low cost coupling" | – | low | same |
| same | quasi-kinematic coupling replacing dowels in engine blocks (bearing caps) | bolts | 5 µm (dowels) → 1.5 µm (QKC) | production | several $ → < $1 per block | same |
| same | K-Dock (servo kinematic coupling with central ball-lock preload post) on semiconductor test heads | ball-lock pull-in, separate actuator | figure only (vs. J-ring) | dock/undock/align time from tens of minutes to a few minutes; done several times per shift | – | same |
| same, thermal note | any kinematic coupling | – | with uniform expansion the coupling's instant centre is also its thermal centre; with non-uniform expansion the seated position shows hysteresis, depending on whether the contacts micro-slip | relevant to a heated plate on a cold base | – | same |
| Hart, Slocum, Willoughby 2004, "Kinematic coupling interchangeability", Precision Eng 28:1–15, DOI 10.1016/S0141-6359(03)00071-0 | canoe-ball and 3-pin couplings on an ABB IRB6400R base and wrist | bolts up to 300 N·m | about 0.06–0.07 mm average at the tool point (laser tracker); estimated total accuracy 0.07–0.18 mm | shop floor. A "refined" mount (bolts torqued in steps of 10/50/100 %, contacts cleaned, bolts greased between trials) gave at least 2:1 better repeatability on the base. Seat gently, with as little sliding as possible; "dithering" (low-frequency vibration) before tightening; horizontal coupling plane best | canoe balls US$1000–3000 per set of three | [PDF](https://wp.optics.arizona.edu/optomech/wp-content/uploads/sites/53/2016/10/Hart-2004.pdf) |
| same, conclusion | – | – | when bolt preload, contact cleanliness and mating procedure vary, a quasi-kinematic 3-pin interface "may offer equal performance to a ball–groove coupling, at much lower cost" | – | – | same |
| Willoughby, Hart, Slocum 2005, J Manuf Syst 24(2):108–121, DOI 10.1016/S0278-6125(05)80011-1 | 3-pin vs. canoe-ball, robot base and wrist | bolted | industrial: canoe 0.05 mm (wrist), 0.10 mm (base); 3-pin 0.11 mm (base), ~0.08 mm (wrist, limited data). Lab best case for 3-pin: about 1 µm. Proper mounting improved repeatability by up to 90 % | "installation procedure is almost as important as the form of coupling itself" (abstract) | – | [abstract](https://mechanosynthesis.mit.edu/experimental-determination-of-kinematic-coupling-repeatability-in-industrial-and-laboratory-conditions) |
| Culpepper 2004, "Design of quasi-kinematic couplings", Precision Eng 28:338–357, DOI 10.1016/j.precisioneng.2002.12.001 | QKC (balls in conical/arc grooves, then faces touch) | 25 N preload, lubricated | 1/4 µm in plane after an initial wear-in. A preload that plastically deforms the contacts removes the wear-in. Compare 0.10 µm for well-designed, lubricated kinematic couplings (Slocum & Donmez 1988). Automotive QKC: 2/3 µm | most low-cost alignment methods manage about 5 µm | ≈ $1 per ball-groove set in volume | [PDF](https://wp.optics.arizona.edu/optomech/wp-content/uploads/sites/53/2016/10/culpepper-2004.pdf) |
| Hale & Slocum 2001, "Optimal design techniques for kinematic couplings", Precision Eng 25(2):114–127, DOI 10.1016/S0141-6359(00)00066-0 | optimisation of 3-groove couplings, friction, stiffness matrix | – | numbers not extracted (full text not reached) | – | – | [record](https://data.zhenzhi.com/details/1/884733289) |
| Slocum 1992, "Design of three-groove kinematic couplings", Precision Eng 14(2):67–76, DOI 10.1016/0141-6359(92)90051-W | 3-groove design method, contact stress and error-motion theory, spreadsheet | – | numbers not extracted | – | – | [record](https://data.zhenzhi.com/details/1/992720612) |
| Slocum & Donmez 1988, "Kinematic couplings for precision fixturing, Part 2: experimental determination of repeatability and stiffness", Precision Eng 10(3):115–122 | heavily loaded ball/groove | – | cited by Culpepper 2004 for 0.10 µm (lubricated); DOI not found | – | – | cited in the Culpepper and Slocum PDFs above |
| Vallance, Morgan, Slocum 2004, "Precisely positioning pallets in multi-station assembly systems", Precision Eng 28:218–231 | pins-in-holes vs. exact constraint for assembly pallets | – | abstract: exact constraint is "much better" than pins-in-holes; numbers not found | pallet error is "one of the largest" error-budget items in precision assembly | – | [typeset.io record](https://www.typeset.io/pdf/precisely-positioning-pallets-in-multi-station-assembly-eaijv2mzrl.pdf) |

Dirt and particles: no paper found that measures repeatability against particle size or powder on the contacts. The
only quantified evidence is Hart 2004 (cleaning contacts, part of a refined procedure that gave ≥ 2:1) and Slocum 2010
(fretting debris on plain steel: sub-µm → ~10 µm after several hundred cycles). Not found: data for Al powder or 200 °C.

### 5b. Commercial kinematic bases (vendor claims)

| Product | Mechanism | Preload / force | Repeatability | Temperature | Price | URL |
|---|---|---|---|---|---|---|
| Thorlabs KB50/M (50 × 50 mm, M6) | 3-point kinematic base, magnetic | not found (page loaded, no spec text) | not found | not found | $103.91 | [Thorlabs](https://www.thorlabs.com/thorproduct.cfm?partnumber=KB50/M) |
| Thorlabs KB1X1 / KB25/M | magnetic kinematic base | not found | 30 µrad angular, 30 µm lateral (snippet only, obsolete 2015 catalogue page) | – | – | [catalogue PDF](https://www.thorlabs.us/catalogpages/Obsolete/2015/NX1F.pdf) |
| Eksma 850-0030, 75 × 75 × 25 mm, anodised Al | two magnets | not stated | 50 µm | – | $105 | [Eksma](https://www.eksmaoptics.com/v/850-0030/75) |
| Newport/MKS BK-1A | magnetic kinematic base | not found | < 100 µrad (snippet only; page blocked) | – | – | [MKS](https://np.d1.mks.com/p/BK-1A) |

### 5c. SEMI kinematic coupling standards

| Standard | What it covers | Numbers | URL |
|---|---|---|---|
| SEMI E57 | kinematic couplings that align and support 300 mm wafer carriers (cassettes, pods, FOUPs, shipping boxes): three pins on the tool, grooves on the carrier. Only the bottom half (the pins) is specified, so carrier makers are free in how they mate with it | pin size and repeatability not found (paywalled). The SEMI store lists E57-0616 as inactive | [SEMI store](https://store-us.semi.org/products/e05700-semi-e57-specification-for-kinematic-couplings-used-to-align-and-support-300-mm-wafer-carriers) |
| SEMI E47.1 | FOUP mechanical specification | not read | [SEMI store](https://store-us.semi.org/products/e04701-semi-e47-1-mechanical-specification-for-foups-used-to-transport-and-store-300-mm-wafers) |
| SEMI E15.1 | 300 mm tool load port | not read | [SEMI store](https://store-us.semi.org/products/e01501-semi-e15-1-specification-for-300-mm-tool-load-port) |

## 6. Quarter-turn, bayonet and camlock fasteners, ball-lock pins, latches and pneumatic clamps

| Item | Mechanism | Force | When unpowered / released | Typical use (as the source states) | Source |
|---|---|---|---|---|---|
| Carr Lane ball-lock pins (BLP/BPD/ABP) | push-button frees two balls; slip-fit pin, no preload | approx. pull-out / calculated double shear (lb, safety factor 2:1 as stated), steel / stainless: 6 mm 230 / 4,000 / 4,400; 8 mm 510 / 7,000 / 8,000; 10 mm 710 / 11,000 / 12,500; 12 mm 1,160 / 16,000 / 18,000. Grip > 8 in: shear −20 to −50 % | balls spring-locked | fixture location and quick release (manual) | [Carr Lane strength data](https://www.carrlane.com/engineering-resources/technical-information/ball-lock-pins-engineering-application/ball-lock-pin-strength-data) |
| (my arithmetic on the row above) | – | axial pull-out is only **5.8–7.3 %** of double-shear strength; recommended hole for 8 mm is 0.315–0.319 in (8.00–8.10 mm), i.e. up to ~0.1 mm clearance | – | a ball-lock pin locates and takes shear; it does not clamp | – |
| Kipp K0790 / K0791 high-shear ball-lock pins | same principle; 1.4542 pin, 1.4125 balls | 8 mm stainless: 63 kN double shear, "theoretical breaking load", "non-binding reference values without consideration of safety factors" (SE) | spring-locked | – | [Kipp K0791 datasheet](https://www.aftfasteners.com/content/K0791-Datasheet-22121-Ball-lock-pins-with-stainless-steel-mushroom-grip-and-high-shear-strength-enUS.pdf) (SE) |
| DESTACO 812 pneumatic toggle clamp (smallest pneumatic hold-down) | over-centre toggle driven by an air cylinder | 810 series: max holding capacity 856 lb (SE) | "Toggle-lock safety feature, so they stay mechanically locked even with total loss of air pressure" | "Common applications … include assembly and welding" | [DESTACO 812](https://www.destaco.com/en/clamping/pneumatic-clamping/pneumatic-toggle-clamp/standard-pneumatic-clamps-812) |
| Southco / Camloc / DZUS quarter-turn fasteners | stud turns 90° into a receptacle | small series max static load 440 N; 2600/2700 series 1,330 N tensile, 900 N working; D4002 4,700 / 3,100 N; 991F 10,000 / 7,000 N (all SE, distributor listing) | spring receptacle holds the stud | access panels and doors | [Southco DZUS on GlobalSpec](https://datasheets.globalspec.com/ds/southco/d4-ehf5-55/f360ca7d-65ab-42a3-980b-fb3bfb40d4a0) (SE); [selection guide](https://industrialmonitordirect.com/blogs/knowledgebase/quarter-turn-fasteners-for-industrial-panels-selection-guide) (SE) |
| Bayonet on an LPBF plate | One Click Metal's starter package lists a "bayonet lock" with the substrate plates (SE) | not found | – | manual plate change on a small LPBF | §1 |
| Push-in "click" latch | STARK.easyclick: clicks in, spring-held with no energy, released by 4 bar | 5 kN clamping, 10 kN retention | holds | "particularly suitable for use as a robot gripper" | §2 |
| Ball-lock preload post on a kinematic coupling | K-Dock on semiconductor test heads: kinematic coupling with a central ball-lock pull-in post | – | – | dock/undock "several times per shift" | §5 (Slocum 2010) |
| Pneumatic swing clamps | **not collected** (no time); see DESTACO and Roemheld catalogues | – | – | – | – |

Not found: any source that describes a robot actuating ball-lock pins, quarter-turn fasteners or toggle clamps as a routine exchange method. In
the sources found these are hand-operated (pins, quarter-turns) or air-operated with a mechanical lock (toggle clamps, zero-point chucks).

## 7. Robot screwdriving

### 7a. Tools (vendor claims)

| Product | Mechanism | Torque | Screws | Speed / cycle | Limits | Price | URL |
|---|---|---|---|---|---|---|---|
| OnRobot Screwdriver (datasheet v1.7) | electric (2 × BLDC), screw held on the bit; "Material type: Magnetic" | 0.15–5 N·m; ±0.04 N·m below 1.33 N·m, ±3 % above | M1.6–M6 (M6 cylinder head, countersunk and button head); length ≤ 50 mm (35 mm thread) | 340 rpm max; 55 mm shank stroke; shank preload 0–25 N | operating 5–50 °C; IP54; 2.5 kg; warranty 3 years or 3 million cycles | not listed | [datasheet PDF](https://onrobot.com/storage/datasheets/screwdriver/datasheet_screwdriver_v1.7_en.pdf) |
| Robotiq Screwdriving Solution (UR e-Series) | electric screwdriver, SF-300 feeder | 0.3–4 N·m on Robotiq's page; other listings say 0.5–4 or 1–4 N·m | M2.5–M5, 4–25 mm long | 1–600 rpm (product sheet); feeder cycle ~3 s (distributor) | – | not found | [Robotiq](https://robotiq.com/solutions/assembly/), [UR+](https://www.universal-robots.com/marketplace/products/01tP40000071NgFIAU) |
| Weber (fixtured / robot feed screwdrivers, e.g. SER-L/SEV-L for lightweight robots) | blow-fed screws | not checked | – | "A cycle time of <1 s is possible" start to start; step feeder up to 0.8 s; feed hose ~10 m/s guide value | – | – | [Weber FAQ](https://www.weber-online.com/en/test-faq-en/) |
| Atlas Copco MicroTorque MTF6000 + QMC/QMT spindle (UR+) | low-torque spindle | "low torque" (figure not found) | – | – | lists cross-thread detection among its error-proofing features | – | [UR+](https://www.universal-robots.com/plus/products/atlas-copco/microtorque-mtf6000-qmcqmt-spindle/) |
| Atlas Copco QST fixtured nutrunners | fixed or robot-carried nutrunner spindles | QST42 from about 6–20 N·m and up; QST50 20–90 N·m (snippet only; page returned 404 through the proxy) | – | – | – | – | [Atlas Copco QST](https://www.atlascopco.com/en-hu/itba/products/assembly-solutions/fixtured-assembly-solutions/qst-fixtured-nutrunner) |
| Reference torque, M6 on a UR flange | – | UR specifies M6 class 8.8 (ISO 4762) at 8.0 N·m for end effectors on the tool flange (snippet only) | – | – | – | – | [UR article](https://www.universal-robots.com/articles/ur/application-installation/end-effector-mounting-on-tool-output-flange/) |

### 7b. Failure modes and evidence

| Source | Finding | URL |
|---|---|---|
| Aronson, Bhatia, Jia et al., "Data-driven classification of screwdriving operations", ISER 2016, Springer SPAR, DOI 10.1007/978-3-319-50115-4_22 (measured) | 1,862 robot screwdriving runs logged (force, torque, current, speed, video). The most common failure was not acquiring the screw before the run started (a pick-up failure, blamed on their vacuum adapter). Cross-threading is the one failure that doesn't pass through its own stages, so the stage sequence doesn't flag it. "Even a one percent failure rate in screwdriving can generate tens of thousands of bad products." The per-class percentages are in their Table 1 (not extracted) | [Springer](https://link.springer.com/chapter/10.1007/978-3-319-50115-4_22) |
| Jia, Bhatia, Aronson, Bourne, Mason, "A survey of automated threaded fastening", IEEE T-ASE 16(1):298–310, 2019 (DOI 10.1109/TASE.2018.2835382, from the accepted manuscript; check on Xplore) | Automated fastening is robust only up to a point, "especially for small screws". Covers feeding, pickup, alignment, driving, failure modes and how to mitigate them | [CMU record](https://publications.ri.cmu.edu/a-survey-of-automated-threaded-fastening), [IEEE](https://ieeexplore.ieee.org/document/8392410) |
| Pencom technical bulletin, "Galling of stainless steel fasteners" (fastener vendor) | Galling is the main problem with stainless. Causes: axial misalignment, high-rpm drivers ("as installation rpm's increase so does the heat"), the same materials on both sides, rough or cut threads, and "grit and debris in the threads". Best design: the screw runs freely to the seat, then goes from snug to full load within 90°. 400-series against 300-series galls less; mixing 304/316 is "debated". Mechanically deformed stainless locknuts are "almost certain to gall". Fixes: wax, baked PTFE or MoS₂ coatings | [PDF](https://www.pencomsf.com/wp-content/uploads/technical-reference-files/galling_stainless_steel_fasteners.pdf) |
| ASSDA Technical FAQ 5, "Galling and its control" | a 304 bolt with a 316 nut "is not necessarily sufficient"; a harder nut (duplex or martensitic 431) reduces risk; nickel-based anti-seize is common | [ASSDA](https://assda.asn.au/publications/technical-faqs/galling-and-its-control) |
| Birmingham, robot unfastening of hex screws (IEEE T-ASE 2020, DOI 10.1109/TASE.2019.2958712) | spiral search to engage the head; "can only deal reliably with undamaged screws". Success rate not found | [record](https://research.birmingham.ac.uk/en/publications/unfastening-of-hexagonal-headed-screws-by-a-collaborative-robot/) |

Is screwdriving used for exchanging tools or fixtures? No vendor or paper found presents robot screwdriving as a way to
exchange tools, fixtures or pallets. Every source above is about product assembly, or disassembly for recycling.
Robot tool and fixture exchange uses tool changers and zero-point or kinematic interfaces instead (see the parent's
categories 2–3).

## 8. Standards and guidelines

| Standard | Covers exchangeable fixtures? | Key content and numbers | URL |
|---|---|---|---|
| ISO 9409-1:2004 (plates; replaces 1996) | yes: robot flange ↔ end effector | Fixes dimensions, designation and marking of the circular flange "to ensure the exchangeability" and orientation of end effectors. Doesn't specify the coupling device or a load rating. 1996 Table 1: pitch circles 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250 mm (series 1/2). Threads: M5 (31.5), M6 (40–63), M8 (80–100), M10 (125–160), M12 (200–250). One H7 location-pin hole (cylindrical or diamond pin), a spigot or recess as datum. Designation e.g. "ISO 9409-1-A40" (the extracted table is garbled, so check thread sizes against the standard) | [1996 preview PDF](https://cdn.standards.iteh.ai/samples/20624/26c34755c9c545da848669c8338f504f/ISO-9409-1-1996.pdf), [2004 record](https://www.evs.ee/en/iso-9409-1-2004) |
| UR10e flange | – | EN ISO 9409-1-50-4-M6 (50 mm pitch circle, 4 × M6) | [UR datasheet](https://www.universal-robots.com/manuals/latest/en/datasheets/ur10e/) |
| ISO 9409-2:2002 (shafts) | yes: shaft-type flange | no load ranges; also meant for simple pick-and-place units | [record](https://www.evs.ee/en/iso-9409-2-2002) |
| SEMI E57 / E47.1 / E15.1 | yes: carrier ↔ tool (kinematic pins) | see 5c; numbers paywalled | see 5c |
| ANSI/SLAS 1-2004 (R2012), microplate footprint | yes in practice: any SBS plate fits any nest or gripper | 127.76 ± 0.25 mm × 85.48 ± 0.25 mm within 12.7 mm of the corners; ± 0.5 mm anywhere along a side; footprint continuous; corner radius 3.18 ± 1.6 mm; at 20 °C. SLAS 2 (heights), 3 (bottom flange), 4 (well positions) are companions. No SLAS standard for the nest itself was found | [SLAS 1 PDF](https://slas.org/SLAS/assets/File/public/standards/ANSI_SLAS_1-2004_FootprintDimensions.pdf), [SLAS standards](https://www.slas.org/education/ansi-slas-microplate-standards/) |
| VDI 2740 Blatt 1 (1995), grippers for manipulators and industrial robots | grippers, not fixtures | listed as current, 47 pages; contents not read | [VDI](https://vdi.de/en/home/vdi-standards/details/vdi-2740-blatt-1-mechanical-devices-for-automation-equipment-grippers-for-manipulators-and-industrial-robots) |
| VDI 2860 (1990-05), handling functions, terminology and symbols | terminology only | a new draft of Blatt 1 exists | [DIN Media](https://www.dinmedia.de/en/technical-rule/vdi-2860/847032), [VDI](https://vdi.de/en/home/vdi-standards/details/vdi-2860-blatt-1-assembly-and-handling-units-handling-functions-handling-units-terminology-definitions-and-symbols) |
| DIN 69893 / ISO 12164 (HSK), ISO 26623 (Capto, made an ISO standard in 2008 when the patent expired) | yes: spindle ↔ tool holder, for automatic tool change on machine tools | repeatability figures not found | [CTE on Capto](https://www.ctemag.com/articles/polygon-power) |
| Zero-point clamping (pallet ↔ machine table) | – | No ISO, DIN or VDI interface standard found. Every system found is vendor-specific (Schunk VERO-S, Zimmer SPN, KIPP UNILOCK and others), and clamping pins differ between makers. This is "not found", not a proof that none exists | [Zimmer SPN](https://zimmer-group.com/en/products/components/machine-tooling-technology/zero-point-clamping-system/standard-series), [KIPP](https://sk.kipp.sk/sk/en/Products/Clamping-technology/Zero-Point-Clamping-Technology/Zero-point-clamping-system.html) |
| Boothroyd–Dewhurst DFA (secondary summary) | design rule | Fastening methods ranked by increasing assembly cost: snap fit < plastic bending < riveting < screw fastening. Remove separate fasteners where you can | [summary](https://engineeronadisk.com/notes_design/dfmaa3.html) |

### Key facts (kinematic couplings, screwdriving, standards)

1. **Robot screwdriving is an assembly process, not a way to swap fixtures.** No source found uses it for tool, pallet or
   fixture exchange. Its most common failures are a missed screw pickup and cross-threading, and cross-threading is the
   hard one to detect ([Aronson 2016](https://link.springer.com/chapter/10.1007/978-3-319-50115-4_22)).
2. **The cobot screwdrivers can't fully tighten an M6.** OnRobot's tops out at 5 N·m and M6 and needs magnetic screws, so
   18-8 stainless screws can't be held on its bit; this is an inference from "Material type: Magnetic"
   ([datasheet](https://onrobot.com/storage/datasheets/screwdriver/datasheet_screwdriver_v1.7_en.pdf)). Robotiq's covers
   0.3–4 N·m and only up to M5. UR itself torques an M6 8.8 flange bolt to 8 N·m. A captive thumb screw driven
   hand-tight is within their range.
3. **Stainless on stainless galls, and debris makes it worse.** That fits the 18-8 thumb screws in stainless helical
   inserts in a powder chamber. Pencom names "grit and debris in the threads" and high-rpm driving as causes and
   recommends low rpm, wax or MoS₂, and harder 400-series or duplex mates
   ([Pencom](https://www.pencomsf.com/wp-content/uploads/technical-reference-files/galling_stainless_steel_fasteners.pdf),
   [ASSDA](https://assda.asn.au/publications/technical-faqs/galling-and-its-control)).
4. **Kinematic couplings reach about 1 µm only in clean lab conditions.** In the lab they repeat to 0.05–1 µm (Slocum
   2010; Culpepper 2004: 0.25 µm). On a shop floor with variable preload and dirt they repeated to 50–110 µm, and the
   mounting procedure mattered about as much as the coupling design (Hart 2004; Willoughby 2005). Those figures were
   measured at the tool point of a large ABB robot, which magnifies angular error at the coupling. My inference, not a
   published result: if the plate only needs height referencing to a few µm or tens of µm, a cheap three-pin or
   quasi-kinematic interface is enough. Hart 2004 reaches the same conclusion for dirty, variable conditions.
5. **Contact materials set the cycle life.** Plain steel ball on steel groove fretted from sub-µm to about 10 µm in
   several hundred cycles. Ceramic (Si₃N₄) or polished stainless, carbide or ceramic contacts are recommended for
   high-cycle use (Slocum 2010). A plate swapped after every build is high-cycle over the machine's life.
6. **Magnets are an accepted preload only for light loads.** Slocum 2010 puts magnets with instruments; heavy-duty
   couplings use bolts or springs through the ball centres, and vertical couplings use a clamp or gravity. Commercial
   magnetic kinematic bases claim 30–100 µm or µrad-level repeatability for about $100, but none states its magnet
   force.
7. **Thermal behaviour of a hot plate.** With uniform expansion the coupling's instant centre is also its thermal
   centre. With non-uniform expansion the plate can seat with hysteresis through micro-slip (Slocum 2010). A 3-groove
   pattern centred on the plate keeps its centre fixed as it grows.
8. **Standards cover the robot flange, not the fixture.** ISO 9409-1 standardises the robot-to-tool flange (the UR10e is
   ISO 9409-1-50-4-M6), SEMI E57 standardises carrier pins, and ANSI/SLAS 1 standardises the plate footprint
   (± 0.25 mm). No standard was found for zero-point pallet interfaces, so a zero-point system ties you to one vendor.
9. **DFA ranks screw fastening as the most expensive way to fasten** and says to remove separate fasteners where
   possible (secondary summary of Boothroyd–Dewhurst).

## 9. Standard practice: frequent robot exchange vs occasional manual exchange

What the sources above show (citations are in the sections named):

**Frequent, robot-loaded exchange (pallets, fixtures, EDM electrodes, end effectors)**
- The standard is a **spring-locked, air-released zero-point chuck** (EROWA ITS, System 3R Macro, SCHUNK VERO-S, STARK.easyclick, AMF, Zimmer
  SPN; §2) or, for end effectors, a **ball-lock tool changer** (ATI, SCHUNK SWS, Stäubli MPS, Zimmer WWR; §3). Not screws, and not robot
  screwdriving (§7: no source uses screwdriving for exchange).
- The features these products share are what make them robot-friendly:
  1. a taper or pin that centres the part and gives 1.5–15 µm repeatability;
  2. a lock that holds with air or power off (spring or reverse taper);
  3. release by 4–6 bar air or a 24 V motor, so the robot only places and lifts and applies no torque;
  4. cleaning air and a seat or slide-position sensor, sold as options;
  5. a capture window the robot has to hit with some compliance: ±0.4 mm radial for STARK, ±1 mm and ±2° for SCHUNK SWS-011.
- **Temperature is the catch.** Ordinary units are rated to 50–80 °C:
  - SCHUNK says conventional pallet systems work to about 60 °C.
  - Zimmer SPN: −10 to +70 °C.
  - STARK with NBR seals: 80 °C.
  - Tool changers: 50–66 °C.

  Versions rated for AM exist:
  - STARK with FKM seals: 150 °C.
  - AMF modules: seals for 150 °C and above.
  - SCHUNK NSE-AM mini 78-20 and NSE-HT mini 88-20: 200 °C maximum actuation temperature, sealed against fine metal dust, inert-gas rated.

  Above 200 °C, SCHUNK's manual (SE) says the clamping-pin screw loses holding force and must be replaced after the cycle. No actuated
  module rated to 200–225 °C was found; only SCHUNK's passive NE-HT centring unit is rated to 500 °C (SE).
- **In LPBF:**
  - Plate exchange is robotic at Additive Industries.
  - High-throughput machines automate the whole cylinder or frame instead: Nikon SLM 25 min, EOS with Grenzebach under 30 min, Velo3D 15 min.
  - Where a vendor names a plate interface, it is a zero-point system: System 3R on 3D Systems, SCHUNK on the DMG MORI LASERTEC 30, AMF on
    Matsuura, TRUMPF.
  - DMG MORI's robot handles small "pucks" printed on, a close analogue of Ø25–75 plates.
  - Neher's set-up uses one centring pin as the "thermal zero point" with four clamping modules.
- **Magnets:** robot magnetic grippers are common for ferrous parts, but every small unit found is rated to 40–80 °C (§4).
  - Electro-permanent units keep holding when power is lost.
  - They are weak in shear (22–35 % of pull-off).
  - They lose 27 % → 7 % of their force across a 0.1–0.25 mm gap for a Ø25 pole.
  - They give zero force on 6061 or 316, so the plate would need a 430 or 416 strike plate 2.5–5 mm or more thick.
  - Hot-rated (230–240 °C) magnetic clamping exists only as large mould-clamping platens.
  - For LPBF build plates, magnets appear only in patents (Blue Origin, GE).
- **Kinematic couplings:** these are the precision answer for gravity- or spring-preloaded seats (SEMI E57 FOUP pins, instrument bases, K-Dock).
  - Lab repeatability is 0.05–1 µm.
  - With dirt and variable preload, the measured figure was 50–110 µm at a large robot's tool point.
  - Cleaning and the preload procedure mattered about as much as the coupling design.
  - Ceramic or polished stainless contacts are needed for high cycle counts (§5).

**Occasional, manual exchange (between campaigns, by a person)**
- Screws or bolts are the default: most LPBF plates are screwed down. People also use captive thumb screws, ball-lock pins for location and
  shear (pull-out is only about 6–7 % of their shear strength), quarter-turns for panels, and toggle clamps with a mechanical over-centre lock (§6).
- The known costs of screws:
  - System 3R says manual plate attachment needs levelling, and unscrewing in powder is "tricky".
  - Stainless-on-stainless threads gall, worse with grit and fast driving (§7).
  - DFA ranks screw fastening as the costliest joining method (§8).
- If a robot ever has to turn screws: cobot screwdrivers top out at 4–5 N·m and M5–M6, and OnRobot's needs magnetic screws. The common failures
  are a missed pickup and cross-threading, and cross-threading is the hard one to detect (§7).

**Facts that bear directly on this design** (my reading, for the caller's calculations):
- **The build plate runs hotter than any rating found.** It is swapped every build by a robot, on a 200–225 °C block, in argon and fine Al
  powder. The hottest actuated zero-point module found is rated to 200 °C actuation (SCHUNK NSE-AM/HT), and that is the closest catalogue
  precedent. Anything at 200–225 °C is beyond published ratings, unless the clamp sits below a cooler layer or the hot interface is passive (a
  seat with a preload from outside the hot zone). A magnet at that temperature would have to be SmCo, AlNiCo or EH/AH-grade NdFeB, acting on a
  ferritic strike plate, with no off-the-shelf small module rated for it.
- **The build module flange is near the limit of ordinary seals.** At 60–85 °C it sits at or above the rating of standard NBR-sealed
  zero-point and tool-changer units (50–80 °C). The FKM versions (STARK ET, 150 °C) or AM versions cover it. Captive screws fit occasional
  manual swaps, but the 18-8 screw in a stainless insert is the galling-prone pair.
- **The Z-coupling magnet is under-rated.** McMaster 5679K95 is NdFeB rated to a maximum of 175 °F (79 °C) (§4, confirmed on the McMaster
  page). Check its temperature under a 200–225 °C module.
- **Not found:**
  - plate-fastening details for EOS, Renishaw, Farsoon, Xact, Aconity and Velo3D;
  - Röhm small-module data;
  - any measurement of holding-force loss or repeatability loss from fine powder in a magnetic or kinematic joint;
  - any zero-point interface standard.
