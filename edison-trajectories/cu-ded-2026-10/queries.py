"""Questions for edison_cu_ded.py. Batch N+1 was written after reading batch N;
the comment above each batch says what it follows up on."""

CONTEXT = """\
CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.
"""

OUTPUT = """\
OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.
"""


def q(body: str) -> str:
    return CONTEXT + "\n" + body.strip() + "\n\n" + OUTPUT


BATCHES = {}

# Batch 1: survey. What exists on DED of Cu-Ni and NAB, copper powder making,
# DED powder requirements, seawater corrosion of printed copper alloys,
# CALPHAD/ICME for copper AM, Navy needs, repair, and ML precedent. Two
# LITERATURE_HIGH questions (closest prior work; powder making) are read when
# batch 3 is written.
BATCHES[1] = {
    "b1-01-closest-prior-work": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: What is the closest prior work to designing a NEW copper alloy
composition specifically for laser additive manufacturing (blown-powder DED
first, LPBF second) with as-deposited seawater corrosion as a design target?
Start with Z. Jia, J. Yang, R. Li, Z. Wang, C. Tan, G. Sun, E.-H. Han,
"Subtractive composition design of nickel-aluminum bronze for laser additive
manufacturing: Achieving superior as-deposited mechanical and corrosion
performance", Additive Manufacturing 127 (2026) 105291,
doi:10.1016/j.addma.2026.105291 (Southeast University). Report in detail:
which laser process it used (DED/laser metal deposition or LPBF), the baseline
and modified compositions, what "subtractive" removes and why, the phases
formed as deposited, the corrosion tests and numbers, the mechanical numbers,
and what it leaves open. Then cover the same group's earlier laser-DED NAB
work (Guifang Sun, Zhandong Wang and co-workers), Barr et al. (Addit. Manuf.
2022, composition effects in LPBF NAB), and any other paper that changes a
copper alloy's composition for AM (Cu-Ni, Cu-Al, Cu-Mn-Al, Cu-Sn, CuCrZr,
GRCop excluded unless a method transfers). Which of these used CALPHAD, a
thermal model, or machine learning to choose the composition?
"""),
    },
    "b1-02-ded-nab": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What is known about blown-powder laser DED (laser metal deposition,
laser cladding) of nickel-aluminum bronze (e.g. C95800, CuAl10Fe5Ni5)? Cover
process windows (power, speed, powder feed, spot), porosity and cracking, the
as-deposited microstructure (martensitic beta', retained beta, kappa phases
I-IV, Widmanstatten alpha) and how reheating by later layers changes it,
mechanical properties, and corrosion in NaCl or seawater, especially
selective phase corrosion (de-aluminification) as deposited vs after heat
treatment. Compare with wire-arc DED NAB (which the Navy has specified, with
a 1250 F / 6 h anneal) and with LPBF NAB.
"""),
    },
    "b1-03-ded-cuni": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What is known about additive manufacturing of copper-nickel alloys
(90-10 C70600, 70-30 C71500, Cu-Ni-Fe-Mn, Cr-modified Cu-Ni such as C72200
or CuNi30Cr2) by blown-powder laser DED or laser cladding, and by wire-arc
DED and LPBF for comparison? Report printability (porosity, hot cracking,
lack of fusion), microsegregation of Ni, Fe and Mn and dendrite spacing,
hardness and tensile data, and any seawater or NaCl corrosion testing of the
printed material versus wrought. Is there ANY corrosion study of Cu-Ni made by
blown-powder laser DED? Which groups (Navy labs, Penn State ARL, NSWC
Carderock, universities, companies) have published on printed Cu-Ni?
"""),
    },
    "b1-04-cu-powder-making": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: How are copper alloy powders for additive manufacturing made, and
what goes wrong? Cover gas atomization (close-coupled, free-fall), water
atomization, electrode induction gas atomization, plasma atomization, plasma
rotating electrode process, centrifugal atomization, plasma spheroidization,
and ultrasonic (vibrating-plate or sonotrode) atomization, for pure Cu,
Cu-Ni, aluminum bronzes / NAB, Cu-Sn, CuCrZr and GRCop. Report particle size
distributions, yield in a target size cut, sphericity and satellites, oxygen
pickup and how it is controlled, crucible and nozzle materials compatible
with copper and copper-nickel melts (graphite, alumina, zirconia, boron
nitride, magnesia), and melt superheat. Specifically: has ultrasonic
atomization been used for copper or copper alloys (any AMAZEMET rePOWDER
reports), at what frequency, and what median particle size resulted? How do
in-house or small-batch atomized copper alloy powders compare with
commercial gas-atomized powder in flow, density, and printed quality?
"""),
    },
    "b1-05-ded-powder-requirements": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What does peer-reviewed work say about powder requirements for
blown-powder laser DED, and how much do they matter? Cover the particle size
range (often quoted as 45-150 or 53-150 um), flowability (Hall, Carney,
angle of repose, avalanche), sphericity, satellites, moisture and oxygen, and
their measured effects on powder catchment efficiency, porosity, surface
finish and deposit chemistry. Include any copper- or copper-alloy-specific
DED work, including high reflectivity at ~1 um wavelength, absorptivity of
Cu-Ni and Al-bronze powders, preheating, and blue or green lasers for copper
DED. Name the papers that actually measured these effects rather than
stating them.
"""),
    },
    "b1-06-seawater-film-mechanisms": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What controls the seawater corrosion resistance of Cu-Ni and
aluminum bronzes, and how does an as-solidified or as-deposited
microstructure change it? Cover protective film formation (Cu2O inner layer,
Ni/Fe-enriched outer layers, time to stabilize), the roles of Fe (1-2 wt%),
Mn and Cr, microsegregation and cored dendrites, kappa phases and martensite
in NAB (selective phase corrosion), velocity limits, sulfide-polluted water,
and biofouling. Which short electrochemical tests (polarization, LPR, EIS,
ASTM G59/G102/G106, G31 immersion) have been shown to rank copper alloys the
same way as long-term seawater exposure, and over what exposure time does
film formation make short tests misleading?
"""),
    },
    "b1-07-icme-calphad-cu": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What ICME and CALPHAD work exists for copper alloys in additive
manufacturing or welding? Cover thermodynamic and mobility databases for Cu
alloys (Thermo-Calc TCCU and MOBCU, others) and their validation for Cu-Ni-Fe-
Mn-Cr and Cu-Al-Ni-Fe-Mn; Scheil and back-diffusion predictions of
microsegregation in Cu-Ni; predictions of kappa phase and beta/martensite in
NAB under rapid cooling and cyclic reheating; and coupled thermal-history +
CALPHAD (or DICTRA / precipitation) models for DED. Also give two or three
examples, any alloy system, where coupling CALPHAD to a DED thermal model was
used to DESIGN a composition (e.g. steels, Ni superalloys, Ti) and was shown
to beat equilibrium-only CALPHAD.
"""),
    },
    "b1-08-navy-needs": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What does the published literature (including technical reports and
conference papers) say about Navy needs for additively manufactured Cu-Ni and
NAB parts, and about Navy-funded work on them? Cover seawater piping, valves,
pump impellers, propellers and propulsor parts, heat exchangers, and repair
of cast NAB (propellers) by laser cladding or DED; NAVSEA qualification and
AM material specifications; work from NSWC Carderock, NSWC Philadelphia, NRL,
Penn State ARL, Naval Postgraduate School, and ONR-funded university groups;
and casting supply-chain delays. Give exact citations and say which claims
come from peer-reviewed sources and which from trade press.
"""),
    },
    "b1-09-precedent-ml-cu-am": {
        "job": "PRECEDENT",
        "query": """\
Has anyone used Bayesian optimization, active learning, machine learning, or
any closed-loop or cost-aware multi-fidelity search to design the COMPOSITION
of a copper alloy (Cu-Ni, aluminum bronze / nickel-aluminum bronze, Cu-Sn,
Cu-Mn-Al, CuCrZr or similar) for additive manufacturing or welding, or to
co-optimize powder atomization settings together with alloy composition for
AM? Include process-parameter optimization of copper alloys in DED or LPBF by
BO/ML as a closer analogue, and seawater corrosion as a target property.
Exclude publications by Sterling G. Baird. Give citations with DOIs and say
plainly whether the combination "cost-aware BO over a linked composition ->
powder -> DED -> corrosion pipeline for copper alloys" has precedent.
""",
    },
    "b1-10-repair-on-cast-nab": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What is known about depositing copper alloys by laser DED, laser
