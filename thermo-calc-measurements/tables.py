#!/usr/bin/env python3
"""Single source for the measurement matrix and the #255 ranking.

    python tables.py            # writes matrix.csv, ranking.csv and refreshes the tables in README.md

Edit the rows here, not in the README. Access codes:
  lab   = our own lab (VCL), or equipment we would buy
  BYU   = a BYU facility (EMF, Chemistry XRD, Geological Sciences / EAL ICP-OES, AML M2, IML)
  UT    = a nearby university facility open to outside academics (mainly the University of Utah
          Materials Characterization Lab, Utah Nanofab, the Utah microprobe; also USU, Weber State)
  NL    = a national-lab user facility (proposal; free for publishable work)
  svc   = commercial service
Cost: capital tiers $ <10k, $$ 10-50k, $$$ 50-250k, $$$$ >250k; per-sample tiers in brackets,
[$] <100, [$$] 100-500, [$$$] 500-2000, [$$$$] >2000. All tiers are estimates unless the README
cites a source. Throughput and automation: H / M / L.
"""
from __future__ import annotations

import csv
import pathlib
import re

HERE = pathlib.Path(__file__).parent

COLS = ["id", "group", "quantity", "method", "instrument_where", "access", "cost", "time_per_sample",
        "throughput", "automation", "samples_from", "checks"]

