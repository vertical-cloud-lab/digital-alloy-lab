# ORCHID group (github.com/orchid-calphad): install and test runs

Issue #235. Run on 2026-11-05 (UTC) on a shared GitHub Actions runner: 4 vCPU, 15 GB RAM shared with four other agents,
no GPU, Ubuntu, CPython 3.12.3 (3.13 where a repo's CI pins it), uv for every environment. Every install and
third-party script ran through the scrubbed-environment wrapper `/tmp/sbx/clean` with `OMP_NUM_THREADS=1`. The repos
are shallow clones under `/tmp/arroyave/src/orchid-calphad__*`. orchid-data and orchid-project.org were treated as
read-only, so anything that writes ran on a copy under `/tmp/arroyave/work/`. No paid API calls, no publishing, no
git writes.

**Bottom line.** Every repo installs from what it ships (orchid-bench and orchid-project.org have no dependency manifest;
their READMEs' package lists work unpinned) and their shipped tests and checks pass. Every headline number we re-ran reproduces:

| claim | reproduced |
|---|---|
| SGTE Cu–Zr one-shot recall 0.72 / 0.73 | 0.722 / 0.728, 315/315 identical predictions |
| GRACE MLIP-only 0.426 / 0.410 | 0.426 / 0.410 |
| tuned 9/13 invariants (MLIP-only 0/13, SGTE 12/13) | gate table byte-identical |
| orchid-bench extractor scores | 19/19 extractors rescored identically (to 1e-16) |

The byte-identical checks fail only on PNG encoding and on one stale committed hash.

**What matters for our Al/Cu work:**
- **Al–Si:** ORCHID has 13 values and **none accepted**, with no ESPEI datasets, so `get_invariant_reactions(source="literature")` returns no data.
- **Al–Cu:** thin. There are 114 values from 4 papers, 30 accepted experimental invariants, no formation enthalpies, no DFT parity rows and 3 ZPF datasets for AlCu-21Kro. The θ eutectic is never matched to literature because of a phase-label parsing gap.
- **Al–Zr:** the best-covered Al system, with 743 values, 88 accepted experimental invariants, 58 accepted multi-reader ΔHf values and 210 ESPEI datasets.
- **Cu–Ni:** no accepted invariants.
- **Ternaries:** no data for Cu–Al–Ni–Fe (nickel aluminium bronze) or Al–Mn–Cr–Zr.
- **Scorer:** the one-shot phase-diagram scorer is hard-wired to Cu–Zr, so it cannot score an Al–Cu or Cu–Ni TDB without porting.

Per-system counts are in `data/al-cu-coverage.csv`. The experimental invariants for reuse are in `data/al-cu-literature-invariants.csv` (345 rows; T in K and °C, compositions as mole fractions, DOI per row).