cladding or arc processes onto cast NAB and wrought Cu-Ni for repair? Cover
dilution, fusion-line defects, liquation and solidification cracking, the
heat-affected zone in cast NAB (kappa dissolution, martensite formation,
hardness peaks), residual stress, and the corrosion of the fusion zone and
HAZ (galvanic coupling between deposit and substrate). Also cover dissimilar
deposition of Cu-Ni or NAB on steel, since the Navy uses bimetallic parts.
How do existing studies judge repair quality, and which tests would a Navy
reviewer expect?
"""),
    },
}

# Batch 2: written at 05:37 UTC while batch 1 was still running (Edison took
# >25 min even for standard LITERATURE jobs), so it builds on the lessons of
# the earlier aluminum/LPBF runs rather than on batch 1. Those runs found:
# the rePOWDER induction module tops out near 1300 C (so 70-30 Cu-Ni has only
# ~60 C of superheat), its sonotrode is Ti-6Al-4V (Cu-Ti forms liquid well
# below 1250 C), 40 kHz gives finer powder but more oxygen, crucible material
# was never settled, Edison's "unobtainable" items are abstract-only, and
# mock reviewers punished preliminary data on a different alloy, loose
# claims of "first", and unspecified test acceptance criteria. Batch 2 also
# checks two claims already in the copper draft with PRECEDENT jobs.
BATCHES[2] = {
    "b2-01-ultrasonic-atomization-cu-melts": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What limits ultrasonic (vibrating-sonotrode) atomization of copper
and copper-nickel melts? Specifically: (a) does Lang's relation
d50 = 0.34 (8 pi sigma / (rho f^2))^(1/3) hold for metal melts on a vibrating
plate, and what surface tension and density values (vs temperature and Ni,
Al, Fe, Mn content) should be used for Cu, 90-10 and 70-30 Cu-Ni, and NAB?
(b) How much melt superheat does ultrasonic or other drop-on-plate
atomization need to avoid freezing on the sonotrode, given that an induction
module limited to about 1300 C leaves only ~60 C above the 70-30 Cu-Ni
liquidus (1238 C)? (c) Which sonotrode materials survive copper alloy melts
(Ti-6Al-4V reacts with Cu to form liquid at low temperature; molybdenum/TZM,
niobium, ceramics or coatings), and is wetting or erosion of the sonotrode by
Cu melts reported? (d) What oxygen contents result when copper alloys are
atomized under argon, and how do 20, 35, 40 and 60 kHz compare in size,
yield and oxygen? Report any ultrasonic atomization of Cu, Cu-Ni, bronzes,
NAB or other alloys melting near 1100-1250 C, with numbers.
"""),
    },
    "b2-02-crucibles-melt-practice": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What crucible and melt practice is used for small (0.1-1 kg)
induction melts of Cu-Ni (10-30 wt% Ni) and nickel-aluminum bronze at
1150-1300 C under argon, as in small-batch powder atomizers? Compare
graphite (carbon pickup by Ni-bearing melts), clay-graphite, alumina,
zirconia, magnesia and boron nitride for reactions, contamination and thermal
shock, and say which are known to react with aluminum- or manganese-bearing
copper melts. Cover hydrogen and oxygen pickup and the steam reaction in
copper melts, deoxidizers used in Cu-Ni (Mn, Ti, Mg, B, Li, P) and their
effect on later weld or AM porosity, and how master alloys (Cu-Ni, Cu-Fe,
Cu-Mn, Cu-Al) are used to reach composition. Give typical composition losses
(e.g. Mn, Al volatilization or oxidation) if reported.
"""),
    },
    "b2-03-nickel-lean-seawater-alloys": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Which copper alloys with less nickel than 70-30 Cu-Ni come closest
to its seawater performance, and on what evidence? Compare 90-10 Cu-Ni,
Cu-Ni with Cr (C72200), manganese-aluminum bronze (C95700), aluminum bronzes
with and without Ni, Cu-Al-Fe-Mn, Cu-Ni-Sn, Cu-Ni-Al (e.g. Hiduron-type),
and Cu-Mn-Al alloys for general corrosion rate, velocity (erosion-corrosion)
limits, pitting and selective attack, sulfide resistance, and biofouling.
Give measured corrosion rates and critical velocities with test conditions.
Which of these have been made by any AM process, and with what corrosion
results? Is there evidence for a composition that matches 70-30 Cu-Ni with
substantially less nickel?
"""),
    },
    "b2-04-cracking-cuni-nab-welding": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What causes solidification cracking, liquation cracking, and
