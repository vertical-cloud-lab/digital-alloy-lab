# bofn-failures: pre-registration

Written and committed on 2026-11-26, before any run of the sweep below. Smoke runs (seed 0, one
campaign per strategy) were made only to check that the code runs and to time it; they are not
part of the results.

**Everything here is synthetic.** The two networks are the lab's own benchmarks, vendored
unmodified: aluminum LPBF (`bofn-prelim`, PR #117) and copper DED (`bofn-cu-ded`, PR #206, with
its hand-written and physics-based truths). The failure layer (`failmodel.py`) is new and
assumed; its rates and regions are given in the README with their sources.

## Question

When a stage of the alloy workflow fails, what should a BOFN campaign do with the run? The
strategies map onto Ax's trial statuses (`policy.py` docstring): `drop` (every failed run
`FAILED`, as Ax 1.0–1.2.3's `complete_trial` did with a missing metric), `abandon` (every failed
run `ABANDONED`), `partial` (Ax ≥ 1.2.4: `COMPLETED` with the metrics it has), `impute`
("soft pushing": an input-caused failure recorded as the worst value seen at the failed stage),
`viab_x` (Ax 1.3's `AddExecutionViability`), `viab_x_partial` (the same with
`fit_abandoned=True`), and `viab_node` (a node-level ledger with a viability model per stage).
`nofail` is the same campaign with failures switched off, as a reference.

All strategies share one search policy, the source benchmarks' best: BOFN with lot reuse
(network EI per dollar over new designs and new prints/sessions on existing lots), on the same
seed data, $100k of new spend, and the same failure draws (one random stream per seed and
stage, consumed in attempt order).

## Cells and scenarios

| Cell | Truth | Seeds |
|---|---|---|
| `al-k1` | aluminum, `kappa = 1` (CALPHAD misses the inoculant; the headline cell of bofn-prelim) | 0–19 |
| `al-k0` | aluminum, `kappa = 0` (the screen is right; most high-solute alloys crack) | 0–19 |
| `cu-toy-k1` | copper, hand-written truth, `(kappa, eta) = (1, 1)` | 0–15 |
| `cu-phys-k1` | copper, physics-based truth, `(1, 1)` | 0–15 |

Scenarios: `mixed` (input-caused and transient failures, labelled correctly; every strategy),
`mislabel` (the same failures, 30 % of labels wrong; only the strategies that read labels:
`impute`, `viab_x`, `viab_x_partial`, `viab_node`; the others are identical to `mixed` by
construction), `transient` (transient failures only; `drop`, `abandon`, `partial`, `viab_node`,
since `viab_x` and `viab_x_partial` then reduce to `drop` and `impute` to `viab_node`).
Priority order (later cells may be cut for time, and that will be said): `al-k1` mixed, `cu-toy-k1`
mixed, `al-k1` mislabel and transient, `cu-toy-k1` mislabel and transient, `cu-phys-k1` mixed,
`al-k0` mixed, then `mislabel` on `cu-phys-k1` and `al-k0`.

## Metrics

- **Primary:** best alloy demonstrated at $100k (the true objective of the best design printed
  or deposited and carried through every test), as a percentage of the cell's true optimum.
- **Secondary:** the same at $50k; spend on failed stages; input-caused failures and repeats
  (an input-caused failure within 0.1 of an earlier one in scaled design space); validated alloys.

## Hypotheses (directions predicted before running)

- **H1.** `drop` does worst once input-caused failures exist: it learns nothing from them, so it
  repeats them. Predicted: lowest primary metric and most repeats in every `mixed` cell.
- **H2.** Keeping the completed stages of a failed run helps: `partial` ≥ `abandon` and
  `viab_x_partial` ≥ `viab_x`.
- **H3.** Treating transient failures as permanent costs something: in `transient`,
  `abandon` < `viab_node` (which keeps the data and leaves the design free to retry).
- **H4.** A failure model helps: `viab_x_partial` and `viab_node` have fewer input-caused
  failures than `partial`.
- **H5.** A failure model over the failing stage's own inputs beats one over the design:
  `viab_node` ≥ `viab_x_partial` on the primary metric, with fewer input-caused failures,
  because the failure regions are simple in the stage inputs (crack severity from `f` and `g`,
  energy density from `P`, `v` and `f`, powder yield `q`) and curved in the design.
- **H6.** With correct labels, `impute` is competitive with `viab_node`, because in these networks
  the failing designs are poor anyway (no design within 60 % of any cell's optimum is in a failure
  region). With 30 % mislabels, `impute` loses more than `viab_node` does, because a transient
  fault near a good design is then written down as a bad result.
- **H7.** Every strategy finishes below `nofail`.

## Analysis plan

Mean ± SE over seeds per strategy and cell. Paired comparisons on matched seeds (the seeds share
the seed data and the failure draws): `viab_node` against each other strategy, and `partial`
against `abandon` and `drop`; two-sided Wilcoxon signed-rank tests with a Holm correction within
each cell and scenario, plus 90 % bootstrap intervals of the mean paired difference. Results are
reported whichever way they go, including where `viab_node` doesn't win.
