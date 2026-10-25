# Independent correctness review: copper-alloy DED Bayesian-optimization benchmark

Saved as **`/workspace/outputs/report.md`**. Supporting tests, reconstructed runs and numerical diagnostics are in `/workspace/outputs/`.

## Verdict and scope

**Not proposal-ready. I would not quote a headline saving from the supplied upload.** The GP arithmetic, fantasy conditioning, node ordering and uploaded cost ledgers pass my tests. The blocking problems for the proposed headline are the evidence and interpretation: no tiered run was uploaded, the supplied README has no “Bottom line” section, and the implementation is a materially modified, noisy KG/EI hybrid rather than an independently validated reproduction of the paper's p-KGFN.

I read `settings.md` first and kept benchmark sources and uploaded results unchanged. I inspected all nine source/document files and all 78 extracted result JSONs. All 78 are in `(kappa, eta) = (1, 1)`:

| Uploaded policy | Finished seeds | Seed IDs | Final spend range |
|---|---:|---|---:|
| ei | 14 | 0–13 | $99,920–$99,960 |
| eifn | 15 | 0–14 | $99,960–$99,960 |
| eifn_reuse | 15 | 0–14 | $97,880–$99,870 |
| pkgfn | 20 | 0–19 | $99,920–$100,000 |
| random | 14 | 0–13 | $99,960–$99,960 |

There are **no uploaded tiered, funnel, screen, audit, no-Utah or sensitivity-cell runs**. The README ends at line 142; its referenced quality scripts/JSON, `logs/plan.sh` and generated tables are absent. I therefore cannot verify the purported README headline as an uploaded result.

I also generated **20 tiered runs and the five missing BOFN+reuse seeds**, under `outputs/reviewer_results/`, to diagnose the missing comparison. Those are explicitly reviewer-generated evidence, not uploaded results. My environment is Python 3.13.7, torch 2.10.0+cpu, BoTorch 0.18.1 and GPyTorch 1.15.2, one thread per run. The uploaded settings name Python 3.12.3 and torch 2.14.1+cpu. I installed the missing GP packages; I did not silently claim an exact environment reproduction. Replayed seed-0 actions/spend through iteration 40 and the complete seed-16 action/spend/score trajectory match the upload.

### What I can reconstruct numerically

The 20 reviewer-generated tiered runs finish at a mean **J = −0.03785325**, or **−7.69% of the positive optimum**. This is a **negative target**. The common starting mean is **−0.04729700**: tiered improves the mean by only **0.00944376 J** (1.92 percentage points of J*) after nearly $100k. Only **5/20** tiered seeds improve their shared-start incumbent, and **none of 80 new immersions passes m_ref**.

| Method/cohort | Mean final J at $100k | Mean final % of J* ± SE | Exact new spend to tiered’s final mean | $100k / that spend |
|---|---:|---:|---:|---:|
| pKGFN: 20 uploaded seeds | 0.288186 | 58.55% ± 4.84 | $5,750 | 17.39 |
| BOFN+reuse: 15 uploaded + 5 reviewer seeds | 0.354535 | 72.03% ± 7.05 | $4,760 | 21.01 |
| Tiered: 20 reviewer seeds | −0.037853 | −7.69% ± 5.37 | $99,190 | 1.01 |

The literal fixed-target result is therefore **$94,250 less new spend for pKGFN (94.25%; 17.39-fold spend ratio)** and **$95,240 less for BOFN+reuse (95.24%; 21.01-fold ratio)** relative to $100k. These are **ratios of mean-curve first-hitting costs**, not a claim that each seed achieves the target or a ratio of median seed costs. They are reviewer-reconstructed point estimates under the provenance above, not a verified missing README quote.

The author’s analysis instead divides tiered’s **first** grid cost to that target ($99,250) by each method’s grid hit: $5,750 and $5,000. It gives **17.26×** for pKGFN and **19.85×** for reuse. Its matched-seed 90% bootstrap intervals are **11.97–21.94×** and **18.35–43.89×** (2,000 resamples). These intervals concern that grid-based estimator, not my exact-cost ratios. Exact tiered first hit is $99,190.