ductility-dip cracking when Cu-Ni (90-10, 70-30) and nickel-aluminum bronze
are welded or deposited, and what does that imply for designing a DED
composition? Cover the effects of Ni content and freezing range, impurity
limits (S, P, Pb, Bi, Se, Te, C, Zn), deoxidizers and grain refiners in
filler metals (ERCuNi with Ti; ERCuNiAl; ERCuMnNiAl), heat input and
restraint, and any crack-susceptibility index (Kou's |dT/d(fs)^(1/2)|, CSC,
freezing-range indices) that has been validated on copper alloys. Include
DED or laser cladding studies that report cracking of Cu alloys and what
removed it.
"""),
    },
    "b2-05-short-tests-vs-immersion": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How well do short electrochemical tests predict long immersion or
service results for Cu-Ni and NAB in seawater, and how should a one-hour
screen be designed? Report studies that measured polarization resistance,
corrosion current, breakdown/pitting potential or impedance at several
exposure times (minutes, hours, days, weeks) alongside mass loss or
long-term exposure, and the correlation they found. How long must a fresh
Cu-Ni surface be exposed before LPR or EIS values become stable, and does
pre-filming change the ranking? For NAB selective phase corrosion, how is
attack depth measured after immersion (cross-section metallography, X-ray
CT), what depths are typical after 30-90 days for cast, heat-treated and AM
NAB, and what acceptance limits do the Navy, ship classification societies,
or industry use?
"""),
    },
    "b2-06-heat-flow-models-cu-ded": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How accurately do analytical heat-flow models (Rosenthal moving
point source, Eagar-Tsai distributed source, Pinkerton's DED model) and
reduced-order numerical models predict melt-pool size, cooling rate through
solidification, and reheating peak temperatures in blown-powder laser DED,
especially for high-conductivity copper alloys? How are they calibrated
(absorptivity, effective conductivity, melt-pool width from single tracks),
and how well do predicted cooling rates match measured dendrite arm or cell
spacing? Report uses of thermal-history models to predict NAB phase
evolution (martensite, kappa precipitation during reheating) or Cu-Ni
segregation in DED, WAAM or welding, and any published temperature-dependent
thermophysical property data for NAB and Cu-Ni (e.g. from NSWC Carderock).
"""),
    },
    "b2-07-ded-process-windows-cu": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What process windows have been reported for blown-powder laser DED
of copper and copper alloys (pure Cu, CuCrZr, Cu-Sn bronzes, Cu-Ni, NAB,
GRCop-42/84), and what limits them? Give laser power, spot size, travel
speed, powder feed rate, layer height, and the resulting porosity, powder
catchment efficiency, dilution and build rate. Compare infrared (~1070 nm)
with blue (~450 nm) or green lasers for copper DED, and report preheating
and substrate effects (copper vs steel substrates). Which porosity mechanisms
(gas, keyhole, lack of fusion, evaporation of Zn/Mn) dominate for copper
alloys in DED?
"""),
    },
    "b2-08-precedent-cuni-ded-corrosion": {
        "job": "PRECEDENT",
        "query": """\
Has anyone published seawater or NaCl corrosion tests of a copper-nickel
alloy (90-10 C70600, 70-30 C71500, or a Cu-Ni-Fe-Mn variant) deposited by
blown-powder laser directed energy deposition, laser metal deposition, or
laser cladding (not wire-arc, not laser powder bed fusion)? A draft proposal
states: "We found no corrosion study of copper-nickel deposited by
blown-powder laser DED." Is that statement accurate as of October 2026? Give
any counterexamples with DOIs, including laser-clad Cu-Ni coatings on steel
tested in seawater, and suggest a safer wording if needed. Exclude
publications by Sterling G. Baird.
""",
    },
    "b2-09-precedent-as-deposited-design": {
        "job": "PRECEDENT",
        "query": """\
Has anyone designed or modified the composition of nickel-aluminum bronze,
aluminum bronze, or copper-nickel so that additively manufactured material
WITHOUT post-build heat treatment matches or beats the seawater or NaCl
corrosion resistance of the heat-treated cast or wrought alloy? Has anyone
used the reheating of earlier layers during DED (intrinsic heat treatment,
interlayer temperature control) to temper NAB or remove martensite in place?
Include Jia et al., Additive Manufacturing 127 (2026) 105291 if relevant and
say what it did. Give DOIs, and state what remains undone. Exclude
publications by Sterling G. Baird.
""",
    },
    "b2-10-commercial-cu-powders": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What is published about commercial gas-atomized Cu-Ni (90-10,
70-30) and NAB powders for AM: suppliers, size cuts offered for DED versus
LPBF, typical oxygen content, flow and apparent density, and minimum order or
lot sizes for custom compositions from industrial gas atomizers? Which
peer-reviewed studies characterized these powders before printing, and what
do studies of powder reuse in DED or LPBF report for copper alloys
(oxidation, satellites, size shift, effect on porosity)? Cite sources for any
minimum lot size; if only vendor pages state it, say so.
"""),
    },
}

# Batch 3: follows up batch 1 (all ten answers read). Batch 1 found:
# (1) a 2011 corrosion study of Cu-30Ni made by CO2-laser direct metal
# deposition on C71500 (Bhattacharya et al., J. Alloys Compd. 509, 6364),
# which contradicts the draft's "no corrosion study" sentence; (2) Jia et al.
# 2026 was unobtainable to Edison too, but the same group's 2025 Corros. Sci.
# and J. Mater. Process. Technol. papers and several 2024-2026 laser-DED NAB
# corrosion papers were identified by DOI only; (3) as-built NAB sometimes
# corrodes LESS than annealed or cast NAB (WAAM in NaCl; LPBF in 3-6 month
# seawater, per a review); (4) Mueller et al. 2024 ultrasonically atomized
# aluminium bronze chips for laser DED, the closest precedent to the
# proposed powder route; (5) no paper couples a DED thermal model to CALPHAD
# to design a copper alloy, and NAB kappa onsets shift with cooling rate
# (Kuprienko 2025, ONR-funded); (6) several ONR/Navy-funded groups work on
# WAAM Cu-Ni and NAB; (7) repair onto cast NAB exists only for a low-Ni
# CuNi2SiCr powder (Yao & Shim 2022) and for arc/wire processes.
BATCHES[3] = {
    "b3-01-dmd-cuni-corrosion-details": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Report the experimental details and results of S. Bhattacharya,
G. P. Dinda, A. K. Dasgupta, H. Natu, B. Dutta, J. Mazumder,
"Microstructural evolution and mechanical, and corrosion property evaluation
of Cu-30Ni alloy formed by direct metal deposition process", J. Alloys Compd.
509 (2011) 6364-6373 (doi:10.1016/j.jallcom.2011.03.091): powder source,
whether pre-alloyed, size, laser and nozzle, substrate, porosity, phases and
segregation, hardness and tensile data, and the corrosion test (electrolyte,
method, duration, values for deposit vs wrought C71500) and the stated cause
of any difference. Do the same, as far as available, for the companion
Cu-38Ni CO2 vs diode laser paper (J. Mater. Sci. 49 (2014) 2415), Adak et al.
2005 (laser cladding of Cu-30Ni), Karnati et al. 2019 (laser metal
deposition of Cu-Ni from blended powders, porosity linked to Ni powder
oxygen), Williams et al. 2025 (J. Manuf. Mater. Process. 9, 170, DED Cu-35Ni
single tracks), and Zhou et al. 2025 (Wear, laser-cladded Cu-Ni-xCr
coatings). Also identify the 2012 shipbuilding review by Andric et al. on
materials and fabrication that summarizes the 2011 study.
"""),
    },
    "b3-02-recent-laser-ded-nab-papers": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: Give a detailed, paper-by-paper account of laser-DED (blown
powder) work on nickel-aluminum bronze and other marine copper alloys
published 2022-2026, with full text where possible. Include at least:
Jia et al., Corrosion Science (2025) 113114 (precipitate refinement and
corrosion of AM NAB); Jia et al., J. Mater. Process. Technol. (2025) 118659
(water cooling during laser deposition of NAB); Jia et al., Additive
Manufacturing 127 (2026) 105291 (subtractive composition design of NAB);
Hu et al., J. Alloys Compd. (2026) 187981 (NAB by laser-powder DED vs LPBF);
the 2024 comparison of heat-treated NAB (C63020) made by L-PBF vs L-DED;
Rayner et al. 2024 (DED of C63020 NAB powder, Dalhousie); Zhao et al.,
Metals 12 (2022) 781 (laser-deposited NAB on SUS630 in 3.5% NaCl); the 2025
study of pre-corrosion and fatigue of DED NAB; the 2025 Additive
Manufacturing study repairing NAB by in-situ synthesis of Cu-Al alloys via
DED; the 2026 Optics and Laser Technology study of pore mitigation in DED
NAB; Wang et al. 2026 (Adv. Eng. Mater., manganese-aluminum bronze by laser
DED); and Zhao et al. 2026 (SSRN, Cr and Zr microalloying of
Cu-8Al-6Ni-4Fe-2Mn for seawater). For each: process and feed, composition,
phases as deposited, porosity, corrosion test and numbers, mechanical
numbers, and what it means for a proposal that designs new DED powder
compositions for as-deposited seawater resistance.
"""),
    },
    "b3-03-as-built-vs-annealed-nab": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Across processes (LPBF, laser DED, wire-arc DED, welds, castings),
does post-build or post-weld annealing (e.g. 675 C / 6 h, 1250 F) improve or
worsen nickel-aluminum bronze corrosion and selective phase corrosion? Build
a table of studies that tested BOTH as-built and annealed NAB in the same
electrolyte. Verify from the primary article: Murray et al., "Selective
laser melting of nickel aluminium bronze", Additive Manufacturing 33 (2020)
101122 - natural or substitute seawater, exposure times, mass losses for
as-built vs cast vs wrought; Shahriari et al. 2023 (npj Mater. Degrad., WAAM
NAB, as-built best); Barr et al. 2022 (LPBF composition and heat treatment);
Morshed-Behbahani et al. 2024 (LPBF NAB, as-built vs tempered); and any
DED study. When does martensitic or beta-prime-rich as-deposited NAB corrode
less, and when more (e.g. heat-affected zones of welds)? What microstructural
variable best predicts the outcome?
"""),
    },
    "b3-04-ultrasonic-atomized-cu-for-ded": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Report everything available on ultrasonic atomization of copper
