"""Questions for edison_insstek.py. Batch N+1 was written after reading batch N;
the comment above each batch says what it follows up on.

Trigger (PR #117, 2026-11-10): a summary of InssTek's material database, as
posted in the PR by the PI. It lists "Al-Bronze / UNS C95300" as a qualified
DED material: Cu balance, Al 9-11%, Fe 0.8-1.5%; typical powder size average
about 83.8 um; melting range 1040-1045 C; applications listed as ship
propellers and marine components; InssTek DMT-produced tensile strength
628 MPa (XY) / 598 MPa (Z)."""

CONTEXT = """\
CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications)
submitted an ONR FY2027 Young Investigator Program proposal in October 2026 to
design new pre-alloyed copper alloy powders for single-stream blown-powder
laser directed energy deposition (DED). Goals: deposits that are dense and
crack-free, built on themselves and deposited on cast nickel-aluminum bronze
(NAB, UNS C95800) and wrought Cu-Ni (repair), that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). The searched space is Cu at least 65 wt% with Ni 0-30,
Al 0-9.5 (upper bound set by retained beta-prime martensite as deposited),
Fe 0-4.5, Mn 0-4, Ti 0-0.5, plus Cr, Si, Nb in Cu-Ni only, with NAB family
rules (above 7 Al: Fe <= Ni <= 5.5). Powder is made in-house by ultrasonic
atomization (AMAZEMET rePOWDER, 40 kHz, induction melting up to 1300 C); the
first copper alloy run uses UNS C63000 bar (Cu-10Al-5Ni-3Fe). Blown-powder DED
is bought at the University of Utah (InssTek MX-Lab: InssTek DMT process,
ytterbium fiber laser of 500 W maximum, 0.4 mm beam, six powder feeders,
45-150 um powder) and at the Colorado School of Mines (FormAlloy X2).
InssTek's material database (summarized for the PI by InssTek) lists
"Al-Bronze / UNS C95300" as a qualified DED material: Cu balance, Al 9-11 wt%,
Fe 0.8-1.5 wt% (no nickel); typical powder size average about 83.8 um;
melting range 1040-1045 C; applications listed as ship propellers and marine
components; tensile strength of InssTek DMT-produced material 628 MPa (XY) and
598 MPa (Z). The database summary gives no yield strength, elongation,
hardness, heat treatment, laser power, machine model or corrosion data.
"""

OUTPUT = """\
OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition /
InssTek DMT, wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought,
weld overlay), the alloy composition in wt%, the condition (as deposited,
heat treated: temperature and time), the test conditions (e.g. 3.5 wt% NaCl
vs natural or substitute seawater per ASTM D1141, duration, flow), and the key
numbers (porosity/density, phase fractions, corrosion current density or rate,
Ecorr, selective-attack depth, hardness, UTS/yield/elongation with direction,
laser power/spot/speed/feed, powder size/flow/oxygen). Tag each item: [CITE]
worth citing; [NUMBERS] gives a quantitative benchmark; [NAVY] Navy/DoD-funded
or Navy application; [INSSTEK] made on an InssTek machine or by InssTek;
[GAP] shows something not yet done. If the literature does not answer part of
the question, say so plainly instead of padding with loosely related work.
End with a ranked "Top 5 things the PI should know" list.
"""


def q(body: str) -> str:
    return CONTEXT + "\n" + body.strip() + "\n\n" + OUTPUT


BATCHES = {}

