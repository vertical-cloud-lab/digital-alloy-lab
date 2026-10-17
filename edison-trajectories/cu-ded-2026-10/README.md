# Copper alloy powders for blown-powder DED: 50 Edison queries (2026-10-17)

*Prepared for PR #117, the copper/DED version of the ONR FY27 YIP proposal
(`near-term-submissions/onr-yip/onr-yip-technical-proposal-cu-ded.tex`).
Sterling asked for two things on 2026-10-17: source Jia et al. 2026 with the
Pi, and run five batches of ten Edison queries that build on each other. The
queries cover single-stream blown-powder DED and copper alloys: naval
applications first, then copper alloy powder making in general.*

## What was run

| Batch | Submitted (UTC) | Built on | Jobs | Done |
| --- | --- | --- | --- | --- |
| 1 | 05:10 | earlier aluminum/LPBF runs, the draft's open questions | 7 LITERATURE, 2 LITERATURE_HIGH, 1 PRECEDENT | 05:42-05:44 |
| 2 | 05:37 | lessons of the aluminum/LPBF runs (batch 1 still running) | 8 LITERATURE, 2 PRECEDENT | 06:08 |
| 3 | 05:46 | batch 1 | 8 LITERATURE, 1 LITERATURE_HIGH, 1 PRECEDENT | 06:16 |
| 4 | 06:11 | batch 2 | 9 LITERATURE, 1 PRECEDENT | 06:41 |
| 5 | 06:20 | batch 3, plus a final novelty check | 9 LITERATURE, 1 PRECEDENT | 06:42-06:52 |