The independent-policy bootstrap is badly distorted by unequal resampled starting means: **815/2,000 resamples (40.75%)** give the method a zero-dollar hit, which the code replaces with $250. Its upper 90% endpoint is consequently **397× for both methods**. I would not use that interval in a proposal.

At the full budget, the matched pKGFN/reuse mean outcomes are **58.55% versus 72.03% of J***. pKGFN loses to reuse in **18/20** seeds (two-sided Wilcoxon p=0.00944). This does not erase its fixed-target saving against tiered; it does prevent attributing that saving specifically to superior KG stage selection.

## Findings

“Blocks the conclusion” means the stated proposal claim cannot be supported without resolving the finding. “Changes the numbers” identifies a numerical/methodological defect or consequential choice, not necessarily evidence that its correction helps pKGFN.

| ID | File and lines | Severity | Finding and evidence |
|---|---|---|---|
| F1 | `settings.md:10–11`; `README.md:111–142`; `results/k1e1/` | **Blocks the conclusion** | The upload contains 20 pKGFN runs, 15 each EIFN/reuse, 14 each EI/random, **zero tiered runs**, and no README “Bottom line.” I enumerated and parsed every JSON. An uploaded 20-seed saving against tiered cannot be computed. Reviewer-completed cohorts are distinguished above. |
| F2 | `policies.py:83–85,409–421,545–547`; `bofn_alloy.py:508–511`; `README.md:97` | **Changes the numbers** | The inner maximum is not explicitly incumbent-anchored; base normals are independent across inner designs; duplicate designs receive different Monte Carlo estimates. At seed 0/iteration 4, 83 inner entries contain only 60 unique designs; the incumbent is absent (nearest distance 0.06624). Identical designs differ in estimated mean J by as much as **0.04517**. Executed snapshot diagnostics and comparison with the paper's common-random-number construction. |
| F3 | `policies.py:61–63,554–567`; `README.md:115–126` | **Changes the numbers** | The production MC setting does not reliably rank stages. Re-scoring the same iteration-40 candidates changes the winner from **Mines at 32 samples to CALPHAD at 1,024**, with CALPHAD's estimated KG/dollar changing from numerical zero to **4.929e-6**. Five additional 32-sample draws choose M, M, M, U and A, never C. This is observed estimator instability, not proof of full-run convergence failure. |
| F4 | `policies.py:475–479,596–605`; `README.md:98–99` | **Changes the numbers** | The Utah/Mines “EI” stored for fallback includes the mean tie-break term, `1e-9 * sample_mean`. Therefore the test for positive EI is not a test for positive EI: an all-zero-EI case can take the EI/cost branch instead of the advertised most-optimistic-sample branch. I executed a two-candidate counterexample with opposite choices. Keep raw EI and tie-breaking separate. Uploaded JSON records only a fallback boolean, not which fallback branch or its inputs. |
| F5 | `policies.py:521–544,635–653`; `bofn_alloy.py:508–511` | **Changes the numbers** | Test bundles are plug-in, last-stage-only KG heuristics, not multistage KG. The “current value” is a candidate-dependent fantasy-averaged control variate, not the independently computed current network optimum. I derived the distinction and numerically measured it; bundle charges themselves pass. For screened variants, full immersion cost is reserved even when the eventual screen stops the bundle. |
| F6 | `policies.py:146–160,306–344`; `README.md:59,83`; `analyze.py:104–107,157–171` | **Blocks the conclusion** | The saving is against a deliberately restricted, weak target, not demonstrated attainment of a useful alloy. This blocks a general cost-advantage interpretation, not the arithmetic of the narrowly defined fixed-target statistic. Tiered is frozen to four strength-ranked, crack-screened compositions. Across all 20 seeds, my 16,384-process-design search on each shortlist finds largest sampled immersion indices only **0.564–0.780**, below 0.849. This is sampled evidence, not a certified global bound. The reconstructed target and saving must be reported with their absolute J and uncertainty, not as a general BO advantage. |
| F7 | `check_truth.py:39–43,46–115,153–159`; `settings.md:9`; `README.md:59–73` | **Changes the numbers** | The truth checker prints diagnostics but asserts none of the required properties. Its one-hour gate omits Utah feasibility and is not the policy's adaptive observed-data gate. Property 4 is not literally universal: **15%** of sampled copper-rich compositions can exceed the policy's Utah density gate of 0.5. I executed the full checker for all four cells and additional tests. |
| F8 | `policies.py:256–267`; `bofn_alloy.py:296–298` | **Changes the numbers** | Budget enforcement is policy-side, not a Lab invariant, and tiered/funnel startup ignores the budget. At a requested **$1,000**, executed tiered spends **$2,240** and funnel **$33,140**. This does **not** demonstrate an overrun at the reviewed $100k budget; none occurs in the audited runs. |
| F9 | `run_sweep.py:32–39`; `analyze.py:69–76` | **Changes the numbers** | Resumption accepts any existing path without validating budget, acquisition settings or source revision. Aggregation also ignores configuration compatibility. A sentinel $1k/S=1 result was silently reused for a requested $100k run in my isolated test. Versioned output directories and configuration/source hashes are needed before corrected sweeps. |
| F10 | `analyze.py:20,79–107,110–124`; `plot.py:106–126` | **Changes the numbers** | The plotted “speed-up” numerator is tiered's **first** cost to reach its final level, not $100k. Costs are rounded up to a $250 grid; a zero-dollar method hit is replaced by $250 in the ratio. Independent bootstraps can compare different initial seed means despite the shared-start design. I executed a toy estimand test and report exact-cost and matched-seed diagnostics separately. |
| F11 | `analyze.py:271–300`; `policies.py:390–402` | **Changes the numbers** | The audit summary is descriptive, not an unbiased population false-rejection estimator: near-cutoff cases are oversampled, KG selects which eligible cases are purchased, and the oracle uses the final gate whereas events use time-varying gates. No uploaded audit run establishes its proposed inferential interpretation. Inspected formulae and ran a small audit smoke test. |
| F12 | `README.md:19,83,89,99`; `policies.py:70–80,151,369–375,669`; `bofn_alloy.py:520–523` | **Cosmetic** | “256 compositions” actually means **261** available compositions after 32 CALPHAD seeds, five full seeds and 224 new calls. `mines_only` removes **new** Utah purchases, not the five sunk Utah observations or Utah GP. “Never stops with money left” is false: fallback excludes C and affordability can terminate early. `normal_qmc` is unused; acquisition bases are pseudorandom normals. These need precise wording, not a new headline. |