alloys and on powders made from copper alloy scrap or machining chips for
DED. Start with Mueller et al. 2024, IOP Conf. Ser. Mater. Sci. Eng. 1296,
012036 (doi:10.1088/1757-899x/1296/1/012036): which atomizer and frequency,
melting method, feedstock (aluminium bronze chips), particle size, shape,
oxygen, yield, and how the powder performed in laser DED. Then: other
ultrasonic or small-batch atomization of Cu, bronzes, Cu-Ni or NAB;
AMAZEMET rePOWDER reports for any alloy melting above 1100 C with the
induction module (crucible plus pour onto the sonotrode) rather than arc or
plasma; and work on recycling naval copper alloy scrap or chips into AM
powder (point-of-need or shipyard sustainment). Give particle-size numbers
with frequency and melt temperature where reported.
"""),
    },
    "b3-05-calphad-nab-kappa-martensite": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How well can CALPHAD and related models predict the phases of
nickel-aluminum bronze after rapid cooling and reheating? Cover: published
thermodynamic assessments of Cu-Al-Ni-Fe(-Mn) and how kappa phases (kappa-I/
II Fe3Al-based, kappa-III NiAl B2, kappa-IV) and beta/beta-prime are
modeled; the Thermo-Calc TCCU versions and any published validation for
NAB; measured vs calculated beta solvus, eutectoid and kappa-precipitation
temperatures (e.g. DTA data at different cooling rates, Kuprienko 2025);
empirical or model equations for the martensite start temperature of
Cu-Al(-Ni-Fe-Mn) as a function of composition; and critical cooling rates
for retaining beta-prime. Which of these quantities could be computed per
candidate composition as a cheap physics node, and how accurate are they?
"""),
    },
    "b3-06-thermal-history-phase-response": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What quantitative links exist between laser-DED or laser-cladding
thermal history and the phases of NAB and Cu-Ni deposits? Report measured or
modeled cooling rates (K/s), interlayer temperatures, linear energy
(J/mm), substrate cooling (e.g. water-cooled substrates), and the resulting
beta-prime martensite fraction, kappa precipitate size and type, Widmanstatten
alpha, dendrite or cell spacing, and Ni/Fe/Mn microsegregation, together with
any corrosion or hardness consequence. Include Hyatt, Magee and Betancourt
1998 (laser-clad NAB, 42.5-595 J/mm), Jia et al. 2025 (water cooling), Li et
al. 2021 (LMD NAB), and studies of intrinsic heat treatment by later layers.
Which thermal-history variables (peak reheat temperature, time above the
beta solvus, cooling rate through 800-500 C) are most predictive?
"""),
    },
    "b3-07-navy-funded-cu-am-programs": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Which research groups have had ONR, NAVSEA, NAVAIR, NRL, NSWC,
or other US Navy support (2018-2026) for additive manufacturing, welding or
repair of copper-nickel and nickel-aluminum bronze, according to the
acknowledgments and affiliations of their papers, theses and reports? For
each give the group, institution, process (WAAM, wire-laser DED, powder DED,
LPBF, cold spray, friction stir), alloy, topic, and grant number if
printed. Known leads: Song, Jimenez, To and Fu (ONR N00014-21-1-2800, WAAM
Cu-Ni corrosion); Lewandowski (Case Western, ONR, WAAM 70-30 Cu-Ni with
Lincoln Electric and NRL); Kuprienko (Ohio State, ONR Manufacturing Science,
WAAM NAB); Doyle (Oregon State, Navy grant, wire-laser DED NAB); Sparrow,
Smith and Ansell (Naval Postgraduate School, LPBF C71500); Norkett and Fisher
(NSWC Carderock, NAB and Cu-Ni property databases); Penn State ARL. Which
gaps do these programs leave for blown-powder DED and alloy design?
"""),
    },
    "b3-08-cavitation-erosion-am-cu": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How do additively manufactured or laser-clad NAB and Cu-Ni resist
cavitation erosion, erosion-corrosion and jet impingement compared with cast
and wrought material? Report test methods (ASTM G32 vibratory cavitation,
G134 cavitating jet, G73 liquid impingement, jet-in-slit, rotating cylinder),
seawater or NaCl media, incubation times and mass-loss rates, and how
as-deposited martensite, kappa phases, grain size and porosity change the
result. Include laser surface melting or cladding of NAB propellers and any
DED or WAAM data. Which of these tests could serve as a mid-cost node
between a one-hour polarization screen and a 30-day immersion?
"""),
    },
    "b3-09-precedent-ni-bearing-repair": {
        "job": "PRECEDENT",
        "query": """\
Has anyone deposited a nickel-bearing nickel-aluminum bronze powder or a
10-30 wt% Ni copper-nickel powder by blown-powder laser directed energy
deposition or laser cladding onto CAST nickel-aluminum bronze or onto
WROUGHT copper-nickel as a repair, and measured cracking, dilution, the
heat-affected zone, or corrosion of the fusion zone and heat-affected zone?
Known near misses: Yao & Shim 2022 (CuNi2SiCr powder on NAB, low Ni), Hyatt
et al. 1998 (laser cladding NAB on NAB with a consumable), Bhattacharya et
al. 2011 (Cu-30Ni direct metal deposition on C71500), and the 2019 Springer
chapter "Laser-Additive Repair of Cast Ni-Al-Bronze Components". Give DOIs,
what each tested, and what remains undone. Exclude publications by Sterling
G. Baird.
""",
    },
    "b3-10-porosity-oxygen-cu-deposits": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What causes gas porosity in laser-deposited and welded Cu-Ni and
aluminum bronzes, and what powder oxygen and moisture limits follow? Cover
the steam reaction (Cu2O + 2H -> 2Cu + H2O), hydrogen and nitrogen pickup,
oxide films on Al-bronze powders, why ERCuNi filler metals contain Ti and Mn
(deoxidizers) and what happens without them, the porosity reported for
laser-deposited Cu-30Ni and blended Cu-Ni powders, shielding gas choices,
and any quantitative relationship between powder oxygen (ppm) and deposit
porosity for copper alloys in DED or LPBF. Should a DED powder for Cu-Ni
contain a deoxidizer such as Ti, and how much?
"""),
    },
}

