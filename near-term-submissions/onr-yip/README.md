# ONR FY2027 Young Investigator Program (YIP): submission package draft

NOFO **N0001426SF004**. Full proposal due **Fri Oct 30, 2026, 5:00 PM ET**
(3:00 PM in Provo) on Grants.gov. Questions due **Fri Oct 16, 5:00 PM ET**.
BYU routing: Kuali record by **Fri Oct 16**, complete and submitted for
internal review by **Fri Oct 23**, SPO submits **Wed Oct 28**. Nothing here has
been sent or submitted.

Revised 2026-10-10 (second pass): the AFOSR A.2.c white paper and the FLAIME
DOE narrative adapted to the ONR format, with corrosion and sustainment of
printed aluminum as the naval application.

| File | What it is | Status |
| --- | --- | --- |
| `onr-yip-technical-proposal.tex` / `.pdf` | Technical proposal for Field 8 (cover, contents, technical approach, management, PI qualifications, CV, letter, responsibility, data management plan, current and pending summary, references) | Draft, 12 of 20 counted pages |
| `abstract.txt` | SF-424 Project Abstract, marked "Approved for Public Release" | Draft, 3,942 of 4,000 characters |
| `budget/budget.py` | Budget model; every rate and quantity is in `ASSUMPTIONS`; writes the tables and the `budget-numbers.tex` macros used by both PDFs | Draft, $747,651 |
| `budget/budget-justification.tex` / `.pdf` | Budget justification for R&R Budget Section L | Draft, red TODOs |
| `budget/budget.csv` | Line items by year | Generated |
| `attachments/field10-facilities.tex` / `.pdf` | R&R Other Project Information, Field 10 (Facilities and Other Resources) | Draft, 1 page, TODOs |
| `attachments/field11-equipment.tex` / `.pdf` | Field 11 (Equipment), including the potentiostat justification | Draft, 1 page, TODOs |
| `kuali-checklist.md` | What BYU routing needs by Oct 23 | Draft |
| `onr-questions.md` | Emails to ONRYIP@navy.mil and the Grants Officer, plus PO questions | Ready to send Mon Oct 12 |
| `po-email.md` | Fit-check email to Dr. Charles Fisher (cc ONRYIP@navy.mil) | Ready to send Mon Oct 12 |
| `carderock-questions.md` | What to ask at the NSWC Carderock lecture, Oct 14 | Ready |
| `support-letter-draft.md` | Letter of support for the chair or dean | Needs signer and real figures |
| `preview/` | PNG renders of the proposal pages other than the CV (110 dpi) | Generated |
| `budget/preview/` | PNG renders of the budget justification's first pages | Generated |
| `onr-yip-technical-proposal-cu-ded.tex` / `.pdf` | **Alternative** technical proposal: seawater-resistant copper alloys designed as powders for blown-powder DED (section 9) | Draft, 17 of 20 counted pages |
| `abstract-cu-ded.txt` | SF-424 abstract for the alternative | Draft, 3,970 of 4,000 characters |
| `preview-cu-ded/` | PNG renders of the alternative's pages (110 dpi) | Generated |
| `attachments/field10-facilities-cu-ded.tex` / `.pdf`, `attachments/field11-equipment-cu-ded.tex` / `.pdf` | Fields 10 and 11 for the alternative (DED instead of LPBF, copper feedstock, powder checks) | Draft, 1 page each, TODOs |

Only one of the two technical proposals would be submitted. Section 9
compares them.

## 1. Page limits and format (NOFO pp. 15-20)

- 8.5 x 11 in, 1 in margins, single-spaced, Times New Roman 12 pt (the PDF
  embeds the real font).
- **Technical proposal: 20 pages.** Counted: Technical Approach, Management
  Approach, PI Qualifications, Responsibility. The draft uses **12** (pages
  1-11 plus Responsibility on page 12). The counted pages are numbered 1, 2,
  ...; excluded parts carry prefixes (CV, L, D, S, R).
- **Excluded:** cover page, table of contents, full CV, data management plan
  (2 pages max; draft is 1), letters of support, cited references, current
  and pending support. The budget has no page limit.
- **Abstract:** one page or 4,000 characters including spaces, whichever is
  less; standard keyboard characters only; Greek letters spelled out; no
  graphics; marked "Approved for Public Release" (p. 17).
- File names at most 68 characters; PDF only; no macros or passwords.

The 8 free pages are room, not a target. The most useful additions: a
quarter-page figure of real preliminary data (powder SEM, a printed cube, the
tensile curve), and corrosion data on the baseline alloy if any exists by
Oct 23.

## 2. What changed in this pass

- **Naval relevance** now leads with corrosion and sustainment of printed
  aluminum: Navy 5000-series sensitization (Golumbfskie et al. 2016, from
  Carderock; NAVSEA's 2012 estimate of $270M to repair cruiser
  superstructure cracking; beta-phase precipitation varying up to 40x between
  plate lots, NAVSEA STTR N18A-T010), the corrosion of printed AlSi10Mg along
  melt-pool borders (Cabrini 2016; Revilla 2017), mixed results for printable
  high-strength alloys (Linder 2024; Zhou 2021; Zhang 2023; Al-Hashem and
  Gupta 2026), FRC East's first printed aluminum fleet parts (Apr 2026), the
  Navy's August 2026 pathway for printed submarine parts, the 2019 America
  Makes "roadblock" statement, and ONR's corrosion program, which asks for
  work on corrosion of AM alloys.
