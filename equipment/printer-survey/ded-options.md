<!-- Public extract of sgbaird/byu-finances proposals/capital-equipment-2026/ded-options.md (2026-11-09), for vertical-cloud-lab/digital-alloy-lab. This survey used public prices only (no vendors contacted, no quotes requested); only this header and the purpose line were changed. -->

# Compact / benchtop DED for copper alloys: evidence-backed comparison

Prepared 2026-11-09 for BYU ME lab CB 154. Web research only. No vendors were contacted and no quotes were requested, so every price below is a public list price, a reseller listing, a trade-press figure or my estimate.

**Evidence labels:** **[V]** vendor or vendor datasheet claim. **[D]** distributor or reseller listing. **[P]** peer-reviewed paper. **[PP]** preprint or conference abstract. **[G]** government report or regulation. **[U]** university facility page. **[N]** trade press. **[I]** my inference, not a sourced fact.

**Scope, per the lead's 2026-11-09 update.** The main Cu thrust is an ONR YIP FY27 proposal on Cu-Ni-Al-Fe-Mn naval alloys:

- Design space: Ni 0-30, Al 0-9.5, Fe 0-4.5 and Mn 0-4 wt%, balance Cu.
- Reference alloys: C71500 (CuNi 70/30), C70600 (CuNi 90/10), and nickel-aluminium bronze (NAB) C95800 / C63000.
- Be-free BeCu replacements (CuNiSi(Cr), CuCrZr, GRCop, Cu-Ni-Sn, pure Cu) are secondary.

The lab already uses two outside machines:

- An InssTek MX-Lab at the University of Utah, which the plan treats as power-capped.
- A FormAlloy X2 at Colorado School of Mines.

Ultrasonic-atomized powder lots are about 0.5 kg each.

---

## 1. Bottom line

1. **Short wavelengths matter for pure Cu, much less for the naval alloys.**
   - CuNi 70/30 conducts about 29-30 W/m·K, CuNi 90/10 about 45-50 and NAB about 36, against about 397 for pure Cu.
   - Infrared (IR) laser DED and arc (WAAM) have both made sound NAB. WAAM has made near-dense CuNi 70/30 and 90/10.
   - Blue or green light is needed for pure Cu, unless you have at least about 2 kW of IR. It helps, but is not required, for CuCrZr and GRCop. Section 2 has the details.
2. **The MX-Lab "power cap" is real but narrower than it sounds.**
   - It is a hard limit for pure Cu, and close to one for CuCrZr and GRCop.
   - For CuNi and NAB, dense bulk deposits at 500 W or less are plausible but not yet published.
   - What does exist at that power: Al-bronze/316L blends at 308-500 W average on an InssTek MX-1000 [PP], an InssTek database Al-bronze at about 98.9% relative density [V], and pulsed Nd:YAG Cu‑38Ni cladding at about 0.4-0.47 kW average with preheat [P].
   - The documented laser windows for sound NAB are 0.6-1.2 kW (wire) up to 9 kW (hot-wire).
3. **Only powder-fed systems can use the atomizer's 0.5 kg lots.** Meltio (all models), Additec and WAAM are wire-only. Commercial ERCuNi and ERCuNiAl wires exist, so these suit fixed-chemistry demonstrators, not composition screening.
4. **Hopper size and minimum fill decide the small-batch fit.**
   - Best small-lot feeders: the InssTek MX-Lab (6 hoppers of 0.4 L, 0.03-2 g/min) and the FormAlloy 16-hopper Alloy Development Feeder.
   - Retrofit option: the Powder Motion Labs X3E (200 mL hopper, 0.01-15 g/min).
   - No vendor publishes a minimum powder charge, so this is the top question to put to vendors.
5. **Recommendation (Section 6).**
   - No. 1: a FormAlloy X-series powder DED with 1-2 kW IR, 4 feeders or the ADF, and an inert glovebox, with the blue head as an option. It is the same family as the Mines X2.
   - No. 2: an InssTek MX-Lab of your own. It is the cheapest and easiest to install, and best for 0.5 kg screening, but has the same power limit as Utah's.
   - No. 3: an Optomec LENS CS 250.
   - A wire machine (a CMT-WAAM cobot or a Meltio M600) complements these for NAB/CuNi demonstrators but cannot use atomizer powder. Mines already has a CMT cobot.
6. **Do not print or atomize real BeCu (C17200, 1.8-2.0% Be) in CB 154.** It would bring in OSHA 29 CFR 1910.1024 (exposure limit 0.2 µg/m³). The CuNi and NAB powders contain Ni, a carcinogen, so they also need enclosed handling and local exhaust (Section 8).

---

## 2. Physics: wavelength, power and conductivity

**Absorptivity of copper**

| Condition | IR (1030-1080 nm) | Green (515 nm) | Blue (450 nm) |
|---|---|---|---|
| Solid Cu, room temperature | under 5% | over 55% | n/a |
| Solid Cu, conduction welding | about 4-5% | about 60% | up to about 80% |
| Molten Cu | about 15% (vs about 5% solid) | n/a | n/a |
| Powder | baseline | n/a | 2.4-3.3 times the IR value, on average |

- Solid Cu, room temperature, IR and green: Fraunhofer ILT [P], https://publica.fraunhofer.de/handle/publica/265766
- Conduction welding, all three wavelengths: Nordet et al., *Opt. Laser Technol.* 147 (2022) 107612 [P], https://sam.ensam.eu/bitstream/10985/23221/3/PIMM_OLT_2021_NORDET.pdf
- Osaka group: under 10% in near-IR against about 60% at 450 nm [P], https://doi.org/10.1117/12.2551900
- Molten Cu at 1070 nm [P]: https://doi.org/10.1007/s40194-020-00849-8
- Powder, 39 powders including Cu and brass: Brandau et al., *Mater. Des.* 2022 [P], https://doi.org/10.1016/j.matdes.2022.110591
- Once a keyhole forms, near-IR absorptivity of Cu alloys can reach 0.91 (NIST, powder bed) [P], https://www.nist.gov/publications/absorptivity-scaling-behaviour-during-laser-powder-bed-fusion-copper-alloys. The hard part is getting there.

**Thermal conductivity and what each alloy needs**

