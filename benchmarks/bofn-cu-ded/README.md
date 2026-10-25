# BOFN on a copper/DED network: does choosing the stage beat tiered screening?

Copper and blown-powder DED version of [`../bofn-prelim/`](../bofn-prelim/README.md), the aluminum LPBF benchmark behind the MS&T26 preliminary results, built for the ONR YIP copper proposal (`near-term-submissions/onr-yip/onr-yip-technical-proposal-cu-ded.tex`, Figs. `fig:synth` and `fig:sim`; issue 205). It asks the same question on the copper workflow: with eight priced stages from a $10 calculation to a $3,100 deposition session, does cost-aware partial evaluation (pKGFN, [Buathong et al., ICML 2024](https://proceedings.mlr.press/v235/buathong24a.html)) reach good alloys with less money than tiered screening or whole-pipeline BO? `bofn-prelim/` and its 292 stored runs are unchanged.

<!-- RESULTS -->

## The benchmark

![network](bofn_cu_network_strip.png)

- **Design space (7-D, all scaled to [0, 1]; copper is the balance):** Ni 0 to 30 wt%, Al 0 to 9.5, Fe 0 to 4.5, Mn 0 to 4 (the proposal's Table `tab:space`); ultrasonic atomizer setting; laser power (about 0 to 1 kW; Utah's MX-Lab is capped at 0.5 of the scale); travel speed.
- **Network:** one GP per node, and each node's output feeds its children.
  - CALPHAD and heat flow return four things in one call: strengthening potential `s`, solidification index `f`, nucleant fraction `g` (the iron-rich primary kappa particles) and a conductivity index `h`. The spec named three outputs; `h` was added so the lack-of-fusion term is a function of node inputs.
  - Atomization returns powder quality `q` from the atomizer setting, Mn and `f` (which stands in for the liquidus margin, since both rise with nickel).
  - Small DED at Utah returns a dense, crack-free index `rho_u` from power (capped at 0.5), speed, `f`, `g`, `h` and `q`.
  - Large DED at Mines returns the dense, crack-free fraction `rho_m` from the same inputs at full power. Its GP also takes `rho_u` as an input so the model can learn the small-to-large transfer; the truth links the two only through shared parents.
  - Microscopy returns retained beta-prime `beta` (Al, Ni, P, v, `rho_m`). Tensile returns strength `U` (`s`, `rho_m`, `beta`). The one-hour screen returns `w` and the 30-day immersion `m` (Ni, Al, Fe, `rho_m`, `beta`; the immersion GP also takes `w`, which the truth ignores).
  - The objective is `J = U * sigmoid((m - m_ref) / 0.05) - 0.3 B`: strength, counted only if the alloy passes immersion, minus 0.3 times the critical-mineral burden `B = 1.0 Ni + 0.3 Al + 0.2 Mn` (known and free to compute). `m_ref = 0.849` is the immersion index of 70-30 copper-nickel (C71500) deposited dense at its best settings in the headline world, so "passes immersion" means "no worse than the reference alloy", the proposal's H5 definition. It is fixed in every cell.
- **Costs per query (round all-in estimates: materials, student time, facility time, shipping):** CALPHAD and heat flow $10; ultrasonic atomization of one 0.5 kg lot $400; small DED at the University of Utah $500 (an allowance like SEM time); large DED at the Colorado School of Mines $3,100 for the first session on a composition ($1,600 for the 2 kg scale-up lot, four more atomizer runs, plus $1,500 for the session: machine time at posted external rates, a certified chemistry check and shipping) and $1,500 for each repeat session on the same lot; microscopy (SEM, EDS, EBSD) $100; tensile $200; one-hour corrosion screen $50; 30-day immersion $400. A full chain on a new composition costs $4,760, so $100k buys about 21 full cycles (PR 86's aluminum chain was $4,210, about 24).
- **Physical rules:** CALPHAD runs automatically before the first experiment on a composition; a 0.5 kg lot must exist before Utah; the scale-up (paid inside the first Mines session) before Mines; a Mines build before microscopy; microscopy before tensile and the screen; the screen before immersion. One lot supports many Utah visits and, once scaled up, four Mines sessions. Reprints and repeat sessions reuse lots.
- **Two bias knobs.** `kappa`: the iron-rich kappa particles nucleate alpha and suppress hot tearing, which a Scheil solidification index cannot see (the copper analogue of Zr inoculation in aluminum, [Martin et al., Nature 2017](https://doi.org/10.1038/nature23894)). At `kappa = 1` they cut the effective index by up to 85%; at `kappa = 0` they do nothing and the screen's physics is right. `eta`: at `eta = 1` the one-hour screen rates fresh films and is blind to the selective attack of retained beta-prime that 30-day immersion finds (welded NAB is attacked selectively in seawater, [Dobson et al. 2024](https://doi.org/10.1016/j.corsci.2024.112004); a quick measurement in air ranked NAB's phases opposite to the order in which they corroded, [Iannuzzi et al. 2017](https://doi.org/10.1149/2.0391709jes)) and to the slow-forming film of low-nickel alloys; at `eta = 0` it agrees with immersion up to its constants. Headline cell `(kappa, eta) = (1, 1)`; sensitivity cells (0, 0), (1, 0) and (0, 1).
- **New for copper: lack of fusion.** `lof = sigmoid((h - P) / 0.08)` with `h = 0.6 (1 - Ni)^2 (1 - 0.6 Al)`: copper-rich, high-conductivity compositions need more laser power than Utah's cap gives, so the small step is blind exactly where Mines can still fuse them.
- **Shared start:** every policy and seed starts from the same data: CALPHAD on 32 compositions plus five random designs carried through every stage (Utah included). That seed data is sunk, and the x-axis counts only new spend, up to $100k.
- **Scoring:** "best alloy demonstrated" is the true `J` of the best design deposited at Mines and carried through tensile *and* immersion. pKGFN gets no credit for builds it has not tested. `rec_printed` (the deposited alloy the policy's own model ranks best, tested or not) is kept as a secondary metric.

## The truth functions and the optimum

Hand-written closed forms on [0, 1] inputs, nothing fitted, as in PR 86. The spec gave the shapes and left the constants to this implementation; where the constants differ from the spec, the reason is the required property they serve (checked by [`check_truth.py`](check_truth.py), which writes [`truth_tables.md`](truth_tables.md)). `sig` is the logistic function.

| Node | Function (inputs on [0, 1]) | Differs from the spec |
|---|---|---|
| strengthening `s` | `(1 - exp(-(0.6 Ni + 0.9 Al + 3.0 Ni Al)) + 0.1 Fe + 0.05 Mn) / 1.15` | constants: a stronger Ni-Al (kappa-III, NiAl) synergy |
| solidification index `f` | `clamp(0.65 Ni + 0.30 Mn - 0.35 Al + 2.5 Ni Al + 0.05 Fe, 0, 1)` | Ni-Al term 2.5 (spec 0.6), so the Ni-Al corner freezes wide again, as the `mc_ni` composition map shows |
| nucleant `g` | `(0.7 Fe (1 + 0.5 Al) + 0.15 Al Ni) / 1.2` | Fe linear (spec Fe^1.3) |
| conductivity `h` | `0.6 (1 - Ni)^2 (1 - 0.6 Al)` | an added CALPHAD output; the spec's `cond` |
| powder quality `q` | `exp(-((a - a*)/0.28)^2) (1 - 0.35 f^2)(1 - 0.10 Mn)`, `a* = 0.35 + 0.40 f` | `f` in place of Ni (the spec's node inputs are `a` and `f`) |
| dense, crack-free `rho_m` (Mines) | `window q^0.3 (1 - 0.75 crack)(1 - lof)`, `window = exp(-(u/0.2)^2)(1 - 0.35 sig((P - 0.85)/0.05))`, `u = P - v - (0.05 + 0.25 f)`, `crack = sig((f_eff - 0.56)/0.05)`, `f_eff = f (1 - kappa 0.85 g/(g + 0.12))`, `lof = sig((h - P)/0.08)` | crack onset 0.56 (spec 0.38), so 70-30 Cu-Ni deposits dense at `kappa = 1` |
| `rho_u` (Utah) | the same at `P_u = min(P, 0.5)`, times `(0.95 + 0.05 q)` | none |
| retained beta-prime `beta` | `Al^1.5 (1 - 0.5 Ni) sig((v - P + 0.2)/0.15)` | none |
| strength `U` | `(0.25 + 0.75 s) rho_m (1 + 0.15 beta)` | none |
| immersion `m` | `clamp(0.30 + 0.55 film + 0.15 Al - 0.60 Al beta + 0.30 min(Fe, 0.4) - 0.15 relu(Fe - 0.5) - 0.30 (1 - rho_m), 0, 1)`, `film = 1 - exp(-Ni/0.15)` | the film saturates by 90-10 (spec Ni^0.7) and iron in solution helps it, so 90-10 Cu-Ni passes |
| one-hour screen `w` | `clamp(0.35 + 0.50 n + 0.25 Al - 0.10 (1 - rho_m) - (1 - eta)(0.60 Al beta - 0.30 min(Fe, 0.4)), 0, 1)`, `n = eta (0.4 Ni^0.7 + 0.6 film) + (1 - eta) film` | at `eta = 1` it also misses part of the slow-forming film |
| objective | `U sig((m - 0.849)/0.05) - 0.3 (Ni + 0.3 Al + 0.2 Mn)` | none |

The CALPHAD crack screen keeps compositions with `f <= 0.34` (about 1% crack probability at `kappa = 0`). The one-hour screen's gate, for the policies that use it, is the top quartile of every screened build so far.

<!-- TRUTH -->

## Policies (all on equal $100k of new spend)

| Policy | What it does each step |
|---|---|
| **pKGFN** | For each stage (CALPHAD; atomize a simulated composition; Utah or Mines on an existing lot; microscopy, tensile, screen or immersion on an existing build), it computes the knowledge gradient per dollar of one more query and buys the best one. It also prices three test bundles (microscopy + tensile, microscopy + screen + immersion, screen + immersion), each valued by the knowledge gradient of its last stage with the intermediate outputs at their posterior means, because one-step KG gives microscopy almost no value of its own (its value is to unlock the tests). |
| BOFN, full pipeline (EIFN) | The same network model. It picks a design by network expected improvement, then runs all eight stages on it ([Astudillo & Frazier 2021](https://arxiv.org/abs/2112.15311)). |
| Tiered screening | A careful lab: CALPHAD on 256 compositions; keep the four strongest with `f <= 0.34`, net of burden; then EI on its own records over those four, where each step is a chain: Utah tracks (at Utah's capped power, on the same energy-density line), Mines only if the small blocks reach the density target (`rho_u >= 0.5`; a lot that passed once is not re-checked), microscopy, tensile, the screen, and immersion only if the screen passes. Lots and scale-ups are reused. |
| Standard BO (EI) | A single GP from the 7 inputs to the objective, all eight stages run per design. |
| Random | Uniform designs, all eight stages run. |
| *Ablation:* BOFN + lot reuse | Network EI per dollar over new designs *and* new Mines sessions on existing lots (every later stage runs). This is partial evaluation without KG's choice of stage. |
| `pkgfn_screen` | pKGFN that trusts the screens: it does not atomize a composition the CALPHAD screen rejects, does not send a lot to Mines before its Utah blocks pass the density gate, and does not immerse a build the one-hour screen stops. |
| `pkgfn_audit` | `pkgfn_screen` with Advance 5's audit: about one in ten candidates a screen would stop goes on anyway (a fixed hash of seed, gate and candidate), plus every candidate that misses a cutoff by less than 0.03 (the CALPHAD screen, the one-hour screen) or 0.05 (the Utah density gate). |
| `mines_only` | pKGFN with the Utah stage removed: every composition goes straight to a 2 kg lot and Mines. The difference to pKGFN is what the two-step DED split buys, the premise of the budget. |
| `funnel` | A fixed top-k funnel at every gate (Reyes, Liu and Diaz Vargas, JOM 2022, found that a sensible funnel can lose to random): the CALPHAD shortlist's top 12, atomized at a = 0.5; the top 6 by powder quality; three Utah settings each and the top 3 by density; two Mines sessions each; the top 3 by the screen go to immersion; then the tiered loop on the finalists. Each gate's false rejections are judged from the truth afterwards. |

### pKGFN implementation notes

[`bofn_alloy.py`](bofn_alloy.py) implements the method from scratch, as `bofn-prelim` does, and does not use the upstream `partial_kgfn` package.

- **GPs:** each node is an exact GP with BoTorch-fitted RBF hyperparameters; fantasy updates are closed-form rank-one, so every KG candidate is scored in one vectorized pass. Fit failures are counted (`gp_fits` in every run JSON).
- **KG:** the inner max runs over a shared design set anchored on the incumbent; fantasies use 10 Gauss-Hermite nodes, and a 2-point-per-output product rule (16 points) for the four CALPHAD outputs. The current value comes from the same fantasy-averaged estimator, so the estimated KG is never negative. Base samples are common random numbers.
- **Candidates** for each stage are the EI-ranked members of a Sobol pool plus perturbations of validated designs. They are ranked by network EI over the best alloy demonstrated so far, as in EIFN. The aluminum version measured EI from the best posterior mean; on this network that is a pure-copper design whose immersion gate is shut (its burden is zero and so is its strength once gated), every EI came out zero, and on one seed the first runs stopped after $4,750. Ties at zero EI are broken by the posterior mean.
- **Fallback:** when KG is numerically zero for every candidate, the policy buys the candidate with the highest network EI per dollar of the cheapest path to a validated build (this purchase plus whatever Mines session and tests it still needs), and if every EI is zero too, the one with the most optimistic posterior sample, so it never stops with money left. The aluminum version divided EI by the cost of the next stage alone. On the copper network, where KG is often flat until some alloy passes immersion, that made the first headline runs buy 58 to 68 lots and 87 to 121 Utah sessions per $100k and validate almost nothing (seeds 2 and 3 ended below zero); those runs were discarded and the sweep restarted. The share of purchases made by the fallback is in the quality table.
- **Lighter MC settings than PR 86:** 32 base samples, 10 candidates per stage and a 256-point Sobol pool per iteration (PR 86: 64 and 16), because the copper network has eight stages and three test bundles to score.

## Caveats (read before quoting numbers)

- **Synthetic truth.** The node functions are hand-built to mirror the qualitative metallurgy (solid-solution and kappa strengthening, a Scheil-type crack criterion with nucleant-driven suppression, a constant-energy-density process ridge with keyholing and lack of fusion, a nickel film, selective attack of beta-prime). Nothing is fitted to data. The bias knobs are the places the benchmark is designed to make the screens wrong.
- **At `kappa = 0`, 70-30 Cu-Ni cracks.** In the world where the Scheil index is taken as exactly right, the wide Scheil range of 70-30 Cu-Ni (`f = 0.72`) makes it crack (`rho_m = 0.26` at its best settings) and fail immersion. 70-30 copper-nickel is routinely welded, which is one reason to read `kappa = 1` as the more realistic copper world, but the sensitivity cells keep `kappa = 0` as the case where the crack screen is right.
- **The one-hour screen never stops the optimum.** In every cell the optimum ranks in the top quartile of dense candidates on the one-hour screen, so the screen's blind spot (`eta = 1`) costs wasted immersions and false rejections of other candidates, not the optimum itself. The CALPHAD screen is the one that cuts the optimum off at `kappa = 1`.
- **Simplifications.** Observations are noise-free. There is one scalar objective (strength gated by immersion, minus the burden), not the proposal's several objectives (Advance 1). One experiment at a time, with no delays (the delays are in `step-costs` but not modelled; Advance 2 is future work). One parameter set per Mines build.
- **Costs.** The step costs are the project's own round all-in estimates. Outside the loop and not modelled: the yearly gas atomization of the finalist (about $12,500 a run), the combustible-dust tests, and the flowing-seawater tests at Carderock (free to the project, months).
- **pKGFN implementation.** It is discrete and one-step myopic, with lighter MC settings than PR 86. Treat its numbers as those of this implementation at these settings.

## Reproduce

```bash
python -m venv /tmp/bofn-venv && /tmp/bofn-venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
/tmp/bofn-venv/bin/pip install botorch matplotlib scipy
cd benchmarks/bofn-cu-ded
python check_truth.py             # required properties, truth_tables.md
logs/plan.sh                      # the sweep in priority order (resumable; one JSON per run)
python analyze.py                 # tables.md
python plot.py                    # figures
```

The figures need the Aptos fonts in `~/.local/share/fonts/aptos/` (Microsoft's zip: `download.microsoft.com/download/8/6/0/860a94fa-7feb-44ef-ac79-c072d9113d69/Microsoft%20Aptos%20Fonts.zip`).

Per-run JSON (every purchase, spend and score, the builds and lots, GP-fit counts, and for the audit the screen and immersion events) is in `results/k<kappa>e<eta>/<policy>_s<seed>.json`.
