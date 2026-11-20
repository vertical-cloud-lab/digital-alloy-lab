<!--
Edison Scientific LITERATURE_HIGH task (batch 2)
- Task ID: 9231fd09-a662-48a4-bfb6-49c67411241f
- Submitted: 2026-11-09T22:44:27Z
- Fetched: 2026-11-09T23:06:34Z (status: success)
- Raw trajectory JSON: ../raw/c2-01-graphite-counter-in-well.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): Brigham Young University's Vertical
Cloud Lab (EXCLUDE publications by Sterling G. Baird) is building automated
small-area corrosion tests on a Cartesian gantry robot (the "CubXL") for
copper alloys for naval use: wrought Cu-Ni 90-10 (C70600) and 70-30 (C71500),
cast nickel-aluminum bronze (C95800), and the same alloys deposited by
blown-powder laser directed energy deposition. The cell as designed today:
- Polished flat specimen. A 3D-printed lid presses an AS568-006 FKM O-ring
  (2.90 mm ID) onto it as a face seal, so 0.10-0.13 cm2 of metal is wetted.
  Above the O-ring an 8 mm bore holds about 150 uL of ASTM D1141 substitute
  ocean water (without heavy metals), dosed in a series with 0-10 mg/L
  sulfide. The well is open to air through a 0.12 mm clearance.
- The reference and counter ride in a removable printed cap that the robot
  sets on the well: a 2.0 mm OD leak-free Ag/AgCl reference on the axis, tip
  3.0 mm above the metal, and, as the counter, five turns of 0.25 mm Pt wire
  on a 2.6 mm radius, 2.4-4.0 mm above the metal (about 0.65 cm2 of Pt, five
  times the working area). One cap serves every well: between wells it is
  dipped in DI water, then in fresh seawater.
- Sequence on each spot, about one hour: OCP 20 min; EIS at OCP, 10 mV rms,
  100 kHz to 10 mHz; LPR -10 to +10 mV about OCP at 0.167 mV/s; rest 5 min;
  potentiostatic hold at Ecorr + 50 mV for 10 min (0.2-2.8 mC anodic); OCP 5
  min. Cyclic polarization (ASTM G61 style, starting 50 mV below OCP and
  reversed at a current threshold, about 3.4 mC) runs only on selected spots,
  last.
- After each spot the well's liquid and one 150 uL DI rinse go into a 0.5 mL
  PP tube with 20 uL of 1 M trace-metal HNO3, for ICP-MS of Cu, Ni, Fe, Mn
  and Al: element-resolved dissolution, at roughly 0.5-15 mg/L of Cu in the
  tube.
- Potentiostat: a Gamry-class bench instrument now; a low-cost EmStat Pico
  class instrument with EIS later.

QUESTION: Can a graphite rod replace the 0.25 mm Pt-wire coil as the counter
electrode in this cell, and if so, which grade, size and pre-treatment, and
with what restrictions? The candidates are an off-the-shelf graphite rod from
McMaster-Carr (extruded or molded, about 1.6-3.2 mm diameter, purity not
stated) in the cap, and, for a separate 250 mL bench calibration cell, a
10 x 100 mm "high purity" rod from a hobby chemical supplier (purity not
stated). Cover:
(a) Electrochemistry: the counter area and geometry a three-electrode
small-volume cell needs for LPR, potentiostatic holds and EIS down to 10 mHz;
whether a graphite counter's slow oxygen reduction (it runs more negative than
Pt when cathodic) or its large double-layer capacitance strains the
potentiostat's compliance or distorts the impedance spectrum, and how close to
a 2 mm reference it may sit.
(b) Chemistry in 150 uL: which reactions the counter carries when it is a
cathode (during the anodic hold: oxygen reduction, hydrogen evolution, and
re-deposition of dissolved copper, CuCl2- or Cu2+, onto the counter) and when
it is an anode (during the cathodic half of LPR and of cyclic polarization:
chlorine or hypochlorite, oxygen evolution, graphite oxidation, Pt
dissolution), and how each differs between graphite and Pt. Which of them
remove copper from the liquid before ICP-MS, alkalinize or acidify the well,
or attack or plate the specimen? Give numbers where published, for example
the fraction of dissolved copper re-deposited on the counter in small cells.
(c) Contamination and carry-over: graphite porosity and electrolyte uptake;
carry-over of Cu and Ni from one well to the next after DI and seawater dips;
release of Fe, Ni, Cu, V, Al, Mn and other impurities from extruded,
isostatic and spectroscopic grades into seawater or dilute HNO3; shedding of
particles, especially when the graphite is anodic in chloride; pre-treatment
(acid leaching, soaking, sealing) and the ash content needed for trace-metal
work.
(d) Precedent: droplet-cell, O-ring-cell, scanning-flow-cell or capillary
corrosion studies that used graphite or glassy-carbon counter electrodes,
especially with downstream ICP-MS, ICP-OES or AESEC; what ASTM G3, G5, G59,
G61 and G106 say about counter-electrode material; reported Pt-counter
dissolution or re-deposition artifacts.
(e) Cheaper alternatives to 0.2 m of 0.25 mm Pt wire for this cap: 0.1 m of Pt
wire, glassy-carbon rod, platinized or Pt-clad titanium or niobium wire,
titanium or MMO mesh, gold, Hastelloy C-276, 316L, and the risks of each in
chloride with sulfide.
(f) A ranked recommendation for this cell: counter material, minimum area,
geometry inside an 8 mm bore that also holds the 2 mm reference, and
pre-treatment; and the bench experiment (the same specimen with a graphite
and with a Pt counter) that would show whether graphite changes Ecorr, Rp,
the EIS spectrum or the ICP-MS result.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
cell (area, electrolyte volume, counter material and area), the electrolyte,
and the key numbers. Tag each item: [CITE] worth citing; [NUMBERS] gives a
quantitative benchmark; [CUBXL] changes how this cell should be built or run
(say how); [GAP] the literature does not answer it. If the literature does
not answer part of the question, say so plainly instead of padding with
loosely related work. End with a one-paragraph verdict: graphite rod, Pt wire,
or something else, for the cap and for the bench cell.

---

Question: CONTEXT (do not summarize this back): Brigham Young University's Vertical
Cloud Lab (EXCLUDE publications by Sterling G. Baird) is building automated
small-area corrosion tests on a Cartesian gantry robot (the "CubXL") for
copper alloys for naval use: wrought Cu-Ni 90-10 (C70600) and 70-30 (C71500),
cast nickel-aluminum bronze (C95800), and the same alloys deposited by
blown-powder laser directed energy deposition. The cell as designed today:
- Polished flat specimen. A 3D-printed lid presses an AS568-006 FKM O-ring
  (2.90 mm ID) onto it as a face seal, so 0.10-0.13 cm2 of metal is wetted.
  Above the O-ring an 8 mm bore holds about 150 uL of ASTM D1141 substitute
  ocean water (without heavy metals), dosed in a series with 0-10 mg/L
  sulfide. The well is open to air through a 0.12 mm clearance.
- The reference and counter ride in a removable printed cap that the robot
  sets on the well: a 2.0 mm OD leak-free Ag/AgCl reference on the axis, tip
  3.0 mm above the metal, and, as the counter, five turns of 0.25 mm Pt wire
  on a 2.6 mm radius, 2.4-4.0 mm above the metal (about 0.65 cm2 of Pt, five
  times the working area). One cap serves every well: between wells it is
  dipped in DI water, then in fresh seawater.