Every job, including standard LITERATURE, took about 30 minutes, so five
sequential batches would not have fit the 3-hour job limit. The batches were
staggered instead: each one was written from the batches that had finished.
`queries.py` holds all 50 questions, and the comment above each batch says
what it follows up on. `edison_cu_ded.py` submits, waits, and fetches.
`batchN/` holds the answers (question first, then Edison's answer), `raw/`
the gzipped verbose trajectories, and `_task_ids.json` the task IDs and times.
The question template follows the earlier runs in
`../recent-developments-2026-10/`:

- a context block, with the PI's own papers excluded;
- a request for DOIs, process, composition, test conditions and numbers;
- tags ([CITE], [NUMBERS], [NAVY], [NOVELTY-RISK], [GAP]);
- an instruction to say so when nothing is found.

**How it was checked.**
- **DOIs:** 100 of the 103 DOIs checked resolved on Crossref with matching
  titles. The three that did not are a CNKI DOI (Gao et al. 2025), a
  Fraunhofer repository DOI (Müller et al. 2021), and an Elsevier chapter
  DOI (Phull and Abdullahi 2017).
- **Full text:** where a paper is open access, its full text was read through
  Europe PMC (Uhlmann et al. 2024; Song et al. 2024) or its Crossref abstract
  (Cabrioli et al. 2025; Sparrow et al. 2026; Ukabhai et al. 2025; Menon et
  al. 2022).
- **Unchecked:** other numbers come from Edison's reading of the papers and
  are marked "(Edison)" where they matter. Edison often reads a paper's
  results through a review (e.g. Nemani et al. 2024) and says so. Treat
  those as leads, not citations.

## 1. Jia et al. 2026 and the Pi

**The Pi is not reachable from this repo.** byu-vcl's `claude.yml` joins the
runner to the tailnet with a "Connect to Tailscale" step and passes the Pi's
`RPI_*` user, host and password variables. This repo's `claude.yml` has
neither, and `tailscale` is not installed on the runner. The block the Pi
gets around is real: ScienceDirect returns 403 to this runner, and MDPI and
nature.com also refused the web-fetch tool. To use the Pi here, a human has to add the Tailscale step and
the variables to `.github/workflows/claude.yml`, since the Claude app cannot
edit workflows. The alternative is to ask for the PDF in byu-vcl, where the
Pi is already wired up.

**What is known without the PDF:**
- Z. Jia, J. Yang, R. Li, Z. Wang, C. Tan, G. Sun, E.-H. Han, *Addit.
  Manuf.* 127, 105291 (July 2026), doi:10.1016/j.addma.2026.105291
  (PII S2214860426002174). It is closed access, NSFC-funded, has 65
  references, and is not yet cited by anyone.
- The authors are at Southeast University (Guifang Sun's laser deposition
  group), Nanjing Forestry University and Soochow University.
- Crossref, OpenAlex and Semantic Scholar carry no abstract. Web search finds
  only the title, and there is no SSRN preprint.
- Edison could not open it in three separate jobs (b1-01, b2-09, b3-02).
- The same group's two earlier papers are also closed to Edison:
  - Jia et al., *Corros. Sci.* 255, 113114 (2025): further precipitate
    refinement vs strength and corrosion of laser-deposited NAB.
  - Jia et al., *J. Mater. Process. Technol.* 335, 118659 (2025):
    water-cooled laser deposition of NAB.

**What to check once the PDF is in hand.** These decide how the proposal
positions itself (b1-01, b2-09):
1. Blown powder or LPBF, and pre-alloyed powder or blended.
2. Which elements were subtracted, and how the composition was chosen
   (metallurgical reasoning, CALPHAD, or a model).
3. The corrosion medium and duration, and whether a heat-treated cast or
   wrought control was tested in the same electrolyte.
4. Whether any deposit was made on a repair substrate.

The current proposal cites it only for what its title says.

## 2. Changes made to the copper proposal in this pass

All 25 new references are in `onr-yip-technical-proposal-cu-ded.tex`, in
citation order. All were checked on Crossref except the ISSC committee report,
which has no DOI.

1. **Removed a wrong claim.** The draft said "We found no corrosion study of
   copper-nickel deposited by blown-powder laser DED." There is one:
   - Bhattacharya et al., *J. Alloys Compd.* 509, 6364 (2011) deposited
     Cu-30Ni by CO₂-laser direct metal deposition on rolled C71500.
   - A 2012 ISSC Committee V.3 report (Sec. 3.3.2) says the deposit corroded
     faster than the wrought plate and blames porosity (b1-03, b2-08, b3-01).
   - Neither source gives the electrolyte or the numbers, so a red TODO asks
     Sterling to check the 2011 article.
   - Laser cladding of Cu-30Ni dates to Adak et al. 2005.
   - `../../near-term-submissions/onr-yip/README.md` §9 now records the
     correction.
2. **Prior art for the powder route.** Ultrasonic atomizers have already made
   copper alloy powder for blown-powder DED, but only in existing
   compositions:
   - Müller et al. 2023 and Uhlmann et al. 2024 used NAB propeller grinding
     chips, on an AMAZEMET AUS 500 (not a rePOWDER). Conditions: induction at
     1300 °C, a 40 kHz carbon-fiber sonotrode, argon 5.0. Median particle size
     was 98 µm, with ~20 µm carbon fibers in the powder. All verified in the
     full text.
   - Cabrioli et al. 2025 used offshore-cable copper and printed it by laser
     DED (verified in the abstract).
3. **As-deposited vs annealed NAB.** Whether annealing helps depends on the
   starting microstructure (b3-03):
   - The same 700 °C anneal lowered the 480-hour corrosion current of cast NAB
     and raised that of sintered + HIPed NAB (Fayanas et al. 2025).
   - As-built wire-arc NAB beat its annealed forms (Shahriari et al. 2023),
     but in a test with 96 h vs 24 h pre-immersion. The text says so.
4. **Laser-deposited NAB corrosion depth.** NAB laser-deposited on 17-4PH
   stainless steel was attacked 1.8 to 3.4 µm deep in 21 days of 3.5% NaCl,
   worst where iron from the steel diluted it (Zhao et al., *Metals* 2022).
5. **Repair precedents.**
   - Laser cladding of cast NAB with an NAB consumable (Hyatt et al. 1998).
   - DED of a low-nickel CuNi2SiCr powder on cast NAB (Yao et al. 2022, two
     papers). Edison reports, via a review, that those deposits were porous
     and softer than the casting; this is not in the proposal.
   - The same group later blended in an aluminum alloy powder to vary the
     aluminum content (Yao et al. 2025).
6. **Short screens can mislead, now with numbers.**
   - Fresh 70-30 Cu-Ni in synthetic seawater: corrosion current fell 8.4× in
     10 days, 8.44 to 1.01 µA/cm² (Yuan and Pehkonen 2007).
   - Welded NAB corroded faster in natural than in simulated seawater (Dobson
     et al. 2024, *Biofouling*).
7. **Cracking indices.** Kou- and Clyne-Davies-type indices have been checked
   against printed Al, steels, Ni superalloys and HEAs, but not copper alloys
   (Jordan and Zhang 2026). This supports H3.
8. **Comparison with other approaches.** New entries, each tuning one stage
   or one alloy, not the linked chain:
   - a Ni superalloy designed by neural network for laser repair (Markanday et
     al. 2022);
   - machine-learning-refined LPBF settings for 70-30 Cu-Ni at NPS (Sparrow
     et al. 2026);
   - Bayesian optimization of a gas atomizer (Tamura et al. 2021);
   - active learning of DED-deposited multi-principal-element alloys
     (Nelaturu et al. 2024);
   - an analytical heat-flow + finite-element multi-fidelity process map
     (Menon et al. 2022);
   - 0.1% Ti added to wire-arc NAB, cutting corrosion current 16% (Zhang et
     al. 2026).
9. **Naval relevance.** ONR-funded wire-arc 70-30 work also uses the cast
   composition (Song et al. 2024, ONR N00014-21-1-2800, verified in the
   paper).
10. **Task 2 powder paragraph:**
    - Crucible TODO: no published comparison exists. Alumina or stabilized
      zirconia come first, since graphite can add carbon to Ni-bearing melts.
    - Sonotrode TODO, with a matching line in Risks: Cu wets and dissolves
      Ti-6Al-4V, and Ti-Cu eutectics form at 875 and 960 °C.
    - Lang's relation: the measured NAB median is about twice its estimate,
      so plate frequency is a search variable.
    - The "vendors quote 45-150 µm" TODO now cites peer-reviewed cuts:
      45-106 µm (Li et al. 2021) and 45-150 µm (Pi et al. 2025).
11. **H5 depth TODO.** Filled with the published 21- and 30-day depths
    (1.8-3.4 µm laser-deposited NAB, >3 µm cast NAB), and the alternative
    "no deeper than the cast NAB reference".
12. **Softened one overreach.**
    - "Fast cooling retains a martensitic phase" is now "can retain", in the
      proposal and in `abstract-cu-ded.txt`. As-built LPBF and wire-arc NAB
      have sometimes corroded less than annealed or cast NAB.
    - The abstract is 3,944 of 4,000 characters (was 3,947).

The rebuilt PDF has 15 counted pages of 20 (was 14) and 100 references (was
75). cringe-filter (proposal context) reports 0 errors, as before.

## 3. Findings by topic

### 3.1 What is new and what is not (novelty map)

Laser DED of copper alloys is not new, and neither are most single pieces of
the proposed workflow. The defensible claim is the combination (b1-01, b1-08,
b2-09, b3-09, b4-09, b5-01):

| Piece | Prior art (DOI) | Status for the proposal |
| --- | --- | --- |
| Pre-alloyed NAB powder by blown-powder laser DED | Li et al. 2021, 10.1016/j.addma.2020.101825: 45-106 µm gas-atomized Cu-9Al-5Fe-5Ni, 99.55% dense, UTS 769-949 MPa, no corrosion. Rayner et al. 2024, 10.1007/978-3-031-67398-6_13 (C63020). Hu et al. 2026, 10.1016/j.jallcom.2026.187981 (LP-DED vs LPBF) | Not new |
| Laser-deposited NAB corrosion | Zhao et al. 2022, 10.3390/met12050781 (on steel, 3.5% NaCl, 21 days). Pi et al. 2025, 10.1038/s41598-025-96674-4 (Mn-Al bronze on matching cast bronze; current 18.7% higher than cast) | Not new; as-deposited vs C71500 in seawater is |
| Blown-powder laser DED of Cu-30Ni, with corrosion | Bhattacharya et al. 2011, 10.1016/j.jallcom.2011.03.091 (worse than wrought, porosity). Adak et al. 2005 | Not new; dense, as-deposited parity is |
| Ultrasonic atomization of NAB for DED | Müller et al. 2023, 10.1088/1757-899X/1296/1/012036; Uhlmann et al. 2024, 10.3390/ma17143396 | Not new for existing alloys |
| Composition changed for AM NAB | Jia et al. 2026; Barr et al. 2022 (LPBF, two commercial grades); Zhang et al. 2026 (Ti in WAAM NAB) | Started; Jia unread |
| Repair on cast NAB | Hyatt et al. 1998 (laser clad, NAB consumable); Yao et al. 2022 (CuNi2SiCr powder DED); Pi et al. 2025 | Partial; no Ni-bearing NAB or 10-30 Ni Cu-Ni powder on both substrates with zone-resolved corrosion |
| ML on copper AM | Sparrow et al. 2026 (LPBF settings for C71500, NPS) | Process only, one alloy |
| ML/BO for DED or atomization | Menon et al. 2022; Nelaturu et al. 2024; Tamura et al. 2021; Kitt et al. 2024 | Separate stages |
| Cost-aware search over composition → powder → DED → corrosion | none found (b1-09, b5-01) | The claim |

Three Edison answers (b1-01, b2-09, b3-02) found nothing that couples CALPHAD
to a DED thermal history to choose a copper alloy composition.

### 3.2 Making copper alloy powder

- **Ultrasonic atomization of copper alloys:**
  - The closest precedent is the Berlin/MarTERA work above. Its
    gas-atomized reference was a Ni-free CuAl9.5Fe, not the same alloy (b4-09).
  - The only *rePOWDER induction* result with numbers is Al-10Cu at 1100 °C
    and 40 kHz: d10/d50/d90 = 36/65/78 µm (Ukabhai et al. 2025,
    10.1051/matecconf/202541703001). Those authors give a ~1300 °C limit for
    the induction module.
  - Ciftcli et al. 2025 (10.2497/jjspm.15E-SIS13-03) show a photo of a copper
    alloy stream on a rePOWDER, with no numbers. They also used a TZM
    sonotrode at 40 kHz, for C103.
  - Ultrasonic powder has been deposited by blown-powder DED for other alloys:
    Fe-Al (10.21741/9781644903599-28) and an Al-Ni-Ce-Mn-Fe alloy, >99% dense
    (10.1088/2631-7990/ae3349).
- **Superheat:** for 70-30 Cu-Ni, a 1300 °C furnace gives only ~60 °C above
  the 1238 °C liquidus. No published minimum superheat for drop-on-plate
  atomization exists (b2-01). This has to be tested on our unit.
- **Sonotrode** (b2-01, b4-02):
  - Ti-6Al-4V is a poor plate for copper (Li and Lin 2004 joining data).
  - Carbon fiber worked for NAB but sheds fibers.
  - TZM is a candidate, but Ni-Mo interaction is a risk for Cu-Ni.
  - SiC stays non-wetting (~137°) yet transfers Si.
  - 1 at% Cr makes Cu wet graphite, which matters for Cr-bearing Cu-Ni.
- **Crucible** (b2-02): no study compares crucibles for 0.1-1 kg Cu-Ni or NAB
  melts. Edison's suggested order is dense alumina, then stabilized zirconia,
  with graphite only if carbon is measured. Clay-graphite is rated to 1200 °C.
- **Lang's relation:**
  - My own calculation (liquid Cu at 1300 °C: σ = 1.24 N/m, ρ = 7.72 g/cm³)
    gives 73 µm at 20 kHz, 46 µm at 40 kHz, and 35 µm at 60 kHz. Edison's
    b2-01 numbers (92/63/58/44 µm) are ~25% high.
  - For NAB at 40 kHz the relation gives ~47 µm. The measured median of
    98 µm is about twice that (b4-03 agrees).
  - Expect coarser powder than the relation predicts. That suits DED, but
    20 kHz may overshoot 150 µm.
- **DED size cuts in peer-reviewed work:**
  - bronzes: 45-106 µm (Li 2021), 45-100 µm (Zhao 2022, *Chin. J. Mech.
    Eng.*), 53-120 µm (Zhao 2022, *Metals*), 45-150 µm (Pi 2025);
  - other DED work: 45-150 µm (Kiani 2024, 10.3390/powders3010003), 50-150 µm
    (Saboori 2019, 10.1016/j.msea.2019.138360).
  - No peer-reviewed vendor minimum lot size was found (b2-10). Roth et al.
    2024 ran a ~10 kg experimental gas atomization of Alloy 400 (Edison).
- **Oxygen and porosity** (b3-10): no literature-certified powder oxygen limit
  exists for copper DED. Steam (Cu₂O + H) and nitrogen both make pores.
  ERCuNi fillers carry Ti as a deoxidizer. Measure oxygen per lot, by
  inert-gas fusion.

### 3.3 Corrosion testing

- **Films take months.** Fresh 70-30's corrosion current fell 8.4× in 10 days
  (Yuan and Pehkonen 2007). Cu-Ni films mature over 2-3 months (Powell 2004,
  Edison). In flowing natural seawater, 70-30's impedance rose and fell over
  180 days (Al-Muhanna and Habib 2010, 10.1016/j.desal.2009.09.065).
- **Natural vs simulated seawater.**
  - Welded NAB pits reached 668-738 µm at weld toes in a marina vs 12 µm in
    simulated seawater, and κIII attack reached 1.33 mm at 12 months (Dobson
    thesis and 10.1016/j.corsci.2024.112004, Edison).
  - In an ASTM D1141 tank the rate was 0.06 mm/yr (Edison).
- **Selective-attack depths for H5:** 21-day laser-deposited NAB 1.8-3.4 µm
  (Zhao 2022); 30-day cast NAB >3 µm at high Al/Ni ratio (Tan et al. 2024,
  10.3390/ma17061330). No Navy or class-society numeric depth limit was found
  (b2-05).
- **Ranking agreement:** in Tan's four cast NAB alloys, 10-day electrochemistry
  ranked them the same as 30-day mass loss. Nothing published tests a
  one-hour screen against 30-day immersion for these alloys. That
  correlation is H5's contribution (b2-05, b4-06).
- **Flow:**
  - Critical velocities are ~3-4 m/s for 90-10 and >4.7 m/s for 70-30 in
    flowing NaCl (Wu et al. 2023, 10.3390/met13020401).
  - C72200 (Cu-16Ni-0.5Cr) tolerates far higher velocity, but Cr-bearing
    Cu-Ni can pit in quiet water (Lewis and LaQue 1981, 10.2172/6255887).
  - Edison suggests a 0-2 wt% Cr search range (b4-04).
- **Cavitation** as a mid-cost node for propeller repair:
  - DED and WAAM NAB cavitation papers exist: 10.1016/j.corsci.2024.111982
    and 10.1016/j.ultsonch.2025.107235 (both unread).
  - FSP NAB lost 15.9 mg vs 33.4 mg for cast in 16 h (Song 2013, Edison;
    b3-08, b5-04).

### 3.4 ICME

- **Databases:** TCCU5 covers Cu, Al, Ni, Fe, Mn, Cr and O, but no published
  validation exists for NAB κ phases or for Cu-Ni-Fe-Mn-Cr (b1-07, b3-05).
- **Kinetics, not just equilibrium:**
  - κ onsets drop with cooling rate: at 424 °C/s vs 0.1 °C/s, κII 962 vs
    1004 °C and κIII 677 vs 717 °C.
  - A 2 s vs 60 s hold at 1035 °C moves κII onset by ~20 °C.
  - Source: Kuprienko 2025, Ohio State, ONR-funded (Edison). This supports
    Advance 3 and is worth citing once checked.
- **No martensite-start equation** for NAB was found in batch 3; batch 5
  (b5-03) followed up through Cu-Al-Ni shape-memory alloys.
- **Thermal history:** reheating above the ~830 °C β solvus dissolves and
  reprecipitates κ (Dharmendra 2019).
- **Cracking:** cast 70-30 can hot crack; wrought 70-30 welds suffer porosity
  more than cracks. Single-phase Al bronze filler cracks while duplex filler
  does not (Lancaster). Crack indices are unvalidated for copper (Jordan and
  Zhang 2026).

### 3.5 Nickel-lean candidates

- **90-10 (C70600)** is the proven low-Ni benchmark in clean seawater, with a
  lower design velocity than 70-30.
- **C72200** is the strongest high-flow candidate (above).
- **Cu-7Ni-3Al-1Fe-1Mn** (cast) corroded at 0.0215 vs 0.0359 mm/yr for C70600
  in 10-day artificial seawater (Yang et al. 2018, 10.3390/ma11091777).
- **Mn-Al bronze** has been printed by laser DED (Wang et al. 2026,
  10.1002/adem.71167, unread) and laser clad (Pi et al. 2025, worse than
  cast).
- **Lowering Ni while raising Al** in NAB costs ductility and corrosion
  resistance (Tan 2024).
- **MARINEL (Cu-19Ni-4.6Mn-1.9Al)** is a naval high-strength Cu-Ni with long
  seawater data (Campbell et al. 2002, 10.5006/1.3277305).

### 3.6 Navy-funded and competing groups (b3-07, b5-02)

| Group | Funding | Process, alloy | Overlap |
| --- | --- | --- | --- |
| Virginia Tech (Fu; Song et al. 2024) | ONR N00014-21-1-2800 (verified) | CMT wire-arc 70-30 Cu-Ni corrosion | As-built beat wrought in 3 h NaCl |
| Case Western (Lewandowski; Adeeko 2026 MS thesis) | ONR (Edison) | Wire-arc 70-30 with Lincoln Electric, sample to NRL | SSRT in D1141 water |
| Ohio State (Kuprienko 2025 PhD) | ONR Manufacturing Science (Edison) | Wire-arc NAB, cooling-rate κ kinetics, cast/wrought interfaces | Thermal-history physics |
| Oregon State (Doyle 2022 MS) | Navy grant (Edison) | Wire-laser DED NAB, no corrosion | Laser DED of NAB |
| Naval Postgraduate School (Sparrow, Smith, Ansell 2026) | NPS | LPBF of mechanically made C71500 powder, ML parameter refinement | ML on Cu-Ni |
| NSWC Carderock (Orzolek, Semple, Fisher 2022; Norkett) | Navy | NAB processing, property databases | Already cited |
| Dalhousie (Bishop, Nasiri, Rayner, Morshed-Behbahani) | NSERC/CFI, DRDC partner (Edison) | DED and LPBF NAB corrosion | Canadian competitor |
| Southeast University (Sun, Jia, Han) | NSFC | Laser-deposited NAB, composition design | Closest; Jia 2026 |
| Berlin (TU Berlin/Fraunhofer IPK/BAM) | EU MarTERA | Ultrasonic NAB powder from propeller chips | Powder route |

None of these uses in-house powder for new compositions, or blown-powder DED
on both repair substrates, judged as deposited against C71500.

### 3.7 Qualification (b4-08)

- The only verified AM-specific NAVSEA route is for wire-arc DED. Its tech pub
  qualification scheme is described by Harwig et al., SAE 2024-01-3808.
- A full-size wire-arc NAB propeller has been characterized (Govindaraj 2025,
  Linnaeus University licentiate thesis).
- A university project can supply a prequalification package:
  - traceable powder lots;
  - deposits on both substrates;
  - mechanical and NDE data;
  - matched C71500 seawater tests.

  Acceptance and installation stay with the Navy.

### 3.8 Methods (b4-07, b5-09)

BO for DED process windows exists:
- multi-fidelity with an Eagar-Tsai low-fidelity model (Menon 2022);
- GP from bead to cube (de Sousa 2026);
- crack-aware graded alloys (Kitt 2024): crack-free walls did not mean
  crack-free cubes;
- active learning over DED compositions: 115 initial plus 42 acquired alloys
  (Nelaturu 2024).

None reports savings in physical corrosion experiments.

### 3.9 Batch 5: follow-ups on batch 3 and the final novelty check

- **Final novelty check (b5-01).** No verified study combines three things:
  1. a copper alloy composition search that evaluates CALPHAD along a
     modeled DED thermal history;
  2. in-house pre-alloyed powder for every candidate;
  3. as-deposited seawater tests against wrought C71500, including deposits
     on cast NAB and wrought Cu-Ni.

  Partial precedents exist:
  - CALPHAD for copper-containing DED gradients (Balkan 2021 thesis; Yang et
    al. 2024, arXiv:2407.16050, 316L to Monel 400);
  - a blended-powder Cu-Al series of 6-12 wt% Al for NAB repair (Yao et al.
    2025, 10.1016/j.addma.2025.104787). Its 12% Al alloy corroded about like
    cast NAB, per a 2026 review. Now cited in the proposal.

  Edison's suggested wording keeps the claim to the combination and says
  that Jia et al. 2026 and the other unread papers must be checked. The
  proposal's comparison section already claims only the combination.
- **Dalhousie (b5-02).** Funded by NSERC and CFI, with a DRDC partnership
  (Edison). The group has published DED of C63020 powder (2024) and a
  comparison of heat-treated L-PBF and L-DED NAB corrosion
  (Morshed-Behbahani et al., *Colloids Surf. A* 708, 136069, 2025,
  10.1016/j.colsurfa.2024.136069; results unread).
- **Martensite and "aluminium equivalent" (b5-03).**
  - Ms equations for Cu-Al-Ni shape-memory alloys (Recarte et al. 1999) err
    by up to ~98 °C even for those alloys, and are untested on NAB.
  - No aluminium-equivalent coefficients and no DED-calibrated κ kinetics
    could be verified.
  - CALPHAD β/α/κ outputs plus cooling and reheating descriptors are the
    defensible cheap inputs. Retained β′ has to be learned as a
    non-equilibrium outcome. This supports H3 as written.
- **Cavitation (b5-04).** The 2024 DED-NAB and 2025 WAAM-NAB cavitation
  papers could not be read. Cavitation remains a plausible mid-cost screen
  for propeller-repair alloys, run beside cast NAB and C71500.
- **2025-2026 NAB AM papers (b5-05).** Hu 2026, Saremi 2026, Roshan 2026,
  Yao 2025, Mahmoudiniya 2026 and Wu 2026 were found by title only. None was
  confirmed to report as-deposited corrosion numbers. Do not tabulate them
  from titles.
- **Corrosion metrology (b5-06):**
  - Do not fit Tafel slopes to a diffusion-limited cathodic branch.
  - Do not assume B = 26 mV. Report Rp and check converted rates against
    mass loss.
  - Screen in ASTM D1141 water and confirm finalists in natural seawater;
    sulfide can reverse a ranking.
- **Absorptivity and catchment (b5-07):**
  - At ~1 µm, solid copper absorbs 4-5%, a fine copper powder bed 44%, and
    untreated copper 17-22% by LPBF calorimetry.
  - The best documented copper DED building efficiency is 36%, with a blue
    laser.
  - No Cu-Ni or NAB DED absorptivity or catchment curve exists, so calibrate
    the heat-flow model on our own single tracks.
- **Point-of-need recycling (b5-08):**
  - MarTERA (NAB chips) and Cabrioli 2025 (>70% lower global-warming
    potential for recycled copper than mining) are the closest work.
  - Navy expeditionary metal AM so far is wire-arc hybrid (Strieby 2024,
    Edison). No shipboard powder making has been shown.
  - Turning shipyard scrap into DED powder fits ONR's "AM and digital
    logistics" thrust, but only as a capability still to be tested.
- **BO for long experiments (b5-09).** Closest methods:
  - two-test Bayesian screening (Hook et al. 2020, arXiv:2009.05418);
  - multi-fidelity BO with training time as the fidelity (Wu, Toscano-
    Palmerin, Frazier and Wilson 2020, arXiv:1903.04703);
  - BO with optimal stopping (Dai et al. 2019);
  - cost-sensitive freeze-thaw BO (Lee et al. 2026, arXiv:2510.21379);
  - pending-point handling in BoTorch.

  None has been applied to corrosion. See the suggestion in Section 4.
- **Cu-Ni segregation (b5-10):**
  - Cu-Ni weld metal can have 38.0 wt% Ni in dendrite cores against 16.4 wt%
    between them (Devletian 2006, Edison).
  - The ONR-funded WAAM work shows attack between dendrites (Song 2024).
  - Measure whether Fe is in solution or precipitated, and compare Scheil and
    back-diffusion predictions with measured profiles before asking them to
    predict corrosion.


## 4. Open items for Sterling

1. **Get Jia et al. 2026** through the Pi or the BYU library, and check the
   four items in Section 1.
2. **Check Bhattacharya et al. 2011** (test medium, numbers, porosity). The
   proposal carries a TODO.
3. **Atomizer, before the first copper run:**
   - the plate material, since Ti-6Al-4V and copper react;
   - the crucible;
   - the induction module's maximum melt temperature;
   - the plate frequencies available.
   - Consider 90-10 Cu-Ni or NAB first, since both melt well below 1300 °C.
4. **Alloy space:**
   - add Cr to 0-2 wt% in Cu-Ni (C72200-like);
   - consider Mn-Al bronze as the nickel-lean bronze family;
   - require duplex (α+β) phase balance in bronzes to avoid cracking.
5. **Corrosion plan:**
   - run concurrent wrought C71500 and cast NAB controls;
   - add 10- and 30-day electrochemistry on the same coupons, to test the
     screen;
   - mask separate deposit, fusion-zone and HAZ exposures on repair coupons,
     with a galvanic (ZRA) test.
6. **Possible additions:** Kuprienko 2025 (ONR-funded κ kinetics) and Hu et
   al. 2026 (DED vs LPBF NAB). Both need the full text before citing.
7. **A method idea from b5-09, not in the proposal:**
   - Read immersion coupons electrochemically at about 1, 10 and 30 days.
     Elapsed time can then enter the models as a fidelity (Wu et al. 2020),
     and the search can decide candidate by candidate whether to start or
     stop a 30-day test.
   - Tan et al. found that 10-day electrochemistry already ranked four cast
     NAB alloys like 30-day mass loss.
   - This would strengthen Advance 2 and H5.

## 5. Where Edison was wrong or inconsistent this time

- **Contradictions between jobs.** b3-02 (LITERATURE_HIGH, focused on
  2022-2026) said no one had printed Cu-Ni by blown-powder DED and no one had
  ultrasonically atomized a marine copper alloy. Both statements contradict
  b1-03, b1-04, b2-01, b2-08, b3-01 and b3-04, which found the 2011 Cu-30Ni
  work and the Berlin NAB powder. A date window in a question hides older
  prior art.
- **Arithmetic.** b2-01's Lang sizes for copper are ~25% too large (Section
  3.2).
