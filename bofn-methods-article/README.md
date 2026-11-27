# BOFN methods write-ups (issue #121)

Two versions of the same methods work, written so that either can be used:

| Version | File | What it is | Size |
|---|---|---|---|
| **MethodsX method article** | [`methodsx/manuscript.tex`](methodsx/manuscript.tex) | A companion to the *Advanced Materials* article (issue #120), in MethodsX's Method Article template (v7, Sep 2024): specifications table, background, method details, method validation, limitations, data availability | abstract ≤ 200 words incl. 3 bullets; background ≤ 500; method details and validation ≈ 3,500; 6 figures, 4 tables |
| **Short version for the *Advanced Materials* article** | [`adv-mater/methods-si.tex`](adv-mater/methods-si.tex) | (A) one Experimental Section paragraph, (B) two optional sentences for §2.6, (C) one SI section | A ≈ 190 words; C ≈ 1,300 words, 2 figures, 2 tables |

Both read their numbers from one generated file,
[`../benchmarks/bofn-paper/paper-stats/numbers.tex`](../benchmarks/bofn-paper/paper-stats/numbers.tex),
through `\stat{key}` macros (for example `\stat{k1-su-pkgfn-tiered}` is pKGFN's speed-up over tiered
screening at κ = 1). They cannot disagree, and rerunning `make stats` after new runs updates both. A
missing key prints as a bold `??key??`.

The code, the runs and the statistics are in [`../benchmarks/bofn-paper/`](../benchmarks/bofn-paper/)
([`PORT.md`](../benchmarks/bofn-paper/PORT.md) describes the port, the reruns and KGFN; this run adds
`paper_stats.py`, `paper_figures.py`, and the κ = 0 and 0.5 runs).

## Build

```bash
make stats      # paper_stats.py + paper_figures.py (needs the pinned environment: ../benchmarks/bofn-paper/requirements.txt)
make draft      # methodsx/manuscript.pdf and adv-mater/methods-si.pdf, with line numbers, red [brackets] and notes
make clean-pdf  # the same text as a reader would see it
make refs       # rebuild references.bib from tools/refs.tsv via Crossref/arXiv, and re-check it
```

`tools/` is a copy of issue #120's reference tools, and the citation keys match
`adv-mater-article/tools/refs.tsv`, so the *Advanced Materials* text pastes in without renaming.

## How the two versions fit issue #120's article

Issue #120's draft (`claude/issue-120-20261127-1859`, `adv-mater-article/`) gives the *Advanced Materials*
article the optimizer's per-step costs, partial evaluation and the replay/acceleration factor, plus the twin
(outline §4). Its §2.6 ("When it pays off") claims "[k]× with a wrong screen, ~1× with a right one" from the
calibrated twin and the clocked benchmark (results T2–T3). Its draft Fig. 6b uses `bofn-prelim` as a
synthetic stand-in. The short version supplies the synthetic, uncalibrated part of that story and nothing
else:

| *Advanced Materials* article | Supplied here | Where |
|---|---|---|
| Experimental Section, after "Function-network model and acquisition" | "Synthetic benchmark of the optimizer" paragraph | `adv-mater/methods-si.tex` §A |
| §2.6, before the twin is calibrated | two optional sentences (spend ratio at κ = 1 and 0; the early-lead result) | §B |
| SI S12 (function-network model) and the synthetic part of S14 | model, policies, protocol, results, validation | §C |
| Fig. 6b (draft) | updated per-κ curves and speed-ups from the 16–20-seed paper set | `paper-stats/curves.csv`, `speedup.csv` |

It does not retell the loop, the atomizer, the campaign or the twin. If the MethodsX article is published
first, §C shrinks to its first paragraph, the 2 × 2 contrasts table and a citation.

## How this differs from the other BOFN work

| | This benchmark (`bofn-paper`) | `bofn-clocked` (DAL PR 297, open) | byu-vcl twin (rounds 3–5, PRs 394, 400, 405) |
|---|---|---|---|
| Question | Does choosing the step pay, in dollars? | Days and dollars to a confirmed alloy | Days from funding, with the lab's real constraints |
| Clock | none; sequential decisions | days; asynchronous, capacity-limited | hourly; people, robots, calendars |
| Noise and failures | none by default (`--noise` available) | noise; failed powders, builds and bars | simulated instruments |
| Truth | `AlloyTruth`, κ ∈ {0, 0.5, 1}, known optimum | the same truth ported to NumPy, plus corrosion | its own Al and Cu truths |
| Policies | the 2 × 2 {KG, EI per $} × {partial, full chain}, standard BO, tiered ± reuse, random | tiered, GP-BO, BOFN, a fixed pKGFN, random, two conventional baselines | heuristic, funnel, Sobol, GP-BO, BOFN, pKGFN |
| Seeds | 20 (κ = 1), 16 (κ = 0, 0.5), the same for every policy | 8–10 | 12–16 |

All three agree on the point this paper makes about pKGFN: it ties full-chain BOFN at best, and the
knowledge gradient adds little over expected improvement per dollar on this network. The clocked
benchmark's diagnosis (`pkgfn_diagnosis/` on PR 297) found the tensile-test KG exactly zero for 73 % of
scored candidates at κ = 0, which is why pKGFN prints a few powders over and over. Cite PR 297 and the
twin rounds once they are merged or public at a fixed commit (marked `[refs once public]` in the MethodsX
draft).

## MethodsX format (checked 2026-11-27)

From the Method Article template v7 (Sep 2024, `legacyfileshare.elsevier.com/promis_misc/MethodsX-Method-Article-Template.docx`)
and Elsevier's pricing and policy pages. The journal's own guide page blocked this runner, so the points
marked † are from the template and pricing files rather than the guide.

- **Title** ≤ 20 words; **keywords** ≥ 3, separated by semicolons; a **Related research article** line,
  which may be "None".
- **Abstract** ≤ 200 words, including 1–3 bullet points. **Graphical abstract** as a separate file, at
  least 1328 × 531 px (`figures/graphical-abstract.png` is 2656 × 1062).
- **Specifications table**: subject area, more specific subject area, name of the method, name and
  reference of the original method, resource availability.
- **Sections, in order:** Background (≤ 500 words), Method details, Method validation (there is no Results
  or Discussion section), Limitations, Ethics statements, CRediT author statement, Acknowledgements,
  Declaration of interests, Supplementary material, References (numbered).
- **Co-submission** with a research article works only with Elsevier journals; *Advanced Materials* is
  Wiley, so ask the MethodsX office how to cite the companion while it is under review.
- **APC** USD 1,660 †; median 77 days from receipt to acceptance in 2026 (PubMed records, not a journal
  figure). Elsevier allows preprints.

## Venue comparison

| | MethodsX | IMMI, "Tools and methods" | STAR Protocols | SoftwareX | JOSS |
|---|---|---|---|---|---|
| Fit | a customization of existing methods (BOFN, p-KGFN) with computational validation: **exact** | ICME/TMS readers, the alloy community; ≤ 8,000 words | step-by-step protocols; would need a how-to rewrite | needs evidence that others use the software | blocked until the repo has > 6 months of public history and shown research use |
| Results allowed? | under "Method validation" | yes | "Expected outcomes" | no ("Impact") | no |
| Companion to a paper under review | "Related research article" may be None; cite the Wiley manuscript as in preparation | only published or accepted works in the reference list | allowed; cite in text | if available | supported |
| Cost | USD 1,660 | free (subscription); USD 3,890 open access | USD 1,920 | USD 1,920 | free |
| Code | repository link | public repository, persistent ID for validation data | DOI before acceptance | GitHub, forked on publication | Zenodo DOI |

Digital Discovery fits the science best ("methods for Bayesian optimization" is in its scope), but it
would be a standalone paper, which is the option ruled out on Nov 27.

## Recommendation

**Publish the MethodsX companion, and keep the *Advanced Materials* SI to the short version.** Reasons:

1. **It is ready now, and the article it serves is not.** The benchmark, its runs and both drafts exist
   today; the *Advanced Materials* article needs 2027 data (campaign 2, the desktop LPBF, the calibrated
   twin) and is due early 2028. A companion submitted in early 2027 can be accepted before the *Advanced
   Materials* article is submitted and then be cited as published, which reviewers weigh more than an SI
   section.
2. **The format matches what the work is.** MethodsX publishes customizations of existing methods with
   computational validation, and puts the results under "Method validation", which is what this is: BOFN
   and p-KGFN adapted to an alloy chain with powder reuse, a screen-error knob, a full-chain KG
   counterpart, and a matched-seed protocol.
3. **It keeps the *Advanced Materials* article on its own story.** The benchmark's findings are nuanced:
   choosing the step buys an early lead but not a better final alloy; screen-then-test is the best policy
   when the screen is right; expected improvement per dollar with powder reuse is the most robust policy;
   and the knowledge gradient as implemented is competitive only when the screen is wrong. They need room to
   be stated with their caveats. Folded into the SI they either take that room or get cut to one line, and
   two of them bear on choices the *Advanced Materials* article still has to make (decisions M7, M8).
4. **It does not cost the *Advanced Materials* article its novelty.** That article's claim is the physical
   demonstration; a synthetic benchmark published first is prior validation, not a precedent.
5. **It gives the campaign paper (#277, Feb 2027) and proposals something citable** for the optimizer.

**Fold it in instead** if any of these holds: the authors do not want to pay the USD 1,660 APC; nobody can
own the companion's revision in 2027; or the *Advanced Materials* editors ask for the optimizer's
validation to be in the same article. The short version is written for that case and needs only the
renumbering noted in its header.

**If not MethodsX:** IMMI's "Tools and methods" is the better audience (TMS, ICME, alloy designers), is
free under subscription, and has an "AI-Enabled Materials Processing" call open until 31 May 2027, but it
expects more novelty than MethodsX and cannot list the companion or arXiv-only work in its references
until accepted. STAR Protocols suits a step-by-step rewrite and costs more. JOSS is an option later
(after April 2027) for a packaged version of the benchmark.

## Where it stands (Nov 27, 2026) and what blocks submission

**Done.**
- All eight policies run on the same seeds at every κ: 20 at κ = 1 and 16 at κ = 0 and 0.5.
- 252 of 252 stored runs rerun action for action on three CPU models.
- Every comparison has a matched-seed interval (`../benchmarks/bofn-paper/paper-stats/`).
- Both versions are drafted, with every number generated. The method text was fact-checked against the
  code by an independent agent, and its 21 findings are fixed.
- All 25 references are checked against Crossref and arXiv.
- PDFs: [`methodsx/manuscript.pdf`](methodsx/manuscript.pdf) (draft, with notes) and
  [`methodsx/manuscript-clean.pdf`](methodsx/manuscript-clean.pdf);
  [`adv-mater/methods-si.pdf`](adv-mater/methods-si.pdf) and
  [`adv-mater/methods-si-clean.pdf`](adv-mater/methods-si-clean.pdf).

**What still blocks submission of the MethodsX companion, and who does it.** No new experiments are needed.

| Item | Who |
|---|---|
| Decide M2 (companion or fold in), M7 and M8 (both affect issue #120's article) | Sterling |
| Author list and order, affiliations, CRediT, funding, competing interests, the AI-use statement | Sterling, with the co-authors |
| Ask the MethodsX office how to cite the companion while it is under review at a Wiley journal | Sterling |
| Read the method details against the code and rerun one cell by hand (`../benchmarks/bofn-paper/PORT.md`, last section) | a co-author who did not write it (Xavier Zaitzeff, if they are an author) |
| Cite bofn-clocked (PR 297) and the byu-vcl twin at fixed commits once they are merged or public | a Claude run, after PR 297 merges |
| Move the text into MethodsX's Word template, which is a .docx (pandoc from the LaTeX, then fix tables by hand); upload the graphical abstract as its own file | a Claude run, then a person checks it |
| Archive the code and runs with a DOI (Zenodo) at submission, not before | Sterling (the account owner) |

**Realistic date.** Late January 2027. That allows two to three weeks for the author decisions and one
internal read over the holidays, then about a week for the template, the DOI and the cover letter. The
short version needs nothing more until issue #120's article is ready to submit.

## Decisions for Sterling

| # | Decision | Default in the drafts |
|---|---|---|
| M1 | Author list and order (who ran the port, the runs, the analysis; Xavier Zaitzeff as co-author?) | placeholders |
| M2 | Companion or fold in (above) | both written |
| M3 | Licence: the repository is MIT-licensed (`LICENSE`, Vertical Cloud Lab @ BYU); confirm that covers the benchmark and its run files for the archive | MIT |
| M4 | When to reserve the archive DOI (Zenodo) | at submission, not before |
| M5 | Whether to wait for PR 297 to merge so the clocked benchmark can be cited at a fixed commit | cite when merged |
| M6 | The AI-use declaration Elsevier asks for | drafted as a bracket |
| M7 | **The live campaign's acquisition function** (issue #120's Experimental Section says partial-evaluation KG per cost). On this benchmark pKGFN as implemented fails when the screen is right; BOFN with powder reuse (EI per $) is robust across κ. Decide before the campaign's pre-registration (SI S13) | flagged in `adv-mater/methods-si.tex` |
| M8 | **§2.6's wording.** Issue #120's outline says "~1× with a right one"; its manuscript (at `2d933f8`) already allows "screening was [faster/slower]" and cites this benchmark as 3.75-fold (90 % CI 2.0–5.7). Here, and in bofn-clocked, screen-then-test *wins* when the screen is right; the matched-seed numbers are 3.8× (95 % CI 1.9–6.3; 90 % CI 2.5–5.6, `paper-stats/speedup.csv`). Pick one interval level for both articles (the drafts here use 95 %) | flagged in `adv-mater/methods-si.tex` §B |