# Batch 4: follows up batch 2 (all ten read). Batch 2 found: (1) Uhlmann et
# al. 2024 (Materials 17, 3396) and Mueller et al. 2023 induction-melted NAB
# propeller-grinding chips at 1300 C and atomized them on a 40 kHz
# carbon-fiber sonotrode for laser DED: X50 98 um, 190 ppm O, carbon fibers
# in the powder; Ti-6Al-4V sonotrodes react with Cu (Ti-Cu eutectics 875 and
# 960 C); TZM worked for C103; (2) crucible choice for 0.1-1 kg Cu-Ni/NAB
# melts is unvalidated (alumina or stabilized zirconia first); (3) C72200
# (Cu-16Ni-0.5Cr) is the strongest low-Ni high-flow candidate, with
# quiet-water localized attack as its risk; (4) Cu-Ni welds are limited by
# porosity more than cracking, cast 70-30 can hot crack, single-phase Al
# bronze filler cracks but duplex filler does not; Kou/CSC indices are not
# validated for copper alloys; (5) fresh 70-30 corrosion current falls
# 8.4-fold over 10 days (Yuan & Pehkonen 2007), so one-hour screens can
# mislead; (6) as-built WAAM 70-30 beat wrought C71500 in short NaCl tests
# (Song 2024, ONR-funded); (7) heat-flow models need fitted conductivity and
# validated reheating outputs.
BATCHES[4] = {
    "b4-01-ultrasonic-nab-powder-deposits": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What happened when ultrasonically atomized copper alloy powder was
actually deposited by laser DED? Follow the Berlin group (Uhlmann, Polte,
Fasselt, Mueller, Kloetzer-Freese, Kleba-Ehrhardt, Biegler, Rethmeier; TU
Berlin / Fraunhofer IPK / BAM) after Uhlmann et al. 2024, Materials 17, 3396
and Mueller et al. 2023, IOP Conf. Ser. Mater. Sci. Eng. 1296, 012036: deposit
density, porosity, catchment, microstructure, hardness, tensile, corrosion,
and comparison with gas-atomized NAB powder; how carbon-fiber sonotrode
debris affected deposits; any repair of propeller bronze. Also report any
other study (any alloy) that printed ultrasonically atomized powder by DED
or LPBF and compared it with gas-atomized powder of the same alloy.
"""),
    },
    "b4-02-sonotrode-and-wetting": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Which materials can contact molten copper, Cu-10Ni to Cu-30Ni, and
aluminum bronze at 1150-1300 C as an ultrasonic sonotrode or melt-delivery
nozzle without dissolving, being wetted, or contaminating the powder? Report
wetting angles and dissolution or erosion data for Cu and Cu-Ni melts on
molybdenum and TZM (note Ni-Mo solubility and intermetallics), tungsten,
niobium, tantalum, graphite and carbon fiber, SiC, Si3N4, sialon, alumina,
zirconia, and boron nitride, and any coatings used on ultrasonic horns or
sonotrodes in molten copper (e.g. ultrasonic degassing or melt treatment of
copper alloys). Which would you test first for a 20-60 kHz sonotrode?
"""),
    },
    "b4-03-liquid-properties-cuni-nab": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What measured liquid density, surface tension, and viscosity data
(vs temperature) exist for Cu-Ni alloys (10-30 wt% Ni, with Fe and Mn), for
Cu-Al and Cu-Al-Ni-Fe (aluminum bronze / NAB) melts, and for pure Cu?
Include electromagnetic levitation, sessile drop, and oscillating drop
results (e.g. Egry, Brillo, Schmitz), the effect of oxygen on Cu surface
tension, and models (Butler) for multicomponent melts. Using these, what
capillary-wave (Lang) droplet sizes follow at 20, 40 and 60 kHz for 90-10
Cu-Ni, 70-30 Cu-Ni and NAB at 50-100 C superheat, and how do they compare
with measured ultrasonic-atomized powder sizes for NAB (X50 about 98 um at
40 kHz) and other metals?
"""),
    },
    "b4-04-chromium-modified-cuni": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What is known about chromium-modified copper-nickel alloys
(C72200 Cu-16Ni-0.5Cr; CuNi30Cr2 / IN-768 castings used by navies; Cu-30Ni-
xCr) as seawater alloys and as candidates for welding or additive
manufacturing? Cover Cr solubility and Cr-rich precipitates, the effect of
Cr segregation on quiet-water localized corrosion, erosion-corrosion and
critical velocity data, weldability and filler metals, and any laser
cladding, DED or LPBF studies (e.g. Gao et al. 2025 SLM Cu-30Ni-xCr with
mixed powders; Zhou et al. 2025 Wear, laser-cladded Cu-Ni-xCr). What Cr
range would a DED powder design space reasonably span?
"""),
    },
    "b4-05-al-bronze-phase-and-cracking": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How do Al content and phase constitution (single-phase alpha vs
duplex alpha+beta; Fe and Ni additions) control hot cracking and porosity
when aluminum bronzes and NAB are welded, clad, or deposited, and how does
that interact with seawater corrosion (selective phase corrosion of beta /
beta-prime, kappa-III)? Report filler metal studies (ERCuAl-A1, A2, A3,
ERCuNiAl, ERCuMnNiAl), the Al and Fe thresholds where cracking or selective
attack appears, and DED or laser cladding examples. What composition
window would avoid both cracking and selective phase corrosion as deposited?
"""),
    },
    "b4-06-accelerated-corrosion-screening": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What accelerated or high-throughput corrosion screening methods
have been used for copper alloys in seawater or chloride, and how well do
they predict longer tests? Cover scanning droplet cells and combinatorial
electrochemistry, multi-electrode arrays, electrochemical noise, zero-
resistance-ammeter galvanic tests, accelerated pre-filming of Cu-Ni (e.g.
ferrous sulfate dosing, controlled clean-seawater prefilming), jet
impingement and rotating cylinder electrodes, and autonomous or robotic
corrosion testing. Give timescales, throughput, and any reported rank
correlation with 30-day or longer immersion for Cu-Ni or NAB.
"""),
    },
    "b4-07-bo-for-ded-process-windows": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How have Bayesian optimization, active learning, and
physics-informed or multi-fidelity surrogates been used to find blown-powder
DED process windows (single tracks, walls, blocks) for any alloy, and with
what savings? Include work that uses analytical thermal models or
normalized process maps as priors or low-fidelity sources, constrained BO
for crack-free/dense deposits, and studies that tune DED settings together
with alloy composition (e.g. compositionally graded DED, in-situ alloying
for alloy discovery). Name the closest analogues to a cost-aware search
over composition, powder, and DED settings with corrosion as an objective,
and report the number of experiments they needed.
"""),
    },
    "b4-08-am-qualification-marine": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What qualification frameworks and acceptance tests apply to
additively manufactured copper alloy parts and repairs for ships? Cover
classification-society rules (DNV-ST-B203, ABS guidance on additive
manufacturing, Lloyd's Register), ASTM F3413/F3187 for DED, AWS D20.1,
NAVSEA technical publications on AM and on NAB propeller repair, and
published case studies of qualifying printed Cu-Ni or NAB parts (valves,
deck drains, propeller repair). What tests (chemistry, density, CT, tensile,
bend, Charpy, corrosion) and acceptance values do they require, and which
of these could a university project reasonably supply?
"""),
    },
    "b4-09-precedent-ua-powder-ded": {
        "job": "PRECEDENT",
        "query": """\
Has anyone deposited ultrasonically atomized metal powder (any alloy;
vibrating sonotrode or plate atomization such as AMAZEMET rePOWDER) by
blown-powder laser directed energy deposition and reported deposit
density, microstructure, or properties, ideally compared with gas-atomized
powder of the same alloy? In particular, has the aluminium bronze powder of
Uhlmann et al. 2024 (Materials 17, 3396) or Mueller et al. 2023 (IOP Conf.
Ser. Mater. Sci. Eng. 1296, 012036) been deposited and tested? Give DOIs.
Exclude publications by Sterling G. Baird.
""",
    },
    "b4-10-nickel-lean-am-alloys": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What additive manufacturing (any process) and laser cladding