| Alloy | k at about 20 °C (W/m·K) | What has worked in DED | Is blue or green needed? |
|---|---|---|---|
| Pure Cu | 396-397 | IR: about 99.9% dense at **2 kW** fibre (RRCAT) [P]. Blue: **99.6%** at 650 W on blown powder (Liu et al., UCSD, *J. Manuf. Process.* 85 (2023) 314) [P]; 0.1% porosity at 180 W with a 3×100 W multi-beam head (Yamaguchi 2024) [P]. No dense IR DED at 500 W or less found. | **Yes**, unless IR is at least about 2 kW [I] |
| GRCop-42 | 344 | NASA blown-powder DED: under 0.1% porosity; power not reported [G]. WSU: workable at 500-950 W on a 1 kW fibre, but a narrow window and no density measured [PP]. NASA RAMPT built large DED GRCop-42 nozzles [G]. | No at 1-2 kW IR; blue widens the window [I] |
| GRCop-84 | 280 | Deposited on LENS (WSU, onto Inconel 718); needed high energy [P] | No at 1-2 kW IR [I] |
| CuCrZr (C18150) | about 324 (80% IACS) | No IR blown-powder DED paper with power and density found. Meltio blue wire at 1 kW: thin single-pass walls only, technology readiness 3-4 [V]. | Probably not at 1-2 kW IR, but unproven [I] |
| CuNi 90/10 (C70600) | about 45-50 | CMT-WAAM sound, with small microporosity [P]. **No laser DED record found.** | No [I] |
| NAB (C95800) | about 36 (as-built laser NAB: 34.1) | Laser powder DED with over 99.8% density, including **ultrasonic-atomized feedstock** (Fraunhofer IPK; the 2023 paper names AMAZEMET rePOWDER) [P]/[PP]. Laser wire: 0.6-1.2 kW [PP] and 9 kW IR hot-wire [P]. WAAM fully dense [P]. | **No** |
| CuNi 70/30 (C71500) | about 29-30 | WAAM dense [P]. Blue wire DED at 0.7-1 kW, with weak fusion between layers at low energy density [PP]. Powder DED from blends works, but elemental Ni causes porosity [P]. Pulsed IR Cu‑38Ni cladding at about 0.4-0.47 kW average with preheat [P]. | **No** |

Sources for the conductivity values:

- Cu, GRCop-42, GRCop-84: NASA [G], https://ntrs.nasa.gov/api/citations/20050192166/downloads/20050192166.pdf
- C18150: CDA [V], https://alloys.copper.org/alloy/C18150
- C71500: Matthey [V], https://www.matthey.ch/fileadmin/user_upload/downloads/fichetechnique/EN/CuNi30Mn1Fe_v25E.pdf
- C70600, cast CC380H: [secondary], https://www.makeitfrom.com/material-properties/EN-CC380H-CuNi10Fe1Mn1-C-Copper-Nickel
- C95800: [secondary, CDA-derived], https://www.concast.com/c95800.php
- As-built NAB: Hatala et al. 2024 [P], https://doi.org/10.3390/met14101143

Sources for the deposition results:

- RRCAT pure Cu at 2 kW: https://research.tees.ac.uk/en/publications/laser-directed-energy-deposition-based-additive-manufacturing-of--2/
- Liu et al. 2023: https://eld.bl.uk/catalog/100184688149_0x000001
- Yamaguchi 2024: https://doi.org/10.1007/s00170-024-14789-w
- NASA GRCop-42: https://ntrs.nasa.gov/citations/20205008272
- WSU GRCop-42: https://arxiv.org/abs/2601.17587
- NASA RAMPT: https://www.nasa.gov/rapid-analysis-and-manufacturing-propulsion-technology
- Meltio CuCrZr v9 datasheet (indexed in July 2026, returns 404 now): https://meltio3d.com/wp-content/uploads/2026/07/Meltio_Copper_CuCrZr_datasheet_v9_06-07-2026.pdf

**What this means for the hardware [I].**

- CuNi and NAB conduct heat 8-14 times worse than pure Cu. They also have higher IR absorptivity, since resistivity drives free-electron absorption.
- **IR is the right tool for them, and 1-2 kW gives comfortable margin.** At 500 W you will probably need substrate preheat, small beads and parameter development.
- For **pure Cu**, a compact system needs blue (at least about 0.5-1 kW) or IR of 2 kW or more.
- **GRCop and CuCrZr** sit between these: about 1-2 kW IR, with blue as a widener.
- The MX-Lab's 400 µm spot at 500 W gives about 0.4 MW/cm², the same intensity as 2 kW into 0.8 mm. But total power, not intensity, is what overcomes heat sinking in high-conductivity Cu. That is why the power cap bites for pure Cu and CuCrZr, not for CuNi and NAB.

---

## 3. CuNi and NAB deposition evidence by process

**Answer to the lead's question: has dense CuNi and NAB been deposited, and by which route?**

- **NAB**
  - IR laser wire DED: yes. Penn State ARL's 9 kW IR hot-wire gave no lack of fusion and minimal porosity [P].
  - IR laser powder DED: yes. InssTek DMT (fibre) Al-bronze reached 98.9% density [V], and the InssTek MX-1000 deposited Al-bronze blends at 0.3-0.5 kW average [PP].
  - Fraunhofer IPK reached over 99.8% from ultrasonic-atomized feedstock (rePOWDER in the 2023 paper). I did not retrieve its laser type or power [PP].
  - WAAM: fully dense [P].
- **CuNi 70/30**
  - WAAM: dense [P].
  - IR laser: only as powder blends, where elemental Ni caused porosity [P], and as pulsed Cu‑38Ni cladding, which was dense with preheat [P].
  - Laser wire: only with blue at 0.7-1 kW, which showed weak fusion between layers [PP].
  - **No measured bulk density from laser DED.**
- **CuNi 90/10**
  - WAAM: near-dense [P].
  - **No laser DED of any kind found, IR or blue.**

| Alloy | Laser powder DED | Laser wire DED | WAAM (CMT/GMAW) | IR at 500 W or less |
|---|---|---|---|---|
| **C71500 70/30** | Blended Cu + Ni-Si-B powder works; **elemental Ni gives gas and shrinkage porosity** (Karnati et al., IJAMT 103 (2019) 239) [P]. Graded 70/30 to Ni (Karnati, *Metals* 9 (2019) 287) [P]. Cu65Ni35 single tracks only (Williams 2025) [P]. No dense bulk build with measured density found. | Blue 700-1000 W: hardness 107-121 HV; low energy density gave poor fusion between layers (Viamontes et al., TMS 2026) [PP] | CMT, Lincoln Techalloy 413 wire: no porosity or cracks by optical microscopy; corrosion better than wrought (Song et al., *Materials* 17 (2024) 876) [P] | Pulsed Nd:YAG Cu‑38Ni cladding on a NAB propeller, about 0.4-0.47 kW average with 165-175 °C preheat: dense, crack-free (Iatan et al., *Materials* 18 (2025) 4301) [P] |
| **C70600 90/10** | **None found** | **None found** | CMT on Gefertec: small microporosity; UTS 495-520 MPa, YS 342-358 MPa, 17-18% elongation, 37-52% stronger than cast (Maleta et al., *Materials* 17 (2024) 50) [P] | None found |
| **NAB C95800 / C63000** | Fraunhofer IPK: propeller-chip powder made by **induction re-melting plus ultrasonic atomization** (the 2023 paper names AMAZEMET rePOWDER), then laser powder DED. Over 99.8% density, about 260 HV1, YS about 650 MPa, UTS about 850 MPa, about 9% elongation (euspen 2025 abstract) [PP]. A related *Addit. Manuf.* 2025 paper: Z-direction UTS 775 MPa, YS 455 MPa, 12.6% elongation [P]. InssTek DMT Al-bronze C95300: 98.9% relative density, UTS 628/598 MPa (XY/Z) [V]. | Penn State ARL, 9 kW IR hot-wire, MIL-CuNiAl wire: no lack of fusion, minimal porosity, YS 410 MPa (Hatala et al., *Metals* 14 (2024) 1143) [P]. Oregon State: 600-1200 W, strength and ductility above cast [PP]. Meltio blue 1 kW ERCuNiAl [V]. | Fully dense at up to 5 kg/h (Ding et al., *Materials* 9 (2016) 652) [P]. YS about 88 MPa above cast (Dharmendra et al., *Addit. Manuf.* 30 (2019) 100872) [P]. NSWC Carderock arc-DED NAB: over 17% higher YS and over 90% higher ductility than cast (NSWCCD-61-TR-2021/9) [G]. NSRP robotic arc-DED NAB qualification, 2023-26 [G]. | InssTek MX-1000 (1 kW fibre): Al-bronze (C61800-type) + 316L blends at **308 W average / 450 W peak** and **500 W average / 750 W peak**. Pure Sn-bronze layers had poor manufacturability (Makarenko et al., arXiv 2110.00103) [PP]. |

