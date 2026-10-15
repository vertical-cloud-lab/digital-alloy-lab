# FLAIME funding-trends synthesis (NSF · DOE · DOD/DOW · NASA, 2020-2026)

*Synthesis of 24 Edison Scientific 1-credit `LITERATURE` (paperqa3) queries — one query per
(topic × agency) cell — that mined the *Acknowledgements / Funding* sections of recent
materials, alloy, additive-manufacturing, and AI-for-materials papers (2020-2026). Per-cell
results, including funded-project tables with PIs, award numbers, and program names, are in
`edison-trajectories/funding-trends/{topic}__{agency}.md`. Submitted 2026-05-05.*

---

## Why this exists

The Genesis Mission Phase I FLAIME proposal targets **autonomous, closed-loop alloy
discovery**. To position FLAIME accurately in the federal funding landscape — and to identify
both **competitor PIs** and **white-space opportunities** — we asked Edison to mine the
literature for what is *actually being funded* in our six core topic areas across four federal
funding sources (NSF, DOE, DOD/DOW, NASA). The output is a 6 × 4 matrix of funded-project
tables grounded in paper acknowledgements (2020-2026).

The matrix surfaces three things the existing `edison-trajectories/funded_programs.md`
(2026-04 LITERATURE_HIGH single-shot survey) did not: **per-agency depth**, **per-topic
program signatures**, and **gap detection** at the (topic, agency) cell level.

## Method and scope (one paragraph)

24 Edison `LITERATURE` queries (1 credit each — `JobNames.LITERATURE` /
`job-futurehouse-paperqa3`, the 1-credit base literature crow; **not** the costlier
`LITERATURE_HIGH` / `job-futurehouse-paperqa3-high` variant). Each query asked Edison to
extract one row per acknowledged award,
then a "Trends" subsection identifying growing/shrinking sub-programs, dominant
PIs/institutions, post-2022 programs, and visible funding gaps. **All 24 queries returned
non-empty answers**; per-cell evidence density ranges from **7-9 funded entries (NASA cells)**
to **22-26 funded entries (NSF cells)**, reflecting agency-level publication norms more than
true funding intensity. Acknowledgement text systematically under-reports award amounts and
periods of performance, so all dollar/duration claims here are exactly as stated in the cells
and should be cross-checked against NSF Award Search, USAspending.gov, and DOE OSTI for the
final proposal.

---

## Big-picture funding trends

### 1. ARPA-E ULTIMATE is the single most visible federal program in our space

`DE-AR0001427` (ULTIMATE) appears across **at least four** topic cells —
[`bayesian-optimization__DOE`](funding-trends/bayesian-optimization__DOE.md),
[`self-driving-labs__DOE`](funding-trends/self-driving-labs__DOE.md),
[`lpbf-additive-manufacturing__DOE`](funding-trends/lpbf-additive-manufacturing__DOE.md),
[`calphad-icme-high-throughput__DOE`](funding-trends/calphad-icme-high-throughput__DOE.md) —
and the BIRDSHOT subproject (Arroyave/Karaman, TAMU) is the closest existing analogue to
FLAIME in the federal portfolio. The 2026 follow-on **ARPA-E CHADWICK (`DE-AR0001988`)**
appears in alloy-optimization papers in the SDL-DOE cell, signalling **continued ARPA-E
investment in AI-enabled alloy development workflows post-ULTIMATE**.
*Implication for FLAIME:* explicitly position FLAIME as a **DOE Office of Science /
Genesis-Mission complement** to ARPA-E's applied scale-up portfolio; cite ULTIMATE/BIRDSHOT
and CHADWICK as evidence that the loop is feasible while emphasizing what FLAIME adds (e.g.,
LPBF-native loop, Al-system focus, partnership-led scale-up).

### 2. NSF DMREF + CMMI + post-2022 TIP/POSE form NSF's "autonomy stack"

NSF's footprint across all six topic cells is consistent: **DMREF** funds the data/ML +
materials co-design layer ([NSF cells for ML, BO, CALPHAD, Al-alloys, SDL]), **CMMI** funds
the manufacturing/sensing/control layer (especially in
[`lpbf-additive-manufacturing__NSF`](funding-trends/lpbf-additive-manufacturing__NSF.md) and
[`calphad-icme-high-throughput__NSF`](funding-trends/calphad-icme-high-throughput__NSF.md)),
and **DMR / MRSEC / NNCI / OAC** fund the underlying instrumentation and compute. **Post-2022
emergence of TIP/POSE** (`TIP-2229018`, Pozzo, UW) and **DMR PREM** (`DMR-2424949`) in
[`self-driving-labs__NSF`](funding-trends/self-driving-labs__NSF.md) signals NSF moving from
single-lab science toward **community/platform/translation funding for SDL infrastructure** —
relevant for FLAIME's planned scale-up narrative even though FLAIME is a DOE proposal.

