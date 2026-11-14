# Measuring what Thermo-Calc calculates (#262)

Thermo-Calc, its add-on modules and pycalphad with open databases predict a long list of quantities
(#262 lists them). This folder works out how we could **measure** each one on our own Al and Cu
alloys: atomized powder, LPBF single tracks, pads and coupons. It focuses on what helps the alloy
discovery campaign in #255. For each quantity it gives:
- the method;
- an instrument and where to find one;
- the sample workflow;
- the analysis, with code;
- how well it fits a self-driving-lab loop;
- which Thermo-Calc output it checks.

Then it ranks the ten measurements worth the most to #255.

**Status:**
- Nothing here has been run on a real sample yet.
- The SOPs are drafts.
- The scripts are tested only on synthetic data with known answers.
- No vendor or facility was contacted.

| Path | What it is |
|---|---|
| [`README.md`](README.md) | this page: short answers, ranking, matrix, notes for each quantity, contacts, verification |
| [`matrix.csv`](matrix.csv), [`ranking.csv`](ranking.csv) | the matrix and ranking as data, written by [`tables.py`](tables.py), which also refreshes the tables below |
| [`sops/`](sops/) | one-page SOP drafts for the top measurements |
| [`analysis/`](analysis/) | analysis scripts, with tests on synthetic data ([`test_analysis.py`](analysis/test_analysis.py)) |
| [`edison/`](edison/) | three Edison `LITERATURE_HIGH` searches: query, answer, references, artifacts, full trajectory |
| [`verify_dois.py`](verify_dois.py), [`doi-check.csv`](doi-check.csv) | every DOI in this folder checked against Crossref/DataCite |

## Short answers

- **Ten measurements carry most of the value for #255** (ranked in [§1](#1-ranked-shortlist-for-255)):
  1. composition by ICP-OES with O/N/H;
  2. Vickers hardness through an aging matrix;
  3. DSC/DTA solidification;
  4. Archimedes density with pore and crack counts;
  5. XRD phases and lattice parameter;
  6. eddy-current conductivity;
  7. single-track cross-sections for heat-source calibration;
  8. sub-size tensile;
  9. potentiodynamic corrosion;
  10. SEM/EBSD of tracks and pads.

  Eight of the ten can start in the next month, using powders we already have and the Utah P1 build (Dec 2–3).
  Eddy current waits on a meter, and corrosion on the reference electrodes (#221).
- **Quick wins for the next month** ([§1.2](#12-quick-wins-for-the-next-month)):
  - send the baseline powders out for ICP-OES and O/N/H;
  - DSC by mail-in at the University of Utah's Materials Characterization Lab;
  - XRD at BYU Chemistry;
  - Archimedes and Vickers on the P1 cubes;
  - single tracks on P1, run through [`melt_pool_calibration.py`](analysis/melt_pool_calibration.py).
- **Where it can be done** (facility pages checked on 2026-11-14, [§5](#5-where-and-who-to-contact)):
  - **BYU** has:
    - powder XRD with a 1200 °C stage (Chemistry XRD Facility);
    - SEM-EDS-EBSD, FIB and TEM (Electron Microscopy Facility);
    - ICP-OES (Geological Sciences, and the fee-for-service Environmental Analytical Lab);
    - the Concept Laser M2.
  - **Not found on any BYU page:** a DSC/DTA, laser flash, dilatometer, tensile frame, microhardness
    tester or particle sizer.
  - **Utah's Materials Characterization Lab** takes outside academics, including mail-in. It has:
    - a DSC/TGA to 1500 °C;
    - a dilatometer;
    - an Instron with Vickers testers;
    - laser-diffraction sizing;
    - He pycnometry.
  - **Utah Nanofab** adds SAXS, nanoindentation and X-ray CT.
  - **National labs** (by proposal) cover atom probe (ORNL CNMS), mail-in synchrotron powder
    diffraction (APS 11-BM), and neutron residual stress (SNS VULCAN; NIST BT-8).
- **Some outputs we can't measure in or near the lab:**
  - activities and chemical potentials;
  - single-crystal Cij;
  - liquid surface tension and viscosity;
  - Marangoni velocity.

  The matrix gives a proxy for each, or a specialist lab to send it to.
- **Code** ([§4](#4-analysis-code)):
  - **Seven scripts, with 11 tests that pass.** One of them, DSC fraction solid with a lag correction, fills
    a gap: no maintained open code for it was found.
  - **Our melt-pool model matches ArroyaveLab's `eagar-tsai`** (the package #238 tested) to 1.6 µm,
    about 80× faster, so it can fit absorptivity to many tracks.
  - **Measured phase boundaries export to ESPEI datasets and ORCHID-style rows.** That way new data for the
    systems #238 found nearly empty (Al–Si, Al–Mn–Cr–Zr, Cu–Al–Ni–Fe, Cu–Ni) plug straight into the
    pycalphad comparisons.

## 1. Ranked shortlist for #255

Each candidate is scored 1–5 on five criteria:
- **Info:** what it tells the campaign about strength, crack-free printing and whether the CALPHAD screen is right. It counts double.
- **TC check:** how directly it checks or calibrates Thermo-Calc and pycalphad, and fills ORCHID gaps.
- **Cost:** 5 is cheapest.
- **Effort:** hands-on time per alloy; 5 is least.
- **Speed:** time to first data; 5 is within two weeks.

The weights are in [`tables.py`](tables.py); change them and rerun it.

<!-- RANKING:START -->
| Rank | Measurement | Matrix rows | Info ×2 | TC check | Cost | Effort | Speed | Score /30 | Quick win | SOP |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Composition (ICP-OES) and O/N/H of every powder, plus one print per alloy | A4, PM1 | 5 | 5 | 3 | 4 | 4 | **26** | yes | [05](sops/05-composition-interstitials.md) |
| 2 | Vickers hardness as-built and through an aging matrix | M3, K6 | 5 | 4 | 5 | 4 | 3 | **26** | yes | [04](sops/04-hardness-conductivity-aging.md) |
| 3 | DSC/DTA: solidus, liquidus, fs(T), latent heat, hot-cracking indices | S1, S2, S5, T3 | 4 | 5 | 4 | 4 | 4 | **25** | yes | [01](sops/01-dsc-solidification.md) |
| 4 | Archimedes density, porosity type and crack density of cubes | T4, A5, S5, B3 | 5 | 3 | 5 | 4 | 3 | **25** | yes | [03](sops/03-density-porosity-cracks.md) |
| 5 | XRD phases and Al lattice parameter (powder, as-built, annealed) | P1, P4, T6 | 3 | 4 | 5 | 4 | 5 | **24** | yes | – |
| 6 | Eddy-current conductivity (%IACS), as-built and through the aging matrix | T8, T9, K6 | 3 | 4 | 4 | 5 | 3 | **22** | yes | [04](sops/04-hardness-conductivity-aging.md) |
| 7 | Single-track cross-sections and heat-source calibration | A1, A5 | 4 | 5 | 3 | 2 | 3 | **21** | yes | [02](sops/02-single-track-melt-pool.md) |
| 8 | Sub-size tensile on benchmarks and finalists | B1, M3 | 5 | 3 | 3 | 2 | 2 | **20** |  | – |
| 9 | Potentiodynamic polarization in NaCl (once the reference electrodes arrive, #221) | B5, P8 | 4 | 2 | 4 | 3 | 3 | **20** | yes | – |
| 10 | SEM/EBSD of tracks and pads: grains, CET, cell spacing, cracks | S6, A3, K5 | 4 | 3 | 3 | 2 | 3 | **19** |  | – |
| 11 | High-temperature XRD: CTE and phase changes on heating | T5 | 2 | 3 | 4 | 4 | 4 | **19** |  | – |
| 12 | Laser flash on 3-4 alloys to calibrate the conductivity relation | T8 | 2 | 4 | 2 | 4 | 2 | **16** |  | – |
| 13 | Calorimetric absorptivity on the desktop machine | A6 | 3 | 4 | 3 | 2 | 1 | **16** |  | – |
| 14 | TEM / SAXS / APT of finalist precipitates | K4 | 3 | 5 | 2 | 1 | 1 | **15** |  | – |
| 15 | Diffusion couples | K1 | 1 | 4 | 4 | 2 | 2 | **14** |  | – |
<!-- RANKING:END -->

Rows 11 and lower aren't in the top ten. They still matter:
- **High-temperature XRD** is cheap at BYU.
- **Laser flash** is needed once, to calibrate eddy current to thermal conductivity.
- **Absorptivity calorimetry** waits for the desktop machine.
- **TEM/SAXS/APT** are for the two finalists.

**Edison's three searches give similar rankings, with two differences** ([q2](edison/q2-lpbf-melt-pool/answer.md),
[q3](edison/q3-high-throughput-calibration/answer.md)):
- **The LPBF search puts powder characterization first.** Powder PSD, morphology and chemistry come first, then tracks, pads,
  cubes and cell spacing, all within a 40–80 g budget of fused powder per alloy. Powder PSD and shape by SEM is
  already in #256's weekly plan (#225), so it is left out of the ten here.
- **The high-throughput search ranks XRD and SEM/EDS first,** and puts nanoindentation mapping where hardness is here.

### 1.1 What each of the ten tells #255, and which Thermo-Calc output it checks

| # | Measurement | Tells #255 | Checks (Thermo-Calc / pycalphad) | Plugs into #238 as |
|---|---|---|---|---|
| 1 | Composition (ICP-OES) and O/N/H | Did the atomizer make what we asked for? How much Mg was lost in printing? How much oxide is in the powder? | Every calculation's input. Also the AM Module's evaporation mode | the composition every comparison is recalculated at |
| 2 | Vickers hardness + aging | The strength screen the optimizer uses before tensile; peak-aging response of Zr/Sc/Er alloys | The General Model Library yield strength; TC-PRISMA peak and over-aged strength and peak time | parity of measured vs predicted strength increments |
| 3 | DSC/DTA | Freezing range and hot-cracking indices (crack risk); incipient melting of as-built material (sets heat treatments) | Liquidus, solidus, Scheil fs(T), latent heat, eutectic fraction | new ZPF/invariant entries for Al–Si (no accepted ORCHID values), Al–Mn–Cr–Zr, Cu–Al–Ni–Fe, Cu–Ni; the AlSi10Mg and C63000 liquidus checks #238 couldn't do |
| 4 | Density, pores, cracks | Printability: lack of fusion, keyholing, cracking | AM Module printability map; Scheil-based crack indices | measured printability classes against the #249 keyhole benchmark |
| 5 | XRD phases + lattice parameter | Which phases form; how much solute LPBF traps | Phase constitution (Scheil vs equilibrium), lattice parameter, solvus | single-phase / two-phase ZPF points on annealed samples |
| 6 | Eddy-current conductivity | Solute in solution and aging kinetics in seconds per sample; thermal conductivity for the AM Module | Electrical resistivity model; TC-PRISMA matrix composition | resistivity parity; conductivity inputs for melt-pool models |
| 7 | Single tracks | Print parameters for the Utah and desktop builds; keyhole boundary | AM Module melt-pool width and depth, heat-source absorptivity | tracks for #249's ORCHID-style keyhole benchmark |
| 8 | Sub-size tensile | The paper's headline numbers vs AlSi10Mg and Scalmalloy | Yield strength models (calibrates the hardness-to-strength factor) | — |
| 9 | Corrosion | The paper's corrosion comparison (#255 "mechanical and corrosion properties") | TCAQ Pourbaix passive/active regions (qualitative) | — |
| 10 | SEM/EBSD of tracks and pads | Grain refinement by Al₃(Sc,Zr)/Al₃Zr, CET, cell spacing, crack paths | CET vs the AM Module's G and R; cooling rate; Zener-limited grain size | — |

### 1.2 Quick wins for the next month

Dates follow #256's schedule (P1 at Utah on Dec 2–3; gate G1 on Dec 4).

| By | Do | Uses | Gives |
|---|---|---|---|
| Nov 20 | **Ship the first chemistry batch:** the 6063 baseline powders (A1–A3), AlSi10Mg, and the C63000 powder from #219. Send to BYU's Environmental Analytical Lab (ICP-OES, fee-for-service), plus O/N/H at an outside lab ([SOP 05](sops/05-composition-interstitials.md)). Ask how they handle Si (#255's open question). #256 planned this for Jan 8; moving it up means every other comparison uses measured compositions. | sealed 5 g samples #256 already plans | measured compositions; oxygen |
| Nov 25 | **XRD** of the same powders at BYU Chemistry: phases plus the Al lattice parameter (`xrd_lattice.py`) | X'Pert Pro, 1 h each | phase IDs; supersaturation baseline |
| Dec 4 | **DSC** of the same powders by mail-in to Utah's Materials Characterization Lab: SDT 650 to 1500 °C; their DSC 3500 stops at 600 °C, below most Al liquidus temperatures ([SOP 01](sops/01-dsc-solidification.md)). Include a pure-Al standard. | 10–25 mg each | liquidus/solidus/fs(T) vs Thermo-Calc and pycalphad, and the first ORCHID-style rows (`espei_export.py`) |
| Dec 2–3 | **Single tracks at P1** on the Aconity MIDI: bare plate and one powder layer, Sobol blocks as in #243 | a few g of AlSi10Mg | heat-source calibration ([SOP 02](sops/02-single-track-melt-pool.md)) |
| Dec 11 | **Archimedes + sections + crack density** on the P1 cubes, with a wrought 6063 reference cube ([SOP 03](sops/03-density-porosity-cracks.md); set-up #144) | balance + density kit | printability classes |
| Dec 11 | **Vickers** on P1 cubes, and **start the aging matrix** on AlSi10Mg and 6063 ([SOP 04](sops/04-hardness-conductivity-aging.md)). Tester: Utah MCL (outside-academic access), until a BYU tester is found. | furnace + tester | hardness baseline; aging curves |
| Dec 11 | **Decide on an eddy-current meter**: none was found on any campus page. A used handheld unit is the cheapest high-throughput instrument on the list. | — | conductivity from January |
| when the electrodes arrive (#221) | **Corrosion baselines** on wrought 6063 and printed AlSi10Mg with the EZstat-Pro (#239) | potentiostat | corrosion baselines |

## 2. The matrix

Codes:
- **Access:**
  - `lab`: our lab, or equipment we would buy;
  - `BYU`: a BYU facility;
  - `UT`: a nearby university facility open to outside academics, mainly Utah's MCL and Nanofab;
  - `NL`: a national-lab user facility, by proposal (free for publishable work);
  - `svc`: a commercial service.
- **Cost**, rough estimates unless a source is given in §5:
  - capital: `$` < $10k, `$$` $10–50k, `$$$` $50–250k, `$$$$` > $250k;
  - per sample: `[$]` < $100, `[$$]` $100–500, `[$$$]` $500–2000, `[$$$$]` > $2000.
- **Throughput and automation:** H/M/L. **ID** links to the notes in §3.

<!-- MATRIX:START -->
| ID | Quantity | Method (direct; proxy) | Instrument and where | Access | Cost | Time / sample | Thru-put | Auto | Samples from | What it checks in Thermo-Calc |
|---|---|---|---|---|---|---|---|---|---|---|
| | **Phase equilibria** | | | | | | | | | |
| P1 | Phase identity, amounts and volume fractions | XRD + Rietveld; SEM-BSE area fractions (Delesse); EBSD phase maps; synchrotron XRD for phases < 1 vol% | PANalytical X'Pert Pro MPD (BYU Chemistry XRD); Apreo C + EDAX/TSL EBSD (BYU EMF); APS 11-BM mail-in | BYU; NL | [$] | 0.5-1 h scan | H | H | powder, DSC bead, annealed + quenched coupon, as-built cube | equilibrium phase fractions (annealed), Scheil fractions (DSC bead), metastable phases (as-built) |
| P2 | Phase compositions (tie-lines) | SEM-EDS on phases > 1-2 um; EPMA-WDS for accuracy; TEM-EDS or APT below 1 um | Apreo C EDS (BYU EMF); Cameca SX-50 EPMA (Utah microprobe); Tecnai TF20 STEM-EDS (BYU EMF) | BYU; UT | [$-$$] | 1-3 h | M | M | annealed + quenched coupons, DSC beads, diffusion couples | phase compositions; ZPF tie-line entries (espei_export.py) |
| P3 | Site fractions | Not practical for us. Rietveld occupancy (synchrotron/neutron) or APT for ordered phases; use the lattice parameter as the proxy | APS 11-BM; ORNL CNMS APT | NL | proposal | weeks | L | L | powder, coupon | sublattice model of L1_2 Al3(Sc,Zr,Er) and similar (indirect) |
| P4 | Solubility limits and solvus | Quench from a temperature series, then XRD lattice parameter (parametric method) and resistivity; DSC dissolution peaks; SEM for second phase | X'Pert Pro (BYU); eddy-current meter (buy); tube furnace | lab; BYU | $$ meter | 1 h per temperature | M | M | printed coupons (supersaturated), cast buttons | solvus of Al3Zr/Al3Sc/Al6Mn etc.; LPBF supersaturation vs equilibrium |
| P5 | Transformation temperatures | DSC/DTA (heating and cooling, several rates); dilatometry; resistivity vs temperature | TA SDT 650 DSC/TGA to 1500 C (Utah MCL); NETZSCH DSC 3500 to 600 C (Utah MCL); Anter dilatometer, ~50 mm rods (Utah MCL) | UT | [$] | 2-3 h | M | H (autosampler) | powder, chips | invariant reactions, solvus, eutectoid in NAB, transformation temperatures |
| P6 | Activities, chemical potentials, driving forces | Knudsen-effusion mass spectrometry or EMF cells (specialist labs). Proxy: phase boundaries (equal chemical potentials) and Mg/Zn evaporation loss | specialist academic labs | svc/academic | [$$$$] | weeks | L | L | bulk | activities (only via proxies for us) |
| P7 | Phase diagrams (sections, invariants) | Key alloys: DSC + XRD + SEM/EDS of annealed and quenched samples; diffusion couples/multiples for isothermal sections | combination of P1, P2, P5 | BYU; UT | [$-$$] | days per section | M | M | powder, buttons, couples | phase diagrams; new ORCHID/ESPEI entries for Al-Si, Al-Mn-Cr-Zr, Cu-Al-Ni-Fe, Cu-Ni |
| | **Aqueous** | | | | | | | | | |
| P8 | Pourbaix stability regions, pH, potential vs SHE | OCP and potentiodynamic polarization vs pH (ASTM G5/G59-style); immersion with XRD/Raman of products | EZstat-Pro potentiostat (lab, #221/#239); Gamry Reference 600+ (Utah Nanofab) | lab; UT | $ (have) | 1-2 h | M | H | polished coupons | TCAQ Pourbaix regions (qualitative: passive vs active) |
| | **Thermochemical** | | | | | | | | | |
| T1 | Heat capacity, enthalpy, entropy | DSC sapphire method (ASTM E1269) to ~550 C for Al; drop calorimetry above; S from integrating cp/T | SDT 650 (Utah MCL) or a dedicated DSC; drop calorimetry at specialist labs | UT; svc | [$] | 3 runs (blank, sapphire, sample) | M | H | powder, discs | cp, H, S |
| T2 | Heat of formation (intermetallics) | Solution or direct-reaction calorimetry | specialist academic labs | svc/academic | [$$$] | weeks | L | L | arc-melted intermetallics | formation enthalpies (none for Al-Cu in ORCHID, #238) |
| T3 | Latent heat, apparent heat release | DSC peak integration (SOP 01) | SDT 650 (Utah MCL) | UT | [$] | with T-liquidus run | M | H | powder | latent heat; Scheil heat release |
| | **Thermophysical** | | | | | | | | | |
| T4 | Density (solid) | Archimedes (SOP 03); He pycnometry of powder; X-ray density from lattice parameter | density kit on a 0.1/0.01 mg balance (lab); Anton Paar Ultrapyc 5000 (Utah MCL) | lab; UT | $ | 10 min | H | M | cubes, powder | density (molar volume) |
| T5 | Thermal expansion, lattice parameter vs T | High-temperature XRD; push-rod dilatometry (ASTM E228) | X'Pert Pro + Anton Paar HTK 1200 stage (BYU Chemistry); Anter dilatometer (Utah MCL) | BYU; UT | [$] | 4-8 h | M | H | powder (HT-XRD), 50 mm bars (dilatometer) | CTE, lattice parameter(T), density(T) |
| T6 | Lattice parameters (cubic) | XRD with Nelson-Riley extrapolation or Rietveld (xrd_lattice.py) | X'Pert Pro (BYU Chemistry) | BYU | [$] | 1 h | H | H | powder, polished coupons | lattice parameter; solute in solution |
| T7 | Liquid viscosity and surface tension | Oscillating drop (EML/ESL), sessile drop, maximum bubble pressure, oscillating-cup viscometry; Al oxide skin is the main error | specialist levitation labs | svc/academic | [$$$$] | weeks | L | L | a few grams of alloy | liquid viscosity, surface tension (AM-module Marangoni inputs) |
| T8 | Thermal diffusivity and conductivity | Laser flash (ASTM E1461) + DSC cp + density, k = alpha*rho*cp; eddy-current conductivity with a fitted Smith-Palmer relation for the rest | commercial LFA service for 3-4 calibration alloys; eddy-current meter (buy) | svc; lab | [$$] LFA; $$ meter | LFA 1 day; eddy current 2 min | L (LFA) / H (EC) | M / H | 10-12.7 mm discs ~2 mm thick (LFA); 10 mm coupons (EC) | thermal conductivity and diffusivity (AM-module inputs) |
| T9 | Electrical resistivity and conductivity | Eddy current, %IACS (ASTM E1004); four-point probe; four-wire bars in a furnace for rho(T) | handheld eddy-current meter (buy); four-point probe (BYU IML, Utah Nanofab) | lab; BYU | $$ | 2 min | H | H | coupons >=10 mm, polished sections | electrical resistivity model; solute in solution; aging |
| T10 | Interfacial energy | Not measured directly: fit to coarsening rate (LSW, kinetics.py) or to TC-PRISMA PSD evolution | via K1 or S1 data | - | - | - | - | - | aged coupons | interfacial energy (TC-PRISMA input) |
| | **Mechanical** | | | | | | | | | |
| M1 | Young's, shear and bulk moduli | Impulse excitation (ASTM E1876) on printed bars; ultrasonic pulse-echo velocities; nanoindentation (Oliver-Pharr) | IET instrument (buy or service); Hysitron TI Premier (Utah Nanofab) | lab/svc; UT | $$ / [$] | 10 min (IET) | H | H | bars ~40x8x2 mm, coupons | E, G, K (polycrystal averages of Thermo-Calc's Cij) |
| M2 | Single-crystal elastic constants C11, C12, C44 | Resonant ultrasound on single crystals: not practical. Compare Voigt-Reuss-Hill averages of predicted Cij with M1 | - | - | - | - | L | L | - | Cij (only through averages) |
| M3 | Hardness and yield strength | Vickers (ASTM E384) incl. aging series (SOP 04); sub-size tensile (ASTM E8); shear punch / small punch; indentation plastometry | Vickers testers and Instron 5969 (Utah MCL); 20 kip frame (#256); Plastometrex PLX-Benchtop (svc) | UT; lab; svc | [$] | 10 min (HV); 1 h (tensile) | H (HV) | H (HV auto-stage) | cubes, sections, bars | General Model Library yield strength; TC-PRISMA peak/over-aged strength |
| | **Solidification** | | | | | | | | | |
| S1 | Liquidus, solidus, incipient melting, freezing range | DSC/DTA, 3 heating rates, extrapolated to zero rate (SOP 01) | TA SDT 650 (Utah MCL; mail-in) | UT | [$] | 2-2.5 h per run | M | H | powder (10-25 mg), printed chips | equilibrium and Scheil liquidus/solidus; ORCHID gaps (AlSi10Mg, NAB, Cu-Ni) |
| S2 | Fraction solid curve, solidification path, fraction eutectic | DSC partial areas with lag correction (dsc_solidification.py); eutectic area fraction on DSC beads; phase sequence by SEM/EDS | SDT 650 + BYU EMF | UT; BYU | [$] | with S1 | M | H | powder, DSC beads | Scheil fs(T), solidification path, eutectic fraction |
| S3 | Microsegregation, partition coefficients | EDS/WDS grid maps on DSC beads or castings, sorted (WIRS-type) and compared with Scheil; APT/TEM-EDS for LPBF cells | Apreo C EDS (BYU EMF); SX-50 EPMA (Utah); APT (ORNL CNMS) | BYU; UT; NL | [$$] | 2-4 h | M | M | DSC beads, castings, tracks | Scheil/back-diffusion segregation; solute trapping in LPBF |
| S4 | Shrinkage | Solid density (T4) vs liquid density (levitation, specialist) | - | svc/academic | [$$$$] | weeks | L | L | - | solidification shrinkage (low priority for LPBF) |
| S5 | Hot-tearing tendency | Crack density on pads and cubes (SOP 03); Kou and CSC indices from measured fs(T); constrained-rod casting | optical microscope + Fiji (lab); DSC (S1) | lab; UT | $ | 1 h per batch | H | M | pads, cubes, DSC | Scheil-based hot-cracking indices; printability (cracking axis) |
| S6 | Columnar-to-equiaxed transition, grain size, texture | EBSD on tracks and pads (ASTM E2627-style grain size); Barker's etch under polarized light for Al | Apreo C + TSL OIM (BYU EMF) | BYU | [$$] | 2-4 h | M | M | tracks, pads | CET vs AM-module G-R; inoculation by Al3(Sc,Zr) |
| | **Kinetics** | | | | | | | | | |
| K1 | Interdiffusion, intrinsic, tracer diffusion; mobility | Diffusion couples + EDS/EPMA line scans, Boltzmann-Matano / Sauer-Freise (pyDiffusion); tracer needs radiotracer labs | furnace (lab); SX-50 EPMA (Utah) | lab; UT | [$$] | days (anneal) + 2 h scan | L | M | bonded or cast couples | mobility databases; interdiffusion coefficients |
| | **DICTRA** | | | | | | | | | |
| K2 | Homogenization, dissolution and growth of second phases | EDS line scans and SEM area fractions vs anneal time; DSC incipient melting before/after | BYU EMF; SDT 650 | BYU; UT | [$$] | 2-4 h | M | M | as-built and annealed coupons | DICTRA homogenization and dissolution kinetics |
| K3 | Interdiffusion at coatings, dissimilar joints; PWHT | EDS line scans + hardness traverses across interfaces (track/plate, DED Cu on steel) | BYU EMF; Vickers | BYU; UT | [$$] | 2 h | M | M | tracks on plate, DED walls | DICTRA interdiffusion profiles |
| | **TC-PRISMA** | | | | | | | | | |
| K4 | Precipitate size distribution, number density, volume fraction, compositions | TEM/STEM dark field with stereological (foil thickness) correction; SAXS; APT | Tecnai TF20 and Iliad (BYU EMF); Anton Paar SAXSpoint 5.0 (Utah Nanofab); LEAP (ORNL CNMS, proposal) | BYU; UT; NL | [$$-$$$$] | 1-3 days | L | L | aged coupons (finalists only) | TC-PRISMA PSD, mean radius, number density, volume fraction, matrix composition |
| K5 | Grain growth and Zener pinning | EBSD grain size vs anneal time and temperature | BYU EMF | BYU | [$$] | 2-4 h | M | M | annealed coupons | grain growth, Zener-limited grain size |
| K6 | TTP and CCT diagrams | Hardness + conductivity aging matrix (SOP 04); DSC at several rates (Kissinger, kinetics.py) | Vickers; eddy-current meter; DSC | lab; UT | $ | 16 conditions per alloy | H | H | small coupons from one cube row | TTP peak times, apparent activation energies |
| | **AM Module** | | | | | | | | | |
| A1 | Melt-pool width, depth, length; peak temperature | Single-track cross-sections and top views (SOP 02); length from high-speed imaging or longitudinal sections; peak T needs calibrated two-colour pyrometry | Utah Aconity MIDI, BYU Concept Laser M2, desktop LPBF (#260); optical/SEM | UT; BYU; lab | [$] | ~18 tracks per mount | M | M | single tracks on plate and on one powder layer | melt-pool size and regime; heat-source calibration (absorptivity, beam radius) |
| A2 | Marangoni flow velocity | In-situ X-ray imaging with tracer particles | APS 32-ID (proposal; status after APS-U unconfirmed) | NL | proposal | beamtime | L | L | tracks | fluid-flow velocity (indirect: pool shape) |
| A3 | Thermal gradient G, solidification rate R, thermal history | Cell/dendrite spacing -> cooling rate; R = v cos(theta) from pool shape; thermocouples in the plate; IR camera | BYU EMF (cell spacing); thermocouples (lab) | BYU; lab | [$] | 1-2 h | M | M | tracks, pads | G, R and cooling rate; thermal history |
| A4 | Composition change by evaporation | ICP-OES of powder vs printed part (SOP 05); EDS across tracks | Thermo iCAP 7400 (BYU EAL / Geological Sciences) | BYU; svc | [$-$$] | 1 day turnaround | M | M | powder + printed chips | evaporation mode (Mg, Zn, Li loss) |
| A5 | Printability maps (keyholing, lack of fusion, balling) | Tracks (regime, balling) + cubes (density, pore type, cracks), SOP 02 and 03 | as A1 + density kit | lab; UT | [$] | per build | M | M | tracks, cubes | printability map; #249 keyhole criteria |
| A6 | Laser absorptivity | Calorimetric (thin disc + thermocouples, Trapp et al. 2017-type); integrating-sphere reflectance at 1070 nm; inverse from A1 | home-built calorimeter on the desktop LPBF; spectrophotometer with sphere | lab | $ | 1 h | M | M | discs, powder layers | absorptivity used by the heat source |
| | **Model libraries** | | | | | | | | | |
| L1 | Ordered-phase solvus (Al3(Sc,Zr) L1_2 analogue of the Ni library) | DSC dissolution; resistivity after anneals; XRD | as P4/P5 | UT; lab | [$] | - | M | M | aged coupons | L1_2 solvus |
| L2 | Alloy colour (noble metals) | Spectrophotometer, CIELAB on polished Cu alloys | benchtop spectrophotometer | lab/svc | $ | 5 min | H | H | polished coupons | optical properties (Cu family only) |
| L3 | Steel, Ni-APB, Ti libraries | Not relevant to Al and Cu alloys | - | - | - | - | - | - | - | - |
| | **Process Metallurgy** | | | | | | | | | |
| PM1 | Inclusions, oxide content | O/N/H by inert gas fusion; SEM of powder cross-sections for oxide films | LECO TCH 600 (Utah powder metallurgy lab, access not stated); commercial labs | UT; svc | [$-$$] | days turnaround | M | L | sealed powder | inclusion/oxide content (slag and steel outputs not relevant) |
| | **Beyond Thermo-Calc** | | | | | | | | | |
| B1 | Stress-strain curve, work hardening, ductility | Sub-size tensile (ASTM E8); indentation plastometry for small coupons | Instron 5969 (Utah MCL); 20 kip frame (#256); Plastometrex (svc) | UT; lab; svc | [$$] | 1 h | L | M | printed bars | (validates strength models; needed for the paper) |
| B2 | Fatigue, creep, cryogenic tensile (#254) | ASTM-type fatigue and creep; tensile at 77 K | commercial labs | svc | [$$$-$$$$] | weeks | L | L | finalist bars | (finalists only; not before Feb 28) |
| B3 | Porosity and keyhole porosity | Archimedes + sections (SOP 03); X-ray CT | Zeiss Xradia 620 Versa (Utah Nanofab) | lab; UT | [$-$$] | 10 min / 2-4 h CT | H / L | M | cubes | (printability) |
| B4 | Residual stress | Bridge-curvature specimens (cheap); XRD sin^2(psi); neutron diffraction; contour method | in-house bridge test; VULCAN at SNS (mail-in proposal); NIST BT-8; commercial contour | lab; NL; svc | $ / proposal | 1 h (bridge) | M | L | bridge specimens, coupons | (distortion, cracking) |
| B5 | Corrosion rate | Potentiodynamic polarization and Tafel/EIS; immersion mass loss; salt fog | EZstat-Pro (lab); Gamry (Utah Nanofab) | lab; UT | $ (have) | 1-2 h | M | H | polished coupons | (paper requirement; Pourbaix check P8) |
| B6 | Powder PSD, shape, flowability, apparent and tap density | SEM image analysis (ISO 13322-1, #225); laser diffraction; Hall/Carney funnels; tap density | BYU EMF; Beckman Coulter LS230 (Utah MCL); SALD 2300 (Utah PM lab); funnels (buy) | BYU; UT; lab | $ | 30 min | H | M | sieved powder | (printability; already in #256's weekly plan) |
| B7 | Spatter and vapour plume | High-speed imaging with laser illumination; schlieren | rented high-speed camera | svc | $$ rental | per build | L | L | tracks | (evaporation, keyholing) |
<!-- MATRIX:END -->

## 3. Notes for each quantity

Each card gives what the matrix can't:
- the workflow from what we already make;
- the analysis;
- how it would run in the self-driving loop.

The "Samples" lines assume:
- **powder:** the 20–63 µm cut of an atomizer run;
- **tracks / pads / cubes:** from Utah P-sessions, the M2 (#243) or the desktop machine (#260);
- **buttons:** remelted powder or the crucible remnant.

The cups and plugs (#250) are atomizer feedstock, not samples. Analyse their bar and master-alloy stock only for the
mass balance (SOP 05).

### Phase equilibria (P1–P7)
- **Phases and fractions (P1).**
  - *Samples:* powder as atomized (rapidly solidified); DSC beads (closer to Scheil); coupons annealed
    long enough to equilibrate and then quenched (equilibrium).
  - *Analysis:* Rietveld in GSAS-II or Profex/BGMN for phase fractions, and BSE area fractions in Fiji, which
    equal volume fractions on a random section.
  - *Time:* 30–60 min per scan.
  - *Loop fit:* XRD with a sample changer is the most automatable structural measurement. It runs on
    composition-graded samples by mapping. A synchrotron (APS 11-BM mail-in) finds phases below
    ~1 vol% that a lab diffractometer misses.
  - *Checks:* equilibrium vs Scheil phase constitution.
- **Phase compositions (P2).**
  - EDS is fine for intermetallics larger than 1–2 µm at 10–15 kV. For tie-lines worth publishing, use EPMA-WDS (Utah microprobe).
  - Phases below 1 µm (LPBF cell walls) need STEM-EDS or APT.
  - *Analysis:* each tie-line becomes one ZPF entry in `espei_export.py`.
- **Site fractions (P3):** not measurable for us. The proxy is the lattice parameter (T6).
- **Solubility and solvus (P4):**
  - Quench coupons from a temperature series, then measure the Al lattice parameter (XRD) and resistivity.
    Both fall as solute leaves solution.
  - DSC dissolution peaks give the solvus on heating.
  - *Checks:* the equilibrium solvus, and how far LPBF exceeds it (supersaturation of Mn, Zr, Sc).
- **Transformation temperatures (P5):**
  - DSC/DTA ([SOP 01](sops/01-dsc-solidification.md)).
  - Dilatometry needs ~50 mm rods on Utah's Anter, longer than our coupons.
  - HT-XRD (T5) is the powder alternative.
- **Activities and driving forces (P6):**
  - No practical direct route. Knudsen-effusion mass spectrometry and EMF cells exist only at specialist labs.
  - Phase boundaries constrain chemical potentials indirectly. Mg/Zn loss in printing (A4) depends on Mg/Zn activity in the melt.
- **Phase diagrams (P7):**
  - Key-sample approach: P1 + P2 + P5 on a few alloys spanning a section.
  - Diffusion multiples give an isothermal section from one sample ([Edison q3 §1](edison/q3-high-throughput-calibration/answer.md)).
  - This is how the ORCHID gaps get filled (§1.1, §4.2).
- **Pourbaix (P8):**
  - OCP and potentiodynamic polarization in NaCl at several pH, with the EZstat-Pro.
  - Corrosion products by XRD or Raman.
  - *Checks:* which side of the predicted passive/active boundaries the alloy sits, qualitatively.

### Thermochemical and thermophysical (T1–T10)
- **cp, H, S (T1):**
  - DSC sapphire method (ASTM E1269): blank, sapphire and sample runs.
  - Below ~550 °C for Al; above that, drop calorimetry at a specialist lab.
  - S comes from integrating cp/T, not from a separate measurement.
- **Heat of formation (T2):** solution or direct-reaction calorimetry, specialist only. #238 found no
  formation enthalpies for Al–Cu in ORCHID, so a collaborator with a calorimeter would add real data there.
- **Latent heat (T3):** from the DSC peak area (SOP 01). Edison found an AlSi5Cu study where DSC latent heats of
  424–438 kJ/kg compared with 434–456 kJ/kg from Thermo-Calc ([Djurdjevic et al. 2025](https://doi.org/10.3390/met15091045),
  via [Edison q1](edison/q1-thermophysical-solidification/answer.md)). That is the scale of agreement to expect.
- **Density (T4):** Archimedes ([SOP 03](sops/03-density-porosity-cracks.md)). Use the He pycnometry density of the
  powder as the reference for porosity in new alloys (Utah MCL Ultrapyc 5000). X-ray density from the lattice
  parameter is a cross-check.
- **CTE and lattice parameter vs T (T5):** high-temperature XRD on the X'Pert's HTK 1200 stage. One powder run gives the Al lattice
  parameter from room temperature to near the solidus, plus any phase change on heating. It is cheaper than making
  dilatometer rods.
- **Lattice parameter (T6):** `xrd_lattice.py`, Nelson–Riley extrapolation. In the synthetic test, a 50 µm
  sample displacement biased a plain average of the a_hkl by +0.0010 Å. The extrapolation removed it (4.0560 Å
  recovered). Calibrate the line positions with NIST SRM 640 (Si) or 660 (LaB₆).
- **Liquid viscosity and surface tension (T7):**
  - Levitation (oscillating drop), sessile drop, maximum bubble pressure, oscillating cup.
  - Al's oxide skin dominates the error, so only specialist labs get usable numbers.
  - Low priority for #255; the AM Module's Marangoni term is checked indirectly through pool shape (A1).
- **Thermal diffusivity and conductivity (T8):**
  - Laser flash (ASTM E1461) on ~12.7 mm × 2–3 mm discs gives α. Then k = α·ρ·c_p.
  - Measure 3–4 alloys by laser flash, fit the Smith–Palmer constants in k = A·L₀·T/ρ_e + B (`conductivity.py`), and
    get k for the rest from %IACS in seconds.
  - Edison's sources put the lattice term for Al alloys at 10.5–12.6 W/m/K
    ([Edison q1 §3](edison/q1-thermophysical-solidification/answer.md)); we fit our own.
  - *Checks:* the conductivity the AM Module uses.
- **Electrical resistivity (T9):**
  - Eddy current (%IACS, ASTM E1004-type) needs a flat area of about 10 mm. 5 mm cubes are too small for most probes.
  - A four-point probe on a polished face, or four-wire bars, are the alternatives.
  - 100 % IACS = 1.7241 µΩ·cm.
  - Resistivity is additive over solute (Matthiessen's rule), so the drop during aging tracks precipitation.
  - Runs at ~1 min per sample: the best throughput on the list.
- **Interfacial energy (T10):** not measured directly. Fit it from the coarsening rate (LSW in `kinetics.py`, with
  K = 8γc_eV_m²D/9RT) or from TC-PRISMA fits to PSD evolution (K4).

### Elastic and mechanical (M1–M3)
- **Moduli (M1):**
  - Impulse excitation (ASTM E1876) on printed bars about 40 × 8 × 2 mm takes minutes and gives E and G.
  - Ultrasonic pulse-echo velocities give E, G and ν on coupons.
  - Nanoindentation (Utah Nanofab) gives a local modulus, but pile-up in soft Al biases it.
- **Single-crystal Cij (M2):** compare Voigt–Reuss–Hill averages of the predicted Cij with M1, since we can't make single crystals.
- **Hardness and yield strength (M3):** Vickers (ASTM E384, SOP 04).
  - σy ≈ HV/3 (Tabor) is only a screen. Calibrate it against our own tensile bars.
  - Profilometry-based indentation plastometry gives a full stress–strain curve from one indent on a small coupon.
    Edison flags it as specialized equipment; the PLX instrument is commercial ([Edison q3 §5](edison/q3-high-throughput-calibration/answer.md)).
  - A send-out PIP test on finalists would stretch scarce tensile powder.

### Solidification (S1–S6)
- **Liquidus, solidus, incipient melting, freezing range (S1):** [SOP 01](sops/01-dsc-solidification.md).
  - Use 3 heating rates, extrapolated to zero rate.
  - Don't use cooling curves for the liquidus: they undercool.
  - Heat 1 on as-atomized powder shows incipient melting of segregated material; Heat 2 on the solidified bead is closer to Scheil.
  - An Al-319 study found the first DSC heating closer to equilibrium and the Scheil curve closer to strongly
    segregated material ([Zhang et al. 2017](https://doi.org/10.1007/s11661-017-4235-2), via Edison q1).
  - **Gaps #238 couldn't fill:**
    - #238 found no published Thermo-Calc liquidus or solidus for AlSi10Mg or NAB;
    - the open Cu database misses the C63000 liquidus by +70 K.
- **fs(T), path, eutectic fraction (S2):** `dsc_solidification.py`. It does the baseline (linear or sigmoidal),
  the Tian lag correction, the partial areas and the comparison with a Scheil curve.
  - In the synthetic test, fs(T) matched the true Scheil curve to within 0.05 K up to fs = 0.8 once the lag was corrected.
    Without the correction the liquidus read 1.5 K high.
  - The DSC smears the eutectic plateau, so at fs = 0.9 the error is 6.5 K. Use the eutectic area fraction on the DSC bead (Fiji) instead.
- **Microsegregation (S3):**
  - EDS/WDS point grids on DSC beads or castings, sorted by composition and plotted against Scheil.
  - In LPBF cells the partition coefficient moves toward 1 (solute trapping). Measuring that needs STEM-EDS or APT, so only for finalists.
- **Shrinkage (S4):** needs the liquid density from levitation. Low priority for LPBF.
- **Hot tearing (S5):** the most useful index for #255. Large columnar grains and periodic cracks are why
  7075 and 6061 couldn't be printed until nucleant nanoparticles were added ([Martin et al. 2017](https://doi.org/10.1038/nature23894),
  checked in the abstract).
  - Measure crack density on pads and cubes (SOP 03).
  - Compute Kou's index, max |dT/d(fs^½)| near fs → 1 ([Kou 2015](https://doi.org/10.1016/j.actamat.2015.01.034)),
    and the Clyne–Davies CSC, (T₀.₉₀ − T₀.₉₉)/(T₀.₄₀ − T₀.₉₀), from both the *measured* and the Scheil fs(T).
  - Edison's sources report qualitative agreement of both indices with LPBF cracking in Al–Si, 5083 and 7xxx alloys
    ([Hyer et al. 2020](https://doi.org/10.1007/s11669-020-00844-y), via Edison q1).
  - Papers differ on the fs^½ window for Kou's index, so the script takes it as an argument and reports it.
  - A constrained-rod casting mold is a cheap in-house extra.
- **CET, grain size, texture (S6):** EBSD of tracks and pads at the BYU EMF (Apreo C with TSL OIM).
  - Map whole melt pools at a coarse step, then 0.05–0.2 µm steps at pool boundaries for Sc/Zr-refined grains (Edison q2 §4).
  - Barker's etch under polarized light is a cheap first look.
  - *Checks:* the CET predicted from the AM Module's G and R.

### Kinetics, DICTRA, TC-PRISMA (K1–K6)
- **Diffusion (K1):**
  - Bonded or cast couples, annealed, then EDS/EPMA line scans.
  - Analyse with Sauer–Freise or Boltzmann–Matano in [pyDiffusion](https://github.com/zhangqi-chen/pyDiffusion)
    ([paper](https://doi.org/10.5334/jors.255)), or with kawin's diffusion-couple example.
  - Mobility data for Al binaries already exist, so this ranks last for #255. A Cu–Ni couple is still a good first
    validation (#238 found no accepted Cu–Ni invariants).
- **Homogenization, dissolution, interfaces (K2, K3):**
  - EDS line scans and SEM area fractions against anneal time.
  - DSC shows incipient melting disappearing as segregation homogenizes.
  - Hardness traverses across track/plate and DED Cu/steel interfaces.
- **Precipitates (K4):**
  - TEM/STEM dark field with a foil-thickness correction, at BYU EMF (Tecnai TF20, Iliad).
  - SAXS for mean size and volume fraction (Utah Nanofab SAXSpoint 5.0); fit with SasView or McSAS3.
  - APT for compositions and number density (ORNL CNMS, by proposal).
  - Finalists only: these are the slowest and costliest rows. They calibrate TC-PRISMA's interfacial energy and nucleation parameters.
- **Grain growth and Zener pinning (K5):** EBSD grain size against anneal time and temperature.
- **TTP (K6):** the SOP 04 aging matrix.
  - Time to peak hardness at 3–4 temperatures gives an Arrhenius Q (`kinetics.py`).
  - Resistivity gives JMAK n and k(T).
  - DSC precipitation peaks at several rates give a Kissinger activation energy
    ([Kissinger 1957](https://doi.org/10.1021/ac60131a045)).
  - *Checks:* TC-PRISMA TTP curves, and kawin as the open alternative
    ([kawin](https://github.com/materialsgenomefoundation/kawin), [paper](https://doi.org/10.1016/j.actamat.2023.118988)).

### Additive Manufacturing Module (A1–A6)
- **Melt pool (A1):** [SOP 02](sops/02-single-track-melt-pool.md). Edison's LPBF search recommends:
  - 20–30 power–speed conditions, two tracks each;
  - at least three transverse sections per track;
  - longitudinal sections near the keyhole transition;
  - bare plate and powder layer;
  - fitting absorptivity to width and depth, with 20–30 % of conditions held out.

  That uses under 1 g of fused powder ([Edison q2 §10](edison/q2-lpbf-melt-pool/answer.md)). Peak temperature
  needs a calibrated two-colour pyrometer; skip it.
- **Marangoni velocity (A2):**
  - Only in-situ X-ray imaging with tracer particles measures it (APS 32-ID by proposal; its status after the APS Upgrade is unconfirmed).
  - Ultrahigh-speed synchrotron X-ray imaging is how the conduction-to-keyhole threshold was measured,
    in a Ti alloy ([Cunningham et al. 2019](https://doi.org/10.1126/science.aav4687), checked in the abstract).
- **G, R, thermal history (A3):**
  - Cell spacing λ = A·Ṫ⁻ⁿ gives the cooling rate, but A and n must be fitted for each alloy, not
    borrowed from cast Al–Si (Edison q2 §3).
  - R = v·cos θ along the pool boundary.
  - Thermocouples in the plate give the macroscopic history.
- **Evaporation (A4):**
  - ICP-OES of powder vs prints from low-, nominal- and high-energy conditions (SOP 05), using an ICP-AES method
    for Al alloys (ASTM E3061, per Edison q2 §5).
  - EDS is too coarse for ~1 % relative Mg loss.
  - *Checks:* the AM Module's evaporation mode, for Al–Mg(–Sc–Zr) in particular.
- **Printability map (A5):**
  - Tracks set the keyhole and balling boundaries, and cubes set lack of fusion.
  - Score the AM Module and the open criteria from #249 on the same classes.
- **Absorptivity (A6):**
  - Calorimetry on thin discs measured 1070 nm absorptivity for Al 1100, 316L and W
    ([Trapp et al. 2017](https://doi.org/10.1016/j.apmt.2017.08.006)).
  - Powder layers absorbed about twice as much as bare discs at low power, and absorptivity rose again once keyholes formed.
  - A home-built calorimeter fits the desktop machine (#260), but only after the machine works.
  - Until then, the fitted absorptivity from A1 is the number.

### Model libraries, Process Metallurgy (L1–L3, PM1)
- **Steel, Ni-APB and Ti libraries** don't apply to Al or Cu alloys.
- **Ordered-phase solvus:** for us, the L1₂ Al₃(Sc,Zr) solvus. Measure it as for P4/P5.
- **Alloy colour (L2):** only for Cu-family alloys. A benchtop spectrophotometer (CIELAB) takes minutes.
- **Process Metallurgy:**
  - Its slag and steel outputs don't apply.
  - What does apply is oxide in the powder: O by inert gas fusion and oxide films in SEM cross-sections (PM1).

### Beyond Thermo-Calc (B1–B7)
- **Tensile (B1):**
  - Sub-size ASTM E8 bars on Utah's Instron 5969 (50 kN) or the 20 kip frame in #256.
  - Finalists go to an outside lab, as #255 plans.
- **Fatigue, creep, cryogenic (B2):** commercial, finalists only, after Feb 28. #254 covers the cryogenic case.
- **Porosity (B3):**
  - Archimedes and sections (SOP 03).
  - µCT on Utah Nanofab's Xradia 620 Versa for 2–3 coupons, to tell lack-of-fusion pores from keyhole pores.
- **Residual stress (B4):**
  - Released-cantilever (bridge) specimens are cheap and repeatable on small Al coupons. Edison notes that XRD sin²ψ on Al
    suffers from texture, weak peaks and an unknown stress-free spacing (q2 §7).
  - For mapping, neutrons: VULCAN at SNS takes mail-in proposals. HFIR's HB-2B is off until about February 2027.
- **Corrosion (B5):**
  - Potentiodynamic polarization with the EZstat-Pro.
  - Fit with [PolCurveFit](https://github.com/Meekevanede/PolCurveFit) ([paper](https://doi.org/10.5006/4171))
    and EIS with [impedance.py](https://github.com/ECSHackWeek/impedance.py).
  - Scanning droplet cells are faster but custom-built (Edison q3 §5).
- **Powder (B6):**
  - PSD and shape from SEM (#225).
  - Laser diffraction at Utah's MCL (LS230) as a cross-check.
  - Hall/Carney flow and tap density with cheap funnels.
  - O/N/H (SOP 05).
- **Spatter and plume (B7):** high-speed imaging at 5–20 kfps or more (Edison q2 §8), with a rented camera, once the desktop machine runs.

## 4. Analysis code

All scripts are in [`analysis/`](analysis/). Each one runs `--demo` on synthetic data, and
`python -m pytest -q test_analysis.py` runs 11 tests (all pass, about 11 s).

| Script | Turns | Into | Test |
|---|---|---|---|
| [`dsc_solidification.py`](analysis/dsc_solidification.py) | DSC/DTA heat flow | solidus, liquidus, fs(T), latent heat, Kou and CSC indices, ΔT vs a Scheil/equilibrium curve, zero-rate extrapolation, τ from a pure-metal peak | recovers L within 1 %, liquidus within 0.5 K, and τ within 5 % |
| [`melt_pool_calibration.py`](analysis/melt_pool_calibration.py) | track width/depth | absorptivity (global and per track), regime, keyhole number Ke, AM Module bias/RMSE | recovers η = 0.31 within 0.02 from noisy tracks |
| [`check_vs_eagar_tsai.py`](analysis/check_vs_eagar_tsai.py) | – | cross-check against ArroyaveLab `eagar-tsai` 0.6.0 | W and D agree within 1.6 µm at 3 settings |
| [`density_porosity.py`](analysis/density_porosity.py) | weighings; micrographs | density with uncertainty (Tanaka water density); Otsu pore fraction | 1.0 % porosity recovered; water density at 20 °C = 998.207 kg/m³ |
| [`conductivity.py`](analysis/conductivity.py) | %IACS, V/I | resistivity, Wiedemann–Franz and fitted Smith–Palmer k, aging fraction | constants recovered |
| [`kinetics.py`](analysis/kinetics.py) | Tp(β), f(t), t_peak(T), r(t) | Kissinger Ea, JMAK n and k, Arrhenius Q, LSW K and γ | Ea, Q, n recovered |
| [`xrd_lattice.py`](analysis/xrd_lattice.py) | peak positions | Nelson–Riley a₀ ± SE | displacement error removed |
| [`espei_export.py`](analysis/espei_export.py) | our phase-boundary measurements | ESPEI ZPF JSON + ORCHID-style rows | ESPEI 0.9.1 `check_dataset` accepts the output |

**The melt-pool model.** It is the Eagar–Tsai moving-Gaussian solution. The field is computed once per
track as (T − T₀)/(ηP), so changing η costs only a contour lookup. That makes fitting dozens of tracks
take seconds. On 2026-11-14 it agreed with ArroyaveLab's `eagar-tsai` 0.6.0 (`check_vs_eagar_tsai.py`):

| P (W) | v (m/s) | η | `eagar-tsai` W / D (µm) | ours W / D (µm) |
|---|---|---|---|---|
| 200 | 0.8 | 0.31 | 172.0 / 80.0 | 173.1 / 80.2 |
| 300 | 1.2 | 0.31 | 192.0 / 90.0 | 192.2 / 90.9 |
| 150 | 0.4 | 0.40 | 204.0 / 97.0 | 205.6 / 97.2 |

(AlSi10Mg-like inputs from #249: k 110 W/m/K, ρ 2650 kg/m³, c_p 1040 J/kg/K, T_l 867 K, 40 µm 1/e²
radius, T₀ 298 K. `eagar-tsai`'s `beam_diameter` is 2σ, which equals our 1/e² radius.)

**Equations and constants the scripts use, with their sources** (DOIs checked in `doi-check.csv`):
- **Melt pool:** the moving Gaussian source of Eagar and Tsai (Welding Journal 62, 1983; no DOI); the keyhole number of
  [Gan et al. 2021](https://doi.org/10.1038/s41467-021-22704-0), as used in #249; and the normalized enthalpy of
  [King et al. 2014](https://doi.org/10.1016/j.jmatprotec.2014.06.005), via #249's scorer.
- **Water density:** [Tanaka et al. 2001](https://doi.org/10.1088/0026-1394/38/4/3). The script gives 998.207 kg/m³ at 20 °C.
- **Cu Kα₁ wavelength:** 1.540593 Å ([Hölzer et al. 1997](https://doi.org/10.1103/PhysRevA.56.4554)).
- **Lattice-parameter extrapolation:** [Nelson and Riley 1945](https://doi.org/10.1088/0959-5309/57/3/302).
- **Coarsening:** LSW, from [Lifshitz and Slyozov 1961](https://doi.org/10.1016/0022-3697(61)90054-3) and
  [Wagner 1961](https://doi.org/10.1002/bbpc.19610650704).
- **Kinetics:** [Kissinger 1957](https://doi.org/10.1021/ac60131a045).
- **Hot cracking:** [Kou 2015](https://doi.org/10.1016/j.actamat.2015.01.034).
- **IACS:** 100 % IACS = 1.7241 µΩ·cm, the 1913 International Annealed Copper Standard.
- **Wiedemann–Franz:** L₀ = π²/3·(k_B/e)² = 2.443 × 10⁻⁸ W·Ω/K².

### 4.1 Open code to use instead of writing our own

A separate check opened each repo below (licence, last commit) and resolved each paper DOI in Crossref. The full list, with
alternatives, is in the PR thread.

| For | Use | Paper |
|---|---|---|
| Equilibrium, Scheil | [pycalphad](https://github.com/pycalphad/pycalphad), [scheil](https://github.com/pycalphad/scheil) | [10.5334/jors.140](https://doi.org/10.5334/jors.140); Scheil validation [10.1016/j.mtla.2020.100689](https://doi.org/10.1016/j.mtla.2020.100689) |
| Fitting TDBs to our data | [ESPEI](https://github.com/PhasesResearchLab/ESPEI) ([dataset format](https://espei.org/0.9.1/reference/dataset_schema.html)) | [10.1557/mrc.2019.59](https://doi.org/10.1557/mrc.2019.59) |
| Precipitation (TC-PRISMA alternative) | [kawin](https://github.com/materialsgenomefoundation/kawin), with Al–Mg–Si and Al–Sc–Zr example databases | [10.1016/j.actamat.2023.118988](https://doi.org/10.1016/j.actamat.2023.118988) |
| Open Al database | COST 507 as shipped in [OpenCalphad's examples](https://github.com/sundmanbo/opencalphad/blob/master/examples/macros/cost507R.TDB) (loads in pycalphad 0.12.0; other copies don't), MatCalc `mc_al` (needs editing) | – |
| DSC method | NIST Recommended Practice Guide SP 960-15 ([PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication960-15.pdf)) | [10.6028/NBS.SP.960-15](https://doi.org/10.6028/NBS.SP.960-15) |
| DSC baselines and onsets | [pkynetics](https://github.com/PPeitsch/pkynetics) (no fraction-solid routine), [pybaselines](https://github.com/derb12/pybaselines) | – |
| Laser flash | [PULsE](https://github.com/kotik-coder/PULsE) | [10.1016/j.simpa.2020.100044](https://doi.org/10.1016/j.simpa.2020.100044) |
| Diffusion couples | [pyDiffusion](https://github.com/zhangqi-chen/pyDiffusion) | [10.5334/jors.255](https://doi.org/10.5334/jors.255) |
| Rietveld | [GSAS-II](https://github.com/AdvancedPhotonSource/GSAS-II), [Profex/BGMN](https://www.profex-xrd.org/) | [10.1107/S0021889813003531](https://doi.org/10.1107/S0021889813003531), [10.1107/S1600576715014685](https://doi.org/10.1107/S1600576715014685) |
| SAXS | [SasView](https://github.com/SasView/sasview), [McSAS3](https://github.com/BAMresearch/McSAS3) | [10.1107/S1600576715007347](https://doi.org/10.1107/S1600576715007347) (McSAS) |
| EBSD | [MTEX](https://github.com/mtex-toolbox/mtex) (MATLAB), [orix](https://github.com/pyxem/orix) | [10.4028/www.scientific.net/SSP.160.63](https://doi.org/10.4028/www.scientific.net/SSP.160.63), [10.1107/S1600576720011103](https://doi.org/10.1107/S1600576720011103) |
| 2D sections → 3D sizes | [GrainSizeTools](https://github.com/marcoalopez/GrainSizeTools) (Saltykov) | [10.21105/joss.00863](https://doi.org/10.21105/joss.00863) |
| Images (pools, pores, cracks, particles) | [Fiji](https://github.com/fiji/fiji) + [MorphoLibJ](https://github.com/ijpb/MorphoLibJ), [scikit-image](https://github.com/scikit-image/scikit-image), [PoreSpy](https://github.com/PMEAL/porespy) | [10.1038/nmeth.2019](https://doi.org/10.1038/nmeth.2019), [10.7717/peerj.453](https://doi.org/10.7717/peerj.453) |
| Melt-pool alternatives | [eagar-tsai](https://github.com/ArroyaveLab/eagar-tsai) (method [10.1016/j.actamat.2019.07.005](https://doi.org/10.1016/j.actamat.2019.07.005)), [3DThesis](https://github.com/ORNL-MDF/3DThesis), [AdditiveFOAM](https://github.com/ORNL/AdditiveFOAM) | [10.21105/joss.07770](https://doi.org/10.21105/joss.07770) (AdditiveFOAM) |
| Nanoindentation | [micromechanics](https://github.com/micromechanics/micromechanics) (Oliver–Pharr) | method [10.1557/JMR.1992.1564](https://doi.org/10.1557/JMR.1992.1564) |
| Corrosion | [PolCurveFit](https://github.com/Meekevanede/PolCurveFit), [impedance.py](https://github.com/ECSHackWeek/impedance.py) | [10.5006/4171](https://doi.org/10.5006/4171), [10.21105/joss.02349](https://doi.org/10.21105/joss.02349) |
| Residual stress (contour) | [pyCM](https://github.com/majroy/pyCM) | [10.1016/j.softx.2020.100458](https://doi.org/10.1016/j.softx.2020.100458) |

No maintained open code was found for:
- DSC fraction solid (hence `dsc_solidification.py`);
- lab-diffractometer sin²ψ;
- ISO 13322-1 image particle sizing (#226 has our own);
- tensile 0.2 % offset yield, which is a few lines of NumPy.

### 4.2 How measurements reach the #238 comparisons

1. **Record every measurement against its run ID** (#159) and the *measured* composition (SOP 05).
2. **Recalculate.** Thermo-Calc (once licensed) and pycalphad with the open databases #238 used (mc_al, the SGTE
   binaries, COST 507) are run for that composition. Store measured, Thermo-Calc and pycalphad values side by side.
3. **Phase boundaries** (S1, P2, P4, P7) go through `espei_export.py`, which writes:
   - **ESPEI ZPF datasets,** for scoring a TDB, or for an MCMC refit of the few parameters that matter;
   - **ORCHID-style rows,** in the columns of #238's `al-cu-literature-invariants.csv`, with `origin = measured_in_house`.

   Begin where ORCHID is thin:
   - **Al–Si:** 13 values, none accepted;
   - **Al–Mn–Cr–Zr and Cu–Al–Ni–Fe:** no data;
   - **Cu–Ni:** no accepted invariants.

   The campaign's seed alloys (Al–Mn–Cr–Zr, Al–Zr(–Er); #256) are exactly these systems.
4. **Tracks** (A1) go into #249's ORCHID-style keyhole benchmark as measured onset and depth points.

### 4.3 Fit to a self-driving-lab loop

- **Automatable now, high throughput:**
  - XRD with a sample changer;
  - eddy-current conductivity;
  - Vickers on an auto-stage;
  - Archimedes;
  - DSC with an autosampler (the Utah SDT 650 is single-sample);
  - image analysis of sections.

  These are also the ones that work on **composition-graded samples** (mapping XRD, EDS, hardness or conductivity across a
  graded coupon or diffusion multiple). DSC, laser flash and tensile need homogeneous bulk.
- **Hands-on bottleneck:** metallography. Tracks, cubes, EBSD and hardness all need polished sections.
  Batch it, one weekly polishing slot as in #256, and standardize the mounts so imaging and indentation can be scripted.
- **Edison's high-throughput search** quotes:
  - about 4 min of XRD instrument time and 2–5 min hands-on per mounted specimen;
  - one alloy-development study running 16 specimens through SEM in under an hour;
  - a scanning droplet cell doing 9 alloys in about 4 h.

  See [Edison q3 §2 and §5](edison/q3-high-throughput-calibration/answer.md). These are literature
  numbers, not ours: time our own (#256 asks for every step to be timed).

## 5. Where, and who to contact

Instruments below were seen on official facility pages on 2026-11-14. Some BYU, APS and INL pages block
CI runners, so a few could only be read through search-engine extracts; they're marked †.
**Nothing was booked and no one was contacted.**

**Access at a glance:**

| Need | BYU | Nearby (outside-academic access) | National lab (proposal) |
|---|---|---|---|
| DSC/DTA to Al/Cu melting | none found | Utah MCL: TA SDT 650 DSC/TGA to 1500 °C (self-serve, assisted or mail-in); Crus Center TA Q600 | – |
| Dilatometry | none found | Utah MCL Anter (≈50 mm rods) | – |
| Laser flash | none found | none confirmed (a Utah unit may have left with its group) | – → commercial |
| XRD | Chemistry XRD Facility: PANalytical X'Pert Pro MPD + HTK 1200 stage † | Utah MCL, Nanofab | APS 11-BM mail-in † (limited after APS-U), SSRL 2-1 mail-in pilot |
| SAXS | none found | Utah Nanofab: Anton Paar SAXSpoint 5.0 | – |
| SEM-EDS-EBSD, FIB, TEM | EMF: Apreo C (EDAX EDS, TSL EBSD), Verios, Helios FIB, Tecnai TF20, Iliad (S)TEM † | Utah Nanofab EMSAL; USU Microscopy Core | – |
| EPMA | none found | Utah microprobe: Cameca SX-50 | – |
| APT | – | CAES MaCS (Idaho Falls) | ORNL CNMS; PNNL EMSL (calls must fit DOE biology/environment) |
| ICP-OES / ICP-MS / XRF | Geological Sciences: Thermo 7400 Duo, Rigaku Primus WD-XRF †; Environmental Analytical Lab: iCAP 7400, fee-for-service †; Chemistry: Agilent 8900 ICP-MS † | Utah Crus Center: Agilent 5800; Weber State | – |
| O/N/H | none found | Utah powder metallurgy group: LECO TCH 600 (access not stated) | – → commercial |
| Tensile, Vickers | none found on facility pages (#256 mentions a 20 kip frame) | Utah MCL: Instron 5969, Vickers and Knoop | – |
| Nanoindentation, CT | none found | Utah Nanofab: Hysitron TI Premier, Zeiss Xradia 620 Versa | – |
| PSD, pycnometry, BET | none found | Utah MCL: LS230, Ultrapyc 5000, 3Flex | – |
| LPBF | AML: Concept Laser M2 † | Utah Metal 3D Printing Core: Aconity MIDI | – |
| Residual stress (neutrons) | – | – | SNS VULCAN (mail-in), NIST BT-8; HFIR HB-2B off until ~Feb 2027 |
| In-situ melt-pool X-ray | – | – | APS 32-ID † (post-upgrade status unconfirmed); CHESS FAST (users have brought print chambers) |

**Who to contact, by role** (contact pages only):
- **BYU:**
  - EMF director ([services](https://microscopy.byu.edu/services));
  - XRD Facility manager ([facility](https://labs.chem.byu.edu/xrd-facility));
  - Environmental Analytical Lab ([EAL](https://pws.byu.edu/eal)), about Si-bearing Al digestion;
  - Geological Sciences lab managers ([facilities](https://geology.byu.edu/research-facilities));
  - Additive Manufacturing Lab supervisor ([AML](https://mfgen.byu.edu/aml));
  - BYU ME and Physics labs, to ask whether a DSC, microhardness tester or eddy-current meter sits in a research group
    (none is on a facility page).
- **Utah:**
  - Materials Characterization Lab staff: a free consultation, then a work-authorization form ([how it works](https://mcl.mse.utah.edu/about/how-it-works/));
  - Nanofab staff ([lab staff](https://www.nanofab.utah.edu/lab-staff/));
  - microprobe lab director ([pricing page](https://www.probelab.utah.edu/pricing.html));
  - Metal 3D Printing Core operator ([core](https://cores.utah.edu/metal-3d-printing/)).
- **National labs:**
  - ORNL Neutron Sciences user office ([users](https://neutrons.ornl.gov/users); the 2027-A call closed Sep 23);
  - APS user office ([proposals](https://www.aps.anl.gov/Users-Information/About-Proposals/Apply-for-Time));
  - CNMS user office ([call](https://www.ornl.gov/facility/cnms/output/call-user-proposals));
  - CAES MaCS scheduling ([MaCS](https://www.boisestate.edu/research/microscopy-and-characterization-suite-macs/));
  - CINT and the Molecular Foundry also run rapid-access calls.
- **Thermo-Calc's account manager:** for the AM Module grid as CSV, which #238 and #249 already asked for, and its electrical
  resistivity and thermal conductivity outputs for the measured compositions.

Commercial instrument tiers and contract labs are being added (see the PR thread).

## 6. Edison literature searches

Three `LITERATURE_HIGH` searches ran on 2026-11-14:

| Search | Question | Answer | References |
|---|---|---|---|
| q1 | how to measure the thermophysical and solidification quantities, with uncertainties and analysis | [answer](edison/q1-thermophysical-solidification/answer.md) | [refs](edison/q1-thermophysical-solidification/references.txt) |
| q2 | how to measure what the AM Module predicts on tracks, pads and coupons with 100–300 g of powder | [answer](edison/q2-lpbf-melt-pool/answer.md) | [refs](edison/q2-lpbf-melt-pool/references.txt) |
| q3 | which measurements automate, and how to feed them back into CALPHAD and kinetic models | [answer](edison/q3-high-throughput-calibration/answer.md) | [refs](edison/q3-high-throughput-calibration/references.txt) |

Edison's answers are long: 62–74 k characters each, with 35–40 cited papers. Only the points cited above are used
here. They are labelled "via Edison" where the full paper wasn't read.

## 7. Verification

- **DOIs.** [`verify_dois.py`](verify_dois.py) looked up every DOI in this folder in Crossref (DataCite for Zenodo) and wrote [`doi-check.csv`](doi-check.csv).
  - For the 62 DOIs in Edison's reference lists, it also checked that the registered title matches the
    title Edison gave: at least 75 % of the title's words appear in Edison's reference. **All 62 pass,** after fixing
    one DOI that contains parentheses.
  - The DOIs cited in this README and the SOPs resolve to the papers named.
- **Claims.**
  - **Trapp et al. 2017, Cunningham et al. 2019 and Martin et al. 2017:** checked against their abstracts (Semantic Scholar, PubMed).
  - **Claims marked "via Edison":** checked against Edison's excerpts of the paper, not the full text. They give the paper's
    result as Edison retrieved it, and should be read as such.
  - **Facility instruments:** read on official pages (marked † where only a search extract was available).
  - **ESPEI's ZPF format:** read in ESPEI's own docs (`docs/reference/dataset_schema.qmd`, commit c9143c8). ESPEI 0.9.1's `check_dataset` validates the exporter's output.
- **What I couldn't check:**
  - **The window for Kou's index** in Kou's paper itself: no abstract was available, and this run's web-search budget
    ran out. The script takes the window as an argument.
  - **Clyne and Davies' original 1981 paper** (no DOI): the CSC definition is as Edison's three sources give it.
  - **Prices:** all are tier estimates.

## 8. Not done, and open questions

- **No measurements, bookings or purchases.** No vendor or facility was contacted.
- **Commercial price tiers and contract labs** are still being collected. Until then the cost column is my estimate.
- **BYU departmental instruments** (ME, Physics, Chemical Engineering) that aren't on facility pages may exist. A short
  e-mail round would settle the DSC, microhardness and eddy-current questions.
- **The SOPs are first drafts.** Every duration in them is an estimate to be replaced by timed runs.