## 1. GP posterior and physical-unit standardization

**Executed and derived; passed, apart from a negligible documented jitter difference.** I fitted two TinyGPs, one using the 0.25 scale floor and one with observed standard deviation above it. I compared `post_std` and `cov_std` with a BoTorch exact RBF GP at the same fitted ARD lengthscales, constant mean, unit outputscale and fixed standardized noise `1e-6`.

TinyGP computes
\[
K=K_{XX}+(10^{-6}+10^{-8})I,\quad
\mu(u)=c+k_{uX}K^{-1}(Y-c),\quad
\Sigma(u,z)=k(u,z)-k_{uX}K^{-1}k_{Xz}.
\]
The extra `1e-8` is numerical jitter (`bofn_alloy.py:223`), not a missing outputscale. Against the nominal-noise BoTorch reference, maximum standardized errors were **5.51e-6 in mean, 5.69e-7 in variance and 5.69e-7 in cross-covariance**. Against an independent dense RBF solve with matched jitter they fell below **6.3e-13, 8.4e-15 and 6.6e-15**, respectively.

The inverse standardization is correct in all requested locations:

- `Network._sample`, lines 448–451, and `Network.kg`, lines 499–502: `(standardized mean + standardized sd * eps) * ys + ym`.
- `policies.expected_improvement`, lines 138–143: raw mean and raw standard deviation, not variance multiplied by the wrong scale. My analytic EI comparison differed by at most **5.6e-17**.
- `Lab.estimate_rho_u`, lines 335–345: `mean_raw`. A numerical check returned exactly **0.7718374112** before a matching Utah observation; after paying $500 it returned the measured **0.5289465258**, not the old prediction.

Noise `1e-6` is in **standardized** output units; raw observation-noise variance is `ys² * 1e-6`. I found no standardization bug. The uploaded fits report **0 failures in 18,774 fits**; this does not certify hyperparameter identifiability.

## 2. KG estimator, fantasies and bundles

