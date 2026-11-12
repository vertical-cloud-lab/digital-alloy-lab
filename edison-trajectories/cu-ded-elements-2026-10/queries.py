"""Edison questions for the copper/DED element search space (PR #117).

Phase 1: one LITERATURE question per element (50, see elements.py), plus one
LITERATURE_HIGH question on the joint bounds of a candidate short list.
Phase 2 and 3 (ANALYSIS, with the phase-1 answers uploaded) are written after
phase 1 returns; see analysis_prompts.py.

The template follows ../cu-ded-2026-10/queries.py (context block, PI's own
papers excluded, citations with DOIs, tags, "say so when nothing is found")
and the per-element questions of the aluminum run (conservative and
non-conservative bound, failure modes, interactions). It adds an inclusion
decision, because here the palette itself is being chosen, and a one-line
VERDICT for tabulation. No date window: a window hid older prior art in the
previous copper run.
"""

from elements import ELEMENTS

CONTEXT = """\
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
"""

OUTPUT = """\
OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.
"""


def verdict_line(el: str) -> str:
    return (
        f"End with exactly one line in this format, filled in:\n"
        f"VERDICT | {el} | decision=<INCLUDE or LIMIT or EXCLUDE> | "
        f"family=<Cu-Ni or Al-bronze or both or none> | "
        f"conservative_max_wt=<number or NA> | "
        f"nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | "
        f"impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>"
    )


def element_prompt(el: str) -> str:
    group, hint = ELEMENTS[el]
    if el == "Cu":
        task = f"""\
ELEMENT UNDER REVIEW: Cu (the matrix). {hint}

Answer for copper as the balance element:
1. LOWER BOUND Cu_min: give a CONSERVATIVE Cu_min (stays within established
   seawater copper alloys) and a NON-CONSERVATIVE Cu_min (defensible but more
   aggressive), in wt%, with reasons: the alpha (fcc) phase field and the
   onset of beta or other second phases, the atomizer limit (liquidus about
   1,200-1,250 C), the validity range of copper CALPHAD databases (TCCU is
   built for copper-rich alloys), and what still counts as a copper alloy
   (UNS C designations).
2. Is there a practical UPPER bound on Cu (a minimum total solute needed for
   seawater resistance or strength), e.g. compared with unalloyed copper in
   seawater?
3. How should the matrix bound interact with the two families (70-30 Cu-Ni at
   about 65-70 wt% Cu versus NAB at about 78-82 wt% Cu): one continuous space
   or two sub-spaces? What is the total solute budget for each?
4. Effects of the copper source (oxygen-free vs tough-pitch, recycled scrap)
   on the powder and deposit.
5. Failure modes that set each bound, and EVIDENCE QUALITY.

{verdict_line('Cu').replace('conservative_max_wt', 'conservative_min_wt').replace('nonconservative_max_wt', 'nonconservative_min_wt')}"""
    else:
        task = f"""\
ELEMENT UNDER REVIEW: {el} ({group}). {hint}

Answer for {el} specifically, not for copper alloys in general:
1. ROLE: what {el} does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their {el} ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how {el} changes corrosion of
   copper alloys in natural or substitute seawater or 3.5 wt% NaCl (corrosion
   rate, Ecorr, film resistance, pitting, crevice, dealloying, erosion-
   corrosion and velocity limits). Give the range where it helps and where it
   harms.
3. DED AND WELDING: effect on solidification cracking, liquation cracking in
   reheated layers, porosity, evaporation or oxidation loss under a laser,
   and on dilution into cast NAB or wrought Cu-Ni repair substrates. Use
   welding and cladding literature (ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl
   fillers) where AM data are missing, and say so.
4. POWDER MAKING: problems in induction melting and atomization (oxidation,
   reaction with alumina, zirconia or graphite crucibles or with a titanium-
   alloy or molybdenum sonotrode, vapor loss, effect on liquidus and surface
   tension).
5. PHASE DIAGRAM AND CALPHAD: maximum solid solubility in Cu (wt%, and the
   temperature), intermetallics and invariant reactions in Cu-{el}, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-{el}, Cu-Ni-{el} and Cu-Al-{el} are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of {el} in the alloy (Cu balance):
   a. DECISION: INCLUDE as a designed addition, LIMIT as an impurity only, or
      EXCLUDE, with a one-paragraph reason.
   b. If INCLUDE: a CONSERVATIVE upper bound (from established commercial or
      Navy alloys, or demonstrated AM or cladding), a NON-CONSERVATIVE upper
      bound (defensible but aggressive: experimental alloys, solubility or
      phase-boundary limits, the liquidus limit), and a FUNCTIONAL FLOOR (the
      smallest content with a measurable effect). Say which family (Cu-Ni,
      aluminum bronze, or both) each bound applies to.
   c. If LIMIT: the maximum tolerable content (wt% or ppm) in DED powder and
      deposit, and the specification or study it comes from.
   d. The failure mode that sets each bound.
8. INTERACTIONS for a later joint-constraint analysis: sums or ratios with Ni,
   Fe, Mn, Al or other elements; elements that {el} neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

{verdict_line(el)}"""
    return CONTEXT + "\n" + task + "\n\n" + OUTPUT


SHORTLIST = ["Ni", "Al", "Fe", "Mn", "Cr", "Sn", "Zn", "Si", "Nb", "Ti", "Zr",
             "Co", "Mg", "B", "P", "Ce", "La", "Y", "Be", "Ag"]

