# *Advanced Materials* collection article (issue #120)

**Working title:** *Closing the loop from custom powder to printed part: cost-aware discovery of supply-secure
printable aluminum alloys*

**Status on 2026-11-27:**
- **What exists:** a planning draft. The manuscript has a drafted introduction, a claim for each Results subsection, an
  Experimental Section skeleton filled from the run records, an SI skeleton, 63 references checked against Crossref,
  and two draft panels drawn from data that already exist.
- **What doesn't:** none of the article's own results exist yet.
- **Target:** an *Advanced Materials* collection due early 2028. The collection itself is still unidentified; see D1.

This folder replaces the October 10 draft, which lives in `digital-alloy-lab-private` and isn't readable from the
public repo. The October plan's ideas (versions A/B, run classes, the qualified novelty sentence) are carried over and
updated with what has happened since.

## Files

| File | What it is |
|---|---|
| [`outline.md`](outline.md) | The argument: thesis, positioning and novelty sentence, the split with the campaign paper, versions A/B, section claims and word budget, risks |
| [`figure-plan.md`](figure-plan.md) | Six figures, two tables and the SI; each panel's status, what it needs, who supplies it, when |
| [`results-needed.md`](results-needed.md) | Every result by section: supplier (campaign/project), status today, owner, due date |
| [`timeline.md`](timeline.md) | Gates back from an early-2028 deadline, and what campaign 1 must log for this article |
| [`journal-format.md`](journal-format.md) | *Advanced Materials* article types, limits and required statements, with sources |
| [`manuscript.tex`](manuscript.tex) → [`manuscript.pdf`](manuscript.pdf) | The manuscript (red brackets wait on data; blue tags name the supplier) |
| [`supporting-information.tex`](supporting-information.tex) → [`.pdf`](supporting-information.pdf) | The SI skeleton |
| [`cover-letter.md`](cover-letter.md) | Cover letter skeleton (not to be sent; nothing has been submitted) |
| [`campaign2-preregistration.md`](campaign2-preregistration.md) | Draft pre-registration for the 2027 campaign: target, baselines, stopping rule, twin analysis; to be committed before its first decision |
| [`templates/`](templates/) | `step-log.csv`: the bench log of time and consumables per step that Table 1 and Fig. 1b are built from |
| [`references.bib`](references.bib), [`reference-check.md`](reference-check.md) | Bibliography built from Crossref/arXiv records, and the check of every entry |
| `figures/` | `fig1-loop.tikz` (draft schematic), `figS-atomizer-runs` (every run so far), `fig6-draft-synthetic` (layout draft from the synthetic benchmark) |
| `data/` | Inputs of the draft figures, pinned to their source commits |
| `tools/` | `build_bib.py`, `check_refs.py`, `make_figures.py`, `refs.tsv` |

**Build:** `make draft` builds the manuscript and SI. `make clean-pdf` builds the same text with the markers hidden.
`make refs` rebuilds and re-checks the bibliography, and `make figs` redraws the draft panels. You need TeX Live
with biblatex-chem, biber and latexmk, plus Python with requests and matplotlib.

## Where it stands

