# Al alloy campaign paper (due Feb 28, 2027)

The paper for the alloy discovery campaign in
[#277](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/277). It is meant to report an aluminum alloy for
laser powder bed fusion (LPBF) that is stronger than AlSi10Mg and uses less critical minerals than Scalmalloy, from
36 Al atomizer runs over three months
([schedule, #256](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md)).
It is written so that the campaign fills it in as it runs: every figure, table and campaign number is drawn from
[`data/`](data/) by one script, and anything still missing shows as a red placeholder with its due date.

**Current draft:** [`manuscript/main.pdf`](manuscript/main.pdf) (25 pages, with line numbers and notes) and
[`manuscript/si.pdf`](manuscript/si.pdf).

## Where it stands (2026-11-27)

| Part | State |
|---|---|
| Outline and argument | Written ([`outline.md`](outline.md)): versions A (new alloy) and B (benchmarked screen), one claim per section, the split with the *Adv. Mater.* article (#120) |
| Introduction | Drafted; citations checked against Crossref |
| Methods | Drafted for every step: CALPHAD screen, burden metric, charges, ultrasonic atomization, powder, LPBF, heat treatment, density and hardness, tensile, corrosion, independent verification, statistics, provenance. The brackets are values to read off the SOP, the run records and the instruments |
| Benchmark comparison (§4) | Drafted with real data: vendor datasheets (PR #285), AlSi10Mg printed at Utah in April 2026 (PR #288), Sc-free commercial and published alloys, and the critical-mineral burden of all of them |
| Results (§3), abstract, conclusions | Placeholders tied to the figure plan; no Al campaign run has happened yet |
| Figures and tables | Fig. 1 (benchmark map) and Fig. 5c are drawn from data; Figs. 2-4, 6 are placeholders that say what they need and when ([`figure-status.md`](figure-status.md)) |
| SI | Skeleton, with the burden inputs (S3) and the Sc-free comparators drawn from data |
| References | 63 entries, all cited. All 47 with a DOI match Crossref or DataCite on title, year and first author ([`manuscript/refs-check.csv`](manuscript/refs-check.csv)). The 16 without a DOI (vendor datasheets, the USGS scandium chapter, the critical minerals list, NASA-STD-6030, two ISO standards, Eagar-Tsai) are listed there for a hand check |
| Target journal | [`journals.md`](journals.md): *Additive Manufacturing Letters* for version A (about 5,000 words, decision within about 4 weeks), *Additive Manufacturing* for version B (5,000-13,000 words, no preprint before submission). Next choices: *MRL* or *Scripta* for A, *Materials & Design* for B |
| Cover letter | Stub in [`cover-letter.md`](cover-letter.md); not worth drafting until G4 |

**What stands in the way** is in [`risks.md`](risks.md). The two decisions that shape the paper are what counts as
new (Sc-free alloys stronger than AlSi10Mg already exist) and which burden metric the claim uses (on import-weighted
mass, AlSi10Mg scores above Scalmalloy). The data risks start with the atomizer, which has made no Al powder yet and
has been down since Nov 13.

## How to use it

```bash
pip install matplotlib pandas numpy requests
python al-campaign-paper/scripts/make_figures.py   # redraw figures, tables, numbers; writes figure-status.md
cd al-campaign-paper/manuscript
make            # main.pdf (draft: notes, line numbers, red placeholders)
make si         # si.pdf
make refs       # check every reference against Crossref / DataCite
```

- **Add data:** append rows to the CSVs in [`data/`](data/) (one row per measurement, with its source; see
  [`data/README.md`](data/README.md)), then re-run the script. Nothing in the manuscript should be typed in by hand if
  a CSV can hold it: the numbers in the text are `\newcommand`s in `manuscript/generated/numbers.tex`.
- **Change a date or an owner:** edit [`figure-plan.csv`](figure-plan.csv); `figure-status.md` follows.
- **Placeholders** are `\placeholder{...}` and stay red in every build, so a draft can't go out with one left in.
  Notes are `\note{...}` and disappear in `make clean-pdf`.

## Files

| File | What |
|---|---|
| [`outline.md`](outline.md) | The argument, versions A/B, the two definitions to freeze, section claims and word budgets, the split with #120, authors to confirm |
| [`risks.md`](risks.md) | What makes the main claim hard by Feb 28: two decisions and twelve data risks, with evidence, owners and dates; versions A, B and C |
| [`journals.md`](journals.md) | Target journals with their formats, limits and timelines |
| [`figure-plan.csv`](figure-plan.csv), [`figure-status.md`](figure-status.md) | Every figure, table and SI item: data needed, file, gate, draft and final dates, owner, and what is drawn now |
| [`manuscript/main.tex`](manuscript/main.tex) | The paper (Elsevier `elsarticle`, numbered references) |
| [`manuscript/si.tex`](manuscript/si.tex) | Supporting information |
| [`manuscript/references.bib`](manuscript/references.bib) | References, built from DOI metadata |
| [`data/`](data/) | The campaign's data, one CSV per measurement type, plus burden inputs and comparators |
| [`scripts/make_figures.py`](scripts/make_figures.py) | Figures, tables and in-text numbers from `data/` |
| [`scripts/mineral_burden.py`](scripts/mineral_burden.py) | Critical-mineral burden: import-weighted (as an interval) and cost-weighted |
| [`scripts/check_refs.py`](scripts/check_refs.py) | Reference check against Crossref and DataCite |
| [`scripts/test_make_figures.py`](scripts/test_make_figures.py) | Runs the figure script on synthetic data in a temporary folder, so the code that draws real campaign data is tested before that data exists |
| [`cover-letter.md`](cover-letter.md) | Cover letter stub |

## Not done here

- Nothing was submitted, e-mailed, deposited or posted. No Zenodo record or preprint was made.
- No lab, facility or company was contacted.
- `literature/al-lpbf-benchmark-alloys/` comes from PR #285, which is merged into this branch so the paper can read it.
  Merge #285 first.
