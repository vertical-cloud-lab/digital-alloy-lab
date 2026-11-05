# eagar-tsai: tests, and a check against measured AlSi10Mg tracks and the Thermo-Calc AM module (#235)

[ArroyaveLab/eagar-tsai](https://github.com/ArroyaveLab/eagar-tsai) 0.6.0 (commit `7639a79`) is a fast
Eagar–Tsai moving-heat-source model. It gives melt-pool width, depth and length, and printability maps
classified by the criteria of Sheikh et al. 2024. Issue #235 asked us to run it and compare it with our
preliminary Genesis Mission results from the Thermo-Calc AM module. For Xavier's Sobol sweep, the unit
error, and the slow-integrand problem in the Linux wheels, see
[`../../edison-trajectories/eagar-tsai-alsi10mg-inputs/sobol-check/`](../../edison-trajectories/eagar-tsai-alsi10mg-inputs/sobol-check/).

## Install and tests

Built from the clone with `uv pip install -e ".[plot]" pytest` (Python 3.12). The compiled integrand loads:
`_INTEGRAND` is a `LowLevelCallable`.

| Run | Result |
|---|---|
| `pytest --deselect tests/test_plot.py` | **91 passed** in 3.9 s ([log](logs/pytest-noplot.log)) |
| `pytest tests/test_plot.py` with no display | the whole pytest process **segfaults** in `test_plot_3d_returns_figure`, which calls pyvista/VTK ([log](logs/pytest-no-display-segfault.log)) |
| `xvfb-run pytest tests/test_plot.py` | 10 passed, 1 failed: `test_plot_3d_returns_figure`, `RenderWindowUnavailable: Render window is not current`, because the runner has no OpenGL or EGL ([log](logs/pytest-plot-xvfb.log), [error](logs/pytest-plot3d-xvfb-error.log)) |

So 101 of 102 tests pass. The failure is the runner's missing OpenGL, not the model. Upstream could skip the 3D test
when no render window is available, so that it can't take down the whole run.

Two things to know before using it for AlSi10Mg:
- **`beam_diameter` is 2σ** (twice the Gaussian standard deviation), i.e. half the 1/e² diameter.
- **The ambient temperature is fixed at 298 K** (`_T0_K` in `_types.py`). There is no input for a heated build plate,
  and AlSi10Mg is often printed on one at 150–200 °C.

## Comparing with the Thermo-Calc AM module

Our AM-module results are in the private repo, which this runner can't reach. The AM module's own worked examples on
help.thermocalc.com need a login, so I couldn't take numbers from them either. Two public points matter:
- The proposal already notes the AM module's weak spot for Al: it computes absorptivity from the liquid's electrical
  resistivity, and that ignores the oxide film (`genesis-mission-proposal/flaime-genesis-proposal.tex`, "Thermo-Calc
  Partnership & AM Module Feedback").
- Thermo-Calc's AlSi10Mg example **AM_11** compares single tracks on cast and LPBF substrates with experiment. Its
  public search-engine summary says the calculated absorptivity had to be **scaled by 1.8** to match the measured
  pools, and that measured pools are deeper than simulated ones, more so as depth grows. I could only see that
  summary, not the
  [page](https://help.thermocalc.com/2025b/content/examples/am/am_11_batch_al10sim.htm) itself.

Like the AM module, eagar-tsai needs a calibrated absorptivity for Al. So I tested eagar-tsai against what an
AM-module printability map is meant to predict: measured AlSi10Mg single tracks.

### eagar-tsai against measured AlSi10Mg single tracks

The data come from Solyaev et al., *On the influence of powder particle size on single-track formation in laser
powder bed fusion of AlSi10Mg alloy*, [arXiv:2507.23422](https://arxiv.org/abs/2507.23422) (2025). That study fitted
its own Eagar–Tsai model to its tracks, so its inputs can be reused directly:
- beam 2R = 80 µm with q ∝ exp(−r²/R²), which is `beam_diameter` = 56.6 µm in eagar-tsai's convention;
- liquid properties (k = 120 W/m/K, ρ = 1800 kg/m³, c = 1800 J/kg/K), with the pool edge at the solidus (836 K);
- A = 0.22, its fit for standard powder (d50 = 44 µm);
- a 60 µm effective layer.

I ran a 21 × 20 grid (40–400 W, 0.1–2.0 m/s, 2 µm cells; 136 s on 4 vCPUs) and drew the study's measured
boundaries over it:

![eagar-tsai printability map vs measured AlSi10Mg single tracks](alsi10mg-printability-vs-solyaev2025.png)

| Defect | Measured (Solyaev et al.) | eagar-tsai 0.6.0, default criteria |
|---|---|---|
| Keyhole | P > 220 W **and** v < 0.8 m/s, classed by D/W > 0.75 | Its keyhole test (W/D ≤ 2.5) flags 157 of 420 points. That includes 79 of the 80 measured-keyhole points, but **78 points outside the region**: 13 at 166–220 W below 0.8 m/s, and 65 above 0.8 m/s. The boundary runs diagonally (166 W at 0.1 m/s, 256 W at 0.9 m/s, 382 W at 1.7 m/s) instead of along the measured box. **eagar-tsai never reaches the study's D/W = 0.75**: its largest D/W on the grid is 0.48, because a conduction model can't make keyhole-shaped pools. |
| Lack of fusion | Tracks are continuous above E_l = P/v = 88 J/m (for v < 1.13 m/s, Pe < 2) | Below 1.13 m/s its LOF test (depth ≤ 60 µm layer) flags 108 of 231 points. That covers all 16 measured-LOF points, plus **92 points where the measured tracks were continuous**. On the measured boundary it predicts pools only 0–18 µm deep. Its LOF tests are meant for bulk parts (layer and hatch overlap), so they are stricter than single-track continuity by construction. |
| Stable | 135 of the 231 scored points | **9 of 420 points** are "defect-free". The keyhole and LOF lines nearly coincide, leaving only a thin band between them. |

At the study's keyhole cross-sections (328 W, 0.335 m/s), eagar-tsai gives W = 236 µm and D = 108 µm (D/W = 0.46),
with a peak of 4,164 K, far above aluminium's boiling point (2,743 K). The earlier AlSi10Mg run on this branch found
the same thing: with the default thresholds, eagar-tsai's map has almost no window for Al. **To use it as a
printability screen for Al, the W/D threshold and the LOF depth rule have to be refit to our own single-track
cross-sections, just as the AM module needed its absorptivity scaled.** Fitting the 2.5 threshold against these
measured keyhole tracks would be a good first test.

The higher-speed branch of the study's LOF boundary (a constant enthalpy density of 8.9 J/mm³ above Pe = 2) is not
drawn. Rebuilding it from the paper's formula did not join the E_l branch at Pe = 2, so speeds of 1.13 m/s and above
are not scored for LOF.

### Stock vs Si-enriched AlSi10Mg

The proposal's AM-module figure compares stock AlSi10Mg with a Si-enriched variant. In eagar-tsai, composition
enters only through the isotherm temperature and four constant properties.
[Sweeping the isotherm](alsi10mg-isotherm-sensitivity.csv) from 836 K (solidus) to 870 K (liquidus) at
200–370 W shrinks W by 4 µm and D by 3–4 µm. A Si-enriched variant lowers the liquidus by roughly 15–20 K, which
moves W and D by about 2 µm. **eagar-tsai can't separate the two alloys**; the differences the AM-module figure
shows (solidification range, phase fractions) come from the CALPHAD side.

### Running it on our private AM-module results

[`scripts/eagar_tsai_vs_am_module.py`](../../scripts/eagar_tsai_vs_am_module.py) `private` runs eagar-tsai on every
row of an AM-module export and writes a parity table and plot (width, depth, length):

```bash
pip install --no-binary eagar-tsai eagar-tsai pandas matplotlib     # Linux; plain pip elsewhere
python scripts/eagar_tsai_vs_am_module.py private am_module_results.csv \
    --beam-convention one_over_e2_radius --out private/eagar-vs-am
```

The CSV needs `power_w`, `velocity_m_s`, `beam_size_um` and `absorptivity`; use the absorptivity the AM module
actually applied. Optional columns are `T_melt_k`, `k_w_mk`, `rho_kg_m3`, `cp_j_kgk` (otherwise the Edison AlSi10Mg
values: 867 K, 110 W/m/K, 2650 kg/m³, 1040 J/kg/K) and `am_width_um` / `am_depth_um` / `am_length_um`, which are what
gets compared. `--beam-convention` says what `beam_size_um` is: `two_sigma`, `one_over_e2_radius`,
`one_over_e2_diameter` or `one_over_e_radius`. The script refuses beams outside 1 µm–1 mm, the unit error behind the
762 GiB arrays. I tested it on a throwaway CSV but haven't committed one, because there are no real AM-module rows
on this side.

```bash
python scripts/eagar_tsai_vs_am_module.py published --out arroyave-orchid-tools/eagar-tsai   # regenerates this folder
```

## Files

| File | What it is |
|---|---|
| `alsi10mg-printability-vs-solyaev2025.csv` | the 420 grid points: eagar-tsai W, D, L, its five defect flags and class, D/W, E_l and the measured class |
| `alsi10mg-printability-vs-solyaev2025.png` | the map above |
| `alsi10mg-printability-vs-solyaev2025-summary.txt` | the agreement counts |
| `alsi10mg-isotherm-sensitivity.csv` | W, D, L and peak T vs melt isotherm (820–880 K) at three process points, 1 µm grid |
| `logs/` | pytest and run logs |