# Batch 1: what InssTek's C95300 listing means. Laser DED of nickel-free
# aluminum bronze (properties, phases); its seawater corrosion as deposited;
# InssTek's own copper alloy work; C95300's marine use and specs; laser power
# for aluminum bronze on infrared systems; commercial aluminum bronze powders
# in DED cuts; a precedent check on the InssTek numbers; and DED repair of
# propellers. Two LITERATURE_HIGH questions (properties; corrosion).
BATCHES[1] = {
    "c1-01-ded-ni-free-al-bronze-properties": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: What does the published literature report for blown-powder laser
DED, laser metal deposition, laser cladding or InssTek DMT of NICKEL-FREE
aluminum bronzes (Cu with 8-11.5 wt% Al and 0.5-5 wt% Fe, little or no Ni):
UNS C95300, C95200, C95400, C61400, C62300, C62400, CuAl10Fe1, CuAl10Fe3,
CuAl10Fe2-C (CC331G), AWS A5.7 ERCuAl-A2 (Cu-9-11Al-0.5-1.5Fe) and ERCuAl-A3,
and thermal-spray grades such as Cu-9.5Al-1Fe?
(1) As-deposited microstructure: alpha, retained beta / martensitic
beta-prime (fractions if measured), gamma-2, kappa; how they change with
layer reheating, deposit height and Al content.
(2) Tensile properties as deposited and after heat treatment: UTS, yield and
elongation, in the build (Z) and transverse (XY) directions; hardness;
porosity. Is a UTS of 628 MPa (XY) and 598 MPa (Z) for DED C95300 consistent
with published DED, LPBF and WAAM data for Cu-10Al-1Fe, and what yield and
elongation usually go with that strength? Which phase gives it?
(3) Compare with cast C95300 (ASTM B148 minimums and typical values, as cast
and heat treated TQ50) and with cast NAB C95800.
(4) The closest wire analogs: WAAM, GMAW cladding or wire-laser DED with
ERCuAl-A2 or CuAl8/CuAl9Fe wire (e.g. Wang et al., Shen et al., Dong et al.,
and Chinese Cu-Al bronze WAAM papers), with numbers.
(5) Any paper, thesis or conference talk from InssTek Inc. or using an
InssTek DMT machine on aluminum bronze.
"""),
    },
    "c1-02-ni-free-al-bronze-seawater-as-deposited": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: How does nickel-free aluminum bronze (Cu-9-11Al-0.8-4Fe, e.g. UNS
C95300, C95400, C61400, CuAl10Fe, ERCuAl-A2 deposits) corrode in seawater or
3.5 wt% NaCl when it is laser deposited, laser clad, welded, wire-arc
deposited or otherwise rapidly solidified, compared with the same alloy cast
and heat treated, and compared with NAB (C95800, C63200) and with Cu-Ni
(C70600, C71500)?
(1) Selective phase corrosion (dealuminification) of retained beta /
beta-prime martensite and of the alpha + gamma-2 eutectoid: which phases are
attacked, how fast, how deep, in which media and durations.
(2) The basis and data behind the classic composition rules for seawater
service: nickel content at least equal to iron content in NAB; Al no more
than about 8.2 + 0.5 Ni wt% (Meigh; CDA Publications 80 and 222; Campbell);
the binary limit near 9.4 wt% Al; and why Ni-free aluminum bronzes need a
temper anneal (for example 600-700 C) for seawater service.
(3) Quantitative comparisons (corrosion current density, polarization
resistance, mass loss, selective-attack depth) between Ni-free aluminum
bronze and NAB, in any condition, with test medium and duration.
(4) What all of this predicts for an as-deposited DED C95300 deposit made
with InssTek DMT (strength 598-628 MPa, which suggests martensitic
beta-prime) used without heat treatment in seawater, and what heat treatment
would restore its corrosion resistance and at what cost in strength.
(5) Is there any published corrosion test of a laser-deposited or DED Cu-Al-Fe
(no Ni) aluminum bronze in seawater or NaCl? If not, say so.
"""),
    },
    "c1-03-insstek-dmt-copper-work": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What copper alloy work has been published by InssTek Inc.
(Daejeon, Korea) or by others using InssTek DMT machines (MX-1, MX-2, MX-3, MX-400, MX-600, MX-1000,
MX-Grande, MX-Mini, MX-Lab)? Cover aluminum bronze (including UNS C95300),
NAB, Cu-Ni, CuNi2SiCr, CuCrZr, Cu-Sn, pure Cu and Cu/steel bimetals. For
each: machine model, laser power and spot, powder supplier and size, process
parameters, density, properties. Is there any published source for the
InssTek C95300 numbers (powder size average about 83.8 um; UTS 628 MPa XY,
598 MPa Z)? Which InssTek machine and laser power did D.-S. Shim's group
(Korea Maritime and Ocean University) use for DED on cast NAB (Yao et al.
2022, J. Mater. Res. Technol. 18:5337; Yao and Shim 2022, J. Alloys Compd.
918:165776; Yao et al. 2025, Addit. Manuf. 105:104787)? Has InssTek DED of
copper alloys been approved by a classification society (Korean Register,
DNV, ABS, Lloyd's Register, Bureau Veritas) or used by a shipbuilder or navy
(Hyundai Heavy Industries, Samsung Heavy Industries, Hanwha Ocean, Republic
of Korea Navy, KRISO) for propellers, valves or other marine parts?
"""),
    },
    "c1-04-c95300-marine-use-and-specs": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Is nickel-free aluminum bronze UNS C95300 (Cu-10Al-1Fe; European
equivalents CuAl10Fe2-C / CC331G, CuAl10Fe3) used for ship propellers or for
seawater-wetted marine parts, and how does its seawater corrosion resistance
compare with NAB (C95800) and Cu-Ni (C70600, C71500)?
(1) What propeller alloys do the rules and standards name (ISO 484; the
classification society propeller material grades such as Cu1 manganese
bronze, Cu2 nickel-manganese bronze, Cu3 nickel-aluminum bronze, Cu4
manganese-aluminum bronze; US Navy MIL-B-24480 for C95800; ASTM B148 grades)?
Is a nickel-free Cu-10Al-1Fe bronze accepted for propellers anywhere?
(2) Typical uses of C95300 (bearings, bushings, gears, valve seats, pickling
hooks, marine hardware) and published guidance on its seawater service.
(3) Properties of C95300 as cast and heat treated (TQ50): minimum and typical
UTS, yield, elongation, hardness; thermal conductivity; solidus and liquidus.
(4) Seawater corrosion data comparing C95300 (or other Ni-free aluminum
bronzes) with C95800 and Cu-Ni: corrosion rate, dealuminification, erosion
and cavitation resistance.
"""),
    },
    "c1-05-ir-laser-power-al-bronze": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: What infrared laser powers, spot sizes, travel speeds and powder