- **A finding that shapes the plan:** in sensitized printed Al-Mg-Sc-Zr,
  cyclic polarization and impedance were unchanged while the beta phase
  covered most grain boundaries (Cabrera-Correa et al. 2023). The fast screen
  can miss exactly the failure the Navy fears, which is why the plan follows
  it with intergranular tests and audits what it discards.
- **Focus areas** now use the NOFO's own list (p. 12): primary Manufacturing
  (Integrated Manufacturing and Sustainment Technologies), secondary
  Materials and Electronics (Sustainable and Operationally Robust Materials).
- **Method:** the workflow now branches after microscopy into tensile tests
  and corrosion tests (a one-hour polarization screen, then intergranular and
  salt-spray tests). New Objective 5, Advance 4 (audit a random tenth of the
  candidates the screens would stop), and hypothesis H5 (the screen predicts
  the long tests).
- **From FLAIME:** the staged specimens (tracks, walls, cubes, then tensile
  bars and corrosion coupons, with a 99% density gate), feedstock weighed to
  0.1 mg into machined aluminum crucibles, ICP-MS composition checks, CALPHAD
  outputs used as weighted inputs, and scandium content as an objective
  (USGS: 100% import reliance, none mined or recovered domestically in 2025).
- **Budget:** two Ph.D. students, one undergraduate, summer salary for the
  PI, a potentiostat in Year 1, and LPBF builds filling what remains under
  the $250,000 annual cap: 28, 29, and 26 builds. Rates now follow BYU's
  2026 planning sheet (faculty summer fringe 19.7%; students 0% while
  enrolled, 7.7% in summer) and 2026-27 tuition.
- **Citation fix carried from FLAIME:** the FLAIME draft cites Thapliyal et
  al. 2020 for Al-Mn-Cr-Zr, but that paper designs an Al-1.5Cu-0.8Sc-0.4Zr
  alloy. It is cited here for what it is; FLAIME itself is unchanged.

## 3. Budget summary (all rates to be confirmed by BYU)

| | Year 1 | Year 2 | Year 3 | Total |
| --- | ---: | ---: | ---: | ---: |
| Direct costs | 176,706 | 170,688 | 171,565 | 518,959 |
| MTDC | 140,298 | 151,728 | 152,036 | 444,062 |
| F&A (51.5% of MTDC) | 72,253 | 78,140 | 78,299 | 228,692 |
| **Total** | **248,959** | **248,828** | **249,864** | **747,651** |

Rates from BYU SPO documents (read through the Wayback Machine): F&A 51.5%
MTDC (DHHS agreement of Aug 2023, provisional from Jan 2025 until amended);
fringe 19.7% on faculty summer salary, 0% on enrolled students, 7.7% (FICA)
on students when not enrolled; 3% inflation; 2026-27 graduate tuition $4,468
per semester (Latter-day Saint rate; $8,936 otherwise). Guesses still to
replace (all in `budget/budget.py`): personnel rates for the PI and students
[per-person rates removed];
potentiostat $18,000; Microscopy
Center $45 per hour; outside salt spray $1,500 per run; supplies.
To rebuild: `cd budget && python budget.py && xelatex budget-justification.tex`
(twice).

## 4. Placeholders still in the package

Red `[TODO ...]` markers in the PDFs, grouped by where they are.

**Technical proposal (`onr-yip-technical-proposal.tex`)**
1. Cover: program officer (confirm after his reply); administrative contact
   (BYU AOR); requested amount (final figures from BYU).
2. §1.5: figure of real preliminary data (powder SEM, cube, tensile curve).
3. §1.7: pre-registration site (e.g., OSF).
4. §1.8 Task 2: alloy families and element ranges to search.
5. §1.10: Carderock talk wording and any contacts who agree to be listed;
   SFRP application (closes Dec 14, 2026).
6. §1.12 Table 2: number of new alloys promised.
7. §3: corrosion or electrochemistry experience, or how the students will
   learn the ASTM methods.
8. Letter of support: signed PDF (draft in `support-letter-draft.md`).
9. §4 Responsibility: start-up equipment list; tensile load frame or
   service; federal award history; integrity statement; citizenship or
   permanent residency; BYU's SAM renewal (registration listed as ending
   Mar 4, 2027); RAO wording on controls; powder safety plan.
10. §5 Data Management Plan: metadata schema.
11. Current and pending: current awards; how the AFOSR and ONR scopes would
    be separated; other proposals submitted before Oct 30; collaborators,
    even unfunded ones (NOFO p. 38).

**Budget justification (`budget/`)**: 2027 fringe rates and whether the
students enroll in summer; the PI's salary base; the RA stipend; tuition for
a student paying the non-member rate; the undergraduate wage; the current
rate agreement PDF and the single-audit link; the potentiostat quote; service
rates (Microscopy Center, ICP-MS, machining, salt spray); travel on ONR's
spreadsheet; and catalog quotes for supplies.

**Field 10 and Field 11 attachments (`attachments/`)**: lab square footage,
tensile load frame, Thermo-Calc license and databases, the Utah facility's
name and printer, the salt-spray lab, the start-up equipment list, and the
potentiostat quote.

