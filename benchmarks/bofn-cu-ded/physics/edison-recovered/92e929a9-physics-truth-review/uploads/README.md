# A physics-based truth for the copper/DED benchmark

Asked on PR 206: the hand-written truth lets nothing below about 6 wt% Ni pass 30-day immersion. Is that real? Should the search space be restricted? Use real simulations (pycalphad, electrochemistry) where possible instead of synthetic functions.

This folder replaces the composition dependence of the hand-written truth (`../bofn_alloy.py`, `AlloyTruth`) with pycalphad calculations and a corrosion model fitted to measurements. It also adds the proposal's own limits on the search space. It is opt-in (`BOFN_TRUTH=phys`); with the variable unset, every stored run reproduces exactly (checked on `random` seed 0).

## Answer in brief

- **The ~6 wt% floor came from a formula, not from data.** The hand-written immersion index is `m = 0.30 + 0.55 (1 - exp(-Ni/0.15)) + 0.15 Al + ...`. With Ni = 0 it cannot exceed about 0.57, against a pass mark of 0.849.
- **No published study compares these alloy families in one 30-day test against 70-30 Cu-Ni** (two Edison literature queries, [`edison/same-test-rates.md`](edison/same-test-rates.md) and [`edison/kinetics-constants.md`](edison/kinetics-constants.md)). The same-test data that do exist are older and partly unpublished. Fitting a film model to them gives:
  - aluminum barely helps over a month (aluminum bronze loses about twice as much as 70-30);
  - iron in solution helps a lot, up to about 1.5 wt% (a threefold cut in Cu-10Ni);
  - nickel's benefit grows roughly linearly up to 30 wt% rather than saturating at 10.
- **So the floor goes up, not down.** Under H5 as written (mass loss no greater than dense 70-30), nothing with less than about **15 wt% Ni** passes, and even 90-10 fails (it loses 1.24 times as much). With 90-10 as the bar, the floor is about **9 wt% Ni**.
- **Yes, restrict the search space, or change the bar.** If H5 keeps 70-30 as the reference, the measurements say a lab should not search below about 10 to 15 wt% Ni, which works against the proposal's low-nickel aim. With 90-10, the Navy's standard seawater piping alloy, as the bar, the floor is about 9 wt%. That choice is for the proposal. The runs here use the 90-10 bar, in the proposal's space and with a 10 wt% Ni floor.
- **How firm this is.** The fit rests on a handful of same-test ratios, some conflicting. One measurement contradicts it: Yang et al. 2018 found Cu-7Ni-3Al-1Fe-1Mn corroding 40% less than C70600 in a 10-day test; the model puts it 28% above. The model also has no Al-Ni interaction. The CALPHAD database is a Ni-superalloy database (see Caveats). Read the floor as "about 10 wt%, give or take a few", not as a constant.

![immersion maps](../bofn_cu_phys_immersion_map.png)

*Can a (Ni, Al) pair pass 30-day immersion? Color: the best immersion margin over Fe, Mn and the process settings (a, P, v); black line: the pass boundary. Left: the hand-written truth. Middle and right: the physics-based truth with 70-30 (H5 as written) and 90-10 as the bar, inside the proposal's limits (hatched: outside them for every Fe and Mn).*

## What is simulated, what is fitted, what is assumed