feed rates have produced dense blown-powder deposits or laser clads of
aluminum bronzes (Ni-free Cu-Al-Fe such as C95300 or CuAl10Fe, and NAB such
as C95800 or C63000/C63020)? Is there any dense aluminum bronze deposit made
at or below 500 W (for example on an InssTek MX-Lab, Optomec LENS, DMG MORI
LASERTEC DED, BeAM, Trumpf, Meltio wire-laser), and how thick a substrate did
it fuse to? Give absorptivity near 1.06-1.07 um for Cu-Al alloys (solid,
powder, melt) compared with pure Cu, Cu-Ni and NAB if measured, and the
thermal conductivity of C95300 compared with C95800, C63000, C70600 and
C71500. What does this imply for depositing C95300, C63000 and C95800
powders with a 500 W, 0.4 mm infrared beam, on themselves and on thick cast
NAB plate? Include laser cladding of aluminum bronze on steel (shafts,
bearings, molds) and on copper, with powers and dilution.
"""),
    },
    "c1-06-commercial-al-bronze-ded-powders": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: Which commercial pre-alloyed aluminum bronze and NAB powders are
available in a blown-powder DED or laser cladding cut (about 45-150, 50-150
or 53-150 um), and what has been measured on them? Cover gas- or
water-atomized CuAl10Fe1, CuAl9.5Fe1 (e.g. thermal-spray grades such as
Oerlikon Metco 51F-NS), CuAl10Fe3, C95300, C95400, CuAl10Ni5Fe4 / C95800,
C63000, C63020, and Mn-Al bronze, from suppliers such as Hoganas, Sandvik
Osprey, Oerlikon Metco, Linde/Praxair, Carpenter Additive, ECKART, Makin
Metal Powders, Kymera, Avimetal, Nanoval, Shanghai or Hunan powder makers,
and InssTek's own powder supply. Report size distribution (d10/d50/d90),
sphericity, Hall flow, apparent density, oxygen and the DED papers that used
each powder. Which powder could serve as a commercial aluminum bronze or NAB
baseline lot of at least 2 kg in a DED cut, and how does a d50 near 84 um
compare with ultrasonically atomized NAB (d10/d50/d90 = 48/98/174 um at
40 kHz; Uhlmann et al., Materials 17, 3396, 2024)?
"""),
    },
    "c1-07-precedent-dmt-c95300": {
        "job": "PRECEDENT",
        "query": q("""
QUESTION: Has anyone published blown-powder laser DED (InssTek DMT or any
other system) of UNS C95300 or another nickel-free Cu-(9-11)Al-(0.8-1.5)Fe
aluminum bronze powder with tensile strengths near 600-630 MPa reported in
both the XY and Z directions? If yes, give the citation, machine, laser
power, powder, condition (as deposited or heat treated), yield, elongation and
any corrosion data. If not, what is the closest published work?
"""),
    },
    "c1-08-ded-propeller-repair-practice": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: How are marine propellers and other seawater components of NAB,