results exist for nickel-lean marine copper alloys: manganese-aluminum bronze
(C95700, CuMn11-13Al8Fe3Ni2-3), Cu-Ni-Al (5-15 Ni, 1-3 Al, e.g. Hiduron-type
or Cu-7Ni-3Al-1Fe-1Mn), and Cu-Al-Fe-Mn without Ni? Report process,
composition, as-deposited phases (beta, kappa, NiAl/Ni3Al precipitation
during reheating), porosity, and corrosion in NaCl or seawater, especially
Wang et al. 2026 (Adv. Eng. Mater., MAB by laser DED) and Ziqiang et al. 2025
(Sci. Rep., laser cladding of ZCuAl8Mn13Fe3Ni2 propeller alloy). Which
nickel-lean composition is the most promising starting point for a DED
powder, and why?
"""),
    },
}

# Batch 5: follows up batch 3 (all ten read) and checks the claims the
# proposal will now make. Batch 3 found: (1) the 2011 Cu-30Ni DMD deposit on
# C71500 corroded faster than the wrought plate, which a 2012 ISSC committee
# review attributes to porosity; (2) the AMAZEMET AUS 500 run on NAB chips
# (not a rePOWDER) and a rePOWDER run on copper cable scrap fed laser DED
# (Cabrioli et al. 2025); (3) whether annealing helps NAB depends on the
# starting microstructure, and the WAAM as-built-vs-annealed comparison had
# unequal pre-immersion; (4) kappa onsets shift with hold time and cooling
# rate (Kuprienko 2025), and no Ms equation for NAB was found; (5) the
# Dalhousie group (Bishop, Nasiri, Rayner, Morshed-Behbahani) works on DED and
# LPBF NAB; (6) DED-NAB and WAAM-NAB cavitation papers exist; (7) Edison's
# HIGH job contradicted earlier jobs on what exists (it missed pre-2022 work).
BATCHES[5] = {
    "b5-01-precedent-final-novelty": {
        "job": "PRECEDENT",
        "query": """\
Check this claim for counterexamples published up to October 2026: "No
published study has (a) designed a new copper alloy composition for
blown-powder laser directed energy deposition with a search that evaluates
CALPHAD along a modeled DED thermal history, (b) made each candidate as
pre-alloyed powder in-house, and (c) tested the as-deposited alloy against
wrought 70-30 copper-nickel (C71500) in seawater, including deposits on
cast nickel-aluminum bronze and wrought copper-nickel." Consider each part
separately and in combination, include Jia et al. 2026 (Addit. Manuf. 127,
105291), Uhlmann et al. 2024, Cabrioli et al. 2025, Bhattacharya et al.
2011, Li et al. 2021, and any 2025-2026 work, and propose the narrowest
accurate wording. Exclude publications by Sterling G. Baird.
""",
    },
    "b5-02-dalhousie-nab-program": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Summarize the Dalhousie University program on additively
manufactured nickel-aluminum bronze (D. P. Bishop, A. Nasiri, A. J. Rayner,
K. Morshed-Behbahani, K. A. Timmons and co-workers), with numbers:
Morshed-Behbahani et al., Colloids Surf. A 708 (2025) 136069 (heat-treated
NAB by L-PBF vs L-DED, corrosion); Morshed-Behbahani et al., Corros. Sci.
228 (2024) 111846 (unusual electrochemical corrosion of LPBF NAB); Rayner et
al., COM 2024 (DED of C63020 powder) and the companion arc-DED heat
treatment paper; the 2025 CIRP J. Manuf. Sci. Technol. surface
post-treatment study; and Timmons et al. 2025 (LPBF C64200). Which process
gave better corrosion resistance and why, what were the powders (size,
source), and who funds the program (e.g. Canadian Department of National
Defence)?
"""),
    },
    "b5-03-martensite-start-al-bronze": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What composition-based rules predict whether beta-prime martensite
is retained in aluminum bronzes and NAB after fast cooling? Cover (a)
martensite start (Ms) equations for Cu-Al-Ni and Cu-Al-Mn shape memory
alloys as functions of Al, Ni, Mn (and Fe) content, and whether they apply
to NAB compositions; (b) the "aluminium equivalent" rules used for aluminum
bronzes (weighting of Fe, Ni, Mn, Si, Sn relative to Al) and their link to
beta content; (c) the beta-solvus and eutectoid temperatures vs composition;
and (d) kappa precipitation kinetics models (JMAK fits, TC-PRISMA /
Kampmann-Wagner, phase-field) for NAB under rapid cooling or cyclic
reheating. Which could serve as a cheap, per-composition physics input next
to CALPHAD, and how accurate is each?
"""),
    },
    "b5-04-cavitation-ded-waam-nab": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Report the methods and numbers of "Advanced cavitation
erosion-corrosion resistance of nickel-aluminum bronze prepared by directed
energy deposition", Corros. Sci. (2024) 111982
(doi:10.1016/j.corsci.2024.111982), and "Comparative analysis of cavitation
erosion behavior in wire-arc directed energy deposition and cast
nickel-aluminum bronze alloys", Ultrason. Sonochem. (2025) 107235
(doi:10.1016/j.ultsonch.2025.107235): process (powder or wire, laser or
arc), composition, test standard and medium, incubation time, mass-loss
rates vs cast NAB, and the microstructural reasons. Also cover friction-stir
processed NAB cavitation as a reference. What does this imply for using a
cavitation test as a mid-cost screening node for propeller-repair alloys?
"""),
    },
    "b5-05-nab-am-2026-details": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Give details (process, composition, phases, density, mechanical
and corrosion numbers) of these 2025-2026 NAB additive manufacturing
papers: Hu et al., J. Alloys Compd. 1066 (2026) 187981 (laser-powder DED vs
LPBF NAB); Saremi et al., Virtual Phys. Prototyp. 21 (2026) e2688627
(heated-platform LPBF NAB design); Roshan et al., Mater. Chem. Phys. 349
(2026) 131759 (pre-corrosion and fatigue of DED NAB); Yao et al., Addit.
Manuf. 105 (2025) 104787 (repair of NAB by in-situ Cu-Al synthesis via DED);
Yao, Shin and Shim (laser remelting for pore mitigation in DED NAB);
Mahmoudiniya et al., Mater. Sci. Eng. A 961 (2026) 150140 (NAB/martensitic
stainless steel by DED); and Wu et al., Mater. Sci. Eng. A 973 (2026) 150695
(wire flat-top laser DED NAB). Which of them report as-deposited corrosion,
and how do DED and LPBF NAB compare?
"""),
    },
    "b5-06-corrosion-metrology-cu": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What are the known pitfalls in measuring corrosion rates of copper
alloys (Cu-Ni, NAB) electrochemically, and what protocol gives defensible
numbers? Cover Tafel extrapolation when the cathodic reaction is
oxygen-diffusion limited, Stern-Geary B values used for Cu-Ni and NAB in
LPR (ASTM G59/G102), EIS equivalent circuits for duplex Cu2O films, effects
of surface finish and pre-immersion time, reference electrodes in seawater,
substitute ocean water (ASTM D1141) vs 3.5% NaCl vs natural seawater, and
how selective phase corrosion depth is measured after immersion
(cross-sections, profilometry, CT). Recommend a protocol for a one-hour
screen plus 30-day immersion on small AM coupons.
"""),
    },
    "b5-07-absorptivity-catchment-cu": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What measured laser absorptivities exist for copper, Cu-Ni,
