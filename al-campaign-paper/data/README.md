# Campaign data behind the paper

Every number in the paper's figures, tables and text comes from a CSV in this folder.
[`../scripts/make_figures.py`](../scripts/make_figures.py) redraws everything from them. Add rows as the campaign
runs and re-run it (Fridays, after the SEM session, per the
[#256 schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#what-has-to-happen-every-week-besides-the-runs)).

```bash
pip install matplotlib pandas numpy        # once
python al-campaign-paper/scripts/make_figures.py
cd al-campaign-paper/manuscript && make    # main.pdf; make si for si.pdf
```

**Rules:**
- **One row per thing measured,** never a mean. The script does the statistics.
- **Every row has a `source`:** the issue comment, file or commit that holds the raw data.
- **Failed and invalid results stay in,** with `valid` = `no` (tensile, corrosion) or a note. The paper reports them.
- **Use the same IDs everywhere:** `alloy_id` from `alloys.csv`, `run_id` from the run table, and `build_id` and
  `specimen_id` as the build sheet names them.
- **This repo is public.** Put no partner prices or quotes, staff names or private links in any column.

## Files

| File | One row per | Filled by | When | Feeds |
|---|---|---|---|---|
| [`alloys.csv`](alloys.csv) | alloy (benchmarks, seeds, optimizer picks, finalists): target composition in wt % | Xavier (targets), Gage (as charged) | when a composition is picked | Table 1, burden, Fig. 1b |
| [`runs.csv`](runs.csv) | Al campaign atomizer run, mapped to its `alloy_id`. The lab's canonical run table is [`atomizer-runs/runs.csv`](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/286); this file only adds the alloy mapping | Gage | run day | SI S1, `\NAlRuns` |
| [`powder.csv`](powder.csv) | sieved lot: mass per cut, D10/D50/D90, shape, oxygen | Ronnie | within 48 h; SEM on Thursdays | Fig. 3, SI S4 |
| [`composition.csv`](composition.csv) | element measured on a powder or part (EDS in-house, ICP-OES/spark-OES/IGF outside), long format | Ronnie (EDS), Sterling (outside reports) | weekly; outside batches Jan 8 and Jan 29 | Fig. 3c, Table 1, Table 3 |
| [`prints.csv`](prints.csv) | build: site, machine, date, lots and laser parameters | Carl | each session | SI S5 |
| [`density.csv`](density.csv) | cube: parameters, Archimedes density, cracks | Carl | week after each session | Fig. 4 |
| [`hardness.csv`](hardness.csv) | specimen and condition: HV mean, SD, n | Carl | week after each session | Fig. 5a, optimizer |
| [`tensile.csv`](tensile.csv) | tensile specimen: geometry, surface, condition, YS/UTS/EL, valid | Carl | Feb 9-12 for the finalists | Fig. 1, Fig. 5, Table 2 |
| [`corrosion.csv`](corrosion.csv) | polarization test: OCP, Ecorr, icorr, Epit, valid | Ben, Jarrett | from Jan 15 | Fig. 6, Table 2 |
| [`calphad_screen.csv`](calphad_screen.csv) | screened composition: freezing range, crack index, strengthening phases, burden, picked as | Xavier | by G1 (Dec 4) | Fig. 2, SI S2 |
| [`element-criticality.csv`](element-criticality.csv) | element: on the 2025 list, U.S. net import reliance, price, source | Sterling (check) | frozen at G1 | burden metrics, SI S3 |
| [`literature-alloys.csv`](literature-alloys.csv) | Sc-free comparator alloy and condition, from a datasheet or paper | anyone, with the source | before submission (re-check every row) | Fig. 1, SI S3 |

## What is in the files now

- **`tensile.csv`:** the five room-temperature tests of commercial AlSi10Mg printed at the University of Utah in April
  2026, copied from [PR #288](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/9ae2c34/preliminary-data/tensile-alsi10mg-utah/results.csv)
  (test 4 broke in the grip, so `valid` = `no`). These are the current in-house comparator. Their caveats are in
  the `note` column.
- **`alloys.csv`:** AlSi10Mg and Scalmalloy at the midpoints of their datasheet composition ranges, and the nine #275
  seeds at their planned melt compositions (role `planned seed`). The seeds aren't approved or made yet.
- **`element-criticality.csv`:** inputs from USGS *Mineral Commodity Summaries 2026* and the final 2025 U.S. List of
  Critical Minerals, collected 2026-11-27. Where USGS gives only a bound, both ends are entered.
- **`literature-alloys.csv`:** Sc-free comparators read by the
  [#275 survey](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-275-20261126-0632/bofn-seeding/first-six/research/datasheets.md)
  on 2026-11-26. Several values were cross-checked against vendor sheets on 2026-11-27 (A20X, Aheadd CP1, Al5X1,
  7A77, Scalmalloy's composition). All still need a person to re-check before submission.
- **Everything else:** headers only. No Al campaign run has happened yet.