### 3. DOD funding clusters around "autonomy-enabling capability" rather than "alloy SDL"

Across the four DOD cells:
- **AFOSR** dominates SDL/BO/autonomy methodology
  ([`self-driving-labs__DOD`](funding-trends/self-driving-labs__DOD.md);
  [`bayesian-optimization__DOD`](funding-trends/bayesian-optimization__DOD.md)),
  including a recent FY23 award `FA9550-23-1-0466`.
- **AFOSR MURI** is the largest visible DOD vehicle in
  [`calphad-icme-high-throughput__DOD`](funding-trends/calphad-icme-high-throughput__DOD.md)
  and [`ml-materials-informatics__DOD`](funding-trends/ml-materials-informatics__DOD.md),
  funding HT phase mapping, autonomous synthesis, and ML-enabled inverse design.
- **ARO/ARL** dominates physics-informed BO for alloys (the cooperative agreement
  `W911NF-22-2-0106` HTMDEC; Khatamsaz/Arroyave/Karaman, TAMU; `bayesian-optimization__DOD`)
  and recently issued an **ARO MURI (FY25)** explicitly for **LPBF superalloy
  solidification** ([`lpbf-additive-manufacturing__DOD`](funding-trends/lpbf-additive-manufacturing__DOD.md)).
- **ONR** dominates LPBF in-situ monitoring/qualification (NAVAIR/NSWC partners).
- **DARPA Make-It / AMD / Accelerated Molecular Discovery** appears in older SDL/BO papers but
  is **not visible in 2024+ alloy LPBF acknowledgements**, suggesting either pivoted DARPA
  priorities or under-citation.

The DOD posture is **"autonomy as a capability,"** not **"closed-loop alloy SDL as a
program."** That is exactly the gap FLAIME could highlight as differentiated from DOE Genesis.

### 4. DOE EERE + national-lab LDRD is the Al-alloy + LPBF stack

[`aluminum-alloys__DOE`](funding-trends/aluminum-alloys__DOE.md) and
[`lpbf-additive-manufacturing__DOE`](funding-trends/lpbf-additive-manufacturing__DOE.md) point
to a coherent **DOE EERE → ORNL MDF → AMMTO/VTO → CMI** pipeline:
- **EERE/AMO + VTO** fund the demonstrator hardware (e.g., DuAlumin-3D pistons, GM/ORNL
  `DE-EE0008877`).
- **Critical Materials Institute (CMI)** is the recurring backbone for **Al-Ce alloy
  CALPHAD/thermodynamics** (LLNL `DE-AC52-07NA27344`; ORNL `DE-AC05-00OR22725`).
- **Sandia Grand Challenge LDRD + ORNL LDRD AI Initiative** carry the AI-enabled
  qualification/closed-loop-control work.
- **ARPA-E ULTIMATE BIRDSHOT** got a stated **$9.5M follow-on**, and an ODS-steel program
  reported smaller INFUSE/BES/DOE-NE follow-ons
  ([`lpbf-additive-manufacturing__DOE`](funding-trends/lpbf-additive-manufacturing__DOE.md)).

This pipeline is the most credible "competition" for FLAIME's outcome story; FLAIME should
**name and cite it explicitly** rather than ignoring it.

### 5. NASA is funding *enabling pieces* but **not** end-to-end alloy SDLs — clear opportunity

All four NASA cells converge on the same finding: NASA funds AM qualification (STMD/RAMPT,
ORCA, TTT), Al-alloy demonstrator metallurgy (Marshall/Glenn for HR-series, GRX-810,
Al-6061-RAM2), ML for AM tools (T3 portfolio, ~$3.5M/yr NRA, 43% AI/ML proposals), and
EPSCoR/ULI/SBIR pathways — but **no NASA award in our 24-cell sample explicitly funds a
closed-loop alloy SDL**. ([`self-driving-labs__NASA`](funding-trends/self-driving-labs__NASA.md),
[`lpbf-additive-manufacturing__NASA`](funding-trends/lpbf-additive-manufacturing__NASA.md),
[`aluminum-alloys__NASA`](funding-trends/aluminum-alloys__NASA.md),
[`ml-materials-informatics__NASA`](funding-trends/ml-materials-informatics__NASA.md)). This is
a near-term **proposal target** post-FLAIME (NASA STMD ECF, ESI, or STRI).

### 6. Dominant PI clusters across the matrix

