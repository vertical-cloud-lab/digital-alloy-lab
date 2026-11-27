# Outline and argument

*Draft of 2026-11-27 (issue [#120](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/120)).
Target: an* Advanced Materials *collection, due early 2028 (see [`README.md`](README.md#decisions-for-sterling)
on the date). The text is in [`manuscript.tex`](manuscript.tex); this file is the argument behind it.*

## 1. The thesis in one sentence

New printable aluminum alloys are scarce not for lack of candidate compositions but because powder for
an untested composition is hard to get and campaigns spend their budget in a fixed order; a laboratory
that makes powder for every candidate in 250 g lots, prints it in-house, and lets a cost-aware optimizer
choose which step to run next for each candidate finds [alloy] at [k]-fold lower cost than
screen-then-test, and the reason is that the cheap screen is wrong about the alloys that matter.

## 2. The argument, step by step

1. **Need.** LPBF prints few Al alloys. AlSi10Mg is the default; the stronger printable alloys rely on
   grain refiners, scandium above all, whose supply is insecure. A printable alloy is a supply decision
   as well as a metallurgical one.
2. **Bottleneck 1, powder.** Gas atomization works in lots far larger than a screening campaign needs, so
   most campaigns calculate, then test very few compositions, or blend elemental powders, or switch to
   DED. Ultrasonic atomization makes spherical powder from a few hundred grams, but nobody has shown
   that it is repeatable at fixed settings for Al, or that the powder's composition follows the charge.
   Without both, it can't be a step that an optimizer calls on demand.
3. **Bottleneck 2, decisions.** Step costs differ by orders of magnitude, yet campaigns run the steps in
   a fixed order. Screen-then-test is cheap but fails when the screen is wrong (CALPHAD crack indices
   don't see Zr/Sc nucleant refinement; equilibrium and Scheil miss melt-pool cooling rates). Full-chain
   testing is robust but spends most of the budget on candidates a cheap step could have dropped.
4. **The tool that fits.** Bayesian optimization of function networks with partial evaluations models
   the workflow as linked surrogates and picks the candidate and step with the most expected gain per
   unit cost. So far it has been tested only on synthetic and retrospective problems.
5. **What we did.** Built the whole loop in one lab: dosed charges, ultrasonic atomization, powder
   characterization, a desktop LPBF system, microstructure and mechanical tests, and an optimizer over
   all of them with measured step costs. Then ran a campaign in which the optimizer chose the step.
6. **What we show.** (i) The atomizer is a dependable step: repeatable, composition follows the charge.
   (ii) Desktop printing ranks candidates as an industrial machine does, with a measured offset.
   (iii) The live campaign stopped most candidates early and found [alloy]. (iv) A twin calibrated on the
   campaigns shows when this beats screening (wrong screen) and when it ties (right screen).
7. **Why it matters beyond Al.** Any multi-step materials workflow with steps of very different cost
   can be run this way, but only if every step is cheap and fast enough to call on demand. Here, that
   meant making powder and printing in-house.

## 3. Positioning and the novelty sentence

What is **not** new, and must not be claimed (checked by the Edison precedent scan of 2026-10-06 on
PR 90's branch, `edison-trajectories/recent-developments-2026-10/05-precedent-novelty.md`):

| Prior work | What it already did | Where this article differs |
|---|---|---|
| Taheri-Mousavi et al., *Adv. Mater.* 2026 (10.1002/adma.202509507) | Composition BO with CALPHAD/ICME, a custom Al alloy, **ultrasonic atomization**, LPBF tuning, tensile | Their optimizer picked compositions; every candidate then went through a fixed sequence. Here the optimizer picks the step, and powder is made for every candidate rather than one. |
| Buathong et al., ICML 2024; Buathong & Frazier 2025 | Cost-aware partial-evaluation BOFN (p-KGFN) | Shown on synthetic networks (Manu-GP) and FreeSolv; here on a physical alloy workflow with real noise and failures |
| Torresi & Friederich, *Digital Discovery* 2026 | Multi-stage BO with an inventory of partly processed samples | Synthetic and retrospective; uniform stage costs in the main tests |
| Alvi et al., *npj Comput. Mater.* 2026 | Cost-aware batch deep-GP BO across unequal-cost queries for alloys | In silico; property sources, not sequential manufacturing steps |
| Hur & Lee, arXiv 2607.04508 (2026) | Proposes a cost-aware measurement agent for metal AM (hardness vs. tensile) | Future tense; no demonstrated campaign. Watch for a published version before submission. |
| APEX (Conn et al. 2025), BIRDSHOT (Paramore 2025), Nelaturu 2024, Talbot 2026 | Closed loops for structural alloys (DED, arc melting, printed NiCoCr) | Fixed step order; purchased or arc-melted feedstock |

**The novelty sentence (qualified, as Edison advised):** "To our knowledge, this is the first
demonstrated application of cost-aware Bayesian optimization of a partially evaluable function network to
an integrated alloy composition–powder production–LPBF–microstructure–mechanical property workflow, in
which the optimizer chose among feasible intermediate and downstream evaluations under measured step
costs." It is only true if Fig. 5a shows candidates stopped at different steps because of the
acquisition, not because of a fixed rule. If the live campaign doesn't get there, say "we propose" and
name only the steps that ran (version B).

**Second novelty, smaller:** the first fixed-setting repeatability study of ultrasonic atomization for an
Al alloy (byu-vcl's October literature check found one replicate study for any alloy, Hinrichs 2021, and none
for Al). Yankin 2025 (AlSi12) looks like a counterexample but varies the settings between runs; its D50 spread
is across settings (checked 2026-11-27). Re-check before submission; this is the claim most likely to be
overtaken.

## 4. Two papers from one campaign: what goes where

Several drafts now draw on the same lab work (this one; the campaign paper, #277; the BOFN methods paper, #121;
two powder-doser papers),
and a journal will check whether this article's results were already published. The #277 session (campaign paper, due Feb 28, 2027) proposed the split below on
2026-11-27 (`al-campaign-paper/outline.md` on `claude/issue-277-20261127-1859`); this outline adopts it
unchanged, and adds the last two rows.

| Result | Campaign paper (Feb 2027) | This article (early 2028) |
|---|---|---|
| Campaign 1 alloys: compositions, powders, prints, properties, corrosion, benchmark map, mineral burden | **Owns** | Cites it; uses its data as prior data for the optimizer |
| Atomization as a method (process window, Block A repeatability, Block B composition spread, failure modes, dosing fidelity) | Reports settings and yields in its SI; no claim | **Owns** |
| The optimizer: per-step costs, partial evaluation, replay/acceleration factor | One paragraph; no acceleration claim | **Owns** |
| CALIBER measurement settings | Uses and cites | **Owns** (unless CALIBER gets its own paper; decision D5) |
| Desktop LPBF, the digital twin | Only if a desktop print is in it | **Owns** |
| Campaign 2 (2027), optimizer-driven, desktop LPBF in the loop | — | **Owns**: the headline alloy for version A |
| Mineral-burden metric | Defines it (B = Σ wᵢ·NIRᵢ, USGS MCS 2026) | Uses the same definition and cites it |
| Dosing accuracy and the doser itself | — | Cites the **powder-doser papers** (drafts for *Digital Discovery* and *Additive Manufacturing* in vertical-cloud-lab/powder-doser); this article reports only what dosing does to charge composition |
| Synthetic benchmarks of the optimizer (`bofn-prelim`/`bofn-paper`: pKGFN, KGFN, screening on the hand-built network) | — | Cites the **BOFN methods paper** (#121, a third draft started on 2026-11-27 on `claude/issue-121-20261127-1900`), which owns them. This article's Fig. 6 comes from the twin fitted to lab records, not from the synthetic network |

Consequence: **this article needs its own materials result**, from a second campaign in 2027. Without it,
the article is a methods-and-platform paper (version B), which is a harder sell in *Advanced Materials*
than in *Digital Discovery* or *npj Computational Materials*.

## 5. Versions A and B

| | Version A: the loop finds an alloy | Version B: the loop, characterized |
|---|---|---|
| Headline | Campaign 2, run by the cost-aware optimizer with desktop LPBF in the loop, finds [alloy], better than campaign 1's best (or than AlSi10Mg printed and tested the same way) at lower mineral burden than Scalmalloy, at [k]-fold lower cost than screen-then-test replayed in the twin | The atomizer is repeatable and composition-faithful; step costs span four orders of magnitude; the optimizer, replayed on both campaigns' real data and on the calibrated twin, would have reached campaign 1's best at [k]-fold lower cost |
| Needs | Desktop LPBF printing Al by ~May 2027; the optimizer running live with partial evaluation; ≥ 1 finalist with ≥ 3 valid tensile specimens and an outside composition check; campaign 2 done by ~Oct 2027 | Blocks A and B done; step-cost logs; campaign 1 data; the twin calibrated |
| Fits | *Advanced Materials* research article | *Advanced Materials* only if the collection is about autonomous labs or methods; otherwise *Digital Discovery*, *npj Comput. Mater.*, *Adv. Intell. Syst.* |
| Decide | Gate G-A3 (Sep 30, 2027; see [`timeline.md`](timeline.md)) | |

## 6. Sections, the claim each makes, and length

*Advanced Materials* research articles have no hard word limit (see [`journal-format.md`](journal-format.md));
the budget below aims at ~6,500 words of main text with 6 figures and 2 tables, the middle of the range for
the journal's recent closed-loop and AM-alloy papers.

| § | Title | Claim | Words | Main data |
|---|---|---|---|---|
| Abstract | | The loop, the alloy, the cost ratio, the condition | ≤ 200 | all |
| 1 | Introduction | Two bottlenecks (powder; fixed-order spending); BOFN fits but is untested on physical workflows | 900 | literature (drafted) |
| 2.1 | The loop and what each step costs | Step costs span ~4 orders of magnitude; composition to measured cube in [d] days at [n] candidates/week | 500 | step-time logs (L1–L3) |
| 2.2 | Making powder for any composition | 250 g charges give LPBF-grade powder; the spread at fixed settings meets the pre-set bar; failures were engineered out | 1000 | Blocks A, B; all runs (A1–A6) |
| 2.3 | Composition fidelity | Dosed charges land within [x] wt%; Si in powder follows the charge; Mg loss [y]; EDS vs ICP [z] | 600 | dosing logs, Block B, ICP (C1–C4) |
| 2.4 | Printing in-house | Desktop LPBF ranks candidates like an industrial machine, with offset [d] | 700 | desktop + Utah builds on shared powders (P1–P5) |
| 2.5 | The optimizer chooses the step | Campaign 2: [p]% stopped before printing; finds [alloy]; outside checks agree | 1100 | campaign 2 (B1–B6) |
| 2.6 | When it pays off | Twin reproduces campaign spend within [x]%; [k]× with a wrong screen, ~1× with a right one | 700 | twin, clocked benchmark (T1–T4) |
| 2.7 | Limits | Gain depends on cost ratios and screen error; desktop coupons rank, don't qualify | 300 | T3, P4 |
| 3 | Conclusion | | 200 | |
| 4 | Experimental Section | Methods for every step, each citing its SOP and script | 1500 | SOPs |

## 7. Title options

- *Closing the loop from custom powder to printed part: cost-aware discovery of supply-secure printable aluminum alloys* (current)
- *Spending experiments where they count: an optimizer that chooses the step, from powder to printed aluminum alloy*
- Version A, alloy-first: *[Alloy]: a scandium-free printable aluminum alloy found by a laboratory that makes its own powder and chooses its own experiments*

"Supply-secure" in the title has to survive decision D9. Under mass-weighted import reliance (MCS 2025), Mn-rich
alloys score worse than Scalmalloy, so if the finalist is Al–Mn–Cr–Zr, say "scandium-free" instead.

## 8. What could break the argument

| Risk | Effect | Mitigation |
|---|---|---|
| Desktop LPBF not printing Al by mid-2027 | Loop cycle time is set by Utah trips; claim (ii) and the cost story weaken | Campaign 2 uses Utah's MIDI with reduced-build coupons; claim (ii) becomes "desktop for tracks only" |
| Optimizer never stops candidates early (screen happens to be right) | The novelty sentence fails | Pre-register the condition; report it as the "right screen" arm of Fig. 6, and fall back to version B |
| Atomizer repeatability fails the bar | Claim (i) becomes "here is the spread", weaker | The bar was set in advance; report the spread and what drives it (plate wear, landing point) |
| EDS can't resolve Si to better than 0.2–0.5 wt% | Composition fidelity can't be shown for Si alloys | ICP-OES on sealed samples; design space without Si (as raised at the Nov 12 kickoff) |
| Campaign paper scoops the alloy | Version A needs a different/better alloy | Campaign 2 starts from campaign 1's data and aims past its best |
| A competitor publishes a demonstrated cost-aware network campaign on metals AM first | Novelty sentence | Re-run the precedent scan in Oct 2027 and Jan 2028 |
| Collection deadline is actually Feb 2027 | This plan collapses into the campaign paper | Decision D1 |
| The burden metric ranks the focus family badly: with B = Σ wᵢ·NIRᵢ (MCS 2025), Al–Mn–Cr–Zr seeds score above Scalmalloy, because Mn is 100 % imported | "Supply-secure" in the title can't rest on Al–Mn–Cr–Zr | Decide D9 before the screen ranks anything; Zr-refined Al–Mg/Al–Fe alloys score well under any import-weighted metric |