URLs for the table:

- Karnati 2019, IJAMT: https://doi.org/10.1007/s00170-019-03553-0
- Karnati 2019, *Metals*: https://mdpi.com/2075-4701/9/3/287
- Williams 2025: https://mdpi.com/2504-4494/9/6/170
- Viamontes et al., TMS 2026: https://www.programmaster.org/PM/PM.nsf/ApprovedAbstracts/A484837CF70F5FAC85258CB4007428A7
- Song et al. 2024: https://doi.org/10.3390/ma17040876
- Iatan et al. 2025: https://doi.org/10.3390/ma18184301
- Maleta et al. 2024: https://doi.org/10.3390/ma17010050
- Müller et al., euspen 2025: https://www.euspen.eu/knowledge-base/AM2525108.pdf
- Müller et al., IOP Conf. Ser. 2023 (rePOWDER): https://doi.org/10.1088/1757-899X/1296/1/012036
- AMAZEMET summary of the rePOWDER work: https://www.amazemet.com/using-ultrasonic-atomization-to-recycle-aluminium-bronze-chips-for-additive-laser-directed-energy-deposition
- *Addit. Manuf.* 2025: https://doi.org/10.1016/j.addma.2025.104804. The figures are from a news summary I could see: https://www.alcircle.com/news/study-highlights-eco-friendly-ways-to-use-nickel-aluminium-bronze-chip-powders-for-directed-energy-deposition-114034
- InssTek materials database: https://www.phillipscorp.com/wp-content/uploads/2026/04/InssTek-Materials-Database.pdf
- Hatala et al. 2024: https://doi.org/10.3390/met14101143
- Oregon State, TMS 2025: https://programmaster.org/PM/PM.nsf/ApprovedAbstracts/753C5FF848FE53C885258B5B001B4244
- Ding et al. 2016: https://doi.org/10.3390/ma9080652
- Dharmendra et al. 2019: https://doi.org/10.1016/j.addma.2019.100872
- NSWCCD-61-TR-2021/9: https://apps.dtic.mil/sti/trecms/pdf/AD1147115.pdf
- NSRP NAB project: https://www.nsrp.org/?p=2416
- Makarenko et al.: https://arxiv.org/abs/2110.00103

**What this means for the proposal.**

- Laser DED of C70600 is a genuine gap. Low-power, small-batch laser DED of the whole Cu-Ni-Al-Fe-Mn space is also undocumented.
- The Missouri S&T result is directly relevant to in-situ alloying with an MX-Lab-type feeder: **avoid elemental Ni in blends**, or deoxidize. Pre-alloyed atomizer lots, or Cu‑Ni master alloys, are safer [P → I].

---

## 4. Comparison table, price first