| Cluster | Topics where they appear | Primary agency footprint |
|---|---|---|
| **Arroyave / Karaman / Allaire / Srivastava (TAMU)** | BO, CALPHAD/ICME, ML, SDL | DOE ARPA-E ULTIMATE; ARO/ARL HTMDEC (`W911NF-22-2-0106`); NSF DMREF |
| **Abolhasani (NCSU) + Pozzo (UW) + Schrier (Fordham)** | Self-driving labs | NSF (multiple `190xxxx`/`220xxxx`/`231xxxx` awards; TIP-POSE; PHY/OAC) |
| **Buehler (MIT) + Ramprasad (GT)** | ML for materials informatics | ONR + ARO + AFOSR MURI |
| **Xinghang Zhang (Purdue), Atieh Moridi (Cornell), Wei Xiong (Pitt), Prahalada Rao (VT), Hui Yang (PSU)** | Al-alloys, LPBF, CALPHAD | NSF CAREER (`CMMI-2046523`, `CMMI-2047218`, `CMMI-2309483`) + NSF MMN (`DMR-2210152`) + DOE Early Career (`DE-SC0022860`) |
| **ORNL MDF — Plotkowski / Sisco / Babu / Dehoff / Nandwana** | Al-Ce-Mg AM, LPBF, qualification | DOE EERE/AMMTO + VTO; ORNL contract `DE-AC05-00OR22725` |
| **LLNL/Ames — Moore, McCall, Rios, Weiss, Sims; Perron** | Al-Ce design, CALPHAD | DOE CMI / EERE-AMO; LLNL contract `DE-AC52-07NA27344` |
| **MIT — LeBeau / Xu / Schuh-adjacent** | AM Al-alloys, characterization | NSF `CMMI-1922206`, MIT.nano shared facility |

These clusters are **the active competition for FLAIME** *and* the most credible coalition
candidates. Several (Arroyave, Plotkowski, Pozzo, Abolhasani) are obvious targets for
solicited reviewer-friendly citations or letters of collaboration in the proposal narrative.

### 7. Visible **gaps / white space** by (topic × agency)

The cells repeatedly call out where federal funding is **conspicuously absent or thin**, even
though the topic is technically in scope. The combinations below are the strongest
**positioning levers** for FLAIME — places where FLAIME's narrative can credibly claim "no one
is funding this yet":

| Gap | Cell evidence | Why it matters for FLAIME |
|---|---|---|
| **NSF: explicitly alloy-centric closed-loop SDL** (most NSF SDL awards are perovskite/thin-film/nanoparticle/microscopy) | [`self-driving-labs__NSF`](funding-trends/self-driving-labs__NSF.md), [`calphad-icme-high-throughput__NSF`](funding-trends/calphad-icme-high-throughput__NSF.md) | FLAIME's Al + LPBF + autonomy combination is **not duplicated** in NSF's portfolio |
| **DOE: end-to-end LPBF SDL with explicit AMMTO / FECM / NETL framing** (DOE LPBF acknowledgements skew ARPA-E + ORNL LDRD; AMMTO is sparse for SDL) | [`self-driving-labs__DOE`](funding-trends/self-driving-labs__DOE.md), [`lpbf-additive-manufacturing__DOE`](funding-trends/lpbf-additive-manufacturing__DOE.md) | Genesis-Mission framing fills exactly this gap |
| **DOD: closed-loop alloy SDL by name** (DOD funds capability building blocks, not "alloy SDL" as a program label) | [`self-driving-labs__DOD`](funding-trends/self-driving-labs__DOD.md), [`bayesian-optimization__DOD`](funding-trends/bayesian-optimization__DOD.md) | Differentiation from DOD-funded autonomy work; opportunity for follow-on DOW MURI |
| **NASA: closed-loop alloy SDL of any kind** | all four NASA cells | Phase-II / post-FLAIME proposal target (STMD ECF/ESI, STRI) |
| **Bayesian optimization for alloy design from NSF: amounts and PIs are systematically not reported in acknowledgements** | [`bayesian-optimization__NSF`](funding-trends/bayesian-optimization__NSF.md) | FLAIME should explicitly include award numbers + amounts in its publications |
| **Al-Cu / Al-Ce / high-strength AM Al under DOD** is thin (mostly ONR + DEVCOM ARL on Al-AM mechanics) | [`aluminum-alloys__DOD`](funding-trends/aluminum-alloys__DOD.md) | Reinforces FLAIME's "DOE-led, defense-relevant" framing |

### 8. Post-2022 program signals worth tracking

