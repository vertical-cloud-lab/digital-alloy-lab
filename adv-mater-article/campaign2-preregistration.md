# Campaign 2 pre-registration (draft)

*Draft of 2026-11-27, for the 2027 campaign that version A of the article rests on. Revised the same day so that
campaign 2 is measured against **industry scandium-free alloys printed and tested in-house** (Sterling, on
[#120](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/120)). The campaign paper
([#277](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/277)) adds the same baselines and owns their
sourcing and first measurement; the two pre-registrations must use the same definitions (marked **with #277**
below). Bracketed items wait on campaign 1 and on decisions D3, D9 and D10 in the [README](README.md). The final
version must be committed (hash and date recorded here) **before the first campaign 2 decision**, and every later
change logged under "Deviations". The synthetic benchmarks showed why: without a fixed target, baseline and
stopping rule, the speed-up depends on which target and seed one picks (PR #293, PR #297).*

## Questions

- **Q1 (live).** Does the cost-aware network optimizer, run on the real lab, stop candidates at different steps
  because of the acquisition, and does what it finds lie beyond the front of the industry baselines measured the
  same way?
- **Q2 (twin).** Across repeated simulated campaigns on a twin fitted to the lab's records, does it reach the
  target at lower spend than screen-then-test, and is the gain larger when the CALPHAD screen misses an effect
  (κ = 1) than when it doesn't (κ = 0)?

The live campaign answers Q1 once; Q2 needs repetition, so it is answered on the twin. Neither is claimed from the
other.

## The baselines: an industry front, measured in-house

Of the scandium-free alloys sold as powder for LPBF, two belong to the families campaign 2 works in, and both are
stronger than AlSi10Mg after a single direct age. Bought, printed, aged and tested here exactly as the candidates
are, they give a one-to-one comparison: if a candidate lies beyond them, the improvement is not an artefact of a
different machine, specimen or test. Their in-house values against their data sheets show whether this lab
measures on a par with industry.

| Baseline | Role | Data sheet: condition, orientation | YS / UTS (MPa), EL (%) | B_NIR (wt %)\* |
|---|---|---|---|---|
| **EOS Aluminium Al5X1**, Al–Mg–Zr–Mn (Mg 2.5–4.2, Zr 0.6–1.8, Mn 0.1–1.0 wt %; Aluminum Association 5A05.50); gas-atomized, 20–63 µm (EOS material data sheet) | Commercial counterpart of the Al–Mg–Zr seeds (O1; Croteau et al. 2018). On their data sheets it is the stronger of the two and has the lower burden | direct aged 400 °C, 6 h; horizontal; EOS M 290, 40 µm, ASTM E8 | 385 / 415, 14.5 (as built: 260 / 310, 23) | 3.1–4.2 |
| **Höganäs forAM Al-HS1**, Al–4.8Mn–0.8Cr–0.8Zr (typical); gas-atomized, 20–63 µm | Commercial counterpart of the Al–Mn–Cr–Zr focus family (seeds S1, O3) | direct aged 375 °C, 4 h, in air; X/Y; bars machined from printed cylinders | 370 / 440, 12 (as built: 220 / 285, 25) | 5.4–5.6 |
| AlSi10Mg: commercial lot, plus the in-house atomized lot as route control | Lower anchor; the campaign paper's comparator | as built, horizontal (EOS M 290, 30 µm) | 270 / 461, 10.2 | 5.2–10.3 |
| Scalmalloy | The burden reference. The campaign paper prints it in-house too (bought, or atomized as D2) and counts it in the in-house front; under the burden condition of T it never binds (below) | direct aged 325 °C, 4 h | 465–500 / 505–530, 11.5–15.8 | 4.7–6.0 |

\* B_NIR = Σ wᵢ·NIRᵢ/100 from the nominal composition (Al5X1 at the midpoints of its ranges), with the campaign
paper's inputs (USGS *Mineral Commodity Summaries 2026*; `tools/mineral_burden_check.py`). A range, because USGS gives
some import reliances only as bounds. Campaign values use each lot's ICP-OES composition; Al5X1's composition ranges
alone span B_NIR 2.0–5.7 wt %, so its lot decides where it sits. Sources: EOS process and
material data sheets for Al5X1, Höganäs data sheet 3312HOG-3, PR #285's AlSi10Mg and Scalmalloy set; all values
checked against the vendors' documents on 2026-11-27.

- **Al5X1 first; Al-HS1 if the budget allows** (the campaign paper's recommendation, `al-campaign-paper/baselines.md`
  on `claude/issue-277-20261127-2117`; decision D0a). On their data sheets, Al5X1 has the higher aged yield strength
  *and* the lower B_NIR (below Scalmalloy's at every allowed import reliance), so under B_NIR it alone sets the
  scandium-free front, and Al-HS1 sits behind it. Al-HS1 still earns its place as the same-family comparator for
  Al–Mn–Cr–Zr candidates, and on another axis: its data sheet advertises strength at temperature. A third purchase,
  Aheadd CP1 (Al–Fe–Zr), would anchor the low-burden end, where the only Sc-free points are a data sheet and a paper.
- **Measured the same way as the candidates** (the campaign paper's protocol, so both papers measure them alike):
  - the same machine: the Utah Aconity MIDI for tensile bars, and in campaign 2 also the desktop LPBF for density
    and hardness. One powder per build, so "the same session" means consecutive builds on the same machine within
    one visit; every campaign 2 session with tensile bars includes at least one baseline build;
  - the same layer thickness, plate temperature, scan strategy, gas flow and powder handling (sieve, dry, humidity
    log);
  - laser power and speed by the same rule, not the same numbers: every alloy, candidate or baseline, gets a 4 × 4
    power–speed grid of density cubes, and its bars are printed at its densest grid point, ties going to the lower
    energy density. One parameter set would favour whichever alloy it was tuned for. (**With #277:** its
    `baselines.md` centres each alloy's grid on that alloy's published energy density, while its pre-registration
    says "the same grid"; both papers should settle on one);
  - the same specimens and test: flat sub-size ASTM E8 bars (6 × 6 mm section), built horizontal, with one surface
    for all alloys (as printed in the campaign paper's `baselines.md`; its pre-registration still lists the surface as
    a decision); clip-on extensometer or DIC over a 25 mm gauge; ASTM E8 strain rates;
  - ICP-OES on every lot, like every candidate powder;
  - heat treatment as each supplier specifies (Al5X1 400 °C 6 h with gas quench; Al-HS1 375 °C 4 h in air); the
    baselines also join their family's hardness aging curve, so the candidates' aging rule is tested on them.
- **Who measures them first.** The campaign paper buys the powders (quotes requested in the week of Nov 30, a PO
  by Dec 11) and prints them in Utah sessions P2–P4. If the PO goes out by Dec 4 and the drum ships from U.S.
  stock, aged Al5X1 tensile results exist by about Jan 22–29, 2027; with a PO on Dec 11 and the drum shipped from
  Europe, by about Feb 8–12. Campaign 2
  reprints the baselines in its own builds, and on the desktop LPBF.

## Fixed before the first decision

| Item | Setting |
|---|---|
| Design space | **3–5 elements** (more spreads ~20–35 runs too thin for the surrogates), [bounds frozen at D10; Si in or out]; Sc excluded |
| Objectives | **Aged yield strength (maximize) and mineral burden B (minimize)**. A print counts only if ≥ 99 % dense and crack-free, and a candidate only if its elongation is no lower than in-house AlSi10Mg's (the campaign paper's floor). **Decide:** whether elongation becomes a third objective |
| Burden metric | B as frozen for the campaign paper before its screen ranks anything (**with #277**, decision D9). That paper's run recommends **B_NIR = Σ wᵢ·NIRᵢ/100** with USGS MCS 2026 inputs and Fe counted as zero. Alloys are compared under the same import reliances (paired), on measured compositions; the front is drawn at the midpoint reliances and the claim tested at the bounds; B_mass and the cost of the critical additions are reported in the SI. B is reported by element. **Known issue to fix:** B_NIR counts Mg like Sc, so Scalmalloy's B is mostly its 4.7 wt % Mg, and a low-Mg alloy beats it without any design effort unless it carries a lot of Mn, Cr or Si instead. Al5X1 does; S1 and O3, rich in Mn, do not. So the claim is not "lower B than Scalmalloy": it is expanding the scandium-free front, with Sc excluded outright. Within that front the Mg-against-Mn weighting still decides where Al-HS1 sits, so the SI redraws the front under each alternative |
| Baselines | As above: Al5X1, and Al-HS1 if bought, printed, aged and tested here the same way as the candidates, in the same sessions; AlSi10Mg in the same sessions as the floor and route control; Scalmalloy as the burden reference. The in-house front is Al5X1, Al-HS1 and Scalmalloy, each in its supplier's condition, as in the campaign paper |
| Parity check | The campaign paper's rule (its §4b, and H5): each in-house baseline's mean yield strength, in its supplier's condition and the horizontal orientation, is at least **90 %** of the data-sheet typical value, reported as a ratio with its 95 % CI (**decide the threshold, with #277**). The 10 % allows for as-printed sub-size bars against the suppliers' machined round bars. UTS is reported against the same row, and elongation against as-printed data-sheet rows where they exist. A baseline below 90 % is investigated before campaign 2's first decision: a set of machined bars separates surface from process, and parameters, extensometry and powder O are checked. If the gap stays, the paper reports the offset and drops "on a par with industry". The same-session comparison stands either way. The baselines also show whether AlSi10Mg's April shortfall is AlSi10Mg's or the process's: their strength comes mostly from the direct age, which depends less on how they were printed. As in the campaign paper's H6, if Al5X1 printed here does not dominate Al-HS1, Al-HS1 joins the front |
| Target T | **The campaign paper's definition of "expands the front"** (its pre-registration §2-§4 at `479f983`), applied to campaign 2. A Sc-free candidate condition meets T if all of these hold: (1) it is stronger than in-house AlSi10Mg, at no lower elongation, against both of AlSi10Mg's conditions (as built and stress-relieved); (2) its B is below Scalmalloy's at every allowed import reliance (paired, measured compositions); (3) no in-house baseline dominates it: every baseline whose B is not robustly above the candidate's is weaker by the strength rule below; (4) secondary, on reported values: no published Sc-free alloy dominates it (next row); (5) it is crack-free and ≥ 99 % dense, with n ≥ 3 valid specimens (5 recommended). Condition (2) is kept so that both papers make the same claim, although under B_NIR it is mostly a statement about Mg and Mn content (outline §9, issue 2); because of it, Scalmalloy never binds in (3), and the front that matters is Al5X1's and Al-HS1's. **Size of the step:** the hypervolume the candidate adds to the in-house front inside the region of interest (yield above in-house AlSi10Mg, B below Scalmalloy's, at the midpoint reliances), as in the campaign paper |
| "Stronger" | **With #277.** Its draft rule needs the means to differ by more than both 95 % CI half-widths, and it plans 3 bars per condition (8 per baseline with 2 spares). At the April AlSi10Mg bars' scatter (CV 5.7 %), applied at Al5X1's ~385 MPa, beating Al5X1 under that rule takes ≈ 110 MPa with n = 3 each and ≈ 55 MPa with n = 5. A Welch test (the 95 % CI of the difference excludes zero) takes ≈ 50 MPa with n = 3 and ≈ 32 MPa with n = 5. **Decide:** the rule and n. Recommended: Welch, n = 5 for baselines and finalists |
| Beyond published alloys | Condition (4) of T, a secondary check as in the campaign paper: whether the candidate is also non-dominated by the published values of Sc-free alloys (the campaign paper's comparator set, `literature-alloys.csv` at its freeze commit). Those were measured on other machines and specimens, so the test is stated as against reported values. It decides whether the alloy can be called new, rather than better than what was measured here. It is the higher bar: on reported values the Sc-free front already runs through Al–1.87Fe–1.02Mg–1.03Zr (376 MPa aged, B_NIR ≈ 1.0) and EOS Al2139 T4 (460 MPa, B_NIR ≈ 3.9), on either side of Al5X1 (the campaign paper's `baselines.md`) |
| Heat treatment | An aging curve per alloy family (Zr-only alloys peak at higher aging temperatures), not one pre-chosen treatment for all; the baselines also at their suppliers' schedules |
| Nodes | CALPHAD → charge → atomize → powder characterization → print (desktop) → density/section/hardness → tensile (finalists) |
| Node costs | median cost per result from campaign 1's step log (Table 1), frozen at [date] |
| Acquisition | **Decision M7, open (Sterling): option A, pKGFN, or option B, BOFN with powder reuse** (next section; this draft doesn't pick). Either way, on a scalar target: the candidate's yield-strength margin over the in-house front at its burden (positive means it expands the front); B below Scalmalloy's is a hard constraint on the design space, since B follows from the composition, as in the campaign paper's optimizer; a node may be queried only if its parents have outputs; [batch size, how pending results are fantasized] |
| Failed vs abandoned steps | [#274 resolution: model failure at the failing step] |
| Prior data | campaign 1 (all runs, prints and tests, including the baselines), [plus seeds: six compositions, #275] |
| Budget | [person-hours and $; e.g. 12 weeks, ≤ 35 atomizer runs] |
| Stopping rule | budget exhausted, or T met and confirmed by the specimens above and an outside composition check |
| Decision log | every decision records: candidate, node, acquisition value, cost, runner-up, model version; committed weekly |
| Stop labels | Every stop is labelled **failure** (the step gave no usable result), **constraint** (a hard rule), or **acquisition** (lower expected gain per cost than another candidate's step). Only acquisition stops test the method |
| Stop audit | A random **25 %** of acquisition stops is pushed one step further; the share that would have been worth continuing is the false-stop rate. Departures from a pre-registered expert stage-gate are logged with what they returned. Under M7 option B the acquisition makes no stops after CALPHAD or atomization, so the audit would apply to its reprint-or-new choices [to define if B is chosen] |
| Failures in the model | Hardware failures (plate, nozzle, cup) are modelled as a per-step failure process, not as a property of the composition (#274) |

## The acquisition function (decision M7): two options

Sterling decides between these before the pre-registration is frozen (by June 2027; results-needed B1). Both are
written out here with the evidence for and against each, and neither is the default. Whichever is chosen, the
other runs in the twin analysis as a secondary arm.

The evidence comes from three synthetic benchmarks, none calibrated to the lab:

- **The BOFN paper set** (issue #121; `benchmarks/bofn-paper/paper-stats/` at `18f5265`, reported in the article's SI
  S14). It has eight policies on the same 20 seeds at κ = 1 and 16 at κ = 0.5 and 0, with a $100k budget, no noise
  and assumed costs. Intervals below are its 95 % matched-seed bootstrap intervals, in points of the optimum (pp).
  Numbers are copied from its `SUMMARY.md`; the manuscript reads them from `numbers.tex`.
- **bofn-clocked** (PR #297, open). It adds clock time, capacity, noise and failed powders, builds and bars, on 8–10
  seeds.
- **byu-vcl's twin, rounds 3–5** (byu-vcl PRs 394, 400 and 405, as summarized in issue #121's README; not readable from
  this repo).

### Option A: pKGFN, the partial-evaluation knowledge gradient per unit cost

Each decision buys one step for one candidate whose parents already have outputs. That step can be a CALPHAD
calculation, an atomization, a print or a tensile test. So a candidate can stop after any step. This is what the
manuscript's novelty sentence, Fig. 5a (every candidate's stops, labelled) and the stop audit (B7) were written for.

| For | Against |
|---|---|
| With a wrong screen (κ = 1) it needed 3.8× less spend than screen-then-test to reach that policy's $100k result (95 % CI 1.9–6.3). | With a right screen (κ = 0) it had the lowest mean of the model-based policies at $100k: 59 % [48, 70], against screen-then-test's 85 % [83, 88] and BOFN with powder reuse's 77 % [63, 89]. It atomizes only alloys it has simulated, and the κ = 0 optimum is a lean, nucleant-free alloy that the seed compositions don't reach. |
| It gave the only resolved early lead of partial over full-chain evaluation: at $25k with κ = 1 it was 16.5 pp ahead of KGFN, its full-chain counterpart [6.1, 28.3]. | That lead was gone by $100k (−2.4 pp [−9.8, +5.9]). In four reruns with four times the Monte Carlo samples, its $25k result fell from 69 % to 46 % of the optimum, so the lead may depend on those settings. |
| It actually stops candidates part-way. Per run at κ = 1 it ran 1.9 new CALPHAD calculations, made 4.8 powders, printed 36.3 times and tensile-tested 7.0 times. So Fig. 5a would show stops at several steps. | It never did better than expected improvement per dollar. With partial evaluation it trailed BOFN with powder reuse at $100k by 6.1 pp at κ = 1 [2.0, 10.0] and by 19.4 pp at κ = 0.5 [10.0, 29.0]. At κ = 0 it trailed by 17.5 pp, not resolved [−0.6, 34.2]. |
| It makes fewer powders per run (4.8, against 11.8 for option B). That would matter if the atomizer stays the bottleneck: it managed 1.7 runs a week in Oct–Nov 2026 (SI Table "Twin assumptions"). The benchmarks charge dollars only, not atomizer capacity. | Its knowledge gradient is often flat. In bofn-clocked, every KG was flat on 64–71 % of its decisions, so the EI fallback decided. In `bofn-prelim`, the tensile-test KG was exactly zero for 73 % of candidates at κ = 0, so it printed a few powders over and over. In the paper set, the fallback decided only 0.7–1.1 % of decisions. |
| An **any-alloy variant** (`pkgfn_free`) may cure the κ = 0 failure. It may atomize compositions it has never simulated, and it values a new powder by atomizing and printing it as one $4,000 move. On the same 16 seeds at κ = 0 it reached 81 % [70, 90] at $100k, 21.8 pp above pKGFN [8.1, 35.9], and level with screen-then-test (−4.6 pp [−16.2, +5.3]) and with BOFN with powder reuse (+4.3 pp [−7.1, +16.2]). At κ = 0.5 it reached 79 % [67, 88], 12.1 pp above pKGFN [0.1, 22.0]. | The variant hasn't been run at κ = 1. It changes three things at once (the candidate rule, the $4,000 move and lighter Monte Carlo settings), so which one repairs pKGFN isn't known. Its stored runs predate a cost fix, which changes one decision on one seed. In bofn-clocked and the byu-vcl twin, a fixed pKGFN tied full-chain BOFN at best. The MethodsX draft calls its results "results of this implementation at these settings, not of p-KGFN in general". |

### Option B: BOFN with powder reuse, network expected improvement per unit cost

Each decision is one of two moves. It is either a new design through the whole chain (CALPHAD, atomize, print,
tensile test), or a reprint and test of an existing powder lot at new laser settings. It picks whichever has the
larger network expected improvement per dollar.

| For | Against |
|---|---|
| It was the most robust policy across κ. At $100k it reached 90 % [85, 94] at κ = 1, the highest of any policy, and 86 % [81, 91] at κ = 0.5. At κ = 0 it reached 77 % [63, 89]; that and full-chain BOFN's 74 % are the best worst cases of any policy. | With a right screen it still lost to screen-then-test. It didn't reach screen-then-test's $100k result within the budget, and its mean was 8.9 pp lower (difference −8.9 [−23.9, +4.8], not resolved). It finished ahead on 11 of 16 seeds but far behind on the rest. |
| With a wrong screen it needed 3.8× less spend than screen-then-test (95 % CI 2.4–5.9). With the screen half right, it finished 8.3 pp ahead of screen-then-test [0.8, 16.4]. | **It never stops a candidate after CALPHAD or after atomization because of the acquisition.** Per run at κ = 1 it simulated 11.8 new compositions and atomized all 11.8, and it printed 30.0 times and tested all 30.0. So Fig. 5a would show no "stopped before printing" candidates. Its step choice is between new powder and a reprint of a lot already made. The novelty sentence would have to narrow to that choice, and the stop audit (B7) would audit reprint-or-new decisions instead [to define if B is chosen]. |
| Its knowledge-gradient alternative was never resolved ahead of it (option A's rows). It is simple and fast (16–27 s per benchmark run, against 225–306 s for pKGFN) and needs no fallback rule. All its stored runs reran action for action. | Its gain over its own full-chain counterpart, BOFN, wasn't resolved at any κ at $100k: +4.2 pp [−2.7, +11.4] at κ = 1, +1.7 [−8.2, +13.6] at κ = 0.5, and +2.4 [−14.1, +18.5] at κ = 0. At $25k with κ = 1 it was +10.9 [−0.8, +22.3]. So the headline comparison against full-chain network BO (H1) has no resolved synthetic support. |
| | It makes more powders per run (11.8 against 4.8), so it loads the atomizer more. Few seeds also misled here: on the first 9 seeds at κ = 0 it averaged 88 % and looked level with screen-then-test; on all 16 it averaged 77 %. |

### What would narrow the choice before June 2027 (evidence still to collect; not a pick)

- Run the any-alloy pKGFN at κ = 1 on the paper set's 20 seeds.
- Isolate which of its three changes repairs it.
- Run both options, with their full-chain counterparts, on the twin fitted to campaign 1 (T1), with the lab's
  measured costs and atomizer capacity. Dollars alone don't capture the atomizer as a bottleneck.
- Decide what the stop audit means under option B, if B is chosen.

## Twin analysis (Q2)

- **Fit out of sample:** the twin is fitted on **campaign 1 only** (T1), and its prediction of campaign 2 (spend and
  days to T, failure counts) is committed here before campaign 2 starts. It passes if campaign 2 lands inside the
  predicted interval (T4). It is refitted on both campaigns only afterwards, for the counterfactuals.
- **Ground truths** are drawn from the fitted posterior over the composition–property landscape, not from one
  hand-built function. The baselines sit at their in-house measured values, so T means the same thing in the twin
  as in the lab.
- **Policies:** the policy chosen at M7, and the other option as a secondary arm. The headline comparison is the
  chosen policy against its own **full-chain counterpart**, which isolates partial evaluation: KGFN for option A,
  full-chain BOFN for option B. Also run: the **best-form screen-then-test**, which uses every CALPHAD output, including
  the primary Al₃(Zr,Sc) fraction, is trained on campaign 1 and has its cut-off k tuned; standard BO;
  multi-fidelity BO; and random. All start from the same prior data and seeds.
- **Conditions:** the **measured** κ (from Fig. 4d's crack-index misses, with its interval) is primary; κ = 0 and κ = 1
  bracket it.
- **Robustness:** decisions and acceleration factors are recomputed with every step cost moved by ±50 %.
- **Model check before campaign 2:** on campaign 1 data, the network must predict yield strength better than a
  GP from composition straight to yield strength (held-out log likelihood).
- **Primary endpoint:** spend to T, the first confirmed expansion of the in-house baseline front. Secondary: days to
  T; best margin over the front at the budget.
- **Analysis:** ≥ 20 seeds per policy and condition; acceleration factor = ratio of median spend to T;
  matched-seed bootstrap 95 % CI, the same level as the synthetic benchmark in SI S14; seeds that never reach T are
  counted as censored, not dropped.
- **H1** is rejected if the median spend to T is not lower than the full-chain counterpart's, and separately than
  the best-form screen's, at the measured κ. **H2** is rejected if the acceleration factor at κ = 1 is not larger than
  at κ = 0.
- **Expected at κ = 0: screen-then-test wins** (decision M8). The paper set and bofn-clocked both found that. In the
  paper set no network policy reached screen-then-test's $100k result when the screen was right. In bofn-clocked,
  screen-then-test reached the first target sooner than BOFN on 10 of 10 seeds. A tie at κ = 0 would be a finding,
  not the expectation.

## What gets reported regardless

The result is reported whatever it is: a tie or a loss to screening, a campaign that doesn't expand the front, and
baselines that miss their data sheets.

## Record

| Version | Commit | Date | Who approved |
|---|---|---|---|
| draft | (this file) | 2026-11-27 | — |
| draft, baselines changed to Al5X1 / Al-HS1 measured in-house | (this file) | 2026-11-27 | — |
| draft, acquisition left open as decision M7 (both options with their evidence); 95 % intervals; screen-then-test expected to win at κ = 0 (M8) | (this file) | 2026-11-27 | — |

## Deviations

None yet.