# fmt: off
MATRIX = [
 # --- phase equilibria
 ("P1", "Phase equilibria", "Phase identity, amounts and volume fractions", "XRD + Rietveld; SEM-BSE area fractions (Delesse); EBSD phase maps; synchrotron XRD for phases < 1 vol%", "PANalytical X'Pert Pro MPD (BYU Chemistry XRD); Apreo C + EDAX/TSL EBSD (BYU EMF); APS 11-BM mail-in", "BYU; NL", "[$]", "0.5-1 h scan", "H", "H", "powder, DSC bead, annealed + quenched coupon, as-built cube", "equilibrium phase fractions (annealed), Scheil fractions (DSC bead), metastable phases (as-built)"),
 ("P2", "Phase equilibria", "Phase compositions (tie-lines)", "SEM-EDS on phases > 1-2 um; EPMA-WDS for accuracy; TEM-EDS or APT below 1 um", "Apreo C EDS (BYU EMF); Cameca SX-50 EPMA (Utah microprobe); Tecnai TF20 STEM-EDS (BYU EMF)", "BYU; UT", "[$-$$]", "1-3 h", "M", "M", "annealed + quenched coupons, DSC beads, diffusion couples", "phase compositions; ZPF tie-line entries (espei_export.py)"),
 ("P3", "Phase equilibria", "Site fractions", "Not practical for us. Rietveld occupancy (synchrotron/neutron) or APT for ordered phases; use the lattice parameter as the proxy", "APS 11-BM; ORNL CNMS APT", "NL", "proposal", "weeks", "L", "L", "powder, coupon", "sublattice model of L1_2 Al3(Sc,Zr,Er) and similar (indirect)"),
 ("P4", "Phase equilibria", "Solubility limits and solvus", "Quench from a temperature series, then XRD lattice parameter (parametric method) and resistivity; DSC dissolution peaks; SEM for second phase", "X'Pert Pro (BYU); eddy-current meter (buy); tube furnace", "lab; BYU", "$$ meter", "1 h per temperature", "M", "M", "printed coupons (supersaturated), cast buttons", "solvus of Al3Zr/Al3Sc/Al6Mn etc.; LPBF supersaturation vs equilibrium"),
 ("P5", "Phase equilibria", "Transformation temperatures", "DSC/DTA (heating and cooling, several rates); dilatometry; resistivity vs temperature", "TA SDT 650 DSC/TGA to 1500 C (Utah MCL); NETZSCH DSC 3500 to 600 C (Utah MCL); Anter dilatometer, ~50 mm rods (Utah MCL)", "UT", "[$]", "2-3 h", "M", "H (autosampler)", "powder, chips", "invariant reactions, solvus, eutectoid in NAB, transformation temperatures"),
 ("P6", "Phase equilibria", "Activities, chemical potentials, driving forces", "Knudsen-effusion mass spectrometry or EMF cells (specialist labs). Proxy: phase boundaries (equal chemical potentials) and Mg/Zn evaporation loss", "specialist academic labs", "svc/academic", "[$$$$]", "weeks", "L", "L", "bulk", "activities (only via proxies for us)"),
 ("P7", "Phase equilibria", "Phase diagrams (sections, invariants)", "Key alloys: DSC + XRD + SEM/EDS of annealed and quenched samples; diffusion couples/multiples for isothermal sections", "combination of P1, P2, P5", "BYU; UT", "[$-$$]", "days per section", "M", "M", "powder, buttons, couples", "phase diagrams; new ORCHID/ESPEI entries for Al-Si, Al-Mn-Cr-Zr, Cu-Al-Ni-Fe, Cu-Ni"),
 ("P8", "Aqueous", "Pourbaix stability regions, pH, potential vs SHE", "OCP and potentiodynamic polarization vs pH (ASTM G5/G59-style); immersion with XRD/Raman of products", "EZstat-Pro potentiostat (lab, #221/#239); Gamry Reference 600+ (Utah Nanofab)", "lab; UT", "$ (have)", "1-2 h", "M", "H", "polished coupons", "TCAQ Pourbaix regions (qualitative: passive vs active)"),
 # --- thermochemical / thermophysical
 ("T1", "Thermochemical", "Heat capacity, enthalpy, entropy", "DSC sapphire method (ASTM E1269) to ~550 C for Al; drop calorimetry above; S from integrating cp/T", "SDT 650 (Utah MCL) or a dedicated DSC; drop calorimetry at specialist labs", "UT; svc", "[$]", "3 runs (blank, sapphire, sample)", "M", "H", "powder, discs", "cp, H, S"),
 ("T2", "Thermochemical", "Heat of formation (intermetallics)", "Solution or direct-reaction calorimetry", "specialist academic labs", "svc/academic", "[$$$]", "weeks", "L", "L", "arc-melted intermetallics", "formation enthalpies (none for Al-Cu in ORCHID, #238)"),
 ("T3", "Thermochemical", "Latent heat, apparent heat release", "DSC peak integration (SOP 01)", "SDT 650 (Utah MCL)", "UT", "[$]", "with T-liquidus run", "M", "H", "powder", "latent heat; Scheil heat release"),
 ("T4", "Thermophysical", "Density (solid)", "Archimedes (SOP 03); He pycnometry of powder; X-ray density from lattice parameter", "density kit on a 0.1/0.01 mg balance (lab); Anton Paar Ultrapyc 5000 (Utah MCL)", "lab; UT", "$", "10 min", "H", "M", "cubes, powder", "density (molar volume)"),
 ("T5", "Thermophysical", "Thermal expansion, lattice parameter vs T", "High-temperature XRD; push-rod dilatometry (ASTM E228)", "X'Pert Pro + Anton Paar HTK 1200 stage (BYU Chemistry); Anter dilatometer (Utah MCL)", "BYU; UT", "[$]", "4-8 h", "M", "H", "powder (HT-XRD), 50 mm bars (dilatometer)", "CTE, lattice parameter(T), density(T)"),
 ("T6", "Thermophysical", "Lattice parameters (cubic)", "XRD with Nelson-Riley extrapolation or Rietveld (xrd_lattice.py)", "X'Pert Pro (BYU Chemistry)", "BYU", "[$]", "1 h", "H", "H", "powder, polished coupons", "lattice parameter; solute in solution"),
 ("T7", "Thermophysical", "Liquid viscosity and surface tension", "Oscillating drop (EML/ESL), sessile drop, maximum bubble pressure, oscillating-cup viscometry; Al oxide skin is the main error", "specialist levitation labs", "svc/academic", "[$$$$]", "weeks", "L", "L", "a few grams of alloy", "liquid viscosity, surface tension (AM-module Marangoni inputs)"),
 ("T8", "Thermophysical", "Thermal diffusivity and conductivity", "Laser flash (ASTM E1461) + DSC cp + density, k = alpha*rho*cp; eddy-current conductivity with a fitted Smith-Palmer relation for the rest", "LFA send-out (NETZSCH lab, TPRL) for 3-4 calibration alloys; eddy-current meter (buy)", "svc; lab", "[$$] LFA; $$ meter", "LFA 1 day; eddy current 2 min", "L (LFA) / H (EC)", "M / H", "10-12.7 mm discs ~2 mm thick (LFA); 10 mm coupons (EC)", "thermal conductivity and diffusivity (AM-module inputs)"),
 ("T9", "Thermophysical", "Electrical resistivity and conductivity", "Eddy current, %IACS (ASTM E1004); four-point probe; four-wire bars in a furnace for rho(T)", "Foerster SIGMATEST 2.070 or Fischer SIGMASCOPE SMP350 ($, buy); four-point probe (BYU IML, Utah Nanofab)", "lab; BYU", "$$", "2 min", "H", "H", "coupons >=10 mm, polished sections", "electrical resistivity model; solute in solution; aging"),
 ("T10", "Thermophysical", "Interfacial energy", "Not measured directly: fit to coarsening rate (LSW, kinetics.py) or to TC-PRISMA PSD evolution", "via K1 or S1 data", "-", "-", "-", "-", "-", "aged coupons", "interfacial energy (TC-PRISMA input)"),
 # --- elastic and mechanical
 ("M1", "Mechanical", "Young's, shear and bulk moduli", "Impulse excitation (ASTM E1876) on printed bars; ultrasonic pulse-echo velocities; nanoindentation (Oliver-Pharr)", "GrindoSonic MK7 or IMCE RFDA ($$); Hysitron TI Premier (Utah Nanofab)", "lab/svc; UT", "$$ / [$]", "10 min (IET)", "H", "H", "bars ~40x8x2 mm, coupons", "E, G, K (polycrystal averages of Thermo-Calc's Cij)"),
 ("M2", "Mechanical", "Single-crystal elastic constants C11, C12, C44", "Resonant ultrasound on single crystals: not practical. Compare Voigt-Reuss-Hill averages of predicted Cij with M1", "-", "-", "-", "-", "L", "L", "-", "Cij (only through averages)"),
 ("M3", "Mechanical", "Hardness and yield strength", "Vickers (ASTM E384) incl. aging series (SOP 04); sub-size tensile (ASTM E8); shear punch / small punch; indentation plastometry", "Vickers testers and Instron 5969 (Utah MCL); 20 kip frame (#256); Plastometrex PLX-Benchtop ($$$)", "UT; lab; svc", "[$]", "10 min (HV); 1 h (tensile)", "H (HV)", "H (HV auto-stage)", "cubes, sections, bars", "General Model Library yield strength; TC-PRISMA peak/over-aged strength"),
 # --- solidification
 ("S1", "Solidification", "Liquidus, solidus, incipient melting, freezing range", "DSC/DTA, 3 heating rates, extrapolated to zero rate (SOP 01)", "TA SDT 650 (Utah MCL; mail-in)", "UT", "[$]", "2-2.5 h per run", "M", "H", "powder (10-25 mg), printed chips", "equilibrium and Scheil liquidus/solidus; ORCHID gaps (AlSi10Mg, NAB, Cu-Ni)"),
 ("S2", "Solidification", "Fraction solid curve, solidification path, fraction eutectic", "DSC partial areas with lag correction (dsc_solidification.py); eutectic area fraction on DSC beads; phase sequence by SEM/EDS", "SDT 650 + BYU EMF", "UT; BYU", "[$]", "with S1", "M", "H", "powder, DSC beads", "Scheil fs(T), solidification path, eutectic fraction"),
 ("S3", "Solidification", "Microsegregation, partition coefficients", "EDS/WDS grid maps on DSC beads or castings, sorted (WIRS-type) and compared with Scheil; APT/TEM-EDS for LPBF cells", "Apreo C EDS (BYU EMF); SX-50 EPMA (Utah); APT (ORNL CNMS)", "BYU; UT; NL", "[$$]", "2-4 h", "M", "M", "DSC beads, castings, tracks", "Scheil/back-diffusion segregation; solute trapping in LPBF"),
 ("S4", "Solidification", "Shrinkage", "Solid density (T4) vs liquid density (levitation, specialist)", "-", "svc/academic", "[$$$$]", "weeks", "L", "L", "-", "solidification shrinkage (low priority for LPBF)"),
 ("S5", "Solidification", "Hot-tearing tendency", "Crack density on pads and cubes (SOP 03); Kou and CSC indices from measured fs(T); constrained-rod casting", "optical microscope + Fiji (lab); DSC (S1)", "lab; UT", "$", "1 h per batch", "H", "M", "pads, cubes, DSC", "Scheil-based hot-cracking indices; printability (cracking axis)"),
 ("S6", "Solidification", "Columnar-to-equiaxed transition, grain size, texture", "EBSD on tracks and pads (ASTM E2627-style grain size); Barker's etch under polarized light for Al", "Apreo C + TSL OIM (BYU EMF)", "BYU", "[$$]", "2-4 h", "M", "M", "tracks, pads", "CET vs AM-module G-R; inoculation by Al3(Sc,Zr)"),
 # --- kinetics, DICTRA, PRISMA
 ("K1", "Kinetics", "Interdiffusion, intrinsic, tracer diffusion; mobility", "Diffusion couples + EDS/EPMA line scans, Boltzmann-Matano / Sauer-Freise (pyDiffusion); tracer needs radiotracer labs", "furnace (lab); SX-50 EPMA (Utah)", "lab; UT", "[$$]", "days (anneal) + 2 h scan", "L", "M", "bonded or cast couples", "mobility databases; interdiffusion coefficients"),
 ("K2", "DICTRA", "Homogenization, dissolution and growth of second phases", "EDS line scans and SEM area fractions vs anneal time; DSC incipient melting before/after", "BYU EMF; SDT 650", "BYU; UT", "[$$]", "2-4 h", "M", "M", "as-built and annealed coupons", "DICTRA homogenization and dissolution kinetics"),
 ("K3", "DICTRA", "Interdiffusion at coatings, dissimilar joints; PWHT", "EDS line scans + hardness traverses across interfaces (track/plate, DED Cu on steel)", "BYU EMF; Vickers", "BYU; UT", "[$$]", "2 h", "M", "M", "tracks on plate, DED walls", "DICTRA interdiffusion profiles"),
 ("K4", "TC-PRISMA", "Precipitate size distribution, number density, volume fraction, compositions", "TEM/STEM dark field with stereological (foil thickness) correction; SAXS; APT", "Tecnai TF20 and Iliad (BYU EMF); Anton Paar SAXSpoint 5.0 (Utah Nanofab); LEAP (ORNL CNMS, proposal)", "BYU; UT; NL", "[$$-$$$$]", "1-3 days", "L", "L", "aged coupons (finalists only)", "TC-PRISMA PSD, mean radius, number density, volume fraction, matrix composition"),
 ("K5", "TC-PRISMA", "Grain growth and Zener pinning", "EBSD grain size vs anneal time and temperature", "BYU EMF", "BYU", "[$$]", "2-4 h", "M", "M", "annealed coupons", "grain growth, Zener-limited grain size"),
 ("K6", "TC-PRISMA", "TTP and CCT diagrams", "Hardness + conductivity aging matrix (SOP 04); DSC at several rates (Kissinger, kinetics.py)", "Vickers; eddy-current meter; DSC", "lab; UT", "$", "16 conditions per alloy", "H", "H", "small coupons from one cube row", "TTP peak times, apparent activation energies"),
 # --- AM module
 ("A1", "AM Module", "Melt-pool width, depth, length; peak temperature", "Single-track cross-sections and top views (SOP 02); length from high-speed imaging or longitudinal sections; peak T needs calibrated two-colour pyrometry", "Utah Aconity MIDI, BYU Concept Laser M2, desktop LPBF (#260); optical/SEM", "UT; BYU; lab", "[$]", "~18 tracks per mount", "M", "M", "single tracks on plate and on one powder layer", "melt-pool size and regime; heat-source calibration (absorptivity, beam radius)"),
 ("A2", "AM Module", "Marangoni flow velocity", "In-situ X-ray imaging with tracer particles", "APS 32-ID (proposal; status after APS-U unconfirmed)", "NL", "proposal", "beamtime", "L", "L", "tracks", "fluid-flow velocity (indirect: pool shape)"),
 ("A3", "AM Module", "Thermal gradient G, solidification rate R, thermal history", "Cell/dendrite spacing -> cooling rate; R = v cos(theta) from pool shape; thermocouples in the plate; IR camera", "BYU EMF (cell spacing); thermocouples (lab)", "BYU; lab", "[$]", "1-2 h", "M", "M", "tracks, pads", "G, R and cooling rate; thermal history"),
 ("A4", "AM Module", "Composition change by evaporation", "ICP-OES of powder vs printed part (SOP 05); EDS across tracks", "Thermo iCAP 7400 (BYU EAL / Geological Sciences)", "BYU; svc", "[$-$$]", "1 day turnaround", "M", "M", "powder + printed chips", "evaporation mode (Mg, Zn, Li loss)"),
 ("A5", "AM Module", "Printability maps (keyholing, lack of fusion, balling)", "Tracks (regime, balling) + cubes (density, pore type, cracks), SOP 02 and 03", "as A1 + density kit", "lab; UT", "[$]", "per build", "M", "M", "tracks, cubes", "printability map; #249 keyhole criteria"),
 ("A6", "AM Module", "Laser absorptivity", "Calorimetric (thin disc + thermocouples, Trapp et al. 2017-type); integrating-sphere reflectance at 1070 nm; inverse from A1", "home-built calorimeter on the desktop LPBF; LAMBDA 1050+ or Cary 7000 with sphere ($$$)", "lab", "$", "1 h", "M", "M", "discs, powder layers", "absorptivity used by the heat source"),
 # --- model libraries, process metallurgy
 ("L1", "Model libraries", "Ordered-phase solvus (Al3(Sc,Zr) L1_2 analogue of the Ni library)", "DSC dissolution; resistivity after anneals; XRD", "as P4/P5", "UT; lab", "[$]", "-", "M", "M", "aged coupons", "L1_2 solvus"),
 ("L2", "Model libraries", "Alloy colour (noble metals)", "Spectrophotometer, CIELAB on polished Cu alloys", "benchtop spectrophotometer", "lab/svc", "$", "5 min", "H", "H", "polished coupons", "optical properties (Cu family only)"),
 ("L3", "Model libraries", "Steel, Ni-APB, Ti libraries", "Not relevant to Al and Cu alloys", "-", "-", "-", "-", "-", "-", "-", "-"),
 ("PM1", "Process Metallurgy", "Inclusions, oxide content", "O/N/H by inert gas fusion; SEM of powder cross-sections for oxide films", "LECO TCH 600 (Utah powder metallurgy lab, access not stated); NSL, Luvak, LTI (svc)", "UT; svc", "[$-$$]", "days turnaround", "M", "L", "sealed powder", "inclusion/oxide content (slag and steel outputs not relevant)"),
 # --- beyond Thermo-Calc
 ("B1", "Beyond Thermo-Calc", "Stress-strain curve, work hardening, ductility", "Sub-size tensile (ASTM E8); indentation plastometry for small coupons", "Instron 5969 (Utah MCL); 20 kip frame (#256); Plastometrex (svc)", "UT; lab; svc", "[$$]", "1 h", "L", "M", "printed bars", "(validates strength models; needed for the paper)"),
 ("B2", "Beyond Thermo-Calc", "Fatigue, creep, cryogenic tensile (#254)", "ASTM-type fatigue and creep; tensile at 77 K", "Westmoreland, IMR, Element (svc)", "svc", "[$$$-$$$$]", "weeks", "L", "L", "finalist bars", "(finalists only; not before Feb 28)"),
 ("B3", "Beyond Thermo-Calc", "Porosity and keyhole porosity", "Archimedes + sections (SOP 03); X-ray CT", "Zeiss Xradia 620 Versa (Utah Nanofab)", "lab; UT", "[$-$$]", "10 min / 2-4 h CT", "H / L", "M", "cubes", "(printability)"),
 ("B4", "Beyond Thermo-Calc", "Residual stress", "Bridge-curvature specimens (cheap); XRD sin^2(psi); neutron diffraction; contour method", "in-house bridge test; VULCAN at SNS (mail-in proposal); NIST BT-8; commercial contour", "lab; NL; svc", "$ / proposal", "1 h (bridge)", "M", "L", "bridge specimens, coupons", "(distortion, cracking)"),
 ("B5", "Beyond Thermo-Calc", "Corrosion rate", "Potentiodynamic polarization and Tafel/EIS; immersion mass loss; salt fog", "EZstat-Pro (lab); Gamry (Utah Nanofab)", "lab; UT", "$ (have)", "1-2 h", "M", "H", "polished coupons", "(paper requirement; Pourbaix check P8)"),
 ("B6", "Beyond Thermo-Calc", "Powder PSD, shape, flowability, apparent and tap density", "SEM image analysis (ISO 13322-1, #225); laser diffraction; Hall/Carney funnels; tap density", "BYU EMF; Beckman Coulter LS230 (Utah MCL); SALD 2300 (Utah PM lab); funnels (buy)", "BYU; UT; lab", "$", "30 min", "H", "M", "sieved powder", "(printability; already in #256's weekly plan)"),
 ("B7", "Beyond Thermo-Calc", "Spatter and vapour plume", "High-speed imaging with laser illumination; schlieren", "Photron FASTCAM Nova S or Phantom TMX (rent) + Cavitar CAVILUX", "svc", "$$ rental", "per build", "L", "L", "tracks", "(evaporation, keyholing)"),
]

