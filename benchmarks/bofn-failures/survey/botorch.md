<!-- Written on 2026-11-26 for issue #274 by a research agent working for Claude; key behaviours were checked by running BoTorch 0.18.1 (verify/). -->
# BoTorch digest: failed experiments, unknown constraints, partial (stage-level) data, function networks

**Scope.** `meta-pytorch/botorch`, `main` @ [`12c754c2986e19d8a6435c0413f7635c1bd9e68c`](https://github.com/meta-pytorch/botorch/commit/12c754c2986e19d8a6435c0413f7635c1bd9e68c) (2026-11-25; latest release v0.18.1, 2026-06-08). Fetched 2026-11-26: all 639 issues, 2,560 PRs (with reviews/inline comments) and 340 discussions (downloaded with `scripts/botorch_fetch.py`; not committed), searched for 70 terms (`hits.tsv`, 3,287 hits, bot comments excluded). Branches: only `main`, `archive`, `gh-pages*`, and one dependabot branch. **No branch touches constraints, failures, networks, or partial evaluation.** I checked claims marked *[verified]* against the installed BoTorch 0.18.1 / GPyTorch 1.15.2 (`verify/`).

`B` = `https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c`. All code links below are pinned to that SHA.

## Key findings

1. **BoTorch has no model for experiments that fail.** The supported pattern is a classifier, as a probability callable, with `fat=None` ([#2776](https://github.com/meta-pytorch/botorch/pull/2776), v0.14.0), shown in the community notebook [clf_constrained_bo](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/notebooks_community/clf_constrained_bo/clf_constrained_bo.ipynb) ([#2700](https://github.com/meta-pytorch/botorch/pull/2700)). Meta's own classifier models never landed: RF/SVC/XGBoost [#3082](https://github.com/meta-pytorch/botorch/pull/3082) was closed unmerged, and SoftKNN [#3243](https://github.com/meta-pytorch/botorch/pull/3243) is still open.
2. **`fat=None` only works in half of the code.** In v0.18.1 and on `main`, the hard feasibility check still assumes `g<=0`. A probability constraint therefore marks every baseline point infeasible, which corrupts the qNEI/qLogNEI incumbent, baseline pruning, and the NEHVI baseline. The fix is the open PR [#3574](https://github.com/meta-pytorch/botorch/pull/3574) (2026-11-25). *[verified]*: 0% of baseline samples were counted feasible and the "all infeasible" warning fired. A logit-form constraint avoids this today (§f2).
3. **Knowledge gradient has no constraint support,** and there is no function-network, EIFN, KGFN or pKGFN code. Maintainer: "KG doesn't support constraints (no published work on it)" ([sdaulton](https://github.com/meta-pytorch/botorch/discussions/2292#discussioncomment-9088696)). BOFN and pKGFN appear only as entries in [`docs/papers.md` L35](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/docs/papers.md?plain=1#L35) and [L99-L100](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/docs/papers.md?plain=1#L99-L100).
4. **The `RuntimeError: shape ... is invalid` has two independent causes:**
   - **Base-sample shape change.** [#1486](https://github.com/meta-pytorch/botorch/pull/1486) (v0.8.0) dropped the trailing output dimension from single-output `base_sample_shape`. [#2254](https://github.com/meta-pytorch/botorch/pull/2254) (v0.11.0) then removed the `rsample(base_samples=)` shim that used to absorb it. *[verified]*
   - **GPyTorch bug** with fantasized, batched multi-output nodes ([#3336](https://github.com/meta-pytorch/botorch/issues/3336), opened from a pKGFN port). The fix is [GPyTorch PR 2762](https://github.com/cornellius-gp/gpytorch/pull/2762), still open.
5. **Maintenance is reduced.** Meta's Adaptive Experimentation team was disbanded and on-call support ended ([#3308](https://github.com/meta-pytorch/botorch/issues/3308), 2026-05-21). Pending-point fixes [#3378](https://github.com/meta-pytorch/botorch/pull/3378)/[#3379](https://github.com/meta-pytorch/botorch/pull/3379) and the constraint fix [#3575](https://github.com/meta-pytorch/botorch/pull/3575) are on `main` but not in any release.

---

## (a) Code-level tools (pinned)

### (i) Outcome constraints in MC acquisition functions

- **Where constraints are applied.** [`SampleReducingMCAcquisitionFunction`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/monte_carlo.py#L146-L348) computes the utility for each MC sample, multiplies it by a smoothed feasibility indicator (or adds it in log space), and then reduces ([`_apply_constraints` L322-L348](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/monte_carlo.py#L322-L348)).
  - Constraint callables map `samples → b×q`, with negative values meaning feasible.
  - Weighting requires non-negative utilities in non-log acqfs.
  - Defaults: `eta=1e-3`, `fat=False` ([L187-L266](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/monte_carlo.py#L187-L266)). The LogEI family uses `fat=True` by default ([`logei.py` L72-L140](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/logei.py#L72-L140)) and refuses `ConstrainedMCObjective` ([L121-L126](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/logei.py#L121-L126)).
- **Smoothing.** [`compute_smoothed_feasibility_indicator`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/objective.py#L135-L211) applies, per constraint:
  - `fat=False`: a sigmoid (`logexpit`);
  - `fat=True`: a fatmoid ([`log_fatmoid` L434-L458](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/safe_math.py#L434-L458));
  - `fat=None`: no transform. The callable must return a probability, and its log is taken ([L204-L209](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/objective.py#L204-L209)).

  `eta` may differ per constraint ([#1526](https://github.com/meta-pytorch/botorch/pull/1526)).
- **Hard indicator.** [`compute_feasibility_indicator`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/objective.py#L101-L132) tests `constraint(samples) <= 0` ([L120-L123](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/objective.py#L120-L123)). It feeds:
  - [`compute_best_feasible_objective`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/utils.py#L98-L179), which gives the incumbent for qNEI/qLogNEI;
  - [`prune_inferior_points`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/utils.py#L355-L449) (pruning is on by default since [#2762](https://github.com/meta-pytorch/botorch/pull/2762));
  - the NEHVI baseline ([`hypervolume.py` L736-L743](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/multi_objective/hypervolume.py#L736-L743)).

  This test is the source of the `fat=None` mismatch in Key finding 2.
- **When nothing is feasible.** BoTorch warns "better to use q(Log)ProbabilityOfFeasibility" ([L160-L165](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/utils.py#L160-L165)). It then sets the incumbent from [`_estimate_objective_lower_bound`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/utils.py#L182-L220), which calls [`get_infeasible_cost`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/utils.py#L223-L281): the 6-sigma bound, per outcome since [#1191](https://github.com/meta-pytorch/botorch/pull/1191). This behaviour comes from the [#3009](https://github.com/meta-pytorch/botorch/issues/3009) → [#3011](https://github.com/meta-pytorch/botorch/pull/3011) fix in v0.16.0.
- **Legacy path.** [`ConstrainedMCObjective`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/objective.py#L402-L482) and [`apply_constraints`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/objective.py#L214-L254) weight samples of f rather than samples of the utility. Maintainers prefer the per-sample-utility path ([sdaulton](https://github.com/meta-pytorch/botorch/discussions/2292#discussioncomment-9072552), [SebastianAment](https://github.com/meta-pytorch/botorch/discussions/2292#discussioncomment-9073098)).
- **Analytic, q=1.** [`LogConstrainedExpectedImprovement`, `LogProbabilityOfFeasibility`, `ConstrainedExpectedImprovement`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/analytic.py#L432-L761) take `{i: (lower, upper)}` bounds on Gaussian outputs. A t-batch bug was fixed in [#3028](https://github.com/meta-pytorch/botorch/pull/3028) ([#3022](https://github.com/meta-pytorch/botorch/issues/3022)).
- **Multi-objective and Thompson sampling.**
  - qLogEHVI/qLogNEHVI add the log feasibility ([`multi_objective/logei.py` L289-L298](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/multi_objective/logei.py#L289-L298)), with `eta=1e-2` for qLogEHVI.
  - [`FeasibilityWeightedMCMultiOutputObjective`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/multi_objective/objective.py#L144-L207).
  - SCBO-style [`ConstrainedMaxPosteriorSampling`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/generation/sampling.py#L226-L357).
- **Docs.** [`docs/constraints.md` L27-L45](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/docs/constraints.md?plain=1#L27-L45): with independent objective and constraint models, constrained EI equals EI × P(feasible).

### (ii) Probability of feasibility and classifier constraints

- **PoF acquisition functions.** [`qLogProbabilityOfFeasibility`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/logei.py#L581-L673) and the analytic [`LogProbabilityOfFeasibility`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/analytic.py#L622-L680) arrived in [#2815](https://github.com/meta-pytorch/botorch/pull/2815) (v0.14.0). They are intended for runs with no feasible point yet. Ax switches to qLogPoF when every observation is infeasible ([Balandat](https://github.com/meta-pytorch/botorch/issues/3009#issuecomment-3307468591)).
- **Classifier as a probability constraint.** Use `constraints=[callable→[0,1]]` with `fat=[None]` ([#2776](https://github.com/meta-pytorch/botorch/pull/2776), designed in [#725](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-2718180986) and [#2700 review](https://github.com/meta-pytorch/botorch/pull/2700#discussion_r1929856321)).
  - Before this, the "unsigmoid" trick was used ([jduerholt/BoFire](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-2612153168)).
  - Open follow-ups:
    - [#3574](https://github.com/meta-pytorch/botorch/pull/3574): hard checks, `fat` typing, clamping p=0.
    - [#3390](https://github.com/meta-pytorch/botorch/pull/3390): `fatmax` gives all-NaN gradients when a classifier returns p=0 exactly.
- **Classifier models.** There is no classifier in `botorch/` or [`botorch_community/models`](https://github.com/meta-pytorch/botorch/tree/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch_community/models). Usable building blocks:
  - [`SingleTaskVariationalGP`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/approximate_gp.py#L301-L522), which takes any GPyTorch likelihood and applies no outcome transform by default.
  - [`ApproximateGPyTorchModel.posterior`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/approximate_gp.py#L148-L182), which returns the **latent** MVN by default. With `observation_noise=True` it returns a `TorchPosterior` wrapping e.g. Bernoulli ([#3242](https://github.com/meta-pytorch/botorch/pull/3242), v0.18.0; [#3066](https://github.com/meta-pytorch/botorch/issues/3066#issuecomment-3482013250)).
  - **SkewGP (exact Bernoulli):** [#1906](https://github.com/meta-pytorch/botorch/pull/1906) was closed unmerged and remains internal ([disc #2790](https://github.com/meta-pytorch/botorch/discussions/2790#discussioncomment-12631104)). Only its probability utilities shipped, in [#1394](https://github.com/meta-pytorch/botorch/pull/1394).
- **Community notebook** "BO with Binary Black-box Constraint" ([ipynb](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/notebooks_community/clf_constrained_bo/clf_constrained_bo.ipynb); site `botorch.org/docs/notebooks_community/clf_constrained_bo`):
  - an `ApproximateGP` with `BernoulliLikelihood` and `VariationalELBO`;
  - `ModelListGP(obj, con)`;
  - `qLogExpectedImprovement(..., constraints=[p(Z)], fat=[None])`, with `p = likelihood(f).probs + 1e-8`;
  - `best_f` set to the best feasible observation.

  Its objective is defined everywhere (Townsend). Real failures leave y missing.

### (iii) NaN and missing outputs; per-output training sets

- **NaN is rejected.** Standard models raise `InputDataError` on any NaN in X, Y or Yvar ([`check_no_nans`/`validate_input_scaling`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/utils/assorted.py#L129-L280)). *[verified]* `Standardize` uses `nanmean`/`nanstd` ([#3072](https://github.com/meta-pytorch/botorch/pull/3072), v0.16.1; [L312-L359](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/transforms/outcome.py#L312-L359)), but that is only for robustness: the model still rejects NaN.
- **`ModelListGP`** ([L23-L39](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/model_list_gp_regression.py#L23-L39)) accepts per-output training sets of different sizes *[verified]*, but not different feature spaces ([Balandat](https://github.com/meta-pytorch/botorch/discussions/2274#discussioncomment-8990802)). For per-model inputs, use [`FilterFeatures`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/transforms/input.py#L1442-L1512) ([saitcakmak](https://github.com/meta-pytorch/botorch/discussions/2274#discussioncomment-8990562)).
- **Correlated outputs with partial observation:**
  - `MultiTaskGP` in long format, one row per (x, task) pair ([Balandat](https://github.com/meta-pytorch/botorch/issues/1674#issuecomment-1430065275)). Unobserved and missing tasks are supported ([#2960](https://github.com/meta-pytorch/botorch/pull/2960), [#3145](https://github.com/meta-pytorch/botorch/pull/3145), [L249-L270](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/multitask.py#L249-L270)).
  - [`LatentKroneckerGP`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/latent_kronecker_gp.py#L59-L674) for NaN-masked grids.
  - [`HeterogeneousMTGP`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/heterogeneous_mtgp.py#L35-L380) for differing search spaces ([#3073](https://github.com/meta-pytorch/botorch/pull/3073); missing-feature imputation in [#3294](https://github.com/meta-pytorch/botorch/pull/3294)).

  With block-design, noiseless data, a multi-task model gives no benefit (autokrigeability; [Balandat](https://github.com/meta-pytorch/botorch/discussions/1771#discussioncomment-5489883)).

### (iv) Pending points with MC acquisition functions

- **How pending points enter.** [`AcquisitionFunction.set_X_pending`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/acquisition.py#L43-L60) stores `X_pending`, detached. [`concatenate_pending_points`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/utils/transforms.py#L378-L404) appends it to every candidate batch, so MC acqfs value `X` jointly with the pending points ([`forward` L268-L290](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/monte_carlo.py#L268-L290)). This amounts to implicit conditioning that lowers the value of points near pending ones ([Balandat](https://github.com/meta-pytorch/botorch/discussions/922#discussioncomment-1269738)).
- **Not supported.** Analytic acqfs raise an error ([L83-L86](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/analytic.py#L83-L86)), as do multi-output acqfs ([L44-L54](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/multioutput_acquisition.py#L44-L54)).
- **qKG** appends pending points to the actual points before fantasizing ([L182-L186](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/knowledge_gradient.py#L182-L186)).
- **qLogNEI** defaults to `incremental=True`, which folds pending points into the baseline ([#2760](https://github.com/meta-pytorch/botorch/pull/2760); [`set_X_pending` L471-L492](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/logei.py#L471-L492)).
  - Since [#3379](https://github.com/meta-pytorch/botorch/pull/3379) (`main` only), a public `X_pending` *replaces* the pending set. Removing an abandoned point is therefore safe only on `main`.
  - Constructor pending points used to be lost in sequential optimization; fixed in [#3378](https://github.com/meta-pytorch/botorch/pull/3378), also `main` only.
  - qNEHVI duplicates: [#2983](https://github.com/meta-pytorch/botorch/issues/2983) → [#2985](https://github.com/meta-pytorch/botorch/pull/2985), v0.16.0.
- **Partial (per-output) pending.** [`DecoupledAcquisitionFunction`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/decoupled.py#L23-L162) takes `X_pending_evaluation_mask` (n′×m), and [`ModelList.fantasize(evaluation_mask=)`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/model.py#L595-L673) does decoupled fantasization ([#1853](https://github.com/meta-pytorch/botorch/pull/1853), v0.9.0). They are used by [qHVKG](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/multi_objective/hypervolume_knowledge_gradient.py#L59-L314) and cost utilities ([#1949](https://github.com/meta-pytorch/botorch/pull/1949)). This is the closest built-in to "stage k pending".
- **Failed-point hack.** Pass NaN or failed points as `X_pending` to "discourage exploration" nearby ([Balandat](https://github.com/meta-pytorch/botorch/issues/2262#issuecomment-2017947549)).

### (v) Function networks, composite functions, partial evaluation, cost

- **No upstream network model.** Searches turned up no `GaussianProcessNetwork`, EIFN, KGFN or pKGFN code, and no PR proposing one.
  - [Disc #2818](https://github.com/meta-pytorch/botorch/discussions/2818) asks how to build a custom variational GP network with Bernoulli nodes; it has no answer.
  - [Issue #3336](https://github.com/meta-pytorch/botorch/issues/3336) (pKGFN port, open) is diagnosed as the GPyTorch `exact_predictive_mean` squeeze bug ([saitcakmak](https://github.com/meta-pytorch/botorch/issues/3336#issuecomment-4960777448)).
- **Closest built-ins:**
  - [`LearnedObjective`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/objective.py#L491-L577): the downstream model is evaluated at upstream samples, with 16 draws per sample, giving a two-layer network. It receives upstream outputs only, not X; pass inputs through with [`GenericDeterministicModel`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/deterministic.py#L67-L134).
  - esantorella's two-stage recipe (`ModelList` + `FilterFeatures` + `LearnedObjective` + qLogNEI). It notes that `q` must be fixed in advance and points to pKGFN ([disc #2400](https://github.com/meta-pytorch/botorch/discussions/2400#discussioncomment-9913975)).
  - Constraints combined with `LearnedObjective`'s extra sample dimension were wrong until [#3575](https://github.com/meta-pytorch/botorch/pull/3575) (`main`; [`repeat_to_match_aug_dim` L52-L95](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/utils.py#L52-L95)).
- **Custom-posterior contract.** [`Posterior`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/posteriors/posterior.py#L19-L145) requires `rsample_from_base_samples`, `base_sample_shape`, `batch_range` and `_extended_shape`. For a single output, [`GPyTorchPosterior.base_sample_shape`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/posteriors/gpytorch.py#L55-L58) is `batch×q`, with **no trailing 1** ([`rsample_from_base_samples` L86-L127](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/posteriors/gpytorch.py#L86-L127)). `get_sampler` raises for unregistered posterior types ([L136-L145](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/sampling/get_sampler.py#L136-L145)), so register one with `GetSampler.register` or pass `sampler=`. `PosteriorList` now samples IID because independently built Sobol samplers were correlated ([L106-L123](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/sampling/get_sampler.py#L106-L123); [#2658](https://github.com/meta-pytorch/botorch/issues/2658) → [#2977](https://github.com/meta-pytorch/botorch/pull/2977)).
- **Cost.** [`InverseCostWeightedUtility`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/cost_aware.py#L86-L221) supports `X_evaluation_mask`. Also relevant: [`qMultiStepLookahead`](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/multi_step_lookahead.py#L51-L322), and `LogEIPerCost` [#3304](https://github.com/meta-pytorch/botorch/pull/3304) (open).

### (vi) 2025–2026 changes and breaking changes for a custom GP network (0.15–0.18+)

**The root-node error, traced.** BOFN calls `node_post.rsample(sample_shape, base_samples[..., [k]])`, and children call `base_samples[..., [k]].unsqueeze(0)` ([BOFN L299-L301, L328-L331](https://github.com/RaulAstudillo06/BOFN/blob/f4fb10b4d06a49410ae49afb32940f820e54d1e9/bofn/models/gp_network.py#L299-L331)). pKGFN's reference code is identical and pins `botorch==0.8.4` ([L402-L404, L438-L442](https://github.com/frazier-lab/partial_kgfn/blob/0754857ef639c59ece7163db78ddfff9bdb90f2e/partial_kgfn/models/decoupled_gp_network.py#L398-L445)). The history:

1. **v0.8.0, [#1486](https://github.com/meta-pytorch/botorch/pull/1486) (2022-11-17).** `base_sample_shape` lost the `+[1]`, and `rsample(base_samples=)` was deprecated. Its shim did `expand(_extended_shape)` and then `squeeze(-1)`, so the trailing dimension still worked (diff: commit `14587f6e5`).
2. **v0.11.0, [#2254](https://github.com/meta-pytorch/botorch/pull/2254) (2024-03-21).** The shim was reaped, so `rsample(..., base_samples)` raises `TypeError`.
3. **Mechanical port.** Rewriting the call as `rsample_from_base_samples(S, base[..., [k]])` passes `S×b×q×1`. GPyTorch's `MultivariateNormal.rsample` infers `sample_shape = base.shape[:base.dim()-loc.dim()]`, which swallows a batch dimension, and fails with `RuntimeError: shape '[16, 4, 4, 1]' is invalid for input of size 64`. With an unbatched X it silently adds a dimension instead. *[verified]* (`verify/botorch_root_node_base_samples.out`)

**Modern pattern** (validated with `optimize_acqf`, q=1 and q=3, on 0.18.1; `verify/botorch_modern_gp_network.py`):
- root nodes: `post.rsample_from_base_samples(S, base[..., k])[..., 0]`;
- children (inputs carry the S dimensions): `post.rsample_from_base_samples(torch.Size([1]), base[..., k].unsqueeze(0))[0, ..., 0]`;
- the network posterior: `base_sample_shape = X.shape[:-1]+(n_nodes,)` and `batch_range=(0,-2)`, with `_extended_shape` written as a *method*. pKGFN made it a `@property`, which is a bug.

**Other breaks that affect BOFN/pKGFN ports:**

| Version | Change |
|---|---|
| 0.11.0 | `fit_gpytorch_model` removed ([#2250](https://github.com/meta-pytorch/botorch/pull/2250)); BOFN imports it |
| 0.12.0 | `FixedNoiseGP` removed ([#2536](https://github.com/meta-pytorch/botorch/pull/2536)); dimension-scaled priors and `Standardize` by default (CHANGELOG 0.12.0); node GP hyperparameters change |
| 0.15.0 | batched L-BFGS-B with independent optimizer state per restart ([#2892](https://github.com/meta-pytorch/botorch/pull/2892)); acquisition values must not couple t-batches |
| 0.16.0 | `condition_on_observations` and input-transform fixes, which matter for fantasizing nodes ([#2989](https://github.com/meta-pytorch/botorch/pull/2989), [#2990](https://github.com/meta-pytorch/botorch/pull/2990), [#3034](https://github.com/meta-pytorch/botorch/pull/3034)); `PosteriorList` IID sampling ([#2977](https://github.com/meta-pytorch/botorch/pull/2977)) |
| 0.17.0 | Python ≥ 3.11; deprecated APIs removed ([#3134](https://github.com/meta-pytorch/botorch/pull/3134)) |
| 0.18.0 | PyTorch ≥ 2.4; NumPyro replaces Pyro; lazy imports ([#3293](https://github.com/meta-pytorch/botorch/pull/3293)); `TorchPosterior` for non-MVN ([#3242](https://github.com/meta-pytorch/botorch/pull/3242)) |
| `main` | fitting on training tensors that have a `grad_fn` now raises `UnsupportedError` ([#3544](https://github.com/meta-pytorch/botorch/pull/3544)), so detach upstream-sample inputs |

## (b) Timeline

| Version / date | PR | Change |
|---|---|---|
| 0.8.0 (Dec 2022) | [#1486](https://github.com/meta-pytorch/botorch/pull/1486) | Posterior/sampler overhaul: `rsample_from_base_samples`; no trailing dimension in base samples |
| 0.9.0 (Jul 2023) | [#1853](https://github.com/meta-pytorch/botorch/pull/1853), [#1949](https://github.com/meta-pytorch/botorch/pull/1949) | Decoupled fantasization; cost utilities with evaluation masks |
| 0.11.0 (May 2024) | [#2254](https://github.com/meta-pytorch/botorch/pull/2254), [#2250](https://github.com/meta-pytorch/botorch/pull/2250) | `rsample(base_samples=)` and `fit_gpytorch_model` removed |
| 0.12.0 (Sep 2024) | [#2536](https://github.com/meta-pytorch/botorch/pull/2536) | `FixedNoiseGP` removed; new default priors |
| 0.13.0 (Feb 2025) | [#2700](https://github.com/meta-pytorch/botorch/pull/2700) | Classifier-constrained community notebook |
| 0.14.0 (May 2025) | [#2776](https://github.com/meta-pytorch/botorch/pull/2776) | `fat=None` probability constraints |
| 0.14.0 | [#2815](https://github.com/meta-pytorch/botorch/pull/2815) | `[q]LogProbabilityOfFeasibility` |
| 0.14.0 | [#2760](https://github.com/meta-pytorch/botorch/pull/2760), [#2762](https://github.com/meta-pytorch/botorch/pull/2762) | Incremental qLogNEI; prune baseline by default |
| 0.14.0 | [#2735](https://github.com/meta-pytorch/botorch/pull/2735) | ModelListGP observation noise without a mask |
| 0.15.0 (Aug 2025) | [#2892](https://github.com/meta-pytorch/botorch/pull/2892), [#2945](https://github.com/meta-pytorch/botorch/pull/2945) | Batched L-BFGS-B; LogPoF input-constructor fix |
| 0.16.0 (Oct 2025) | [#3011](https://github.com/meta-pytorch/botorch/pull/3011) | Incumbent when nothing is feasible, plus the "use qLogPoF" warning |
| 0.16.0 | [#3016](https://github.com/meta-pytorch/botorch/pull/3016) | Worst known feasible value for infeasible trials in test problems |
| 0.16.0 | [#3028](https://github.com/meta-pytorch/botorch/pull/3028) | Analytic constrained t-batch fix |
| 0.16.0 | [#2977](https://github.com/meta-pytorch/botorch/pull/2977), [#2985](https://github.com/meta-pytorch/botorch/pull/2985) | `PosteriorList` IID sampling; qNEHVI pending fix |
| 0.16.0 | [#2960](https://github.com/meta-pytorch/botorch/pull/2960) | Missing tasks in MTGP |
| 0.16.0 | [#2989](https://github.com/meta-pytorch/botorch/pull/2989), [#2990](https://github.com/meta-pytorch/botorch/pull/2990), [#3034](https://github.com/meta-pytorch/botorch/pull/3034) | Conditioning and transform fixes |
| 0.16.1 (Nov 2025) | [#3072](https://github.com/meta-pytorch/botorch/pull/3072) | NaN-robust `Standardize` |
| 0.18.0 (Jun 2026) | [#3242](https://github.com/meta-pytorch/botorch/pull/3242) | Non-MVN `TorchPosterior` |
| `main` (Oct 2026) | [#3378](https://github.com/meta-pytorch/botorch/pull/3378), [#3379](https://github.com/meta-pytorch/botorch/pull/3379) | Pending-point semantics |
| `main` (Nov 2026) | [#3575](https://github.com/meta-pytorch/botorch/pull/3575) | Constraints with `LearnedObjective` |
| Open | [#3574](https://github.com/meta-pytorch/botorch/pull/3574) | `fat=None` everywhere |
| Open | [#3390](https://github.com/meta-pytorch/botorch/pull/3390) | NaN gradients |
| Open | [#3243](https://github.com/meta-pytorch/botorch/pull/3243) | SoftKNN classifier |
| Open | [#3520](https://github.com/meta-pytorch/botorch/pull/3520) | `nanstd` gradients |
| Open | [#3304](https://github.com/meta-pytorch/botorch/pull/3304) | `LogEIPerCost` |
| Closed unmerged | [#3082](https://github.com/meta-pytorch/botorch/pull/3082) | RF/SVC/XGBoost "deterministic failure" models |
| Closed unmerged | [#1906](https://github.com/meta-pytorch/botorch/pull/1906) | SkewGP |

## (c) sgbaird's threads (all 9)

- **[#1220](https://github.com/meta-pytorch/botorch/issues/1220) KG with inequality constraints for constrained multi-fidelity work (open).** It was opened on sgbaird's request.
  - sgbaird's comments: [thanks](https://github.com/meta-pytorch/botorch/issues/1220#issuecomment-1125387237); [the Khatamsaz et al. 2022 alloy example](https://github.com/meta-pytorch/botorch/issues/1220#issuecomment-1227581380); [asks about multi-objective KG](https://github.com/meta-pytorch/botorch/issues/1220#issuecomment-1227582209); [cross-reference to #1100](https://github.com/meta-pytorch/botorch/issues/1220#issuecomment-1319527786).
  - Maintainers: intra-point constraints work in BoTorch's qKG, while inter-point constraints break one-shot initial conditions ([esantorella](https://github.com/meta-pytorch/botorch/issues/1220#issuecomment-1571058228), [Balandat](https://github.com/meta-pytorch/botorch/issues/1220#issuecomment-1569269988)).
- **[#1749](https://github.com/meta-pytorch/botorch/issues/1749) NChooseK and cardinality constraints.**
  - sgbaird: [links the Ax #769/#727 relaxation](https://github.com/meta-pytorch/botorch/issues/1749#issuecomment-1474763398); [2026 note on the BoFire BONSAI scheme](https://github.com/meta-pytorch/botorch/issues/1749#issuecomment-4653922497).
  - Resolved by non-linear constraints with q>1 ([#1793](https://github.com/meta-pytorch/botorch/pull/1793)).
- **[#180](https://github.com/meta-pytorch/botorch/issues/180) and [PR #250](https://github.com/meta-pytorch/botorch/pull/250) heteroskedastic GP.**
  - sgbaird: ["PR never got merged"](https://github.com/meta-pytorch/botorch/issues/180#issuecomment-1162405860); [Noack & Reyes motivation](https://github.com/meta-pytorch/botorch/pull/250#issuecomment-1461228484).
  - Balandat would not land a known-broken model ([comment](https://github.com/meta-pytorch/botorch/issues/180#issuecomment-1162603831)). The issue was closed as inactive in 2026.
- **[#1763](https://github.com/meta-pytorch/botorch/issues/1763) input constructors (open).** sgbaird [added qNIPV](https://github.com/meta-pytorch/botorch/issues/1763#issuecomment-1528839665).
- **[#3308](https://github.com/meta-pytorch/botorch/issues/3308) maintenance update.** sgbaird [offered community help](https://github.com/meta-pytorch/botorch/issues/3308#issuecomment-4932172243). There is no maintainer reply yet.
- **Docs PRs** [#1051](https://github.com/meta-pytorch/botorch/pull/1051) (landed as `72911450a`) and [#1898](https://github.com/meta-pytorch/botorch/pull/1898) (landed as `e5bf538`). [Disc #2214](https://github.com/meta-pytorch/botorch/discussions/2214) is a BO hackathon post.

None of sgbaird's threads covers failures or networks. The closest are #1220 (constrained or cost-aware multi-fidelity) and #3336, which was opened from the lab's own pKGFN port.

## (d) Other relevant threads (one line each)

1. [#725](https://github.com/meta-pytorch/botorch/issues/725): classifier as an output constraint for failed experiments (2021–25). Balandat proposed a probit GP ([comment](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-788031750)). bletham warned that GP classifiers smooth over hard edges and suggested RF/SVM-type classifiers ([1](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-791161534), [2](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-792941614)). mshvartsman suggested Matern, large outputscale, or warping ([comment](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-792131841)).
2. [Disc #1042](https://github.com/meta-pytorch/botorch/discussions/1042): binary outcome constraint. Balandat endorses a Dirichlet GP plus PoF weighting, and mentions SkewGP ([comment](https://github.com/meta-pytorch/botorch/discussions/1042#discussioncomment-1856185)).
3. [Disc #1059](https://github.com/meta-pytorch/botorch/discussions/1059#discussioncomment-1973566): "build a classification model for trial failures … in conjunction with an outcome model".
4. [#943](https://github.com/meta-pytorch/botorch/issues/943#issuecomment-918802564): diverging simulation gives NaN. Advice: random-forest classifier, or impute the "worst outside option" rather than a huge value.
5. [#2262](https://github.com/meta-pytorch/botorch/issues/2262#issuecomment-2017947549): unobtainable points. Advice: a classifier, or NaN points as `X_pending`.
6. [#640](https://github.com/meta-pytorch/botorch/issues/640#issuecomment-749703844): probit `ApproximateGP` in a ModelList; Bernoulli probability-weighted `GenericMCObjective`.
7. [Disc #2424](https://github.com/meta-pytorch/botorch/discussions/2424#discussioncomment-10035703): `SingleTaskVariationalGP`(Bernoulli) + LogCEI on the latent GP. esantorella relates it to "failure-aware BO" and "missing not at random". Pitfall: LogCEI on the latent f gives Φ(μ/σ), not the predictive Φ(μ/√(1+σ²)).
8. [Disc #2401](https://github.com/meta-pytorch/botorch/discussions/2401): variational classifier for simulation crashes; warm-starting a state_dict whose size grows.
9. [PR #2700](https://github.com/meta-pytorch/botorch/pull/2700) and [PR #2776](https://github.com/meta-pytorch/botorch/pull/2776): notebook; per-sample probabilities in the acqf ([SebastianAment](https://github.com/meta-pytorch/botorch/pull/2700#discussion_r1933001918)).
10. [PR #3574](https://github.com/meta-pytorch/botorch/pull/3574) (open): `fat=None` hard-feasibility bug in incumbent, pruning, NEHVI and factories.
11. [PR #3390](https://github.com/meta-pytorch/botorch/pull/3390) (open): p=0 classifier gives NaN gradients through `fatmax`.
12. [PR #3082](https://github.com/meta-pytorch/botorch/pull/3082) (closed) and [#3243](https://github.com/meta-pytorch/botorch/pull/3243) (open): Meta's failure-classifier models (Ax [#4555](https://github.com/facebook/Ax/pull/4555), [#5072](https://github.com/facebook/Ax/pull/5072); both open). jduerholt suggested a RF `EnsembleModel` for uncertainty ([comment](https://github.com/meta-pytorch/botorch/pull/3082#issuecomment-3559091562)).
13. [#3009](https://github.com/meta-pytorch/botorch/issues/3009) / [#3011](https://github.com/meta-pytorch/botorch/pull/3011): degenerate qLogNEI when nothing is feasible. Advice: use qLogPoF ([esantorella](https://github.com/meta-pytorch/botorch/issues/3009#issuecomment-3293143557)).
14. [Disc #2292](https://github.com/meta-pytorch/botorch/discussions/2292): constraint mechanics. KG with `ConstrainedMCObjective` is "not thoroughly evaluated" and "may no longer be non-negative" ([sdaulton](https://github.com/meta-pytorch/botorch/discussions/2292#discussioncomment-9119365)). `best_f` is the same under both paths ([SebastianAment](https://github.com/meta-pytorch/botorch/discussions/2292#discussioncomment-11168786)).
15. [#2851](https://github.com/meta-pytorch/botorch/issues/2851#issuecomment-2876903656): qEI's per-sample weighting equals EI·PoF only under independence. It also handles dependent and non-Gaussian constraints.
16. [#2238](https://github.com/meta-pytorch/botorch/issues/2238#issuecomment-1980068389): safe BO through a chance constraint `γ − P(w(x)>0)` in `nonlinear_inequality_constraints`. Caveat: nothing rewards learning the constraint. Related: BE-CBO, arXiv 2402.07692 ([jduerholt](https://github.com/meta-pytorch/botorch/issues/2238#issuecomment-1980410986)).
17. [#3336](https://github.com/meta-pytorch/botorch/issues/3336): pKGFN multi-output node fantasy shape error; GPyTorch [PR 2762](https://github.com/cornellius-gp/gpytorch/pull/2762) is open.
18. [Disc #2818](https://github.com/meta-pytorch/botorch/discussions/2818): POGPN (partially observable GP network) base-sample questions; unanswered.
19. [Disc #2400](https://github.com/meta-pytorch/botorch/discussions/2400#discussioncomment-9913975): two-stage process A→B→C. Recipe: ModelList, `LearnedObjective`, and pKGFN as the principled option.
20. [Disc #2274](https://github.com/meta-pytorch/botorch/discussions/2274): `ModelListGP` for composite functions; `FilterFeatures`.
21. [Disc #1771](https://github.com/meta-pytorch/botorch/discussions/1771#discussioncomment-5489883): "block design" versus heterotopic data; autokrigeability.
22. [#1674](https://github.com/meta-pytorch/botorch/issues/1674#issuecomment-1430065275): partial observations through a long-format `MultiTaskGP`.
23. [Disc #922](https://github.com/meta-pytorch/botorch/discussions/922#discussioncomment-1239690): the semantics of `X_pending`.
24. [#2983](https://github.com/meta-pytorch/botorch/issues/2983) / [#3378](https://github.com/meta-pytorch/botorch/pull/3378) / [#3379](https://github.com/meta-pytorch/botorch/pull/3379): pending-point bugs in sequential greedy optimization.
25. [#2658](https://github.com/meta-pytorch/botorch/issues/2658): correlated Sobol samples across posteriors. The IID fallback drops QMC ([comment](https://github.com/meta-pytorch/botorch/issues/2658#issuecomment-3330486856)).
26. [#3066](https://github.com/meta-pytorch/botorch/issues/3066) / [PR #3242](https://github.com/meta-pytorch/botorch/pull/3242): `GPyTorchPosterior` assumes an MVN; Bernoulli and Beta give a `TorchPosterior`.
27. [Disc #2790](https://github.com/meta-pytorch/botorch/discussions/2790#discussioncomment-12631104): SkewGP is internal only; [PR #1906](https://github.com/meta-pytorch/botorch/pull/1906) is closed.
28. [Disc #1449](https://github.com/meta-pytorch/botorch/discussions/1449#discussioncomment-3844259): imputing large values for NaN creates artificial discontinuities.
29. [PR #3016](https://github.com/meta-pytorch/botorch/pull/3016): the benchmark convention of scoring infeasible trials at the worst feasible value.
30. [#2938](https://github.com/meta-pytorch/botorch/issues/2938) (open): KG with a fantasized fully Bayesian GP raises `shape ... is invalid`. Fantasization of non-standard models is "not well-tested" ([hvarfner](https://github.com/meta-pytorch/botorch/issues/2938#issuecomment-3117953383)).

## (e) Gaps that matter for multi-stage experiments with stage-level failures

1. **No failure or viability model type,** and no censored or "missing-not-at-random" likelihood. Users build a variational GP classifier themselves (§a-ii). SkewGP, RF/XGBoost and SoftKNN exist only internally or in open PRs.
2. **Probability constraints are inconsistent.** The soft path (`fat=None`) and the hard path (`<= 0`) disagree in v0.18.1 and on `main` ([#3574](https://github.com/meta-pytorch/botorch/pull/3574)). p=0 gives NaN gradients ([#3390](https://github.com/meta-pytorch/botorch/pull/3390)).
3. **No feasibility-aware lookahead.** There is no constrained KG, KGFN, pKGFN, or multi-step lookahead with failures ([sdaulton](https://github.com/meta-pytorch/botorch/discussions/2292#discussioncomment-9088696)). Fantasization of failure outcomes is absent: fantasies always produce a y.
4. **No DAG/network model or posterior.** `LearnedObjective` covers two stages, cannot see X, and only became constraint-safe on `main` ([#3575](https://github.com/meta-pytorch/botorch/pull/3575)).
5. **Pending semantics are all-or-nothing.** "Running at stage k, done upstream" needs the decoupled machinery (`ModelList` with evaluation masks), which only qHVKG fully uses. There is no "abandoned" or "failed" state. Replacement semantics for incremental qLogNEI exist only on `main`.
6. **Cost-awareness ignores failure.** `InverseCostWeightedUtility` divides by expected cost but has no "cost spent before failure" or "probability of reaching stage k".
7. **Data validation forces dropping rows.** NaN is rejected, so each node's GP must be trained on its own subset. That is fine for networks, but nothing exploits the selection bias that failures introduce.
8. **Upstream risk.** There is a GPyTorch bug in fantasies of batched multi-output nodes ([PR 2762](https://github.com/cornellius-gp/gpytorch/pull/2762), unmerged), and support is reduced ([#3308](https://github.com/meta-pytorch/botorch/issues/3308)).

## (f) Recommendations: a failure-prone node in a GP network

**f1. Model structure.** For each failure-prone stage k, train:
- the node's regression GP on successful runs only;
- a viability classifier node `v_k`, whose inputs are the stage's own inputs and its parents' outputs.

Make `v_k` a node in the DAG so the network posterior samples its latent jointly. P(viable) then depends on the sampled upstream outputs, and MC weighting captures that dependence (cf. [#2851](https://github.com/meta-pytorch/botorch/issues/2851#issuecomment-2876903656)). Keep upstream-stage data from runs that later failed: per-node training sets are native to networks and `ModelListGP` ([§a-iii](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/model_list_gp_regression.py#L23-L39)).

**f2. Classifier choice.**
- **Default.** `SingleTaskVariationalGP(X, y01, likelihood=BernoulliLikelihood(), inducing_points=X, learn_inducing_points=False)` fitted with `VariationalELBO`. Use no outcome transform, a Matern kernel, and optionally input warping or a larger outputscale prior so the boundary can be sharp ([mshvartsman](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-792131841), [bletham](https://github.com/meta-pytorch/botorch/issues/725#issuecomment-791161534)).
- **Alternatives** if failure regions have hard edges and data are plentiful: a soft-KNN as in [#3243](https://github.com/meta-pytorch/botorch/pull/3243), which is differentiable, or a RF/XGBoost ensemble ([#3082](https://github.com/meta-pytorch/botorch/pull/3082)), which is not. These give weaker uncertainty.
- **Use as a constraint on ≤ 0.18.1.** Expose the latent `f` and use `c(Z) = log_ndtr(-f) − log_ndtr(f)` with `eta=1.0, fat=[False]`. This weights each sample by exactly Φ(f), stably even in log space, and keeps the hard check `f ≥ 0` correct *[verified]* (`verify/botorch_probit_logit_trick.out`). Passing a *list* keeps the fat-tailed LogEI smoothing ([#3574](https://github.com/meta-pytorch/botorch/pull/3574) notes that lists only "worked by accident").
- After #3574 lands, `fat=[None]` with `ndtr(f)` is equivalent.

**f3. EI-type acquisition.**
- Use qLogEI or qLogNEI on the final node, with `constraints=[c_k for each failure node]`. The per-sample product E[I(y_final)·Π_k Φ(f_k)] equals EI×PoF under independence; in a network the dependence is kept.
- Use `X_baseline` from completed runs. With qLogEI, set `best_f` to the best *successful* final output.
- While there are zero successes, use `qLogProbabilityOfFeasibility` ([#2815](https://github.com/meta-pytorch/botorch/pull/2815)), as Ax does ([Balandat](https://github.com/meta-pytorch/botorch/issues/3009#issuecomment-3307468591)).
- Avoid analytic LogCEI on a latent classifier GP: it gives Φ(μ/σ) and ignores the probit link (disc [#2424](https://github.com/meta-pytorch/botorch/discussions/2424)).
- Clamp probabilities at ≥ 1e-12, or use the log form, to avoid the NaN gradients of [#3390](https://github.com/meta-pytorch/botorch/pull/3390).

**f4. KG and pKGFN.** There is no upstream support, so implement this mixture, which is the natural extension of pKGFN's per-node evaluation:

α_k(x) = [ p_k(x)·KG_k^success(x) + (1−p_k(x))·KG_k^fail(x) ] / E[cost_k]

- The success fantasy updates node k's GP and gives the classifier a label 1.
- The failure fantasy updates only the classifier (label 0). Its value is usually small but positive, because it reduces uncertainty about the boundary.
- Fantasize per node with `ModelList.fantasize(evaluation_mask=…)` ([L595-L673](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/models/model.py#L595-L673)).
- In the inner maximization of posterior mean, weight by Π_k Φ(f_k) (penalized/cKG-style).
- If the full mixture is too costly, use the heuristic α ≈ p_k·KG_k/cost. sdaulton warns that constrained KG may go negative ([comment](https://github.com/meta-pytorch/botorch/discussions/2292#discussioncomment-9119365)), so clamp it.

**f5. Pending and abandoned points.**
- **Running at stage k.** Treat the design as pending only for nodes ≥ k (decoupled `X_pending_evaluation_mask`, [L91-L135](https://github.com/meta-pytorch/botorch/blob/12c754c2986e19d8a6435c0413f7635c1bd9e68c/botorch/acquisition/decoupled.py#L91-L135)), and condition upstream nodes on their observed outputs.
- **Failed at stage k:**
  1. keep the upstream observations;
  2. add label 0 for `v_k` at (x_k, observed parent outputs);
  3. drop the design from `X_pending`;
  4. do not impute downstream y values. For benchmark scoring only, use the worst-feasible convention ([#3016](https://github.com/meta-pytorch/botorch/pull/3016)), never a huge value ([#943](https://github.com/meta-pytorch/botorch/issues/943#issuecomment-918802564), [disc #1449](https://github.com/meta-pytorch/botorch/discussions/1449#discussioncomment-3844259)).
- **Abandoned, with no information.** Remove it from pending and record no label.
- **Rebuilding the acqf.** On v0.18.1, rebuild the acqf after any change to the pending set rather than calling `set_X_pending` on incremental qLogNEI. Replacement semantics landed in [#3379](https://github.com/meta-pytorch/botorch/pull/3379), which is unreleased.
- **The failed-point hack.** Keeping failed designs as permanent `X_pending` ([#2262](https://github.com/meta-pytorch/botorch/issues/2262#issuecomment-2017947549)) is only a fallback when there is no classifier; with a classifier it double-penalizes.

**f6. Sampling and engineering.**
- Use the modern root/child base-sample pattern (§a-vi) and one Sobol draw across all nodes. Do not build per-node samplers with the same seed ([#2658](https://github.com/meta-pytorch/botorch/issues/2658)).
- Register the network posterior with `GetSampler.register`.
- Detach upstream samples before refitting nodes ([#3544](https://github.com/meta-pytorch/botorch/pull/3544)).
- For multi-output nodes in fantasies, either avoid batched multi-output GPs (use a `ModelList` of single-output GPs) or carry the GPyTorch fix from [PR 2762](https://github.com/cornellius-gp/gpytorch/pull/2762).
- For reproducibility, pin `botorch==0.18.1` / `gpytorch==1.15.2`, or pin `main@12c754c` to get #3378, #3379 and #3575.

## Artifacts

In this repo: the reproductions (`verify/botorch_*.py`, each with its `.out`) and the download and search scripts (`scripts/botorch_fetch.py`, `scripts/botorch_search.py`). The raw downloads (639 issues, 2,560 PRs, 340 discussions, with all comments, fetched 2026-11-26) are not committed; `botorch_fetch.py` regenerates them.
