# Seeding the BOFN campaign: which experiments come first (#275)

[#275](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/275) asks how to choose the
initial experiments for the Al alloy campaign in
[#255](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255) and its schedule in
[#256](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/256). It suggests a mix of
three sources, about three runs each: agent-chosen (literature, databases, CALPHAD), known
baselines (AlSi10Mg, Scalmalloy), and Sobol or another space-filling design. It also asks how to
bring in the databases from [#7](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/7)
and [#8](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/8), how "fantasy" data
(synthetic or from the literature) could stand in until real data exist, and whether 3 + 3 + 3
makes sense with 25 experiments left. Edison Scientific was used as a rubber duck throughout.

<!-- SHORT-ANSWERS -->

## What the 25 experiments are

The [#256 schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#the-36-al-runs)
has 36 Al atomizer runs. Five are the 6063 baseline repeats (A1–A5) and six are flex slots
(X1–X6), which leaves 25 runs whose composition someone has to choose:

| Block | Runs | When | Seed or optimizer? |
|---|---|---|---|
| D benchmarks | D1 (AlSi10Mg-type), D2 (Scalmalloy-type), D1-r (repeat) | Nov 30, Dec 2, Feb 8 | baseline seeds |
| B dosing checks | B30 (Si ≈ 3.9 wt%), B15 (Si ≈ 2.1 wt%) | Dec 1, Dec 3 | known-composition seeds on the Al–Si line |
| S CALPHAD seeds | S1–S4 | Dec 7–10 | agent-chosen seeds |
| R optimizer rounds | R1–R4, 3 each | Jan 5 – Feb 3 | optimizer |
| F finalists | F1 ×2, F2 ×2 | Jan 25–28 | repeats of optimizer picks |

So the schedule already spends 8 runs on seeds before the optimizer's first batch (D1, D2, B30,
B15, S1–S4), plus D1-r late. The flex slots X1–X3 (Dec 14–16) also come before the first batch
is picked on Dec 18.

**The optimizer picks its first two batches before it has any strength data on a new
composition.** Tensile bars of the seeds are printed at P3 (Jan 12–13) and tested Jan 19–22. By
Dec 18 (R1) and Jan 8 (R2), the only strength data are commercial AlSi10Mg from P1 and wrought
6063. So the downstream nodes of the network run on priors (literature data, models, the
"fantasy" data below) for most of the campaign. What goes into those priors matters at least as
much as how the 25 runs are split.

## Seeds for every node, not just compositions

BOFN keeps a separate GP for each node, and each one needs its own starting data. Most of that
data doesn't need an atomizer run.

| Node | Inputs → outputs | Seeds that cost no atomizer run | Seeds from atomizer runs | When |
|---|---|---|---|---|
| CALPHAD descriptors | composition → liquidus, solidus, freezing range, Scheil cracking index, phase fractions | It is a cheap, known function: compute thousands of compositions (pycalphad now, Thermo-Calc once licensed, [#141](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/141)) | — | W1–W3 |
| Mineral burden | composition → weighted critical-mineral content | Analytic | — | — |
| Dosing and composition fidelity | charge recipe → measured composition (EDS, ICP-OES) | 6063 and 4047 as received | B30, B15, D1, D2, then every run | Dec 1–3 |
| Atomization | measured composition (or its descriptors), superheat, amplitude → yield in cut, D10/D50/D90, sphericity, oxygen | Earlier runs (Oct 2, 6, 8, the 4047 runs in [#159](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159)), flagged by settings; Lang's relation as a prior mean for D50 ([#111](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/111)) | A1–A5 (noise), then every run | from Nov 17 |
| Powder characterization (SEM/EDS) | powder → size and shape, satellites, homogeneity | Commercial AlSi10Mg 15–45 µm powder; the NAB analysis pipeline from [#225](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/225) | Every run (weekly Thursday session) | weekly |
| Print parameters (single tracks, cubes) | powder descriptors + power, speed, hatch, layer → melt-pool depth and width, mode, density, cracks | **Literature:** the Barrionuevo LPBF dataset already in [`database-samples/`](../database-samples/) has 353 AlSi10Mg rows from 15 papers and 12 printers, including 18 on AconityLAB and 27 on a Concept Laser M2 (the BYU machine). **Models:** Eagar–Tsai and the AM Module printability maps ([#262](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/262)). **P1:** commercial AlSi10Mg, single tracks in Sobol blocks as in [#243](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243), plus cubes | In-house 6063 and D1 at P2; S-run tracks at P2 | P1 Dec 2–3, P2 Dec 16–17 |
| Hardness (the fast strength screen) | printed material, heat treatment → HV | P1 AlSi10Mg cubes, wrought 6063, published HV for the benchmarks | D1 and S runs from P2 and P3 | from Dec 11 |
| Tensile | printed material → yield strength, UTS, elongation | P1 AlSi10Mg bars; literature tensile data for AlSi10Mg, Scalmalloy and Sc-free LPBF alloys (Edison q2, below) | Seeds from P3, finalists | Dec 14–16, Jan 19–22, Feb 9–12 |
| Corrosion | material → OCP, polarization | Wrought 6063 and printed AlSi10Mg, already in #256 | Finalists | when the electrodes arrive ([#221](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/221)) |

Two consequences:

- **The print-parameter node doesn't need new alloys to get started.** Commercial AlSi10Mg at P1,
  the literature rows and the melt-pool models seed it. The atomizer runs only have to teach it
  how a new composition shifts the window.
- **Space-filling should happen in each node's own input space.** A downstream GP sees CALPHAD
  descriptors and powder properties, not raw wt%. Once the CALPHAD screen exists, pick
  space-filling seeds in descriptor space (`seed_design.py --candidates ... --features ...`).

<!-- STRATEGIES -->

## Space-filling around the points we already have

[`seed_design.py`](seed_design.py) adds space-filling points around everything already in
[`seeds.csv`](seeds.csv) (6063, D1, D2, B30, B15; add the agent picks there). It works in the space
a GP with `Normalize` over the design box sees: each element's wt% divided by its upper bound. The
bounds are the finalized ones on [PR #72](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/72)
(Al ≥ 85 wt%, per-element caps, a 0.10 wt% floor for any element that is switched on, and its joint
caps). Candidates have one to three additions from the elements on hand per
[#146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146) (Mn, Cr, Mg, Ti, Er, Zn,
plus Si through 4047) and at least 3 wt% of additions in all. The four methods:

| Method | What it does |
|---|---|
| `sobol` | First feasible points of a scrambled Sobol sequence. Ignores the existing points |
| `sobol-exclusion` | Walks the same sequence and skips points within a radius of an existing or picked point (the heuristic in #275) |
| `maximin` | Greedy maximin: each pick is the candidate farthest from everything so far |
| `imse` | Greedy integrated-variance reduction: each pick most lowers the average variance of a GP over the whole feasible pool. Before any outcome is measured, that variance depends only on where the points are, so no data are needed |

Three new points, averaged over 10 scrambles ([`results/space_filling_compare.csv`](results/space_filling_compare.csv);
distances in normalized units, GP length scale 0.5):

| Method | Nearest existing point | Nearest pair of new points | Mean distance to nearest point | Mean GP variance |
|---|---|---|---|---|
| (existing points only) | | | 0.843 | 0.844 |
| `sobol` | 0.747 | 0.911 | 0.731 | 0.757 |
| `sobol-exclusion` | 0.789 | 1.062 | 0.731 | 0.759 |
| `maximin` | 1.557 | 1.850 | 0.802 | 0.830 |
| `imse` | 0.633 | 0.931 | **0.640** | **0.669** |

The picks for seed 0 ([`results/`](results/)):

| Method | SF1 (wt%) | SF2 (wt%) | SF3 (wt%) |
|---|---|---|---|
| `sobol`, `sobol-exclusion` | Al-2.72Cr-0.31Ti | Al-0.86Mn-2.12Cr-0.30Er | Al-4.57Mg-0.47Ti |
| `maximin` | Al-3.00Cr-0.50Er-7.45Zn | Al-4.44Mn-0.50Ti-7.06Zn | Al-4.86Mg-0.48Ti-0.45Er |
| `imse` | Al-0.52Mn-0.11Er-5.37Zn | Al-3.50Mn-0.69Cr-0.59Mg | Al-0.33Cr-3.77Mg-1.70Si |

What this shows:

- **Three points don't fill a 7-D space.** The best method lowers the mean GP variance from 0.84
  to 0.67. The worst-covered composition stays about as far from any experiment as before (fill
  distance 1.57 → about 1.5 for every method). Exploration in raw composition space with three
  runs mostly buys three more scattered points. In a reduced space (CALPHAD descriptors, or one
  or two sub-system families) the same three runs cover far more.
- **Exclusion rarely bites with this few existing points.** With five existing points in 7-D, the
  first Sobol points are already more than 0.5 from all of them, so `sobol` and
  `sobol-exclusion` pick the same three alloys here. Exclusion starts to matter once the existing
  set is large: literature points, or a dense CALPHAD screen.
- **Maximin sends every point to a corner.** Al-3Cr-0.5Er-7.5Zn and Al-4.4Mn-0.5Ti-7.1Zn sit on
  several caps at once. They are the hardest to melt, dose and print, and they cover the space
  worse on average than plain Sobol.
- **`imse` covers best on average,** and its picks are moderate compositions such as
  Al-3.5Mn-0.7Cr-0.6Mg, a Zr-free cousin of the Al–Mn–Cr–Zr focus system. Use it, but check its
  picks against the CALPHAD liquidus and cracking screen before dosing.

<!-- SIMULATION -->

## Literature and "fantasy" data

#275's "fantasy modelling" (synthetic or literature data standing in until real data exist) is a
different thing from BoTorch's `fantasize`, which conditions a model on sampled outcomes at
pending points so that a batch doesn't pick the same point twice. That second meaning is what
[#104](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/104) is about, and it is
what pKGFN needs. To keep the two apart, this folder calls the first kind **pseudo-data**.

<!-- PSEUDODATA -->

## Files

| File | What |
|---|---|
| [`seeds.csv`](seeds.csv) | Points already chosen: the 6063 baseline, D1, D2, B30, B15. Add the agent picks here, and replace nominal compositions with measured ones as they come in |
| [`seed_design.py`](seed_design.py) | Space-filling picks around `seeds.csv`, in composition space or in descriptor space after the CALPHAD screen |
| [`budget_split_sim.py`](budget_split_sim.py) | Toy simulation of how to split 25 runs between seeds and optimizer batches |
| [`results/`](results/) | Outputs of the two scripts |
| [`edison/`](edison/) | The Edison queries, answers, artifacts and full trajectories, and `edison_tasks.py`, which submits, waits for and fetches them |

```bash
pip install numpy scipy
python bofn-seeding/seed_design.py                       # 3 picks, imse
python bofn-seeding/seed_design.py --compare             # all four methods
python bofn-seeding/seed_design.py --elements Mn Cr Mg Si Er Ti Zn Zr   # once Zr is on the shelf

pip install torch botorch
python bofn-seeding/budget_split_sim.py --reps 30 --workers 4
```