# Ranking for #255. Scores 1-5 (5 = best): info = what it tells the campaign (strength, crack-free
# printing, whether the CALPHAD screen is right); tc = how directly it checks or calibrates
# Thermo-Calc/pycalphad and fills ORCHID gaps; cost (5 = cheapest); effort (5 = least hands-on per
# alloy); speed (5 = first data within two weeks). Total = 2*info + tc + cost + effort + speed.
RANKING = [
 # key, measurement, matrix rows, info, tc, cost, effort, speed, quick_win, sop
 ("composition", "Composition (ICP-OES) and O/N/H of every powder, plus one print per alloy", "A4, PM1", 5, 5, 3, 4, 4, True, "05"),
 ("hardness", "Vickers hardness as-built and through an aging matrix", "M3, K6", 5, 4, 5, 4, 3, True, "04"),
 ("dsc", "DSC/DTA: solidus, liquidus, fs(T), latent heat, hot-cracking indices", "S1, S2, S5, T3", 4, 5, 4, 4, 4, True, "01"),
 ("density", "Archimedes density, porosity type and crack density of cubes", "T4, A5, S5, B3", 5, 3, 5, 4, 3, True, "03"),
 ("xrd", "XRD phases and Al lattice parameter (powder, as-built, annealed)", "P1, P4, T6", 3, 4, 5, 4, 5, True, "-"),
 ("eddy", "Eddy-current conductivity (%IACS), as-built and through the aging matrix", "T8, T9, K6", 3, 4, 4, 5, 3, True, "04"),
 ("tracks", "Single-track cross-sections and heat-source calibration", "A1, A5", 4, 5, 3, 2, 3, True, "02"),
 ("tensile", "Sub-size tensile on benchmarks and finalists", "B1, M3", 5, 3, 3, 2, 2, False, "-"),
 ("corrosion", "Potentiodynamic polarization in NaCl (once the reference electrodes arrive, #221)", "B5, P8", 4, 2, 4, 3, 3, True, "-"),
 ("ebsd", "SEM/EBSD of tracks and pads: grains, CET, cell spacing, cracks", "S6, A3, K5", 4, 3, 3, 2, 3, False, "-"),
 ("htxrd", "High-temperature XRD: CTE and phase changes on heating", "T5", 2, 3, 4, 4, 4, False, "-"),
 ("lfa", "Laser flash on 3-4 alloys to calibrate the conductivity relation", "T8", 2, 4, 2, 4, 2, False, "-"),
 ("absorb", "Calorimetric absorptivity on the desktop machine", "A6", 3, 4, 3, 2, 1, False, "-"),
 ("prisma", "TEM / SAXS / APT of finalist precipitates", "K4", 3, 5, 2, 1, 1, False, "-"),
 ("couples", "Diffusion couples", "K1", 1, 4, 4, 2, 2, False, "-"),
]
# fmt: on