- **Swapped numbers.** b2-01 gave 190 ppm oxygen for the ultrasonic NAB
  powder; b3-04 and b4-03 give 130 ppm, with 190 ppm for the gas-atomized
  reference. The values are in a figure that could not be read from the text,
  so neither is quoted in the proposal.
- **Equipment.** Early answers implied the NAB run was on a rePOWDER. b3-04
  found it was an AUS 500.
- **Navy documents.** Several answers said a Navy AM specification for
  wire-arc NAB or Cu-Ni could not be verified. Edison does not search
  ASSIST; MIL-PRF-32804, -32815 and -32816 were checked there on 2026-10-17.
- **Secondary reading.** Many results were read through a review (Nemani et
  al. 2024) or a later thesis (Kuprienko, Adeeko). Edison flags this, and the
  proposal does not quote those numbers.
- **Verbosity.** Standard LITERATURE jobs now return 20-50 K characters with
  tables and run ~30 minutes, about as long as LITERATURE_HIGH.

## Task IDs

All times are UTC on 2026-10-17. Raw trajectories: `raw/<name>.json.gz`.

| Name | Job | Task ID | Submitted | Fetched | Status |
| --- | --- | --- | --- | --- | --- |
| [`b1-01-closest-prior-work`](batch1/b1-01-closest-prior-work.md) | LITERATURE_HIGH | `ed902e26-fd17-4f11-8309-dc9f5c5c924d` | 05:10 | 05:42 | success |
| [`b1-02-ded-nab`](batch1/b1-02-ded-nab.md) | LITERATURE | `83c4382b-0668-473f-9f8a-ab068b3c6c91` | 05:10 | 05:42 | success |
| [`b1-03-ded-cuni`](batch1/b1-03-ded-cuni.md) | LITERATURE | `70814fb7-d0ca-4d06-8818-841e6a0154c9` | 05:10 | 05:42 | success |
| [`b1-04-cu-powder-making`](batch1/b1-04-cu-powder-making.md) | LITERATURE_HIGH | `e0a95fe6-6d76-432d-85e8-b2ce48e5ac3e` | 05:10 | 05:44 | success |
| [`b1-05-ded-powder-requirements`](batch1/b1-05-ded-powder-requirements.md) | LITERATURE | `cf5e23c9-cdbd-4ead-8d0e-bdb734f32c99` | 05:10 | 05:42 | success |
| [`b1-06-seawater-film-mechanisms`](batch1/b1-06-seawater-film-mechanisms.md) | LITERATURE | `695a9d41-f20a-4d61-ae57-92af3b1248ee` | 05:10 | 05:42 | success |
| [`b1-07-icme-calphad-cu`](batch1/b1-07-icme-calphad-cu.md) | LITERATURE | `413b4e08-3e52-4cda-b8dd-f1257c3046db` | 05:10 | 05:42 | success |
| [`b1-08-navy-needs`](batch1/b1-08-navy-needs.md) | LITERATURE | `547ec63c-d418-4e5b-a51e-19a259f65ed1` | 05:10 | 05:42 | success |
| [`b1-09-precedent-ml-cu-am`](batch1/b1-09-precedent-ml-cu-am.md) | PRECEDENT | `9a135f0a-50a2-44c7-b213-1b9dc3a8d2cb` | 05:10 | 05:42 | success |
| [`b1-10-repair-on-cast-nab`](batch1/b1-10-repair-on-cast-nab.md) | LITERATURE | `0112f9fd-a99c-45d7-9b7a-dd53c3a55555` | 05:10 | 05:42 | success |
| [`b2-01-ultrasonic-atomization-cu-melts`](batch2/b2-01-ultrasonic-atomization-cu-melts.md) | LITERATURE | `4f682962-96a3-4ab9-8128-08ceaae95e73` | 05:37 | 06:08 | success |
| [`b2-02-crucibles-melt-practice`](batch2/b2-02-crucibles-melt-practice.md) | LITERATURE | `14972c4a-bfc1-4200-a826-5dedf50fafd1` | 05:37 | 06:08 | success |
| [`b2-03-nickel-lean-seawater-alloys`](batch2/b2-03-nickel-lean-seawater-alloys.md) | LITERATURE | `c9833365-3e58-47e0-a285-58a7c69d8305` | 05:37 | 06:08 | success |
| [`b2-04-cracking-cuni-nab-welding`](batch2/b2-04-cracking-cuni-nab-welding.md) | LITERATURE | `f6ce3ed1-8e93-4230-bf0a-876adaa985dd` | 05:37 | 06:08 | success |
| [`b2-05-short-tests-vs-immersion`](batch2/b2-05-short-tests-vs-immersion.md) | LITERATURE | `14416633-6364-4823-b85e-daa613017132` | 05:37 | 06:08 | success |
| [`b2-06-heat-flow-models-cu-ded`](batch2/b2-06-heat-flow-models-cu-ded.md) | LITERATURE | `cb999416-b429-4ffb-88a3-eb0093a12c7c` | 05:37 | 06:08 | success |
| [`b2-07-ded-process-windows-cu`](batch2/b2-07-ded-process-windows-cu.md) | LITERATURE | `13cc8d3b-4e30-4dc6-bec3-efefaee291fc` | 05:37 | 06:08 | success |
| [`b2-08-precedent-cuni-ded-corrosion`](batch2/b2-08-precedent-cuni-ded-corrosion.md) | PRECEDENT | `0ff6e38c-46cf-4a70-9152-136cd0898516` | 05:37 | 06:08 | success |
| [`b2-09-precedent-as-deposited-design`](batch2/b2-09-precedent-as-deposited-design.md) | PRECEDENT | `96525e49-088d-443d-a4e8-6dfd0c280a00` | 05:37 | 06:09 | success |
| [`b2-10-commercial-cu-powders`](batch2/b2-10-commercial-cu-powders.md) | LITERATURE | `01090695-cefa-423d-b504-06ede2b4db8a` | 05:37 | 06:09 | success |
| [`b3-01-dmd-cuni-corrosion-details`](batch3/b3-01-dmd-cuni-corrosion-details.md) | LITERATURE | `925abe7b-5acf-4953-8379-f19edb1a8e9f` | 05:46 | 06:16 | success |
| [`b3-02-recent-laser-ded-nab-papers`](batch3/b3-02-recent-laser-ded-nab-papers.md) | LITERATURE_HIGH | `f1a334b2-df7e-46c3-bbf9-73d65a364256` | 05:46 | 06:16 | success |
| [`b3-03-as-built-vs-annealed-nab`](batch3/b3-03-as-built-vs-annealed-nab.md) | LITERATURE | `18dab2a5-9c9c-477b-a3a2-5856a68768aa` | 05:46 | 06:16 | success |
| [`b3-04-ultrasonic-atomized-cu-for-ded`](batch3/b3-04-ultrasonic-atomized-cu-for-ded.md) | LITERATURE | `b93c9cc9-31ad-44d3-9dbf-898b17ecd928` | 05:46 | 06:16 | success |
| [`b3-05-calphad-nab-kappa-martensite`](batch3/b3-05-calphad-nab-kappa-martensite.md) | LITERATURE | `99c12723-c37b-4550-9bd5-47d18750c625` | 05:46 | 06:16 | success |
| [`b3-06-thermal-history-phase-response`](batch3/b3-06-thermal-history-phase-response.md) | LITERATURE | `e2e87126-d111-493e-82ca-e89a442c49f3` | 05:46 | 06:16 | success |
| [`b3-07-navy-funded-cu-am-programs`](batch3/b3-07-navy-funded-cu-am-programs.md) | LITERATURE | `19d70011-c7ec-47ef-a020-16561f510d45` | 05:46 | 06:16 | success |
| [`b3-08-cavitation-erosion-am-cu`](batch3/b3-08-cavitation-erosion-am-cu.md) | LITERATURE | `61bad818-736f-47a4-9c7e-3f9b3348abdf` | 05:46 | 06:17 | success |
| [`b3-09-precedent-ni-bearing-repair`](batch3/b3-09-precedent-ni-bearing-repair.md) | PRECEDENT | `50f607e6-b432-411f-9c7b-f993baf9061c` | 05:46 | 06:17 | success |
| [`b3-10-porosity-oxygen-cu-deposits`](batch3/b3-10-porosity-oxygen-cu-deposits.md) | LITERATURE | `1c764462-13f2-4a2b-8501-9fc55b4650f2` | 05:46 | 06:17 | success |
| [`b4-01-ultrasonic-nab-powder-deposits`](batch4/b4-01-ultrasonic-nab-powder-deposits.md) | LITERATURE | `72c8d01e-68d1-441c-80d6-d38f5bdadcc6` | 06:11 | 06:41 | success |
| [`b4-02-sonotrode-and-wetting`](batch4/b4-02-sonotrode-and-wetting.md) | LITERATURE | `56cc4802-3f13-42c0-a2a9-556393227548` | 06:11 | 06:41 | success |
| [`b4-03-liquid-properties-cuni-nab`](batch4/b4-03-liquid-properties-cuni-nab.md) | LITERATURE | `ae462e78-bbfc-4fdd-b3b7-94d27225e306` | 06:11 | 06:41 | success |
| [`b4-04-chromium-modified-cuni`](batch4/b4-04-chromium-modified-cuni.md) | LITERATURE | `9864ee44-946d-4a61-a4aa-f3c82e2666b4` | 06:11 | 06:41 | success |
| [`b4-05-al-bronze-phase-and-cracking`](batch4/b4-05-al-bronze-phase-and-cracking.md) | LITERATURE | `35ff7da1-9b33-48f5-be8b-02ddcbbebba7` | 06:11 | 06:41 | success |
| [`b4-06-accelerated-corrosion-screening`](batch4/b4-06-accelerated-corrosion-screening.md) | LITERATURE | `fd7064b9-a644-42dc-9196-47550bffdeb8` | 06:11 | 06:41 | success |
| [`b4-07-bo-for-ded-process-windows`](batch4/b4-07-bo-for-ded-process-windows.md) | LITERATURE | `e2806913-5a0a-4937-a752-e79545467dab` | 06:11 | 06:41 | success |
| [`b4-08-am-qualification-marine`](batch4/b4-08-am-qualification-marine.md) | LITERATURE | `9bc6bf04-7fc3-46b1-979d-088e4c993e87` | 06:11 | 06:41 | success |
| [`b4-09-precedent-ua-powder-ded`](batch4/b4-09-precedent-ua-powder-ded.md) | PRECEDENT | `7d388cc1-e5a1-49d8-88f0-c73333c43c59` | 06:11 | 06:41 | success |
| [`b4-10-nickel-lean-am-alloys`](batch4/b4-10-nickel-lean-am-alloys.md) | LITERATURE | `4a7669c6-b815-4939-b8fa-c113c2997a04` | 06:11 | 06:41 | success |
| [`b5-01-precedent-final-novelty`](batch5/b5-01-precedent-final-novelty.md) | PRECEDENT | `5e00978c-82dc-449f-9c58-9057ee6cb816` | 06:20 | 06:51 | success |
| [`b5-02-dalhousie-nab-program`](batch5/b5-02-dalhousie-nab-program.md) | LITERATURE | `b45018d6-acf4-4651-90d6-490f52bcf3ab` | 06:20 | 06:42 | success |
| [`b5-03-martensite-start-al-bronze`](batch5/b5-03-martensite-start-al-bronze.md) | LITERATURE | `e66da3ae-694f-4411-aa47-cfd00d8633bb` | 06:20 | 06:51 | success |
| [`b5-04-cavitation-ded-waam-nab`](batch5/b5-04-cavitation-ded-waam-nab.md) | LITERATURE | `768b1c22-c6f9-4a77-9253-c3c35c417c4d` | 06:20 | 06:42 | success |
| [`b5-05-nab-am-2026-details`](batch5/b5-05-nab-am-2026-details.md) | LITERATURE | `dba9c173-6152-4a52-95ad-a0b790903889` | 06:20 | 06:42 | success |
| [`b5-06-corrosion-metrology-cu`](batch5/b5-06-corrosion-metrology-cu.md) | LITERATURE | `332a778e-556a-4651-a1b9-30c710b8332e` | 06:20 | 06:51 | success |
| [`b5-07-absorptivity-catchment-cu`](batch5/b5-07-absorptivity-catchment-cu.md) | LITERATURE | `04a840be-d0ab-4488-9e63-7a24cda84ce0` | 06:20 | 06:51 | success |
| [`b5-08-point-of-need-recycling`](batch5/b5-08-point-of-need-recycling.md) | LITERATURE | `3dc07109-89a5-41f4-a7f8-cef0e9d895c6` | 06:20 | 06:51 | success |
| [`b5-09-bo-delayed-long-experiments`](batch5/b5-09-bo-delayed-long-experiments.md) | LITERATURE | `04c29905-5680-4dc7-9348-8204ec420901` | 06:20 | 06:52 | success |
| [`b5-10-cuni-segregation-film-am`](batch5/b5-10-cuni-segregation-film-am.md) | LITERATURE | `1a8c4326-4281-450f-bdf7-31ac5fcb5a78` | 06:20 | 06:52 | success |