**Not drafted at all**: the SciENcv biosketch and current-and-pending forms,
and the signed letter.

## 5. Program officer plan

1. **Mon Oct 12:** send `po-email.md` to Dr. Charles Fisher (Materials &
   Processes for AM, Code 332), cc ONRYIP@navy.mil (first email only; NOFO
   p. 11). Send Email 1 of `onr-questions.md` to ONRYIP@navy.mil the same
   day.
2. **Also consider Dr. David Shifler** (Corrosion Science and Corrosion
   Control Technologies, Code 332, david.a.shifler.civ@us.navy.mil). His
   program page asks for the "corrosion mechanism in additive manufactured
   (AM) alloys" and says machine learning can "accelerate materials
   discovery". With corrosion now a main objective, his program may fit as
   well as Dr. Fisher's. A short note to him, without the ONRYIP cc, asking
   whether he would rather see it in his program is cheap. If he takes it,
   SF-424 Field 4b becomes `332 [Shifler, David]`, and the Materials and
   Electronics focus area should move to primary.
3. **Wed Oct 14:** Carderock talk (`carderock-questions.md`).
4. **Fri Oct 16, 5 PM ET:** last day for questions.

Other Code 332/351 contacts the research turned up (not contacted): Dr. Pani
Varanasi (Computer-Aided Materials Design; also Structural Metals, which
lists "temperature-resistant aluminum alloys"); Dr. Jennifer Wolk
(Manufacturing Focus Area Lead); Mr. Bill Nickerson and Dr. Michael Brindza
(Code 351 Aerospace Structures and Materials, "Reliability and Sustainment").
Both the Materials and the Manufacturing focus areas sit in Code 33, which
gets at most five YIP awards (NOFO p. 6).

## 6. Timeline

| Date (2026) | Step |
| --- | --- |
| Mon Oct 12 | Send PO email and ONR questions. Ask chair or dean for the letter. Tell BYU RAO; open the Kuali record. |
| Wed Oct 14 | NSWC Carderock lecture; collect answers from `carderock-questions.md`. |
| Fri Oct 16, 5 PM ET | ONR question cutoff. |
| Mon Oct 19 | BYU rates in the budget; potentiostat quote; Field 10 and 11 TODOs filled. |
| Wed Oct 21 | Signed letter in hand; proposal text final. |
| Fri Oct 16 | BYU: Kuali record started and SPO told (two weeks out). |
| Fri Oct 23 | BYU: complete in Kuali and submitted for internal review (five business days out). |
| Wed Oct 28 | SPO submits on Grants.gov (BYU rule and NOFO p. 28: two business days early). |
| Fri Oct 30, 5 PM ET | Deadline. |

## 7. Build and checks

```bash
cd near-term-submissions/onr-yip
xelatex onr-yip-technical-proposal.tex && xelatex onr-yip-technical-proposal.tex
(cd budget && python budget.py && xelatex budget-justification.tex && xelatex budget-justification.tex)
cringe-filter lint -c proposal onr-yip-technical-proposal.tex
cringe-filter score -c proposal onr-yip-technical-proposal.tex
```

- cringe-filter (proposal): 0 errors; info notes are long list sentences,
  repeated short phrases, and "Robust" inside the NOFO's focus-area name.
- Emails (email context): 0 findings, at or under the 170-word budget.
- References: the new corrosion and Navy references were checked on
  Crossref (DOIs) or by opening the source page on 2026-10-10.

## 8. Sources read on 2026-10-10

- NOFO: https://files.simpler.grants.gov/opportunities/19850d71-3af6-4f9f-bf6e-1ee9b1f8d8b7/attachments/0a379549-42bb-4c7d-b54a-cc85e280a200/FY27_YIP_NOFO_N0001426SF004__003.pdf
- ONR programs: Materials & Processes for AM; Corrosion Science and Corrosion
  Control; Computer-Aided Materials Design (URLs in the reference list).
- Navy: FRC East release (Apr 27, 2026); Navy PPD 802-8436658 release
  (Aug 21, 2026); NAVSEA Carderock pages on AM and corrosion laboratories;
  ONR Summer Faculty Research Program dates (applications close Dec 14,
  2026).
- USGS Mineral Commodity Summaries 2026, Scandium.

## 9. Alternative: copper alloys for blown-powder DED

`onr-yip-technical-proposal-cu-ded.tex` and `abstract-cu-ded.txt`, drafted
2026-10-17 after the Oct 16 call with Dr. Fisher (the call notes are private
and are not in this repo). Same NOFO, same program (Materials & Processes for
AM, Code 332), same method. What it designs is different: a pre-alloyed
copper alloy powder for single-stream, blown-powder directed energy
deposition (DED) that deposits dense and crack-free, on itself and on the
alloys it would repair, and resists seawater as deposited at least as well as
70-30 copper-nickel. Nickel-aluminum bronze (NAB) is the second family.