def score(r):
    _, _, _, info, tc, cost, effort, speed, *_ = r
    return 2 * info + tc + cost + effort + speed


def md_escape(s):
    return str(s).replace("|", "\\|")


def matrix_md():
    head = ("| ID | Quantity | Method (direct; proxy) | Instrument and where | Access | Cost | Time / sample | "
            "Thru-put | Auto | Samples from | What it checks in Thermo-Calc |")
    sep = "|" + "---|" * 11
    out, group = [], None
    for r in MATRIX:
        d = dict(zip(COLS, r))
        if d["group"] != group:
            group = d["group"]
            out.append(f"| | **{group}** | | | | | | | | | |")
        out.append("| " + " | ".join(md_escape(d[c]) for c in
                   ["id", "quantity", "method", "instrument_where", "access", "cost", "time_per_sample",
                    "throughput", "automation", "samples_from", "checks"]) + " |")
    return "\n".join([head, sep] + out)


def ranking_md():
    rows = sorted(RANKING, key=lambda r: -score(r))
    head = "| Rank | Measurement | Matrix rows | Info ×2 | TC check | Cost | Effort | Speed | Score /30 | Quick win | SOP |"
    sep = "|" + "---|" * 11
    out = []
    for i, r in enumerate(rows, 1):
        key, name, ids, info, tc, cost, effort, speed, qw, sop = r
        files = {"01": "01-dsc-solidification.md", "02": "02-single-track-melt-pool.md",
                 "03": "03-density-porosity-cracks.md", "04": "04-hardness-conductivity-aging.md",
                 "05": "05-composition-interstitials.md"}
        sop_link = f"[{sop}](sops/{files[sop]})" if sop in files else "–"
        out.append(f"| {i} | {name} | {ids} | {info} | {tc} | {cost} | {effort} | {speed} | **{score(r)}** | "
                   f"{'yes' if qw else ''} | {sop_link} |")
    return "\n".join([head, sep] + out)


def write_csvs():
    with open(HERE / "matrix.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        w.writerows(MATRIX)
    with open(HERE / "ranking.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "key", "measurement", "matrix_rows", "info", "tc_check", "cost", "effort", "speed",
                    "score", "quick_win", "sop"])
        for i, r in enumerate(sorted(RANKING, key=lambda r: -score(r)), 1):
            w.writerow([i, *r[:8], score(r), r[8], r[9]])


def refresh_readme():
    p = HERE / "README.md"
    if not p.exists():
        return
    s = p.read_text()
    for tag, body in (("MATRIX", matrix_md()), ("RANKING", ranking_md())):
        s = re.sub(rf"(<!-- {tag}:START -->).*?(<!-- {tag}:END -->)",
                   lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), s, flags=re.S)
    p.write_text(s)


if __name__ == "__main__":
    write_csvs()
    refresh_readme()
    for i, r in enumerate(sorted(RANKING, key=lambda r: -score(r)), 1):
        print(i, score(r), r[1])
