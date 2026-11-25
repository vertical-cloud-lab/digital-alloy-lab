"""Questions for edison_reviewers.py: the published backgrounds of the program
officer, the YIP program manager and the Government scientists likely to
review the copper/DED version of the ONR FY2027 YIP proposal (DAL PR 117).

NOFO N0001426SF004, p. 31: "The cognizant Program Officer and other Government
scientific experts will perform the evaluation of technical proposals", with
support contractors possible as subject-matter consultants. The CONTEXT block
is the one DAL's edison-trajectories/cu-ded-2026-10/queries.py uses, so the
answers line up with that batch."""

CONTEXT = """\
CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal for the Materials &
Processes for Additive Manufacturing program (ONR Code 332). The work designs
new pre-alloyed copper alloy powders for single-stream blown-powder laser
directed energy deposition (DED). Goals: deposits that are dense and
crack-free, both built on themselves and deposited on cast nickel-aluminum
bronze (NAB) and wrought Cu-Ni (repair), and that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe, Mn, Cr; aluminum
bronzes / NAB with Ni, Fe, Mn. Lower nickel content is a secondary objective.
Powder is made in-house by ultrasonic atomization. Method: composition ->
powder -> DED deposit -> microstructure -> corrosion/hardness is a network of
linked models searched by cost-aware Bayesian optimization (cheap steps such
as CALPHAD, pre-placed powder tracks and one-hour electrochemical screens are
run more often than expensive ones such as 2 kg blown-powder builds and
30-day immersion). CALPHAD is evaluated along a heat-flow model of the DED
thermal history. Purchased DED sessions run at outside facilities.
"""

OUTPUT = """\
OUTPUT FORMAT: First, a short profile built only from the published record
(papers, technical reports, conference talks, program pages): positions and
affiliations with years, main research topics, methods, and recurring
co-authors. Then the publications most relevant to the proposal, each with a
full citation and DOI and one line on what it found. Then 3-6 numbered
IMPLICATIONS for the proposal: what this reader is likely to value, what they
would probe or doubt, which of their own results the proposal should cite or
build on, and wording or framing that would land well or badly with them.
Tag claims that rest on a single source or on a program web page rather than
a peer-reviewed paper. If the record is thin or a name is ambiguous (several
people share it), say so plainly instead of guessing, and do not invent
affiliations, titles or papers.
"""


def q(body: str) -> str:
    return CONTEXT + "\n" + body.strip() + "\n\n" + OUTPUT


