# *Advanced Materials* collection article (issue #120)

**Working title:** *Closing the Loop from Custom Powder to Printed Part: Cost-Aware Discovery of Supply-Secure
Printable Aluminum Alloys* ("supply-secure" depends on D9)

**Status on 2026-11-27:**
- **What exists:** a planning draft. The manuscript has a drafted introduction, a claim for each Results subsection, an
  Experimental Section skeleton filled from the run records, an SI skeleton, 75 references (68 checked against Crossref or arXiv, 7 vendor data sheets checked by hand),
  and four draft panels drawn from data that already exist (Fig. 1a, Fig. 5c's frame, Fig. 6b's layout, Figure S1).
- **What doesn't:** none of the article's own results exist yet.
- **Target:** an *Advanced Materials* collection due early 2028, as a Research Article (typically 3,000–8,000 words in all,
  3–8 display items). The collection itself is still unidentified: no public call matches, so it is presumably by
  invitation (D1). Format and limits are in [`journal-format.md`](journal-format.md).

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
| `figures/` | `fig1a-draft-network-photos` (the loop with lab photographs, from #284), `fig1-loop.tikz` (schematic alternative), `fig5c-draft-benchmarks` (yield strength against mineral burden), `fig6-draft-synthetic` (layout from the synthetic benchmark), `figS-atomizer-runs` (every run so far) |
| `data/` | Inputs of the draft figures, pinned to their source commits |
| `tools/` | `build_bib.py`, `check_refs.py`, `make_figures.py`, `refs.tsv`; `atomizer_analysis.py` (Fig. 2, Fig. 3b and the repeatability check from the per-run YAML records: `make atomizer RUNS='<glob>'`, or `--selftest`); `mineral_burden_check.py` (burden ranges for D9) |

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
2. **There are several papers.**
   - The campaign paper (#277, due Feb 28, 2027) takes campaign 1's alloys.
   - The BOFN methods paper (#121, drafting started today) takes the synthetic benchmarks.
   - The powder-doser papers (in vertical-cloud-lab/powder-doser) take dosing accuracy.
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
5. **Campaign 2 is measured against industry Sc-free alloys printed here (D0, decided Nov 27).** EOS Al5X1
   (Al–Mg–Zr–Mn) and Höganäs Al-HS1 (Al–Mn–Cr–Zr), at least one, are bought as powder and printed, aged and tested
   in the same builds as the candidates. They are the points on the front campaign 2 has to expand, and their
   in-house values against their data sheets show whether the lab measures on a par with industry. The campaign
   paper (#277) adds the same baselines and owns their sourcing and first measurement. Its run recommends buying
   Al5X1 first (quotes in the week of Nov 30, a PO by Dec 11), which would give aged Al5X1 tensile results between
   late January and mid-February 2027.
   - Data sheets, directly aged: Al5X1 385 MPa, Al-HS1 370 MPa yield (horizontal). Checked against the vendors'
     documents on Nov 27.
   - Under the campaign paper's burden metric (B_NIR, MCS 2026), Al5X1 is both stronger and lower in burden
     (3.1–4.2 wt %) than Al-HS1 (5.4–5.6 wt %), so on data-sheet values Al5X1 alone sets the front (draft Fig. 5c).
6. **The mineral-burden metric needs deciding (D9).** With MCS 2026 inputs, the Al–Mn–Cr–Zr seed S1 scores above
   Scalmalloy (6.6–7.3 against 4.7–6.0 wt %), while Zr-refined Al–Mg and Al–Fe seeds score below it. B_NIR counts
   Mg like Sc, so any alloy with less Mg than Scalmalloy's 4.7 wt % beats it on burden. That is why the claim is now
   about the Sc-free front, not about Scalmalloy.

## Decisions for Sterling

| # | Decision | Why it matters now |
|---|---|---|
| D0 | **Decided (Sterling, Nov 27):** campaign 2 is measured against the industry Sc-free alloys EOS Al5X1 and Höganäs Al-HS1 (at least one), printed, aged and tested in-house the same way as the candidates. They are points on the front campaign 2 tries to expand, with a parity check against their data sheets. This replaces the in-house "reference alloy" of the first revision | [`outline.md`](outline.md) §5, [`campaign2-preregistration.md`](campaign2-preregistration.md), Fig. 5c, Table 2; consistent with #277 |
| **D0a** | **One baseline or both, and which first.** The campaign paper's run recommends **Al5X1 first, Al-HS1 if the budget allows**, and asks whether to add Aheadd CP1 for the low-burden end. Neither vendor publishes a price, lead time or minimum order; quote requests are drafted there, not sent (`al-campaign-paper/baselines.md` on `claude/issue-277-20261127-2117`) | Under B_NIR, Al5X1's data sheet is stronger and lower in burden than Al-HS1's, so Al5X1 alone sets the front. Al-HS1 is the same-family comparator for the Al–Mn–Cr–Zr seeds. Same answer here: Al5X1 for the front claim, Al-HS1 if campaign 2 stays in Mn–Cr–Zr. The PO date sets when the first results exist (by Dec 11 for results before the campaign paper's freeze) |
| **D0b** | **The rule for "stronger", and n** (with #277) | With the April bars' 5.7 % scatter, the draft rule (non-overlapping 95 % CIs) needs ≈ 110 MPa over Al5X1 at n = 3, or ≈ 55 MPa at n = 5. A Welch test on the difference needs ≈ 50 or ≈ 32 MPa. Recommended: Welch, n = 5 for baselines and finalists in campaign 2 (the campaign paper plans 3 per condition). Also decide the parity threshold (the campaign paper proposes in-house yield ≥ 90 % of the data sheet's) and the elongation floor |
| **D1** | **Which collection, its exact deadline, and the article type.** #256's schedule took Feb 28, 2027 to be this article; the Oct 23 note on #160 says "late February" with no year; this thread says early 2028. No public *Advanced Materials* call matches: its collections are invited (Rising Stars, topical issues such as 2024's "Advanced Materials for Additive Manufacturing", institution issues), so the invitation letter is the source ([`journal-format.md`](journal-format.md)) | If the collection actually closes in Feb 2027, this plan folds into the campaign paper. If it's Rising Stars, the article must be "conceptualized and supervised" by the early-career PI |
| D2 | Adopt the split with the campaign paper ([`outline.md`](outline.md) §4)? | Duplicate-publication risk; who owns Blocks A/B |
| D3 | Commit to a second, optimizer-driven campaign in Jul–Oct 2027, with version A/B decided at G-A3 (Sep 30, 2027)? | Version A needs it; nobody has planned it yet |
| D4 | Authors, order, CRediT roles | Placeholders by role in the manuscript |
| D5 | Does CALIBER get its own paper first? (The powder-doser repo already has two papers in draft; this article cites them for dosing.) | Who owns the EDS calibration (Fig. 3e) |
| D6 | Corrosion in this article, the campaign paper, or separately? (also asked in `alloy-corrosion/README.md`) | SI S16 and a methods paragraph |
| D7 | Desktop LPBF: build (FT-1, FT-1V or the full design) or buy, and who orders when | The critical path for version A: first coupons ~1–2.5 months after the order, plus laser-safety and EHS approval |
| D8 | Funding and a lab for outside ICP-OES, O/N/H and tensile | Fig. 3, Fig. 5d, independent verification |
| D9 | The mineral-burden metric, frozen together with the campaign paper before its screen ranks anything: its proposed B_NIR = Σ wᵢ·NIRᵢ with MCS 2026 inputs, or an alternative | **Issue to fix: B_NIR counts Mg like Sc.** Scalmalloy's B (4.7–6.0 wt %) is mostly its 4.7 wt % Mg, so any lower-Mg alloy beats it; Al5X1 does (3.1–4.2). Seed S1 (Al–4.8Mn–0.9Cr–1.1Zr–1.2Mg, the FLAIME focus family) scores *higher* than Scalmalloy (6.6–7.3), because Mn is 100 % imported and used at ~5 wt %, and Al-HS1 overlaps it (5.4–5.6). Zr is <25 % imported, so Zr-refined Al–Mg and Al–Fe alloys score lower (`tools/mineral_burden_check.py`, now on the campaign paper's inputs). Comparing against the Sc-free front takes Scalmalloy out of the claim, but the Mg-against-Mn weighting still ranks the baselines. Also, the FLAIME abstract's "100 % of zirconium mineral concentrates" doesn't match MCS 2025 or 2026 (<25 %) |
| D10 | Freeze the design space: Si in or out (EDS limit raised at the kickoff), and order Zr feedstock (5 of the 9 proposed seeds need it; not on the order) | The seeds and the screen depend on it |
| D11 | Where data and code are deposited (e.g. Zenodo, with DOIs reserved only at submission) | The Data Availability Statement |
| D12 | CLAUDE.md bars naming staff of partner companies "or at national labs". This folder withholds the author lists of cited papers by AMAZEMET and Thermo-Calc staff, but lists national-lab authors of published papers as ordinary citations. OK? | The bibliography is in a public repo |

## What blocks submission, and who has to do it

| Item | Who | By | Notes |
|---|---|---|---|
| D0a–D12 above | **Sterling** | D0a, D0b with the campaign paper's freeze (its draft says Dec 1); D1, D2, D7 by Dec 18, 2026; the rest by Mar 2027 | D7 is on the critical path |
| Fix or replace the collection cup (#269); then Block A, ≥ 5 valid runs with full run records, two splits each | **Gage, Ronnie** | Mar 31, 2027 | The most important single dataset; it needs Mo plates, the 45 µm sieve and one lot of 6063 |
| Bench logs of time and consumables for every step, from now on (L1–L2) | **everyone at a station**, compiled by Gage | ongoing | This is Fig. 1 and Table 1, and it costs nothing if logged at the bench |
| Block B composition spread, with EDS per particle and ICP | **Gage** (runs), **Ronnie** (EDS), **Sterling** (ICP) | Jun 2027 | |
| EDS against ICP calibration for Si-free and Si-bearing alloys (CALIBER) | **Ronnie** | Jun 2027 | Only 1 of 17 standards-based EDS runs is valid so far |
| An ICP route that dissolves Si (HF digest, or an outside lab), and an outside lab for O/N/H (BYU has no analyser) | **Sterling** (safety, vendor, funding), **Ronnie** | Mar 2027 | Without it, Si-bearing alloys can't be shown composition-faithful; the fallback is a Si-free design space (D10) |
| Desktop LPBF built, commissioned and printing dense Al cubes | **Carl**, after Sterling's D7 | May 2027 for version A | |
| Utah MIDI sessions on shared powders (reference builds) | **Carl** | Sep 2027 | Find out whether Utah has the Ø55 mm kit (~30 g a build, against ~440 g) |
| Industry baselines (B6, B8): buy Al5X1 (and Al-HS1 if the budget allows); print, age and tensile-test them with the candidates; ICP of each lot; parity check against the data sheets | **Gage** (quote requests, week of Nov 30), **Sterling** (PO by Dec 11, D0a), **Carl** (Utah builds, tensile), as planned in the campaign paper's run (#277) | first results late Jan to mid-Feb 2027 (campaign paper); reprinted in every campaign 2 build (Jul–Oct 2027) | A baseline below the parity threshold is explained before campaign 2's first decision; machined bars separate surface from process |
| Live optimizer: costs, failure handling, seeding, a non-flat acquisition, pre-registration | **Xavier, Sterling** (with Claude runs) | Jun 2027 | |
| Mineral burden for every alloy (B4) | **Xavier** or a Claude run | Mar 2027 | |
| Campaign 2 (~25–35 atomizer runs; prints; hardness, density; tensile on finalists) | **whole team** (new experiments) | Jul–Oct 2027 | |
| Twin refit to lab records; counterfactual benchmarks; validation against campaign 2 | **Sterling** (with Claude runs) | Apr 2027, then Dec 2027 | |
| Outside composition and tensile on finalists | **Sterling** (vendor), **Carl** (specimens) | Dec 2027 | |
| Cups and bar for the charges | **Paul** | ongoing | |
| Corrosion panel, if D6 keeps it | **Ben, Jarrett** | Oct 2027 | |
| Submission package: the ML checklist (required for ML studies), cover-letter disclosure of the related manuscripts (#277, #121, the doser papers), every composition disclosed (incl. commercial powders), TOC image (55 × 50 mm, not AI-made), suggested reviewers, COI, OA decision (APC USD 6,250) | **Sterling** (Claude runs can draft) | Jan 2028 | Requirements in [`journal-format.md`](journal-format.md) |
| Drafting, figure scripts, reference and precedent checks | Claude runs, on request | as data lands | Re-run the precedent scan in Oct 2027 and Jan 2028 |

## Realistic submission date

**Tuesday, Feb 15, 2028**, about two weeks before a late-February deadline, if D1 confirms that deadline and only
if version A holds up:
- **For *Advanced Materials*, aim for version A.** Version B (the platform and a replay of the optimizer) has no
  new alloy, so it fits *npj Computational Materials*, *Digital Discovery* or *Additive Manufacturing* better, and
  it can be ready by **Jul 2027** if Block A runs by the end of March.
- **Version A by Feb 2028: possible, not yet likely.** It needs:
  - the desktop LPBF ordered by January 2027 and printing Al by May;
  - the industry baselines (Al5X1 and/or Al-HS1) printed and tested here, first by the campaign paper and again in
    campaign 2's builds;
  - campaign 2 in July–October;
  - an optimizer that makes audited step choices on lab data;
  - an alloy beyond the in-house front of those baselines (stronger, or lower in burden).
- **If the desktop LPBF or campaign 2 slips past about August 2027,** version A moves to mid-2028 and misses the
  collection. Submit it as a regular article, and send version B elsewhere.
- **If the collection actually closes in Feb 2027,** this plan folds into the campaign paper.

## Data and code availability (plan)

The run records, powder and print measurements, campaign decision logs and step-cost logs would be deposited with a
DOI. So would the code for the optimizer, the twin and every figure (this folder, the optimizer code and the byu-vcl
twin, archived at the submitted commit). The DOIs would be reserved at submission and published at acceptance or when
the preprint goes up. Nothing has been deposited or published. The draft statement is in `manuscript.tex`, and the
journal's requirements are in [`journal-format.md`](journal-format.md).