**Executed explicit conditioning tests; derived estimator distinctions; inspected bundle planning.** For standardized GP covariance `c(u,z)` and fantasy normal `w`, the code correctly uses
\[
\mu^+(u)=\mu(u)+\frac{c(u,z)}{\sqrt{v(z)+\sigma_n^2}}w,
\qquad v^+(u)=v(u)-\frac{c(u,z)^2}{v(z)+\sigma_n^2}.
\]
I independently appended each fantasy observation to the training matrix and solved the augmented GP. Mean/variance update errors were below **7.3e-12/6.0e-14**. An unvectorized candidate-by-fantasy network calculation agrees with `Network.kg` for **all eight stages**, including chunk sizes 1 and 2, to floating-point precision. A second test includes nonzero KG. The broadcast is correctly `[candidates, fantasies, inner points, base samples]`; `node_input` propagates changed parents to children. I found no candidate/fantasy axis swap.

The CALPHAD product rule is correct **for the independent-node GP model**: 16 combinations of four ±1 normals, equal weights 1/16, zero means and identity covariance. It is a very coarse quadrature of the nonlinear gated/max objective: its marginal fourth moment is 1 rather than the Gaussian 3. Sixteen points should not be represented as a high-fidelity four-output expectation.

The current term is
\[
\sum_f p_f\max_x\hat\nu_f(x)
-\max_x\sum_f p_f\hat\nu_f(x),
\]
not `E[max future] - max current` evaluated independently. With exact expectations the tower property makes these equivalent. With finite base samples and finite fantasy quadrature, the code's candidate-dependent centering changes the estimator while enforcing nonnegativity by Jensen. At iteration 4, sampled centers for the tested candidates differ from the common current estimate by up to **6.68e-4 J**. This is a defensible variance-reduction choice only if its numerical bias/ranking sensitivity is evaluated; “KG is never negative” is not a correctness proof.

The paper's Algorithm 3 shares each node/sample normal across designs as well as fantasy models. `eps_for(m,S)` does not: it generates a different row per design. The code does share rows across acquisition candidates/fantasies, so the README's CRN statement is partially true, not wholly false. Duplicate inner designs then get independent integration errors and extra chances to win the maximum. Add the exact incumbent/posterior maximizer explicitly, deduplicate the inner set, and test shared design-wise base normals. The existing “anchors” are top pool entries and perturbations, not guaranteed incumbents.

**Bundles:** S+T, S+K+I and K+I cost **$300, $550 and $450**. Their nominal prices and actual unscreened charges are correct. Posterior-mean intermediate inputs make a practical unlock heuristic, but do not integrate uncertainty in microscopy/screen outcomes, include the information from all purchased stages, or optimize an actual continuation policy. S+K+I also still needs tensile to be validated; the fallback path-cost calculation includes it. Do not call these bundles an exact multistep p-KGFN calculation. For trusting variants, actual screen rejection can omit immersion after it has been reserved in the nominal bundle cost.

## 3. Shapes, node inputs and physical rules

**Executed 100 random full designs, 25 in each truth cell.** For every node I compared `AlloyTruth.full(x)` with `Lab.full_eval(x)` observations **and their recorded input tensors**, plus J and every charge. All node/input errors were **exactly zero** and every new full chain cost **$4,760**.

I checked every specified ordering: `s/f/g/h = (Ni,Al,Fe,Mn)`; `q = (a,Mn,f)`; `rho_u = (min(P,0.5),v,f,g,h,q)`; `rho_m = (P,v,f,g,h,q,rho_u)`; `beta = (Al,Ni,P,v,rho_m)`; `U = (s,rho_m,beta)`; `w = (Ni,Al,Fe,rho_m,beta)`; `m = (Ni,Al,Fe,rho_m,beta,w)`. They match `SPEC`, `node_input` and Lab methods.

CALPHAD is automatically bought before atomization; Utah/Mines require an existing lot; microscopy requires an existing build; tensile and screen assert microscopy; immersion asserts a screen. **Mines is intentionally allowed without Utah**, consistent with the requested rules. The Utah cap is applied before truth evaluation and GP use; changing only P from 0.7 to 0.99 leaves Utah truth unchanged.