bronzes and NAB, as solid surfaces, powders, and melt pools, at 1030-1070 nm
(and 450-532 nm for comparison), e.g. from calorimetry or integrating-sphere
measurements during DED or LPBF? How do absorptivity and powder catchment
efficiency in coaxial blown-powder DED depend on particle size (e.g. 45-150
um), powder stream focus and laser spot for copper alloys, and which
analytical models of catchment (e.g. Ancalmo and Narra 2025) have been
validated? Give numbers usable to calibrate a heat-flow model for Cu-Ni and
NAB deposits.
"""),
    },
    "b5-08-point-of-need-recycling": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What work exists on turning naval or maritime copper alloy scrap
(NAB propeller grinding chips, Cu-Ni pipe offcuts, cable copper) into AM
feedstock at or near the point of need, and what does it show about powder
quality, cost, energy, and logistics? Cover the EU MarTERA project
(Uhlmann et al. 2024; Mueller et al. 2021, 2023), Cabrioli et al. 2025
(rePOWDER atomization of offshore-cable copper for laser DED, life-cycle
assessment), Navy or DoD expeditionary or shipyard powder-making efforts
(e.g. recycling chips on ships, ultrasonic atomizers on vessels), and any
analysis of how small-lot atomization changes qualification. Quote numbers
(yields, oxygen, energy, CO2) where reported.
"""),
    },
    "b5-09-bo-delayed-long-experiments": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What Bayesian optimization and active-learning methods handle
experiments that take weeks and give partial readings along the way (e.g.
corrosion films that evolve, creep, fatigue), and experiments still pending
when the next choice is made? Cover freeze-thaw BO and learning-curve
extrapolation, multi-fidelity BO with time or duration as the fidelity,
asynchronous batch BO with pending points (fantasies, local penalization),
BO with delayed feedback, and cost-aware stopping of running experiments.
Report any applications to corrosion, materials degradation, or alloy design,
and say which is closest to deciding, candidate by candidate, whether a
30-day immersion is worth starting given a one-hour electrochemical screen.
"""),
    },
    "b5-10-cuni-segregation-film-am": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How does dendritic segregation of Ni, Fe and Mn in as-solidified
or as-deposited Cu-Ni (welds, castings, WAAM, LPBF, laser deposits) change
corrosion product film formation and localized attack in seawater, and how
large is the segregation (EDS/EPMA core-to-interdendrite contrast) as a
function of cooling rate? Include Song et al. 2024 (WAAM 70-30), Liu et al.
2024 and Nadimi et al. 2025 (LPBF 70-30), Cu-Ni weld metal studies, and the
role of Fe in solution vs precipitated. Can a Scheil or back-diffusion
calculation predict the measured contrast, and does it predict corrosion?
"""),
    },
}

# Batch 6 (2026-10-17, afternoon): three LITERATURE_HIGH follow-ups, asked for
# as "a couple high effort follow ups" after the 50-query run. b6-01 follows
# up the open DED-facility TODO and the question of whether the University of
# Utah's InssTek (an MX-Lab: 300-500 W ytterbium fiber laser, 400 um beam,
# six hoppers) can deposit Cu-Ni and NAB, or whether a blue laser is needed;
# it builds on b2-07 and b5-07 (pure-Cu optics only). b6-02 audits the draft's
# claims that rest on Edison readings or abstracts, after a manual check found
# one written backwards (Ni is enriched in the dendrite cores of printed 70-30,
# not between them; b5-10). b6-03 asks whether the MX-Lab's multi-hopper
# blending can be a cheap, lower-fidelity node ahead of atomizing a
# pre-alloyed lot (builds on b4-07, b5-01 and Yao et al. 2025).
AUDIT_OUTPUT = """\
OUTPUT FORMAT: Go claim by claim (C1, C2, ...). For each give a verdict:
SUPPORTED (as written), WEAKER (supported only in a narrower or different
form; give corrected wording of at most two sentences), CONTRADICTED (give
the contrary evidence), or UNCHECKABLE (say what could not be read). Cite the
best source with DOI and state the exact finding it reports: process,
composition, test medium and duration, and the numbers. Say whether you read
the full text, the abstract, or a later paper or review that reports it.
Then, for the novelty claim N, list any published study that combines two or
more of its three parts, with DOI and what it did. End with a ranked list of
the corrections the PI must make before submission.
"""