| System (vendor, country) | Price (USD; source, year) | Laser: λ / max power | Feedstock | Envelope; atmosphere | Cu-alloy evidence on this platform | Fit for 0.5 kg powder lots | Facility | US support |
|---|---|---|---|---|---|---|---|---|
| **InssTek MX-Lab** (Korea), the Utah baseline | **Not published; quote only** [D]. Budget placeholder $250-400k [I] | Yb fibre, **500 W max** (2026 brochure; the 2020 Rev.3 sheet says 300 W) [V]. 400 µm spot. DMT closed-loop melt-pool height. | Powder. CVM vibratory feeder, up to **6 × 0.4 L** hoppers, 0.03-2 g/min (Ti-6Al-4V) [V] | 150 × 150 × 150 mm, 3-axis. Optional Ar ≥ 99.999%, **O₂ ≤ 50 ppm** [V] | Al-bronze in vendor gradient and composite demos; DB Al-bronze 98.9% dense (machine not stated) [V]. Sibling MX-1000 ran Al-bronze/316L at 308-500 W average [PP]. No CuNi, CuCrZr, GRCop or pure Cu. | **Best.** Six-powder in-situ alloying; a 0.4 L hopper holds about 1.7 kg of NAB powder [I] | 220 V single-phase, 15(20) A. 27 × 30 × 33 in, 785 lb. "EN 60825-1" listed; laser class not stated, so confirm Class 1 [V] | Phillips (since July 2025); Additive Plus |
| **InssTek MX-Fab 1/3** | Quote only | Yb fibre, 1 kW or 2 kW [V]. 0.8-2.4 mm spot. | Powder, 6 × 1 L hoppers [V] | 500 × 600 × 386 mm, 5-axis. O₂ ≤ 50 ppm [V] | Same InssTek database | Good | **6,600 lb**, 61 × 82 × 92 in [V]. Not compact. | Phillips |
| **Optomec LENS CS 250** (USA) | "Base under $300k" (2020) [N]; about $400k (Aniwaa) [N] | Fibre. Power not published; the LDH 3.X head covers 0.5-3 kW [N]. | Powder, up to 4 feeders [N] | 250³ mm, 3- or 5-axis. Optional inert processing aimed at Cu and Ti [N] | Pure-Cu LENS process announced 2019, no data published [N/V]. Nebraska lists GRCop-84 and Cu-Ni as R&D materials on LENS MTS [U]. | Good: feeders "flow small quantities… very precisely" [V]. Minimum fill not published. | "Fits through a doorway" [N] | Albuquerque |
| **Optomec LENS 450 / CS 150** (legacy compact) | Not published | IPG fibre, **400 W** [V] | Powder, 1-4 feeders [V] | 100³ mm (150³ for the 450 XL / CS 150). O₂ under 10 ppm [V] | None found | Good | 450: 1 × 1 × 1.5 m. CS 150: 600 kg, CDRH Class 1 airtight [V] | USA. Datasheets are 2016/2018; current sale status unclear. |
| **FormAlloy X-series / X2** (USA) | **From $200k in 2019** (500 W, 1 feeder, 3-axis) [N]. Configured price not published. | IR fibre (1 kW at Mines and JHU; 1070 nm at JHU) or a blue option. AX head rated to 8 kW [N/U]. | Powder: up to 4 feeders or the **16-hopper ADF** [N] | 250 × 250 × 300 mm (Mines/JHU). Glovebox option. O₂ and H₂O under 100 ppm (JHU) [U] | Blue FormAlloy: **pure Cu 99.6%** (UCSD) [P; machine named in a secondary source]. GRCop-42 deposited under a NASA JPL STTR [G]. No CuNi or NAB found. | Very good, if the ADF is configured. Minimum fill not published. | Not published. Chiller and 3-phase likely [I]. | San Diego |
| **FormAlloy L-series** (blue) | Not published | Nuburu blue, power not stated [N] | Powder | Inert chamber [N] | As above | n/a | n/a | Blue-source supply risk (see Nuburu row) |
| **Meltio M450** (Spain) | **$154,269 or $203,210** (MatterHackers; "currently unavailable") [D] | 6 × 200 W diodes, 976 nm, **1.2 kW** [D] | **Wire** 0.8-1.2 mm | 145 × 168 × 390 mm. Sealed, controlled atmosphere [D] | Cu and Al "under development" [D] | **None** (wire only) | 560 × 600 × 1414 mm, 250 kg. 3-phase 208/230 or 400 V, 2-5 kW peak. Chiller included [D]. | Possibly being retired [D] |
| **Meltio M600** | **$240,125 or $296,230** (MatterHackers) [D] | 9 diodes, **450 nm, 1.0 kW** [V] | Wire 0.8-1.2 mm, up to 4 wires [V] | 300 × 400 × 600 mm. Full inert chamber, **50 ppm O₂** after about 8 m³ Ar (about 2 h, €30-40) [V] | **ERCuNiAl validated:** about 565 MPa UTS, 255 MPa YS, 32% elongation as-printed [V]. CuCrZr thin walls only, readiness 3-4 [V]. Pure Cu in development [V]. | **None** (wire only) | 1050 × 1150 × 1950 mm, 800-1000 kg. 3-phase 380-415 V or 200-240 V; 4-6 kW average, 10.6 kW peak. Chiller included. Laser-safe enclosure [V]. | Meltio Inc. and resellers |
| **Meltio Engine Blue** (robot/CNC kit) | Quote only | 9 diodes, 450 nm, 1.0 or 1.4 kW [N] | Wire | Host-dependent; local shielding [I] | As M600 | None | Needs a host robot or CNC plus a laser enclosure | As above |
| **AddUp Modulo 250 → BeAM 400/800** (France) | Quote only | Yb fibre: 500 W (10Vx nozzle) or 2 kW (24Vx) [V] | Powder: 2 vibratory feeders × **2.5 L** (about 13 kg of steel) [V] | Modulo 250: 400 × 250 × 300 mm (2018) [N]. Modulo 400: 650 × 400 × 400 mm, inert [V]. | "CuAl" is in AddUp's tested-materials list [V] | Poor: hoppers far too big | Modulo 400: **6,600 kg**, 2.8 m tall [V] | Cincinnati centre. Modulo 250 no longer listed. |
| **Additec µPrinter / AMDROID** | µPrinter about $90k (2019), **discontinued** [N]. AMDROID quote only. | µPrinter: 3 × 200 W diodes. AMDROID X: 6-12 kW [N] | Wire (powder optional on µPrinter) | 160 × 120 × 450 mm, Ar chamber (µPrinter) [N] | None found | Poor | n/a | Spain/US |
| **Nikon Lasermeister LM300A** (2024 entrant) | 100A launched at ¥30M (2019) [V]. LM300A quote only. | IR | Powder | 297 × 210 × 400 mm [N] | No Cu in the material list [N] | n/a | 1,350 kg [N] | Nikon AM |
| **Laserline LDMblue** + LMD head | Quote only | **445 nm, 1-3 kW CW** (2019-2022) [N] | Powder via a head | Integrator-built | 1 kW blue cladding of pure Cu powder (Britten & Ocylok, SPIE 2019) [P] | Depends on head and feeder | Class 4 source; needs motion, enclosure and chiller | Laserline Inc. |
| **Nuburu** blue lasers | n/a | 450 nm | n/a | n/a | Supplied FormAlloy's L-series | n/a | n/a | **Distressed in 2025-26** (see note) [N] |
| **TRUMPF TruDisk green** | Quote only | 515 nm, 200 W-3 kW [V] | Source only | n/a | Green laser deposition of Cu (Fraunhofer IWS 2020) [P]. EWI green DED project, no results yet [N]. | n/a | Class 4 source | TRUMPF Inc. |
| **HMT AMBIT** heads | Quote only | IR heads on a CNC tool-changer | Powder or wire | Host CNC | None found | Depends | Needs a CNC host | n/a |
| **DMG MORI LASERTEC 65 DED hybrid**, 2nd gen (2026), reference only | Quote only; [I] seven-figure class | **3 kW** IR diode standard; **optional 2 kW blue, 450 nm** [V/N] | Powder: pots of 0.5 / 2.3 / 5 L [V] | 735 × 650 × 560 mm travels [V] | Blue option marketed for Cu [V] | S pot (0.5 L) OK | Full machine tool | DMG MORI USA |
| **Compact WAAM** (CMT cobot; MetalWorm MW500 LAB; WAAM3D MiniWAAM PTA) | Not published; [I] about $0.1-0.25M for a CMT cobot cell | Arc | Wire 1.0-1.2 mm | Local shielding | **Dense CuNi 70/30, CuNi 90/10 and NAB are well documented** (Section 3) [P]. MW500 LAB lists "aluminium nickel bronze" [N]. MiniWAAM showed a 316L/NAB part [N]. | None (wire) | 3-phase welding supply, fume extraction, weld curtains | **Mines already has a UR10e + Fronius TPS 400i CMT cobot** [U] |

---

## 5. Notes per system

