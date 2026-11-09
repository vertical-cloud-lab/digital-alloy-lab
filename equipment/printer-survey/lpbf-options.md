<!-- Public extract of sgbaird/byu-finances proposals/capital-equipment-2026/lpbf-options.md (2026-11-09), trimmed for vertical-cloud-lab/digital-alloy-lab: figures and specs from a private vendor quote were removed. Every price left is a vendor list price, reseller listing or press figure, or an estimate marked [I]. -->

# Compact / desktop LPBF for small-batch novel Al alloys: comparison (web research, 2026-11-09)

Context: BYU ME, room CB 154. The printer would sit next to an AMAZEMET rePOWDER ultrasonic atomizer making 0.1-2 kg batches (D50 often ≥45 µm, more O than gas-atomized powder). The use is Bayesian-optimization / closed-loop LPBF parameter qualification across many Al compositions. The lab's current reference machine is the Univ. of Utah Aconity MIDI.

Evidence tags: **[V]** vendor claim, **[P]** peer-reviewed (including reviewed SFF proceedings), **[R]** press, reseller or aggregator, **[I]** my inference or arithmetic. Bracketed IDs such as [AO2] point to the source list at the end. No vendors were contacted.

Limitation: the web-search budget for this session ran out near the end. Some items could not be checked: papers using a Sisma or ORLAS machine for Al, Han's Laser models, the EOS M 100 gas spec, and whether plate heating exists on the XM200G. Treat those as open questions.

---

## TL;DR

- **Powder economy:** Only a few machines can run builds from rePOWDER-sized batches without a full-size powder charge:
  - AO Metal A30: 25-156 g of Al per build [AO2]
  - Aconity MIDI with the Ø55 mm platform plus powder feeder: about 20 cm³ [AC7]
  - Sisma MYSINT100 with a Ø34 mm cylinder [SI1]
  - TruPrint 1000 with the Ø50 mm reduction [TR1]
  - One Click Metal Lab module, 78×53 mm [OC2]
  - Sharebot MetalONE: 800 g minimum load [SB1]
  - Renishaw RBV-style kits [SW1]
- **No peer-reviewed Al density data on the new desktop class.** I found none for the AO A30, FastForm, SnowPod, Scrap 1 or similar machines. Dense AlSi10Mg is well documented at about 200 W on research machines ([PH2][PH3]), so the physics allows it. Atmosphere (O₂), powder quality and parameter windows are the real risks. Require an acceptance print with your own rePOWDER powder.
- **API / closed loop:** Aconity is the only vendor with a documented Python API for changing per-part parameters in real time [AC5]. Sharebot exposes G-code laser paths and a parameter-search mode [SB1]. Most others offer only "open parameters" in a GUI slicer. That is enough for batch-sequential BO (one parameter matrix per build) but not for in-layer control.
- **Plate heating:** This matters for crack-prone Al-Mn-Cr-Zr and Sc/Zr alloys and is missing on most cheap machines. The A30 has none [AO1]. The One Click Metal Lab module goes to 200 °C [OC2], the Prima Print 150 family to 300 °C [PR1], and Aconity to 800-1200 °C ([AC3][AC6]).
- **Ranked shortlist** (details in section 3):
  1. **Xact Metal XM200G** (400 W, Reactive/argon, XMini module), all-in about $170-250k
  2. **AO Metal A30-300**, all-in about $90-130k, *conditional* on an acceptance test and origin documentation
  3. **One Click Metal MPRINT + Lab module (200 °C)**, all-in about $180-270k
- **Cheaper interim option:** Ask Aconity/Utah about the Ø55 mm reduced-platform + powder-feeder kit for the MIDI you already use [AC7]. It may let you print rePOWDER batches before any purchase.

---

## 1. Comparison table (price first)