| Node | Hand-written truth | Physics-based truth | Source |
|---|---|---|---|
| CALPHAD `f` (crack index) | `0.65 Ni + 0.30 Mn - 0.35 Al + 2.5 Ni Al + 0.05 Fe` | Scheil freezing range to 99% solid / 250 K | **pycalphad + scheil**, MatCalc `mc_ni` v2.036 |
| CALPHAD `g` (nucleant) | `(0.7 Fe (1 + 0.5 Al) + 0.15 Al Ni) / 1.2` | Fe-rich solid (bcc kappa_I-like or fcc gamma-Fe) in equilibrium with the melt 1 K above the solidus / 0.05 | **pycalphad** |
| CALPHAD `s` (strength) | `(1 - exp(-(0.6 Ni + 0.9 Al + 3 Ni Al)) + 0.1 Fe + 0.05 Mn) / 1.15` | yield-strength estimate: solid solution from the alpha composition at 700 C (3.5, 17, 12 and 10 MPa per wt% Ni, Al, Fe, Mn) plus 600 sqrt(f_kappa) MPa from the kappa fraction at 700 C, (sigma - 70) / 700 | **pycalphad** phases; handbook-scale coefficients |
| CALPHAD `h` (lack-of-fusion threshold) | `0.6 (1 - Ni)^2 (1 - 0.6 Al)` | thermal conductivity from Matthiessen's rule on the alpha composition at 900 C (1.1, 0.65, 2.0 and 2.9 uOhm cm per at% Ni, Al, Fe, Mn; within 20% of the CDA conductivities of C71500, C70600, C61400 and C95800) and the Wiedemann-Franz law, times the solidus rise; pure Cu = 0.95 | **physics** (+ pycalphad solidus) |
| retained beta-prime | `Al^1.5 (1 - Ni/2)` x cooling factor | equilibrium beta fraction at 900 C x the same cooling factor | **pycalphad** |
| 30-day immersion `m`, one-hour screen `w` | hand-written film, Al, Fe and beta terms | paralinear film model (below), integrated over 30 days, or read at 1 hour | model structure from corrosion science; **constants fitted** to same-test data |
| q, rho_u, rho_m, U, objective, costs | | unchanged (the crack onset moved to 200 K of Scheil range so that 70-30, at 162 K, deposits dense; the CALPHAD screen keeps Scheil range <= 125 K) | |

**The pycalphad grid** ([`calphad_grid.py`](calphad_grid.py), [`calphad_grid.csv`](calphad_grid.csv)) covers 9 Ni x 8 Al x 4 Fe x 3 Mn = 864 compositions with the database handling of `near-term-submissions/onr-yip/pycalphad-cu/run_calphad.py` (same file, same sha256). Each composition gets the equilibrium liquidus and solidus (bisection to 0.5 C), the first solid, a Scheil simulation (2 C steps; 810 of 864 converged to the end, and the rest still give the 99%-solid temperature), equilibrium phase fractions at 1,000, 950, ..., 600 C, the alpha composition at 900 and 700 C, and the phases 1 K above the solidus. The run took 2.1 core-hours (about 35 min on the 4-core runner). The truth interpolates the grid multilinearly. That leaves kinks at grid nodes, which is why the optimum sits on one (Ni 15, Al 3, Fe 1.5). A finer grid would move it by up to half a step.

What the grid changes compared with the hand-written functions ([`../bofn_cu_phys_calphad_vs_synthetic.png`](../bofn_cu_phys_calphad_vs_synthetic.png)):

- **Mn dominates the Scheil range.** Cu-10Ni-1.5Fe freezes over 42 K with no Mn, 152 K with 2 wt% Mn and 176 K with 4 wt% (the Mn-enriched last liquid heads for the Cu-Mn minimum). Cu-30Ni with 0.6 Fe and 0.8 Mn: 162 K. Al narrows the range up to about 5 wt% and widens it again once NiAl forms first (Ni >= 5, Al >= 6).
- **Beta is a high-Al, low-Ni, Mn-driven phase.** At 900 C it appears only above about 8 wt% Al with less than about 4 wt% Ni (no Mn). With 2 wt% Mn it starts at about 6.5 wt% Al and reaches about 10 wt% Ni. The hand-written `Al^1.5 (1 - Ni/2)` gives every aluminum alloy some beta and ignores Mn.
- **Nickel goes into NiAl when Al is present.** At 700 C, mc_ni leaves 0.2 wt% Ni in NAB's alpha against about 3 wt% measured. The film model therefore reads the alpha solid solution at 900 C, which the fast cooling of DED retains: 2.4 wt% Ni, 8.1 Al, 2.2 Fe for NAB, close to the measured alpha.
- **The proposal's limits remove 25% of the box:** liquidus <= 1,250 C (58 of 864 grid points exceed it), Cu >= 65 wt% (122 points), Ni >= Fe above 7 wt% Al, and Fe <= 2.3 wt% below 1.5 wt% Al. `feasible()` in [`truth_phys.py`](truth_phys.py) applies them to every candidate pool, perturbation, random design and seed design (`bofn_alloy.sobol`, `local_perturb`, `rand_designs`).

## The corrosion model

Current density (uA/cm2) at time t:

`i(t) = 1 / (1/i_L + 1/sqrt(K_cu q(t) / 2t)) + i_fl q(t)`, with `q(t) = 10^-(fast + slow (1 - exp(-t/tau)))`