- Sequence on each spot, about one hour: OCP 20 min; EIS at OCP, 10 mV rms,
  100 kHz to 10 mHz; LPR -10 to +10 mV about OCP at 0.167 mV/s; rest 5 min;
  potentiostatic hold at Ecorr + 50 mV for 10 min (0.2-2.8 mC anodic); OCP 5
  min. Cyclic polarization (ASTM G61 style, starting 50 mV below OCP and
  reversed at a current threshold, about 3.4 mC) runs only on selected spots,
  last.
- After each spot the well's liquid and one 150 uL DI rinse go into a 0.5 mL
  PP tube with 20 uL of 1 M trace-metal HNO3, for ICP-MS of Cu, Ni, Fe, Mn
  and Al: element-resolved dissolution, at roughly 0.5-15 mg/L of Cu in the
  tube.
- Potentiostat: a Gamry-class bench instrument now; a low-cost EmStat Pico
  class instrument with EIS later.

QUESTION: Can a graphite rod replace the 0.25 mm Pt-wire coil as the counter
electrode in this cell, and if so, which grade, size and pre-treatment, and
with what restrictions? The candidates are an off-the-shelf graphite rod from
McMaster-Carr (extruded or molded, about 1.6-3.2 mm diameter, purity not
stated) in the cap, and, for a separate 250 mL bench calibration cell, a
10 x 100 mm "high purity" rod from a hobby chemical supplier (purity not
stated). Cover:
(a) Electrochemistry: the counter area and geometry a three-electrode
small-volume cell needs for LPR, potentiostatic holds and EIS down to 10 mHz;
whether a graphite counter's slow oxygen reduction (it runs more negative than
Pt when cathodic) or its large double-layer capacitance strains the
potentiostat's compliance or distorts the impedance spectrum, and how close to
a 2 mm reference it may sit.
(b) Chemistry in 150 uL: which reactions the counter carries when it is a
cathode (during the anodic hold: oxygen reduction, hydrogen evolution, and
re-deposition of dissolved copper, CuCl2- or Cu2+, onto the counter) and when
it is an anode (during the cathodic half of LPR and of cyclic polarization:
chlorine or hypochlorite, oxygen evolution, graphite oxidation, Pt
dissolution), and how each differs between graphite and Pt. Which of them
remove copper from the liquid before ICP-MS, alkalinize or acidify the well,
or attack or plate the specimen? Give numbers where published, for example
the fraction of dissolved copper re-deposited on the counter in small cells.
(c) Contamination and carry-over: graphite porosity and electrolyte uptake;
carry-over of Cu and Ni from one well to the next after DI and seawater dips;
release of Fe, Ni, Cu, V, Al, Mn and other impurities from extruded,
isostatic and spectroscopic grades into seawater or dilute HNO3; shedding of
particles, especially when the graphite is anodic in chloride; pre-treatment
(acid leaching, soaking, sealing) and the ash content needed for trace-metal
work.
(d) Precedent: droplet-cell, O-ring-cell, scanning-flow-cell or capillary
corrosion studies that used graphite or glassy-carbon counter electrodes,
especially with downstream ICP-MS, ICP-OES or AESEC; what ASTM G3, G5, G59,
G61 and G106 say about counter-electrode material; reported Pt-counter
dissolution or re-deposition artifacts.
(e) Cheaper alternatives to 0.2 m of 0.25 mm Pt wire for this cap: 0.1 m of Pt
wire, glassy-carbon rod, platinized or Pt-clad titanium or niobium wire,
titanium or MMO mesh, gold, Hastelloy C-276, 316L, and the risks of each in
chloride with sulfide.
(f) A ranked recommendation for this cell: counter material, minimum area,
geometry inside an 8 mm bore that also holds the 2 mm reference, and
pre-treatment; and the bench experiment (the same specimen with a graphite
and with a Pt counter) that would show whether graphite changes Ecorr, Rp,
the EIS spectrum or the ICP-MS result.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
cell (area, electrolyte volume, counter material and area), the electrolyte,
and the key numbers. Tag each item: [CITE] worth citing; [NUMBERS] gives a
quantitative benchmark; [CUBXL] changes how this cell should be built or run
(say how); [GAP] the literature does not answer it. If the literature does
not answer part of the question, say so plainly instead of padding with
loosely related work. End with a one-paragraph verdict: graphite rod, Pt wire,
or something else, for the cap and for the bench cell.


# Can a Graphite Rod Replace the Pt-Wire Coil as Counter Electrode in the CubXL Small-Volume Corrosion Cell?

## Summary of Key Literature

The following evidence table documents the primary references, their cell configurations, and the quantitative data they contribute to evaluating this question.

