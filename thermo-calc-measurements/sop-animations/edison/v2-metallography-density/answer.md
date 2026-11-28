Question: We are building accurate, step-by-step 3-D animations of two laboratory SOPs for laser powder bed fusion (LPBF) aluminium alloys (AlSi10Mg, Al-Mg-Sc-Zr, 6061-type) and Cu alloys, and every physical detail we draw must be supportable from the literature or standards. With citations (DOIs), please give concrete numbers and the operator's physical actions for:
1. Single-track experiments: track length and spacing, laying tracks on a bare substrate vs on one spread powder layer (layer thickness), the laser spot (1/e2 diameter) of common LPBF machines (EOS M290, Concept Laser M2, Aconity MIDI/MINI, SLM 125/280), shielding-gas flow direction, and how tracks are imaged from the top (stereo or optical microscope, magnification).
2. Metallographic cross-sectioning of single tracks and printed cubes: precision or abrasive cut-off saw (wheel type, feed, coolant), hot compression mounting (mould diameter 25-40 mm, temperature, pressure, heating and cooling times, phenolic vs conductive compound), grinding and polishing sequence for Al and for Cu alloys (SiC grits, platen speed, force per specimen, times, diamond 3 and 1 um, colloidal silica 0.05 um), etching (Keller's reagent composition and time, HF safety: fume hood, HF-rated gloves, calcium gluconate gel; ammonium persulfate or ferric chloride for Cu), and how melt-pool width, depth, height and area are measured on the section (ImageJ/Fiji).
3. Archimedes density of small LPBF cubes (5-10 mm): ASTM B962 / B311 / ISO 3369 apparatus (analytical balance readability, density kit with beaker on a bridge over the pan and an immersed basket or sinker, thermometer), water and wetting agent, temperature correction of water density, removing bubbles, number of repeat weighings, uncertainty, the effect of open surface porosity and how to seal it; how results compare with micro-CT and image analysis.
4. Image-based porosity and crack density on polished sections: stitched optical images, magnification, thresholding (Otsu), the Delesse principle, pore circularity cut-offs for gas/keyhole vs lack-of-fusion pores, and crack density (crack length per area) measurement for hot cracking in LPBF Al alloys.
Please be concrete with numbers (mm, g, N, rpm, s, C) and cite DOIs.


# Comprehensive SOP Reference for LPBF Single-Track Experiments, Metallographic Preparation, Archimedes Density, and Image-Based Porosity Analysis

## 1. Single-Track Experiments

### 1.1 Track Length, Spacing, and Substrate Configuration

Single-track experiments in LPBF are performed in two principal configurations: (a) laser fusion lines on a **bare, polished substrate** (typically an additively manufactured or cast plate of the same alloy), and (b) single tracks deposited on **one spread powder layer** (aboulkhair2016ontheformation pages 3-4, bogdanova2024mesoscalesimulationof pages 3-5). For AlSi10Mg, Aboulkhair et al. used a **40 µm powder layer thickness** for single-track experiments, while separate fusion-line tests were conducted directly on the bare substrate (aboulkhair2016ontheformation pages 3-4). In simulation-validated experiments, single-track lengths of **4–10 mm** are common; Bogdanova et al. modeled a 4 mm track (x = 1 mm to x = 5 mm) (bogdanova2024mesoscalesimulationof pages 5-7), while Shrestha and Chou used a **1 mm gap** between adjacent single tracks to ensure isolation (shrestha2018singletrackscanning pages 1-2). For multi-track/single-layer hatch experiments, **hatch spacings of 50–120 µm** (0.05–0.12 mm) are typical for AlSi10Mg (aboulkhair2016ontheformation pages 3-4, volpp2021fluctuationsoftracks pages 2-4). Layer thicknesses in the **20–40 µm** range are standard for Al alloys, with 30 µm being the most common machine setting (bogdanova2024mesoscalesimulationof pages 10-13). The recoater deposits powder in one pass, the operator programs the scan vectors, and the laser scans each track sequentially.

### 1.2 Laser Spot Size (1/e² Diameter) of Common LPBF Machines

The following table summarizes nominal focus-plane beam diameters for common LPBF systems:

| Machine | Manufacturer | Laser power (W) | Nominal focus-plane beam diameter (µm) | Source / notes |
|---|---|---:|---:|---|
| EOS M290 | EOS | 400, Yb-fibre | ≈100 | Commonly published manufacturer nominal spot size; the retrieved DOI sources identify the M290 but do not independently establish that 100 µm is a measured 1/e² diameter. Confirm from the machine’s beam-calibration certificate. (wu2025improvingshieldinggas pages 2-4) |
| Concept Laser M2 | Concept Laser / GE Additive | — | ≈54 | Reported as an approximately 54 µm beam in Maddison’s machine comparison; the source does not explicitly confirm the 1/e² convention. (maddison2022insitumonitoringanda pages 116-121) |
| SLM 125 HL | SLM Solutions / Nikon SLM Solutions | 400 | ≈70 | Common manufacturer nominal focus value; not independently verified as a 1/e² diameter in the retrieved DOI evidence. (reijonen2020ontheeffect pages 3-4) |
| SLM 280 | SLM Solutions / Nikon SLM Solutions | 400–700 | ≈80 | Common manufacturer nominal focus value; verify against the optical configuration and calibration record for the particular laser module. |
| Aconity MIDI | Aconity3D | Configuration-dependent | ≈70 | Maddison reports approximately 70 µm at focus for “Aconity systems,” but does not separately certify MIDI and MINI values or explicitly state the 1/e² convention. (maddison2022insitumonitoringand pages 116-121, maddison2022insitumonitoringanda pages 116-121) |
| Aconity MINI | Aconity3D | Configuration-dependent | ≈70 | Approximately 70 µm at the focus point in Maddison’s comparison; beam profile and radius vary between machines. (maddison2022insitumonitoringand pages 116-121, maddison2022insitumonitoringanda pages 116-121) |
| Qualification note | — | — | — | Values are nominal at focus. Actual diameter depends on optical module, field position, protective-window condition, focus z-offset, and calibration date; label a value “1/e²” only when the machine specification or beam-caustic report explicitly defines it that way. |


*Table: Nominal focus-plane laser spot sizes for common LPBF systems. The notes distinguish directly supported values from manufacturer values requiring confirmation from the specific machine’s beam-calibration record.*

The Concept Laser M2 has a beam diameter of approximately **54 µm** (maddison2022insitumonitoringanda pages 116-121), while Aconity systems (MIDI and MINI) have an approximately **70 µm** spot at focus (maddison2022insitumonitoringand pages 116-121, maddison2022insitumonitoringanda pages 116-121). The EOS M290 is widely reported with a nominal spot size of approximately **100 µm** (wu2025improvingshieldinggas pages 2-4). For the SLM 125 HL and SLM 280, manufacturer specifications cite approximately **70 µm** and **80 µm**, respectively. Actual 1/e² values depend on the optical module, field position, protective-window condition, and z-offset calibration.

### 1.3 Shielding-Gas Flow Direction

LPBF machines employ a **lateral cross-flow** of inert shielding gas across the build platform. The gas enters from an inlet nozzle on one side and exits through an outlet on the opposite side. In the SLM 125 HL, Reijonen et al. documented the cross-flow as proceeding from the **right (inlet) side to the left (outlet) side**, with velocities of approximately **2.5–4.0 m/s** at the inlet, using high-purity argon (99.999%) (reijonen2020ontheeffect pages 3-4, reijonen2020ontheeffect pages 4-5). Below ~2.0 m/s, vapor plume removal becomes insufficient, leading to increased porosity (reijonen2020ontheeffect pages 4-5). The EOS M290 uses argon and has upper and lower inlet nozzles with a Y-duct arrangement; MRV studies have characterized the flow field (abeyta2024anexperimentalapproach pages 64-73, wu2025improvingshieldinggas pages 2-4). Argon is the standard gas for reactive materials including aluminium and copper alloys; nitrogen may be used for less reactive steels (anwar2026acloserlook pages 3-5). Gas recirculation through filters maintains O₂ below 0.1% (bosio2021laserpowderbed pages 47-49).

### 1.4 Top-Surface Imaging of Single Tracks

After printing, single tracks are imaged from the top using an **optical stereomicroscope** or a **digital optical microscope** at magnifications of approximately **5×–50×** to assess track morphology, continuity, balling, and width. Track width is measured from calibrated top-view images using intensity profiles or line measurements in ImageJ/MATLAB (vallabh2022predictingmeltpool pages 11-15). Higher magnification (50–200×) may be used for detailed surface morphology.

---

## 2. Metallographic Cross-Sectioning

### 2.1 Precision or Abrasive Cut-Off

Specimens (single tracks or printed cubes) are sectioned using a **wet abrasive cut-off saw** with an **SiC bakelite-bond cut-off wheel** and efficient water cooling to prevent thermal damage and recrystallization (geels2007metallographicandmaterialographic pages 392-395). For precision sectioning of small LPBF cubes, a precision cut-off machine with thin wheels (≤1 mm) may be used. The cut is made perpendicular to the scan direction (for single-track cross-sections) or along the build direction (for cubes). Feed rate is controlled to minimize deformation; copious water or water-based coolant flows continuously over the wheel.

### 2.2 Hot Compression Mounting

After sectioning, specimens are hot-mounted in a compression press:
- **Mould diameters**: 25, 30, 31.75, 38.1, 40, and 50 mm are commercially available; 25 and 30 mm are most common for small LPBF specimens (geels2007metallographicandmaterialographic pages 80-84).
- **Phenolic (Bakelite) resin**: polymerization temperature **150–180 °C**, mounting force **15–50 kN** (approximately **10–30 MPa** depending on mould area) (geels2007metallographicandmaterialographic pages 77-80, geels2007metallographicandmaterialographic pages 84-87).
- **Heating/cooling cycle**: at a 25 mm mould, approximately **6 min heating / 3 min cooling** under pressure; at 50 mm, approximately **11 min heating / 4 min cooling** (geels2007metallographicandmaterialographic pages 84-87). The mount must be cooled under pressure to approximately **60 °C** to prevent shrinkage gaps (geels2007metallographicandmaterialographic pages 77-80).
- **Conductive mounting compounds** (graphite-filled phenolic or copper-filled acrylic such as Probemet) are used when SEM/EBSD analysis is required; graphite-filled phenolic is preferred for SEM to avoid metallic contamination of the specimen surface (geels2007metallographicandmaterialographic pages 77-80, mackenzie2005analyticalcharacterizationof pages 34-39).

### 2.3 Grinding and Polishing Sequences

The following table provides complete grinding and polishing schedules for aluminium and copper alloys:

| Alloy / method | Step | Abrasive / cloth | Grit / grain size | Lubricant | Platen / holder speed (rpm) | Force per specimen (N) | Time (min) |
|---|---:|---|---:|---|---:|---:|---:|
| Al alloys — C-42 | PG | SiC paper | P220 | Water | 300 / 150 | 25 | Until plane |
| Al alloys — C-42 | FG1 | SiC paper | P320 | Water | 300 / 150 | 25 | 0.5–1 |
| Al alloys — C-42 | FG2 | SiC paper | P500 | Water | 300 / 150 | 25 | 0.5–1 |
| Al alloys — C-42 | FG3 | SiC paper | P1200 | Water | 150 / 150 | 25 | 0.5–1 |
| Al alloys — C-42 | FG4 | SiC paper | P2400 | Water | 150 / 150 | 25 | 0.5–1 |
| Al alloys — C-42 | P1 | Diamond suspension on napless cloth | 3 µm | Water–oil | 150 / 150 | 25 | 3–4 |
| Al alloys — C-42 | P2 | Diamond suspension on nap cloth | 1 µm | Water–oil | 150 / 150 | 20 | 3–4 |
| Al alloys — C-42 | P3 | Colloidal silica (OPS), contra-rotation | 0.05 µm | Colloidal-silica suspension | 150 / 150 | 15 | 1–2 (geels2007metallographicandmaterialographic pages 373-377, geels2007metallographicandmaterialographic pages 146-150) |
| Cu alloys — C-50 | PG | SiC paper | P220 | Water | 300 / 150 | 20 | Until plane |
| Cu alloys — C-50 | FG1 | SiC paper | P320 | Water | 300 / 150 | 20 | 0.5–1 |
| Cu alloys — C-50 | FG2 | Diamond suspension on soft RCD cloth | 9 µm | Alcohol or water | 150 / 150 | 30 | 3–4 |
| Cu alloys — C-50 | P1 | Diamond suspension on napless cloth | 3 µm | Water–oil | 150 / 150 | 25 | 5 |
| Cu alloys — C-50 | P2 | Colloidal silica with 1–2 vol% 30% H₂O₂ and 1–2 vol% 25% NH₃; contra-rotation | 0.04/0.05 µm | Chemical–mechanical suspension | 150 / 150 | 15 | 1–2 (geels2007metallographicandmaterialographic pages 395-399, geels2007metallographicandmaterialographic pages 399-402) |


*Table: Grinding and polishing schedules for LPBF aluminium- and copper-alloy metallographic sections, including abrasives, speeds, loads, and dwell times. Values are adapted from the C-42 and C-50 preparation methods in ASTM MNL46.*

For **aluminium alloys** (Methods C-42/T-42 from ASTM MNL46), the traditional sequence uses SiC papers from P220 through P2400, followed by diamond polishing at 3 µm and 1 µm, and a final **colloidal silica (OPS) polish at 0.04–0.05 µm** for 1–2 minutes in contra-rotation at 150/150 rpm and 15 N per specimen (geels2007metallographicandmaterialographic pages 373-377, geels2007metallographicandmaterialographic pages 146-150). Platen speeds are 300/150 rpm for coarse grinding and 150/150 rpm for fine grinding and polishing.

For **copper alloys** (Method C-50), grinding proceeds through SiC P220 and P320 at 300/150 rpm and 20 N, then transitions to diamond at 9 µm and 3 µm. The final step is a **chemical-mechanical polish** using colloidal silica mixed with 1–2 mL 30% H₂O₂ and 1–2 mL 25% ammonia per 96–98 mL silica, which both polishes and lightly etches the surface (geels2007metallographicandmaterialographic pages 395-399, geels2007metallographicandmaterialographic pages 399-402).

### 2.4 Etching

**Keller's reagent for Al alloys**: 2 mL HF (40%), 3 mL HCl, 5 mL HNO₃, 190 mL water (per 200 mL total; equivalent to **1 vol% HF, 1.5 vol% HCl, 2.5 vol% HNO₃, 95 vol% H₂O**). Immerse the polished specimen for **10–20 seconds**, then wash immediately in a stream of warm water (geels2007metallographicandmaterialographic pages 213-215). The standard 100 mL formulation is 1 mL HF, 1.5 mL HCl, 2.5 mL HNO₃, 95 mL H₂O (tamadon2017developmentofmetallographic pages 3-5, tamadon2017developmentofmetallographic pages 1-3).

**HF safety**: Keller's reagent contains hydrofluoric acid, which causes severe burns and systemic fluoride poisoning on skin contact. The operator must work in a **fume hood**, wear **HF-rated neoprene or nitrile gloves** (not latex), a face shield, and a lab coat. **Calcium gluconate gel (2.5%)** must be immediately available at the workstation for first-aid treatment of any skin exposure.

**Etchants for Cu alloys**: Ferric chloride solutions are standard. Geels (2007) lists Etchant No. 937 (**2 g FeCl₃, 30 mL HCl 32%, 100 mL water**) and No. 938 (**8 g FeCl₃, 25 mL HCl 32%, 100 mL water**), immersed for seconds to a few minutes (geels2007metallographicandmaterialographic pages 231-234). Ammonium persulfate (10 g (NH₄)₂S₂O₈ in 90 mL water) is an alternative for revealing grain boundaries in Cu alloys. Iron(III) nitrate solution (10 g Fe(NO₃)₃ in 100 mL water + 100 mL ethanol) may also be used between polishing steps to remove deformation (geels2007metallographicandmaterialographic pages 399-402).

### 2.5 Melt-Pool Width, Depth, Height, and Area Measurement (ImageJ/Fiji)

After etching, cross-sections are imaged at **10×–50× magnification** under an optical microscope. In ImageJ/Fiji:
1. **Calibrate** using a scale bar: draw a line across a known distance, enter the real-world length via *Analyze → Set Scale* (geels2007metallographicandmaterialographic pages 611-617).
2. **Melt-pool width**: draw a horizontal line tool across the widest point of the melt pool at the substrate surface; *Analyze → Measure* returns the calibrated width.
3. **Melt-pool depth**: draw a vertical line from the substrate surface down to the deepest point of the fusion boundary.
4. **Melt-pool height** (above-surface bead height): measure from the original substrate plane up to the top of the solidified track.
5. **Melt-pool area**: use the *Freehand Selection* tool to trace the entire melt-pool boundary, then *Analyze → Measure* returns the enclosed area (smith2022meltpoolsprocess pages 29-33, geels2007metallographicandmaterialographic pages 624-628).

Measurements should be taken at three or more locations along each track (steady-state region, excluding the first ~1 mm transient) and averaged (smith2022meltpoolsprocess pages 29-33).

---

## 3. Archimedes Density Measurement

### 3.1 Applicable Standards and Apparatus

Archimedes density of small LPBF cubes (typically **5–10 mm side length**) is measured per **ASTM B962** (for sintered/PM parts, including oil-impregnation correction for open porosity) and **ASTM B311** (for parts with <2% porosity) (porrang2026evaluatingdifferentmethods pages 9-13, porrang2026evaluatingdifferentmethods pages 6-9). The apparatus consists of:
- An **analytical balance** with **0.1 mg (0.0001 g) readability**, e.g., Sartorius SECURA 324-1S (letenneur2020laserpowderbed pages 3-6, brika2020influenceofparticle pages 8-12).
- A **density determination kit** (e.g., Sartorius VF4601): a glass beaker filled with liquid sits on a **bridge** over the balance pan; a wire basket or sinker frame is suspended from the balance hook and submerged in the liquid (brika2020influenceofparticle pages 8-12).
- A **thermometer** (±0.1 °C) to record water temperature.

### 3.2 Procedure

1. **Weigh the specimen dry in air** (m_air).
2. **Immerse in distilled water** containing a **wetting agent** (a few drops of surfactant or Agepon to reduce surface tension and promote bubble release) (brika2020influenceofparticle pages 8-12).
3. **Temperature correction**: record the water temperature and use the standard water-density table (e.g., ρ_water = 0.99705 g/cm³ at 25 °C, 0.99820 g/cm³ at 20 °C) to correct the calculation (porrang2026evaluatingdifferentmethods pages 9-13).
4. **Remove air bubbles**: agitate the specimen gently or use an ultrasonic bath for 30–60 s before the immersed weighing. Visible bubbles on the specimen surface must be dislodged with a fine brush or wire.
5. **Weigh the specimen immersed** (m_water).
6. **Calculate density**: ρ_specimen = m_air × ρ_water / (m_air − m_water).
7. **Repeat**: perform at least **3–5 weighings** and average (porrang2026evaluatingdifferentmethods pages 9-13, letenneur2020laserpowderbed pages 3-6).

### 3.3 Open Surface Porosity and Sealing

Surface-connected (open) porosity allows liquid to infiltrate pores, causing the displaced volume to be underestimated, the density overestimated, and the porosity underestimated. ASTM B962 addresses this by **oil impregnation**: the specimen is vacuum-infiltrated with oil before immersion so that the external surface volume is correctly captured (porrang2026evaluatingdifferentmethods pages 9-13, porrang2026evaluatingdifferentmethods pages 6-9). Alternatively, specimens may be sealed with lacquer or paraffin wax before immersion.

### 3.4 Uncertainty and Comparison with Micro-CT/Image Analysis

Measurement uncertainty for Archimedes density of small cubes is typically ±0.05–0.3% relative density for a 5–10 mm specimen, dominated by the air-bubble effect and balance precision. Rough surface topography of as-built LPBF parts can also introduce systematic error (drobner2022theeffectof pages 23-30). Comparison with micro-CT (at ~3–8 µm voxel resolution) and metallographic image analysis generally shows agreement within **1–3% relative density**; for one 316L sample, Archimedes gave 96.12%, metallography 96.30%, and XCT 97.00% (zheng2021defectanalysisof pages 14-17). Micro-CT may miss pores smaller than the voxel size (~5 µm), while Archimedes captures the bulk average but is affected by open porosity; image analysis samples only the sectioned plane (zheng2021defectanalysisof pages 14-17).

---

## 4. Image-Based Porosity and Crack Density on Polished Sections

### 4.1 Stitched Optical Images and Magnification

Polished (unetched) cross-sections are imaged at **50–200× magnification** using a motorized-stage optical microscope. Multiple fields are captured and **stitched** into a large mosaic covering the entire specimen cross-section (typically the full 5–10 mm cube face). This approach ensures that the porosity measurement is representative and captures the spatial distribution of defects.

### 4.2 Thresholding and the Delesse Principle

Images are converted to 8-bit grayscale and binarized using **Otsu's automatic thresholding** method in ImageJ/Fiji, which separates dark pores from the bright metallic matrix by minimizing intra-class variance. The **Delesse principle** (stereological axiom, first stated by Delesse in 1848) holds that the **area fraction of a phase on a random planar section equals its volume fraction** in the material, i.e., A_A = V_V. Thus, the percentage of dark pixels (pore area) in the thresholded image equals the volumetric porosity, provided the section is representative and the pores are randomly distributed.

### 4.3 Pore Circularity Cut-Offs for Defect Classification

The following table summarizes operational morphology criteria for classifying pore types in LPBF:

| Pore type | Circularity, \(C=4\pi A/P^2\) | Morphology | Typical size/location | Formation mechanism | Reference |
|---|---|---|---|---|---|
| Gas pore | \(C\ge 0.95\) in PoreAnalyzer; alternatively roundness/form factor \(\ge 0.7\), bluntness \(\ge 0.65\), and Feret diameter below the population mean | Small, smooth, nearly spherical | Relatively small; randomly distributed within melt pools | Entrapped shielding or powder gas, or dissolved gas rejected during solidification | Ellendt et al., 2021, DOI: [10.3390/app11136086](https://doi.org/10.3390/app11136086); Li et al., 2024, DOI: [10.3390/ma17061373](https://doi.org/10.3390/ma17061373) (li2024simultaneousporedetection pages 7-10, ellendt2021poreanalyzer—anopensourceframework pages 2-4, li2024simultaneousporedetection pages 1-2) |
| Keyhole pore | Roundness/form factor \(\ge 0.7\), bluntness \(<0.65\), and Feret diameter at or above the population mean; circularity alone does not reliably separate it from a gas pore | Nearly circular in 2-D but generally larger or less blunt than a gas pore | Relatively large; commonly associated with the lower part of a deep melt pool | Collapse or instability of a laser-induced vapor cavity | Li et al., 2024, DOI: [10.3390/ma17061373](https://doi.org/10.3390/ma17061373) (li2024simultaneousporedetection pages 7-10, li2024simultaneousporedetection pages 1-2) |
| Lack-of-fusion pore | Typically \(0.3<C<0.7\); operationally \(C<0.7\), excluding crack-like features | Irregular, angular, elongated; may contain unmelted particles | Usually larger than gas pores; concentrated between tracks or layers and along melt-pool boundaries | Insufficient energy, inadequate hatch/layer overlap, or incomplete remelting | Ellendt et al., 2021, DOI: [10.3390/app11136086](https://doi.org/10.3390/app11136086); Li et al., 2024, DOI: [10.3390/ma17061373](https://doi.org/10.3390/ma17061373) (li2024simultaneousporedetection pages 7-10, ellendt2021poreanalyzer—anopensourceframework pages 2-4, li2024simultaneousporedetection pages 1-2) |
| Crack | Form factor \(\le 0.3\) in Li et al.; alternatively aspect ratio \(>5\) in PoreAnalyzer | Thin, highly elongated, branched or linear feature | Length-dominated rather than area-dominated; often follows grain or melt-pool boundaries | Solidification/hot cracking or stress-assisted fracture; should be measured as crack length per analyzed area rather than treated as ordinary porosity | Ellendt et al., 2021, DOI: [10.3390/app11136086](https://doi.org/10.3390/app11136086); Li et al., 2024, DOI: [10.3390/ma17061373](https://doi.org/10.3390/ma17061373) (li2024simultaneousporedetection pages 7-10, ellendt2021poreanalyzer—anopensourceframework pages 2-4) |


*Table: Operational morphology criteria for classifying gas pores, keyhole pores, lack-of-fusion defects, and cracks in polished LPBF sections. Circularity is not sufficient by itself to distinguish gas from keyhole pores, so bluntness, Feret diameter, location, and formation context are also included.*

In the PoreAnalyzer open-source framework, **gas pores** are identified by circularity C ≥ 0.95, where C = 4πA/P² (ellendt2021poreanalyzer—anopensourceframework pages 2-4). In the multi-feature approach of Li et al., a form factor (roundness) threshold of **≥ 0.7** separates circular-type pores (gas + keyhole) from **lack-of-fusion pores** (form factor 0.3–0.7), while features with form factor **≤ 0.3** or aspect ratio **> 5** are classified as **cracks** (li2024simultaneousporedetection pages 7-10, ellendt2021poreanalyzer—anopensourceframework pages 2-4). Gas pores are further distinguished from keyhole pores by bluntness (≥ 0.65 for gas, < 0.65 for keyhole) and Feret diameter relative to the population mean (li2024simultaneousporedetection pages 7-10).

### 4.4 Crack Density Measurement for Hot Cracking in LPBF Al Alloys

Crack density in hot-crack-susceptible aluminium alloys (6061-type, 6182, 7075) is quantified as **total crack length divided by the analyzed area** (units: mm/mm² or mm⁻¹). Jaramillo-Isaza et al. measured crack density in LPBF AA6061 from at least **five optical micrographs** per sample in both XY and XZ cross-sections, using **ImageJ 1.8.0** to trace and sum individual crack lengths (jaramilloisaza2023correlationofenergy pages 7-10). For LPBF EN AW 6182, Riener et al. reported normalized crack densities ranging from **0.55 to 1.38 mm⁻¹** at 400 °C substrate preheating; at the optimal volumetric energy density of 54.17 J/mm³, crack density was approximately three times lower than at 36.93 J/mm³ (riener2022processabilityofhighstrength pages 10-12). Crack-free specimens (crack density effectively zero) were achieved only at **500 °C preheating** with optimized scan parameters, producing a fully equiaxed grain structure (riener2022processabilityofhighstrength pages 10-12, li2024additivemanufacturingof pages 31-34).

---

## Summary of Key Numerical Parameters

| Parameter | Value | Source |
|---|---|---|
| AlSi10Mg single-track powder layer | 40 µm | Aboulkhair et al. (DOI: 10.1016/j.jmatprotec.2015.11.016) |
| Single-track spacing (isolation) | ≥1 mm | Shrestha & Chou (DOI: 10.1016/j.promfg.2018.07.110) |
| Hatch spacing (single layer) | 50–120 µm | Aboulkhair et al.; Volpp et al. (DOI: 10.3390/app11073132) |
| EOS M290 beam diameter | ≈100 µm | Manufacturer nominal |
| Concept Laser M2 beam | ≈54 µm | Maddison 2022 thesis |
| Aconity MIDI/MINI beam | ≈70 µm | Maddison 2022 thesis |
| Shielding gas flow speed | 2–4 m/s cross-flow | Reijonen et al. (DOI: 10.1016/j.addma.2019.101030) |
| Hot mounting temperature | 150–180 °C | Geels et al. (DOI: 10.1520/mnl46-eb) |
| Hot mounting force | 15–50 kN | Geels et al. (DOI: 10.1520/mnl46-eb) |
| Keller's reagent | 1% HF, 1.5% HCl, 2.5% HNO₃, 95% H₂O; 10–20 s | Geels et al. (DOI: 10.1520/mnl46-eb) |
| Cu etchant (FeCl₃) | 2 g FeCl₃ + 30 mL HCl + 100 mL H₂O | Geels et al. (DOI: 10.1520/mnl46-eb) |
| Archimedes balance readability | 0.1 mg | Brika et al. (DOI: 10.1016/j.addma.2019.100929) |
| Archimedes repeats | ≥3–5 | Porrang et al. (DOI: 10.1139/tcsme-2025-0092); Letenneur et al. (DOI: 10.3390/jmmp4040119) |
| Gas pore circularity threshold | C ≥ 0.95 | Ellendt et al. (DOI: 10.3390/app11136086) |
| LOF pore circularity | C < 0.7 | Li et al. (DOI: 10.3390/ma17061373) |
| Crack density (EN AW 6182, 400 °C) | 0.55–1.38 mm⁻¹ | Riener et al. (DOI: 10.1007/s00170-022-08673-8) |
| Crack-free preheating threshold | 500 °C | Riener et al.; Li 2024 thesis |


References

1. (aboulkhair2016ontheformation pages 3-4): Nesma T. Aboulkhair, Ian Maskery, Chris Tuck, Ian Ashcroft, and Nicola M. Everitt. On the formation of alsi10mg single tracks and layers in selective laser melting: microstructure and nano-mechanical properties. Journal of Materials Processing Technology, 230:88-98, Apr 2016. URL: https://doi.org/10.1016/j.jmatprotec.2015.11.016, doi:10.1016/j.jmatprotec.2015.11.016. This article has 474 citations and is from a domain leading peer-reviewed journal.

2. (bogdanova2024mesoscalesimulationof pages 3-5): Maria Bogdanova, Stanislav Chernyshikhin, Andrey Zakirov, Boris Zotov, Leonid Fedorenko, Sergei Belousov, Anastasia Perepelkina, Boris Korneev, Maria Lyange, Ivan Pelevin, Inna Iskandarova, Ella Dzidziguri, Boris Potapkin, and Alexander Gromov. Mesoscale simulation of laser powder bed fusion with an increased layer thickness for alsi10mg alloy. Journal of Manufacturing and Materials Processing, 8:7, Jan 2024. URL: https://doi.org/10.3390/jmmp8010007, doi:10.3390/jmmp8010007. This article has 27 citations.

3. (bogdanova2024mesoscalesimulationof pages 5-7): Maria Bogdanova, Stanislav Chernyshikhin, Andrey Zakirov, Boris Zotov, Leonid Fedorenko, Sergei Belousov, Anastasia Perepelkina, Boris Korneev, Maria Lyange, Ivan Pelevin, Inna Iskandarova, Ella Dzidziguri, Boris Potapkin, and Alexander Gromov. Mesoscale simulation of laser powder bed fusion with an increased layer thickness for alsi10mg alloy. Journal of Manufacturing and Materials Processing, 8:7, Jan 2024. URL: https://doi.org/10.3390/jmmp8010007, doi:10.3390/jmmp8010007. This article has 27 citations.

4. (shrestha2018singletrackscanning pages 1-2): Subin Shrestha and Kevin Chou. Single track scanning experiment in laser powder bed fusion process. Procedia Manufacturing, 26:857-864, Jan 2018. URL: https://doi.org/10.1016/j.promfg.2018.07.110, doi:10.1016/j.promfg.2018.07.110. This article has 44 citations and is from a peer-reviewed journal.

5. (volpp2021fluctuationsoftracks pages 2-4): Joerg Volpp, Filippo Belelli, and Riccardo Casati. Fluctuations of tracks and layers during aluminium laser powder-bed fusion. Applied Sciences, 11:3132, Apr 2021. URL: https://doi.org/10.3390/app11073132, doi:10.3390/app11073132. This article has 4 citations.

6. (bogdanova2024mesoscalesimulationof pages 10-13): Maria Bogdanova, Stanislav Chernyshikhin, Andrey Zakirov, Boris Zotov, Leonid Fedorenko, Sergei Belousov, Anastasia Perepelkina, Boris Korneev, Maria Lyange, Ivan Pelevin, Inna Iskandarova, Ella Dzidziguri, Boris Potapkin, and Alexander Gromov. Mesoscale simulation of laser powder bed fusion with an increased layer thickness for alsi10mg alloy. Journal of Manufacturing and Materials Processing, 8:7, Jan 2024. URL: https://doi.org/10.3390/jmmp8010007, doi:10.3390/jmmp8010007. This article has 27 citations.

7. (wu2025improvingshieldinggas pages 2-4): H. Hugo Estrada Medinilla, Christopher J. Elkins, Jorge Mireles, Andres Estrada, and Ryan B. Wicker. Improving shielding gas flow distribution to enhance quality and consistency in metal laser powder bed fusion processes. Journal of Manufacturing and Materials Processing, 10:3, Dec 2025. URL: https://doi.org/10.3390/jmmp10010003, doi:10.3390/jmmp10010003. This article has 0 citations.

8. (maddison2022insitumonitoringanda pages 116-121): G Maddison. In-situ monitoring and control during laser powder bed fusion of nickel superalloys. Unknown journal, 2022.

9. (reijonen2020ontheeffect pages 3-4): Joni Reijonen, Alejandro Revuelta, Tuomas Riipinen, Kimmo Ruusuvuori, and Pasi Puukko. On the effect of shielding gas flow on porosity and melt pool geometry in laser powder bed fusion additive manufacturing. Additive Manufacturing, 32:101030, Mar 2020. URL: https://doi.org/10.1016/j.addma.2019.101030, doi:10.1016/j.addma.2019.101030. This article has 285 citations and is from a highest quality peer-reviewed journal.

10. (maddison2022insitumonitoringand pages 116-121): G Maddison. In-situ monitoring and control during laser powder bed fusion of nickel superalloys. Unknown journal, 2022.

11. (reijonen2020ontheeffect pages 4-5): Joni Reijonen, Alejandro Revuelta, Tuomas Riipinen, Kimmo Ruusuvuori, and Pasi Puukko. On the effect of shielding gas flow on porosity and melt pool geometry in laser powder bed fusion additive manufacturing. Additive Manufacturing, 32:101030, Mar 2020. URL: https://doi.org/10.1016/j.addma.2019.101030, doi:10.1016/j.addma.2019.101030. This article has 285 citations and is from a highest quality peer-reviewed journal.

12. (abeyta2024anexperimentalapproach pages 64-73): A Abeyta. An experimental approach for characterizing gas flow in the build chamber of laser powder bed fusion systems utilizing particle image velocimetry. Unknown journal, 2024.

13. (anwar2026acloserlook pages 3-5): Tasrif Ul Anwar and Nadia Kouraytem. A closer look at shielding gas in laser powder bed fusion: a review. Journal of Physics: Materials, 9(1):012003, Jan 2026. URL: https://doi.org/10.1088/2515-7639/ae2a70, doi:10.1088/2515-7639/ae2a70. This article has 1 citations.

14. (bosio2021laserpowderbed pages 47-49): F Bosio. Laser powder bed fusion of alsi10mg+ 4cu and alsi10mg alloys. Unknown journal, 2021.

15. (vallabh2022predictingmeltpool pages 11-15): Chaitanya Krishna Prasad Vallabh, Soumya Sridar, Wei Xiong, and Xiayun Zhao. Predicting melt pool depth and grain length using multiple signatures from in-situ single camera two-wavelength imaging pyrometry for laser powder bed fusion. Journal of Materials Processing Technology, 308:117724, Oct 2022. URL: https://doi.org/10.1016/j.jmatprotec.2022.117724, doi:10.1016/j.jmatprotec.2022.117724. This article has 55 citations and is from a domain leading peer-reviewed journal.

16. (geels2007metallographicandmaterialographic pages 392-395): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

17. (geels2007metallographicandmaterialographic pages 80-84): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

18. (geels2007metallographicandmaterialographic pages 77-80): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

19. (geels2007metallographicandmaterialographic pages 84-87): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

20. (mackenzie2005analyticalcharacterizationof pages 34-39): Analytical Characterization of Aluminum, Steel, and Superalloys This article has 119 citations.

21. (geels2007metallographicandmaterialographic pages 373-377): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

22. (geels2007metallographicandmaterialographic pages 146-150): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

23. (geels2007metallographicandmaterialographic pages 395-399): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

24. (geels2007metallographicandmaterialographic pages 399-402): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

25. (geels2007metallographicandmaterialographic pages 213-215): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

26. (tamadon2017developmentofmetallographic pages 3-5): Abbas Tamadon, Dirk Pons, Kamil Sued, and Don Clucas. Development of metallographic etchants for the microstructure evolution of a6082-t6 bfsw welds. ArXiv, 7:423, Oct 2017. URL: https://doi.org/10.3390/met7100423, doi:10.3390/met7100423. This article has 51 citations.

27. (tamadon2017developmentofmetallographic pages 1-3): Abbas Tamadon, Dirk Pons, Kamil Sued, and Don Clucas. Development of metallographic etchants for the microstructure evolution of a6082-t6 bfsw welds. ArXiv, 7:423, Oct 2017. URL: https://doi.org/10.3390/met7100423, doi:10.3390/met7100423. This article has 51 citations.

28. (geels2007metallographicandmaterialographic pages 231-234): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

29. (geels2007metallographicandmaterialographic pages 611-617): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

30. (smith2022meltpoolsprocess pages 29-33): Lonnie Smith. Melt pools, process parameters, and defects in lpbf uns n07718. Text, Jan 2022. URL: https://doi.org/10.1184/r1/19874881.v1, doi:10.1184/r1/19874881.v1. This article has 0 citations and is from a peer-reviewed journal.

31. (geels2007metallographicandmaterialographic pages 624-628): K. Geels, Db Fowler, W-U Kopp, and M. Rückert. Metallographic and materialographic specimen preparation, light microscopy, image analysis and hardness testing. ArXiv, Jan 2007. URL: https://doi.org/10.1520/mnl46-eb, doi:10.1520/mnl46-eb. This article has 210 citations.

32. (porrang2026evaluatingdifferentmethods pages 9-13): Bita Porrang, Muhammad Asim Ghaffar, and Ali Hosseini. Evaluating different methods to measure porosity in fused filament fabricated metals. Transactions of the Canadian Society for Mechanical Engineering, 50:1-9, Jan 2026. URL: https://doi.org/10.1139/tcsme-2025-0092, doi:10.1139/tcsme-2025-0092. This article has 4 citations and is from a peer-reviewed journal.

33. (porrang2026evaluatingdifferentmethods pages 6-9): Bita Porrang, Muhammad Asim Ghaffar, and Ali Hosseini. Evaluating different methods to measure porosity in fused filament fabricated metals. Transactions of the Canadian Society for Mechanical Engineering, 50:1-9, Jan 2026. URL: https://doi.org/10.1139/tcsme-2025-0092, doi:10.1139/tcsme-2025-0092. This article has 4 citations and is from a peer-reviewed journal.

34. (letenneur2020laserpowderbed pages 3-6): Morgan Letenneur, Pete Imbrogno, Amin Molavi-Kakhki, and Vladimir Brailovski. Laser powder bed fusion with intentionally-seeded porosity for prototyping of powder metallurgy parts. Journal of Manufacturing and Materials Processing, 4:119, Dec 2020. URL: https://doi.org/10.3390/jmmp4040119, doi:10.3390/jmmp4040119. This article has 11 citations.

35. (brika2020influenceofparticle pages 8-12): Salah Eddine Brika, Morgan Letenneur, Christopher Alex Dion, and Vladimir Brailovski. Influence of particle morphology and size distribution on the powder flowability and laser powder bed fusion manufacturability of ti-6al-4v alloy. Additive manufacturing, 31:100929, Jan 2020. URL: https://doi.org/10.1016/j.addma.2019.100929, doi:10.1016/j.addma.2019.100929. This article has 617 citations and is from a highest quality peer-reviewed journal.

36. (drobner2022theeffectof pages 23-30): E Drobner. The effect of heat transfer on microstructural development for inconel718 nickel-based superalloy in laser powder bed fusion. Unknown journal, 2022.

37. (zheng2021defectanalysisof pages 14-17): Zhi-Ping Zheng, L. Peng, and Di Wang. Defect analysis of 316 l stainless steel prepared by lpbf additive manufacturing processes. Coatings, 11:1562, Dec 2021. URL: https://doi.org/10.3390/coatings11121562, doi:10.3390/coatings11121562. This article has 34 citations.

38. (li2024simultaneousporedetection pages 7-10): Jiaming Li, Xiaoxun Zhang, Fang Ma, Shuxian Wang, and Yuanyou Huang. Simultaneous pore detection and morphological features extraction in laser powder bed fusion with image processing. Materials, 17:1373, Mar 2024. URL: https://doi.org/10.3390/ma17061373, doi:10.3390/ma17061373. This article has 9 citations.

39. (ellendt2021poreanalyzer—anopensourceframework pages 2-4): Nils Ellendt, Fabian Fabricius, and Anastasiya Toenjes. Poreanalyzer—an open-source framework for the analysis and classification of defects in additive manufacturing. Applied Sciences, 11:6086, Jun 2021. URL: https://doi.org/10.3390/app11136086, doi:10.3390/app11136086. This article has 13 citations.

40. (li2024simultaneousporedetection pages 1-2): Jiaming Li, Xiaoxun Zhang, Fang Ma, Shuxian Wang, and Yuanyou Huang. Simultaneous pore detection and morphological features extraction in laser powder bed fusion with image processing. Materials, 17:1373, Mar 2024. URL: https://doi.org/10.3390/ma17061373, doi:10.3390/ma17061373. This article has 9 citations.

41. (jaramilloisaza2023correlationofenergy pages 7-10): Catalina Jaramillo-Isaza, Oscar-Fabian Higuera-Cobos, July-Andrea Taborda-Ríos, Omar E. Lopez-Botello, and Patricia Zambrano-Robledo. Correlation of energy density and manufacturing variables of aa6061 through laser powder bed fusion and its effect on the densification mechanism. Metals, 13:1904, Nov 2023. URL: https://doi.org/10.3390/met13111904, doi:10.3390/met13111904. This article has 6 citations.

42. (riener2022processabilityofhighstrength pages 10-12): Kirstin Riener, Tino Pfalz, Florian Funcke, and Gerhard Leichtfried. Processability of high-strength aluminum 6182 series alloy via laser powder bed fusion (lpbf). The International Journal of Advanced Manufacturing Technology, 119:4963-4977, Jan 2022. URL: https://doi.org/10.1007/s00170-022-08673-8, doi:10.1007/s00170-022-08673-8. This article has 56 citations.

43. (li2024additivemanufacturingof pages 31-34): Ying-Jie Li. Additive manufacturing of 6061 and 7075 aluminium alloy with selective laser melting. Unknown journal, 2024. URL: https://doi.org/10.70675/5f083431z1407z40f1z83bfz19a675dc42f6, doi:10.70675/5f083431z1407z40f1z83bfz19a675dc42f6.