1. **The article's own data don't exist yet.**
   - The atomizer has made 2 usable lots in 10 runs (Oct 2 to Nov 13), both C63000 bronze. No Al powder has been weighed.
   - Block A, the repeatability runs that Fig. 2 rests on, was scheduled for Nov 17–24. It hasn't run: the
     collection cup failed on Nov 13 (#269).
   - The desktop LPBF is a design with fast-track options; nothing is ordered (#260, PRs #266, #294).
   - The optimizer exists only in synthetic benchmarks. The twin exists, but isn't fitted to any lab measurement
     (audit, PR #293).
2. **There are three papers.**
   - The campaign paper (#277, due Feb 28, 2027) takes campaign 1's alloys.
   - The BOFN methods paper (#121, drafting started today) takes the synthetic benchmarks.
   - This article takes atomization as a method, the cost-aware optimizer and step costs, the desktop LPBF, the twin,
     and a second campaign in 2027.
   - The #277 session proposed this split independently; [`outline.md`](outline.md) §4 adopts it.
3. **The novelty claim has a clear test.** The optimizer must be seen choosing among costed steps on a physical alloy
   workflow (Fig. 5a). Ultrasonic atomization of a custom Al alloy, and the composition-to-property route, are
   already in *Advanced Materials* (Taheri-Mousavi et al., 2026).
4. **The synthetic evidence supports a narrower claim than "10×".**
   - In `bofn-prelim`, cost-aware network BO beats screen-then-test only when the screen is wrong: 3.75× less spend
     (90 % CI 2.0–5.7) at κ = 1. When the screen is right (κ = 0), it loses to screening.
   - It doesn't beat full-chain network BO or standard BO at $100k.
   - The clocked benchmark (PR #297) found the automated lab 2.5–2.9× faster at 2.2–2.5× the money.
   - The article's claim is therefore conditional: the gain appears when the screen is wrong, and the twin maps
     where that happens.

## Decisions for Sterling

| # | Decision | Why it matters now |
|---|---|---|
| **D1** | **Which collection, its exact deadline, and the article type.** #256's schedule took Feb 28, 2027 to be this article; the Oct 23 note on #160 says "late February" with no year; this thread says early 2028. | If the collection actually closes in Feb 2027, this plan folds into the campaign paper |
| D2 | Adopt the split with the campaign paper ([`outline.md`](outline.md) §4)? | Duplicate-publication risk; who owns Blocks A/B |
| D3 | Commit to a second, optimizer-driven campaign in Jul–Oct 2027, with version A/B decided at G-A3 (Sep 30, 2027)? | Version A needs it; nobody has planned it yet |
| D4 | Authors, order, CRediT roles | Placeholders by role in the manuscript |
| D5 | Does CALIBER get its own paper first? | Who owns the EDS calibration (Fig. 3e) |
| D6 | Corrosion in this article, the campaign paper, or separately? (also asked in `alloy-corrosion/README.md`) | SI S16 and a methods paragraph |
| D7 | Desktop LPBF: build (FT-1, FT-1V or the full design) or buy, and who orders when | The critical path for version A: first coupons ~1–2.5 months after the order, plus laser-safety and EHS approval |
| D8 | Funding and a lab for outside ICP-OES, O/N/H and tensile | Fig. 3, Fig. 5d, independent verification |
| D9 | The mineral-burden metric: the campaign paper's B = Σ wᵢ·NIRᵢ, and which USGS edition | Defined four ways in the FLAIME proposal; computed for nothing yet |
| D10 | Freeze the design space: Si in or out (EDS limit raised at the kickoff), and order Zr feedstock (5 of the 9 proposed seeds need it; not on the order) | The seeds and the screen depend on it |
| D11 | Where data and code are deposited (e.g. Zenodo, with DOIs reserved only at submission) | The Data Availability Statement |
| D12 | CLAUDE.md bars naming staff of partner companies "or at national labs". This folder withholds the author lists of cited papers by AMAZEMET and Thermo-Calc staff, but lists national-lab authors of published papers as ordinary citations. OK? | The bibliography is in a public repo |

## What blocks submission, and who has to do it

| Item | Who | By | Notes |
|---|---|---|---|
| D1–D12 above | **Sterling** | D1, D2, D7 by Dec 18, 2026; the rest by Mar 2027 | D7 is on the critical path |
| Fix or replace the collection cup (#269); then Block A, ≥ 5 valid runs with full run records, two splits each | **Gage, Ronnie** | Mar 31, 2027 | The most important single dataset; it needs Mo plates, the 45 µm sieve and one lot of 6063 |
| Bench logs of time and consumables for every step, from now on (L1–L2) | **everyone at a station**, compiled by Gage | ongoing | This is Fig. 1 and Table 1, and it costs nothing if logged at the bench |
| Block B composition spread, with EDS per particle and ICP | **Gage** (runs), **Ronnie** (EDS), **Sterling** (ICP) | Jun 2027 | |
| EDS against ICP calibration for Si-free and Si-bearing alloys (CALIBER) | **Ronnie** | Jun 2027 | |
| Desktop LPBF built, commissioned and printing dense Al cubes | **Carl**, after Sterling's D7 | May 2027 for version A | |
| Utah MIDI sessions on shared powders (reference builds) | **Carl** | Sep 2027 | Find out whether Utah has the Ø55 mm kit (~30 g a build, against ~440 g) |
| Live optimizer: costs, failure handling, seeding, a non-flat acquisition, pre-registration | **Xavier, Sterling** (with Claude runs) | Jun 2027 | |
| Mineral burden for every alloy (B4) | **Xavier** or a Claude run | Mar 2027 | |
| Campaign 2 (~25–35 atomizer runs; prints; hardness, density; tensile on finalists) | **whole team** (new experiments) | Jul–Oct 2027 | |
| Twin refit to lab records; counterfactual benchmarks; validation against campaign 2 | **Sterling** (with Claude runs) | Apr 2027, then Dec 2027 | |
| Outside composition and tensile on finalists | **Sterling** (vendor), **Carl** (specimens) | Dec 2027 | |
| Cups and bar for the charges | **Paul** | ongoing | |
| Corrosion panel, if D6 keeps it | **Ben, Jarrett** | Oct 2027 | |
| Drafting, figure scripts, reference and precedent checks | Claude runs, on request | as data lands | Re-run the precedent scan in Oct 2027 and Jan 2028 |

## Realistic submission date

**Tuesday, Feb 15, 2028**, about two weeks before a late-February deadline, if D1 confirms that deadline:
- **Version B by then: likely.** It needs Block A by the end of March 2027, Block B and the step-cost logs.
- **Version A by then: possible, not yet likely.** It needs the desktop LPBF ordered by January 2027 and printing Al by
  May, a second campaign in July–October 2027, and an optimizer that makes real step choices on lab data.
- **If any of those slips past about August 2027,** version A moves to mid-2028 and would likely miss the collection.
  The options then are version B for the collection, or version A as a regular submission.

## Data and code availability (plan)

The run records, powder and print measurements, campaign decision logs and step-cost logs would be deposited with a
DOI. So would the code for the optimizer, the twin and every figure (this folder, the optimizer code and the byu-vcl
twin, archived at the submitted commit). The DOIs would be reserved at submission and published at acceptance or when
the preprint goes up. Nothing has been deposited or published. The draft statement is in `manuscript.tex`, and the
journal's requirements are in [`journal-format.md`](journal-format.md).