manganese bronze and aluminum bronze repaired by laser DED, laser cladding or
other additive processes, in industry and navies (Korea, Japan, China, Europe,
US Navy and NAVSEA)? Which filler or powder is used (matching NAB, Ni-free
aluminum bronze, Cu-Ni, CuNi2SiCr, other), what post-repair heat treatment
the rules require (for example the NAVSEA 675 C stress relief / temper anneal
for NAB welds, classification society rules for propeller repair), and what
corrosion or fatigue results were measured at the fusion line? Has a
Ni-free aluminum bronze filler or powder (C95300-like, ERCuAl-A2) been used
to repair NAB propellers, and with what corrosion consequences?
"""),
    },
}

# Batch 2: follow-ups on what batch 1 left open. Batch 1 found no published
# corrosion test of laser-deposited nickel-free Cu-Al-Fe, a laser-surface-
# melted near-Ni-free bronze whose beta-prime-rich layer did better in short
# NaCl tests (Guo et al. 2026), and welded NAB whose beta-prime was attacked
# selectively in seawater (Dobson 2024). c2-01 asks how fast that attack
# appears and whether short tests can see it, since the proposal's H5 says a
# one-hour screen plus microstructure predicts 30-day immersion. c2-02 asks
# whether 4-5.5 wt% Ni (the C63000 bar now being atomized) changes the
# as-deposited phases compared with nickel-free C95300 at the same Al.
BATCHES[2] = {
    "c2-01-beta-prime-attack-timescale": {
        "job": "LITERATURE_HIGH",
        "query": q("""
QUESTION: How quickly does selective phase corrosion (dealuminification) of
retained beta / martensitic beta-prime appear in aluminum bronzes and NAB in
seawater or 3.5 wt% NaCl, and can short electrochemical tests detect it?
The PI's hypothesis H5: corrosion rates, breakdown potentials and impedance
from a ONE-HOUR electrochemical screen, together with composition and
microstructure, predict which candidates pass a 30-day immersion test (mass
loss no greater than wrought 70-30 Cu-Ni; selective attack no deeper than
cast NAB). The proposal assumes the one-hour screen misses beta-prime attack,
which develops over weeks.
(1) Collect studies that measured BOTH a short electrochemical test (OCP,
LPR, EIS or polarization within about 24 h) AND longer immersion or
exposure (days to months; mass loss, selective-attack depth, cross sections)
on beta- or beta-prime-containing aluminum bronze or NAB: welds and heat-
affected zones, laser surface melted layers (e.g. Guo et al. 2026, Materials
19, 3995, where a beta-prime-rich layer did better in short NaCl tests),
laser clads, WAAM, LPBF, quenched castings. Did the short tests and the long
exposures rank the conditions the same way? Give times to first visible
selective attack and attack depth versus time where reported.
(2) Which test methods detect dealuminification quickly: potentiostatic
holds, cyclic polarization features, EIS signatures, acidified or heated
chloride, ammonia or sulfide additions, dezincification-style tests (ISO
6509 analogs) applied to aluminum bronze, scanning probes? With what
validation against long exposure?
(3) Does nickel-free aluminum bronze (Cu-9-11Al-1-4Fe, e.g. C95300, C95400,
CuAl10Fe) show selective attack of beta-prime faster or deeper than NAB with
5 Ni, for the same quench or deposit condition?
(4) What does this imply for using a deliberately beta-prime-rich deposit
(for example InssTek DMT C95300) as a known-risk control sample when testing
H5 on a small-volume well cell and in 30-day immersion?
"""),
    },
    "c2-02-nickel-and-beta-prime-retention": {
        "job": "LITERATURE",
        "query": q("""
QUESTION: In laser DED, laser cladding, LPBF, laser surface melting and
welding of aluminum bronzes, how much retained beta / martensitic
beta-prime forms as deposited, and how does it depend on Al, Ni, Fe and Mn
and on cooling rate and layer reheating? Specifically compare nickel-free
Cu-(9-11)Al-(1-4)Fe (C95300, C95400, CuAl10Fe) with NAB containing 4-5.5 wt%
Ni (C63000 Cu-10Al-5Ni-3Fe, C95800, C63200) processed the same way. Report
measured beta-prime fractions (XRD, EBSD, image analysis), martensite start
temperatures and their composition dependence, the eutectoid temperature and
composition shifts caused by Ni and Fe, critical cooling rates for retaining
beta, and how multi-layer reheating in DED tempers beta-prime into alpha +
kappa (or alpha + gamma-2 without Ni). Include laser-DED NAB results from
Southeast University (G. Sun, Z. Wang and co-workers), Muller et al. 2023
(IOP Conf. Ser. 1296, 012036; needle-like beta-prime at 1300 W), Doyle 2022
(wire-laser C95800), Murray et al. 2020 (LPBF NAB), Hyatt et al. 1998 (laser
clad NAB), and any nickel-free laser work. Is a Cu-10Al-5Ni-3Fe (C63000)
powder deposited by blown-powder DED at 300-500 W likely to be as
beta-prime-rich as nickel-free C95300?
"""),
    },
}