**InssTek MX-Lab (Utah's machine; the baseline)**

- **Specs.** The 2026 Phillips/InssTek brochure lists a Yb fibre laser at max 500 W with a 400 µm spot, 150 mm cube travel, and up to six 0.4 L hoppers. It runs on Ar ≥ 99.999% at O₂ ≤ 50 ppm, measures 27 × 30 × 33 in and weighs 785 lb ([brochure](https://www.phillipscorp.com/wp-content/uploads/2026/04/HYB-InssTek-Brochure_2026Apr_compressed.pdf)) [V].
- **Older spec sheet.** The 2020 Rev.3 sheet gives max **300 W**, a build rate of 1.5 ± 0.2 cm³/h, 220 V single-phase at 15(20) A, and EN 60825-1 laser safety ([datasheet](https://dipaul.ru/upload/iblock/c19/74xw2oocyxtfsb060f664hnz00l0ya8i.pdf)) [V]. **Ask Utah whether its unit is the 300 W or the 500 W version.** Its lab page does not say ([Utah](https://3dprinting.metallurgy.utah.edu/direct_energy_deposition/index.php)) [U].
- **Monitoring and software.** Two cameras track melt-pool height in real time (DMT). The machine also has auto-Z, auto powder calibration, logging of laser power, melt-pool images, XYZ and feed, and "Material Designer" composition software ([MX-Lab report](https://www.phillipscorp.com/wp-content/uploads/2026/04/Material-Research-Report-MX-Lab.pdf); [3DNatives 2024](https://www.3dnatives.com/en/insstek-alloy-research-mx-lab-ded-3d-printer-051120244/)) [V/N].
- **Cu evidence is vendor-only so far.**
  - Cu-Sn and Al-bronze are on the applicable-materials list.
  - The MX-Lab report shows an SS316L→Al-bronze graded sample and an Al-bronze + CoCrW composite.
  - The materials database reports DMT Al-bronze C95300 at 7.448 vs 7.530 g/cm³ (98.9%), UTS 628/598 MPa, YS 291/295 MPa and 26/21% elongation (XY/Z), from 48-115 µm powder (mean 84 µm) ([database](https://www.phillipscorp.com/wp-content/uploads/2026/04/InssTek-Materials-Database.pdf)) [V].
  - No CuNi data was found.
- **Price and support.** No public price; Phillips (US distributor since July 2025, [DailyCADCAM](https://dailycadcam.com/phillips-additive-introduces-inssteks-mx-lab-mx-fab-ded-metal-3d-printers-in-us/)) and Additive Plus quote on request. Additive Plus says installation, training and initial DMT parameter support are included ([Phillips](https://shop.phillipscorp.com/products/insstek-mx-lab); [Additive Plus](https://additiveplus.com/product/insstek-mx-lab/)) [D].

**InssTek MX-Fab**

- This is the in-family power upgrade: 1-2 kW, 6 × 1 L hoppers and 5 axes ([brochure](https://www.phillipscorp.com/wp-content/uploads/2026/04/HYB-InssTek-Brochure_2026Apr_compressed.pdf)) [V].
- At 6,600 lb and 61 × 82 × 92 in it is not a benchtop system. Check CB 154's floor loading and door clearance before considering it [I].

**Optomec LENS CS 250 and the legacy LENS 450 / CS 150**

- **CS 250.** Launched in 2020 as a "compact research-oriented" system for alloy development: 250 mm cube, four integrated feeders, optional inert processing for "reactive and reflective" alloys including Cu, and a base price under $300k ([VoxelMatters](https://www.voxelmatters.com/optomec-presents-cs250-and-hc-tbr-metal-3d-printers-for-research-to-production/); [3DPI](https://3dprintingindustry.com/news/optomec-launches-compact-cs250-and-industrial-hc-tbr-lens-metal-3d-printers-178877/)) [N].
- **CS 250 laser power is not published.** Optomec's LDH 3.X head covers 0.5-3 kW ([VoxelMatters](https://www.voxelmatters.com/optomecs-new-lens-ldh-3x/)) [N].
- **Legacy compact units.** The LENS 450 (400 W IPG, 100 mm cube, under 10 ppm O₂, Class 1, 1 × 1 × 1.5 m; [2016 sheet](https://www.engineering.pitt.edu/contentassets/788c4963536149dbba851c972922e23f/lens_450_datasheet-web.pdf)) and the CS 150 (400 W, 150 mm cube, 600 kg; [2018 sheet](https://optomec.com/wp-content/uploads/2018/11/LENS-150-AM-CA_WEB0918.pdf)) sit in **the same power class as the MX-Lab**. They are no upgrade on Utah's machine.
- **Copper.** Optomec announced a pure-Cu LENS process in 2019 but published no density or conductivity. It said bronze, brass and cupronickel "may" follow ([3DPI](https://3dprintingindustry.com/news/optomec-updates-lens-system-to-3d-print-in-copper-165920/)) [N/V]. Nebraska lists GRCop-84 and Cu-Ni as R&D materials on its LENS MTS ([UNL](https://nercf.unl.edu/major-equipment/optomec-lens-machine-tool-series/)) [U].
- **Ownership.** Optomec has acquired Huffman; I could not confirm when ([DE247](https://www.digitalengineering247.com/article/optomec-acquires-huffman/news)) [N]. I found no 2025-26 LENS launches, so confirm the CS 250 is still offered and supported.

**FormAlloy X-series / X2 (the Mines machine) and L-series**

- **Base configuration.** In 2019 the X-series started at $200k with a 500 W head, one feeder and three axes. Upgrades covered higher-power IR or **blue** heads, up to 4 feeders, 5 axes, and a glovebox inert atmosphere ([AM Media](https://www.additivemanufacturing.media/blog/post/directing-the-future-of-laser-metal-deposition-lmd)) [N].
- **Mines X2.** 1 kW, 4 feeders, 250 × 250 × 300 mm, melt-pool monitoring with closed-loop control; lists "alloys of… Cu" ([Mines ADAPT](https://adapt.mines.edu/capabilities/)) [U].
- **JHU unit.** 1070 nm, 1 kW, O₂ and H₂O under 100 ppm, same envelope ([JHU](https://engineering.jhu.edu/MCP/?p=13932); I could not open this page, so these figures come from a search summary) [U].
- **Small-batch feeder.** The **16-hopper Alloy Development Feeder** is made for "high throughput bulk alloy synthesis" ([2020 listing](https://www.mfgnewsweb.com/archives/4/56462/Current-News-apr20/ad_info.aspx)) [N]. A 2019 summary said each vial holds 15-20 mL; I could not verify that. The AX head is rated to 8 kW ([3DPI](https://3dprintingindustry.com/news/formalloy-announces-new-powder-feeder-and-robotic-integration-for-metal-deposition-systems-155745/)) [N].
- **Monitoring.** DEDSmart includes a 55 FPS melt-pool camera, laser-profilometer layer checks and closed-loop power control ([DEDSmart](https://formalloy.com/dedsmart/)) [V].
- **Blue L-series and Cu.** The L-series used a **Nuburu** blue laser; the first unit went to UCSD in 2017 ([3DPrint](https://3dprint.com/188512/formalloy-l-series-blue-laser/)) [N]. UCSD later reported 99.6%-dense pure Cu by blue blown-powder DED (Liu, Wang, Kaufmann, Vecchio, *J. Manuf. Process.* 85 (2023) 314) [P]. A secondary write-up names the machine as a FormAlloy L221 ([summary](https://chanelink.com/community/730.html)).
- **GRCop and hybrid heads.** FormAlloy and NMSU have a NASA JPL STTR depositing GRCop-42 ([award](https://inknowvation.com/node/181254)) [G]. I found **no hybrid blue/IR FormAlloy head**.

**Meltio M450 / M600 / Engine Blue**

- **M450.** 6 × 200 W, 976 nm, 1.2 kW IR, wire 0.8-1.2 mm, 145 × 168 × 390 mm, 250 kg. Cu is "under development." Listed at $154k or $203k and shown "currently unavailable," so it may be being retired ([MatterHackers](https://matterhackers.com/store/l/meltio-m450-wire-laser-metal-3d-printer)) [D].
- **M600 specs.** 9 × 450 nm diodes totalling 1 kW, fibre-free head, 300 × 400 × 600 mm, full inert chamber, closed loop, 800-1000 kg. Inerting to 50 ppm O₂ takes about 8 m³ Ar ([datasheet 2026](https://meltio3d.com/wp-content/uploads/2026/08/Technical-datasheet_-Meltio_M600_26_08.pdf); [FAQ](https://multistation.com/voy_content/uploads/sites/4/2024/03/faq-meltio-m600-launch.pdf)) [V].
- **M600 copper.** ERCuNiAl "Marine Bronze" is a parameterized Meltio material. The search-indexed datasheet text gives about 565 MPa UTS, 255 MPa YS and 32% elongation as-printed at 1.0 kW blue ([materials](https://meltio3d.com/materials/); [v9 PDF, now 404](https://meltio3d.com/wp-content/uploads/2026/07/Meltio_Marine_Bronze_ErCuNiAl_datasheet_v9_06-07-2026.pdf)) [V].
  - CuCrZr is reliable only as thin single-pass walls.
  - Pure Cu parameters are still in development.
  - I found **no Meltio CuNi 70/30 or 90/10 profile**, although commodity ERCuNi wire "may" run on its open-wire policy [V/I].
- **Engine Blue.** A 1.0 or 1.4 kW blue robot/CNC kit ([LFW](https://www.laserfocusworld.com/laser-processing/article/55264409/metal-3d-printer-integration-kit-features-14-kw-blue-laser-head)) [N].
- **Fit for this lab.** All Meltio models are **wire-only**, so none can consume atomizer powder.

**AddUp (BeAM) Modulo 250**

- The Modulo 250 was the small 5-axis R&D model: 400 × 250 × 300 mm, 500 W ([Metal AM 2018](https://www.metal-am.com/beam-to-exhibit-modulo-250-directed-energy-deposition-machine-at-formnext-2018/)) [N].
- AddUp now lists only the BeAM 400/800 ([AddUp](https://addupsolutions.com/machines/ded/)) [V].
- The Modulo 400 sheet gives 6,600 kg, two vibratory feeders of 2.5 L each (about 13 kg of steel), nozzles of 200-500 W or 400-2000 W, and "CuAl" among tested materials ([spec](https://addupsolutions.com/wp-content/uploads/2023/09/Modulo-400-Tech-Specs-22-EN.pdf)) [V]. Not compact, and the hoppers are badly matched to 0.5 kg lots.

**Additec µPrinter / AMDROID**

- The µPrinter (2019) offered 600 W of diodes, wire plus powder, an Ar chamber, 160 × 120 × 450 mm and about $90k, but is listed as discontinued ([Aniwaa](https://www.aniwaa.com/product/3d-printers/additec-uprinter/)) [N].
- AMDROID / AMDROID X are field-deployable 6-12 kW laser-wire robots, not lab benchtops ([TCT 2025](https://www.tctmagazine.com/additec-launches-amdroid-laser-ded-system-at-milam-2025/)) [N].

**Blue and green sources: Laserline, Nuburu, TRUMPF, and DMG MORI as reference**

- **Laserline LDMblue.** 445 nm at 1 kW (2019), 1.5-2 kW (2020) and 3 kW CW (2022), marketed for Cu cladding and AM ([Semiconductor Today](https://semiconductor-today.com/news_items/2022/apr/laserline-180422.shtml)) [N]. 1 kW blue cladding of pure Cu is published (SPIE 2019, https://doi.org/10.1117/12.2506007) [P]. It is a source, not a DED system, so you would need an integrator, a head, motion and a Class 1 enclosure.
- **Cost of blue.** Meltio says blue sources cost "several hundred per cent" more than equivalent near-IR ([Meltio blog](https://meltio3d.com/blue-lasers-for-laser-wire-deposition/)) [V].
- **Nuburu (avoid as a sole source).**
  - April 2025: pivoted to defense and security ([BusinessWire](https://www.businesswire.com/news/home/20250415617014/en/NUBURU-Announces-Strategic-Corporate-Update-Focused-on-Defense-Security-Advanced-Technologies-and-Growth-Initiatives)).
  - January 2026: bought the Italian blue-laser maker Lyocon to "reactivate" its laser business ([BusinessWire](https://www.businesswire.com/news/home/20260120738380/en)).
  - February-September 2026: trading halts, NYSE American suspension, and 1-for-4.99 and 1-for-40 reverse splits ([Semiconductor Today](https://www.semiconductor-today.com/news_items/2026/sep/nuburu-100926.shtml)) [N].
  - I found no evidence that legacy Nuburu lasers (as on the FormAlloy L-series) are still supported.
- **TRUMPF TruDisk green.** 515 nm, 200 W-3 kW ([TRUMPF](https://trumpf.com/en_GB/products/lasers/disk-lasers/trudisk-with-green-wavelength)) [V].
  - Fraunhofer IWS published green-laser deposition of Cu ([doi](https://doi.org/10.1007/s00170-020-05117-z)) [P].
  - EWI runs a green DED head, with no results published yet ([EWI](https://ewi.org/ewis-green-laser-capability-for-electrification-copper-welding-and-ded)) [N].
  - I found no compact turnkey green DED product.
- **DMG MORI LASERTEC 65 DED hybrid (2nd gen, launched January 2026).** 3 kW IR standard plus an **optional 2 kW blue** for Cu. Powder pots come in S/M/L sizes of 0.5/2.3/5 L ([DMG MORI](https://us.dmgmori.com/products/machines/additive-manufacturing/powder-nozzle/lasertec-65-3d-hybrid)) [V]. It is a full-size hybrid machine tool, included only as a price and capability reference.

**Hybrid Manufacturing Technologies AMBIT**

- Tool-changeable laser-cladding heads that turn an existing CNC into a hybrid machine ([LFW](https://laserfocusworld.com/industrial-laser-solutions/article/14216354/hybrid-cncs-expand-additive-manufacturing)) [N].
- No price, no blue head and no Cu data found. Only relevant if BYU has a suitable CNC to host it.

**Compact wire-arc and plasma systems**

- **This is the most mature route for dense CuNi and NAB** (Section 3), but it is wire-only.
- **Mines already has one.** Its ADAPT lab has a **UR10e cobot with a Fronius TPS 400i CMT** and a Panasonic robot arc cell ([Mines ADAPT](https://adapt.mines.edu/capabilities/)) [U]. Commodity ERCuNi (70/30) and ERCuNiAl wires could be run there instead of buying a WAAM cell [I].
- **Packaged compact options.**
  - MetalWorm MW500 LAB: Fanuc CRX-5iA plus Fronius TPS 400i or iWave 500i; lists "aluminium nickel bronze" ([Metal AM](https://www.metal-am.com/metalworm-adds-mw500-lab-directed-energy-deposition-additive-manufacturing-machine/)) [N].
  - WAAM3D MiniWAAM: plasma (PTA) wire, 600 × 600 × 500 mm envelope in a 1.6 × 1.5 × 1.6 m enclosure; showed a 316L/NAB demo ([datasheet](https://www.multistation.com/voy_content/uploads/2026/03/miniwaam-data-sheet-november-2025-v1.1.pdf); [TCT](https://www.tctmagazine.com/waam3d-launches-compact-miniwaam-metal-3d-printer-tct-3sixty/)) [V/N].
  - Neither publishes a price.

---

## 6. Ranked shortlist: Be-free Cu-alloy research next to an ultrasonic atomizer

**How far a 0.5 kg lot goes [I].**

- At 2 g/min feed and 50-70% powder capture, 0.5 kg is about 4 h of deposition. That makes about 250-350 g of deposit, or 30-40 cm³ of CuNi or NAB.
- That is enough for 10-20 small density, hardness and corrosion coupons, or about 6-9 sub-size tensile blanks.
- So the **minimum hopper charge, and the "heel" a feeder leaves behind, decide how many compositions one lot covers.** This must be answered by each vendor (Section 9).

**Assumptions behind the cost estimates [I].**

- Year-1 dollars, excluding characterization equipment and post-warranty service.
- Service contracts typically run 8-12% of machine price per year from year 2.
- Ranges are my estimates where no public price exists. **Replace them with quotes before submitting.**

### No. 1: FormAlloy X-series powder DED, configured to match or exceed the Mines X2

**Configuration:**

- 1-2 kW IR fibre laser on the AX head.
- Inert glovebox chamber.
- Four standard feeders, or the 16-hopper ADF for small lots.
- DEDSmart closed-loop monitoring and a heated build plate.
- Price the blue head as an option now, or as an upgrade path, for pure Cu, CuCrZr and GRCop.

**Why it ranks first:**

- 1-2 kW IR overlaps the 0.6-1.2 kW laser-wire window documented for NAB and the 0.7-1 kW blue-wire range used for CuNi 70/30, leaving margin for bulk builds without preheat [I].
- It adds the power that Utah's MX-Lab lacks for GRCop and CuCrZr. Blue gives the only compact, demonstrated route to 99.6%-dense pure Cu (UCSD).
- It is the same platform as Mines, so parameter sets and students can move between the two labs.
- It is a US vendor.

| Item | Estimate |
|---|---|
| Machine, IR 1-2 kW, 4 feeders, glovebox, monitoring | $400-650k [I]. Basis: $200k base in 2019 for 500 W, 1 feeder, 3-axis, no inert chamber [N]; add laser, feeders, glovebox and monitoring, plus about 30% inflation since 2019. |
| Blue head option | +$150-300k [I]. Basis: blue sources cost "several hundred %" more than near-IR [V]. |
| ADF or two extra feeders | $30-80k [I] |
| Installation, rigging, training | $15-30k [I] |
| Chiller (if not bundled), 3-phase drop, Ar dewar manifold | $15-45k [I] |
| Laser safety: if Class 1, an SOP and Laser Safety Officer sign-off; if not, an interlocked laser-controlled area | $2-30k [I] |
| Powder and Ni hygiene: glovebox or downdraft bench, rated HEPA vacuum, sealed transfer, P100 respirators, air monitoring | $15-40k [I] |
| Year-1 consumables and argon: nozzles, cover glass, substrates, filters, about 50-100 purges | $15-30k [I] |
| **All-in, year 1** | **About $0.5-0.9M IR-only; about $0.65-1.2M with blue** [I] |

### No. 2: InssTek MX-Lab of your own

**Configuration:** 500 W, all six CVM hoppers, atmosphere-control option, plus a substrate heater (bought or built).

**Why it ranks second:**

- Lowest cost and easiest facility. It is about 0.5 m³ and runs on single-phase 220 V.
- It is the best fit for 0.5 kg lots and six-powder in-situ composition screening.
- Recipes transfer directly from Utah.
- The catch: it is power-capped exactly like Utah's. **Before buying, run CuNi 70/30, CuNi 90/10 and NAB density cubes on Utah's machine.**

| Item | Estimate |
|---|---|
| Machine | **$250-400k [I]**. No public price; Phillips and Additive Plus quote on request. Basis: the 2019 FormAlloy 500 W base price plus six feeders, vision and atmosphere control. |
| Installation and training | $0-10k. Additive Plus says installation, training and DMT parameter support are included [D]. |
| 220 V single-phase 20 A circuit; Ar 99.999% supply | $5-15k [I] |
| Substrate preheat stage (Iatan preheated to 165-175 °C) | $5-15k [I] |
| Laser safety | About $1-3k for the SOP if Class 1 is confirmed (the datasheet cites EN 60825-1 but no class); about $10-30k otherwise [V/I] |
| Powder and Ni hygiene | $15-40k [I] |
| Year-1 consumables and argon | $10-20k [I] |
| **All-in, year 1** | **About $0.3-0.5M** [I] |

### No. 3: Optomec LENS CS 250, the alternative to No. 1

**Configuration:** 3-axis, about 1-2 kW fibre laser on the LDH 3.X head, 4 feeders, inert processing option.

**Why it ranks third:**

- Similar capability to No. 1, with a long LENS research history.
- Its Cu evidence is vendor-only.
- The laser power and price are unpublished, and I found no 2025-26 LENS launches, so confirm the CS 250 is still offered.

| Item | Estimate |
|---|---|
| Machine | **$300-500k [I]**. Basis: "base under $300k" in 2020 [N]; Aniwaa about $400k [N]. |
| Ancillaries (installation, power, Ar, chiller if needed, Ni hygiene, consumables) | $60-130k [I] |
| **All-in, year 1** | **About $0.36-0.63M** [I] |

**Wire complement, not ranked because it cannot use atomizer powder.**

- **CMT-WAAM** is the best-documented dense route for all three naval reference alloys. Use the Mines cobot first; a dedicated CMT cobot cell would be about $0.1-0.25M [I].
- **Meltio M600** lists at $240-296k [D]. It has a vendor-validated blue ERCuNiAl profile and an inert chamber, and needs 3-phase power. Its all-in year 1 is about $0.3-0.38M [I].

---

## 7. Verdict for each shortlisted system: can it print the Cu alloys we want?

**FormAlloy X-series, 1-2 kW IR (plus blue option)**

- **NAB:** **yes, high confidence** [I, grounded in P/PP].
  - Laser powder DED has made NAB over 99.8% dense from ultrasonic-atomized feedstock (Fraunhofer IPK; power not retrieved).
  - Laser wire DED has made it sound at 0.6-1.2 kW (Oregon State) and 9 kW IR (ARL).
  - 1-2 kW IR overlaps the documented wire window.
  - No FormAlloy-specific NAB data was found.
- **CuNi 70/30:** **likely yes, ≥ 99% expected with pre-alloyed powder** [I]. Laser powder DED from blends is published (watch for elemental-Ni porosity), and 0.7-1 kW blue wire has deposited it, with weak fusion between layers at the low-energy end. There is no FormAlloy-specific data and no bulk density figure anywhere.
- **CuNi 90/10:** **likely, but unpublished for any laser DED.** It has the highest conductivity of the three naval alloys (45-50 W/m·K), so I expect it to be the hardest to make dense [I]. Plan dense-cube trials.
- **GRCop-42:** plausible at about 1 kW IR. WSU found a 500-950 W window on a 1 kW fibre; NASA DED reached under 0.1% porosity; FormAlloy has an STTR on it. FormAlloy-measured density is not published.
- **CuCrZr:** unproven by IR DED anywhere. Expect behaviour like GRCop at 1-2 kW [I].
- **Pure Cu:** **only with the blue option** (99.6%, UCSD, blue blown powder) or IR of 2 kW or more (99.9%, RRCAT).

**InssTek MX-Lab, 500 W**

- **Al-bronze / NAB:** **yes, for coupons and graded samples**, on vendor evidence. That includes MX-Lab demos and a 98.9%-dense DMT Al-bronze, plus 308-500 W average Al-bronze-rich deposits on the 1 kW sibling [PP]. Fully dense bulk NAB at 500 W or less is **plausible but not demonstrated**; prove it at Utah first.
- **CuNi 70/30 and 90/10:** **unproven on this platform.** The closest evidence is about 0.4-0.47 kW average pulsed Cu‑38Ni cladding with preheat (dense, crack-free) [P]. Expect it to need preheat and a narrow window, especially for 90/10 [I].
- **GRCop-42 and CuCrZr:** doubtful. The only 500 W GRCop-42 result is one of six workable settings on a different machine, with no density measured [PP].
- **Pure Cu:** **no.** There is no evidence of dense pure Cu by IR DED at 500 W or less, and about 2 kW IR is the practical floor [P/I].

**Optomec LENS CS 250, about 1-2 kW IR**

- Expect it to match FormAlloy for NAB, CuNi and GRCop, since it is the same physics at the same power [I].
- Optomec's Cu claims (a pure-Cu process, and bronze or cupronickel "may" work) have **no published density or conductivity data**.
- There is no blue option, so pure Cu would need 2 kW or more IR plus Optomec's back-reflection-tolerant optics. That is unverified.

---

## 8. Beryllium-copper and nickel hazards

- **Don't print actual BeCu.** C17200 contains 1.80-2.00% Be. Melting, laser welding and laser cutting of it are recognized inhalation hazards (Materion safety guidance as retrieved: https://hkvxni.files.cmp.optimizely.com/download/defdd728a04211eea3693aa4a5458726) [V].
- **What OSHA 29 CFR 1910.1024 would require:**
  - Limits: exposure limit (PEL) 0.2 µg/m³ as an 8-h average, short-term limit (STEL) 2.0 µg/m³ over 15 min, and action level 0.1 µg/m³.
  - A regulated area, exposure monitoring, medical surveillance including the BeLPT blood test, and decontamination ([eCFR](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1910/section-1910.1024)) [G].
- **Health effects.** Chronic beryllium disease can occur below the exposure limit and has no cure, and Be is an IARC Group 1 carcinogen ([OSHA](https://www.osha.gov/beryllium/health-effects)) [G].
- **Implication [I].**
  - Atomizing or printing BeCu would contaminate the atomizer, the DED chamber, filters and powder-handling gear for every later user.
  - Keep the program Be-free.
  - If a BeCu baseline is needed, buy wrought C17200 test coupons rather than powder.
- **Ni-bearing powders (all CuNi and NAB).**
  - Nickel compounds are IARC Group 1 and metallic Ni is Group 2B ([ATSDR](https://www.atsdr.cdc.gov/ToxProfiles/tp15-c7.pdf)) [G].
  - OSHA's limit for Ni metal and insoluble compounds is 1 mg/m³ ([OSHA](https://www.osha.gov/chemicaldata/509)). NIOSH recommends 0.015 mg/m³ and treats Ni as a potential occupational carcinogen ([NIOSH](https://cdc.gov/niosh/idlh/7440020.html)) [G].
  - Plan for enclosed powder transfer, local exhaust or HEPA, and P100 respirators. Also check combustible-metal-dust handling for the fines [I].

---

## 9. Questions for vendors (for the quotes, not sent)

1. **Minimum powder charge.** What is the minimum mass per hopper to start and hold a stable feed rate for a Cu alloy at 4.2-4.5 g/cm³ apparent density? What heel stays unusable? How long does a hopper changeover and clean take between 0.5 kg lots without cross-contamination? Is a small-volume hopper or vial option available (FormAlloy ADF, Powder Motion Labs X3E 200 mL)?
2. **Powder spec.** What particle-size range, flow (Hall or Carney) and satellite or fines limits apply? Will it accept ultrasonic-atomized powder with a wider distribution (Fraunhofer reports more fines and coarse particles than gas-atomized)?
3. **Cu-alloy data on the quoted configuration.** Do you have parameter sets and measured density (Archimedes plus CT), tensile and conductivity for CuNi 70/30, CuNi 90/10, NAB C95800/C63000, CuCrZr and GRCop-42? Can we get sample coupons, and run a paid trial with our own powder?
4. **Power and wavelength.** What IR power options exist? Can the system be upgraded to blue later, and at what price? Is back-reflection protection or isolation fitted for Cu? For InssTek: is any MX-Lab option above 500 W, and is Utah's unit 300 W or 500 W?
5. **Substrate preheat.** What maximum build-plate temperature is available?
6. **Atmosphere.** What O₂ and H₂O levels are achievable, and how much time and argon does it take to reach them? What argon flow is used during deposition? Glovebox or chamber?
7. **Laser safety.** Is the system Class 1 as delivered, or does it need a laser-controlled area? What interlocks and viewing windows are fitted?
8. **Facility.** What electrical service is needed? Is the chiller included, and what does it need? Compressed air? Footprint, weight, floor loading and door clearance? Exhaust and filtration for Ni-bearing fume and fines? Combustible-dust guidance?
9. **Software openness.** Are G-code and all parameters open? Is there an API or export for logs and raw melt-pool camera data? Is the closed-loop controller user-configurable?
10. **Commercial terms.** Academic price and what it includes (training, initial parameter development), warranty length, service contract cost, lead time, and location of US field service and spares (Phillips for InssTek). What is the supply continuity of the laser source, especially any Nuburu-derived blue source?
11. **Meltio.** Is there a validated ERCuNi (70/30) or CuNi 90/10 wire profile? When will the 1.4 kW Marine Bronze profile arrive? Is the M450 still sold?

---

## 10. Caveats and unverified items

- **Prices.**
  - No public price was found for the MX-Lab, MX-Fab, CS 250, FormAlloy's current systems, Laserline, AMBIT or DMG MORI.
  - All-in figures marked [I] are planning estimates only.
  - The MatterHackers Meltio prices disagree between listings, and the M450 page shows the machine as unavailable.
- **Meltio datasheets.** The Marine Bronze and CuCrZr PDFs return 404 now. Their numbers come from search-indexed text of those PDFs.
- **Fraunhofer IPK NAB work.** The laser power for the ultrasonic-atomized NAB → DED work was not retrieved, and the euspen-abstract and *Addit. Manuf.* 2025 property sets differ, probably because of different conditions or orientation.
- **Absorptivity of the naval alloys.** No measured 1064 nm absorptivity was found for CuNi or NAB. The claim that these alloys absorb IR better than Cu is inference from their resistivity.
- **Conductivity values.** The copper.org alloy pages for C71500, C70600 and C63000 blocked automated fetch. The values come from Matthey, makeitfrom and Concast; check them against the CDA pages by hand.
