## constraint-satisfaction

**What it is.** Campaign scripts for constrained multi-objective active learning over a fixed pool of 40,553 refractory HEA compositions (Nb-Mo-Ta-V-W-Cr, pre-computed CALPHAD/property columns in `design_space.csv`). Six policies share one code base: feasibility-first with physics priors as GP mean (`campaign_const_w_priors.py`), the same without priors, pEHVI x P(BCC), EHVI x POF, EHVI x correlated POF (Gaussian copula), and random. Surrogates are scikit-learn GPs (ARD RBF + white noise, `n_restarts_optimizer=10`).

**Install.** Python 3.11 (as in `constraint-satisfaction.yml`), unpinned scikit-learn / SciPy stack; resolved to numpy 2.4.6, pandas 3.1.1, scikit-learn 1.9.1, scipy 1.17.1, matplotlib 3.11.2. 3 s with a warm uv cache, no problems.
```
uv venv --python 3.11 /tmp/arroyave/venvs/constraint-satisfaction
uv pip install --python /tmp/arroyave/venvs/constraint-satisfaction/bin/python scikit-learn matplotlib pandas numpy scipy openpyxl
```

**Run (scaled down).** Defaults are seeds 1-200, 100 iterations, 25 workers. I ran five policies with `--seeds 1-2 --iterations 20 --workers 2 --plot-every 10` (driver: `scripts/constraint-satisfaction-run.sh`), then the repo's own `plot_metrics.py --auto` and my summary script `scripts/constraint-satisfaction-summarize.py`.
```
/tmp/sbx/clean bash scripts/constraint-satisfaction-run.sh
cd /tmp/arroyave/work/constraint-satisfaction && python plot_metrics.py --auto --out-dir plots_metrics
```
A single-seed smoke test (`campaign_const_w_priors.py --seeds 1 --iterations 10 --workers 1`) took 16 s.

**Outcome: PASS.** All five scripts ran to completion with exit code 0 and no warnings. Wall times (2 seeds x 20 iterations, 2 workers): const_w_priors 23 s, const_NO_priors 24 s, pEHVI 26 s, EHVI x POF 35 s, random 32 s. `plot_metrics.py --auto` wrote 10 metric plots. **`campaign_ehvi_pofcorr.py` is far slower.** Run with the same settings, it hit the 300 s `timeout` after only 3 and 2 iterations (seeds 1 and 2), against 20 iterations in 23-35 s for the other scripts. The bottleneck is the Gaussian-copula POF, which calls `scipy.stats.multivariate_normal(...).cdf` (4-D, Genz integration) on all ~40k pool points at every iteration (line 732). So that policy alone took over 100 s per iteration here (`logs/constraint-satisfaction-run-campaign_ehvi_pofcorr.log`).

**Key numbers** (`data/constraint-satisfaction-summary.csv`, `figures/constraint-satisfaction-hv.png`, `figures/constraint-satisfaction-repo_plot_metrics-TrueMeasPass_All_With_BCC.png`):
- Only **24 of 40,553** pool points satisfy every constraint (solidus, density, yield strength, Pugh ratio, single-phase BCC).
- Truly feasible alloys found after 20 iterations (mean of 2 seeds): const_w_priors **13.0**, const_NO_priors 12.5, EHVI x POF 5.0, pEHVI **0**, random **0**. Final feasibility-classifier F1: 0.81 / 0.44 / 0.68 / 0.19 / 0.00.
- Fixed-range scaled hypervolume shows the opposite ranking (pEHVI 4.98 > random 4.00 > EHVI x POF 3.61 > no-prior 3.06 > with-prior 2.50). The logged HV is computed over measured points whether or not they are feasible, so in this setting it rewards policies that ignore the constraints. Use the feasibility counts, not HV, when comparing policies.

**Problems found.**
- No dependency or path problems. The scripts take a `--data-path` flag, and `design_space.csv` ships with the repo, so nothing is missing.
- EHVI x POF and pEHVI log very large acquisition values early in a run, for example `[Seed 2, Iter 001] idx=40345 | PHASE-ONLY (non-BCC) | Pareto?=No | acq=3.071e+18`. This looks like an unnormalised EHVI term before the GP has data. It is not fatal, but it makes the first picks effectively arbitrary.
- `plot_metrics.py` hard-codes three directory names (`results_const_no_prior`, `results_const_prior`, `results_opt`); it only works on other names through `--auto`.
- The default `--workers 25` would oversubscribe most machines; set it explicitly.
- `campaign_ehvi_pofcorr.py` takes over 100 s per iteration on a 40k-point pool because of `mvn.cdf(z[i:i + POF_BATCH])` (line 732). At the default 200 seeds x 100 iterations that is out of reach without subsampling the pool or using a cheaper joint-feasibility approximation.

**Relevance to us.** High. This is the clearest ArroyaveLab example of **constraint-first BO with physics priors as GP mean functions**. It maps directly onto LPBF printability constraints (keyhole/lack-of-fusion/cracking) and Al-alloy composition constraints, with Thermo-Calc or Eagar-Tsai predictions as priors. It works on a discrete pool and does one point per iteration (no batch), in plain scikit-learn rather than BoTorch.

TABLE: constraint-satisfaction | PASS (py3.11, unpinned sklearn stack, 3 s) | 5 of 6 campaign scripts PASS (2 seeds x 20 iters, 23-35 s each) + plot_metrics.py; ehvi_pofcorr timed out (2-3 iters in 300 s) | PASS | with-prior finds 13/24 truly feasible alloys in 20 iters vs 0 for random/pEHVI; logged HV ignores feasibility