| System | Price (USD; source, year) | Build volume · small-build option · min. Al charge | Laser | Atmosphere · O₂ | Plate heat | Openness · API · monitoring | Al evidence · reactive-powder rules | Facility | Origin · US support |
|---|---|---|---|---|---|---|---|---|---|
| **AO Metal A30** (-200/-300) | $59k (200 W) / $64k (300 W) [AO2 V, 10/2026] | Ø30×60 mm; the whole machine is small-build. **Al: 25 g** (10 mm test parts), **49 g** (20 mm parts), **156 g** (full dispenser) [AO2 V] | 200 or 300 W fiber, 1064 nm; 75 µm spot (55 µm opt.); ≤12 m/s; 15-100 µm layers [AO2 V] | Ar, "<2 L/min"; filter + gas loop [AO1 V]. **No O₂ spec published** | **None** (250/900 °C only on A50/A100) [AO1 V] | Power, speed, pattern, hatch, layer, contour/infill set zone-by-zone in AO Build Slicer [AO1 V]. API not stated; monitoring not specified | "Aluminium"/AlSi10Mg in 9 "proven" alloys [AO2 V]; no density data or papers found. No Al restriction; explosion-proof wet vac required for reactive metals [AO2 V] | 120 V 1-ph 60 Hz, ≤2.5 kW, "dedicated 50 A circuit"; 1000×620×1100 mm; **≈100 kg** [AO2 V] | "Designed and manufactured in the U.S.A.", Additive Plus, Gardena CA [AO2 V]. Provenance questions raised by press [AO4 R] (see notes) |
| **One Click Metal MPRINT** (+Lab module) / MPRINTpro | MPRINT ≈€89k; "$149k in the US" as printed. MPRINTpro €120k / $149k. MPUREpro sieve $39k [OC5 R, 11/2025] | 150×150×150 (195 ext.). **Lab module 78×53×90 mm** (MPRINT only) [OC1][OC2 V]. Charge not published; [I] ~0.3 kg for a 20 mm-tall Lab build | MPRINT 200 W fiber, 70 µm, 22 m/s jump, 20-80 µm. Pro 500 W, 80 µm, 20-120 µm [OC1 V] | N₂ or Ar. Replaceable gas filter (MPRINT); self-cleaning permanent filter on Pro [OC1 V][OC5 R]. O₂ not published | **≤200 °C** (Heating and Lab modules) [OC2 V] | "Open parameters" (reseller) [OC9 R]. Vendor sells parameter sets; "third-party powder or modified parameters cannot be guaranteed" [OC3 V]. No API found | AlSi10Mg and Elementum **6061-RAM2** offered [OC3][OC4 V]; OCM AlSi10Mg ≈€70/kg [OC5 R]. No papers found | MPRINT 230 V, 9.5 A; Pro 220-240 V, 13.5 A; 1.1×1.9×0.8 m; 440/500 kg [OC1 V] | Germany (Tamm). TRUMPF spin-off 2019, INDEX Group majority 2021 [OC7 R]. US via reseller (MasterGraphics, now m5d) [OC8 R] |
| **Xact Metal XM200G** / XM200C | XM200C **$65k** [AO4 R, 4/2025]. XM200G **from $90k MSRP** [XM3 R]. Options quote-only | XM200C 127³ mm; XM200G 150³ mm (Z ext. to 290 mm). **"XMini Material Development Module"** option, size not published [XM4 R]. [I] standard bed needs ~1.5 kg for a 20 mm build | XM200C 100 W Yb (200 W kit), >20 µm, gantry scanner ≤650 mm/s [XM1 V]. XM200G 1-2× 100/200/**400 W**, **50 or 100 µm** [XM2 V] | "Non-Reactive or **Reactive**" configuration [XM4 R]; reactive means argon for Al/Ti, per launch press [XM3][XM6 R]. O₂ shown on HMI, value not published | Not documented (verify) | "Open platform… develop their own printing parameters and use their own powder" [XM1 V]. 2 cameras (XM200C) [XM8 R]. No API found | XM200C: AlSi10Mg "with optional kit". XM200G lists AlSi10Mg [XM1][XM2 V]. **XM200G AlSi10Mg study** (390 W, 60 µm; 355 MPa UTS) [XM5 P] | 100-120 **or** 200-240 VAC 1-ph, 1.5 kW (2 kW peak); "not all configurations on 120 V". XM200G 650×780×1930 mm, ~380 kg [XM2 V] | **USA** (State College, PA). Resellers GoEngineer, Cimquest |
| **Sisma MYSINT100** | Quote only (none found) | Ø100×100 mm. **Removable cylinders Ø34 / Ø63.5 / Ø100 mm** [SI1 V]. [I] Ø34 mm needs ~0.1 kg for a 20 mm build | 200 W (opt. 2×200 W), 55 µm (opt. 30 µm), ~1070 nm, 7 m/s, 10-50 µm [SI1 V][SI2 R] | N₂/Ar [SI1 V]. O₂ not published | Not stated | Not stated | **Glove box "required for titanium and aluminium"** [SI1 V]. No Al papers checked | 230 V 50/60 Hz; 1445×730×1680 mm; 650 kg [SI1 V] | Italy. Platform the TruPrint 1000 was derived from [SI3 R]. No US support found |
| **TruPrint 1000 → ATLIX xBUILD 1000** (+ Green Edition) | New "from $170k" [TR6 R]. Used 2019 units €95-100k [TR7 R] | Ø100×100 mm. **Optional Ø50×100 mm reduction "when using high-priced materials"**; interchangeable cylinders + glovebox [TR1 V]. [I] ~0.15 kg for a 20 mm Ø50 build | 200 W fiber (opt. 2×200 W), 80 µm (opt. motorized 55/80 µm), 2 m/s, 20-60 µm [TR1 V]. **Green Ed.:** TruDisk 1020, 515 nm, 1×500 W, **200 µm** beam, Ø97×100 mm [TR2 V] | N₂/Ar. **O₂ ≤3000 ppm standard; ≤100 ppm option** [TR1 V] | Not listed for the 1000 (2000/3000 list ≤200 °C) [TR2 V] | "Parameter availability upon request"; built-in powder-bed camera with image analysis [TR1 V]. No API found | **Aluminum "available with specific option"** [TR1 V]. Röchling lists its TruPrint 1000 for AlSi10Mg [TR8 R]. Green Ed. marketed for Cu and precious metals [TR2 V] | 230 V / 7 A; 780×2050×1160 mm; 900 kg incl. powder; fits a standard door [TR1 V] | ATLIX (Schio IT / Ditzingen DE), carved out of TRUMPF 2025, PE-owned. Renamed xBUILD 2026-09-01, "technically unchanged" [TR3-TR5 R] |
| **Aconity MINI** (MIDI for reference) | "Price on demand" [AC3 R]; no public figure | MINI Ø140 × 190-200 mm [AC2][AC3]. **MIDI: Ø55 mm reduced platform + powder feeder, builds from ~20 cm³** [AC7 V-user]. Ask whether the MINI takes the same kit | Single-mode 400 W or 1000 W; 80 µm F-theta or 80-500 µm 3D scanning; layers ≥10 µm [AC1 R] | Ar; optional vacuum chamber <1 mbar [AC3 R]. O₂ not published | MINI opt. **≤800 °C** [AC3]. MIDI induction **≤1200 °C** [AC6][AC7] | Full parameter autonomy [AC3]. **Aconity API: real-time per-part parameter changes from Python** [AC5]. Coaxial pyrometer, high-speed CMOS [AC1] | NUS lists Aluminium for its MINI [AC4]; Utah says Al printable on MIDI [AC6] | 2050×1500×2295 mm, **1155 kg** [AC2]. Electrical not found ([I] likely 3-phase) | Germany. AconityUS at UTEP, El Paso [AC8] |
| **Coherent / OR Laser ORLAS CREATOR** | ~€77k at 2016 launch [OR5 R]. **Listed discontinued** [OR3 R] | Ø100×110 mm [OR1 R] | 250 W Yb, 1070 nm, ≥40 µm [OR1][OR2] | Ar/N₂ [OR2] | n/a | n/a | One used listing claims Al (unverified) | 717×858×1794 mm; 470 kg [OR2] | Germany. Coherent removed its product page (~2021) [OR4 R] |
| **Farsoon FS121M** | On request [FA1 R] | 120×120×100 mm [FA1] | 200 W (reseller) or 300/500 W (datasheet) fiber; several spot sizes [FA2][FA3 R] | Not obtained | Not obtained | "Unlock machine parameters and powder choice" [FA2] | **No Al on FS121M list** (316L, 17-4PH, MS1, HX, Cu, CuSn10, CoCr) [FA3 R] | Not obtained | **China** (Changsha). Farsoon Americas, Round Rock TX [FA2]. West-Coast distributor is Additive Plus [AO7 R] |
| **EOS M 100** | No list price; aggregator $200-280k (low confidence) [EO3 R] | Ø100×95 mm incl. plate [EO1] | 200 W Yb, 40 µm [EO1] | Not confirmed; compressed air 4,000 hPa, 50 L/min [EO1] | n/a | EOSPRINT ([I] parameter editing is license-dependent; verify) | **No Al material** for M 100 in sources (CoCr SP2, 316L, Ti64) [EO2 R] | 200-240 V, ≤1.7 kW; 800×950×2250 mm; 580 kg [EO1] | Germany. EOS North America |
| **3D Systems DMP Flex 100** | Not found (academic bundles exist) [DM3] | 100×100×90 mm incl. plate [DM1] | **100 W** fiber, 1070 nm [DM1] | Not obtained | n/a | Closed LaserForm workflow ([I]) | No Al in LaserForm list found [DM1] | Not obtained | USA |
| **DMG MORI LASERTEC 12 SLM** | Aggregator $300-650k (low confidence) [LT2 R] | 125×125×200 mm. **rePLUG** powder module (<2 h material change); **rePLUG RESEARCH** for material/parameter development [LT1 V] | 200 W std, 400 W opt.; 35 µm focus; ≥20 µm layers [LT1 V] | Argon, "minimum consumption" [LT1 V] | Not stated | "Adjust all machine settings and process parameters", any powder supplier [LT1 V] | Al not listed [LT1] | Not obtained | Germany/Japan. DMG MORI USA |
| **Prima Additive Print Sharp 150** | Quote only | Ø150×160 mm; no reduction kit found [PR1 R] | 300 W single-mode Yb, 1070 nm, air-cooled [PR1 R] | O₂ monitoring <100 ppm (family page) [PR1 R] | **≤300 °C** (family page) [PR1 R] | Positioned for R&D | Aluminium in material list [PR1 R] | Not obtained | Italy |
| **Sharebot MetalONE** | ~€65k planned (2020) [SB2 R]; £67,875 UK retail (undated) [SB3 R] | 65×65×100 mm "laboratory size" distributor (100³ opt.). **Minimum powder load 800 g** [SB1 V]. Reducer kit to a ~Ø10 mm zone for scarce powder [SB4 V] | 300 W fiber, 1064 nm, air-cooled; 500/1000 W opts (chiller); 40 µm [SB1 V] | N₂-Ar, 2.5 L/min; N₂ generator option [SB1 V] | Not stated | **Open parameters, remote control, laser paths in G-code, built-in camera, parameter-search test mode, log file** [SB1 V] | Al not confirmed ("produce your own alloys"). **ATEX vacuum with oil inertization** option [SB1 V] | 1050×600×1500 mm; ~315 kg [SB1 V] | Italy. No US support found |
| **Open Additive PANDA** | From $219,900 [OA1 R]; $199k (2020) [OA2 R] | 152×152×178 mm [OA1] | Laser-agnostic open architecture [OA2] | Inert, reactive-capable [OA2] | Not obtained for PANDA (the AFRL large-format prototype had one [OA3]) | Open; AMSENSE sensing suite [OA4]; AFRL work on multi-sensor feedback control [OA3] | Not found | Not obtained | USA (Beavercreek OH). **openadditive.com now redirects to unrelated domains** (checked 2026-11-09); viability unclear |
| **BLT / Han's small models** | Not verified | BLT-A100 specs blank on Aniwaa [BL1 R] | n/a | n/a | n/a | n/a | BLT's Al alloys are on larger S-series machines [BL2 R] | n/a | China. BLT sold in US via GoEngineer [BL3 R] |

---

## 2. Notes per system

**AO Metal A30 (Additive Plus).**
- **Specs and price:** The Oct-2026 datasheet lists $59k (200 W) and $64k (300 W), Ø30×60 mm, 1064 nm fiber, 75 µm spot (55 µm optional), argon at <2 L/min, no plate heating, 120 V, about 100 kg. Installation, operator training and a 12-month warranty are included; lead time is 12-16 weeks [AO2]. The web page says 8-14 weeks [AO1].
- **Inconsistencies in AO's own materials:** The datasheet says ≈100 kg and a "dedicated 50 A" 120 V circuit, while its front page says "no dedicated room". The website also says Cu/Au/Ag need the blue laser, which only the A50/A100 offer [AO1], yet the A30 flyer lists gold and silver as "proven". Get these reconciled in writing, and check any quote against the datasheet.
- **Strongest point:** powder economy. 25 g of Al runs a 10 mm-tall test set [AO2], so one rePOWDER batch covers dozens of parameter builds.
- **Weak points for Al:**
  - no O₂ specification or logging spec
  - no plate heating
  - no API
  - no published Al density data
- **Provenance:** 3DPrint.com (2025-04-28) found AO's domains, phones and emails lead to Additive Plus / A Plus Industrial. It wrote that "almost all of those roads lead back to SIU System, a Russian 3D printer reseller and distributor". It could not identify AO engineering staff and left open whether the machine is Russian or a rebadged Chinese design [AO4]. That is an open question, not a finding.
- **Related facts:** Additive Plus is also Farsoon's (China) West-Coast distributor (since Feb 2024) [AO7]. Its "R&D bundle" pairs an A50 with an ATO Lab ultrasonic atomizer (3DLAB) and a Camsizer X2 [AO3][AO5]. For federal or university procurement, ask for a certificate of origin and the source countries of the laser, galvo and controller.

**One Click Metal (MPRINT / MPRINTpro).**
- **Company:** German TRUMPF spin-off, majority-owned by INDEX since 2021 [OC7].
- **Why it matters for small-batch alloy research:** The **Lab module** (78×53×90 mm) has a **200 °C preheatable plate** and is described as "ideal for research and material development" [OC2]. The tech-spec page lists it as an option on the 200 W MPRINT only; the 500 W MPRINTpro is listed with the Standard, Heating and Extended modules [OC1].
- **Al materials:** AlSi10Mg and 6061-RAM2 (an Elementum 3D crack-resistant 6061 variant) are offered as materials with sold parameter sets [OC3][OC4].
- **Pricing:** The 3DPrint.com pricing (Nov 2025) shows the same "$149,000 in the US" for MPRINT and MPRINTpro, which is probably an error. Budget conservatively.
- **Unknowns:**
  - how far users can edit parameters
  - whether the machine can be scripted
  - minimum cartridge fill

**Xact Metal (XM200G / XM200C / XM200S).**
- **Pricing and specs:** US-built. The XM200G can be configured with one 400 W laser, a 50 µm spot and a "Reactive" (argon) package, plus an **XMini Material Development Module** [XM2][XM4]. It runs on 100-120 V or 200-240 V single-phase [XM2]. The XM200C dropped to $65k when the XM200G launched at $90k [XM3].
- **Published Al use:** A reviewed SFF-2024 paper (Univ. of Southern Denmark and Taiyo Nippon Sanso) printed coarse (>100 µm) non-explosible AlSi10Mg on an XM200G at 390 W and 60 µm layers. The best set reached 355 MPa UTS, 220 MPa YS and 4.4 % elongation [XM5]. The same paper measured the explosibility of standard AlSi10Mg and pure Al powders, which is why the Reactive package matters [XM5].
- **XM200S:** the 2018 sibling, not evaluated separately; the XM200G is the current platform.
- **Company health:** reports record orders in 2026 [XM9].
- **Unknowns:** XMini dimensions and minimum charge, plate heating, O₂ ppm and logging, and the build-file format or API.

**Sisma MYSINT100.**
- **Small-build option:** Three removable build cylinders (Ø34 / Ø63.5 / Ø100 mm) [SI1]. The Ø34 mm cylinder is among the smallest powder charges on an industrial machine.
- **Al handling:** The vendor says the glove box is *required* for Ti and Al [SI1].
- **Lineage and support:** The TruPrint 1000 was derived from this platform [SI3]. Sisma now focuses on jewelry, so US research support is doubtful. There is no published preheat or O₂ spec.

**TRUMPF TruPrint 1000 (now ATLIX xBUILD 1000).**
- **Al-relevant options:** The best-documented Al options among compact industrial machines:
  - O₂ option down to 100 ppm
  - Ø50 mm reduced build for expensive powders
  - Al "available with specific option"
  - motorized 55/80 µm optics
  - powder-bed camera
  - (all from [TR1]) plus an industrial AlSi10Mg user [TR8]
- **Drawbacks:** Only 200 W per laser. No documented preheat or API. The vendor changed hands: TRUMPF's AM unit was sold in 2025 and rebranded ATLIX, with xBUILD names from Sept 2026 [TR3-TR5].
- **Green Edition:** 500 W at 515 nm with a large 200 µm beam [TR2], built for Cu and precious metals. For Al, green offers little absorptivity advantage ([I], see section 4).

**Aconity MINI / MIDI.**
- **Strengths:** The reference class for this kind of research:
  - single-mode 400/1000 W lasers
  - preheat up to 800 °C (MINI) or 1200 °C (MIDI)
  - pyrometer and camera options
  - documented API used to change part parameters in real time from Python [AC5]
- **Drawbacks:** Not compact (MINI 1155 kg) and quote-only.
- **Small-batch fit:** AMAZEMET runs an Aconity MIDI with a **Ø55 mm reduced platform and powder feeder that prints from ~20 cm³ of powder** [AC7]. AMAZEMET and Aconity3D also co-exhibited at Formnext 2025 [AM4]. This is the closest thing to an "AMAZEMET LPBF partner". AMAZEMET does not sell an LPBF printer.

**Coherent/OR Laser ORLAS CREATOR.** Listed as discontinued [OR3]. Coherent removed its page [OR4], and the brochure host no longer resolves ([I], observed). Not recommended for new purchase.

**Farsoon FS121M.**
- **Specs and Al:** Chinese; US subsidiary in Round Rock TX. Al is not on the FS121M material list [FA3].
- **Procurement flag:** Factually, both Chinese-made and the brand that Additive Plus distributes [AO7].

**EOS M 100.** A dental/medical machine. Its materials list (CoCr, 316L, Ti64) has no Al [EO2]. Poor fit.

**3D Systems DMP Flex 100.** Its 100 W laser [DM1] is too low for productive Al work [I], and no Al material is listed.

**DMG MORI LASERTEC 12 SLM.**
- **Strengths:** Open parameters, any powder supplier, and the rePLUG RESEARCH module for material and parameter development [LT1].
- **Drawbacks:** 125×125 mm bed and no published minimum charge. Price only from an aggregator (high).

**Prima Additive Print Sharp 150.**
- **Strengths:** 300 W single-mode laser, ≤300 °C plate, <100 ppm O₂ monitoring, Al listed [PR1]. Good Al physics.
- **Drawbacks:** Ø150 mm bed with no reduction kit found, so a larger powder charge. Italian vendor; US support not found.
- **Sibling:** A dual-wavelength Print Genius 150 went to the University of Birmingham [PR2].

**Sharebot MetalONE.** The best "scriptable small-batch" spec sheet of the cheap machines:
- 800 g minimum load and 65×65 mm lab distributor
- G-code laser paths, parameter-search mode, camera and logs
- 300-1000 W lasers and an ATEX inerting vacuum [SB1]

The drawbacks are no confirmed Al results, no preheat spec, no US support and an older (2019-20) product.

**Open Additive PANDA.**
- **Strengths:** Truly open, US-made and sensor-rich, with AFRL feedback-control work [OA2-OA4].
- **Viability risk:** The website domain now redirects elsewhere and I found no 2025-26 news. I could not identify a product called "AMSL"; the company's sensing product is AMSENSE [OA4].

**New 2025-2026 entrants.** None has documented Al density data; none is recommended for this use yet [I].
- **Mastrex MX-Series** (US-based): desktop from $39k; MX-300 at $185k with dual 500 W; Al claimed [NE2].
- **FastForm DeskFab X1** (China): 300 W; Al claimed; ~1,000 machines shipped in H1 2025 [NE5].
- **SnowX SnowPod:** Kickstarter Q4-2026, 80×80×100 mm, 316L is the only material named [NE1].
- **Scrap Labs Scrap 1:** $14.2k kit / $18k assembled; ships 2027 [NE3].
- **Metal Base Metal 1.0:** 60 W diode, ~€8.5k [NE4].
- **Xact XM200G µHD:** 25 µm spot, for 5-15 µm powder, so not a fit for coarse ultrasonic powder [NE6].
- **Others in 3DPrint.com's 2025 roundup** (no Al data): Phrozen FORGE, 2OneLab Create, RitonLab, ADDiTEC Fusion S [AO4].

**Small-batch kits across vendors.**
- **Renishaw AM400 RBV:** 80×80 mm plate, ≤55 mm tall, no heated plate. Swansea used it with 3DLAB ultrasonic-atomized powder (D50 49 µm) and reached 99.25-99.79 % density in 316L [SW1, P]. This is direct evidence that ultrasonic powder at this PSD prints densely on a reduced platform.
- Also see TruPrint Ø50 mm [TR1], MYSINT Ø34 mm [SI1], OCM Lab [OC2], Xact XMini [XM4], DMG rePLUG RESEARCH [LT1] and Aconity Ø55 mm + feeder [AC7].

---

## 3. Ranked shortlist for "small-batch novel Al next to an ultrasonic atomizer, with closed-loop parameter optimization"

Ranking weights [I]:
1. Builds from ≤0.5-2 kg of powder
2. Al physics: ≥300 W preferred, argon, low and logged O₂, preheat a plus
3. Per-part parameter control with a scriptable job format or API
4. Price
5. US support and procurement risk

BO in practice is batch-sequential: each build carries a matrix of parameter sets, you measure density/cracking/microstructure, then BO picks the next matrix. Per-part parameters plus a scriptable build-file format are enough for that. True in-layer closed loop needs an API (Aconity), which none of the top 3 documents.

Cost assumptions (all [I], not quotes):
- USD, purchase-tax exempt, €1 ≈ $1.15
- argon from dewars/cylinders, no room renovation beyond an electrical drop and an O₂-depletion alarm
- year-1 service = vendor warranty; budget about 8-12 %/yr afterward
- accessory prices are typical US street estimates (benchmark: OCM MPUREpro sieve station $39k [OC5]; North-American AlSi10Mg $135-145/kg [XM5])

### 1. Xact Metal XM200G
**Recommended configuration:** single 400 W, 50 µm spot, **Reactive (argon)** package, **XMini Material Development Module**, glovebox, 200-240 V single-phase.

**Why first:**
- US-made with US support
- 400 W with a 50 µm spot gives Al processing margin
- open parameters with third-party powder [XM1]
- documented AlSi10Mg printing on this exact platform [XM5]
- the XMini module targets exactly this use

**Risks:** XMini minimum charge and dimensions are unpublished; no documented preheat or API.

| Item | Low | High |
|---|---|---|
| XM200G base [XM3] | $90k | $90k |
| 400 W + Reactive + XMini + glovebox options [I] | $30k | $60k |
| Install/training (if not included) [I] | $0 | $10k |
| Inert ultrasonic sieve station [I] | $20k | $40k |
| ATEX wet separator / explosion-proof vac, filter-passivation supplies [I] | $8k | $15k |
| Argon supply (manifold, regulators, room O₂ alarm) + year-1 gas [I] | $8k | $15k |
| Build plates, depowdering/inert transfer, Class D extinguisher, powder storage [I] | $5k | $12k |
| Spares year 1 (filters, windows, recoater blades) + reference AlSi10Mg (10 kg) [I] | $5k | $10k |
| **All-in estimate** | **≈$170k** | **≈$250k** |

### 2. AO Metal A30-300, conditional
**Recommended configuration:** 300 W, ask for the 55 µm spot, argon, plus the explosion-proof wet vac and sieve that are required anyway [AO2].

**Why second:**
- best powder economy of anything found (25-156 g of Al per build [AO2]), which fits rePOWDER batches exactly
- cheapest by far, runs on 120 V
- zone-by-zone open parameters [AO1]
- [I] 300 W in a 75 µm spot is ~6.8 MW/cm². That is more intense than the 200 W / ~150 µm (~1.1 MW/cm²) setups that reached ~99 % in AlSi10Mg [PH2]. Laser power is not the blocker; atmosphere and powder quality are.

**Make purchase conditional on:**
- (a) an acceptance print of *your* rePOWDER Al powder reaching ≥99 % density, with a logged O₂ trace (target ≤500 ppm, ideally ≤100 ppm)
- (b) a written country-of-origin and component-sourcing declaration your procurement office accepts [AO4]
- (c) access to the build-file format so parameter matrices can be generated by script

**Gaps:** no plate heating (a limit for crack-prone alloys), no API, no published Al data.

| Item | Low | High |
|---|---|---|
| A30-300 (list $64k) [AO2] | $64k | $64k |
| 55 µm spot option (price unknown) [I] | $0 | $5k |
| Install + operator training | included [AO2] | included |
| Dedicated 120 V / 50 A circuit [I] | $2k | $6k |
| Explosion-proof wet vac (required) [AO2][I] | $5k | $12k |
| Sieving machine with inert handling (required) [AO2][I] | $5k | $20k |
| Argon supply + room O₂ alarm + year-1 gas [I] | $5k | $10k |
| External O₂ analyzer for logging, if not built in [I] | $2k | $6k |
| Spares, filters, plates, reference powder (AO AlSi10Mg $380/10 kg [AO3]) [I] | $3k | $7k |
| **All-in estimate** | **≈$90k** | **≈$130k** |

### 3. One Click Metal MPRINT + Lab module
**Recommended configuration:** MPRINT (200 W, 70 µm) with **Lab module 78×53×90 mm, 200 °C** and Heating module, an MPURE (or MPURElite) inert sieving unit, argon, and AlSi10Mg + 6061-RAM2 parameter sets.

**Why third:**
- the only budget-class option with a **documented heated small-build module** [OC2]
- vendor Al parameter sets, including a crack-resistant 6061 [OC4]

**Risks:**
- 200 W limits build rate for high-conductivity lean alloys [I]
- parameter openness and scripting are unverified
- US support only through a reseller
- the US price is ambiguous [OC5]

| Item | Low | High |
|---|---|---|
| MPRINT (€89k EU; "$149k US" as printed) [OC5] | $105k | $150k |
| Lab + Heating modules (unpriced) [I] | $10k | $25k |
| MPURE / MPURElite sieving (MPUREpro is $39k [OC5]) [I] | $20k | $39k |
| Install/training, freight [I] | $5k | $15k |
| ATEX wet separator, argon setup + year-1 gas, O₂ alarm [I] | $14k | $27k |
| Parameter licences, cartridges, plates, spares [I] | $5k | $15k |
| **All-in estimate** | **≈$180k** | **≈$270k** |

**Alternatives that did not make the top 3:**
- **TruPrint 1000 / xBUILD 1000** with Ø50 mm reduction, 100 ppm O₂ option and Al option: best-documented compact industrial Al package. [I] All-in ≈ $250-330k, but only 200 W per laser and the vendor is in transition [TR1][TR3-TR6].
- **Aconity MINI:** best technical fit (API, preheat, single-mode 400 W+) but no public price and 1155 kg [AC2][AC5].
- **Cheapest interim step:** ask Aconity/Utah about a **Ø55 mm reduced platform + powder feeder for the existing MIDI** [AC7].
- **Sharebot MetalONE:** the most scriptable cheap machine, but no US support and no Al data [SB1].

---

## 4. Physics: why Al is hard in LPBF and what is needed

- **Reflectivity and energy coupling.**
  - Al alloys absorb **<10 % of 1064 nm** light [PH7].
  - Powder-bed absorptivity is higher than for bulk metal and varies strongly with conditions [PH6].
  - Alsaddah et al. base their case for 450-808 nm diode lasers on higher absorptivity at shorter wavelengths [PH7]. For Al the 515 nm gain is modest compared with Cu or Au [I]. TRUMPF positions its green TruPrint 1000 for Cu and precious metals [TR2], while saying its larger TruPrint 5000 Green is "also suitable for aluminum" [TR9 V].
  - Al's high thermal conductivity spreads heat quickly. Early work could only make reasonable Al parts with **≥150 W** and slow scanning [PH1].
- **Oxide film.** Louvis et al. found **oxidation is the main obstacle**:
  - thin Al₂O₃ films form on solid and molten material
  - the top oxide vaporizes under the beam
  - Marangoni stirring breaks the oxide at the melt-pool base
  - **pores form where oxide films meet between hatches**
  - so dense parts need methods that disrupt or avoid these films [PH1]
- **Atmosphere.**
  - Lower chamber O₂ (100 ppm vs 1000 ppm) improved elongation, with only a small effect on strength [PH11].
  - O₂ contamination (30 ppm vs 500 ppm vs uncontrolled) penalized ductility in Al alloys [PH12].
  - Argon is the norm for Al. Practical target for alloy development [I]: **≤500 ppm, ideally ≤100 ppm, logged per layer**.
  - Only TRUMPF (≤100 ppm option) [TR1] and the Prima family (<100 ppm monitoring) [PR1] publish such numbers among compact machines.
- **Hot cracking.**
  - High-strength 6xxx/7xxx alloys crack in LPBF because of columnar solidification. Zr-based nucleants assembled onto 7075/6061 powders suppress it [PH5].
  - Eutectic-forming Ce additions (Al-Cu-Ce(-Zr)) give >99.5 % density and a *predicted* hot-tearing resistance better than AlSi10Mg [PH10]. This is relevant to your Al-Ce and Zr/Sc/Er palette.
  - Plate preheat (100-200 °C+) lowers residual stress and cracking tendency [I]. It can also start Al₃(Sc,Zr) precipitation in situ, so treat preheat as a BO variable.
- **Volatile loss of Mg and Zn.**
  - SLM of AA7075 lost Zn and Mg (not Cu/Cr/Fe), which increased track instability, porosity and solidification cracking [PH8].
  - Mg vaporization drives keyhole porosity in Al-Ce-Mg; scan strategy can limit it [PH9].
  - Implication [I]: over-alloy Mg/Zn in the atomizer feedstock and close the loop with post-print chemistry (ICP-OES).
- **Powder.**
  - Al's low density and oxide skin hurt flowability and spreading [I].
  - AMAZEMET's 40 kHz setting gives **D50 45-60 µm** [AM1], coarser than typical 20-63 µm LPBF cuts. Coarse cuts (≈20-125 µm) for Al and Ti are studied in a TUHH dissertation [PH14].
  - Effective layer thickness is about 2× nominal and should exceed D90 [XM5]. Plan on ≥50-60 µm nominal layers or a tighter sieve cut, and on the yield loss that comes with it [I].
  - Ultrasonic powder at D50 49 µm printed to 99.25-99.79 % on a Renishaw RBV (316L) [SW1].
- **Explosibility.** Standard AlSi10Mg and pure Al powders ignited in Hartmann-type tests. Pure Al gave the lowest minimum ignition energy (<10 mJ) and higher peak explosion pressure (≈1.15 MPa vs ≈0.6 MPa) [XM5]. Hence the wet separators, filter passivation, ATEX vacuums and "reactive" kits.
- **Can 100-300 W desktops make >99 % dense Al?**
  - **Yes on ~200 W research machines:**
    - Kempen et al.: Concept Laser M1, 200 W, ~150 µm beam, up to 99 % [PH2]
    - Thijs et al.: >99 % at ≥200 W [PH3]
    - Aboulkhair et al.: 99.8 % after balancing parameters and scan strategy [PH4]
  - An ORNL study found >99 % at 32-54 J/mm³ [PH16]. That is a useful prior window for BO.
  - **Unproven on the new desktop class:** I found **no peer-reviewed Al density data** for the AO A30, FastForm, SnowPod, Scrap 1, Phrozen or 2OneLab. Spot intensities (A30-300 ≈6.8 MW/cm²; XM200G 400 W/50 µm ≈20 MW/cm²) are adequate [I]. Atmosphere control and powder handling are what must be demonstrated.

---

## 5. Questions to ask vendors

1. Residual O₂ achievable with **argon** on this exact model. What sensor type and range? Is O₂ logged per layer and exportable? What is the purge time and argon use per build?
2. **Minimum powder charge** for a 10 mm and a 20 mm-tall build with *Al* on the smallest build option (XMini, Lab module, Ø50, Ø34, Ø55 + feeder). What powder is unrecoverable or overflow per build?
3. Accepted **PSD**: will it run D50 ≈ 45-60 µm, D90 ≈ 90 µm ultrasonic powder? What are the minimum layer thickness and recoater type for coarse Al?
4. **Acceptance test:** will you print our rePOWDER Al powder (or AlSi10Mg we supply) and report Archimedes/CT density, O₂ trace and parameters before PO?
5. **Reactive-powder rules:** filter type, wet separator or passivation procedure, ATEX zoning, insurer or fire-marshal documents. Is Al restricted on this model or does it need a kit?
6. **Plate heating:** maximum °C on the small-build option; heating rate; uniformity.
7. **Parameter control granularity:** per part? per region? contour/hatch/up-skin? per layer? Can it change mid-build?
8. **Scriptability:** documented build-file format (CLI/ILT/G-code/JSON), command-line slicer, or API (Python/REST) to queue jobs and read sensor data. Licence costs?
9. **In-situ monitoring:** layer camera, melt-pool camera or photodiode, pyrometer. Raw data export format and rate.
10. Published or customer **Al results on this exact model** (papers, density, tensile).
11. **Electrical:** voltage, phase and amperage (AO: is a dedicated 120 V / 50 A circuit really required?); compressed air; chiller; heat load; exhaust.
12. **Footprint and weight**: confirm the A30's weight (≈100 kg per the datasheet); door-width and floor-loading needs.
13. **Country of origin** of the machine and of the laser, galvo, controller and software. Can you provide a certificate of origin and a Buy-American/NDAA-type declaration for federal funds?
14. **US service:** nearest field engineer, response time, spares stock location, remote diagnostics, warranty scope and length, cost of year-2 service.
15. **Training and installation** included? Lead time? Edu discount? Payment milestones?
16. Consumables pricing: filters, protective glass, recoater blades, build plates, inert gas use per hour.
17. ATLIX and Open Additive specifically: product roadmap and support commitment after the ownership or website changes.
18. Aconity: can the Ø55 mm reduced platform + powder feeder be retrofitted to the Utah MIDI or a MINI, and at what price?

---

## Sources

**AO Metal / Additive Plus**
- [AO1] https://aometal.com/product/a30-ao-metal-3d-printer/
- [AO2] https://aometal.com/wp-content/uploads/2026/10/AO-Metal-A30-datasheet-2026-v2.pdf
- [AO3] https://aometal.com/
- [AO4] https://3dprint.com/317638/push-button-metal-3d-printing-for-50000/ (2025-04-28)
- [AO5] https://3dadept.com/additive-plus-introduces-a-line-of-compact-metal-3d-printers/
- [AO6] https://www.voxelmatters.com/es/additive-plus-lanza-la-serie-ao-una-linea-de-impresoras-3d-destinada-a-abaratar-la-lpbf/
- [AO7] https://3dprint.com/307205/farsoon-expands-u-s-3d-printing-presence-with-additive-plus-partnership-on-the-west-coast/ (2024-02-16)

**One Click Metal**
- [OC1] https://oneclickmetal.com/technical-specifications
- [OC2] https://oneclickmetal.com/build-modules
- [OC3] https://oneclickmetal.com/aluminum-alsi10mg/
- [OC4] https://oneclickmetal.com/aluminum-a6061/
- [OC5] https://3dprint.com/321763/oneclickmetal-turns-up-the-heat-with-500w-lpbf-machine-for-e120000/ (2025-11-04)
- [OC7] https://www.tctmagazine.com/index-group-acquires-majority-interest-in-one-click-metal/
- [OC8] https://www.mastergraphics.com/one-click-metal
- [OC9] https://filament2print.com/en/metal-dmls/2684-mprint-one-click-metal-lpbf-metal-3d-printer.html

**Xact Metal**
- [XM1] https://cdn.goengineer.com/xact_metal_3d_printer_xm200c_technical_data.pdf
- [XM2] https://cdn.goengineer.com/xact-metal-xm200g-data-sheet-goengineer.pdf
- [XM3] https://www.tctmagazine.com/xact-metal-launches-xm200g-metal-3d-printer-drops-price-of-x/
- [XM4] https://www.dynamism.com/3d-printers/industrial-3d-printers/xact-metal-xm200gs.html
- [XM5] Depboylu et al., SFF 2024: https://utw10945.utweb.utexas.edu/sites/default/files/2024/58%20Towards%20Affordable%20Aluminum%20Additive%20Manufactur.pdf
- [XM6] https://www.tctmagazine.com/xact-metal-xm200g-metal-3d-printing-affordable/
- [XM8] https://additivemanufacturing.media/products/xact-metal-introduces-xm200c-metal-3d-printer
- [XM9] https://www.tctmagazine.com/xact-metal-achieves-record-machine-orders-in-q2-q3-2026/

**Sisma**
- [SI1] https://www.sisma.com/prodotto/mysint-100/
- [SI2] https://www.epfl.ch/research/domains/m2c/?p=527
- [SI3] https://www.voxelmatters.com/trumpf-acquires-sismas-additive-manufacturing-business/

**TRUMPF / ATLIX**
- [TR1] TruPrint 1000 flyer (11/2022): https://headland.au/static/d87e49df79ca2401f7a6403c8d0f506c/TRUMPF-TruPrint1000-flyer-EN-1-1.pdf
- [TR2] TRUMPF AM systems overview (08/2021): https://headland.au/static/b5f880aa094eddc2ad52d1dddd1f01af/TRUMPF-Advanced-Manufacturing-systems-flyer.pdf
- [TR3] https://www.metal-am.com/trumpf-to-sell-additive-manufacturing-business-to-lenbach-equity-opportunities/
- [TR4] https://www.metal-am.com/trumpf-additive-manufacturing-rebrands-as-atlix-ahead-of-formnext-2025/
- [TR5] https://www.tctmagazine.com/atlix-announces-rebranded-additive-manufacturing-portfolio/ (2026-09-02)
- [TR6] https://www.aniwaa.com/product/3d-printers/trumpf-truprint-1000-lmf/
- [TR7] https://www.machineseeker.ie/trumpf-truprint+1000/i-22483182
- [TR8] https://www.roechling.com/group/additive-manufacturing/technologies/selective-laser-melting
- [TR9] https://trumpf.com/en_US/products/machines-systems/additive-production-systems/truprint-5000-green-edition

**Aconity / AMAZEMET**
- [AC1] https://www.royce.ac.uk/equipment-and-facilities/powder-laser-bed-melting-2/
- [AC2] https://www.aniwaa.com/product/3d-printers/aconity3d-aconitymini/
- [AC3] https://www.3dnatives.com/3d-materials/en/3d-printers/aconitymini/
- [AC4] https://am.nus.edu.sg/equipment/metal-printer-aconity-mini
- [AC5] https://aconity-control.readthedocs.io/en/latest/overview.html
- [AC6] https://aerospace.research.utah.edu/?p=67
- [AC7] https://www.amazemet.com/aconity-midi-lpbf-system-in-amazemets-rd-facility (2023)
- [AC8] https://laserfocusworld.com/industrial-laser-solutions/article/14220744/additive-manufacturing-company-aconity3d-establishes-us-operations
- [AM1] https://www.amazemet.com/atomization-methods-in-metal-powder-production-essential-guide
- [AM4] https://formnext.amazemet.com/

**ORLAS CREATOR**
- [OR1] https://www.fabricatingandmetalworking.com/2017/02/affordable-3d-metal-printing-small-shops/
- [OR2] https://content.coherent.com/legacy-assets/pdf/CREATOR_EN_web.pdf (host no longer resolves)
- [OR3] https://www.aniwaa.com/product/3d-printers/coherent-creator/
- [OR4] https://3dprint.com/278304/maker-of-creator-metal-3d-printer-to-be-bought-by-lumentum-for-5-7b/
- [OR5] https://www.engineering.com/?p=18571

**Farsoon**
- [FA1] https://www.aniwaa.com/product/3d-printers/farsoon-fs121m/
- [FA2] https://www.findlight.net/uploads/products/datasheet/fs121m-accessible-compact-robust-industrial-metal-3d-printer_1675026433.pdf
- [FA3] https://top3dshop.com/product/farsoon-fs121m-3d-printer

**EOS, 3D Systems, DMG MORI**
- [EO1] https://pdf.medicalexpo.com/pdf/eos-gmbh-electro-optical-systems/system-data-sheet-eos-m-100/72628-217433.html
- [EO2] https://www.metal-am.com/eos-introduces-m-100-system-eostate-meltpool-monitoring-and-new-stainless-steel-powder/
- [EO3] https://laser-spec-hub.vercel.app/equipment/metal-3d-printing/eos-m-100-0-2kw
- [DM1] https://3dsystems.com/3d-printers/dmp-flex-100
- [DM3] https://test-it.3dsystems.com/sites/default/files/2023-03/3d-systems-academic-DMP-bundles-brochure-usen-2023-03-07-a-web_0.pdf
- [LT1] https://us.dmgmori.com/products/machines/additive-manufacturing/powder-bed/lasertec-12-slm
- [LT2] https://laser-spec-hub.vercel.app/equipment/metal-3d-printing/dmg-mori-lasertec-12-slm

**Prima Additive, Sharebot**
- [PR1] https://multistation.com/en/product/prima-additive-print-150-family
- [PR2] https://www.metal-am.com/?p=98543
- [SB1] https://www.multistation.com/voy_content/uploads/sites/4/2023/08/flyer_metalone.pdf
- [SB2] https://www.fabbaloo.com/2020/01/sharebot-entering-the-metal-3d-printing-arena
- [SB3] https://daemon3dprint.com/main/sharebot-metalone.html
- [SB4] https://www.directindustry.com/prod/sharebot-srl/product-173451-2818639.html

**Open Additive**
- [OA1] https://www.aniwaa.com/product/3d-printers/openadditive-panda/
- [OA2] https://www.fabbaloo.com/2020/06/open-additive-opens-up-metal-additive-manufacturing
- [OA3] https://www.metal-am.com/open-additive-awarded-contract-to-develop-multi-laser-am-technology/
- [OA4] https://www.inknowvation.com/sbir/companies/open-additive-llc

**BLT**
- [BL1] https://www.aniwaa.com/product/3d-printers/blt-bright-laser-technologies-blt-a100/
- [BL2] https://www.metal-am.com/blt-launches-high-strength-aluminium-and-titanium-alloys-for-additive-manufacturing/
- [BL3] https://www.goengineer.com/3d-printing/metal/blt

**Small-batch kit evidence**
- [SW1] Palmer et al., SFF 2024 (Swansea; Renishaw AM400 RBV + ultrasonic powder): https://utw10945.utweb.utexas.edu/sites/default/files/2024/60%20Use%20of%20Cored%20Wire%20in%20the%20Optimisation%20of%20New%20Al.pdf

**New entrants**
- [NE1] https://3dprint.com/332624/metal-3d-printers-for-the-desktop-are-finally-starting-to-feel-like-desktop-products/
- [NE2] https://www.3dnatives.com/en/mastrex-affordable-lpbf-systems-19052026/
- [NE3] https://makers101.com/scrap-labs-scrap-1-metal-3d-printer/
- [NE4] https://3dprintingindustry.com/news/metal-base-pre-launches-sub-e10000-lpbf-metal-3d-printer-on-kickstarter-248083/
- [NE5] https://3dprint.com/320049/push-button-metal-fastform-sells-1000-lpbf-machines/
- [NE6] https://www.tctmagazine.com/xact-metal-launches-xm200g-mhd-metal-3d-printer-xm300g-development-continues/

**Physics**
- [PH1] Louvis, Fox, Sutcliffe, J. Mater. Process. Technol. 211 (2011) 275: https://livrepository.liverpool.ac.uk/3173955/1/632653.pdf
- [PH2] Kempen et al., SFF 2011: https://utw10945.utweb.utexas.edu/Manuscripts/2011/2011-37-Kempen.pdf
- [PH3] Thijs et al., Acta Mater. (2013), postprint: https://lirias.kuleuven.be/bitstream/123456789/369343/3/Thijs%20et%20al%202012_fine-structured%20aluminium%20products%20with%20controllable%20texture%20by%20SLM%20of%20AlSi10Mg%20powder_postprint.pdf
- [PH4] Aboulkhair et al., Addit. Manuf. 1-4 (2014) 77: https://eprints.nottingham.ac.uk/33426
- [PH5] Martin et al., Nature 549 (2017) 365: https://doi.org/10.1038/nature23894
- [PH6] Trapp et al., Appl. Mater. Today (2017): https://www.osti.gov/biblio/1392171
- [PH7] Alsaddah et al., Int. J. Adv. Manuf. Technol. (2021): https://eprints.whiterose.ac.uk/171431/
- [PH8] npj Mater. Degrad. (2019), SLM AA7075: https://www.nature.com/articles/s41529-019-0101-6
- [PH9] ORNL, Al-Ce-Mg: https://www.ornl.gov/publication/microstructure-and-properties-additively-manufactured-al-ce-mg-alloys
- [PH10] ORNL, Al-Cu-Ce(-Zr): https://impact.ornl.gov/en/publications/al-cu-ce-zr-alloys-with-an-exceptional-combination-of-additive-pr/
- [PH11] Baroutaji et al. (2023): https://research.aston.ac.uk/files/118457090/Baroutajietal_2023_VoR.pdf
- [PH12] Bauer et al., SFF 2016: https://utw10945.utweb.utexas.edu/sites/default/files/2016/029-Bauer.pdf
- [PH14] TUHH dissertation, coarse PSD: https://tore.tuhh.de/bitstreams/0535e5fa-1fba-4f44-9d65-b1471e1ff2cc/download
- [PH16] ORNL, AlSi10Mg energy window: https://impact.ornl.gov/en/publications/understanding-the-laser-powder-bed-fusion-of-alsi10mg-alloy/
