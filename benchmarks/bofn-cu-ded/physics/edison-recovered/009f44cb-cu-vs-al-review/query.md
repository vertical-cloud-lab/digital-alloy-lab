Independent re-analysis: why does a cost-aware Bayesian-optimization benchmark give such different results on an aluminum and a copper alloy network? Please act as a skeptical reviewer who is willing to run code.

Two synthetic benchmarks share their method code. They ask whether cost-aware partial evaluation (pKGFN: partial knowledge gradient for function networks, Buathong et al., ICML 2024) reaches good alloys with less money than tiered screening or full-pipeline BO.
- **Aluminum, laser powder bed fusion** (files prefixed `al_`; results in `al_results.zip` as `k1/<policy>_s<seed>.json`, kappa = 1). Four priced stages: CALPHAD $10, atomize $1,500, print $2,500, tensile $200. Objective J = U - 0.3 B.
- **Copper, blown-powder DED** (unprefixed files; results in `cu_results.zip`). Eight priced stages: CALPHAD and heat flow $10; a 0.5 kg powder lot $400; small DED at Utah $500 with laser power capped at 0.5; large DED at Mines $3,100 for the first session on a lot and $1,500 for repeats; microscopy $100; tensile $200; a one-hour corrosion screen $50; 30-day immersion $400. Objective J = U * sigmoid((m - m_ref)/0.05) - 0.3 B, with burden B = 1.0 Ni + 0.3 Al + 0.2 Mn. The headline cell is (kappa, eta) = (1, 1).

Read `settings.md` (copper), `al_README.md` and `README.md` first, then `compare_tables.md` (our side-by-side tables, written by `compare.py`).

The results (best alloy demonstrated at $100k of new spend, % of each truth's optimum, mean over 20 seeds; aluminum, then copper):
- pKGFN: 84%, then 59%.
- BOFN, full pipeline: 86%, then 73%.
- BOFN with lot reuse: 90%, then 72%.
- Standard BO: 84%, then 14%.
- Random: 68%, then 22%.
- Tiered screening: 63%, then -8%. On copper it never demonstrates an alloy that passes immersion.

What `cu_results.zip` holds:
- `results/k1e1/`: the copper headline runs. Every baseline has 20 seeds. pKGFN is being re-run at the aluminum production Monte Carlo settings (S = 64 base samples, 16 candidates per stage, a 512-design pool) with two fixes from your earlier code review (task 42ee31fc): the fallback's EI test without the tie-break (F4), and the inner max anchored on every deposited design and deduplicated (F2). None of those re-runs had finished at upload time, so there is no `pkgfn` file in `results/`.
- `quality/results-light/k1e1/`: the first copper pKGFN sweep at lighter settings (S = 32, 10 candidates, a 256 pool), 20 seeds. Use these for pKGFN. They are the runs behind the 59%.
- `results/k1e1/tiered_ni_s*.json`: a new corrosion-aware tiered screening. The shortlist keeps only compositions with at least 10 wt% Ni. When fewer than four of them pass the CALPHAD crack screen, it is filled with the eligible compositions of lowest solidification index.
- `results/k1e1/tiered_ni_ref_s*.json`: the same shortlist, but a build goes to immersion when its one-hour screen is at least that of a reference coupon: dense C70600 (90-10 Cu-Ni), which passes immersion. The spec's gate, used by `tiered_ni`, is the 75% quantile of every screened build so far, seed builds included.
- `compare/results-nogate/k1e1/`: an ablation of eifn, eifn_reuse, ei and random on the same copper network, stages, costs and seeds, but with J = U - 0.3 B (no immersion gate; run with BOFN_NOGATE=1). Its optimum is in `landscape.json`.
- `landscape.json` (`landscape.py`): both truths on 10^6 random designs.
- `needle.json` (`needle.py`): whether the copper needle is in composition or in process. For example, 62% of random copper designs would pass immersion if deposited fully dense, but only 3.2% pass as deposited.
- `density.json` (`density.py`): the copper deposition index, factor by factor.

Please do the following, and say for each item whether you executed it or only inspected it.

1. **Recompute** from the JSON, independently of our scripts (write your own code first, then compare): the side-by-side table, the no-gate table, the light against high-fidelity pKGFN table (matched seeds, Wilcoxon), and tiered against corrosion-aware tiered. Normalize each run by the optimum of the truth it was scored on (al_optimum.json, truth_tables.json, landscape.json). List every discrepancy with compare_tables.md.

2. **Is there a clear reason for the differences?** For each gap (standard BO 84 to 14, random 68 to 22, tiered 63 to -8, pKGFN 84 to 59, and pKGFN falling behind BOFN by 13 to 15 points rather than 2 to 6), test the candidate explanations with the data and the code. Rank them by how much of the gap each explains, and run a decisive check where you can. Candidates:
   - (a) The landscape. The immersion gate makes the region within 60% of the optimum 14 times smaller than in aluminum, and only 3% of designs pass immersion. The Ni burden pushes away from the Ni that immersion needs. The five shared seed designs start at -10% of the optimum, against +35% in aluminum.
   - (b) Network depth. A new copper composition shows its value only after four or five more purchases (lot, Mines, microscopy, tensile, screen, immersion), against two in aluminum. One-step KG is flat until some alloy passes immersion: see the `fallback` flags in each pKGFN run's rows.
   - (c) Implementation differences between `al_policies.py` and `policies.py` in pKGFN: EI measured from the best demonstrated alloy rather than the best posterior mean, the path-priced fallback, test bundles, lighter Monte Carlo settings, and anchoring. Diff the two files and say which differences could change the results, and in which direction.
   - (d) Tiered screening's shortlist rule on an immersion-gated objective.
   - (e) Costs: $4,760 against $4,210 per full chain (21 against 24 full cycles).
   - (f) Anything else in the code or data.

3. **The deposition index.** The copper truth's dense, crack-free index (rho_u at Utah, rho_m at Mines) is window × q^0.3 × (1 - 0.75 crack) × (1 - lof). Copper-rich alloys reach a median of 0.40 at Utah. The proposal's gate is "99% relative density"; the benchmark's Utah gate is rho_u >= 0.5. Is this index physically defensible as written? Propose a physically scaled replacement: relative density from lack-of-fusion and keyhole porosity, a separate crack index, and a porosity-strength knockdown. Say whether and how it would change the comparison.

4. **Corrosion-aware tiered screening.** Are `tiered_ni` and `tiered_ni_ref` fair, realistic baselines? What do their runs show (look at `shortlist`, `w_ref`, the actions `screen-fail` and `utah-fail`, and the builds' w and m)? Is the spec's relative screen gate what limits `tiered_ni`? Does using `tiered_ni_ref` as the tiered baseline change any conclusion, for example the bofn-prelim-style speed-up over tiered screening?

5. **Verdict.** Which claims of the aluminum benchmark survive on copper? What is the most defensible two-sentence summary for a proposal's preliminary-results paragraph? What should be run next to make the copper benchmark decisive?

Report format: a Markdown document containing:
- (a) a findings table with severity (changes the conclusion / changes a number / cosmetic) and how you established each finding;
- (b) your recomputed tables next to ours;
- (c) the ranked explanations of the differences, with the evidence for each;
- (d) which checks you executed;
- (e) the verdict.

Be concrete, quantitative and unsparing. Save the report as report.md in your outputs as well as returning it as your answer.
