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
   unit cost. So far it has been tested only on synthetic and retrospective problems, and cost-aware BO
   has run live only within a single instrument (nanoindentation, Chawla et al. 2026).
5. **What we did.** Built the whole loop in one lab: dosed charges, ultrasonic atomization, powder
   characterization, a desktop LPBF system, microstructure and mechanical tests, and an optimizer over
   all of them with measured step costs. Then ran a campaign in which the optimizer chose the step.
6. **What we show.** (i) The atomizer is a dependable step: repeatable, composition follows the charge.
   (ii) Desktop printing ranks candidates as an industrial machine does, with a measured offset.
   (iii) The live campaign stopped most candidates early and found [alloy], which lies beyond the
   strength–burden front of commercial scandium-free alloys (EOS Al5X1, Höganäs Al-HS1) printed and tested
   here the same way, while those alloys came within [x] % of their data sheets. (iv) A twin calibrated on the
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
| Commercial Sc-free LPBF alloys: EOS Al5X1 (Al–Mg–Zr–Mn), Höganäs Al-HS1 (Al–Mn–Cr–Zr), Aheadd CP1 (Al–Fe–Zr) | Sc-free alloys sold as powder, 300–385 MPa aged on their data sheets; Al–Mn–Cr–Zr and Al–Mg–Zr in the peer-reviewed literature too (Croteau 2018; Mehta et al., *Mater. Des.* 2024) | Not a precedent for the method, but the bar for the alloy: campaign 2 is measured against Al5X1 and Al-HS1 printed here (§5) |
| Buathong et al., ICML 2024; Buathong & Frazier 2025 | Cost-aware partial-evaluation BOFN (p-KGFN) | Shown on synthetic networks (Manu-GP) and FreeSolv; here on a physical alloy workflow with real noise and failures |
| Torresi & Friederich, *Digital Discovery* 2026 | Multi-stage BO with an inventory of partly processed samples | Synthetic and retrospective; uniform stage costs in the main tests |
| Alvi et al., *npj Comput. Mater.* 2026 | Cost-aware batch deep-GP BO across unequal-cost queries for alloys | In silico; property sources, not sequential manufacturing steps |
| Fadhel et al., arXiv 2601.17587 (2026) | Adaptive experimental design finds feasible DED settings for GRCop-42 in batches | One step (process parameters), one alloy; no powder making or cost-aware choice among steps |
| Chawla et al., *Digital Discovery* 2026 (10.1039/d5dd00518c) | Cost-aware BO run live on a real nanoindentation workflow, with instrument constraints | Experimental, but within one characterization instrument; no manufacturing steps. Found by a search on 2026-11-27, after the October Edison scan |
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
| The industry Sc-free baselines (EOS Al5X1, Höganäs Al-HS1): sourcing, first in-house prints and tests, parity with their data sheets | **Owns** the first measurement (#277 run of 2026-11-27, with sourcing and schedule) | Cites it; reprints the baselines in campaign 2's builds and on the desktop LPBF, and reports those |
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

## 5. Versions A and B, and what campaign 2 is measured against

| | Version A: the loop finds an alloy | Version B: the loop, characterized |
|---|---|---|
| Headline | Campaign 2, run by the cost-aware optimizer with desktop LPBF in the loop, finds a Sc-free alloy [name] that lies beyond the strength–burden front of the commercial Sc-free alloys EOS Al5X1 and Höganäs Al-HS1, bought as powder and printed, aged and tested in the same builds, with the grain-refinement mechanism shown by EBSD. The twin, fitted on campaign 1 and checked against its own prediction of campaign 2, estimates the saving over full-chain network BO and over the best-form screen | The atomizer is repeatable and composition-faithful; step costs span four orders of magnitude; the optimizer, replayed on both campaigns' real data and on the calibrated twin, would have reached campaign 1's best at [k]-fold lower cost |
| Needs | Desktop LPBF printing Al by ~May 2027; the optimizer running live with partial evaluation; the baselines printed and tested in-house; ≥ 1 finalist with ≥ 3 (better 5) valid tensile specimens and an outside composition check; campaign 2 done by ~Oct 2027 | Blocks A and B done; step-cost logs; campaign 1 data; the twin calibrated |
| Fits | *Advanced Materials* research article, if the alloy expands the in-house front | Probably not *Advanced Materials*, because it has no new alloy; *npj Comput. Mater.*, *Digital Discovery* or *Additive Manufacturing* |
| Decide | Gate G-A3 (Sep 30, 2027; see [`timeline.md`](timeline.md)) | |

### What campaign 2 is measured against

**Baselines: an industry front, measured in-house (decided by Sterling on 2026-11-27).** Scandium-free LPBF
aluminum stronger than AlSi10Mg is already sold, so a new alloy has to be judged against it, measured the same way.
Two of the commercial alloys are the counterparts of the seed families:

| | EOS Aluminium Al5X1 | Höganäs forAM Al-HS1 |
|---|---|---|
| Family; composition (wt %) | Al–Mg–Zr–Mn: Mg 2.5–4.2, Zr 0.6–1.8, Mn 0.1–1.0 (AA 5A05.50) | Al–Mn–Cr–Zr: Mn 4.8, Cr 0.8, Zr 0.8 (typical) |
| Seed family it stands for | Al–Mg–Zr (O1; Croteau et al. 2018) | Al–Mn–Cr–Zr, the FLAIME focus family (S1, O3) |
| Data sheet, horizontal: as built → directly aged | 260 → 385 MPa YS, 23 → 14.5 % EL (400 °C, 6 h; EOS M 290, 40 µm) | 220 → 370 MPa YS, 25 → 12 % EL (375 °C, 4 h; bars machined from printed cylinders) |
| B_NIR (MCS 2026, nominal composition) | 3.1–4.2 wt % | 5.4–5.6 wt % |

- **Same machine, same build, same test.** Both are bought as gas-atomized powder and printed with the candidates.
  They use the same laser parameters (or the same short sweep, if they aren't dense with them), the same specimens and
  test, ICP-OES on each lot, and the same aging rule. If a candidate lies beyond them, the improvement can't come from a
  different machine or test.
- **Parity.** Their in-house values against their data sheets (pre-set band, ±10 % on yield strength and UTS) show
  whether the lab measures on a par with industry. That is the check AlSi10Mg failed in April (issue 1 in §9).
- **The target T is expanding their front.** Against each in-house baseline, a candidate has to have lower B or be
  stronger, and it has to be stronger than in-house AlSi10Mg. The pre-registration gives the statistical rule.
- **What the data sheets already say.** Under B_NIR, Al5X1 is both stronger and lower in burden than Al-HS1. So
  Al5X1 alone sets the front, and Al-HS1 matters as the same-family comparator for Al–Mn–Cr–Zr candidates, or on
  another axis (its data sheet advertises strength at temperature). "At least one" means Al5X1 if the claim is about
  the front, and Al-HS1 if campaign 2 stays in the Mn–Cr–Zr family (README D0a; sourcing is in #277's run).
- **New, not only better than what was measured here.** A low-burden alloy can lie beyond the in-house front and
  still be a published one: Aheadd CP1's data-sheet point does. The pre-registration therefore also reports whether
  the finalist beats the published values of Sc-free alloys, which decides whether it can be called new.
- **AlSi10Mg stays**, as the route control and the floor, reprinted in the same builds with recorded parameters,
  machined parity bars and an extensometer. Scalmalloy stays as data-sheet context, unless the campaign paper prints
  it.

## 6. Sections, the claim each makes, and length

*Advanced Materials* research articles are "typically 3000–8000 words (in their entirety) including 3–8 display
items", with no hard limit ([`journal-format.md`](journal-format.md)). The budget below aims at ~5,000 words of main
text plus ~1,800 in the Experimental Section, with 6 figures and 2 tables (8 display items, the upper end). Recent
comparables run 3.6–6.6k words of main text, median ~4.5k.

| § | Title | Claim | Words | Main data |
|---|---|---|---|---|
| Abstract | | The loop, the alloy, the cost ratio, the condition | ≤ 200 | all |
| 1 | Introduction | Two bottlenecks (powder; fixed-order spending); BOFN fits but is untested on physical workflows | 750 | literature (drafted) |
| 2.1 | The loop and what each step costs | Step costs span ~4 orders of magnitude; composition to measured cube in [d] days at [n] candidates/week | 400 | step-time logs (L1–L3) |
| 2.2 | Making powder for any composition | 250 g charges give LPBF-grade powder; the spread at fixed settings meets the pre-set bar; failures were engineered out | 800 | Blocks A, B; all runs (A1–A6) |
| 2.3 | Composition fidelity | Dosed charges land within [x] wt%; Si in powder follows the charge; Mg loss [y]; EDS vs ICP [z] | 450 | dosing logs, Block B, ICP (C1–C4) |
| 2.4 | Printing in-house | Desktop LPBF ranks candidates like an industrial machine, with offset [d] | 550 | desktop + Utah builds on shared powders (P1–P5) |
| 2.5 | The optimizer chooses the step | Campaign 2: [p]% stopped before printing; finds [alloy] beyond the in-house front of Al5X1 and Al-HS1, which match their data sheets to [x] %; outside checks agree | 900 | campaign 2 (B1–B7, V1–V2) |
| 2.6 | When it pays off | Twin reproduces campaign spend within [x]%; [k]× with a wrong screen, ~1× with a right one | 550 | twin, clocked benchmark (T1–T4) |
| 2.7 | Limits | Gain depends on cost ratios and screen error; desktop coupons rank, don't qualify | 250 | T3, P4 |
| 3 | Conclusion | | 150 | |
| 4 | Experimental Section | Methods for every step, each citing its SOP and script | 1800 | SOPs |

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
| The burden metric ranks the focus family badly: with B = Σ wᵢ·NIRᵢ (MCS 2026), Al–Mn–Cr–Zr seeds score above Scalmalloy, because Mn is 100 % imported | "Supply-secure" in the title can't rest on Al–Mn–Cr–Zr | Decide D9 before the screen ranks anything; Zr-refined Al–Mg/Al–Fe alloys score well under any import-weighted metric |
| The baselines print below their data sheets here, as AlSi10Mg did | "On a par with industry" fails; the one-to-one comparison still holds | Pre-set parity band; find the cause (parameters, surface, extensometry, powder O) before campaign 2; if it stays, report the offset |
| The baseline powders take months to arrive, or can only be bought through a machine vendor | Campaign 2 starts without its comparison | Sourcing and lead times in #277's run; order with campaign 1's purchases; buy one if not both (D0a) |
| Campaign 2 doesn't beat Al5X1 on strength or on burden | Version A has no alloy | Pre-registered: report the margin either way; a front expansion on burden alone (lower B at Al5X1's strength) also counts |

## 9. Issues raised in a mock review (2026-11-27), and what changed

An independent read of the draft manuscript, figure plan and pre-registration (one model playing an *Advanced
Materials* editor and referee, without this outline) raised the points below. They are treated as issues to fix,
not as a verdict on the paper. Two of them come from the lab's own data.

| Issue | Change made (or still needed) |
|---|---|
| **AlSi10Mg printed here is below its data sheets.** The April Utah bars gave 228 ± 13 MPa yield (as built, horizontal, as-printed surface, n = 4), below every as-built data-sheet row (233–300 MPa, machined). A target of "above as-built AlSi10Mg" is therefore low, and it says nothing about whether the lab's numbers compare with industry's | Campaign 2 is measured against **industry Sc-free alloys printed and tested here** (Al5X1, Al-HS1; §5), with a **pre-set parity check** against their data sheets. AlSi10Mg stays as the route control and floor: reprinted in the same builds, with recorded laser parameters, machined parity bars and an extensometer. The likely causes of the gap get tested, not assumed: unrecorded laser parameters, as-printed surfaces, small flat coupons against round machined bars, and a strain channel that read elastic slopes of 29–49 GPa on four of the five bars, with crosshead speeds faster than ASTM E8 allows while measuring yield (PR #288). Data sheets are context in Fig. 5c, not the comparison |
| **The burden measure lets any low-Mg alloy win.** B = Σ wᵢ·NIRᵢ counts Mg like Sc. Scalmalloy's B is mostly its 4.7 wt % Mg, so an alloy with less Mg beats it without any design effort; Al5X1 does (3.1–4.2 against 4.7–6.0 wt %) | The claim is no longer "lower B than Scalmalloy": it is expanding the Sc-free front, with Sc excluded outright. B is still frozen with the campaign paper before its screen ranks anything (D9), reported by element, and the SI redraws the front under the alternatives (cost of the critical additions, Sc content). Still open: whether a metric that weighs Sc's small, export-controlled market more heavily should replace B_NIR in both papers |
| **The figures describe instruments, and the alloy gets half a figure** | Fig. 5c now carries the comparison (the finalist against the in-house front, with parity lines to the data sheets) and Fig. 5d the finalist. Still to decide for version A: whether the finalist needs a figure of its own (aging curves, EBSD) |
| **The evidence that choosing the step helps is simulated** | Campaign 2's decision log, labelled stops and stop audit (Fig. 5a–b); the twin fitted on campaign 1 must predict campaign 2 (next two rows) |
| The twin comparison is built in: κ = 1 is a screen ignoring a feature the CALPHAD node computes; the twin is validated in sample | Baseline is now the **best-form screen** (all CALPHAD outputs, trained on campaign 1, tuned cut-off); the **headline comparison is pKGFN vs full-chain network BO**; the twin is **fitted on campaign 1 and must predict campaign 2 out of sample**; truths drawn from the fitted posterior; measured κ primary; ±50 % cost robustness (pre-registration) |
| "Stopped p % before printing" doesn't show the stops were right; failures will masquerade as decisions | Stops labelled failure / constraint / acquisition; a **random 25 % of acquisition stops pushed one step further** (false-stop rate); hardware failures modelled as a per-step process; design space cut to 3–5 elements (Fig. 5a, B7) |
| Composition fidelity is tested on Si, with a method (5 kV EDS) that can't see Mn, Cr, Fe, Ni, Cu, Zn, Ce or Er | **ICP-OES on every campaign powder by sieve fraction**, a fidelity check on Zr, Sc/Er and Mn, sectioned-particle maps before any "within a particle" claim (§2.3, C5) |
| Overclaims in the introduction and abstract | Fixed: "no other process can make", "a fixed order" (now fixed stage-gates), the universal negative about tested methods (now narrowed, with multi-information-source, freeze-thaw and Hyperband cited), the twin claim in the abstract, "any composition", Scheil wording, the best-so-far tautology |
| Missing controls and baselines | Added to the plan: route control (in-house AlSi10Mg on both machines, P6), the industry Sc-free baselines printed and tested in-house (B6, replacing the in-house "positive control" alloy of the first revision), Taheri-Mousavi's alloy on Fig. 5c, aging curves per family, ≥ 8 alloys and matched preheat for the printer transfer, powder mass per node in Table 1. **Still to decide:** whether laser remelting of cast or arc-melted buttons, a cheap hot-cracking screen that needs no powder, should be a node (or argued against), and how this route compares with nanoparticle-decorated commercial powder (Martin 2017) |