Nine Mines sessions on one lot cost **3,100, 1,500, 1,500, 1,500, 3,100, 1,500, 1,500, 1,500, 3,100**. Scale-up renews on sessions 1, 5 and 9, not after an off-by-one fifth cheap session. Invalid downstream ordering assertions fired in my tests.

## 4. Fairness, budget and ledger

**Executed full uploaded-result reconciliation; inspected all policy branches.** Shared seed builds agree across policies for each common seed. The initial data cost **$24,120** before `spent` and the purchase log are reset: 32 calculations plus five complete chains. The data and physical inventory are retained. Each seeded lot has three prepaid-scale-up Mines sessions left; reuse methods can exploit this while whole-pipeline methods choose not to. This is shared inventory, not an accounting leak, but the claim must be about **new spend after that inventory exists**.

For every uploaded run I reconstructed
\[
\text{spend}=\sum_g n_g\,\text{COSTS}_g
+1600\left(\sum_{\ell}\left\lceil n_{M,\ell}/4\right\rceil-5\right),
\]
where per-lot session totals include the five seed builds. **All 78 residuals are $0.** Inventory-based A/U/M/S/T/K/I counts agree with the recorded purchase counts, and session balances agree with session totals. Every uploaded pKGFN action increment matches its stage or bundle price: 564 repeat Mines purchases at $1,500, 246 scale-up purchases at $3,100, and all 273 test bundles at the prices above. No uploaded spend exceeds $100,000. I also reconciled all 28 reviewer-generated result files, including the 25 $100k headline additions and three $6k smoke runs: **106/106 total run files pass** the ledger, budget, session-balance and final-score checks.

`best_validated` is consistently the maximum true J computed from **measured tensile and immersion** on a Mines build, including the shared seed builds. It does not require immersion to pass the threshold; the objective itself has the sigmoid gate. Every final row agrees with the maximum recorded validated build J. Recomputing from stored U/m and four-decimal composition produces at most **2.01e-5** error from serialization. `rec_printed` and the optional recommender use free truth only as diagnostics; I found **no route feeding those oracle scores back into acquisition decisions**. Funnel truth-based rejection scoring runs after decisions.

Tiered explicitly pays for **224 new calculations = $2,240**. Including the five full-seed compositions it screens 261 available compositions, not literally 256. Full-policy admission uses conservative complete-chain costs; pKGFN checks action/bundle affordability and first-versus-repeat Mines costs. These enforce the reviewed $100k ceiling. They are not a general Lab-level guarantee: the small-budget counterexamples in F8 must be fixed before budget sweeps.

**Variants:** I inspected all branches and executed seed-0/$6k smoke tests. `pkgfn_screen`, `pkgfn_audit` and `mines_only` finish at **$5,960, $5,820 and $5,960**, with no checked prerequisite violations. Strict screen gating works, including the post-screen check inside immersion bundles. Audit eligibility is deterministic hashing plus near-cutoff permission, not a promise that 10% of actual purchases are audits. `mines_only` buys zero new Utah queries but retains five seed Utah observations and the rho_u surrogate. Funnel implements 12→6→3 lots, three Utah settings per retained powder lot, two Mines builds per finalist and three screen-selected immersions, then the tiered loop. I executed its initialization, not a full $100k funnel performance sweep.

## 5. Copper-port changes and fallback

**Inspected the supplied implementation/comments; counted every uploaded decision; replayed seed 16.** The aluminum source was not supplied, so I cannot independently establish a source diff or confirm the history of discarded aluminum/copper runs.

EI over the **best demonstrated J** is a reasonable proposal heuristic for this scoring rule. EI over the best posterior mean can set an unrealistically high acquisition threshold when all feasible validated designs are poor. Neither candidate heuristic changes the KG formula, and neither makes it a full reproduction of the paper. Posterior-mean zero-EI tie-breaking is sensible if kept lexicographic; adding the tie-break to the numeric EI later used by fallback is the F4 bug. Maximizing one optimistic posterior sample is an exploratory heuristic, not an EI/cost or KG/cost decision; it also favors actions with more variable predicted samples and ignores cost in its final zero-EI branch.

The fallback is **not rare**:

- **418/1,944 purchases = 21.50%**, accounting for **18.03% of pKGFN spend**.
- Median seed fallback share: **6.24%**; range **0.97–82.14%**.
- Seed 16: **92/112 purchases**, $83,800 on fallback, final J **−0.005514** (−1.12% of J*).
- While the row's best validated J is nonpositive, **380/893 = 42.55%** of purchases use fallback; after it is positive, **38/1,051 = 3.62%** do.

These figures show a network acquisition whose one-step/discrete incumbent-switch signal often collapses in the poor-alloy/gated regime. They do not show that theoretical p-KGFN is intrinsically incapable of this problem. The reported performance belongs to this hybrid, including the fallback and bundles. BOFN+reuse is a necessary ablation; the comparison cannot attribute reuse savings to KG's stage selection alone.

## 6. Monte Carlo and candidate fidelity

**Executed two fixed-candidate re-scores and five extra low-sample draws.** I replayed seed 0 without changing its purchases, saving all eligible stage candidates, costs, inner set, fantasies and fitted models at iterations 4 and 40. I then changed only the objective base-sample count for scoring, keeping the candidate and inner sets fixed.

| Iteration | 32-sample winning stage; KG/$ | 1,024-sample winning stage; KG/$ | Same candidate? |
|---|---|---|---|
| 4 | Mines; 1.2554e-6 | Mines; 1.8786e-6 | **No**: candidate 9 → 2, zero-based stage indices |
| 40 | Mines; 8.2293e-8 | CALPHAD; 4.9289e-6 | **No** |

At iteration 40, the 1,024-sample best Mines value is **3.9078e-7 per dollar**, so CALPHAD is **12.6 times** larger. The production estimate for CALPHAD is just floating-point zero. Five other 32-sample draws choose Mines three times, Utah once and atomization once. These results substantiate the README's *qualitative* warning, not its exact unstored reference values; its reference base-sample draws were not supplied.

**Conclusion:** 32 samples is demonstrably unreliable for some stage rankings. I cannot establish that the cuts “cripple” full-run performance, or that 1,024 is ground truth. These probes hold the small candidate/inner sets fixed and retain the 2-point CALPHAD fantasy rule; they do not test pool/candidate omissions or fantasy-quadrature convergence. Before proposal use, run prespecified paired seeds at S=256 and at least selected S=1,024 iterations, with larger candidate/pool settings and a higher-order CALPHAD fantasy check. Do not select favorable settings after examining their speed-ups.

## 7. Truth and required properties

**Executed `cell_report` for all four cells without overwriting the upload.** The regenerated `truth_tables.md` is **byte-for-byte identical** to the supplied table. The headline optimum reproduces as **J*=0.492187251856**; `(0,0)` reproduces as **0.381561510051**. These are reproducible heuristic multistart search results, not certified global optima.

1. **Screens and optimum:** the headline optimum has f≈0.74 and fails f≤0.34. The searched best crack-screen-feasible J is **72.206%** of J*, and `(0,0)` keeps **92.101%** through the two diagnostic screens, meeting the stated 85% criterion *under that checker's gate*. The actual tiered rule adds a four-composition shortlist, Utah qualification and an adaptive observed-w gate; the checker does not establish its achievable ceiling or the full workflow's 85% retention. The “dense candidates” reference distribution also includes the crack filter, rather than all dense candidates. At eta=0, w is still not a constant/monotone transformation of m; I found a dense, crack-passing pair with the w ordering reversed relative to m. “Both screens right” is too strong a label.
2. **Reference alloys:** the headline values reproduce: C71500 U≈0.476/m≈0.8493; C70600 U≈0.380/m≈0.8717; NAB U≈0.793/m≈0.5516 at the script's best-J settings. C70600 is weaker and passes; NAB is stronger, retains beta-prime and fails. However, the code does not perform an explicit fast/cool-versus-slow/hot intervention test, and C71500 fails immersion at kappa=0, as README admits. `m_ref` itself is a finite Sobol-search reference: another fixed search finds C71500 m=0.84928185 versus reference 0.84913540. This small difference is numerical, not a GP bug.
3. **Ridge:** reproduced **17/10,201** process-grid points within 0.5% of headline J*, P=0.53–0.64 along P−v=0.23–0.24. This demonstrates a finite near-optimal ridge on the tested slice, not a globally certified ridge manifold.
4. **Copper-rich power cap:** reproduced median best Utah density≈0.40 versus Mines≈0.88; 15% are below Utah 0.3, and 100% exceed Mines 0.7. But **15% also reach Utah 0.5** in the same composition sample; “cannot fuse at Utah” is not a universal property established by this truth. At the optimum's composition, separately optimized Utah/Mines maxima are **0.9195/0.9302**: the cap is almost irrelevant to reaching the optimum. The README's detailed percentages are accurate; the broad requirement needs qualification.