| | Aluminum version | Copper/DED version |
| --- | --- | --- |
| Title | Cost-Aware Selection of Experiments for Printable, Corrosion-Resistant High-Strength Aluminum Alloys | Cost-Aware Design of Seawater-Resistant Copper Alloy Powders for Blown-Powder Directed Energy Deposition |
| Alloys | Al with Zr or Sc, plus Cu, Mg, Zn, Mn, Cr | Cu-Ni (10-30 Ni) with Fe, Mn, Cr; Al bronzes with Ni, Fe, Mn |
| Process | LPBF builds bought from a Utah user facility | Single-stream blown-powder DED sessions on a FormAlloy X2 at an outside facility (Sam's), with pre-placed powder tracks on the same laser as a cheaper first step |
| Powder | Ultrasonic atomization, LPBF size range | Same atomizer at 40 kHz; sieved into 45-105 and 100-200 um cuts; flow, density, oxygen and carbon checked; a first lot of about 0.5 kg for tracks, then about 2 kg (about six runs) for each composition the search sends to blown powder |
| Physics inputs | CALPHAD at equilibrium / Scheil | CALPHAD evaluated along a heat-flow model of the DED thermal history (new Advance 3, new H3: process-aware beats equilibrium beats none) |
| Corrosion | Polarization screen, then intergranular and salt-spray tests | Polarization, LPR, and impedance in substitute ocean water, then 30-day immersion with mass loss and depth of selective attack; flowing seawater left to Navy labs |
| New branch | none | Repair coupons on cast NAB and wrought Cu-Ni plate (cracks, dilution, hardness across the fusion line) |
| Supply objective | Scandium content | Nickel content |
| Kept as is | | Linked-model cost-aware search, Advances 1, 2 and the audit (now Advance 5), H1, H2, H4, the synthetic benchmark figures (still aluminum, captioned as such), management, responsibility, DMP |
| Overlap with the AFOSR white paper | Same alloy system and method | Method only, so the scopes separate cleanly |

**What the new sections rest on (checked 2026-10-17).** Navy facts come from
primary sources: NAVSEA's AM material specifications on ASSIST (MIL-PRF-32804,
wire-arc 70-30 Cu-Ni; MIL-PRF-32815, LPBF 70-30 Cu-Ni; MIL-PRF-32816, wire-arc
NAB, which keeps the castings' 1250 F, 6-hour anneal; none for blown-powder
laser DED of either alloy), MIL-B-24480A, MIL-T-16420K, CDA data sheets and
Pub 222, the ONR program pages (the AM program's thrusts include "large scale
AM" and "additive repair"), the Federal Register critical-minerals lists
(nickel since 2022, copper since 2025), and HII, NNS, NAVSUP, and DVIDS
releases on printed Cu-Ni parts and the casting bottleneck. Every literature
reference was checked on Crossref. The proposal also cites NSWC Carderock's NAB
processing paper and its temperature-dependent property databases for NAB and
Cu-Ni, as inputs to the heat-flow model.

**Edison follow-up (2026-10-17, 50 queries).** The full synthesis is in
[`edison-trajectories/cu-ded-2026-10/README.md`](../../edison-trajectories/cu-ded-2026-10/README.md).
Its section 2 lists the 12 edits it made to the proposal. They raise the
draft to 15 counted pages and 100 references. The main ones:

- **A wrong claim removed.** The earlier draft said there was no corrosion
  study of Cu-Ni made by blown-powder laser DED. There is one: Cu-30Ni made
  by direct metal deposition on C71500 (Bhattacharya et al. 2011). A 2012
  ISSC review reports that it corroded faster than the plate.
- **Prior art for the powder route.** Ultrasonic atomization of NAB chips
  (and of copper scrap) for laser DED is already published, in existing
  compositions.
- **Annealing.** Evidence that annealing NAB helps or hurts depending on the
  starting microstructure.
- **Short screens.** Numbers showing that one-hour screens can mislead.
- **Comparison section.** New entries for the nearest ML, BO and DED work.
- **Powder size.** Peer-reviewed DED powder cuts (45-106 and 45-150 um)
  replace the vendor convention.

Jia et al. 2026 is still unread: Edison could not open it, and the Pi is not
reachable from this repo's workflow.

**High-effort follow-ups and the U of U InssTek (2026-10-17, afternoon).**
Three `LITERATURE_HIGH` Edison jobs (batch 6) and the answer to "does the
InssTek at UofU have a DED laser that works with copper?" are in section 6
of the synthesis. In short:
- **The machine.** The InssTek in Prof. Zak Fang's Metal AM lab is most
  likely an MX-Lab: a 500 W ytterbium fiber laser (infrared, not blue), a
  400 um beam, six hoppers, and 45-150 um powder.
- **Infrared is likely enough for these alloys.** 70-30 Cu-Ni, 90-10 and NAB
  conduct heat at about a tenth of pure copper's rate, and infrared DED of
  aluminum bronze has been reported. Pure copper would need a blue laser.
- **Power is the limit.** No published infrared DED of Cu-Ni or NAB at
  500 W or less was found, and thick repair plates are the hard case.
- **Claims audit.** Five sentences of the draft were corrected or qualified.
  One was backwards: nickel is richer in the dendrite cores of printed 70-30,
  not between them. Three references were added (blended-powder DED of
  Cu-Ni), for 103 in total; the draft is still 15 counted pages.
- **Option, not adopted.** The MX-Lab's hoppers could blend pre-alloyed
  powders into a cheap, lower-fidelity node ahead of atomizing. It is in
  section 6.3 of the synthesis, not in the proposal.

**Search space and the CubXL (2026-10-17, evening).** Sterling asked for
the copper search space to be backed the way the aluminum one was, and for a
look at the CubXL for the corrosion screen.
- **Search space.** 50 Edison queries, one per element, plus a joint query,
  two ANALYSIS syntheses, subagent checks of every answer, and a TCCU7
  coverage table. All of it is in
  [`edison-trajectories/cu-ded-elements-2026-10/`](../../edison-trajectories/cu-ded-elements-2026-10/README.md).
  - **Searched from the start:** Ni 0-30, Al 0-9.5, Fe 0-4.5, Mn 0-4,
    Ti 0-0.5, plus Cr 0-0.7, Si 0-0.5 and Nb 0-0.8 in Cu-Ni only.
  - **Hard limits:** Cu at least 65, and a CALPHAD liquidus of at most
    1,250 °C.
  - **Rules keyed to Al:** Ni at least Fe above 7 Al; Fe at most 2.3 below
    1.5 Al.
  - **Year 2 additions, as matched tests:** Zr and B; Sn and Ge, in NAB
    only; and La or Ce.
  - **In the proposal:** a new Task 2 paragraph and Table 1 replace the
    two-sentence alloy space and its TODO. The draft is now 16 counted
    pages, with 111 references.
- **CubXL.** The one-hour screen needs a potentiostat, but probably not an
  $18,000 benchtop unit.
  - **Instrument:** an EmStat Pico (about $580, with impedance) on the CubXL
    covers the currents copper alloys give in 3-4 mm wells.
  - **Cross-check:** a borrowed benchtop instrument covers the flat-cell
    checks.
  - **What the CubXL adds:** wells across repair fusion lines, ICP-MS of
    every used electrolyte, and immersion vials sampled over time.
  - **Write-up:** `cubxl-electrochemistry.md`. The proposal's corrosion
    paragraph and Fields 10 and 11 now describe the CubXL.
  - **Still open:** the equipment line is a TODO (option a or b in that
    file), because `budget.py` is private.

**Atomizer set-up for copper, from AMAZEMET (2026-10-17, night).** Bartosz
Kalicki answered the copper questions by message
([PR #117](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-6243956526)).
- **Pure copper:** a 0.5 mm nozzle, the 1:1.5 booster, and a carbon-carbon
  (CFC) part with a Mo coating. He wrote "CFC nozzle"; he most likely means
  the plate. In the consumables tour on Sep 30 (Training Video 9 at 39:01,
  [byu-vcl notes](https://github.com/vertical-cloud-lab/byu-vcl/blob/88eeace/atomizer-training/notes/groupC.md))
  he showed us a CF plate with a Mo-coated tip "used mostly for copper", and
  he has said CF plates only run on the 1:1.5 booster (byu-vcl#268). Asked to
  confirm. The first pour heats the plate; once the melt wets it,
  atomization is continuous.
- **NAB and 90-10:** nickel and iron "can lead to high reactivity with the
  crucible", so coat the crucible and use an hBN nozzle. He said the same in
  training (Video 4 at 3:35). The same tour shows BN nozzles, alumina
  sealing rods for reactive melts, and Mo- and W-coated CF plates in our
  kit (Video 9 at 34:17-39:22).
- **Published basis:** AMAZEMET's Choma et al. 2026 (*Materials* 19, 2803,
  doi:10.3390/ma19132803; Bartosz is a co-author) atomized about 500 g of
  CuSn8 per run on a rePOWDER induction module at about 1300 °C. They used
  C/C plates with Si-Mo, Si-W and three other coatings, a standard 0.5 mm
  graphite nozzle, about 50 ppm O2, and 0.6 bar working pressure after a
  1.5 bar burst at the start. 80-90% of the feed became powder, much of it
  63-150 um. The Edison runs (cu-ded-2026-10) did not find this paper.
- **In the proposal:** Preliminary results state the 1,300 °C working limit.
  Task 2 describes the hBN nozzle for Ni- and Fe-bearing melts and the
  coated plate, cites Choma 2026, adds an SEM check for plate fibers, and
  adds carbon to the oxygen analysis. It also said the crucible was
  BN-coated, which was wrong (corrected 2026-10-18, below). Risks covers
  coating wear and carbon pickup, and Fields 10 and 11 match. The
  Ti-6Al-4V-plate and ceramic-crucible TODOs are gone. Still 16 counted
  pages, now with 112 references.
- **First run** (superseded 2026-10-18, below): NAB (McMaster 8203K41) on a
  copper-only crucible set, with oxygen-free copper (8965K72) as a fallback
  that uses the pure-copper set-up as given; 90-10 is on hold.

**Crucible coating, corrected (2026-10-18).** The lab has no BN-coated
crucible
([PR #117](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-6244476716)).
The previous entry took a pre-run checklist item in the training SOP,
"Crucible BN-coated the night before and dry" (byu-vcl PR #255,
`atomizer-training/sop.md`), as lab practice. It records Bartosz's advice;
the aluminum runs have used bare graphite.
- **What he said in training:** crucibles are not sold coated. Users spray
  their own, like paint: a thin coat of BN in an alcohol carrier with
  inorganic binders, applied the night before and left to dry. A bottle is
  about $50, and a coat lasts a few runs (Training Video 1, Sep 29,
  41:59-43:10). On Sep 28 he said a coating is good for reactive melts and
  that aluminum and magnesium are fine without one. He named a US maker in
  Oak Ridge (ZYP Coatings) and offered to name the spray AMAZEMET uses
  (phone recording, 10:34-11:36).
- **Spray:** ZYP's BN Aerosol Lubricoat (13 oz) is $45 from ZYP and
  $52.95 at Delphi Glass, ground shipping only. Its carrier is ethanol and
  acetone and its binder magnesium silicate, which fits his description.
  ZYP's datasheet for the aerosol gives 1,000 °C (1,832 °F) in air,
  1,400 °C in vacuum and 1,800 °C in inert gas; Delphi's "1800 °F" is the
  in-air figure for glass kilns. (This line first cited the datasheet for
  EAS-25, a water-based paint ZYP makes for Pyrotek; its limits are the
  same.) Henze's HeBoCoat SL-E 125 (ethanol, inorganic binders) also fits,
  but I found it only from a UK seller.
- **NAB from bare graphite has precedent:** Müller et al. 2023 atomized NAB
  grinding chips on an AMAZEMET rePowder with "a graphite-based crucible and
  pouring system", a 1 mm nozzle, 1300 °C and a 40 kHz CF plate. Yield was
  77% and oxygen 0.0125%. The paper doesn't mention a coating and didn't
  measure carbon. Earlier notes put this run on an AUS 500; that is the
  machine Uhlmann et al. 2024 name (the version AMAZEMET developed with Blue
  Power).
- **In the proposal:** Task 2 now says the crucible is graphite and is
  sprayed with BN before Ni- and Fe-bearing melts, and cites Müller 2023 for
  NAB from graphite on our model. The Preliminary-results TODO, the Risks
  wording and Field 10 match. Still 16 counted pages, 112 references.
- **First runs:** oxygen-free copper (C10100) first, in the bare crucible,
  with the pure-copper set-up Bartosz gave. NAB follows once the crucible is
  sprayed, or goes in a spare bare crucible if he agrees.

**Coating sources and alumina (2026-10-18, later)**
([PR #117](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-6245344292)).
- **ZYP Coatings:** 120 Valley Court, Oak Ridge, TN 37830; +1-865-482-5717;
  info@zypcoatings.com; Mon-Fri 8-5 Eastern. It sells direct online (US and
  Canada prices).
- **Fastest BN options:** ZYP's BN Lubricoat Blue Spray (SKU 1066, $31,
  12 oz trigger bottle) is water-based with an alumina binder and has the
  same three limits. ZYP says it is non-flammable and non-pressurized, so it
  need not go by ground like the aerosol (SKU 1047-00). McMaster 10515K35 is
  a 13 oz BN-and-ceramic aerosol rated 32-1,560 °F; McMaster doesn't name
  the maker, and the product detail and SDS need a login (the SDS names
  Momentive; see 2026-10-20, below).
- **Alumina:** ZYP's A Aerosol (SKU 4039, $72) has the same carrier and
  binder as the BN aerosol and is rated to 1,500 °C in vacuum with carbon
  present. It would suit these alloys chemically. Molten Cu makes 110-117°
  with alumina at 1,150-1,400 °C (Shen et al. 2005, doi:10.1557/JMR.2005.0127),
  and Cu-rich Al-Cu melts about 120° at 1,100 °C (Schmitz 2011, RWTH
  dissertation). AMAZEMET's patent EP4192985B1 melts CuCrZr in an alumina
  crucible. Oxygen in the copper lowers the angle, to as little as 22° at
  1,300 °C (Diemer et al. 1999, doi:10.1111/j.1151-2916.1999.tb02163.x),
  another reason to use C10100 rather than C11000. BN stays first: it is
  what Bartosz advised, and hBN is soft, while a flake of alumina is a hard
  particle that could block the 0.5 mm nozzle or end up in the powder. ZYP
  rates its solvent-based oxide aerosols "low adherence". Of the Year-2
  additions, Ti and Zr can react with both alumina and BN, and La and Ce
  form oxides more stable than alumina; ZYP sells yttria (Y Aerosol,
  Type Y) for reactive melts like those.
- **McMaster:** no alumina coating that fits. It has alumina casting
  compounds and ceramic adhesives, which go on thick, and 0.5 um BN powder
  (1402N13), which could be stirred into ethanol as a weak, binder-free
  stopgap.
- **Coating service:** none found that could coat a crucible this week.
  CVD pBN or SiC on graphite is custom work, and a plasma-sprayed coating
  would change how the nozzle and sealing rod seat.

**McMaster 10515K35 SDS (2026-10-20)**
([PR #117](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-6282838103)).
- **What it is:** Momentive Technologies' Boron Nitride Spray II (part
  2111750, Strongsville, OH; SDS v1.1 of 2024-12-12), a "high temperature
  mold release for metals and glasses". $52.73 from McMaster.
- **Carrier:** ethanol 30-60%, acetone 10-30%, methanol 1-5% and MIBK
  0.1-1%, with propane, n-butane and isobutane as propellant. This is the
  same family as ZYP's aerosol (ethanol/acetone, propane/butane). The
  contents are 94.5% volatile, so the dried coat is about 5.5% of the can;
  BN is 1-5%.
- **Binder:** not named; non-hazardous ingredients need not be listed. The
  Prop 65 table lists 0.034% quartz, which suggests a silicate mineral such
  as a clay. Momentive's water-based grades use bentonite or alumina. ZYP's
  aerosol uses magnesium silicate and fires to 97% BN.
- **Ratings:** Momentive's
  [coatings page](https://www.momentivetech.com/products/boron-nitride-coatings-2024)
  rates its dried BN coatings to 850 °C in oxidizing atmospheres and
  1,800 °C in inert gas or vacuum; McMaster's 1,560 °F (849 °C) is the
  in-air figure. About 100 ft² per 13 oz can (ZYP: 30-50).
- **Silicon bound:** the can holds about 20 g of solids for its 100 ft², so
  a coat is about 0.2 mg/cm². Even 0.5 g of coat, all of it silica (47% Si)
  and all dissolved into a 300 g NAB charge, would add 0.08% Si; C63000
  allows 0.25%.
- **Handling:** signal word Danger: extremely flammable aerosol. The
  methanol brings the organ-damage statement (H370) and the MIBK the
  suspected-carcinogen one (H351). Spray outside the atomizer, in a fume
  hood away from ignition sources, with gloves and goggles, and let it dry
  there. Ships as UN1950, Limited Quantity.

**DED facility: a FormAlloy X2 (2026-10-21)**
([PR #117](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-6321072541)).
Sam, at a facility with a FormAlloy X2 (name and location still to fill in),
sent external rates and photos of copper-nickel tracks from a senior design
project. The photos are not in this repo.
- **Rates:** machine time $155 per hour and labor $165 per hour (the
  facility's external SIF rate). A typical build of four 1-inch cubes is
  3 machine hours and about 2 labor hours, so **$795**, or $1,204 with BYU's
  51.5% F&A (a purchase of services, not a subaward, so it is in MTDC).
  Machine time scales with deposition rate and volume. We supply the powder,
  or the facility supplies it at cost.
- **Powder size:** about 50 to 150 um, sometimes up to 200 um; the usual cuts
  are 45-105 and 100-200 um. Our rePOWDER is a 40 kHz system (training notes:
  scan 39-41 kHz). At 40 kHz, NAB came out at d10/d50/d90 = 48/98/174 um
  (Uhlmann 2024), and on our model 80-90% of each ~500 g CuSn8 charge became
  powder, much of it 63-150 um (Choma 2026, checked in the full text). So
  nearly all of a lot is usable, and a 20 kHz stack isn't needed.
- **Quantity:** the X2's hoppers need about 2 kg of each powder, and the
  facility plans on 50% catchment. Four 1-inch cubes are 65.5 cm3: 0.59 kg of
  Cu-Ni or 0.50 kg of NAB, so about 1.2 or 1.0 kg fed. Whether one 2 kg lot
  covers both sessions for a composition depends on whether the powder left
  in the hopper comes back and whether a part-filled hopper still feeds (ask
  Sam). At about 0.36 kg of in-cut powder per 0.5 kg run, 2 kg is **about
  six atomizer runs** (about ten at AMAZEMET's general advice of 250-300 g
  per run), and coated plates wear out after a few runs.
- **What it does to the design:** the proposal said a composition costs one
  atomizer run. Blown powder now costs about six. The draft therefore adds
  the step Sam's group already used: powder spread in grooves and melted by
  the same laser. These **pre-placed tracks** need a few grams per groove,
  so the first 0.5 kg lot is plenty. Tracks on cast NAB and wrought Cu-Ni
  plate also show early whether a composition fuses to the repair
  substrates. The models treat them as a cheaper, less faithful measurement;
  the audit (Advance 5) checks how often they mislead. Only compositions
  whose tracks are sound get the 2 kg lot. The scale-up becomes one more
  decision the cost-aware rule makes.
- **Laser:** not stated. Cornell's X2 has a 500 W infrared laser, a 1.2 mm
  spot, two powder feeders and an 8 x 8 in bed
  ([Moridi lab](https://moridi.mae.cornell.edu/equipment-2)), and FormAlloy
  also sells blue lasers. Sam's tracks suggest this X2 already melts Cu-Ni
  (confirm they were made on it). Pure copper would still need blue (see the
  U of U entry above).
- **U of U InssTek:** now the fallback. It has no rate yet, and its 45-150 um
  window is narrower.
- **Budget (for `budget.py`, which is private).** The session line still
  fills what remains under the $250,000 cap, so the cover totals should move
  by less than one session. Proposed changes, with my guesses marked:

  | Line | Basis | Per year |
  | --- | --- | --- |
  | DED sessions (replaces LPBF builds) | $795: 3 h at $155 + 2 h at $165 | what remains |
  | Pre-placed track sessions | guess: 1 machine h + 2 labor h = $485, 6 a year | $2,910 |
  | Copper feedstock (OFC bar, Ni, Fe, Mn, Al, Cu master alloys), replacing the Al master alloys and Al bar | guess: about 35 kg a year (about 7 scale-ups and 25 first lots) | $4,000 |
  | Coated C/C plates, hBN nozzles, BN spray, crucibles | guess: about 65 copper runs a year; ask AMAZEMET for prices | $6,000 |
  | Commercial 70-30 Cu-Ni and NAB powder, 45-105 um | at least 2 kg each; quote needed | $1,500, then $750 |
  | Cast NAB and wrought C71500 plate (repair substrates, build plates) | guess | $1,500 |
  | Oxygen and carbon analyses, outside lab | guess: about 20 lots | $2,000 |
  | Shipping powder and deposits | guess | $600 |

  These lines take about $18,500 of the $29,750 (Year 1) that the LPBF
  builds and aluminum feedstock had. The rest buys about **14, 16 and 13
  blown-powder sessions** in Years 1-3, or about 7 compositions a year at
  two sessions each. Replacing the $18,000 potentiostat with option (b) in
  `cubxl-electrochemistry.md` frees about $11,300 of MTDC in Year 1, about
  14 more sessions.
- **In the proposal:**
  - Fig. 1 has a pre-placed-tracks node, and immersion now sits under the
    corrosion screen.
  - §1.1 notes the 2 kg hopper and about six runs; Preliminary results
    mentions Sam's Cu-Ni tracks (TODO: ask Sam's permission).
  - Task 2 gives the 40 kHz sizes and Sam's cuts (the frequency TODO is
    gone; the search's atomizer settings are now melt temperature, pour
    pressures and plate amplitude). It names the X2, the session, the
    2 kg / 50% figures and the track step.
  - Management gives the session count. Risks, Table 2 (Y1, M1), Advance 4,
    the DMP and the abstract (3,970 of 4,000 characters) mention the
    tracks.
  - Fields 10 and 11 name the X2; Field 10 still fits on one page.
  - 17 of 20 counted pages (was 16), 112 references; cringe-filter 0
    errors.

**Placeholders specific to this version** (red TODOs in the PDF):

1. **DED facility.** Sam's FormAlloy X2 (2026-10-21, above). Still to fill
   in: the facility's name and location, the laser (wavelength, power,
   spot), the shielding, preheat, turnaround, whether unused hopper powder
   comes back, and whether a smaller hopper can run a few hundred grams.
   Get the rates in writing for the budget justification. The budget macros
   are still the aluminum version's (28, 29 and 26 LPBF builds at $800);
   enter the lines in the 2026-10-21 table in `budget/budget.py` (private).
   The totals should move by less than one session a year.
2. **Atomizer for copper.** Settled (see above): the 1,300 °C working limit,
   graphite crucibles sprayed with BN before Ni- and Fe-bearing melts (the
   spray still has to be bought), an hBN nozzle for those melts, and a Mo- or
   W-coated C/C plate on the 1:1.5 booster. Still open:
   - the plate, nozzle bore and setpoint for NAB and Cu-Ni (asked);
   - the charge size (the draft assumes about 0.5 kg, as in Choma 2026);
   - the price of coated C/C plates and hBN nozzles, now that each
     composition sent to blown powder takes about six runs.
   The plate frequency is settled: our unit runs at 40 kHz, which fits the
   X2's cuts.
3. Commercial 70-30 Cu-Ni and NAB powders for the baselines, at least 2 kg
   each in 45-105 um (the facility can also supply powder at cost).
4. A first copper powder lot (SEM and size distribution) as preliminary
   data: C10100 in the bare crucible, then NAB once the crucible is sprayed.
   The runs are planned for the week of Oct 19; attachments can be replaced
   until SPO submits on Oct 28. Also ask Sam whether the facility's Cu-Ni
   tracks, and a photo, may be shown; if not, cut the sentence in
   Preliminary results and the "already used for copper-nickel" clause in
   Task 2.
5. Thermo-Calc: confirm the BYU license includes TCCU, and which version
   (the search-space coverage numbers are for TCCU7, Thermo-Calc 2026b).
6. Oxygen (inert-gas fusion) and carbon (combustion) analysis at a service
   lab. Carbon, because the crucible is graphite and the plates are C/C.
7. Immersion durations, the selective-attack depth limit in H5 (the TODO now
   lists published 21- and 30-day depths of 1.8 to 3.4 um and more than 3 um),
   and natural or substitute seawater.
8. Search space: proposed (Table 1, `search_space.py`). Still open: the
   number of new alloys promised (about 7 compositions a year can go to
   blown powder at the estimated session count, so 6 over three years would
   be safe), and whether to add Mn-Al bronze (C95700) as a Ni-free branch.
9. Handling nickel powders (safety plan).
10. Fields 10 and 11 have copper versions (`attachments/*-cu-ded.*`), now
    naming the X2. The letter of support carries the copper title as a
    bracketed option; its "powder-to-part demonstration on an aluminum
    alloy" holds for both.
11. Check the 2011 Cu-30Ni corrosion study's conditions and numbers, and get
    Jia et al. 2026, through the Pi (byu-vcl) or the library. Read
    literally, the 2011 abstract ranks the deposit above the plate, the
    reverse of the ISSC review the draft cites, so check the direction
    before submission.
12. The potentiostat and equipment line: a module potentiostat on the
    CubXL plus a borrowed benchtop for cross-checks, or the $18,000 benchtop
    unit (`cubxl-electrochemistry.md`). The first option now buys about 14
    more DED sessions in Year 1.
13. Collaborators: if Sam agrees, name Sam as an unfunded collaborator in
    the Management section and in current and pending support (NOFO p. 38).

All other TODOs (cover contacts, CV, responsibility, DMP schema, current and
pending) are the same as in section 4.
