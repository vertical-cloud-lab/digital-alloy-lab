<!--
Edison Scientific LITERATURE task (phase 4)
- Task ID: 6019b766-9f83-4a81-9026-5ae0dc2d3fbe
- Submitted: 2026-10-17T19:03:31Z
- Fetched: 2026-10-17T19:30:59Z (status: success)
- Raw trajectory JSON: ../raw/ec-01-droplet-cell-screen.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

LAB CONTEXT: the lab has a small open-frame gantry liquid handler (about
390 x 230 x 120 mm working volume; one head carrying a 20 uL pipette, a vial
capper and cameras; no tool changer; Python/YAML control software that drives
PalmSens EmStat and Admiral Squidstat potentiostats for OCP, CV,
chronoamperometry and chronopotentiometry, not yet EIS). It owns no
potentiostat and can borrow a conventional benchtop one. Specimens are small:
polished faces of DED single tracks, thin walls and blocks (a few mm to 20 mm
across), and cross-sections of repair coupons that cross the fusion line into
cast NAB or wrought Cu-Ni.

QUESTION: How well can a small-area, robot-positioned electrochemical cell
(scanning droplet cell, capillary microcell, or an O-ring well clamped on
the specimen, with a mini Ag/AgCl reference and Pt counter electrode) replace
a conventional flat cell (about 1 cm2, ASTM G59/G61/G106 practice) for
screening copper alloys (Cu-Ni, aluminum bronze, NAB, brasses) in seawater or
3.5% NaCl? Report: (1) published comparisons of droplet or microcell versus
conventional-cell corrosion current, polarization resistance, impedance and
breakdown potentials for copper alloys or, if none, for other alloys; (2)
pitfalls (crevice at the O-ring or droplet edge, oxygen depletion and mass
transport, IR drop, reference drift, droplet evaporation, current ranges of
nA on mm2 areas); (3) local measurements across welds, cladding or AM
deposits, especially the fusion line and heat-affected zone of NAB or Cu-Ni
(selective phase corrosion of retained beta or martensite); (4) automated or
high-throughput corrosion screening platforms (scanning droplet cells,
multi-electrode arrays, self-driving labs) that used copper alloys or
seawater, with throughput numbers; (5) minimum potentiostat specifications
for LPR, EIS and cyclic polarization on such areas (current resolution,
compliance, EIS frequency range). Give DOIs and numbers.

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

LAB CONTEXT: the lab has a small open-frame gantry liquid handler (about
390 x 230 x 120 mm working volume; one head carrying a 20 uL pipette, a vial
capper and cameras; no tool changer; Python/YAML control software that drives
PalmSens EmStat and Admiral Squidstat potentiostats for OCP, CV,
chronoamperometry and chronopotentiometry, not yet EIS). It owns no
potentiostat and can borrow a conventional benchtop one. Specimens are small:
polished faces of DED single tracks, thin walls and blocks (a few mm to 20 mm
across), and cross-sections of repair coupons that cross the fusion line into
cast NAB or wrought Cu-Ni.

QUESTION: How well can a small-area, robot-positioned electrochemical cell
(scanning droplet cell, capillary microcell, or an O-ring well clamped on
the specimen, with a mini Ag/AgCl reference and Pt counter electrode) replace
a conventional flat cell (about 1 cm2, ASTM G59/G61/G106 practice) for
screening copper alloys (Cu-Ni, aluminum bronze, NAB, brasses) in seawater or
3.5% NaCl? Report: (1) published comparisons of droplet or microcell versus
conventional-cell corrosion current, polarization resistance, impedance and
breakdown potentials for copper alloys or, if none, for other alloys; (2)
pitfalls (crevice at the O-ring or droplet edge, oxygen depletion and mass
transport, IR drop, reference drift, droplet evaporation, current ranges of
nA on mm2 areas); (3) local measurements across welds, cladding or AM
deposits, especially the fusion line and heat-affected zone of NAB or Cu-Ni
(selective phase corrosion of retained beta or martensite); (4) automated or
high-throughput corrosion screening platforms (scanning droplet cells,
multi-electrode arrays, self-driving labs) that used copper alloys or
seawater, with throughput numbers; (5) minimum potentiostat specifications
for LPR, EIS and cyclic polarization on such areas (current resolution,
compliance, EIS frequency range). Give DOIs and numbers.

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Small-area electrochemistry for marine copper-alloy DED screening

**Conclusion.** A robot-positioned cell is well suited to **ranking deposits and mapping a polished repair cross-section**, including regions too narrow for a 1 cm² cell. It is **not yet a quantitative replacement** for conventional-cell corrosion rates, polarization resistance, impedance, or breakdown potentials in copper alloys. Direct comparisons on pure Cu already show cell-dependent behavior; no located study validates all four measurements for Cu–Ni, nickel–aluminum bronze (NAB), aluminum bronze, or brass in seawater. Use the local cell to down-select, then establish agreement—or an explicitly empirical relationship—with flat-cell tests and 30-day penetration measurements on the same as-deposited material. [CITE] [GAP] (arjmand2012influenceofph pages 1-5, arjmand2012influenceofph pages 19-23, sakairi2010developmentofa pages 3-4, sur2023ahighthroughput pages 3-4)