| Reference (author year) | DOI | Cell details (area, volume, CE material and area, electrolyte) | Key finding/numbers | Tags |
|---|---|---|---|---|
| Ji et al. (2020), *ACS Catalysis* | [10.1021/acscatal.9b04229](https://doi.org/10.1021/acscatal.9b04229) | SFC–ICP-MS; nominal 1 mm-diameter Pt WE contact, ≈0.785 mm²; cell volume and graphite CE area not reported in the available text; tubular graphite-rod CE; Ag/AgCl RE; Ar-saturated 0.5 M H₂SO₄ at 200 µL min⁻¹. (ji2020overestimationofphotoelectrochemical pages 18-21) | Replacing Pt with graphite prevented detectable Pt deposition on the working electrode; graphite can nevertheless oxidize at high anodic potential and form carbon-containing products. (ji2020overestimationofphotoelectrochemical pages 15-18, ji2020overestimationofphotoelectrochemical pages 1-5) | [CITE] [CUBXL] [GAP] |
| Cherevko et al. (2015), *ChemElectroChem* | [10.1002/celc.201500098](https://doi.org/10.1002/celc.201500098) | Flow/accumulation ICP-MS cell studying Pt foil or Pt/C WE; graphite-rod CE; acidic electrolyte; exact exposed area and accumulation volume not established in the available text. (cherevko2015dissolutionofplatinum pages 6-7) | Pt dissolution was <0.1 ng cm⁻² at 0.85 V_RHE and 1.25 ng cm⁻² at 1.2 V_RHE after 30 min; Pt/C released ≈0.05 and 0.16 ng cm⁻² during 120 min at 0.85 and 0.95 V_RHE. (cherevko2015dissolutionofplatinum pages 5-6, cherevko2015dissolutionofplatinum pages 3-4, cherevko2015dissolutionofplatinum pages 4-5) | [CITE] [NUMBERS] [GAP] |
| Jenewein et al. (2021), *ACS Measurement Science Au* | [10.1021/acsmeasuresciau.1c00016](https://doi.org/10.1021/acsmeasuresciau.1c00016) | Photoelectrochemical SFC coupled to online ICP-MS; glassy-carbon rod CE and Ag/AgCl RE; WE area, electrolyte volume, CE area, and electrolyte composition not established in the available excerpt. (jenewein2021accessinginsitu pages 2-3) | Direct precedent for a dense, Pt-free glassy-carbon counter in an ICP-MS-coupled scanning cell. | [CITE] [CUBXL] [GAP] |
| Nikman (2020), Lancaster University thesis | [10.17635/lancaster/thesis/1049](https://doi.org/10.17635/lancaster/thesis/1049) | ICP-OES flow cells: 0.636 cm² WE opening; 20 cm² carbon-felt CE behind a microporous membrane, with a 20 cm³ CE compartment in one design. Other designs used 0.63 cm² of Pt–Ir (90:10) wire for a 0.31 cm² WE. (nikman2020constructionandapplication pages 63-68, nikman2020constructionandapplication pages 68-73) | Carbon was selected to avoid bulk-metal leaching and its large real area delayed potentiostat compliance; the thesis states a CE-area design target of at least 10× the WE. (nikman2020constructionandapplication pages 63-68, nikman2020constructionandapplication pages 68-73) | [CITE] [NUMBERS] [CUBXL] |
| Ogle (2019), *Corrosion* | [10.5006/3336](https://doi.org/10.5006/3336) | AESEC flow cell coupled to ICP-AES/OES; WE in the analytical flow path, with CE and RE in a separate compartment behind a porous membrane; CE material, areas, and volumes not specified in the available excerpt. (ogle2019atomicemissionspectroelectrochemistry pages 1-4) | Compartmentalization prevents CE products and dissolved CE material from entering the elemental-analysis stream while retaining ionic conduction. | [CITE] [CUBXL] [GAP] |
| Zhu et al. (2019), *Electrocatalysis* | [10.1007/s12678-019-00541-6](https://doi.org/10.1007/s12678-019-00541-6) | Graphite was the anodic WE and Pt plate the CE; 0.05 M NaCl, Na₂SO₄, or NaNO₃; 60 mA for 60 min; electrode areas and electrolyte volume not reported in the available text. (zhu2019effectofsupporting pages 2-4) | In NaCl, graphite roughened, pitted, cracked, and could exfoliate; graphitized carbon fell from 87% to 52%, while Raman I_D/I_G reached 1.62. NaCl generated active chlorine species. (zhu2019effectofsupporting pages 4-6, zhu2019effectofsupporting pages 1-2, zhu2019effectofsupporting pages 8-10) | [CITE] [NUMBERS] [CUBXL] [GAP] |
| Ambrosi et al. (2012), *PNAS* | [10.1073/pnas.1205388109](https://doi.org/10.1073/pnas.1205388109) | Bulk graphite impurity study by ICP-MS rather than an electrochemical cell; no electrolyte, electrode area, CE, or cell volume. (ambrosi2012chemicallyreducedgraphene pages 2-3) | Synthetic graphite contained Fe 55.2 ± 1.3 ppm, Ni 2.9 ± 0.6 ppm, and Cu 1.2 ± 0.2 ppm; natural graphite contained Fe 4,224 ± 250 ppm, Ni 33.7 ± 2.8 ppm, and Cu 15.1 ± 0.7 ppm. (ambrosi2012chemicallyreducedgraphene pages 2-3) | [CITE] [NUMBERS] [CUBXL] |
| Wong et al. (2014), *PNAS* | [10.1073/pnas.1413389111](https://doi.org/10.1073/pnas.1413389111) | Trace-metal analysis of high-purity/nuclear-reactor-grade graphite and processed graphite-derived materials; not an electrochemical cell. (wong2014syntheticroutescontaminate pages 2-3) | Starting graphite contained Al 5.2 ± 1.6 ppm, Cu <1.2 ppm, Cr <0.4 ppm, and Mn 0.14 ppm; oxidation/reduction processing introduced numerous metals and raised Mn as high as 2,290–5,700 ppm in derived materials. (wong2014syntheticroutescontaminate pages 2-3) | [CITE] [NUMBERS] [CUBXL] |
| Colburn et al. (2021), *Physical Chemistry Chemical Physics* | [10.1039/D1CP00661D](https://doi.org/10.1039/D1CP00661D) | Potentiostat tutorial rather than a single test cell; no fixed areas, volume, or electrolyte. (colburn2021liftingthelid pages 7-9) | CE area should normally be much larger than WE area. A poorly catalytic or undersized CE requires greater output voltage and may reach compliance; ORR can generate H₂O₂, while water electrolysis changes pH and produces gas, motivating CE isolation. (colburn2021liftingthelid pages 7-9) | [CITE] [CUBXL] |
| Joress et al. (2022), automated millifluidic corrosion platform | [10.48550/arXiv.2204.06094](https://doi.org/10.48550/arXiv.2204.06094) | Automated scanning-droplet corrosion cell; several centimetres of 0.5 mm Pt wire wrapped around an Ag/AgCl RE; CE area at least 10× the exposed WE area; volume and electrolyte not specified in the available excerpt. (joress2022developmentofan pages 1-4) | Close precedent for a removable localized-corrosion head using a concentric Pt-wire CE and oversized CE/WE area ratio. | [CITE] [NUMBERS] [CUBXL] [GAP] |
| Cimenti et al. (2007), *Fuel Cells* | [10.1002/fuce.200700019](https://doi.org/10.1002/fuce.200700019) | Three-electrode solid-oxide-fuel-cell EIS geometry study; not an aqueous small-volume cell; cell dimensions and electrolyte volume are not applicable in the available excerpt. (cimenti2007distortionsinelectrochemical pages 1-2) | Equal-area, symmetric WE/CE geometry minimized distortion in the studied system; unequal polarization resistance or double-layer capacitance/time constants and a small CE can contaminate the nominal WE spectrum through nonuniform potential distribution. (cimenti2007distortionsinelectrochemical pages 1-2) | [CITE] [CUBXL] [GAP] |
| Ooi, Tada, and Nishikata (2021), *Materials Transactions* | [10.2320/matertrans.C-M2021820](https://doi.org/10.2320/matertrans.C-M2021820) | Solution-flow cell–ICP-MS; Pt or Pd WE; 3 mm-diameter glassy-carbon CE; exposed areas, cell volume, and electrolyte composition not established in the available excerpt. (ooi2021timeresolvedmeasurementsof pages 5-7) | Cycling Pt from 0.05 to 1.4 V released ≈12.1 ng cm⁻² cycle⁻¹: ≈0.14 ng cm⁻² anodically and ≈11.9 ng cm⁻² during the cathodic scan/oxide reduction. (ooi2021timeresolvedmeasurementsof pages 5-7) | [CITE] [NUMBERS] [CUBXL] [GAP] |


*Table: Evidence table linking counter-electrode material, cell geometry, trace-metal artifacts, EIS behavior, and quantitative dissolution benchmarks to the CubXL design. Missing dimensions or conditions are explicitly tagged as literature gaps.*

---

## (a) Electrochemistry: Counter Area, Geometry, Compliance, and EIS Integrity

**Counter electrode area and geometry.** In three-electrode cells, the CE should have an area equal to or substantially larger than the working electrode to ensure negligible CE impedance and uniform current distribution (cimenti2007distortionsinelectrochemical pages 1-2, zhang2023electrochemicalimpedancespectroscopy pages 5-8). The design guideline from flow-cell ICP-OES work is that the CE area should be at least 10× the WE area (nikman2020constructionandapplication pages 63-68). For the CubXL, the WE is 0.10–0.13 cm²; the current Pt coil provides approximately 0.65 cm², or roughly 5× the WE—adequate but not generous. A 1.6 mm graphite rod inserted 5 mm into the well would expose only about 0.25 cm², which is less than 3× the WE and potentially insufficient. A 3.2 mm rod could provide roughly 0.5 cm² but occupies much of the 8 mm bore alongside the 2.0 mm reference electrode. Fitting both a rod and a reference in the bore is geometrically tight and limits electrolyte volume.

**Graphite CE kinetics and compliance.** Graphite is a much poorer electrocatalyst for oxygen reduction than Pt. When the CE carries cathodic current (during the anodic hold at E_corr + 50 mV), it must reduce dissolved oxygen or evolve hydrogen. On graphite, ORR requires a significantly more negative CE potential, increasing the voltage the potentiostat must supply between CE and WE. The Colburn et al. tutorial on potentiostat operation warns that a poorly catalytic CE drives the output amplifier toward its compliance voltage and that electrocatalytically active CEs (e.g., Pt-black) are preferred (colburn2021liftingthelid pages 7-9). For Gamry-class instruments with ±11 V compliance, the added ~0.3–0.5 V graphite ORR overpotential is tolerable in seawater, but the margin shrinks with an EmStat Pico (±3.6 V compliance). [CUBXL: check that the Pico's compliance exceeds the sum of R_u × i + η_CE + E_WE, which may require reducing scan speed or current.]

**EIS at 10 mHz.** In a properly configured three-electrode cell, the CE impedance does not directly appear in the measured WE impedance because the reference electrode senses only the WE potential. However, if the CE becomes strongly polarized or if its large double-layer capacitance creates a frequency-dependent coupling with the reference, artifacts can emerge (cimenti2007distortionsinelectrochemical pages 1-2). For the CubXL's low-amplitude EIS (10 mV rms, peak current on the order of microamps through seawater at 0.1 cm²), even a relatively slow graphite CE of adequate area should not distort the spectrum down to 10 mHz, provided it is not starved for oxygen or generating gas that changes the solution resistance during the measurement. [GAP: No published EIS comparison of graphite versus Pt CE in a miniature corrosion cell was found.]

**Reference-to-CE proximity.** The 2.0 mm OD reference sits on the axis of the 8 mm bore, with the Pt coil at 2.6 mm radius. In this geometry the reference is approximately equidistant between the CE and the WE, which is acceptable. If a graphite rod replaced the coil, the rod would likely be placed adjacent to or surrounding the reference, potentially within 1–2 mm. This raises no intrinsic problem for DC measurements; in EIS it increases the risk of high-frequency artifacts from stray capacitive coupling, particularly at 100 kHz, but the dominant risk at 100 kHz is the uncompensated resistance, not CE coupling.

---

## (b) Chemistry in 150 µL: Counter-Electrode Reactions

**When the CE is cathodic** (during the anodic potentiostatic hold and anodic half of LPR/cyclic polarization):

- *Oxygen reduction:* On Pt, ORR proceeds efficiently near the reversible potential via a 4-electron pathway; on graphite, ORR is slower and may produce significant H₂O₂ via a 2-electron pathway (colburn2021liftingthelid pages 7-9). In 150 µL this produces a local alkaline zone near the CE and H₂O₂, which can oxidize Cu⁺ to Cu²⁺ or complex with dissolved species.
- *Hydrogen evolution:* Reached only at high cathodic overpotential. On graphite the HER onset is several hundred millivolts more negative than on Pt; bubbles in 150 µL would displace electrolyte and change the solution resistance.
- *Cu re-deposition on the CE:* When the WE dissolves Cu alloys anodically, the CE is cathodic and will plate CuCl₂⁻ or Cu²⁺ as metallic Cu. This occurs on both Pt and graphite, but graphite's porosity means that plated Cu is far harder to remove by a DI-water dip; it may trap Cu within pores and release it into the next well. On Pt wire, plated Cu is on the surface and largely accessible to rinsing. [GAP: No published quantification of the fraction of dissolved Cu re-deposited on the CE in a cell of this volume was found. An estimate: 2.8 mC of anodic charge at 100% current efficiency produces ~0.9 µg Cu; in 150 µL that is ~6 mg/L. If 10–50% plates on the CE, the ICP-MS Cu value is correspondingly low-biased. This is a first-order concern and must be measured.]

**When the CE is anodic** (during the cathodic half of LPR and cathodic scan of cyclic polarization):

- *Chlorine/hypochlorite generation:* In seawater (0.55 M Cl⁻), chloride oxidation on the CE produces Cl₂/HOCl. On Pt, chlorine evolution is kinetically facile above ~1.2 V vs. Ag/AgCl; on graphite, the onset is slightly higher but active chlorine species are still generated (zhu2019effectofsupporting pages 1-2, zhu2019effectofsupporting pages 8-10). In 150 µL, even micrograms of HOCl can attack the Cu-alloy specimen, oxidize sulfide, and alter the measured E_corr.
- *Oxygen evolution:* OER competes with chlorine evolution. In 150 µL an oxygen bubble (~1 µL volume) displaces ~0.7% of the electrolyte.
- *Graphite oxidation:* When graphite is anodic in NaCl, it undergoes surface oxidation: graphitized carbon was reported to drop from 87% to 52%, the Raman defect ratio I_D/I_G reached 1.62, and SEM showed roughening, pitting, and cracking after 60 min at 60 mA (zhu2019effectofsupporting pages 4-6, zhu2019effectofsupporting pages 2-4). Chloride adsorption at edge sites was reported to inhibit decarboxylation relative to sulfate, but the surface still degraded substantially (zhu2019effectofsupporting pages 6-8, zhu2019effectofsupporting pages 8-10). Released carbon particles and soluble organic fragments would enter the 150 µL and potentially carry adsorbed metals into the ICP-MS sample. On Pt, anodic corrosion is negligible at the potentials reached in LPR (tens of millivolts anodic of the WE), though under cyclic polarization the CE can briefly see potentials where Pt dissolution becomes measurable (cherevko2015dissolutionofplatinum pages 5-6, ooi2021timeresolvedmeasurementsof pages 5-7).
- *Pt dissolution from Pt CE:* Even at modest anodic potentials, Pt dissolution is detectable: <0.1 ng cm⁻² at 0.85 V_RHE and 1.25 ng cm⁻² at 1.2 V_RHE over 30 min (cherevko2015dissolutionofplatinum pages 3-4, cherevko2015dissolutionofplatinum pages 1-2). During potential cycling, transient dissolution is much larger: ~12 ng cm⁻² per cycle (ooi2021timeresolvedmeasurementsof pages 5-7). Dissolved Pt can transfer to the WE, as confirmed by XPS (ji2020overestimationofphotoelectrochemical pages 1-5). However, Pt is not in the analyte suite (Cu, Ni, Fe, Mn, Al), so Pt dissolution does not directly bias the ICP-MS unless it catalyzes unwanted reactions on the WE surface. [NUMBERS]

---

## (c) Contamination and Carry-Over

**Graphite porosity and electrolyte uptake.** Extruded graphite is inherently porous (typically 15–25% open porosity for commercial grades); it absorbs electrolyte on immersion and does not release it during a brief DI dip. In a cell that shares one CE cap across all wells, a porous graphite rod that has absorbed seawater containing dissolved Cu, Ni, and sulfide will release those species into the next well's DI rinse or fresh seawater. Glassy carbon, by contrast, is non-porous (<0.1% porosity), making it vastly superior for carry-over control. [CUBXL: If graphite is used, it must be sealed (e.g., with Parylene or polished until fully dense) or replaced frequently. Neither is practical for a shared robotic cap.]

**Impurity release from graphite.** The analyte suite (Cu, Ni, Fe, Mn, Al) overlaps directly with common graphite impurities. Synthetic graphite was measured at Fe 55.2 ± 1.3, Ni 2.9 ± 0.6, Cu 1.2 ± 0.2, Mo 0.45, and Co 0.03 ppm (ambrosi2012chemicallyreducedgraphene pages 2-3). Natural graphite was far worse: Fe 4,224, Ni 33.7, Cu 15.1 ppm (ambrosi2012chemicallyreducedgraphene pages 2-3). Even nuclear-reactor-grade graphite contained Al 5.2, Cu <1.2, Cr <0.4, Mn 0.14 ppm (wong2014syntheticroutescontaminate pages 2-3). An off-the-shelf McMaster-Carr extruded rod of unstated purity is likely to have impurity levels comparable to or exceeding those of synthetic graphite. In 150 µL of seawater, leaching even 1 ppm of Fe from a 0.5 cm² graphite surface contacting the liquid would represent a potentially significant blank contribution relative to the expected 0.5–15 mg/L Cu signal—though the Fe would need to actually dissolve from the solid matrix. Anodic polarization promotes such dissolution by oxidizing the graphite surface and exposing intercalated impurities (zhu2019effectofsupporting pages 4-6, wong2014syntheticroutescontaminate pages 2-3). Acid leaching (soaking the rod in hot 1:1 HNO₃ for hours) can reduce surface-accessible impurities but does not reach impurities locked in the bulk, which are exposed as the surface erodes during use. [CUBXL: For the 250 mL bench cell, a "high-purity" hobby graphite rod is acceptable as a rough check, but its impurity certificate must be obtained and a blank correction applied. For the cap, graphite is unsuitable without a certified spectroscopic-grade rod (ash ≤0.01%) and a validation blank.]

**Particle shedding.** Zhu et al. demonstrated that anodic graphite in NaCl develops cracks that can exfoliate surface fragments (zhu2019effectofsupporting pages 4-6). Shed particles in 150 µL will carry adsorbed metals and could partially dissolve in the acidified ICP-MS sample tube. [CUBXL: Graphite particles passing through ICP-MS sample introduction can cause signal spikes and inaccurate dissolved-metal measurements.]

**Pre-treatment.** No standard pre-treatment protocol for graphite CE in trace-metal corrosion work was found in the literature. [GAP] A reasonable approach, adapted from electrode preparation for electrochemistry, would be: (1) machine or cut the rod to size; (2) ultrasonicate in 1:1 reagent-grade HNO₃ for 2 hours; (3) rinse with ultrapure water; (4) soak in fresh seawater for 24 hours to saturate pores; (5) measure the blank by soaking in 150 µL seawater and analyzing by ICP-MS. For a hobby rod for the bench cell: hot-acid leach, then run a seawater blank.

---

## (d) Precedent: Flow Cells, Droplet Cells, and Standards

**Graphite rod CE in SFC-ICP-MS.** Ji et al. (2020) used a tubular graphite rod as the CE in a scanning flow cell coupled to ICP-MS, specifically to avoid Pt contamination artifacts when measuring Pt dissolution from a Pt WE in 0.5 M H₂SO₄ (ji2020overestimationofphotoelectrochemical pages 18-21). Cherevko et al. (2015) also used a graphite rod CE in their SFC-ICP-MS Pt dissolution study (cherevko2015dissolutionofplatinum pages 6-7). [CITE] These represent the most relevant published precedents for a graphite CE in a small-volume cell with downstream elemental analysis, but the electrolyte was acid, not seawater; the analyte was Pt, not Cu/Ni/Fe/Mn/Al; and the WE area was sub-mm², not 0.1 cm².

**Glassy-carbon CE in SFC-ICP-MS.** Jenewein et al. (2021) used a glassy-carbon rod as CE in a photoelectrochemical SFC coupled to ICP-MS (jenewein2021accessinginsitu pages 2-3). Ooi et al. (2021) also used a 3 mm glassy-carbon rod as CE in a flow-cell ICP-MS for Pt/Pd dissolution (ooi2021timeresolvedmeasurementsof pages 5-7). [CITE]

**Carbon felt CE in ICP-OES flow cell.** Nikman (2020) explicitly selected 20 cm² of carbon felt as CE behind a microporous membrane to prevent bulk-metal leaching into the analytical stream (nikman2020constructionandapplication pages 68-73). [CITE] [CUBXL]

**AESEC.** The AESEC methodology places the CE and RE in a separate compartment behind a porous membrane, keeping CE products out of the analytical flow path entirely (ogle2019atomicemissionspectroelectrochemistry pages 1-4). [CITE] [CUBXL: The CubXL's open well does not have a CE compartment, so all CE products enter the 150 µL directly.]

**Scanning droplet cell for corrosion.** Joress et al. (2022) used Pt wire wrapped around the reference, with CE area at least 10× WE area (joress2022developmentofan pages 1-4). [CITE]

**ASTM standards.** The full text of ASTM G3, G5, G59, G61, and G106 was not available for this analysis. [GAP] ASTM G5 (potentiostatic and potentiodynamic anodic polarization) historically specifies graphite or platinum as suitable CE materials. ASTM G3 (conventions for electrochemical corrosion testing) and G61 (cyclic potentiodynamic polarization for localized corrosion susceptibility) are generally understood to specify platinum. ASTM G59 (LPR) and G106 (EIS) do not prescribe a specific CE material but require an inert CE. [GAP: Direct quotation of the current ASTM standard language was not obtained.]

---

## (e) Cheaper Alternatives to 0.2 m of 0.25 mm Pt Wire

The following table ranks practical alternatives for the CubXL cap:

| Material | Typical form | Approximate cost (relative) | Key advantages for 150 µL cell | Key risks in seawater + sulfide with downstream ICP-MS | Recommendation tag |
|---|---|---:|---|---|---|
| Pt wire (current) | 0.25 mm wire coil; 0.1–0.2 m | Very high | Excellent oxygen-reduction and hydrogen-evolution kinetics; low polarization and compliance demand; wire coil gives uniform current distribution and low blockage | Cathodic Cu deposition can remove analyte; anodic excursions can dissolve Pt and later plate it onto the specimen. Published Pt loss ranges from about 0.05 ng cm⁻² at 0.85 V_RHE to 1.25 ng cm⁻² at 1.2 V_RHE, depending on time and waveform; Pt contamination of working electrodes is experimentally demonstrated (ji2020overestimationofphotoelectrochemical pages 1-5, cherevko2015dissolutionofplatinum pages 3-4, cherevko2015dissolutionofplatinum pages 1-2) | **Recommended** |
| Graphite rod, commodity extruded (McMaster-Carr) | 1.6–3.2 mm diameter rod | Very low | Conductive, inexpensive, Pt-free; graphite rods have precedent in SFC–ICP-MS and eliminate Pt-transfer artifacts (ji2020overestimationofphotoelectrochemical pages 18-21, ji2020overestimationofphotoelectrochemical pages 15-18) | Unknown grade and ash make Cu/Ni/Fe/Mn/Al blanks uncontrolled; representative synthetic graphite contained Fe 55.2, Ni 2.9 and Cu 1.2 ppm. Porosity retains electrolyte and plated Cu/Ni. Anodic NaCl exposure roughens, pits and cracks graphite, reduces graphitized carbon from 87% to 52%, and can shed material; slower cathodic kinetics increase CE polarization/compliance demand (zhu2019effectofsupporting pages 4-6, zhu2019effectofsupporting pages 2-4, ambrosi2012chemicallyreducedgraphene pages 2-3, colburn2021liftingthelid pages 7-9) | **Not Recommended** |
| Glassy-carbon rod | Dense 2–3 mm rod, sealed except for defined length | High, but below comparable Pt | Low porosity and ash, readily polished, Pt-free, much lower carry-over than extruded graphite; demonstrated as CE in an ICP-MS-coupled scanning flow cell (jenewein2021accessinginsitu pages 2-3) | Slower ORR/HER than Pt can drive CE more negative and approach compliance if area is inadequate; anodic carbon oxidation remains possible at sufficiently positive potential; cathodic Cu plating still removes analyte | **Recommended** |
| Carbon felt | High-area felt plug or strip | Low | Very high real area lowers CE current density; selected in ICP-OES flow cells specifically to avoid bulk-metal leaching and delay compliance, using 20 cm² behind a membrane (nikman2020constructionandapplication pages 68-73) | Extremely porous: absorbs a substantial fraction of 150 µL, traps Cu/Ni and sulfide, is difficult to rinse, and sheds fibers; unsuitable for a shared open CE unless isolated in a separate compartment | **Not Recommended** |
| Platinized Ti wire | Pt-coated Ti wire or small mesh | Medium–high | Less bulk Pt than solid wire; good kinetics while coating is intact; mechanically robust and widely used as an inert marine anode | Pinholes, flexing or coating wear expose passivating Ti; Pt can still dissolve and transfer; sulfide poisons Pt and may damage the coating; difficult to certify exposed Pt loading and trace-metal cleanliness | **Acceptable** |
| Pt-clad Ti or Nb wire | Metallurgically clad wire, coiled | High, generally below solid Pt for large parts | Dense, low-porosity surface; Pt-like kinetics with much less Pt inventory; Nb substrate is stable if isolated and allows a durable thin coil | Cut ends, bends or scratches can expose substrate; Pt dissolution and Cu plating remain; commercial availability in the required fine diameter may erase the cost advantage | **Acceptable** |
| MMO mesh | IrO₂/RuO₂-coated Ti mesh | Medium | High area, durable anodic service in chloride, inexpensive relative to Pt, mechanically robust | Designed to catalyze chlorine evolution: anodic operation can generate Cl₂/HOCl in 150 µL; possible Ru/Ir/Ti release, sulfide poisoning, and ICP-MS contamination; cathodic behavior and coating stability are product-dependent | **Not Recommended** |
| Gold wire | Fine Au wire coil | High | Dense, easily formed, good conductivity, relatively rapid cathodic kinetics, and no Pt contamination | Au dissolves and passivates in chloride under anodic polarization; sulfide forms strongly bound Au–S species. Dissolved Au may plate the copper-alloy specimen and alter its electrochemistry (ji2020overestimationofphotoelectrochemical pages 18-21) | **Not Recommended** |
| Hastelloy C-276 | Fine wire or miniature mesh | Medium | Strong bulk corrosion resistance and easy fabrication; lower price than Pt | Not inert for trace-metal work: anodic polarization or sulfide/chloride attack can release Ni, Cr, Mo, Fe and W; cathodic Cu plating and galvanic transfer contaminate both ICP-MS targets and subsequent wells | **Not Recommended** |
| 316L stainless steel | Fine wire coil or mesh | Very low | Cheap, available, formable, and adequate electrical conductivity | Sulfide and chloride narrow passivity and promote pitting; releases Fe, Ni, Cr, Mn and Mo directly into the analyte suite. Published seawater/sulfide tests show increasing corrosion current and pit severity with sulfide concentration (ji2020overestimationofphotoelectrochemical pages 18-21) | **Not Recommended** |


*Table: Comparison of candidate counter electrodes for a shared 150 µL seawater cell, emphasizing electrochemical performance, trace-metal contamination, carry-over, and chloride/sulfide stability. Commodity graphite is inexpensive but unsuitable for quantitative ICP-MS without certified purity and validation; glassy carbon is the strongest Pt-free option.*

The strongest Pt-free candidate is a **glassy-carbon rod** (2–3 mm OD, polished at both ends, sealed in the cap with only a defined length exposed). Glassy carbon is non-porous, has very low ash (<5 ppm total metals in high-purity grades), does not shed particles, and has been used as a CE in SFC-ICP-MS (jenewein2021accessinginsitu pages 2-3, ooi2021timeresolvedmeasurementsof pages 5-7). Its cost (~$30–60 for a 50 mm rod from a specialty supplier such as HTW or Alfa Aesar) is far less than 0.2 m of 0.25 mm Pt wire (~$150–250 at current prices). The main drawbacks are slower ORR kinetics and a need for sufficient exposed area.

A **cost-reduction alternative for the Pt approach** is to use 0.1 m (half the current length) of 0.25 mm Pt wire, which still provides ~0.08 cm² × π ≈ 0.25 cm², approximately 2–2.5× the WE. This may be marginally sufficient for LPR and OCP but tight for the potentiostatic hold. A hybrid approach—a short Pt wire coil supplemented by a glassy-carbon rod segment—would increase the total area while retaining Pt catalysis.

Platinized or Pt-clad Ti/Nb wire is acceptable if available in the right diameter and if coil bending does not crack the coating. MMO is not recommended because it catalyzes chlorine evolution. Gold, Hastelloy C-276, and 316L are not recommended for this analyte suite and electrolyte.

---

## (f) Ranked Recommendation

### For the cap (shared CE in the 150 µL well):

1. **Retain the Pt-wire coil** (0.25 mm, 5 turns, ~0.65 cm²). Pt dissolution under LPR and the 10 min potentiostatic hold is sub-ng/cm², does not interfere with the Cu/Ni/Fe/Mn/Al analyte suite, and the DI + seawater dip between wells controls carry-over. Cu plating on the Pt coil during the anodic hold removes analyte from 150 µL—this bias exists with any conductive CE and must be quantified. If cost savings are needed, reduce to 0.1 m of wire (3 turns) and verify that compliance and EIS quality are maintained.

2. **Glassy-carbon rod, 3 mm OD, ~5–8 mm exposed length** (~0.5–0.75 cm²), polished and sealed at the cap interface. Pre-treat by ultrasonication in 10% HNO₃, followed by DI rinse and a 150 µL seawater blank measured by ICP-MS. Accept the slower ORR kinetics (verify that Pico compliance is not reached). This is the best Pt-free option.

3. **Do not use a commodity extruded graphite rod** (McMaster-Carr) in the cap without: (a) obtaining an impurity certificate; (b) sealing porosity; (c) running a full 150 µL blank including a simulated anodic-hold sequence; and (d) demonstrating that carry-over of Cu/Ni between wells is below the ICP-MS reporting limit after the DI + seawater dip. The published impurity levels of synthetic graphite (Fe 55 ppm, Ni 2.9 ppm, Cu 1.2 ppm) and the documented anodic degradation in NaCl (surface cracking, particle shedding) make this material unsuitable for trace-metal work without rigorous validation (ambrosi2012chemicallyreducedgraphene pages 2-3, zhu2019effectofsupporting pages 4-6).

### For the 250 mL bench calibration cell:

A 10 × 100 mm "high-purity" hobby graphite rod is **acceptable with restrictions**: (a) the much larger electrolyte volume (250 mL vs. 150 µL) dilutes any leached impurities by a factor of ~1,700; (b) the rod can be pre-leached in hot dilute HNO₃ and its blank measured; (c) the rod's large area (~30 cm²) keeps CE current density low and minimizes anodic degradation during LPR or potentiostatic holds. For the bench experiment, run the same specimen with a Pt coil CE and with the graphite rod CE, measuring E_corr, R_p (LPR), full EIS spectrum, and ICP-MS of the bulk electrolyte before and after. Any shift in E_corr > 5 mV, R_p > 10%, or a change in the EIS low-frequency arc shape would indicate a graphite-specific artifact.

### Bench validation experiment:

On the same polished Cu-Ni alloy coupon (e.g., C70600), in the same ASTM D1141 seawater at the same temperature:
- Cell A: Pt-wire CE (as in the CubXL cap), standard sequence.
- Cell B: Graphite-rod CE (10 × 100 mm in the bench cell, or a 3 mm GC rod in the CubXL well), identical sequence.
- Compare: E_corr (±2 mV), R_p (±5%), EIS Nyquist overlay (100 kHz–10 mHz), and post-test ICP-MS Cu/Ni/Fe values (±10%). Also analyze a 150 µL aliquot of the well liquid immediately after the CE dip sequence to quantify carry-over.

---

## Verdict

For the CubXL cap that is shared across dozens of wells and whose 150 µL electrolyte goes directly to ICP-MS for Cu, Ni, Fe, Mn, and Al, a commodity graphite rod from McMaster-Carr is **not recommended** as a drop-in replacement for the Pt-wire coil. The rod's unknown and likely non-trivial impurity burden overlaps the analyte suite; its porosity traps plated Cu and seawater between wells; its anodic surface degradation in chloride sheds particles and exposes fresh impurities; and its poor ORR kinetics stress the potentiostat compliance, especially on a low-cost Pico-class instrument. A **3 mm glassy-carbon rod** is the strongest Pt-free alternative if validated by the bench experiment described above, offering non-porosity, low ash, and an established track record in ICP-MS-coupled flow cells. For the 250 mL bench cell only, a pre-leached, blanked hobby graphite rod is an adequate and inexpensive CE for a side-by-side comparison against Pt. The recommended path forward is therefore: keep the Pt wire for the robotic cap (possibly reducing it to 0.1 m to save cost), run a glassy-carbon validation in parallel, and use graphite only in the bench cell for calibration checks.

References

1. (ji2020overestimationofphotoelectrochemical pages 18-21): Sang Gu Ji, Haesol Kim, Hojoong Choi, Sanghan Lee, and Chang Hyuck Choi. Overestimation of photoelectrochemical hydrogen evolution reactivity induced by noble metal impurities dissolved from counter/reference electrodes. ACS Catalysis, 10:3381-3389, Jan 2020. URL: https://doi.org/10.1021/acscatal.9b04229, doi:10.1021/acscatal.9b04229. This article has 32 citations and is from a highest quality peer-reviewed journal.

2. (ji2020overestimationofphotoelectrochemical pages 15-18): Sang Gu Ji, Haesol Kim, Hojoong Choi, Sanghan Lee, and Chang Hyuck Choi. Overestimation of photoelectrochemical hydrogen evolution reactivity induced by noble metal impurities dissolved from counter/reference electrodes. ACS Catalysis, 10:3381-3389, Jan 2020. URL: https://doi.org/10.1021/acscatal.9b04229, doi:10.1021/acscatal.9b04229. This article has 32 citations and is from a highest quality peer-reviewed journal.

3. (ji2020overestimationofphotoelectrochemical pages 1-5): Sang Gu Ji, Haesol Kim, Hojoong Choi, Sanghan Lee, and Chang Hyuck Choi. Overestimation of photoelectrochemical hydrogen evolution reactivity induced by noble metal impurities dissolved from counter/reference electrodes. ACS Catalysis, 10:3381-3389, Jan 2020. URL: https://doi.org/10.1021/acscatal.9b04229, doi:10.1021/acscatal.9b04229. This article has 32 citations and is from a highest quality peer-reviewed journal.

4. (cherevko2015dissolutionofplatinum pages 6-7): Serhiy Cherevko, Gareth P. Keeley, Simon Geiger, Aleksandar R. Zeradjanin, Nejc Hodnik, Nadiia Kulyk, and Karl J. J. Mayrhofer. Dissolution of platinum in the operational range of fuel cells. Chemelectrochem, 2:1471-1478, May 2015. URL: https://doi.org/10.1002/celc.201500098, doi:10.1002/celc.201500098. This article has 270 citations and is from a peer-reviewed journal.

5. (cherevko2015dissolutionofplatinum pages 5-6): Serhiy Cherevko, Gareth P. Keeley, Simon Geiger, Aleksandar R. Zeradjanin, Nejc Hodnik, Nadiia Kulyk, and Karl J. J. Mayrhofer. Dissolution of platinum in the operational range of fuel cells. Chemelectrochem, 2:1471-1478, May 2015. URL: https://doi.org/10.1002/celc.201500098, doi:10.1002/celc.201500098. This article has 270 citations and is from a peer-reviewed journal.

6. (cherevko2015dissolutionofplatinum pages 3-4): Serhiy Cherevko, Gareth P. Keeley, Simon Geiger, Aleksandar R. Zeradjanin, Nejc Hodnik, Nadiia Kulyk, and Karl J. J. Mayrhofer. Dissolution of platinum in the operational range of fuel cells. Chemelectrochem, 2:1471-1478, May 2015. URL: https://doi.org/10.1002/celc.201500098, doi:10.1002/celc.201500098. This article has 270 citations and is from a peer-reviewed journal.

7. (cherevko2015dissolutionofplatinum pages 4-5): Serhiy Cherevko, Gareth P. Keeley, Simon Geiger, Aleksandar R. Zeradjanin, Nejc Hodnik, Nadiia Kulyk, and Karl J. J. Mayrhofer. Dissolution of platinum in the operational range of fuel cells. Chemelectrochem, 2:1471-1478, May 2015. URL: https://doi.org/10.1002/celc.201500098, doi:10.1002/celc.201500098. This article has 270 citations and is from a peer-reviewed journal.

8. (jenewein2021accessinginsitu pages 2-3): Ken J. Jenewein, Attila Kormányos, Julius Knöppel, Karl J. J. Mayrhofer, and Serhiy Cherevko. Accessing in situ photocorrosion under realistic light conditions: photoelectrochemical scanning flow cell coupled to online icp-ms. ACS Measurement Science Au, 1:74-81, Aug 2021. URL: https://doi.org/10.1021/acsmeasuresciau.1c00016, doi:10.1021/acsmeasuresciau.1c00016. This article has 39 citations and is from a peer-reviewed journal.

9. (nikman2020constructionandapplication pages 63-68): Shahin Nikman. Construction and application of an on-line flow cell icp-oes setup for real time dissolution detection. ArXiv, Jan 2020. URL: https://doi.org/10.17635/lancaster/thesis/1049, doi:10.17635/lancaster/thesis/1049. This article has 1 citations.

10. (nikman2020constructionandapplication pages 68-73): Shahin Nikman. Construction and application of an on-line flow cell icp-oes setup for real time dissolution detection. ArXiv, Jan 2020. URL: https://doi.org/10.17635/lancaster/thesis/1049, doi:10.17635/lancaster/thesis/1049. This article has 1 citations.

11. (ogle2019atomicemissionspectroelectrochemistry pages 1-4): Kevin Ogle. Atomic emission spectroelectrochemistry: real-time rate measurements of dissolution, corrosion, and passivation. Corrosion, 75:1398-1419, Sep 2019. URL: https://doi.org/10.5006/3336, doi:10.5006/3336. This article has 126 citations and is from a peer-reviewed journal.

12. (zhu2019effectofsupporting pages 2-4): Kai Zhu, Xiaoli Ren, Xiuping Sun, Lijing Zhu, and Zhirong Sun. Effect of supporting electrolyte on the surface corrosion and anodic oxidation performance of graphite electrode. Electrocatalysis, pages 1-11, Sep 2019. URL: https://doi.org/10.1007/s12678-019-00541-6, doi:10.1007/s12678-019-00541-6. This article has 21 citations.

13. (zhu2019effectofsupporting pages 4-6): Kai Zhu, Xiaoli Ren, Xiuping Sun, Lijing Zhu, and Zhirong Sun. Effect of supporting electrolyte on the surface corrosion and anodic oxidation performance of graphite electrode. Electrocatalysis, pages 1-11, Sep 2019. URL: https://doi.org/10.1007/s12678-019-00541-6, doi:10.1007/s12678-019-00541-6. This article has 21 citations.

14. (zhu2019effectofsupporting pages 1-2): Kai Zhu, Xiaoli Ren, Xiuping Sun, Lijing Zhu, and Zhirong Sun. Effect of supporting electrolyte on the surface corrosion and anodic oxidation performance of graphite electrode. Electrocatalysis, pages 1-11, Sep 2019. URL: https://doi.org/10.1007/s12678-019-00541-6, doi:10.1007/s12678-019-00541-6. This article has 21 citations.

15. (zhu2019effectofsupporting pages 8-10): Kai Zhu, Xiaoli Ren, Xiuping Sun, Lijing Zhu, and Zhirong Sun. Effect of supporting electrolyte on the surface corrosion and anodic oxidation performance of graphite electrode. Electrocatalysis, pages 1-11, Sep 2019. URL: https://doi.org/10.1007/s12678-019-00541-6, doi:10.1007/s12678-019-00541-6. This article has 21 citations.

16. (ambrosi2012chemicallyreducedgraphene pages 2-3): Adriano Ambrosi, Chun Kiang Chua, Bahareh Khezri, Zdeněk Sofer, Richard D. Webster, and Martin Pumera. Chemically reduced graphene contains inherent metallic impurities present in parent natural and synthetic graphite. Proceedings of the National Academy of Sciences, 109:12899-12904, Jul 2012. URL: https://doi.org/10.1073/pnas.1205388109, doi:10.1073/pnas.1205388109. This article has 258 citations and is from a highest quality peer-reviewed journal.

17. (wong2014syntheticroutescontaminate pages 2-3): Colin Hong An Wong, Zdeněk Sofer, Marie Kubešová, Jan Kučera, Stanislava Matějková, and Martin Pumera. Synthetic routes contaminate graphene materials with a whole spectrum of unanticipated metallic elements. Proceedings of the National Academy of Sciences, 111:13774-13779, Sep 2014. URL: https://doi.org/10.1073/pnas.1413389111, doi:10.1073/pnas.1413389111. This article has 187 citations and is from a highest quality peer-reviewed journal.

18. (colburn2021liftingthelid pages 7-9): Alex Colburn, Katharine Levey, Danny O'Hare, and Julie Macpherson. Lifting the lid on the potentiostat: a beginner's guide to understanding electrochemical circuitry and practical operation. Physical chemistry chemical physics : PCCP, 23 14:8100-8117, Feb 2021. URL: https://doi.org/10.1039/d1cp00661d, doi:10.1039/d1cp00661d. This article has 166 citations.

19. (joress2022developmentofan pages 1-4): Howie Joress, Brian DeCost, Najlaa Hassan, Trevor M. Braun, Justin M. Gorham, and Jason Hattrick-Simpers. Development of an automated millifluidic platform and data-analysis pipeline for rapid electrochemical corrosion measurements: a ph study on zn-ni. SSRN Electronic Journal, Apr 2022. URL: https://doi.org/10.48550/arxiv.2204.06094, doi:10.48550/arxiv.2204.06094. This article has 19 citations.

20. (cimenti2007distortionsinelectrochemical pages 1-2): M. Cimenti, A. C. Co, V. I. Birss, and J. M. Hill. Distortions in electrochemical impedance spectroscopy measurements using 3‐electrode methods in sofc. i – effect of cell geometry. Fuel Cells, 7:364-376, Oct 2007. URL: https://doi.org/10.1002/fuce.200700019, doi:10.1002/fuce.200700019. This article has 102 citations and is from a peer-reviewed journal.

21. (ooi2021timeresolvedmeasurementsof pages 5-7): Azusa Ooi, Eiji Tada, and Atsushi Nishikata. Time-resolved measurements of dissolution rates of platinum and palladium by a solution flow cell combined with icp-ms. MATERIALS TRANSACTIONS, 62:797-806, Jun 2021. URL: https://doi.org/10.2320/matertrans.c-m2021820, doi:10.2320/matertrans.c-m2021820. This article has 11 citations and is from a peer-reviewed journal.

22. (zhang2023electrochemicalimpedancespectroscopy pages 5-8): Jianbo Zhang, Shangshang Wang, and Kei Ono. Electrochemical Impedance Spectroscopy, pages 301-350. CRC Press, Mar 2023. URL: https://doi.org/10.1201/9781003299295-11, doi:10.1201/9781003299295-11. This article has 1674 citations.

23. (zhu2019effectofsupporting pages 6-8): Kai Zhu, Xiaoli Ren, Xiuping Sun, Lijing Zhu, and Zhirong Sun. Effect of supporting electrolyte on the surface corrosion and anodic oxidation performance of graphite electrode. Electrocatalysis, pages 1-11, Sep 2019. URL: https://doi.org/10.1007/s12678-019-00541-6, doi:10.1007/s12678-019-00541-6. This article has 21 citations.

24. (cherevko2015dissolutionofplatinum pages 1-2): Serhiy Cherevko, Gareth P. Keeley, Simon Geiger, Aleksandar R. Zeradjanin, Nejc Hodnik, Nadiia Kulyk, and Karl J. J. Mayrhofer. Dissolution of platinum in the operational range of fuel cells. Chemelectrochem, 2:1471-1478, May 2015. URL: https://doi.org/10.1002/celc.201500098, doi:10.1002/celc.201500098. This article has 270 citations and is from a peer-reviewed journal.
