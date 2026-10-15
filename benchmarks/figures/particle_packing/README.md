# Particle-packing BOFN benchmark — design-stage figures

Companion artifacts for `edison-trajectories/crabnet-particle-packing-bofn-plan.md`.
These are design-stage figures (no BO algorithm has been run against this
benchmark yet); they document the proposed cascade and verify that the
underlying emulator data path actually works.

- Generator: `benchmarks/particle_packing_visualize.py`
- Code source: [`sparks-baird/matsci-opt-benchmarks`](https://github.com/sparks-baird/matsci-opt-benchmarks) v0.2.3
- Data sources (pull locally; do not commit):
  - Zenodo `10.5281/zenodo.7513019` — raw Sobol CSVs
    - `sobol_probability_filter.csv` md5 `21063bee0ef0a00b218f3a4b7aed8290`
    - `sobol_regression.csv` md5 `3e6c2be63903fb4c8c6f99848a5b9f8c`
  - Zenodo `10.5281/zenodo.7696165` — surrogate snapshot
    - `model_metadata.json` md5 `99de50536770b78cf31d32f53eb392f2`
    - `surrogate_models.pkl` (3.97 GB; ORC-only, do not load on GHA runners)

## Figures

### `particle_packing_dag.png`

Six-node DAG: each stage (FBA force-biased pack and LS Lubachevsky–Stillinger
refine) is split into three discrete fidelity nodes at `n_particles ∈
{128, 512, 2048}`, with matched-fidelity edges FBA-K → LS-K. Per-node
outputs are packing fraction φ, runtime t, and failure probability P_fail.
The 9 shared design variables are the log-normal `mu1..3, std1..3, comp1..2`
plus `safety_factor`; `n_particles` is fixed by node identity rather than
entering as a continuous knob, so a query is a pair `(node_idx, x ∈ R^9)`.
This gives p-KGFN both a cascade *and* an explicit fidelity-selection
problem and mirrors how FLAIME's mesh-density / `n_coupons` settings would
be promoted from a continuous knob to discrete fidelities.

Cost badges combine the `n_particles=128` smoke test of the bundled
`PackingGeneration.exe` in `matsci-opt-benchmarks==0.2.3` (FBA ~0.01 s,
LS ~1.6 s) with the empirical scaling to `n_particles=512` and `2048` from
the released regression dataset.

### `particle_packing_emulator_diagnostics.png`

2×3 parity grid for the six emulator targets, mirroring the diagnostic role
of PR #58's `node_correlations.png`:

- `fba_isna_prob`, `ls_isna_prob` — failure-probability filter heads
- `fba`, `ls` — packing-fraction heads (with percentile-rank noise feature)
- `fba_time_s`, `ls_time_s` — runtime heads (with percentile-rank noise feature)

Models are 16-tree random forests trained on a 2k–4k row subsample of the
Zenodo CSVs, replaying the exact target decomposition in
[`notebooks/particle_packing/1.2-ri-surrogate.ipynb`](https://github.com/sparks-baird/matsci-opt-benchmarks/blob/main/notebooks/particle_packing/1.2-ri-surrogate.ipynb).
This is intentionally lighter than the production emulator so it fits in CI;
the production path should load `surrogate_models.pkl` on ORC.

## Reproducing locally

```bash
mkdir -p benchmarks/data/particle_packing
curl -L -o benchmarks/data/particle_packing/sobol_probability_filter.csv \
  'https://zenodo.org/records/7513019/files/sobol_probability_filter.csv?download=1'
curl -L -o benchmarks/data/particle_packing/sobol_regression.csv \
  'https://zenodo.org/records/7513019/files/sobol_regression.csv?download=1'
python benchmarks/particle_packing_visualize.py
```

Set `PARTICLE_PACKING_DATA=/some/other/dir` to point at a different cache.
The DAG always renders; the diagnostics grid is skipped if the CSVs are not
found.

## Not yet here

Once `benchmarks/partial_kgfn/particle_packing_problem.py` lands, this
directory should also gain (mirroring PR #58):

- `particle_packing_cost_efficiency.png` — equal-cost anytime curve, mean ± 1σ
- `particle_packing_node_selection.png` — node-selection histogram + failure inset
- `particle_packing_summary.{csv,json}` — per-algorithm summary stats
