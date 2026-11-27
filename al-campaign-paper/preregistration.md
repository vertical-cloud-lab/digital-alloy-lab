# Pre-registration (DRAFT, not frozen)

*A draft for Sterling to edit and commit **before the CALPHAD screen ranks any campaign composition**: by Tue Dec 1,
2026, so the screen can rank on Dec 2-3 and the seeds can be picked at G1 (Fri Dec 4). The commit hash that freezes it goes in SI Section S9 and the Methods (§2.2, §2.12). Every choice below
is a proposal; the open ones are marked **Decide**. After the freeze, any change gets a dated entry in the change
log at the bottom, with its reason, so a reviewer can see what was fixed in advance and what wasn't.*

## 1. The claim being tested

> A scandium-free aluminum alloy, printed by PBF-LB/M from powder atomized in-house, is **stronger than AlSi10Mg**
> printed and tested the same way, at no lower ductility, and carries **less critical-mineral burden than
> Scalmalloy**. To count as a discovery it must also lie **beyond the scandium-free alloys already reported**, on
> strength against burden.

## 2. The comparator and "stronger"

- **Comparator.** AlSi10Mg printed in the *same build* as each finalist, from two powders:
  1. commercial gas-atomized AlSi10Mg;
  2. AlSi10Mg-type powder atomized in-house (runs D1 and D1-r).
  Until then, the April 2026 Utah build (228 ± 13 MPa yield, n = 4) is a provisional comparator and is reported as
  such.
- **Specimens.** Flat ASTM E8/E8M sub-size bars, 6 × 6 mm reduced section, built horizontal, with the same surface
  for all alloys. **Decide:** as-printed or machined.
- **Test.** Room temperature, with a clip-on extensometer or DIC over a 25 mm gauge, and the strain rate within
  ASTM E8/E8M limits while yield is measured. Bars that break outside the gauge are excluded and reported.
- **Conditions.** AlSi10Mg as built and stress-relieved (**Decide:** 300 °C for 2 h or the vendor's 285 °C).
  Each candidate as built and after one direct age chosen before printing. A candidate is compared in each of its
  conditions with AlSi10Mg in *both* of its conditions, and the claim holds only if it passes against both (as-built
  AlSi10Mg is the stronger, stress-relieved the more ductile).
- **Rule.** The candidate is stronger if all of these hold:
  - mean yield(candidate) − mean yield(AlSi10Mg) > hw(candidate) + hw(AlSi10Mg), where hw is the half-width of the
    95 % Student-t confidence interval;
  - mean elongation(candidate) ≥ mean elongation(AlSi10Mg);
  - n ≥ 3 valid bars each.
- **Datasheets.** Vendor datasheet values are context in the paper. They are never the bar.

## 3. Critical-mineral burden

- **Inputs.** [`data/element-criticality.csv`](data/element-criticality.csv) at the freeze commit: USGS *Mineral
  Commodity Summaries 2026* net import reliance and 2025 prices, and the final 2025 U.S. List of Critical Minerals.
  Later USGS editions aren't swapped in.
- **Primary metric, B_NIR.** B_NIR = Σ wᵢ · NIRᵢ / 100 over alloying elements other than Al (wt % of the alloy).
  Fe counts zero. Where USGS gives only a bound, it is carried as an interval.
- **"Less than Scalmalloy".** The candidate's whole B_NIR interval lies below the lower end of Scalmalloy's
  (4.7 wt % on the current inputs).
  - **Decide:** this robust form, or a percentage below Scalmalloy's midpoint (FLAIME's O4 uses ≥ 40 %).
- **Reported alongside, not used for the claim:**
  - B_cost: the cost of the critical additions, with Sc priced as metal and as Al-2Sc master alloy;
  - Sc content;
  - B_NIR with Al counted.
- **Composition used.** The measured composition from the outside laboratory (§5). Until that arrives, the target
  composition, labelled as such.

## 4. "Beyond the scandium-free alloys already reported"

- **Comparator set.** [`data/literature-alloys.csv`](data/literature-alloys.csv) at the freeze commit. Every row is
  checked against its source or marked unverifiable. Unverifiable rows are shown but left out of the test below.
- **Test.** No alloy in that set has both a higher reported yield strength and a lower B_NIR midpoint than the
  candidate (Pareto non-dominated).
- **Caveat.** The literature values are mostly on machined specimens from tuned processes, so the paper states the
  comparison as against reported values, not like-for-like.