## 1. What paired cell measurements establish

The most informative comparisons are below. **In particular, “similar polarization curves” does not establish equal corrosion current or pit-initiation potential:** the copper studies changed oxygen access, sampling scale, or scan protocol. The steel weld study demonstrates useful *relative* spatial ranking despite substantial absolute offsets. [CITE] (arjmand2012influenceofph pages 1-5, sakairi2010developmentofa pages 3-4, cruz2020characterizationofcorrosion pages 9-10)

| Study | Material; electrolyte | Local vs conventional geometry/protocol | Quantitative comparison | Limitation for Cu-alloy seawater screening |
|---|---|---|---|---|
| Arjmand & Adriaens (2012), DOI: [10.3390/ma5122439](https://doi.org/10.3390/ma5122439) | Unalloyed Cu; 0.01–5 mol/L NaCl, pH 3–11 | ~100 µm microcapillary vs macrocell; **nonmatched scan rates:** 10 vs 1 mV/s; EIS 50 kHz–0.1 Hz, 25 mV at OCP | Scale changed the response, not merely its magnitude. At the microscale, `Epit` decreased from 546 to 271 mV vs Ag/AgCl as pH increased 3→11. At 0.01 mol/L NaCl, pH 7, peak imaginary impedance was **0.7 MΩ micro vs 102 Ω macro** (raw impedance—not area-normalized equivalence). Microcell passive current at neutral pH was <15 µA/cm², versus 25–30 µA/cm² at acidic/alkaline pH. (arjmand2012influenceofph pages 1-5, arjmand2012influenceofph pages 5-11, arjmand2012influenceofph pages 19-23) | Best direct Cu comparison, but not Cu–Ni, bronze, NAB, brass, seawater, or ASTM-matched testing. Different scan rates and sampled areas preclude treating microcell `Epit`, `Rp`, or EIS as interchangeable with macrocell values. |
| Sakairi et al. (2010), DOI: [10.2355/isijinternational.50.1466](https://doi.org/10.2355/isijinternational.50.1466) | Pure Cu, Ni, Fe; 0.5 mol/L H₃BO₃ + 0.05 mol/L Na₂B₄O₇ + 0.01 or 0.1 mol/L NaCl | Three-electrode coaxial flow-droplet cell vs traditional macrocell; matched 1 mV/s polarization | Overall polarization behavior was described as similar, but Cu rest potential in the droplet cell differed by about **100 mV** from the macrocell. Cu/Ni line scans gave about **6 nA on Cu vs 2 nA on Ni**; demonstrated spatial resolution was about **200 µm**. (sakairi2010developmentofa pages 1-3, sakairi2010developmentofa pages 3-4, sakairi2010developmentofa pages 4-5) | Pure metals in dilute chloride/borate buffer, not seawater or engineering Cu alloys. The ~100 mV Cu offset shows that oxygen access and droplet geometry can materially shift OCP despite qualitatively similar curves. |
| da Cruz & Bertazzoli (2020), DOI: [10.1007/s11665-019-04531-z](https://doi.org/10.1007/s11665-019-04531-z) | API X70 steel friction-stir weld; deaerated 0.1 mol/L Na₂SO₄, pH 4 | 250 µm aperture, 30 µL microcell, exposed area 4.90×10⁻⁴ cm²; macro areas 0.277 cm² (base metal) and 0.203 cm² (hard zone); matched 1 mV/s | Base metal: `i_corr` **47 vs 28 µA/cm²**, `Rp` **476±68 vs 1177 Ω·cm²**, `E_corr` **−0.382±0.009 vs −0.640 V Ag/AgCl** (micro vs macro). Hard zone: `i_corr` **31 vs 25 µA/cm²**, `Rp` **542±23 vs 1068 Ω·cm²**, `E_corr` **−0.364±0.006 vs −0.611 V**. The local method preserved the relative zone ranking but not absolute values. (cruz2020characterizationofcorrosion pages 2-3, cruz2020characterizationofcorrosion pages 9-10) | Strong quantitative evidence that local cells can rank weld zones while giving biased absolute kinetics; material and acidic sulfate medium are unlike Cu alloys in aerated seawater. Different reference configurations also complicate absolute-potential comparison. |
| Sur et al. (2023), DOI: [10.1149/1945-7111/aceeb8](https://doi.org/10.1149/1945-7111/aceeb8) | 316L and CoCrFeMnNi controls; deaerated 0.1 mol/L H₂SO₄ | Flowing SDC with ~0.3 cm droplet footprint vs 300 mL conventional cell with comparably sized 0.29 cm O-ring opening; same potentiostat and sequence | Reported only **minimal differences** in `E_corr`, `E_crit`, `i_crit`, and `i_pass`, with similar polarization curves. SDC sequence used 15 min OCP, EIS 50 kHz–10 mHz at 20 mV RMS, reduction, then LSV at 5 mV/s. (sur2023ahighthroughput pages 2-3, sur2023ahighthroughput pages 3-4, sur2023ahighthroughput media a55d4e9c, sur2023ahighthroughput pages 4-6) | Useful matched-geometry validation, but neither copper alloys nor chloride/seawater; the ~7 mm² footprint is much larger than a true 100–500 µm microcell and samples more microstructural heterogeneity. |
| **Direct evidence gap** | Cu–Ni, aluminum bronze, NAB, or brass in ASTM D1141 substitute ocean water or 3.5 wt% NaCl | Paired small-area and ~1 cm² ASTM-style cells using identical exposure history, aeration, scan rate, reference, and area normalization | **No located publication provides paired `i_corr`, `Rp`, EIS, and breakdown/repassivation potentials for these engineering copper alloys—especially across an AM/repair fusion line.** | A local cell can be qualified as a **ranking and mapping tool**, but cannot presently be claimed to replace ASTM G59/G61/G106-scale measurements quantitatively without an alloy-specific bridging study. |


*Table: Direct paired studies show that local cells often preserve material or weld-zone rankings but can shift absolute potentials, corrosion currents, polarization resistance, and impedance. No paired seawater study was located for NAB, Cu–Ni, aluminum bronze, or brass.*

Two qualifications matter when interpreting the table. Arjmand and Adriaens used **10 mV/s locally versus 1 mV/s macroscopically**, so their Cu results isolate neither area nor cell geometry; their **0.7 MΩ versus 102 Ω** EIS comparison is *raw* peak imaginary impedance, not an area-normalized polarization-resistance ratio. Their experiment also spans **0.01–5 mol/L NaCl**, much of it far more concentrated than seawater. Conversely, Sur and colleagues’ encouraging paired curves are for stainless/complex alloys in **deaerated sulfuric acid**, with approximately matched millimeter-scale exposed areas—not a micrometer-scale Cu-alloy seawater validation. [NUMBERS] [CITE] (arjmand2012influenceofph pages 19-23, sur2023ahighthroughput pages 3-4, sur2023ahighthroughput media a55d4e9c)

**Full paired-study citations:** F. Arjmand and A. Adriaens, “Influence of pH and Chloride Concentration on the Corrosion Behavior of Unalloyed Copper in NaCl Solution: A Comparative Study Between the Micro and Macro Scales,” *Materials* **5** (2012), 2439–2464, **DOI: 10.3390/ma5122439**; M. Sakairi *et al.*, “Development of a Low Solution Resistance Type Solution Flow Droplet Cell and Investigation of Its Electrochemical Performance,” *ISIJ International* **50** (2010), 1466–1470, **DOI: 10.2355/isijinternational.50.1466**; J. R. da Cruz and R. Bertazzoli, “Characterization of Corrosion Within Friction Stir Weld Zones of an API X-70 Steel Using a Novel Microcell Setup,” *Journal of Materials Engineering and Performance* **29** (2020), 98–108, **DOI: 10.1007/s11665-019-04531-z**; D. Sur *et al.*, “A High Throughput Aqueous Passivation Testing Methodology for Compositionally Complex Alloys Using a Scanning Droplet Cell,” *Journal of The Electrochemical Society* **170** (2023), 081507, **DOI: 10.1149/1945-7111/aceeb8**. [CITE] (arjmand2012influenceofph pages 1-5, sakairi2010developmentofa pages 1-3, cruz2020characterizationofcorrosion pages 1-2, sur2023ahighthroughput pages 2-3)

## 2. Failure modes and controls for a millimeter-scale cell

- **Seal-induced attack:** an O-ring can create an oxygen-starved crevice at precisely the location where chloride attack is being sought; a silicone-gasket capillary can leak or trap a crevice. Record the wetted footprint optically **before and after**, examine whether attack initiates at the seal, and classify seal-adjacent breakdown separately from interior pits. A free droplet avoids a compressed gasket but has a moving contact line and uncertain area; a renewed-flow droplet reduces solution-history artifacts. Arjmand and Adriaens explicitly added a thin silicone tip gasket to prevent leakage through tip–sample crevices; Sur *et al.* balanced inlet/outlet flow to stabilize a **crevice-free** droplet. [CITE] (arjmand2012influenceofph pages 19-23, sur2023ahighthroughput pages 3-4)
- **Oxygen and transport:** a stagnant well can deplete dissolved O₂ as the cathodic reactant; a thin free-droplet rim can instead enhance oxygen access. Either changes mixed potential, LPR and the Cu/Cu₂O/Cu-chloride film. Sakairi *et al.* observed an approximately **100 mV** Cu rest-potential difference between cell types, and da Cruz and Bertazzoli identify oxygen ingress—including through silicone—as a concern. Specify aerated versus deaerated conditions, liquid depth, solution replenishment and hold time; do not equate a stagnant well with flowing seawater. [NUMBERS] [CITE] (sakairi2010developmentofa pages 3-4, cruz2020characterizationofcorrosion pages 9-10, ding2019evolutionofthe pages 1-3)
- **Uncompensated resistance and reference placement:** characterize high-frequency solution resistance on *each* geometry and assess potential error as **I × Rᵤ** during polarization. Put the miniature reference close to, but out of the path of, the exposed spot; compare it against a maintained reference in the actual test electrolyte before/after each run. A bare Ag/AgCl-coated wire is not necessarily a stable, composition-independent seawater reference: Sakairi *et al.* measured its potential shifting with chloride concentration. Report reference filling solution and all potentials against that reference rather than mixing Ag/AgCl and SCE values. [CITE] (sakairi2010developmentofa pages 1-3, arjmand2012influenceofph pages 19-23, huo2025modulatingheatinput pages 4-5)
- **Evaporation, deposits and electrical noise:** a small stagnant volume changes salinity and pH during long OCP/EIS runs; products from one spot contaminate the next unless the electrolyte is renewed. A steel-weld microcell study used approximately **30 µL** under **75 ± 3% relative humidity** specifically to limit evaporation. Enclose or humidify the droplet, keep temperature and fill volume fixed, exchange solution between sites, shield leads and evaluate dummy-cell leakage. Do not re-use an anodically cycled spot for its “initial” EIS: even Cu impedance changed after successive polarization cycles. [NUMBERS] [CITE] (cruz2020characterizationofcorrosion pages 2-3, arjmand2012influenceofph pages 19-23, sur2023ahighthroughput pages 2-3)
- **Statistical area effect:** a tiny aperture may miss the rare connected β′ region, porosity or defect that determines block-scale attack. Repeat on distinct locations and specimens, include deliberately **straddling** spots, and retain the distributions and worst observed attack rather than only mean E₍breakdown₎. High-throughput SECCM work on stainless steel likewise found substantial pitting-descriptor dispersion and warned against undersampling. [CITE] (coelho2023estimatingpittingdescriptors pages 2-3, ding2019evolutionofthe pages 9-12)

## 3. Repair fusion lines: evidence and what remains unmeasured

**[NAVY] [CITE] Cast NAB provides a strong reason to interrogate the HAZ rather than just deposit bulk.** Ding *et al.* tested cast C95800-like NAB of **Cu balance, Al 9.22 wt%, Fe 4.17 wt%, Ni 4.17 wt%, Mn 1.23 wt%** in **3.5 wt% NaCl**. In-situ AFM found β′ martensite attack exceeding **50 nm at 60 min** and stabilizing near **500 nm by 150 min**; lamellar α alongside κIII lost approximately **25 nm in 60 min**, while distant α did not show the same attack. After initial exposure, conventional-cell apparent *i*₍corr₎ fell from **11.35 to 3.78 µA/cm²** by **240 h** as the protective film developed. These are **cast-material AFM/SVET and bulk electrochemical results**, not capillary measurements on an AM fusion line. Y. Ding *et al.*, “Evolution of the Corrosion Product Film on Nickel-Aluminum Bronze and Its Corrosion Behavior in 3.5 wt % NaCl Solution,” *Materials* **12** (2019), 209, **DOI: 10.3390/ma12020209**. [NUMBERS] (ding2019evolutionofthe pages 1-3, ding2019evolutionofthe pages 9-12, ding2019evolutionofthe pages 6-9)

**[NAVY] [CITE] Welding and Cu–Ni evidence identifies which zones to map.** Long-term immersed **plasma-welded NAB** developed selective β′ attack in the HAZ and κIII-associated attack beyond it or beneath biofouling/crevices; these observations concern welding, **not blown-powder laser DED**. T. H. E. Dobson, *Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze*, University of Bristol PhD thesis (2024); **no verified thesis DOI** in the retrieved record. Separately, S. Xing *et al.*, “Characterization of Corrosion Behavior and Corrosion Production Property of 90-10 Cupronickel Welding Joints in Flowing Seawater,” *Metals* **13** (2023), 294, **DOI: 10.3390/met13020294**, cut **separate approximately 10-mm-diameter specimens** from weld metal, HAZ and base metal: the HAZ had the lowest resistance, and its pits after **30 days** were **7, 6 and 4 µm** at **1, 3 and 5 m/s**, respectively. The base alloy was **Cu balance, Ni 9–11 wt%, Fe 1.5–1.8 wt%, Mn 0.5–1.0 wt%**, whereas weld filler was **Cu balance, Ni 28–33 wt%**, with **Ti 0.2–0.5 wt%**; hence it is **not** evidence that a composition-matched Cu–Ni laser repair behaves identically. [NUMBERS] (dobson2024corrosionmechanismsand pages 1-6, xing2023characterizationofcorrosion pages 1-2, xing2023characterizationofcorrosion pages 9-12)

For AM, R. Huo *et al.*, “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing,” *Materials* **18** (2025), 2205, **DOI: 10.3390/ma18102205**, measured *i*₍corr₎ increasing from **2.56 ± 0.04 to 7.52 ± 0.07 µA/cm²** as **wire-arc** heat input rose **243.8→644.7 J/mm**. Its approximately **1 cm² conventional-cell** results demonstrate process sensitivity, but neither small-area screening nor powder-laser DED performance. [NUMBERS] [GAP] (huo2025modulatingheatinput pages 1-2, huo2025modulatingheatinput pages 4-5)

**Proposed mapping, not a published validated protocol:** polish an as-built block or repair cross-section and place nonoverlapping apertures in deposit, deposit-side fusion boundary, directly **across** the fusion boundary, substrate-side HAZ and remote substrate; image/register every footprint against optical/SEM phase maps. Start at roughly **0.5–1 mm** aperture for reproducible ranking; use approximately **100–250 µm** only where the actual HAZ is narrower, with the increased current/noise and sampling penalties. A coaxial flow droplet distinguished deposited Ni from Cu (**approximately 6 versus 2 nA**) with approximately **200 µm** spatial resolution, whereas a **250 µm** masked cell mapped five zones of a *steel* friction-stir weld. The literature located does **not** establish comparable resolution or calibrated electrochemical contrasts for a cast-NAB/Cu–Ni DED repair interface. [NUMBERS] [GAP] (sakairi2010developmentofa pages 3-4, sakairi2010developmentofa pages 4-5, cruz2020characterizationofcorrosion pages 2-3)

## 4. Automation and achievable throughput

**[CITE] [NUMBERS] Actual saline Cu-containing example:** C. D. Grill, J. P. Kollender and A. W. Hassel, “Combinatorial Electrodeposition of Cobalt-Copper Material Libraries,” *Journal of The Electrochemical Society* **163** (2016), D3069–D3075, **DOI: 10.1149/2.0101612jes**, used a robot-positioned **577 µm effective-diameter** gasketed scanning cell on a Cu–Co electrodeposited composition library, measuring polarization in **5 wt% NaCl** over **±250 mV from OCP at 5 mV/s**. It demonstrates automated chloride mapping of a *Cu-containing* alloy, but reports **no defensible tests/hour figure** and is neither Cu–Ni/NAB nor seawater-equivalent. Its published composition gradient is in **atomic percent**; no verified wt% conversion is available, so it is intentionally not quoted here as a wt% range. (grill2016combinatorialelectrodepositionof pages 3-4, grill2016combinatorialelectrodepositionof pages 2-3)

**[CITE] [NUMBERS] Documented serial and parallel benchmarks:** Sur *et al.* tested **nine** non-Cu alloy compositions in approximately **4 h (26 min/site)** using a renewed-flow cell: **15 min OCP**, **50 kHz–10 mHz EIS**, followed by a destructive scan, in acid rather than seawater. B. DeCost *et al.*, “Towards Automated Design of Corrosion Resistant Alloy Coatings with an Autonomous Scanning Droplet Cell,” *JOM* **74** (2022), 2941–2950, **DOI: 10.1007/s11837-022-05367-0**, report an approximately **4.5-mm footprint** and closed-loop deposition/characterization, including **Cu deposited from CuSO₄ and dissolved in 1 mol/L H₂SO₄**; no corrosion tests/hour or marine-Cu-alloy demonstration is reported. A. Heyne *et al.*, “Qualification of Proxy Experiments for Accelerated Electrochemical Testing in Self-Driving Labs,” *Analytical and Bioanalytical Chemistry* **418** (2026), 5345–5360, **DOI: 10.1007/s00216-026-06609-9**, ran **four channels concurrently in 3.5 wt% NaCl**, but their alloys were stainless steel/Ni-containing complex alloys, not copper alloys. Their **100 kHz→1, 0.1 or 0.01 Hz** EIS measurements took approximately **1, 2.5 or 17 min**, respectively; a ±15 mV LPR scan took approximately **5 min**. They found LPR and low-frequency |Z| need not agree, so |Z| at 0.1 Hz is a **screening proxy**, not automatically *R*ₚ. [GAP] (sur2023ahighthroughput pages 2-3, decost2022towardsautomateddesign pages 1-4, decost2022towardsautomateddesign pages 10-13, heyne2026qualificationofproxy pages 2-4, heyne2026qualificationofproxy pages 8-11)

A **single-head, serial** robot cannot claim four-channel parallel throughput. With **15 min OCP + approximately 2.5 min EIS to 0.1 Hz + approximately 5 min LPR**, its optimistic instrument-only time is **22.5 min/site**, or approximately **2.7 sites/h**, *before* approach, filling, cleaning, stabilization checks and repeat locations. Cyclic polarization and 0.01-Hz EIS should therefore be reserved for finalists. This is a calculation from published timings, **not a demonstrated throughput of the described gantry**. [NUMBERS] (sur2023ahighthroughput pages 2-3, heyne2026qualificationofproxy pages 8-11)

## 5. Potentiostat and qualification requirements

**Engineering minimums, not manufacturer specifications or ASTM limits:** For a circular **1-mm-diameter** spot, area is **0.00785 cm²**; *j* = **1 µA/cm²** gives **7.85 nA**. A **0.5-mm** spot gives **1.96 nA**, and a **100-µm** spot only **0.0785 nA (78.5 pA)**. For ±10 mV LPR and **10 kΩ·cm²** area-normalized *R*ₚ, the approximately expected signal at 1-mm diameter is **7.85 nA**; resolve at least **≤0.1 nA** reliably there. For 100-µm work, aim for approximately **≤1–10 pA usable noise**, guarded/shielded leads and explicit leakage/dummy-cell verification. *R*ₚ in Ω·cm² requires converting measured Ω by the **actual wetted area**; a reading of |Z| at 0.1 Hz alone is not an interchangeable *R*ₚ measurement. [NUMBERS] (arjmand2012influenceofph pages 19-23, heyne2026qualificationofproxy pages 8-11, sakairi2010developmentofa pages 3-4)

Specify **three-electrode potentiostatic control**, at least approximately **±2 V working-electrode polarization around OCP**, **≥±10 V available counter-electrode compliance** and a **≥±10 mA current range** to accommodate high-current breakdown on larger spots. These are conservative *procurement design targets*, **not verified minimums** of ASTM or of any particular EmStat/Squidstat. Require an EIS option capable of at least approximately **100 kHz→10 mHz** for full confirmation, a calibrated approximately **5–20 mV AC** excitation, and software access to phase, raw current and fitted high-frequency solution resistance; **100 kHz→0.1 Hz** can serve faster triage. Published protocols span **50 kHz→0.1 Hz at 25 mV** for Cu and **50 kHz→10 mHz at 20 mV RMS** for a scanning cell; the former Cu spectra followed disruptive polarization and do not validate 25 mV as a universally linear EIS amplitude. [CITE] (arjmand2012influenceofph pages 19-23, sur2023ahighthroughput pages 2-3, sur2023ahighthroughput pages 3-4, heyne2026qualificationofproxy pages 8-11)

**[SPEC] Standards boundary:** ASTM **G59** addresses polarization-resistance measurements, **G61** cyclic potentiodynamic polarization for localized corrosion, **G106** verification of EIS equipment, and **D1141** substitute ocean water. They do **not**, on the evidence assembled here, certify an O-ring well or droplet as equivalent to a 1 cm² flat cell; the numerical hardware targets above must not be presented as standard-imposed values. No current ASTM edition identifiers, standard DOIs, or model-specific PalmSens/Admiral compliance, noise and EIS-option ratings could be independently verified from the retrieved primary sources. Check those documents and exact instrument configurations before procurement or claiming conformity. The cited published seawater/NAB and automated NaCl experiments establish the relevant methods and media, not a qualification of this particular robot or borrowed potentiostat. [SPEC] [GAP] (takaloo2011corrosionbehaviorof pages 3-5, huo2025modulatingheatinput pages 4-5, heyne2026qualificationofproxy pages 2-4)

**Decision rule.** On as-deposited C71500-reference, cast-NAB substrate and each candidate deposit/repair, run paired local and conventional tests with matched polish, electrolyte batch, O₂ state, reference, exposure time and scan rate; include independent spots that cross the fusion boundary. Accept local-cell descriptors for **ranking only** if replicated order and uncertainty agree; retain conventional-cell measurements and **30-day maximum selective-attack depth** as the seawater-performance decision. A pit beginning at a gasket, an unstable reference, or a changing wetted area invalidates a numerical breakdown-potential comparison. No located work establishes that a passing local LPR/EIS screen alone predicts wrought **70–30 Cu–Ni (Cu balance, Ni approximately 30 wt%)** equivalence after 30 days. [GAP] (arjmand2012influenceofph pages 1-5, arjmand2012influenceofph pages 19-23, ding2019evolutionofthe pages 9-12, xing2023characterizationofcorrosion pages 9-12, heyne2026qualificationofproxy pages 8-11)

References

1. (arjmand2012influenceofph pages 1-5): Farzin Arjmand and Annemie Adriaens. Influence of ph and chloride concentration on the corrosion behavior of unalloyed copper in nacl solution: a comparative study between the micro and macro scales. Materials, 5:2439-2464, Nov 2012. URL: https://doi.org/10.3390/ma5122439, doi:10.3390/ma5122439. This article has 97 citations.

2. (arjmand2012influenceofph pages 19-23): Farzin Arjmand and Annemie Adriaens. Influence of ph and chloride concentration on the corrosion behavior of unalloyed copper in nacl solution: a comparative study between the micro and macro scales. Materials, 5:2439-2464, Nov 2012. URL: https://doi.org/10.3390/ma5122439, doi:10.3390/ma5122439. This article has 97 citations.

3. (sakairi2010developmentofa pages 3-4): Masatoshi Sakairi, Takuya Murata, Tatsuya Kikuchi, and Koji Fushimi. Development of a low solution resistance type solution flow droplet cell and investigation of its electrochemical performance. Isij International, 50:1466-1470, Oct 2010. URL: https://doi.org/10.2355/isijinternational.50.1466, doi:10.2355/isijinternational.50.1466. This article has 11 citations and is from a peer-reviewed journal.

4. (sur2023ahighthroughput pages 3-4): Debashish Sur, Howie Joress, Jason Hattrick-Simpers, and John R. Scully. A high throughput aqueous passivation testing methodology for compositionally complex alloys using a scanning droplet cell. Journal of The Electrochemical Society, 170:081507, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceeb8, doi:10.1149/1945-7111/aceeb8. This article has 21 citations and is from a peer-reviewed journal.

5. (cruz2020characterizationofcorrosion pages 9-10): Juliane Ribeiro da Cruz and Rodnei Bertazzoli. Characterization of corrosion within friction stir weld zones of an api x-70 steel using a novel microcell setup. Journal of Materials Engineering and Performance, 29:98-108, Jan 2020. URL: https://doi.org/10.1007/s11665-019-04531-z, doi:10.1007/s11665-019-04531-z. This article has 10 citations and is from a peer-reviewed journal.

6. (arjmand2012influenceofph pages 5-11): Farzin Arjmand and Annemie Adriaens. Influence of ph and chloride concentration on the corrosion behavior of unalloyed copper in nacl solution: a comparative study between the micro and macro scales. Materials, 5:2439-2464, Nov 2012. URL: https://doi.org/10.3390/ma5122439, doi:10.3390/ma5122439. This article has 97 citations.

7. (sakairi2010developmentofa pages 1-3): Masatoshi Sakairi, Takuya Murata, Tatsuya Kikuchi, and Koji Fushimi. Development of a low solution resistance type solution flow droplet cell and investigation of its electrochemical performance. Isij International, 50:1466-1470, Oct 2010. URL: https://doi.org/10.2355/isijinternational.50.1466, doi:10.2355/isijinternational.50.1466. This article has 11 citations and is from a peer-reviewed journal.

8. (sakairi2010developmentofa pages 4-5): Masatoshi Sakairi, Takuya Murata, Tatsuya Kikuchi, and Koji Fushimi. Development of a low solution resistance type solution flow droplet cell and investigation of its electrochemical performance. Isij International, 50:1466-1470, Oct 2010. URL: https://doi.org/10.2355/isijinternational.50.1466, doi:10.2355/isijinternational.50.1466. This article has 11 citations and is from a peer-reviewed journal.

9. (cruz2020characterizationofcorrosion pages 2-3): Juliane Ribeiro da Cruz and Rodnei Bertazzoli. Characterization of corrosion within friction stir weld zones of an api x-70 steel using a novel microcell setup. Journal of Materials Engineering and Performance, 29:98-108, Jan 2020. URL: https://doi.org/10.1007/s11665-019-04531-z, doi:10.1007/s11665-019-04531-z. This article has 10 citations and is from a peer-reviewed journal.

10. (sur2023ahighthroughput pages 2-3): Debashish Sur, Howie Joress, Jason Hattrick-Simpers, and John R. Scully. A high throughput aqueous passivation testing methodology for compositionally complex alloys using a scanning droplet cell. Journal of The Electrochemical Society, 170:081507, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceeb8, doi:10.1149/1945-7111/aceeb8. This article has 21 citations and is from a peer-reviewed journal.

11. (sur2023ahighthroughput media a55d4e9c): Debashish Sur, Howie Joress, Jason Hattrick-Simpers, and John R. Scully. A high throughput aqueous passivation testing methodology for compositionally complex alloys using a scanning droplet cell. Journal of The Electrochemical Society, 170:081507, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceeb8, doi:10.1149/1945-7111/aceeb8. This article has 21 citations and is from a peer-reviewed journal.

12. (sur2023ahighthroughput pages 4-6): Debashish Sur, Howie Joress, Jason Hattrick-Simpers, and John R. Scully. A high throughput aqueous passivation testing methodology for compositionally complex alloys using a scanning droplet cell. Journal of The Electrochemical Society, 170:081507, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceeb8, doi:10.1149/1945-7111/aceeb8. This article has 21 citations and is from a peer-reviewed journal.

13. (cruz2020characterizationofcorrosion pages 1-2): Juliane Ribeiro da Cruz and Rodnei Bertazzoli. Characterization of corrosion within friction stir weld zones of an api x-70 steel using a novel microcell setup. Journal of Materials Engineering and Performance, 29:98-108, Jan 2020. URL: https://doi.org/10.1007/s11665-019-04531-z, doi:10.1007/s11665-019-04531-z. This article has 10 citations and is from a peer-reviewed journal.

14. (ding2019evolutionofthe pages 1-3): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

15. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

16. (coelho2023estimatingpittingdescriptors pages 2-3): Leonardo Bertolucci Coelho, Daniel Torres, Vincent Vangrunderbeek, Miguel Bernal, Gian Marco Paldino, Gianluca Bontempi, and Jon Ustarroz. Estimating pitting descriptors of 316 l stainless steel by machine learning and statistical analysis. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00403-z, doi:10.1038/s41529-023-00403-z. This article has 32 citations and is from a peer-reviewed journal.

17. (ding2019evolutionofthe pages 9-12): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

18. (ding2019evolutionofthe pages 6-9): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

19. (dobson2024corrosionmechanismsand pages 1-6): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

20. (xing2023characterizationofcorrosion pages 1-2): Shaohua Xing, Shuyu Bai, Ran Liu, Yingshuang Liu, Jiantao Qi, Jian Hou, and Dalei Zhang. Characterization of corrosion behavior and corrosion production property of 90-10 cupronickel welding joints in flowing seawater. Metals, 13:294, Feb 2023. URL: https://doi.org/10.3390/met13020294, doi:10.3390/met13020294. This article has 7 citations.

21. (xing2023characterizationofcorrosion pages 9-12): Shaohua Xing, Shuyu Bai, Ran Liu, Yingshuang Liu, Jiantao Qi, Jian Hou, and Dalei Zhang. Characterization of corrosion behavior and corrosion production property of 90-10 cupronickel welding joints in flowing seawater. Metals, 13:294, Feb 2023. URL: https://doi.org/10.3390/met13020294, doi:10.3390/met13020294. This article has 7 citations.

22. (huo2025modulatingheatinput pages 1-2): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

23. (grill2016combinatorialelectrodepositionof pages 3-4): Carina Daniela Grill, Jan Philipp Kollender, and Achim Walter Hassel. Combinatorial electrodeposition of cobalt-copper material libraries. Journal of The Electrochemical Society, 163:D3069-D3075, Jan 2016. URL: https://doi.org/10.1149/2.0101612jes, doi:10.1149/2.0101612jes. This article has 14 citations and is from a peer-reviewed journal.

24. (grill2016combinatorialelectrodepositionof pages 2-3): Carina Daniela Grill, Jan Philipp Kollender, and Achim Walter Hassel. Combinatorial electrodeposition of cobalt-copper material libraries. Journal of The Electrochemical Society, 163:D3069-D3075, Jan 2016. URL: https://doi.org/10.1149/2.0101612jes, doi:10.1149/2.0101612jes. This article has 14 citations and is from a peer-reviewed journal.

25. (decost2022towardsautomateddesign pages 1-4): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

26. (decost2022towardsautomateddesign pages 10-13): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

27. (heyne2026qualificationofproxy pages 2-4): Annica Heyne, Mert Ozan, Ahmad Rashid Hazem, and Ozlem Ozcan. Qualification of proxy experiments for accelerated electrochemical testing in self-driving labs. Analytical and Bioanalytical Chemistry, 418:5345-5360, Jun 2026. URL: https://doi.org/10.1007/s00216-026-06609-9, doi:10.1007/s00216-026-06609-9. This article has 1 citations and is from a peer-reviewed journal.

28. (heyne2026qualificationofproxy pages 8-11): Annica Heyne, Mert Ozan, Ahmad Rashid Hazem, and Ozlem Ozcan. Qualification of proxy experiments for accelerated electrochemical testing in self-driving labs. Analytical and Bioanalytical Chemistry, 418:5345-5360, Jun 2026. URL: https://doi.org/10.1007/s00216-026-06609-9, doi:10.1007/s00216-026-06609-9. This article has 1 citations and is from a peer-reviewed journal.

29. (takaloo2011corrosionbehaviorof pages 3-5): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 43 citations and is from a peer-reviewed journal.