- `fast = a_al Al_alpha/7 + a_ni0 Ni_alpha/30`: the Al2O3-rich layer and Ni in the metal act at once.
- `slow = a_ni Ni_alpha/30 + a_fe min(Fe_solution, 1.5)/1.5`: Ni and Fe enrich the Cu2O film as it matures.
- The first term is an O2-diffusion-limited cathode in series with parabolic film growth. The second is steady dissolution of the film (paralinear kinetics; copper's own rate barely falls after the first week).
- Retained beta-prime adds `beta x i_sel` after a one-day incubation. Porosity multiplies the mass loss by `1 + (1 - rho_m)`.
- `m = 1 - log10(M30 / 22) / 1.5`. The gate's width of 0.05 in `m` is therefore a 19% change in mass loss.
- The one-hour screen reads `i(1 h)`, which sees the fast terms but only 0.4% of the film's maturation (tau = 10 days), and none of the beta attack (eta = 1).

**Fit** ([`calibrate_corrosion.py`](calibrate_corrosion.py), output in [`calibration_fit.txt`](calibration_fit.txt)): Nelder-Mead on log-ratio residuals. Same-test data only, each used inside its own test:

| Target | Measured | Model |
|---|---|---|
| 90-10 / 70-30 mass loss over 30 days | 0.95 (30 d, 2 m/s), 2.1-2.5 (62 d, 0.15 m/s), 1.5 (1 y); target 1.4 | 1.24 |
| Cu / 70-30 | about 3 (2-h ratio 3.2; long-term 2-10) | 3.47 |
| Al bronze / 70-30 | 2.1 (1 y, Inco, grade unreported) | 1.82 |
| Cu-10Ni with 0 / 1.5 wt% Fe, 60 d quiescent 3.4% NaCl | 3.1 (Popplewell, Hart and Ford 1973) | 2.60 |
| late/early rate over 78 days (days 16-78 / 0-5): Cu, Cu-20Ni, Cu-30Ni | 0.70, 0.36, 0.18 | 0.88, 0.34, 0.25 |
| 2-h current, stagnant 3.5% NaCl: Cu, Cu-9.3Ni, Cu-18.8Ni, Cu-28.4Ni, Cu-7Al (uA/cm2) | 7.9, 4.7, 3.8, 2.5, 3.2 (Yang 2019) | 6.0, 5.7, 5.4, 5.0, 5.5 |
| 70-30 mean current over the first month | about 2 uA/cm2 (28 um/y over 62 d) | 1.1 |
| *Not fitted:* Cu-7Ni-3Al-1Fe-1Mn / C70600, 10 days artificial seawater | 0.60 (Yang et al. 2018) | 1.28 |

Sources: Lewis and LaQue 1981 (DOI [10.2172/6255887](https://doi.org/10.2172/6255887)), which reproduces the Inco and Wrightsville Beach tests and Popplewell et al. 1973 (DOI [10.1016/0010-938X(73)90007-3](https://doi.org/10.1016/0010-938X(73)90007-3)); Yang 2019 (DOI [10.26190/unsworks/21760](https://doi.org/10.26190/unsworks/21760)); Yang et al. 2018 (DOI [10.3390/ma11091777](https://doi.org/10.3390/ma11091777)).

Fitted constants: a_al = 0.05 (the lower bound), a_ni0 = 0.10, a_ni = 0.51, a_fe = 0.58, tau = 10 days (the upper bound), K_cu = 1e5 (the lower bound, so the paralinear term dominates), i_fl = 3.6 uA/cm2. Three constants sit on bounds, which says the data cannot separate them. The O2 limit (30 uA/cm2) and the beta-prime rate (5 uA/cm2 per unit beta fraction) are priors: no measurement of either was found. Adding the Yang 2018 ratio to the fit moves a_al to 0.17 and leaves the rest within 10%; the model still cannot reproduce that ratio (1.02 against 0.60), because it has no Al-Ni interaction.

**Dense, beta-free coupons** ([`phys_tables.md`](phys_tables.md)): 30-day mass loss relative to 70-30: Cu 3.46, 90-10 1.24, aluminum bronze C61400 1.82, NAB 1.29, Cu-7Ni-3Al-1Fe-1Mn 1.59, the hand-written truth's optimum (13Ni-5.5Al-2.2Fe) 1.31. Mean rates of 13 to 45 um/y over the month, in the measured range for quiet seawater.

## The physics-based landscape

| | Al LPBF (`bofn-prelim`, kappa = 1) | Cu, hand-written truth | Cu, physics-based, 70-30 bar (H5 as written) | Cu, physics-based, 90-10 bar | 90-10 bar, Ni >= 10 wt% |
|---|---|---|---|---|---|
| search space | box | box | proposal's limits (75% of the box) | proposal's limits | proposal's limits, Ni >= 10 (46% of the box) |
| lowest Ni that passes immersion | | ~7 wt% | 14.6 wt% | 9.2 wt% | |
| designs that pass immersion | | 3.2% | 0.14% | 0.70% | 1.1% |
| designs with J > 0 | 28% | 3.0% | 0.01% | 0.24% | 0.29% |
| expected best of 24 random designs (% of J*) | 61% | 10% | -71% | -28% | |
| mean best of the five shared seed designs | +35% | -10% | -106% | -46% | |
| J* (Ni, Al, Fe, Mn wt%) | | 0.49 (13, 5.5, 2.2, 0) | 0.089 (15, 3, 1.5, 0) | 0.190 (15, 3, 1.5, 0) | same optimum |

Reference alloys at their best settings, 90-10 bar ([`phys_tables_c70600.md`](phys_tables_c70600.md)): 70-30 passes (J = -0.07: its 30 wt% Ni costs more burden than its strength earns), 90-10 passes by definition (J = 0.03), aluminum bronze and NAB fail (NAB keeps 0.25 beta-prime at its best settings), and the hand-written optimum's composition (13Ni-5.5Al-2.2Fe) misses narrowly (m = 0.793 against 0.808). Under the 70-30 bar the optimum barely clears zero (J* = 0.089), so policy comparisons normalized by it would be noise. That is why the runs use the 90-10 bar.

<!-- PHYS-RUNS -->

## Caveats

- **The database.** mc_ni v2.036 is a Ni-superalloy database. Its Cu-rich results are extrapolations, with no Cu-Al-Ni ternary parameters, no Cu in NiAl and no gamma-2 (Cu9Al4) phase (`../../../near-term-submissions/onr-yip/pycalphad-cu/README.md`). NAB's computed liquidus is 51 C high, and the Mn effect on beta (0 to 0.90 at 900 C between 0 and 2 wt% Mn for Cu-5Ni-9.5Al-4.5Fe) may be overstated. A Cu database such as TCCU, or a new assessment, would change the numbers, not the method.
- **The corrosion constants.** They come from a handful of same-test ratios measured under different flows and durations, three of them land on bounds, and one same-test result (Yang 2018) contradicts the fit. The structure is standard, but the floor it gives is an estimate. The proposal's own 30-day tests, with a C71500 coupon in every batch, are what would settle it.
- **Strength.** `s` is a handbook-scale estimate from phase fractions, not a fitted strength model. Retained beta still uses the hand-written cooling factor, `sig((v - P + 0.2) / 0.15)`, so a dense deposit keeps 50 to 66% of the high-temperature beta. NAB fails immersion for that reason.
- **The lack-of-fusion threshold.** It falls steeply with a few percent of solute, so in this truth Utah's power cap binds only near pure copper (Cu-2.5Ni already needs only 0.36 of full power). The hand-written truth's required property 4 was a design choice; the physics does not support it.
- **Interpolation.** The grid is multilinear. The optimum sits on a grid node (Ni 15, Al 3, Fe 1.5), and finer grids would shift it.

## Reproduce

```bash
# venv as in ../README.md, plus: pip install pycalphad scheil pandas
python physics/calphad_grid.py                                   # 864 compositions, about 35 min on 4 cores (resumable)
python physics/calibrate_corrosion.py                            # the corrosion fit
BOFN_TRUTH=phys python physics/check_phys.py                     # 70-30 bar: phys_tables.md/json
BOFN_TRUTH=phys BOFN_REF=C70600 python physics/check_phys.py     # 90-10 bar: phys_tables_c70600.md/json
python physics/plot_phys.py maps                                 # the two map figures
physics/run_phys.sh                                              # the runs (results-phys/, results-phys-ni10/)
python physics/analyze_phys.py && python physics/plot_phys.py curves
python physics/edison/lit_queries.py submit|fetch                # the two literature queries
```