| Agency | Post-2022 program (visible in cells) | Cell |
|---|---|---|
| NSF | **TIP/POSE** for SDL community infrastructure | [self-driving-labs__NSF](funding-trends/self-driving-labs__NSF.md) |
| NSF | **DMR PREM** as partnership/diversity vehicle for SDL | [self-driving-labs__NSF](funding-trends/self-driving-labs__NSF.md) |
| NSF | **PFI-TT** translation awards in LPBF (Rao, VT, `PFI-TT 2322322`) | [lpbf-additive-manufacturing__NSF](funding-trends/lpbf-additive-manufacturing__NSF.md) |
| NSF | **OAC MRI / CC* Compute** as autonomy enablers | [bayesian-optimization__NSF](funding-trends/bayesian-optimization__NSF.md), [ml-materials-informatics__NSF](funding-trends/ml-materials-informatics__NSF.md) |
| DOE | **ARPA-E CHADWICK (`DE-AR0001988`, 2026)** as ULTIMATE successor for AI-enabled alloy design | [self-driving-labs__DOE](funding-trends/self-driving-labs__DOE.md) |
| DOE | **BES Data Science Initiative (`DE-SC0020381`)** for BO-for-alloys | [bayesian-optimization__DOE](funding-trends/bayesian-optimization__DOE.md) |
| DOE | **EERE/AMO `DE-EE0010214`** (CALPHAD+BO alloy/coatings) | [bayesian-optimization__DOE](funding-trends/bayesian-optimization__DOE.md) |
| DOD | **ARO MURI (FY25, LPBF superalloy solidification)** | [lpbf-additive-manufacturing__DOD](funding-trends/lpbf-additive-manufacturing__DOD.md) |
| DOD | **AFOSR FY23 awards (`FA9550-23-1-0466`)** for autonomous experimentation | [self-driving-labs__DOD](funding-trends/self-driving-labs__DOD.md) |
| NASA | **STMD STRI for AM certification (~$3M/yr × 5)** | [ml-materials-informatics__NASA](funding-trends/ml-materials-informatics__NASA.md) |
| NASA | **EPSCoR `80NSSC19M0149` for ICME solidification** | [calphad-icme-high-throughput__NASA](funding-trends/calphad-icme-high-throughput__NASA.md) |

---

## Implications for the FLAIME proposal narrative

1. **Cite ULTIMATE/BIRDSHOT and CHADWICK by name.** They are the obvious comparator. Frame
   FLAIME as **complementary** (Office-of-Science-aligned, partnership-led, Al/LPBF-specific)
   rather than redundant.
2. **Name the ORNL MDF + CMI + LLNL/Ames Al-Ce pipeline** in the related-work section. Not
   citing it would be a credibility gap; citing it is also an opportunity to position FLAIME
   as the *autonomy/closed-loop layer* on top of an existing alloy-design ecosystem.
3. **Reference the HTMDEC ARL cooperative agreement** (`W911NF-22-2-0106`) when discussing
   high-throughput infrastructure — it's the dominant DOD-funded analogue for autonomous
   alloy discovery, and acknowledging it shows literature awareness.
4. **Acknowledge the NSF post-2022 TIP/POSE/PREM trajectory** when discussing the
   democratization / community-building / Phase-II scale-up vision. Genesis is DOE, but the
   community infrastructure norms are being set at NSF.
5. **Highlight the four explicit gap cells** (NSF alloy-SDL, DOE EERE-framed LPBF SDL, DOD
   alloy-SDL by name, NASA SDL of any kind) as the white-space that FLAIME plus a 2-3 year
   follow-on roadmap is positioned to occupy.
6. **Bake award-number reporting into the FLAIME publication policy.** The NSF and NASA cells
   repeatedly flag that paper acknowledgements drop award numbers and amounts — making the
   field opaque to exactly the kind of trend analysis we just ran. FLAIME should commit to
   full award-ID disclosure in publications, which is also useful for our own reporting.

---

## Caveats

- **Literature-derived only.** Acknowledgements undercount real funding. Cross-check named
  awards against NSF Award Search (https://nsf.gov/awardsearch/), USAspending.gov, DOE OSTI,
  DOD's Defense Innovation Marketplace, and NASA NSPIRES before quoting any specific
  statistic in the proposal.
- **paperqa3 corpus bias.** The 1-credit `LITERATURE` job uses a fixed, mostly open-access
  corpus; closed-access journals (e.g., some Acta Materialia, Materials Science and
  Engineering A papers) and DOE OSTI gray literature may be partially missed.
- **Self-reported program names.** Some "trend" claims hinge on whether authors cited a
  program by name — e.g., "DMREF" vs. an opaque `1922xxx` award number — and absence in
  acknowledgements is *not* evidence of absence in the portfolio.
- **Per-cell coverage varies by ~3× between NSF and NASA cells.** This reflects publication
  norms, not real funding intensity.
- **PR #58 was not merged into this branch.** Its content was scanned via existing repo
  context (the merged base `b41c0c5` already includes most material referenced in the issue);
  the focus of this work is the Edison literature survey requested in the issue rather than
  a code merge.

## Files

- [`funding-trends/README.md`](funding-trends/README.md) — task-ID manifest (24 cells)
- [`funding-trends/{topic}__{agency}.md`](funding-trends/) — per-cell evidence tables
  (executive summary + funded-projects table + trends + caveats), one file per cell
