# BOFN on a copper/DED network: does choosing the stage beat tiered screening?

Copper and blown-powder DED version of [`../bofn-prelim/`](../bofn-prelim/README.md), the aluminum LPBF benchmark behind the MS&T26 preliminary results, built for the ONR YIP copper proposal (`near-term-submissions/onr-yip/onr-yip-technical-proposal-cu-ded.tex`, Figs. `fig:synth` and `fig:sim`; issue 205). It asks the same question on the copper workflow: with eight priced stages from a $10 calculation to a $3,100 deposition session, does cost-aware partial evaluation (pKGFN, [Buathong et al., ICML 2024](https://proceedings.mlr.press/v235/buathong24a.html)) reach good alloys with less money than tiered screening or whole-pipeline BO? `bofn-prelim/` and its 292 stored runs are unchanged.

<!-- RESULTS -->
## Bottom line (Oct 27)

**The aluminum headline does not carry over to copper as specified, and the reason is clear: the immersion gate.** At `(kappa, eta) = (1, 1)` (both screens biased), best alloy demonstrated at $100k, % of the optimum:

| Policy | n | $25k | $50k | $100k |
|---|---|---|---|---|
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | **73% ± 7** |
| BOFN + lot reuse | 20 | 14% ± 5 | 32% ± 8 | **72% ± 7** |
| pKGFN, aluminum production settings (Oct 27) | 7 | 3% ± 5 | 25% ± 10 | **59% ± 11** |
| pKGFN, light settings (first sweep) | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 |
| Tiered, Ni ≥ 10 wt%, reference screen (Oct 27) | 20 | 8% ± 4 | 16% ± 4 | **24% ± 5** |
| Random | 20 | −1% ± 4 | 7% ± 5 | 22% ± 5 |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 |
| Tiered, Ni ≥ 10 wt% (Oct 27) | 20 | −7% ± 5 | 1% ± 5 | 10% ± 6 |
| Tiered screening (the spec's rule) | 20 | −9% ± 5 | −9% ± 5 | −8% ± 5 |

- **Network-aware BO wins by a wide margin.** BOFN reaches 73% (full pipeline) and 72% (lot reuse), against 14% for standard BO and 22% for random designs.
- **Against a fair tiered baseline, the aluminum-style speed-up comes back for BOFN.** Corrosion-aware tiered screening (`tiered_ni_ref`) ends at 24%.
  - BOFN on the full pipeline first reaches that level at $34k: **3.0× less spend** (90% bootstrap CI 1.7–4.2).
  - BOFN + lot reuse reaches it at $35k: 2.8× (1.7–4.1).
  - pKGFN at the aluminum settings (7 seeds) reaches it at $47k: 2.1× (90% CI 0.9–2.4).
  - The light-settings pKGFN reached it at $47k: 2.1× (1.5–3.9).
  - At $100k BOFN is ahead of it by 49 points (17 of 20 matched seeds; Wilcoxon p = 0.0003).
  - The spec's tiered rule (−8%) gives no meaningful speed-up, because every policy passes its level in its first few purchases.
- **pKGFN at the aluminum production settings.** Seeds 0 to 5 and 7 end at 59% ± 11 (65, 86, −1, 78, 58, 91, 35). The same seeds at the light settings end at 64% ± 4 (63, 47, 60, 78, 73, 77, 51; 3 wins, 0 ties and 4 losses for the high-fidelity runs, Wilcoxon p = 0.69). BOFN on the full pipeline ends at 87% ± 4 on those seeds (1 win, 0 ties and 6 losses for the high-fidelity runs, Wilcoxon p = 0.047). So the lighter settings were not why pKGFN lags. Per run it still deposits about 38 builds at Mines and completes only 5 through tensile and immersion; per $100k it buys 38 Mines sessions, 6 tensile tests and 11 immersions. On 3 of the 7 seeds KG was flat for most of the budget: the EI fallback made 70% and 67% and 89% of the purchases on seeds 1 and 2 and 7, against 1% and 3% and 27% and 5% on the others. The fallback prices the whole path to a validated build but buys only the next step, and the next decision rarely finishes the path. BOFN + lot reuse, which buys the whole path at once, reaches 72%.
- **Corrosion-aware tiered screening** (two new variants, 20 seeds each):
  - A 10 wt% Ni floor on the shortlist raises its ceiling from −19% to 60%, but alone it reaches only 10%. The spec's one-hour-screen gate (top quartile of everything screened so far, which the high-Ni seed builds set) stops most of its Cu-Ni builds before immersion: 2.5 immersions per run.
  - Gating the screen on a dense 90-10 Cu-Ni reference coupon gives 9.9 immersions per run, 2.6 of which pass, and 24%. That is random's level (22%), a pattern seen in aluminum too, where tiered screening ended below random.
  - Its weak seeds spend most of the budget on lots that fail Utah's density gate: new lots atomized at poor settings.
- **Why copper differs from aluminum** (next section): the immersion gate acting on the deposit's density.
  - 62% of random copper designs have a composition that would pass immersion if deposited fully dense, but only 3.2% pass as deposited, and the five shared seed alloys start at −10% of the optimum (aluminum: +35%).
  - On the same copper network without the gate, BOFN reaches 85 to 88% (aluminum: 86 to 90%), standard BO 65% (gated: 14%) and random 51% (gated: 22%).
- **The "density" of 0.40 is not a density.** It is the lack-of-fusion factor of a multiplicative deposit-quality index, a strength knockdown. Read as relative density through a porosity-strength relation, 0.40 is about 87% dense and Utah's gate of 0.5 about 90%, far laxer than the proposal's 99%. The section [The deposition index is not a density](#the-deposition-index-is-not-a-density) gives two ways to fix it; both need your call.

**What the data supports for the proposal.** "In a synthetic version of the copper workflow, with both screens biased, searches that model the linked steps reached about 73% of the optimum after $100,000, against 14% for standard Bayesian optimization and 24% for screening with a nickel floor for seawater, which they matched with about a third of the spend. The immersion requirement separates them: a deposit that is not nearly fully dense fails it, and a model of the linked steps learns that from the intermediate measurements." The published one-step cost-aware rule reached 59% at the aluminum benchmark's production settings (7 of 20 seeds so far; 59% at the first sweep's light settings). The claim that choosing the stage beats running the full chain is not supported on this network. Edison's suggested wording is under Quality checks.

**The proposal is unchanged this session.** Fig. `fig:sim` (`bofn_cu_best_vs_spend_k1_partial_vs_full.png`) and the paragraph still show the first sweep: light-settings pKGFN and the spec's tiered rule. [`variants/bofn_cu_best_vs_spend_k1_partial_vs_full_current.png`](variants/bofn_cu_best_vs_spend_k1_partial_vs_full_current.png) has the high-fidelity pKGFN, and [`variants/bofn_cu_best_vs_spend_k1_partial_vs_full_corrosion_aware_tiered.png`](variants/bofn_cu_best_vs_spend_k1_partial_vs_full_corrosion_aware_tiered.png) uses the corrosion-aware tiered baseline. Switching the proposal is a decision: `python plot.py --proposal` overwrites Fig. `fig:sim`, and the PDF then needs a rebuild.

**Not done yet** ([`logs/plan.sh`](logs/plan.sh) resumes where this session stopped):
- pKGFN at the aluminum settings for the remaining seeds (6 and 8 to 19).
- The sensitivity cells (0, 0), (1, 0) and (0, 1).
- The new policies (`pkgfn_screen`, `pkgfn_audit`, `mines_only`, `funnel`), and with them the screen-audit and two-step tables.
- The S = 256 fidelity check.
- A decision on the deposition index and the Utah gate.
- The Edison analysis review of the high-fidelity results.

![partial vs full evaluation, current runs](variants/bofn_cu_best_vs_spend_k1_partial_vs_full_current.png)

*Best alloy demonstrated against new spend at `(kappa, eta) = (1, 1)`, with pKGFN at the aluminum production settings (7 seeds) and every other policy at 20 seeds. The proposal's Fig. `fig:sim` is the same plot from the first sweep (light-settings pKGFN, 20 seeds): [`bofn_cu_best_vs_spend_k1_partial_vs_full.png`](bofn_cu_best_vs_spend_k1_partial_vs_full.png).*

![corrosion-aware tiered baseline](variants/bofn_cu_best_vs_spend_k1_partial_vs_full_corrosion_aware_tiered.png)

*The same with corrosion-aware tiered screening (Ni ≥ 10 wt%, reference-coupon screen gate) as the tiered baseline.*

![all policies](bofn_cu_best_vs_spend_k1e1_all_policies.png)

![where the money went](bofn_cu_allocation_k1e1.png)

*Purchases per $100k (mean over seeds) at (1, 1), excluding the shared seed data.*

### Every policy, best alloy demonstrated (% of optimum, mean ± SE over seeds)

**`(kappa, eta) = (1, 1)`** (the crack screen misses the nucleant; the one-hour screen misses beta-prime):

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | 3% ± 5 | 25% ± 10 | 59% ± 11 | $100k (57% of seeds) | >$100k (43% of seeds) | >$100k (29% of seeds) |
| pKGFN, light settings (first sweep) | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 | $86k (60% of seeds) | >$100k (35% of seeds) | >$100k (5% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 14% ± 5 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| Tiered screening | 20 | -9% ± 5 | -9% ± 5 | -8% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt% | 20 | -7% ± 5 | 1% ± 5 | 10% ± 6 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 8% ± 4 | 16% ± 4 | 24% ± 5 | >$100k (10% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:

| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |
|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | 19% ± 10 | 30% ± 12 | 71% ± 6 | $54k (86% of seeds) | $92k (57% of seeds) | >$100k (29% of seeds) |
| pKGFN, light settings (first sweep) | 20 | 19% ± 6 | 37% ± 7 | 68% ± 4 | $52k (80% of seeds) | $78k (60% of seeds) | >$100k (25% of seeds) |
| BOFN, full pipeline | 20 | 15% ± 6 | 39% ± 9 | 73% ± 7 | $67k (85% of seeds) | $74k (75% of seeds) | $88k (70% of seeds) |
| BOFN + lot reuse | 20 | 13% ± 4 | 32% ± 8 | 72% ± 7 | $54k (85% of seeds) | $65k (85% of seeds) | $81k (65% of seeds) |
| Tiered screening | 20 | -8% ± 5 | -8% ± 5 | -6% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt% | 20 | 2% ± 4 | 7% ± 4 | 13% ± 5 | >$100k (0% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 8% ± 4 | 16% ± 4 | 24% ± 5 | >$100k (10% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |
| Standard BO | 20 | 6% ± 3 | 7% ± 3 | 14% ± 6 | >$100k (15% of seeds) | >$100k (5% of seeds) | >$100k (5% of seeds) |
| Random | 20 | -1% ± 4 | 7% ± 5 | 22% ± 5 | >$100k (5% of seeds) | >$100k (0% of seeds) | >$100k (0% of seeds) |

Matched seeds (Wilcoxon signed-rank; every pair and both speed-up tables in [`tables.md`](tables.md)):

| pKGFN: picks the stage against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |
|---|---|---|---|---|
| pKGFN, light settings (first sweep) | 7 | -11 points (3/0/4; p = 0.58) | -2 points (3/0/4; p = 0.94) | -5 points (3/0/4; p = 0.69) |
| Tiered screening | 7 | +17 points (6/1/0; p = 0.031) | +37 points (7/0/0; p = 0.016) | +69 points (7/0/0; p = 0.016) |
| Tiered, Ni ≥ 10 wt% | 7 | +14 points (5/1/1; p = 0.094) | +30 points (6/0/1; p = 0.047) | +53 points (7/0/0; p = 0.016) |
| Tiered, Ni ≥ 10 wt%, reference screen | 7 | -7 points (2/0/5; p = 0.47) | +4 points (5/0/2; p = 0.69) | +31 points (6/0/1; p = 0.047) |
| BOFN, full pipeline | 7 | -21 points (0/0/7; p = 0.016) | -21 points (1/0/6; p = 0.22) | -29 points (1/0/6; p = 0.047) |
| BOFN + lot reuse | 7 | -14 points (1/0/6; p = 0.11) | -15 points (2/0/5; p = 0.38) | -3 points (3/0/4; p = 0.81) |
| Standard BO | 7 | -0 points (2/1/4; p = 0.84) | +20 points (4/0/3; p = 0.22) | +47 points (5/0/2; p = 0.078) |
| Random | 7 | +4 points (4/1/2; p = 0.56) | +22 points (5/0/2; p = 0.16) | +40 points (6/0/1; p = 0.031) |

Purchases per $100k:

| Policy | n | C ($10) | A ($400) | U ($500) | M ($1,500+) | S ($100) | T ($200) | K ($50) | I ($400) | new lots | Mines sessions that paid a scale-up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pKGFN: picks the stage | 7 | 4.6 | 17.6 | 16.3 | 37.9 | 13.4 | 5.9 | 11.9 | 11.3 | 17.6 | 12.7 |
| pKGFN, light settings (first sweep) | 20 | 6.7 | 12.4 | 11.3 | 40.5 | 15.7 | 7.2 | 14.0 | 12.8 | 12.4 | 12.3 |
| BOFN, full pipeline | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| BOFN + lot reuse | 20 | 12.6 | 12.6 | 12.6 | 29.3 | 29.3 | 29.3 | 29.3 | 29.3 | 12.6 |  |
| Tiered screening | 20 | 224.0 | 22.8 | 44.2 | 24.9 | 24.9 | 24.9 | 24.9 | 4.0 | 22.8 |  |
| Tiered, Ni ≥ 10 wt% | 20 | 224.0 | 31.0 | 67.4 | 18.4 | 18.4 | 18.4 | 18.4 | 2.5 | 31.0 |  |
| Tiered, Ni ≥ 10 wt%, reference screen | 20 | 224.0 | 26.5 | 53.6 | 21.1 | 21.1 | 21.1 | 21.1 | 9.9 | 26.5 |  |
| Standard BO | 20 | 19.7 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |
| Random | 20 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 | 21.0 |  |


<!-- /RESULTS -->

<!-- WHY -->
## Why the copper results differ from the aluminum ones

[`compare/`](compare/) puts the two benchmarks side by side; every table is in [`compare/tables.md`](compare/tables.md). The two use the same baseline code, the same five seed draws per seed (uniform on [0, 1]^7, mapped onto different truths), the same GP code and the same budget. Four differences explain the gap, in this order:

**1. The copper objective is a needle; the aluminum one is a hill. The needle is the immersion gate acting on the deposit's density.** On 10^6 uniform random designs ([`compare/landscape.py`](compare/landscape.py), [`compare/needle.py`](compare/needle.py)):

| | Al (kappa = 1) | Cu (1, 1) | Cu (1, 1), no immersion gate |
|---|---|---|---|
| share of designs with J > 0 | 28% | **3.0%** | 20% |
| share with J at least 60% of J* | 3.3% | **0.23%** (14× less) | 0.78% |
| share with J at least 80% of J* | 0.51% | **0.012%** (43× less) | 0.036% |
| expected best of the 26 designs a random search sees (5 seed + 21 new) | 62% | **12%** | 45% |
| the five shared seed designs (mean best over 20 seeds) | +35% | **−10%** | |

- **Most of the needle is in the deposit, not the composition.**
  - Only 3.2% of random copper designs pass immersion (`m >= m_ref`). Had the same designs deposited fully dense, 62% would. Edison reproduced this independently: 3.19% and 61.5%.
  - The immersion index loses 0.03 for every 0.1 of `rho_m` (the `0.30 (1 − rho_m)` term), against a sigmoid gate 0.05 wide. A deposit below about 0.9 therefore fails immersion and forfeits most of its strength credit; an alloy well below the reference scores about minus 0.3 times its burden. Only 0.14% of random designs deposit that densely.
  - In aluminum a porous build lost strength in proportion and kept the rest.
  - Composition matters too, though less. At each composition's best settings, 84% of random aluminum compositions and 31% of copper ones can reach 60% of the optimum. At the optimum's settings, 66% and 5% can.
- **The burden also fights the gate.** It puts its heaviest weight (1.0) on Ni, the element immersion needs. In aluminum the heavily weighted element, Sc, had a cheap substitute, Zr, for the same nucleant.
- **The random rows follow the landscape.** Random reached 68% in aluminum and 22% in copper, against expected bests of 62% and 12% for its 26 designs.

![the two landscapes](compare/compare_landscape.png)

*Share of uniform random designs that reach each fraction of the optimum (log scale).*

![composition slices](compare/compare_landscape_maps.png)

*A composition slice through each optimum, each point at its best atomizer, power and speed (2,048 settings). At the best settings both are broad hills. The copper needle comes from the process: a deposit that is not nearly fully dense fails immersion.*

**2. The gate is what breaks the model-free baselines, and the network's intermediate outputs are what let BOFN through it.** On the same copper network, stages, costs and seeds, the ablation scores J = U − 0.3 B instead of the gated objective ([`compare/results-nogate/`](compare/results-nogate/), 20 seeds each, as % of that truth's optimum, 0.745):

| Policy | Cu (1, 1) as benchmarked | Cu without the immersion gate | Al (kappa = 1) |
|---|---|---|---|
| BOFN + lot reuse | 72% ± 7 | **88% ± 2** | 90% ± 2 |
| BOFN, full pipeline | 73% ± 7 | **85% ± 5** | 86% ± 4 |
| Standard BO | 14% ± 6 | **65% ± 4** | 84% ± 3 |
| Random | 22% ± 5 | **51% ± 3** | 68% ± 2 |
| the shared seed data (start) | −10% | 23% | 35% |

- **Without the gate, the network-aware policies land where they did in aluminum.** The model-free baselines recover most of the way: in Edison's words, the gains are about 73% (standard BO) and 62% (random) of their Al-to-Cu drops "numerically, not as identified causal fractions". The rest is the narrower copper landscape: the expected best of 26 random designs is 45%, against 62% in aluminum.
- **This is a compound ablation.** Removing the gate also changes what BOFN and standard BO buy. Only for random are the designs identical with and without the gate, which makes its row a clean rescoring.
- **With the gate, standard BO's GP learns the wrong lesson.** 97% of designs return only minus their burden, a sloped floor that tells it to cut nickel, away from the alloys that pass.
- **BOFN models density, the immersion index and strength as separate nodes.** Those nodes carry signal even when an alloy fails immersion. That is the network's advantage on this problem, and why it is so large.

**3. A copper composition shows its value only after four or five more purchases, and one-step KG is flat until something passes immersion.** An aluminum powder needed a print and a tensile test. A copper lot needs a Mines session, microscopy, tensile, the one-hour screen and immersion. While no demonstrated alloy has J > 0, KG has nothing to improve on. This is the aluminum README's finding ("one-step KG can't see that a powder's value only shows once it is printed"), with two to three times as many steps between a purchase and its payoff.

| Policy, (1, 1), 20 seeds | median new spend to the first demonstrated alloy with J > 0 (all seeds) | seeds that reach one by $100k |
|---|---|---|
| BOFN, full pipeline | $14k | 20 |
| Tiered, Ni ≥ 10 wt%, reference screen | $19k | 17 |
| BOFN + lot reuse | $21k | 20 |
| Standard BO | $24k | 20 |
| Random | $31k | 17 |
| pKGFN, light settings (first sweep) | $39k | 19 |
| pKGFN, aluminum settings (7 seeds so far) | $47k | 6 of 7 |

Medians are over all 20 seeds; a seed that never demonstrates one counts as more than $100k. The shared seed data of five seeds already holds such an alloy. J > 0 is not the same as a hard immersion pass, because the gate is a sigmoid. Of the light-settings pKGFN's purchases made before it had such an alloy, the EI fallback made 42% because KG was flat; after, it made 4% ([`compare/tables.md`](compare/tables.md); each purchase is classified by the state when it was made, as Edison corrected).

**Unfinished builds matter more.** The light-settings pKGFN deposited about 40 builds per run at Mines but carried only about 6 through tensile and immersion; BOFN carried all 21 of its builds through. Edison scored every deposited design against the truth, an oracle the policy cannot use. The best of pKGFN's builds is worth 68.5% of the optimum, against 58.6% demonstrated, so unfinished validation explains at most about 10 of its 15-point gap to BOFN.

**4. Tiered screening's shortlist rule fails for a different reason on each network.**
- In aluminum, the shortlist was the right family with the optimum screened out: a 65% ceiling, and tiered screening reached 63%.
- In copper, ranking by CALPHAD strength net of a Ni-heavy burden picks aluminum bronzes with 2 to 6 wt% Ni. None of the 80 shortlisted compositions (20 seeds × 4) can pass immersion at any settings: the ceiling is −19%.
- A corrosion-aware shortlist (Ni ≥ 10 wt%) raises the ceiling to 60%. The bottom line has what it reaches.

**What does not explain it.**
- **Costs.** $4,760 against $4,210 per full chain: the copper runs fit 21 full chains, the aluminum ones 23. Edison cut the aluminum runs at 21 chains: standard BO, random and BOFN drop by only 3.3, 3.6 and 0.7 points, against Al-to-Cu drops of 69, 46 and 13.
- **The baselines' code.** EIFN, BOFN + reuse, standard BO and random use the same pools (1,024 or 2,048 Sobol designs plus local perturbations), the same 64 Monte Carlo samples and the same GP code in both benchmarks.
- **pKGFN's code.** It differs from the aluminum version in ways that matter for pKGFN alone:
  - EI is measured from the best demonstrated alloy, not the best posterior mean.
  - The fallback prices the path to a validated build.
  - There are three test bundles.
  - Tests are limited to N_CAND candidates per stage; in aluminum every untested build was a candidate.
  - The first sweep's settings were lighter.
  
  The re-run at the aluminum settings tests the last one (bottom line). None of these touches the baselines' 40 to 70 point drops.
<!-- /WHY -->

## The deposition index is not a density

The two DED nodes return `rho = window × q^0.3 × (1 − 0.75 crack) × (1 − lof)`, with an extra factor of `0.95 + 0.05 q` at Utah. It is a product of four factors on [0, 1], strength is proportional to it (`U ∝ rho_m`), and it lowers the immersion index. Calling it a "dense, crack-free index" invites reading it as relative density, and read that way its values make no sense. The median 0.40 that copper-rich alloys reach at Utah would mean 60% porosity, which no DED deposit has: an under-powered copper deposit is roughly 80 to 95% dense, or it does not build at all.

![the deposition index, factor by factor](compare/density_factors.png)

*The 200 copper-rich compositions of required property 4 (Ni and Al under about 2 wt% each), each at its best Utah and Mines settings over 16,384 settings ([`compare/density.py`](compare/density.py), [`compare/density.json`](compare/density.json)).*

- **Where the 0.40 comes from.** It is the lack-of-fusion factor alone. At their best settings, the process window, the powder and the crack factor are 0.96 to 1.00 at both sites. `1 − lof = sig((P − h)/0.08)` is 0.41 at Utah, where power is capped at 0.5 and copper-rich alloys have a conductivity index `h` of about 0.53. At Mines (best P about 0.75) it is 0.94.
- **What the index can stand for.** The exponential porosity-strength relation, `index = exp(−b φ)` with porosity φ and b between 4 and 10, reads the index as the strength knockdown of a porous deposit. Under that reading the values become plausible relative densities (b = 7, with b = 4 to 10 in brackets):
  - 0.40 is 87% dense (77 to 91%).
  - Utah's gate of 0.5 is 90% dense (83 to 93%).
  - 0.88, copper-rich at Mines, is 98.2% dense.
  - 0.93, the optimum at Mines, is 99.0% dense.
  
  So the shape of the truth is defensible, but its name and the Utah gate are not.
- **The gate does not match the proposal.** The proposal scales up "only compositions whose small blocks at Utah reach 99% relative density" (`onr-yip-technical-proposal-cu-ded.tex`, line 907). Under the b = 7 reading that is an index of about 0.93. The benchmark's gate, `rho_u >= 0.5` (tiered screening, the funnel and the screen-trusting pKGFN variants), is about 90%, much laxer.
- **Options for the next round (your call).**
  - (a) Keep the truth. Call the node "deposit quality (a strength knockdown; 0.93 is about 99% dense)" in the README and in Fig. `fig:synth` (now "Dense index" and "Dense fraction"), report the implied relative density, and move the Utah gate to the proposal's 99% (index 0.93).
  - (b) Rewrite the two nodes to return relative density, `1 − φ`, with lack-of-fusion porosity up to about 20% and keyhole porosity up to about 10%, plus a separate crack index, and knock strength down by `exp(−b φ)`.
  
  (b) is more physical, but it changes what every GP models, so every run would have to be redone. Neither changes the runs reported here: the policies see the node only through their GPs.


![network](bofn_cu_network_strip.png)

- **Design space (7-D, all scaled to [0, 1]; copper is the balance):** Ni 0 to 30 wt%, Al 0 to 9.5, Fe 0 to 4.5, Mn 0 to 4 (the proposal's Table `tab:space`); ultrasonic atomizer setting; laser power (about 0 to 1 kW; Utah's MX-Lab is capped at 0.5 of the scale); travel speed.
- **Network:** one GP per node, and each node's output feeds its children.
  - CALPHAD and heat flow return four things in one call: strengthening potential `s`, solidification index `f`, nucleant fraction `g` (the iron-rich primary kappa particles) and a conductivity index `h`. The spec named three outputs; `h` was added so the lack-of-fusion term is a function of node inputs.
  - Atomization returns powder quality `q` from the atomizer setting, Mn and `f` (which stands in for the liquidus margin, since both rise with nickel).
  - Small DED at Utah returns a deposit-quality index `rho_u` (dense and crack-free, 0 to 1; a strength knockdown, not a relative density: see [The deposition index is not a density](#the-deposition-index-is-not-a-density)) from power (capped at 0.5), speed, `f`, `g`, `h` and `q`.
  - Large DED at Mines returns the same index `rho_m` from the same inputs at full power. Its GP also takes `rho_u` as an input so the model can learn the small-to-large transfer; the truth links the two only through shared parents.
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

**The optimum**, by multi-start local search from the 20 best of 400,000 random designs (`check_truth.py`; every "% of optimum" in this README is normalized by it):

| (kappa, eta) | J* | Ni | Al | Fe | Mn | a | P | v | s | f | g | h | q | rho_u | rho_m | beta | U | w | m | burden |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (1, 1) headline | **0.492** | 0.43 | 0.58 | 0.50 | 0.00 | 0.64 | 0.58 | 0.34 | 0.73 | 0.74 | 0.41 | 0.12 | 0.81 | 0.79 | 0.93 | 0.15 | 0.76 | 0.88 | 0.95 | 0.61 |
| (0, 0) | **0.382** | 0.32 | 0.38 | 0.40 | 0.00 | 0.50 | 0.63 | 0.48 | 0.55 | 0.40 | 0.29 | 0.21 | 0.94 | 0.63 | 0.95 | 0.11 | 0.64 | 0.97 | 0.92 | 0.43 |
| (1, 0) | **0.492** | 0.43 | 0.58 | 0.50 | 0.00 | 0.64 | 0.58 | 0.34 | 0.73 | 0.74 | 0.41 | 0.12 | 0.81 | 0.79 | 0.93 | 0.15 | 0.76 | 1.00 | 0.95 | 0.61 |
| (0, 1) | **0.382** | 0.32 | 0.38 | 0.40 | 0.00 | 0.50 | 0.63 | 0.48 | 0.55 | 0.40 | 0.29 | 0.21 | 0.94 | 0.63 | 0.95 | 0.11 | 0.64 | 0.79 | 0.92 | 0.43 |

- At `kappa = 1` the optimum is a copper-nickel-aluminum alloy with iron and no manganese: about 13 wt% Ni, 5.6 wt% Al and 2.2 wt% Fe, in the family of the high-strength Cu-Ni-Al alloys. Its solidification index is 0.74, far above the screen's 0.34, yet it deposits 93% dense because the iron-rich nucleant cuts the effective index to about a third. `eta` changes only the one-hour screen, so (1, 0) has the same optimum, and (0, 1) the same as (0, 0).
- At `kappa = 0` the optimum is leaner (about 10 wt% Ni, 3.6 wt% Al, 1.8 wt% Fe) at `f` = 0.40, just above the screen's cutoff.

**Required property 1 (the screens and the optimum).** At (1, 1) the optimum fails the CALPHAD crack screen (`f` = 0.74 > 0.34). The best design that passes it scores 72% of the optimum (about 8.5 wt% Ni, 3.3 wt% Al, 2.3 wt% Fe), which is the ceiling for tiered screening. At (0, 0) the best design passing both screens keeps 92% of the optimum (the spec asks for at least 85%). The one-hour screen ranks the optimum at the top of the dense candidates in every cell, so it is the CALPHAD screen that cuts the optimum off (see Caveats).

**Required property 2 (reference alloys at their best settings for J, headline world).**

| Alloy | J (% of J*) | strength U | rho_m | beta | immersion m | passes immersion | burden |
|---|---|---|---|---|---|---|---|
| C71500 (70-30 Cu-Ni) | -0.073 (-15%) | 0.48 | 0.85 | 0.00 | 0.85 | yes | 1.04 |
| C70600 (90-10 Cu-Ni) | 0.120 (24%) | 0.38 | 0.96 | 0.00 | 0.87 | yes | 0.37 |
| C95800 (NAB) | -0.146 (-30%) | 0.79 | 0.92 | 0.48 | 0.55 | no | 0.49 |

C71500 passes by definition (`m_ref` is its immersion index); C70600 is weaker and passes with a third of the nickel; C95800 (NAB) is the strongest but carries retained beta-prime (0.48) and fails. C71500 and NAB score below zero because of their burden and the immersion gate. At `kappa = 0` C71500 cracks (see Caveats).

**Required property 3 (a ridge, not a point).** With the other inputs at the optimum, 17 points of a 101 × 101 (P, v) grid lie within 0.5% of J* (P from 0.53 to 0.64 along P − v ≈ 0.23) and 63 within 2% (P from 0.47 to 0.68). The ridge is shorter than the aluminum one because lack of fusion ends it at low power and keyholing at high power.

**Required property 4 (Utah's power cap).** For 200 random copper-rich compositions (Ni ≤ 0.07 and Al ≤ 0.2 scaled, under about 2 wt% each), the median best `rho_u` at Utah's cap is 0.40 against 0.88 at Mines; 15% cannot reach 0.3 at Utah, and 100% reach 0.7 at Mines. At the optimum's composition the cap does not bind (0.92 at Utah, 0.93 at Mines).

Every value above is in [`truth_tables.md`](truth_tables.md), for all four cells.

## Policies (all on equal $100k of new spend)

| Policy | What it does each step |
|---|---|
| **pKGFN** | For each stage (CALPHAD; atomize a simulated composition; Utah or Mines on an existing lot; microscopy, tensile, screen or immersion on an existing build), it computes the knowledge gradient per dollar of one more query and buys the best one. It also prices three test bundles (microscopy + tensile, microscopy + screen + immersion, screen + immersion), each valued by the knowledge gradient of its last stage with the intermediate outputs at their posterior means, because one-step KG gives microscopy almost no value of its own (its value is to unlock the tests). |
| BOFN, full pipeline (EIFN) | The same network model. It picks a design by network expected improvement, then runs all eight stages on it ([Astudillo & Frazier 2021](https://arxiv.org/abs/2112.15311)). |
| Tiered screening | As the spec describes it: CALPHAD on 256 compositions (224 new calls on top of the 32 seed compositions; with the five seed alloys, it ranks 261); keep the four strongest with `f <= 0.34`, net of burden; then EI on its own records over those four, where each step is a chain: Utah tracks until the small blocks reach the density target (`rho_u >= 0.5`), scanning travel speed at Utah's full capped power (0.25, 0.45, 0.65) and retiring a lot that fails all three; then Mines (the first build on a lot at the setting that passed at Utah, later ones at the EI choice), microscopy, tensile, the screen, and immersion only if the screen passes. Lots and scale-ups are reused. The first version drew Utah settings from EI on records that a Utah failure leaves flat, and spent about $90k on 182 Utah sessions of one lot that cannot pass; those runs were discarded. On this network the shortlist is aluminum bronzes with 2 to 6 wt% Ni that fail immersion (see Bottom line). |
| Standard BO (EI) | A single GP from the 7 inputs to the objective, all eight stages run per design. |
| Random | Uniform designs, all eight stages run. |
| *Ablation:* BOFN + lot reuse | Network EI per dollar over new designs *and* new Mines sessions on existing lots (every later stage runs). This is partial evaluation without KG's choice of stage. |
| `tiered_ni` (corrosion-aware tiered screening, Oct 27) | Tiered screening whose shortlist keeps only compositions with at least 10 wt% Ni, the 90-10 Cu-Ni seawater floor. Few compositions with 10 wt% Ni pass the crack screen (none in 14 of 20 seeds), so the rule needs a decision. When fewer than four pass, the shortlist is filled with the eligible compositions CALPHAD rates least crack-prone (lowest `f`): the crack screen becomes a ranking rather than a cutoff. Everything else is as in tiered screening, including the spec's one-hour-screen gate (top quartile of every screened build so far). |
| `tiered_ni_ref` (Oct 27) | `tiered_ni` with a corrosion-aware screen gate: a build goes to immersion if its one-hour screen is at least that of a reference coupon, dense C70600 (90-10 Cu-Ni, `w` = 0.71 at `eta = 1`). C70600 passes immersion in every cell. A lab would run the coupon alongside its builds; its screen value comes from the truth, as `m_ref` does. |
| `pkgfn_screen` | pKGFN that trusts the screens: it does not atomize a composition the CALPHAD screen rejects, does not send a lot to Mines before its Utah blocks pass the density gate, and does not immerse a build the one-hour screen stops. |
| `pkgfn_audit` | `pkgfn_screen` with Advance 5's audit: about one in ten candidates a screen would stop goes on anyway (a fixed hash of seed, gate and candidate), plus every candidate that misses a cutoff by less than 0.03 (the CALPHAD screen, the one-hour screen) or 0.05 (the Utah density gate). |
| `mines_only` | pKGFN with no new Utah purchases (the five seed designs' Utah results stay in the data): every new composition goes straight to a 2 kg lot and Mines. The difference to pKGFN is what the two-step DED split buys, the premise of the budget. |
| `funnel` | A fixed top-k funnel at every gate (Reyes, Liu and Diaz Vargas, JOM 2022, found that a sensible funnel can lose to random): the CALPHAD shortlist's top 12, atomized at a = 0.5; the top 6 by powder quality; three Utah settings each and the top 3 by density; two Mines sessions each; the top 3 by the screen go to immersion; then the tiered loop on the finalists. Each gate's false rejections are judged from the truth afterwards. |

### pKGFN implementation notes

[`bofn_alloy.py`](bofn_alloy.py) implements the method from scratch, as `bofn-prelim` does, and does not use the upstream `partial_kgfn` package.

- **GPs:** each node is an exact GP with BoTorch-fitted RBF hyperparameters; fantasy updates are closed-form rank-one, so every KG candidate is scored in one vectorized pass. Fit failures are counted (`gp_fits` in every run JSON).
- **KG:** the inner max runs over a shared design set: every deposited design (the incumbent among them), the top posterior-mean and top-EI designs of the pool, and the design attached to every candidate, deduplicated (since Oct 27, after the Edison code review's finding F2; before, the set was not explicitly anchored and duplicate designs got independent Monte Carlo errors). Fantasies use 10 Gauss-Hermite nodes, and a 2-point-per-output product rule (16 points) for the four CALPHAD outputs. The current value comes from the same fantasy-averaged estimator, so the estimated KG is never negative. Base samples are common random numbers across candidates and fantasies.
- **Candidates** for each stage are the EI-ranked members of a Sobol pool plus perturbations of validated designs. They are ranked by network EI over the best alloy demonstrated so far, as in EIFN. The aluminum version measured EI from the best posterior mean; on this network that is a pure-copper design whose immersion gate is shut (its burden is zero and so is its strength once gated), every EI came out zero, and on one seed the first runs stopped after $4,750. Ties at zero EI are broken by the posterior mean.
- **Fallback:** when KG is numerically zero for every candidate, the policy buys the candidate with the highest network EI per dollar of the cheapest path to a validated build (this purchase plus whatever Mines session and tests it still needs), and if every EI is zero too, the one with the most optimistic posterior sample, so it does not stop while a stage other than CALPHAD is affordable. Until Oct 27 the EI tested for Utah and Mines candidates included the 1e-9 posterior-mean tie-break, so an all-zero case could take the EI branch (Edison finding F4); the tie-break now only ranks. The aluminum version divided EI by the cost of the next stage alone. On the copper network, where KG is often flat until some alloy passes immersion, that made the first headline runs buy 58 to 68 lots and 87 to 121 Utah sessions per $100k and validate almost nothing (seeds 2 and 3 ended below zero); those runs were discarded and the sweep restarted. The share of purchases made by the fallback is in the quality table.
- **Monte Carlo settings (Oct 27): the aluminum benchmark's production settings.** 64 base samples, 16 candidates per stage, a 512-design Sobol pool, 32 + 16 anchors and 24 perturbations of each of the 8 best pool designs, as in `bofn-prelim`. The first copper sweep ran lighter on every one of these (32, 10, 256, 24 + 12 and 16), "because the copper network has eight stages and three test bundles to score"; those 20 runs are kept in [`quality/results-light/`](quality/results-light/) and compared below. At these settings a run takes about 25 to 35 minutes on one core, 2.9 times the light setting. Every run stores its settings and `CODE_VERSION`, and `run_sweep.py` will not resume a stored run whose settings differ from the code's (Edison finding F9).

## Caveats (read before quoting numbers)

- **Synthetic truth.** The node functions are hand-built to mirror the qualitative metallurgy (solid-solution and kappa strengthening, a Scheil-type crack criterion with nucleant-driven suppression, a constant-energy-density process ridge with keyholing and lack of fusion, a nickel film, selective attack of beta-prime). Nothing is fitted to data. The bias knobs are the places the benchmark is designed to make the screens wrong.
- **At `kappa = 0`, 70-30 Cu-Ni cracks.** In the world where the Scheil index is taken as exactly right, the wide Scheil range of 70-30 Cu-Ni (`f = 0.72`) makes it crack (`rho_m = 0.26` at its best settings) and fail immersion. 70-30 copper-nickel is routinely welded, which is one reason to read `kappa = 1` as the more realistic copper world, but the sensitivity cells keep `kappa = 0` as the case where the crack screen is right.
- **The one-hour screen never stops the optimum.** In every cell the optimum ranks in the top quartile of dense candidates on the one-hour screen, so the screen's blind spot (`eta = 1`) costs wasted immersions and false rejections of other candidates, not the optimum itself. The CALPHAD screen is the one that cuts the optimum off at `kappa = 1`.
- **Simplifications.** Observations are noise-free. There is one scalar objective (strength gated by immersion, minus the burden), not the proposal's several objectives (Advance 1). One experiment at a time, with no delays (the delays are in `step-costs` but not modelled; Advance 2 is future work). One parameter set per Mines build.
- **Costs.** The step costs are the project's own round all-in estimates. Outside the loop and not modelled: the yearly gas atomization of the finalist (about $12,500 a run), the combustible-dust tests, and the flowing-seawater tests at Carderock (free to the project, months).
- **pKGFN implementation.** It is discrete and one-step myopic. Since Oct 27 it runs at the aluminum benchmark's production Monte Carlo settings; the first sweep's lighter runs are kept for comparison. Treat its numbers as those of this implementation at these settings.

## Quality checks

**GP fitting.** Fit failures are counted in every run (`gp_fits`); the table at the end of [`tables.md`](tables.md) sums them per cell, with the share of pKGFN-type purchases chosen by the EI fallback because KG was flat. In the replayed seed-0 run below, none of 137 fits failed; fitted lengthscales ranged from 0.13 to 254 (median 0.91), none at BoTorch's lower bound of 0.025 and 3% above 10 (input directions learned as nearly flat).

**Monte-Carlo noise in the knowledge gradient** ([`quality/mc_noise.py`](quality/mc_noise.py), seed 0 at (1, 1)). The run was replayed (it reproduces the stored run: 62.8% of the optimum at $100k), and at iterations 4, 12, 24 and 40 the very same candidate sets were re-scored with five other base-sample draws at S = 32 (for the MC standard error) and with S = 1,024 as a reference:

| iteration | stage chosen at S = 32 | stage at S = 1,024 | same design | gap between best and second-best stage, in MC standard errors |
|---|---|---|---|---|
| 4 | Mines | Mines | no | 1.6 |
| 12 | microscopy + screen + immersion | microscopy + screen + immersion | yes | 0.7 |
| 24 | tensile | tensile | yes | 0.4 |
| 40 | Mines | CALPHAD | no | 0.3 |

The stage choice survived at three of four probed iterations and the design at two. The gaps between the best and second-best stage were all within 1.6 MC standard errors, so these were close calls, and at iteration 40 the reference put CALPHAD first by a wide margin (KG per dollar 3.3e-5 against 4.4e-7 for the Mines session chosen at S = 32), where S = 32 returned zero for CALPHAD. As in the aluminum version, the production setting underestimates the small knowledge gradients of cheap stages. Results are in [`quality/mc_noise_k1e1_s0.json`](quality/mc_noise_k1e1_s0.json).

**Independent review** (Edison Analysis, task `42ee31fc`, Oct 25; report [`edison/results/code-review.md`](edison/results/code-review.md), full transcript [`edison/results/code-review.json`](edison/results/code-review.json), brief [`edison/brief-code.md`](edison/brief-code.md)). Uploaded: the code, this README as it then stood, `settings.md` and the 78 headline runs finished at the time (no tiered runs yet; an earlier submission failed without an answer and one was cancelled after the fallback fix, both kept in `edison/results/`). It verified the GP posterior against BoTorch and a dense solve, the rank-one fantasy update against explicitly augmented GPs for all eight stages, and the cost ledger of every uploaded run, and found no GP-fit failure in 18,774 fits. It ran its own 20 tiered runs: they end at -7.7% of the optimum, and none of their 80 new immersions passes, which matches the stored runs. Its findings, and what was done about each on Oct 27:

- The speed-up over tiered screening is measured against a level below where the other policies start, so it measures nothing useful. **Addressed:** the speed-up is now also measured against corrosion-aware tiered screening (`tiered_ni_ref`, 24% at $100k), a level the other policies have to work for.
- The inner maximization is not explicitly anchored on the incumbent, and duplicate designs get different Monte Carlo estimates. At S = 32 the stage ranking is unstable: at iteration 40, five other draws chose M, M, M, U and A where S = 1,024 chose CALPHAD, as the noise check above found. **Fixed:** every deposited design is now in the inner set, which is deduplicated, and the production settings are the aluminum ones (S = 64).
- **A bug:** the fallback's test for positive EI on Utah and Mines candidates includes the 1e-9 posterior-mean tie-break, so a case where every EI is zero can take the EI branch instead of the optimistic-sample branch. **Fixed**, and pKGFN is being re-run (below).
- The test bundles are plug-in, last-stage heuristics, not multistage KG. Still open.
- `check_truth.py` prints the required properties but asserts none of them. Property 4 holds for the median copper-rich composition, not for all of them: 15% can still pass Utah's density gate. **Fixed:** `check_required` asserts all four, and `python check_truth.py --check-stored` checks `truth_tables.json`; all hold.
- `run_sweep.py` resumes from any existing file without checking its settings or code version. **Fixed:** it compares the stored settings and `CODE_VERSION` and refuses to resume a mismatch unless given `--rerun`.
- The audit table is descriptive, not an unbiased estimate: near-cutoff cases are oversampled, and the truth check uses the final gate. Still open (no audit runs yet).
- Wording, fixed above: the fallback does stop if only CALPHAD is affordable; `mines_only` keeps the five seed Utah results.

**Independent review: copper against aluminum** (Edison Analysis, task `009f44cb`, Oct 27). Report: [`edison/results/compare-review.md`](edison/results/compare-review.md); its recomputation, notebook and CSVs: `edison/results/compare-review-*`; brief: [`edison/brief-compare.md`](edison/brief-compare.md). Uploaded: both benchmarks' code, the copper README as it stood mid-session, [`compare/`](compare/) with its tables, and both result sets. That is 186 copper runs (the high-fidelity pKGFN re-runs had not finished) and 164 aluminum runs.
- **Every number reproduces.** It recomputed every populated cell of the side-by-side, no-gate and tiered tables from the JSON, independently of our scripts, and found no discrepancy.
- **Ranked explanations.** First, the immersion and deposition geometry plus the seed state dominate the model-free drops. Second, the shortlist rule causes the tiered drop. Third, the long validation path, myopic KG and unfinished builds cause pKGFN's. The effect sizes of the pKGFN implementation differences (EI incumbent, path-priced fallback, bundles, light settings) are "not identified". Cost differences are small. This README's section on the differences follows that ranking and quotes its numbers.
- **Corrections, applied above.**
  - The first-alloy medians are over all seeds.
  - The fallback split classifies each purchase by the state before it (42% and 4%).
  - J > 0 is not a hard immersion pass.
  - Aluminum fit 23 full chains, not 24.
  - The no-gate comparison is a compound ablation except for random.
- **Corrosion-aware tiered.** It calls `tiered_ni_ref` "a defensible corrosion-informed comparator", with two caveats. Its reference screen value comes from the truth (a real coupon would cost money and carry noise). And its filled shortlists mostly violate the crack screen (6 of 80 compositions pass it). Its Utah failures reflect powder and settings, not chemistry: every stored Ni shortlist composition can pass Utah's gate at the right atomizer setting.
- **Density.** It agrees the index "can serve as a qualitative build-quality utility … but not as a measured fraction of theoretical density". It proposes a calibrated replacement: relative density from powder, lack-of-fusion and keyhole porosity; a separate crack index; and a fitted knockdown `U = U_dense (1 − φ)^n exp(−a φ_LOF − b c_crack)`.
- **Metric.** "Best alloy demonstrated" differs from the published pKGFN objective, which values the posterior-mean recommendation. Scored by `rec_printed`, light pKGFN is 67.9%, 5.4 points behind BOFN rather than 14.7.
- **Its proposal wording:** "In a synthetic copper directed-energy-deposition benchmark with a deliberately biased corrosion screen, full-pipeline function-network Bayesian optimization reached 73% of the truth's optimum after $100,000 of new purchases, compared with 14% for conventional Bayesian optimization; a corrosion-aware tiered comparator reached 24%. A light-setting partial-evaluation knowledge-gradient implementation reached 59% and did not beat full-pipeline search, so we will test whether validated, physically calibrated deposition and corrosion models and higher-fidelity acquisition settings change that ranking."

**Higher fidelity (Oct 27): pKGFN at the aluminum production settings.** The first sweep ran pKGFN lighter than bofn-prelim's production run on every setting: S = 32 base samples, 10 candidates per stage, a 256-design pool, 24 + 12 anchors and 16 perturbations. The headline pKGFN runs now use the aluminum settings (64, 16, 512, 32 + 16 and 24), with the two Edison fixes (F2 anchoring, F4 fallback). The settings and the fixes changed together, so this comparison does not separate them.

| pKGFN settings | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | KG-flat fallback share | C | A | U | M | S | T | K | I |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| light (first sweep): S = 32, 10 candidates, 256 pool, old fallback test; all seeds | 20 | 12% ± 6 | 27% ± 7 | 59% ± 5 | $86k (60%) | >$100k (35%) | 22% | 6.7 | 12.4 | 11.3 | 40.5 | 15.7 | 7.2 | 14.0 | 12.8 |
| light, the 7 seeds re-run so far | 7 | 15% ± 10 | 27% ± 12 | 64% ± 4 | $60k (71%) | >$100k (43%) | 27% | 6.9 | 15.1 | 10.4 | 39.6 | 16.9 | 7.6 | 15.4 | 14.1 |
| high fidelity (aluminum production): S = 64, 16 candidates, 512 pool, fixes F2 and F4 | 7 | 3% ± 5 | 25% ± 10 | 59% ± 11 | $100k (57%) | >$100k (43%) | 39% | 4.6 | 17.6 | 16.3 | 37.9 | 13.4 | 5.9 | 11.9 | 11.3 |

Matched seeds, high fidelity minus light (n = 7; wins/ties/losses; Wilcoxon): $25k -11 points (3/0/4; p = 0.58); $50k -2 points (3/0/4; p = 0.94); $100k -5 points (3/0/4; p = 0.69). BOFN (full pipeline) on the same seeds: 87% ± 4 at $100k; high-fidelity pKGFN minus BOFN: $25k -21 points (0/0/7; p = 0.016); $50k -21 points (1/0/6; p = 0.22); $100k -29 points (1/0/6; p = 0.047).

![fidelity](compare/compare_pkgfn_fidelity.png)

*pKGFN's best alloy demonstrated for every seed at both settings (thin lines) and their means (thick), with BOFN's mean (full pipeline) for reference.*

The S = 256 check stays queued at the end of [`logs/plan.sh`](logs/plan.sh).

## Reproduce

```bash
python -m venv /tmp/bofn-venv && /tmp/bofn-venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
/tmp/bofn-venv/bin/pip install botorch matplotlib scipy
cd benchmarks/bofn-cu-ded
python check_truth.py             # required properties, truth_tables.md
logs/plan.sh                      # the sweep in priority order (resumable; one JSON per run)
python analyze.py                 # tables.md
python plot.py                    # figures
python compare/landscape.py       # copper against aluminum: the two truths on random designs
python compare/density.py         # the deposition index, factor by factor
python compare/compare.py         # compare/tables.md and the compare_*.png figures (needs compare/results-nogate/)
```

The no-gate ablation runs with `BOFN_NOGATE=1 python run_sweep.py --cells 1,1 --seeds 0-19 --kinds eifn eifn_reuse ei random --out compare/results-nogate`.

The figures need the Aptos fonts in `~/.local/share/fonts/aptos/` (Microsoft's zip: `download.microsoft.com/download/8/6/0/860a94fa-7feb-44ef-ac79-c072d9113d69/Microsoft%20Aptos%20Fonts.zip`).

Per-run JSON (every purchase, spend and score, the builds and lots, GP-fit counts, and for the audit the screen and immersion events) is in `results/k<kappa>e<eta>/<policy>_s<seed>.json`.
