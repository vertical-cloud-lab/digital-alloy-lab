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
| `onr-yip-technical-proposal-cu-ded.tex` / `.pdf` | **Alternative** technical proposal: seawater-resistant copper alloys designed as powders for blown-powder DED (section 9) | Draft, 14 of 20 counted pages |
| `abstract-cu-ded.txt` | SF-424 abstract for the alternative | Draft, 3,947 of 4,000 characters |
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
| Process | LPBF builds bought from a Utah user facility | Single-stream blown-powder DED sessions, facility TBD |
| Powder | Ultrasonic atomization, LPBF size range | Same atomizer; sized for blown powder; flow, density, oxygen checked; atomizer settings chosen by the search |
| Physics inputs | CALPHAD at equilibrium / Scheil | CALPHAD evaluated along a heat-flow model of the DED thermal history (new Advance 3, new H3: process-aware beats equilibrium beats none) |
| Corrosion | Polarization screen, then intergranular and salt-spray tests | Polarization, LPR, and impedance in substitute ocean water, then 30-day immersion with mass loss and depth of selective attack; flowing seawater left to Navy labs |
| New branch | none | Repair coupons on cast NAB and wrought Cu-Ni plate (cracks, dilution, hardness across the fusion line) |
| Supply objective | Scandium content | Nickel content |
| Kept as is | | Linked-model cost-aware search, Advances 1, 2 and the audit (now Advance 5), H1, H2, H4, the synthetic benchmark figures (still aluminum, captioned as such), management, responsibility, DMP |
| Overlap with the AFOSR white paper | Same alloy system and method | Method only, so the scopes separate cleanly |

**Placeholders specific to this version** (red TODOs in the PDF):

1. **DED facility, system, and price per session.** The budget macros are
   still the aluminum version's: its G line is 28, 29, and 26 LPBF builds at
   $800. DED sessions will cost more and there will be fewer; re-price in
   `budget/budget.py` (private) and the totals on the cover page change.
   Materials lines also change (copper bar, nickel and master alloys instead
   of aluminum bar and Al master alloys).
2. **Atomizer limits for copper:** the induction module's maximum melt
   temperature (70-30 Cu-Ni melts close to it), the crucible material, the
   charge size, and the plate frequencies (sets the median size; Lang's
   relation gives about 75 um for a copper melt at 20 kHz).
3. Commercial 70-30 Cu-Ni and NAB powders for the baselines.
4. A first copper powder lot (SEM and size distribution) as preliminary
   data, if a run fits before Oct 23.
5. Thermo-Calc: confirm the BYU license includes a copper database.
6. Oxygen analysis (inert-gas fusion) at a service lab.
7. Immersion durations, the selective-attack depth limit in H5, and natural
   or substitute seawater.
8. Alloy families and element ranges; number of new alloys promised.
9. Handling nickel powders (safety plan).
10. Fields 10 and 11 have copper versions (`attachments/*-cu-ded.*`). The
    letter of support carries the copper title as a bracketed option; its
    "powder-to-part demonstration on an aluminum alloy" holds for both.

All other TODOs (cover contacts, CV, responsibility, DMP schema, current and
pending) are the same as in section 4.