BATCHES = {
    1: {
        "r1-01-fisher-program-officer": {
            "job": "LITERATURE_HIGH",
            "query": q("""
QUESTION: Summarize the published research of Dr. Charles R. Fisher, now
the ONR Code 332 program officer for Materials & Processes for Additive
Manufacturing, whose papers list the Naval Surface Warfare Center Carderock
Division (NSWCCD). Cover his work on welding and additive manufacturing of
copper alloys (nickel-aluminum bronze, 70-30 and 90-10 Cu-Ni), wire-arc DED,
laser powder bed fusion, heat treatment, residual stress and distortion,
temperature-dependent material property databases for ICME (for example with
J. E. Norkett in Integrating Materials and Manufacturing Innovation, 2025-2026,
and with S. M. Orzolek and J. K. Semple on NAB processing in Additive
Manufacturing, 2022), and any work on steels, titanium or qualification of
printed parts. What open problems and next steps do his papers state? Where
would a reader with this background agree with, and push back on, a proposal
to design new copper alloys for as-deposited use by blown-powder laser DED
(kappa-phase control in NAB, the post-build anneal the cast and wire-arc
alloys need, specification compliance such as MIL-PRF-32804, -32815 and
-32816, and whether new compositions are a realistic route to Navy use)?
"""),
        },
        "r1-02-carderock-copper-am": {
            "job": "LITERATURE",
            "query": q("""
QUESTION: Who at NSWC Carderock Division (and NSWC Philadelphia) has
published on additive manufacturing, welding, heat treatment or seawater
corrosion of copper alloys (NAB, Cu-Ni, manganese-aluminum bronze) since
2015? Include S. M. Orzolek, J. K. Semple, J. E. Norkett, J. H. Canaday and
others the literature turns up. For each, give the papers and what they
measured. What questions do these papers leave open, and which of them does
a cost-aware search for as-deposited DED copper alloys answer? Which of
their datasets or property databases could the proposal use as inputs or
benchmarks? What would this group count as convincing evidence that a new
composition deserves Navy qualification testing?
"""),
        },
        "r1-03-shifler-corrosion": {
            "job": "LITERATURE",
            "query": q("""
QUESTION: Summarize the published work and stated research priorities of Dr.
David A. Shifler, ONR Code 332 program officer for Corrosion Science and
Corrosion Control Technologies, and any earlier Navy laboratory positions
the record shows. Cover marine
corrosion, copper alloys in seawater, high-temperature corrosion, coatings,
corrosion of additively manufactured alloys, and his views on accelerated
tests and life prediction. A reviewer with this background will read the
proposal's corrosion plan: polarization, linear polarization resistance and
impedance in ASTM D1141 substitute ocean water as a one-hour screen, then
30-day immersion with mass loss and depth of selective phase attack, with
flowing seawater left to Navy labs, plus an audit that tests a random share
of the candidates the screen rejects. What would he want added, and which of
his papers should the plan cite?
"""),
        },
        "r1-04-varanasi-camd": {
            "job": "LITERATURE",
            "query": q("""
QUESTION: Summarize the published research and career of Dr. Chakrapani V.
(Pani) Varanasi, listed by ONR as a Code 332 program officer for
Computer-Aided Materials Design (CAMD) and Structural Metals. What did he
work on before ONR (for example at the Air Force Research Laboratory, the
University of Dayton Research Institute or the Army Research Office), and
what kinds of computational materials design, ICME, high-throughput
screening and materials informatics work has CAMD funded? How should a
proposal that couples CALPHAD along a DED heat-flow model with cost-aware
Bayesian optimization describe its computational advance to this reader, and
what would he probe (uncertainty quantification, validation against
experiment, transfer to other alloy systems)?
"""),
        },
        "r1-05-wolk-manufacturing": {
            "job": "LITERATURE",
            "query": q("""
QUESTION: Summarize the published work and stated priorities of Dr. Jennifer
N. Wolk, listed by ONR as the Manufacturing focus area lead, and any
earlier Navy laboratory roles the record shows. Cover additive manufacturing
qualification and certification for the Navy, rapid qualification
frameworks, ICME and digital-thread approaches, fatigue and properties of
printed metals, and any statements on copper alloys, repair, or replacing
castings with printed parts. What would she look for in a YIP proposal on
alloy design for blown-powder DED, and what claims about qualification
should the proposal avoid or state carefully?
"""),
        },
        "r1-06-yip-program-and-pm": {
            "job": "LITERATURE",
            "query": q("""
QUESTION: The ONR Young Investigator Program is managed by Dr. Reginald G.
Williams (ONR Code 34). What is his published research background? Then,
from papers that acknowledge ONR Young Investigator Program grants, which
YIP-funded projects since 2015 dealt with additive manufacturing of metals,
alloy design, welding, or corrosion, and what did they emphasize
(fundamental mechanisms, Navy transition, new capabilities)? What does that
record suggest about how a materials YIP proposal should balance basic
science against Navy application?
"""),
        },
        "r1-07-navy-lab-am-corrosion-experts": {
            "job": "LITERATURE",
            "query": q("""
QUESTION: Besides ONR program officers, the NOFO says "other Government
scientific experts" evaluate proposals. Which researchers at the Naval
Research Laboratory (for example the Materials Science and Technology
Division and the Center for Corrosion Science and Engineering, including NRL
Key West), NAVAIR, the Naval Postgraduate School and Navy-affiliated
laboratories such as Penn State ARL have published since 2015 on directed
energy deposition or laser cladding of metals, repair of naval components,
copper alloys in seawater, or corrosion of printed alloys? For each, list
the papers and the expertise a reviewer would bring, and what each would be
most likely to question in this proposal.
"""),
        },
        "r1-08-navy-ml-autonomous-materials": {
            "job": "LITERATURE",
            "query": q("""
QUESTION: Which Navy and ONR-funded researchers have published on machine
learning, Bayesian optimization, active learning, autonomous or
high-throughput experimentation for alloy design, additive manufacturing
process development, or corrosion prediction since 2018 (including NRL,
NSWC and ONR-funded university groups)? A reviewer from this group will
judge the method: cost-aware Bayesian optimization of a network of linked
models with steps of different costs and durations. What have these groups
already shown, what would they consider new, and what benchmarks or
baselines would they expect the proposal to report?
"""),
        },
    },
}