- **Decide:** whether the claim also needs non-domination on elongation.

## 5. Composition and independent verification

- **In-house.** EDS on every powder lot, standards-based (DTSA-II), with the acquisition settings recorded.
- **Outside, accredited lab.**
  - Benchmark and finalist powders, and one printed coupon per finalist.
  - Methods: ICP-OES for Mg, Mn, Cr, Zr, Fe, Ti, Er; spark-OES on a printed coupon for Si; inert-gas fusion for O.
  - Samples go under coded IDs, and the results are reported as received.
- **Composition tolerance.** A finalist counts as the alloy named if every intentional addition is within
  ±10 % relative, or ±0.1 wt %, whichever is larger, of its target. **Decide** the tolerance.

## 6. The screen and the seeds

- **Design space.** The lab's palette without Sc, Al ≥ 85 wt %, and the bounds of PR #72 as amended by #275.
  - **Decide:** Si allowed or not. The kickoff, 11:29, suggested keeping it out unless it can be measured.
    Spark-OES makes it measurable.
  - **Base.** Run the screen on the base the charges use (6063). The pure-Al base understates the crack index of
    Fe-, Mn- and Cr-rich compositions (O3: 2 K on pure Al, 569 K on 6063).
- **Screen.** Report Scheil and equilibrium calculations with the database and version named.
  - Criteria: freezing range to f_s = 0.99, Kou's crack index near f_s^½ = 1, strengthening-phase fraction at the
    aging temperature, a primary L1₂ phase ahead of α-Al, and B_NIR.
  - If no Thermo-Calc licence: pycalphad with MatCalc `mc_al`, which can't place the Al₃Zr liquidus, and COST 507,
    which supplies it. The finalists are re-checked in Thermo-Calc if it becomes available.
- **Seeds.** S1-S4, plus O1-O3 if there are slots. All are published alloys (#275), and the paper says so: they
  anchor the model and are not claimed as discoveries.
  - **Decide:** keep S1. Its B_NIR (6.6-7.3 wt %) is above Scalmalloy's, so it can't satisfy §3 whatever its
    strength.

## 7. The optimizer (choosing compositions only)

- **Fix before round 1:**
  - the model (a GP surrogate, or BO over function networks);
  - inputs (composition and CALPHAD quantities) and objective (hardness and relative density in rounds; yield
    strength for finalists);
  - acquisition function, batch size (3), and the burden constraint from §3 as a hard constraint;
  - stopping rule (fixed rounds R1-R4, cut order as in [`risks.md`](risks.md)).
- **No acceleration claim** is made in this paper (the split with #120 in [`outline.md`](outline.md)).

## 8. Hypotheses, stated before the data

Each one is reported whether it holds or not.

- **H1, printability.** Among compositions with a high Kou index (above about 500 K on the charges' 6063 base),
  those whose Scheil path forms at least a threshold fraction of a Zr-, Sc- or Ti-bearing primary phase print
  crack-free, and the others crack. **Decide** the threshold before the freeze, by fitting it to the published
  alloys of preliminary Fig. 2a. That figure shows a primary phase alone isn't enough: two known crackers have one.
- **H2, composition fidelity.** Mn and Zn are lost preferentially in ultrasonic atomization (Żrodowski et al. 2021), and
  Mg in PBF-LB/M (Croteau et al. 2018). Measured Mn in powder and parts falls below target by more than the
  tolerance in §5. Mg is over-charged by design, so its loss is reported against the nominal charge, not tested.
- **H3, powder route.** In-house AlSi10Mg-type powder (D1) and commercial AlSi10Mg, printed in the same build, differ
  in mean yield strength by less than 20 MPa (two one-sided tests at the 5 % level). Whatever the result, the primary
  comparator is D1, which shares the candidates' powder route; the commercial powder is reported alongside.
- **H4, the claim.** At least one candidate meets §2 and §3. Whether it also meets §4 is the paper's headline
  (version A); if not, version B.

## 9. What gets reported whatever happens

- Every atomizer run, including failed ones, and every specimen, including invalid ones, with the reason.
- The version of the paper (A or B) chosen at G4 by the rule in [`outline.md`](outline.md), and why.

## 10. Sign-off and change log

| Date | Commit | Who | Change and reason |
|---|---|---|---|
| | | | Frozen (fill in at G1) |