The README discloses most formula changes and the principal caveats accurately: added h, stronger Ni–Al synergy, changed crack onset, film saturation, Fe contribution, noise-free observations, no delays and eta not eliminating the optimum. The separate original specification was not supplied, so I checked formulas against the uploaded README, not an unavailable original.

**Construction-induced advantages/difficulties:** kappa deliberately makes the conservative crack gate reject the global optimum. Tiered never revises its four-composition shortlist using corrosion evidence; it cannot respond by changing composition. The high-strength Al-rich shortlist is especially poor for immersion, well below even the broader 72% crack-screen ceiling. Conversely, a sigmoid-gated objective with independent uncertain upstream GPs creates flat incumbent-switch KG regions, explicitly requiring the fallback/bundle patches. Lot reuse benefits from deterministic shared composition/powder responses and sunk scale-ups. eta affects only w, not the true optimum. The truth also ignores rho_u in rho_m, w in m, and rho_m in beta; I verified all three ignored-coordinate effects are exactly zero. The first two are disclosed; the beta simplification should also be explicit.

The objective is **soft-gated**, not “strength counted only if immersion passes”: the gate is 0.5 at m_ref, 0.269 one gate-scale below it, and 0.731 one scale above. Fully tested failing alloys can still have positive J. That distinction matters when interpreting a cost-to-low-target headline.

## 8. Additional reproducibility and reporting issues

- Store source revision/hash, complete environment, budget and acquisition settings with every run; refuse incompatible resume files. No uploaded source hash proves which historical code produced each file.
- Save selected raw EI, KG, KG/$, actual action cost, nominal continuation cost, fallback reason and candidate identity. A boolean cannot distinguish EI fallback from optimistic fallback or diagnose F4 from an uploaded run alone.
- Deduplicate inner points before integration and retain full-precision design/lot/build identifiers. Four-decimal compositions suffice for approximate plotting, not exact independent truth replay.
- Report the target's absolute J, how far it is above the shared-start mean, both literal-$100k and first-hit saving definitions, exact purchase-cost hits, matched-seed confidence intervals and failure fractions. A ratio to a very weak negative target is not evidence of a good validated alloy.
- Dead/unused items include `normal_qmc`, `fvals` in the funnel helper and `Data.events` for the actual policy audit. The runner defaults to the machine's visible CPU count rather than a quota-aware worker count. I used explicit worker counts; these issues did not corrupt my tests.

## Required fixes and reruns before proposal use

1. **Restore the actual claim and evidence.** Supply the intended README “Bottom line,” complete matched 20-seed cohorts, quality scripts and logs. Treat my generated baselines as a reconstruction under a different Python/torch environment, not as missing uploaded evidence magically recovered.
2. **Repair numerical/algorithm bookkeeping.** Separate raw EI from tie-breaks; explicitly include incumbents and deduplicate inner designs; test paper-style common random numbers; document/validate the centered current-value estimator and coarse multi-output quadrature. Add regression tests to preserve the GP, fantasy, physical and ledger passes established here.
3. **Make purchasing transactional.** Centralize affordability checks, including tiered/funnel initialization and renewed scale-ups. Reject stale resume configurations. Log full action provenance.
4. **Rerun the affected comparisons in one pinned environment.** At minimum use 20 matched production seeds after fixes, a prespecified higher-fidelity subset, and the BOFN+reuse ablation. If the implementation remains a bundle/fallback hybrid, label it as such rather than attributing all gains to Buathong et al.'s method.
5. **Use a defensible headline endpoint.** Keep the requested tiered-final target as a descriptive result, but also compare positive, practically meaningful absolute J targets with success rates and censored failures. Prespecify a stronger, explicitly adaptive tiered alternative or show that the conclusion survives relaxing the fixed four-composition shortlist and varying gates/costs. This tests whether the finding is stage selection or simply a screening baseline engineered to exclude useful alloys.

