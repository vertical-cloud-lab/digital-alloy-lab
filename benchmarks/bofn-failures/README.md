# BOFN with failed vs. abandoned experiments: a benchmark on the lab's aluminum and copper networks

Issue [#274](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/274). When a stage of
the alloy workflow fails (the powder won't atomize, a build crashes, a bar breaks outside the gauge),
what should a Bayesian-optimization campaign do with the run? This benchmark answers that on the two
synthetic function networks the lab already uses for its proposals: the aluminum LPBF network
(`bofn-prelim`, PR #117) and the copper DED network (`bofn-cu-ded`, PR #206, with both its
hand-written and its physics-based truth). The strategies are named for what Ax does with each
trial status, checked against Ax's code and threads (`survey/ax.md`) and BoTorch's
(`survey/botorch.md`).

**Everything here is synthetic.** The networks are hand-built or physics-informed simulators, not
data, and the failure layer (`failmodel.py`) is an assumption, sourced below.

<!-- RESULTS -->

## The question in Ax's terms

A function network fails at a stage, not as a whole trial: the stages upstream of a failure
produced good data, and an input-caused failure says something about *that stage's* inputs (which
include measured intermediates such as powder yield), not about the whole design. Ax gives each trial
one status. What each strategy does with a run that stopped early:

| Strategy | Ax analogue (version) | Completed stages of a failed run | Failed design pending? | Failure model |
|---|---|---|---|---|
| `drop` | every failure `FAILED`; also what `Client.complete_trial` did with a missing metric from 0.5.0 to 1.2.3 | not fit (since 1.2.2) | no, may be suggested again | none |
| `abandon` | every failure `ABANDONED` | not fit | yes, for good | none |
| `partial` | `Client.complete_trial` with missing metrics (≥ 1.2.4): `COMPLETED`, partial data fit | fit | yes, for the stages it lacks | none |
| `keep` | the same, as Ax actually treats it below 100 trials when the arm has any objective or constraint metric | fit | no | none |
| `impute` | "soft pushing" (Xavier, above; BoTorch maintainers' advice in [#943](https://github.com/meta-pytorch/botorch/issues/943#issuecomment-918802564)): an input-caused failure is recorded as the worst value seen at that stage; a transient one is dropped | fit | no | implicit |
| `viab_x` | `AddExecutionViability` (1.3.0, opt-in): transient → `FAILED`, input-caused → `ABANDONED`; GP on 0/1 labels over the design, `P(viable) ≥ 0.8` after 3 abandoned runs | not fit | input-caused: yes | over the design `x` |
| `viab_x_partial` | the same with `fit_abandoned=True` (every status fit, `FAILED` included) | fit | input-caused: for the stages it lacks | over `x` |
| `viab_node` | a node-level ledger (proposed in [`bofn-failed-vs-abandoned.md`](../../bofn-failed-vs-abandoned.md) §4) | fit | no | per stage, over that stage's own inputs |
| `viab_node_ec` | `viab_node`, plus failures priced into the acquisition: EI × P(no transient fault) / expected cost of a chain that stops at its first failure | fit | no | per stage |
| `nofail` | reference: the same campaign with failures switched off | | | |

Every strategy runs the same search policy, the source benchmarks' best: BOFN with lot reuse
(`eifn_reuse`: network expected improvement per dollar over new designs and new prints or DED
sessions on powder lots already made). With failures switched off, every strategy reproduces the
source run action for action on both networks (`tests/`). A full-pipeline variant (`+full`, every
decision a new design through every stage, the source `eifn`) checks that the findings are not an
artefact of lot reuse.

How each Ax behaviour is emulated, and where the emulation is a simplification:

- **Fit / not fit** is exact: each node's GP is trained on the observations the strategy keeps.
- **Pending** follows BoTorch's `X_pending` effect with a kriging believer: the pending design's
  missing node outputs are added to their GPs at the posterior mean (hyperparameters fixed), which
  lowers the value of nearby candidates. The source benchmarks sample each candidate's network
  posterior marginally, so joint sampling with `X_pending` isn't available.
- **Viability** is what Ax fits: an ordinary GP regression on 0/1 labels (noise learned), and each
  Monte Carlo sample of the network counts as an improvement only if the sampled viability clears
  0.8 (BoTorch's sigmoid with `eta = 1e-3`). `viab_x` uses one GP over the 7-D design;
  `viab_node` one GP per failing stage, over that stage's node inputs, sampled with the sampled
  parent outputs. Neither is a classifier; a Bernoulli variational GP is BoTorch's recommended
  model (`survey/botorch.md` §f) and is left for later.
- **CALPHAD** never fails and is always kept: it is a simulation the lab stores whatever happens
  downstream.

## The networks

| Cell | Network (vendored unmodified, `vendor/SOURCES.md`) | Stages that can fail | True optimum |
|---|---|---|---|
| `al-k1` | aluminum LPBF, `kappa = 1` (CALPHAD misses the Zr inoculant): CALPHAD → ultrasonic atomization → LPBF build → tensile | atomize, build, tensile | 0.694 |
| `al-k0` | aluminum, `kappa = 0` (the crack screen is right, so most high-solute alloys crack) | same | 0.485 |
| `cu-toy-k1` | copper DED, hand-written truth, `(kappa, eta) = (1, 1)`: CALPHAD + heat flow → atomization → small DED (Utah, power-capped) → large DED (Mines) → microscopy → tensile → 1-h screen → 30-day immersion | atomize, Utah, Mines, tensile, immersion | 0.492 |
| `cu-phys-k1` | copper DED, physics-based truth (pycalphad grid, seawater-corrosion fit, the proposal's search-space limits), `(1, 1)` | same | 0.431 |

The scores are "best alloy demonstrated" as in the source benchmarks: the true objective of the best
design carried through every test, as a percentage of the cell's optimum (`optima.json`, computed by
`calibrate.py`; within 0.5 % of the source READMEs' values). All campaigns start from the source
benchmarks' shared seed data (CALPHAD on 32 compositions and five full runs, sunk and
failure-free) and spend $100k at the source costs.

## The failure model (`failmodel.py`)

Two kinds of failure, drawn independently at every stage attempt:

**Transient** (Ax `FAILED`: unrelated to the inputs, could be repeated):

| Stage | Probability | Source |
|---|---|---|
| ultrasonic atomization | 0.15 aluminum, 0.20 copper | Between bofn-clocked's assumed 0.10 and the lab's own record: of the ten logged runs (Oct 2 to Nov 13, [`atomizer-runs/runs.csv`](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/8320f13623c7961fcce12ee4d5d2033f4d8c9936/atomizer-runs/runs.csv) on PR #286), seven made little or no usable powder, and six of those seven for reasons unrelated to the alloy (setup, a plate on its second use, a generator trip). Of the five copper runs, three failed that way. The rates here assume the SOP fixes since then (new plate each run, plate-height gauge) have taken hold. |
| LPBF build, Mines DED session | 0.08 | bofn-clocked's assumption (recoater crash, delamination, support failure) |
| Utah DED session, 30-day immersion | 0.05 | assumed |
| tensile | 0.03 | bofn-clocked's assumption (bar breaks outside the gauge) |

**Input-caused** (Ax `ABANDONED`: the inputs make the stage fail), each a steep logistic of a term
the network's own truth already contains, so the failure regions move with the composition through
CALPHAD's outputs:

| Stage | Failure | Region |
|---|---|---|
| LPBF build / Mines session | severe hot cracking: up to 60 % of the most cracked builds curl into the recoater or delaminate | crack severity above about 0.9 (the truth's `sigmoid((f_eff − onset)/0.05)`, with the inoculant/nucleant effect `kappa` included), as for unmodified 7075 ([Martin et al. 2017](https://doi.org/10.1038/nature23894)) |
| LPBF build | lack of fusion: layers don't bond | far below the energy-density ridge (the truth's window term below 0.05) |
| LPBF build / Mines session | keyholing: spatter and swelling | laser power above about 0.92 of the range |
| Utah / Mines session | the deposit never fuses | the truth's lack-of-fusion index above 0.85 (copper-rich alloys at Utah's power cap) |
| print or deposit (precondition) | too little usable powder to spread or feed | powder quality `q < 0.25`; the lab measures `q`, so it doesn't pay for the print (the "very little powder" runs of Oct 21 and Nov 13) |

`calibrate.py` places these regions (`optima.json`): every optimum is viable, and no design within
60 % of any cell's optimum is in a failure region, as one would expect physically (a crashed build
is a bad alloy or a bad setting). Of random designs, 64 % (`al-k1`), 86 % (`al-k0`), 52 %
(`cu-toy-k1`) and 46 % (`cu-phys-k1`) would fail somewhere for input reasons.

**Labels.** The lab writes down which kind each failure was. In the `mislabel` scenario 30 % of
labels are wrong (the operator can't always tell a bad plate from a bad alloy; Oct 28 and Nov 13
took a video review to trace). The precondition is always labelled correctly. One random stream
per (seed, stage), consumed in attempt order, gives every strategy the same faults and label flips.

## Scenarios, seeds and analysis

Pre-registered in [`PREREGISTRATION.md`](PREREGISTRATION.md) before the sweep. `mixed` (both kinds,
labelled correctly) for every strategy; `mislabel` for the strategies that read labels (the others
run identically by construction); `transient` (transient faults only) for the strategies that differ
there. 20 seeds for aluminum, 16 for copper; 12 for the full-pipeline check. Comparisons are on
matched seeds (same seed data and failure draws): two-sided Wilcoxon signed-rank tests with a Holm
correction within each cell and scenario, and 90 % bootstrap intervals of the mean difference.
All tables: [`tables.md`](tables.md); per-run JSON: `results/<cell>/<scenario>/<strategy>_s<seed>.json`.

## Reproduce

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu && pip install botorch scipy matplotlib pytest
cd benchmarks/bofn-failures
python -m pytest tests/ -q              # vendored code unchanged; exact reproduction of the source runs with failures off
python calibrate.py all                 # optima.json
python run_sweep.py --plan plan.txt     # every campaign in plan.txt, resumable; about 4.5 h on 4 cores
python analyze.py && python plot.py     # tables.md, summary.json, figures/
```

Versions used: Python 3.14.4, torch 2.15.0 (CPU), BoTorch 0.18.1, GPyTorch 1.15.2, Ax 1.3.1 (survey checks only).