JOINT_PROMPT = CONTEXT + f"""
TASK: JOINT BOUNDS AND PALETTE. Separate per-element questions are running for
50 elements. This question looks at them together. Candidate short list
(Cu as balance): {", ".join(SHORTLIST)}; impurities C, S, P, Pb, Bi, O, H, N.

1. Which 8-15 of the short-listed elements should form the search palette for
   the stated goal (as-deposited seawater resistance at least equal to C71500,
   crack-free blown-powder DED on itself and on cast NAB and wrought Cu-Ni,
   lower nickel), and which should be dropped or kept as impurity limits?
   Rank them and give the reason for each.
2. One consolidated markdown table for the chosen palette plus Cu: lower
   bound, conservative upper bound, non-conservative upper bound (wt%), the
   failure mode setting the upper bound, and key citations. Give Cu_min.
3. Joint constraints tighter than the per-element bounds, with numbers and
   sources, for example: the aluminum equivalent for retained beta or
   martensite in aluminum bronzes (Al + factors x Mn, Si, Sn, Zn, Ni, Fe), the
   Fe/Ni ratio and kappa phase control in NAB, Fe and Mn together in Cu-Ni
   (Fe in solid solution), Cr with Fe and Si in Cr-modified Cu-Ni, the zinc
   equivalent in brasses, total solute versus liquidus (the alloy liquidus must
   stay below about 1,250 C, which caps Ni near 30 wt% in Cu-Ni), and impurity
   sums (Pb + S + P + C) for weldability.
4. Should the space be one continuous Cu-Ni-Al-Fe-Mn-... simplex or two
   sub-spaces (Cu-Ni branch, aluminum bronze branch)? What lies between them
   (e.g. Cu-Ni-Al alloys such as MARINEL or cast Cu-7Ni-3Al), and is that
   region worth searching?
5. Which pairs and ternaries in the palette are assessed in Thermo-Calc TCCU
   (or published CALPHAD work) and which rely on extrapolation only?

Express every composition in wt%. Cite peer-reviewed work, standards and
handbooks with DOIs where available. Say plainly where evidence is thin.
"""


def phase1() -> dict:
    jobs = {f"el-{i:02d}-{el}": {"job": "LITERATURE", "query": element_prompt(el),
                                 "element": el}
            for i, el in enumerate(ELEMENTS, start=1)}
    jobs["joint-shortlist"] = {"job": "LITERATURE_HIGH", "query": JOINT_PROMPT,
                               "element": None}
    return jobs


PHASES = {1: phase1()}


# Phase 4: the electrochemical side (Sterling, 2026-10-17: "look into use of
# our CubXL for this project ... on the electrochemical side, noting that we
# have access to a potentiostat, but not sure if that's necessary"). Written
# from a survey of the byu-vcl CubXL threads (#133, #231, #213, PR #278): the
# CubXL is a GRBL gantry liquid handler (Opentrons P20 pipette, vial capper,
# cameras, no tool changer) driven by CubOS on a Raspberry Pi, whose
# potentiostat drivers (Admiral Squidstat, PalmSens EmStat) cover OCP, CV, CA
# and CP but not yet EIS; the lab owns no potentiostat and can borrow one.
ECHEM_CONTEXT = CONTEXT + """
LAB CONTEXT: the lab has a small open-frame gantry liquid handler (about
390 x 230 x 120 mm working volume; one head carrying a 20 uL pipette, a vial
capper and cameras; no tool changer; Python/YAML control software that drives
PalmSens EmStat and Admiral Squidstat potentiostats for OCP, CV,
chronoamperometry and chronopotentiometry, not yet EIS). It owns no
potentiostat and can borrow a conventional benchtop one. Specimens are small:
polished faces of DED single tracks, thin walls and blocks (a few mm to 20 mm
across), and cross-sections of repair coupons that cross the fusion line into
cast NAB or wrought Cu-Ni.
"""

PHASES[4] = {
    "ec-01-droplet-cell-screen": {
        "job": "LITERATURE",
        "query": ECHEM_CONTEXT + """
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
""" + "\n" + OUTPUT,
    },
    "ec-02-potentiostat-free": {
        "job": "LITERATURE",
        "query": ECHEM_CONTEXT + """
QUESTION: For ranking copper alloys (Cu-Ni, aluminum bronze, NAB) by seawater
corrosion, what can be measured WITHOUT a full potentiostat, and how well does
it agree with LPR, EIS and long immersion? Cover: (1) open-circuit potential
time series with a high-impedance voltmeter during immersion (film formation
and ennoblement of Cu-Ni over days); (2) metal release: copper and nickel
dissolved into the immersion solution, sampled in small aliquots over time
and measured by ICP-MS/OES or colorimetry (e.g. bathocuproine or
bicinchoninic acid for copper, dimethylglyoxime for nickel), including
published copper release rates of 90-10 and 70-30 Cu-Ni in seawater; (3)
mass loss of small coupons (ASTM G31/G1) and its detection limit for alloys
corroding at about 0.01-0.05 mm/yr; (4) image-based measures (corrosion
product color, area fraction attacked) and dealloying depth; (5) galvanic
coupling of a deposit to cast NAB or wrought Cu-Ni with a zero-resistance
ammeter, relevant to repairs; (6) low-cost open-source or module
potentiostats (Rodeostat, MYSTAT, EmStat Pico, ABE-Stat, KickStat or similar)
validated against commercial instruments for corrosion LPR or EIS. Which of
these could replace or supplement a one-hour electrochemical screen as a
cheap node in a cost-aware search, and which cannot? Give DOIs and numbers.
""" + "\n" + OUTPUT,
    },
}
