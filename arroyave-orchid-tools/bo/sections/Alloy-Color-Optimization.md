## Alloy-Color-Optimization

**What it is.** The figure-reproduction code for "Jeweler-in-the-Loop: Personalized Alloy Color Optimization via Preference-Based BO". It runs a BoTorch `PairwiseGP` preferential-BO over 933 quinary (E1–E5, element names obfuscated) jewelry alloys whose colors came from Thermo-Calc's Optical Properties model. A two-objective EHVI variant trades color preference against alloy price ($/g). A third script regenerates colors through TC-Python.

**Declared dependencies.** From the README: numpy, pandas, matplotlib, torch, botorch, gpytorch, linear_operator and pillow (no pins, "Python 3.9+"). `color_dataset_generation.py` also needs `tc_python` and a Thermo-Calc licence with the TCNOBL3 database.

**Commands**
```bash
cp -r /tmp/arroyave/src/ArroyaveLab__Alloy-Color-Optimization /tmp/arroyave/work/Alloy-Color-Optimization
/tmp/sbx/clean bash -c "uv venv --python 3.12 /tmp/arroyave/venvs/Alloy-Color-Optimization && uv pip install --python /tmp/arroyave/venvs/Alloy-Color-Optimization/bin/python --torch-backend cpu numpy pandas matplotlib torch botorch gpytorch linear_operator pillow"
cd /tmp/arroyave/work/Alloy-Color-Optimization   # all three runs below are wrapped in /tmp/sbx/clean timeout 400 bash -c "..."
CUDA_VISIBLE_DEVICES= python pref_gold_optimization.py --csv color_quinary_5%.csv --color-plot images/color_progress.png --tournament-plot images/tournament_progress.png --rgb-space-plot images/rgb_projections.png
CUDA_VISIBLE_DEVICES= python multiobjective_ehvi.py --csv color_quinary_5%.csv --plot out/multiobj_objectives.png
python color_dataset_generation.py --in color_quinary_5%.csv --out /tmp/x.csv          # needs Thermo-Calc
python -I /tmp/arroyave/results/bo/scripts/Alloy-Color-Optimization-rank.py /tmp/arroyave/work/Alloy-Color-Optimization data/Alloy-Color-Optimization-summary.json
```
Resolved versions: torch 2.15.0+cpu, botorch 0.18.1, gpytorch 1.15.2, linear-operator 0.6.1, numpy 2.5.4 and pandas 3.1.1, all on Python 3.12. No scale-down was needed: the defaults are already small (pref-BO uses 3 initial points and 10 iterations with seed 42; EHVI uses 5 initial points and 15 iterations with seed 0).

**Outcome: PASS** for both BO scripts, which ran unmodified on the latest stack. **NOT RUNNABLE** for `color_dataset_generation.py`, which needs a Thermo-Calc licence: `ModuleNotFoundError: No module named 'tc_python'`.

**Timings.** Install took about 1 s from cache. Preference BO ran in **30 s** and the EHVI run in **68 s**.

**Key numbers** (`data/Alloy-Color-Optimization-summary.json`; figures `figures/Alloy-Color-Optimization-color_progress.png` and `-multiobj_objectives.png`)
- **Preference BO** reached gold-likeness **0.9968** at iteration 7, 10 evaluations in total. That is the **global maximum** of the 933-alloy dataset (rank 1/933; the runner-up is 0.9940). The best value after the 3 random initial points was 0.8503.
- **EHVI (color vs price)** raised hypervolume from 0.5023 at iteration 1 to **0.5948** at iteration 15. Every one of the 15 BO picks costs **$36.9–50.3/g**, against a dataset price range of $3.9–50.3/g with a median of $15.4/g. The first pick was the single most expensive alloy in the set. See problem 2.

**Problems found**
1. **Printed Pareto front has the wrong sign** (multiobjective_ehvi.py:323): `pareto_mask = is_non_dominated(train_obj)`. BoTorch's `is_non_dominated` assumes maximization, but `train_obj` holds the *minimized* quantities (color distance, price), so the console prints the anti-Pareto set. The run's list includes `(0.0202, $48.81/g)` and `(0.0528, $47.36/g)`, both dominated by the queried point `(0.0102, $42.50/g)`. The plot function gets it right with `is_non_dominated(-pareto_tensor)` (line 141), so only the text output is wrong. Fix: `is_non_dominated(-train_obj)`.
2. **Likely sign and scale mismatch in the EHVI acquisition**, found by reading the code and consistent with the run. `price_gp = SingleTaskGP(compositions, price_norm_all)` models **+price**, while the hypervolume partitioning uses `train_y = -train_obj`, that is **−price**, and BoTorch EHVI maximizes every model output. A higher predicted price therefore counts as *more* improvement, which matches the BO picking only the most expensive alloys. The color output is a `PairwiseGP` latent utility on an arbitrary scale, whereas the partitioning uses min–max-scaled color distance in [−1, 0]. **Empirical check:** a two-line patch (`scripts/Alloy-Color-Optimization-signfix.sh`) makes the price GP model −price and fixes the printed front. With the same seed and budget, the BO picks now span **$3.9–38.4/g**, including the cheapest alloy in the dataset at iteration 14. Final HV is **0.8158, against 0.5948** unpatched, under the script's own running scaling, so the comparison is approximate. The printed front is now a valid minimization front. Logs: `logs/Alloy-Color-Optimization-ehvi-signfix.log`; figure: `figures/Alloy-Color-Optimization-multiobj_objectives_signfix.png`. The color-scale mismatch remains. A full fix would also put both objectives on matching scales, or build the front from the latent utility.
3. Very frequent `NumericalWarning: A not p.d., added jitter of 1.0e-02 to the diagonal` from the PairwiseGP Laplace fits (15 in the pref run alone, trimmed from the logs), plus `FutureWarning: torch.jit.script is deprecated` and a BoTorch `UserWarning` about `torch.tensor(ref_point)` copy construction.
4. Running the pref script with the README paths overwrites the committed `images/*.png`. I ran it on a copy.

**Relevance to us.** Medium. Preferential BO (`PairwiseGP`) is a good pattern for human-in-the-loop judgments such as "this melt-pool cross-section or surface looks better". A cost-aware EHVI over a discrete composition set is close to our supply-risk or cost objective. Reuse the structure, not the code as is, because of the sign bug in problem 2.

TABLE: Alloy-Color-Optimization | OK (py3.12, latest botorch 0.18.1, CPU torch) | pref-BO 30 s + EHVI 68 s, defaults; TC-Python data script needs licence | PASS (BO) / NOT RUNNABLE (TC script) | pref-BO finds global best (0.9968, rank 1/933) in 10 evals; EHVI price objective sign-flipped (models +price vs −price front; 2-line fix raises final HV 0.595→0.816) and printed Pareto is anti-Pareto