BATCHES[6] = {
    "b6-01-laser-and-system-for-cu-ded": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: The blown-powder DED system the PI can reach is an InssTek MX-Lab
at the University of Utah (InssTek's DMT process: coaxial blown-powder laser
DED with closed-loop melt-pool height control; ytterbium fiber laser near
1.07 um, 300 W or 500 W maximum depending on configuration; 400 um beam;
150 x 150 x 150 mm stroke; up to six powder hoppers; optional argon
atmosphere with O2 at or below 50 ppm). Is this adequate for depositing
90-10 and 70-30 Cu-Ni (with Fe, Mn, Cr) and NAB, both built on themselves and
on cast NAB and wrought Cu-Ni plate, or is a blue (about 450 nm) or green
(about 515 nm) laser, or a multi-kilowatt infrared system, needed?
(1) Which papers deposited Cu-Ni, NAB, aluminum bronze, Mn-Al bronze,
CuNi2SiCr, CuSn or other copper alloys by blown-powder laser DED with an
infrared laser at or below 1 kW? Give spot, power, travel speed, feed rate,
density, cracking and dilution. Include LENS (Optomec) work at 400-500 W
(e.g. GRCop-84 on Inconel 718), Missouri S&T work on Cu-Ni from blended
powders, and the direct metal deposition (DMD) Cu-30Ni papers (Bhattacharya
et al. 2011, J. Alloys Compd. 509:6364; Mukherjee and Ghosh 2011, Mater. Sci.
Eng. A 528:3289), with their laser type and power.
(2) Which copper alloy papers used InssTek DMT machines (MX-3, MX-400,
MX-600, MX-1000, MX-Grande, MX-Lab)? In particular, which machine and laser
power did D.-S. Shim's group (Korea Maritime and Ocean University) use for
CuNi2SiCr and in-situ Cu-Al deposited on cast NAB (Yao et al. 2022, J. Mater.
Res. Technol. 18:5337 and J. Alloys Compd. 918:165776; Yao et al. 2025,
Addit. Manuf. 105:104787)? Any Korean propeller repair or Cu/steel bimetal
work on InssTek machines?
(3) How do Cu-Ni and NAB differ from pure Cu and CuCrZr in absorptivity near
1.07 um (solid, powder, melt pool) and in thermal conductivity, and what does
that imply for the minimum power to melt them with a 0.4 mm beam (e.g. a
normalized-enthalpy or Rosenthal estimate)? Report measured or modeled values
for Cu-Ni or NAB, not only pure Cu.
(4) Where have blue or green lasers been shown to matter for copper alloy DED
or cladding (pure Cu, CuCrZr, GRCop, CuSn, Cu-Ni, NAB)? Quantify the gain
over infrared on the same alloy: deposition or catchment efficiency,
porosity, dilution, minimum power, width of the process window. Has any Cu-Ni
or NAB been deposited with a blue or green laser?
(5) For deposits on large copper alloy substrates (cast NAB, wrought Cu-Ni,
pure Cu), what power, preheat and travel speed avoided lack of fusion at the
interface, and what dilution and heat-affected zone resulted? Does a
300-500 W, 0.4 mm beam limit repair coupons, and how have others worked
around low power (preheating, thin substrates, higher feed)?
(6) Is back-reflection from copper into fiber lasers documented as a risk in
DED, and what protections are used?
(7) Which US university, national laboratory, Navy laboratory or commercial
service has published blown-powder laser DED of copper alloys with blue
lasers or with infrared lasers of 1 kW or more, and on which systems?
"""),
    },
    "b6-02-claims-audit": {
        "job": "LITERATURE_HIGH",
        "query": CONTEXT + """
QUESTION: Audit these claims from the draft proposal. Each gives the source
the draft cites. Several were taken from abstracts or from a literature
agent's reading, not from the full text.
C1. In laser-deposited NAB, fast cooling can retain martensitic beta' that
corrodes selectively in seawater (Liu et al. 2021, Mater. Sci. Eng. A
826:142006; Dobson et al. 2024, Corros. Sci. 232:112004).
C2. Laser-deposited NAB contains martensitic beta' along with alpha and kappa
phases and is much stronger than cast NAB (Liu et al. 2021; Li et al. 2021,
Addit. Manuf. 39:101825).
C3. NAB made by laser powder bed fusion formed stronger films than wrought NAB
but resisted localized corrosion worse, and annealing reversed both
(Morshed-Behbahani et al. 2024, Corros. Sci. 228:111846).
C4. Wire-arc NAB corroded in its residual beta phase (Cai et al. 2023,
Corros. Sci. 214:111040).
C5. The same 700 C anneal lowered the corrosion current of cast NAB after
480 h in salt solution and raised that of sintered NAB (Fayanas et al. 2025,
J. Jpn. Soc. Powder Powder Metall. 72:S819).
C6. As-built wire-arc NAB resisted corrosion better than annealed coupons, in
a test with unequal immersion times (Shahriari et al. 2023, npj Mater.
Degrad. 7:85).
C7. Laser-deposited NAB on SUS630 stainless steel was attacked 1.8 to 3.4 um
deep in 21 days in 3.5% NaCl, most where iron from the steel diluted it (Zhao
et al. 2022, Metals 12:781).
C8. In plasma-welded NAB, retained beta' in the heat-affected zone corroded
selectively in seawater (Dobson et al. 2024, Corros. Sci. 232:112004), and
welded NAB corroded faster in natural than in simulated seawater (Dobson et
al. 2024, Biofouling 40:193).
C9. In printed 70-30 Cu-Ni, Ni is enriched in the dendrite or cell cores, the
Ni-poor regions between them are attacked first, and the corrosion film forms
unevenly (Song et al. 2024, Materials 17:876, wire-arc; Liu et al. 2024,
Corros. Sci. 232:112040, LPBF).
C10. The corrosion resistance of LPBF 70-30 depends on the laser settings
(Nadimi et al. 2025, J. Alloys Metall. Syst. 9:100155).
C11. As-built wire-arc 70-30 beat wrought plate in three-hour tests in salt
solution (Song et al. 2024).
C12. The one corrosion study of Cu-Ni made by blown-powder laser DED is
Bhattacharya et al. 2011 (J. Alloys Compd. 509:6364; CO2-laser direct metal
deposition of Cu-30Ni on wrought 70-30 plate), and the deposit corroded
faster than the plate because of porosity (ISSC 2012 Committee V.3 report).
Give the electrolyte, duration and numbers if any source reports them, and
name any other corrosion study of laser-deposited or laser-clad Cu-Ni.
C13. On 70-30 Cu-Ni in synthetic seawater, the corrosion current fell more
than eightfold over the first ten days, 8.44 to 1.01 uA/cm2 (Yuan and
Pehkonen 2007, Corros. Sci. 49:1276).
C14. The corrosion product film on Cu-Ni builds up over weeks to months, and
films on 90-10 tubes in natural seawater were still changing after six months
(Ma et al. 2015, Corros. Sci. 91:245; Ekerenam et al. 2018, Acta Metall. Sin.
Engl. Lett. 31:1148); the alloy's iron content changes the film (Zhu et al.
2021, Anti-Corros. Methods Mater. 68:113).
C15. Ultrasonic atomizers have made powder for blown-powder DED from NAB
grinding chips (Mueller et al. 2023, IOP Conf. Ser. Mater. Sci. Eng.
1296:012036; Uhlmann et al. 2024, Materials 17:3396) and from copper cable
scrap (Cabrioli et al. 2025, J. Manuf. Mater. Process. 9:320), but only in
existing compositions.
C16. Solidification-cracking indices (Kou 2015 and similar) have been checked
against printed aluminum alloys, steels, nickel superalloys and high-entropy
alloys, but not copper alloys (Jordan and Zhang 2026).
N. Novelty: no published study combines (a) a copper alloy composition
search that evaluates CALPHAD along a modeled DED thermal history, (b)
in-house pre-alloyed powder for every candidate, and (c) as-deposited
seawater corrosion tests against wrought C71500, including deposits on cast
NAB and wrought Cu-Ni.

""" + AUDIT_OUTPUT,
    },
    "b6-03-blended-vs-prealloyed-ded": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: The University of Utah's InssTek MX-Lab can feed up to six powders
at once, so a composition can also be made in the melt pool from blends of
elemental, master-alloy, or commercial pre-alloyed copper alloy powders
before the ultrasonic atomizer makes a pre-alloyed lot of it. Could such
in-situ alloyed deposits be a cheap, lower-fidelity stand-in for deposits
from pre-alloyed powder in a multi-fidelity search? Cover copper alloys first
(Cu-Ni from Cu + Ni or Cu + Cu-Ni powders; Cu-Al and NAB from Cu + Al or
Cu + Al-alloy powders, e.g. Yao et al. 2025, Addit. Manuf. 105:104787;
graded Cu-Ni or Cu-Al deposits; Missouri S&T work on Cu-Ni from blended
elemental powders), then other alloys (Ti-6Al-4V and Ti alloys from elemental
blends, Ni superalloys, steels, high-entropy alloys, e.g. Nelaturu et al.
2024 and Kitt et al. 2024; compositionally graded libraries). Report:
(1) composition accuracy and homogeneity against the target (EDS or ICP maps,
unmelted or partly melted particles, macrosegregation, evaporation losses of
Mn and Al); (2) porosity, cracking and microstructure (phases, grain size,
martensite) compared with the same composition deposited from pre-alloyed
powder; (3) differences in hardness, tensile properties and especially
corrosion in NaCl or seawater between blended and pre-alloyed deposits;
(4) whether rankings of compositions by hardness, cracking or corrosion from
blended deposits agree with rankings from pre-alloyed deposits or from cast
or wrought material, with numbers; (5) any multi-fidelity, transfer-learning
or active-learning work that used blended-powder DED or graded libraries as a
lower-fidelity source; (6) practical problems of multi-hopper feeding with
powders of different density and size (e.g. Cu, Al, Ni), feed-rate
calibration, and separation of particles in the stream. Say plainly where no
blended-versus-pre-alloyed comparison exists for copper alloys.
"""),
    },
}