**Bottom line:** I found no hidden GP rescaling failure, broadcast bug or missing purchase charge in the uploaded runs. I did find incomplete claim evidence, consequential acquisition-estimation choices, a real fallback-logic defect, a distorted independent-bootstrap interval, and a baseline whose restricted composition choice makes its final target negative and unusually weak. The narrow fixed-target comparison is numerically real in my reconstructed cohorts. The code supports an exploratory comparison of the particular algorithms implemented here, subject to the provenance and numerical limits above. It does **not yet support an unqualified proposal headline about p-KGFN's experimental-cost advantage.**

### Executed versus inspected checks and artifacts

| Requested item | What I executed | What remains inspected/limited |
|---|---|---|
| 1. GP | BoTorch/dense exact reference; both standardization regimes; analytic EI; rho_u measured/predicted branch | No exhaustive stress test of all fitted historical posteriors |
| 2. KG | Augmented-data fantasies; all stages versus scalar loops; chunk/broadcast checks; quadrature moments; current-term/CRN snapshots | Bundle lookahead is derived/inspected, not validated as optimal multistep planning |
| 3. Physics/shapes | 100 full designs across four cells; all node inputs/observations/J/costs; nine Mines sessions; invalid-order assertions; Utah cap | No external experimental metallurgy validation |
| 4. Fairness/ledger | All 78 uploaded ledgers/counts/scores; reviewer-completed headline cohorts; small-budget counterexamples; variant smoke tests | No full screen/audit/no-Utah/funnel performance sweep |
| 5. Port/fallback | Every uploaded fallback flag; complete instrumented seed-16 replay; fallback counterexample | Aluminum source and discarded runs absent |
| 6. MC | Iterations 4/40 at 32 vs 1,024; five independent low-S draws at iteration 40 | No full higher-fidelity/pool-size convergence sweep |
| 7. Truth | Full four-cell checker, exact table reproduction, added cap/reference/ignored-edge checks | Search is not globally certified; original separate specification absent |
| 8. Other | Resume sentinel; aggregation estimand example; source hashes | Plotting inspected, not used to infer numerical results |

Evidence is saved in `outputs/`: `provenance.json`, `source_sha256.json`, `review_tests.py`, `gp_lab_tests.json`, `gp_matched_jitter_tests.json`, `kg_tests.json`, `kg_nonzero_tests.json`, `ledger_audit.csv`, `row_delta_audit.json`, `fallback_by_seed.csv`, `mc_rescore.json`, `mc40_rescore.json`, `mc40_low_replicates.json`, `inner_set_diagnostics.json`, `truth_recomputed.json/.md`, `tiered_shortlist_diagnostics.json`, `headline_review.py`, `headline_reviewer_comparison.csv`, `headline_reviewer_stats.json`, `complete_ledger_audit.csv`, and the separate reviewer result JSONs/logs. The report itself is `outputs/report.md`.

Primary method reference: Buathong et al., *Bayesian Optimization of Function Networks with Partial Evaluations*, ICML 2024, PMLR 235:4752–4784, especially Eq. 3 and Algorithms 1–3 ([paper](https://proceedings.mlr.press/v235/buathong24a.html)). I archived the paper and saved its full BibTeX through the citation helper; source-code findings refer to the supplied files and line numbers, not to an assumed upstream implementation.

### Discretionary analytical decisions

- I kept uploaded results immutable and generated missing baselines in a separate directory, because no valid tiered comparison could be inferred from the upload alone.
- I matched fitted GP hyperparameters rather than refitting a competing model, isolating posterior arithmetic from optimizer differences; I reported the extra numerical jitter separately.
- I used explicit augmented-GP fantasy solves and scalar network loops to avoid validating vectorization against itself.
- I held candidates, costs, fantasies and inner sets fixed for MC probes, isolating scoring noise rather than conflating it with a changed policy trajectory.
- I distinguished exact purchase-cost hits, the author's $250-grid estimand and the literal $100k comparison, and used matched-seed uncertainty for the shared-start design.
- I treated sampled shortlist potential and multistart truth optima as numerical search evidence, not mathematical global bounds; I did not claim a full convergence or external metallurgy validation.