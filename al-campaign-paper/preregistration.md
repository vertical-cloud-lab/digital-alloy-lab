# Pre-registration (DRAFT, not frozen)

*A draft for Sterling to edit and commit **before the CALPHAD screen ranks any campaign composition**: by Tue Dec 1,
2026, so the screen can rank on Dec 2-3 and the seeds can be picked at G1 (Fri Dec 4). The commit hash that freezes it goes in SI Section S9 and the Methods (§2.2, §2.12). Every choice below
is a proposal; the open ones are marked **Decide**. After the freeze, any change gets a dated entry in the change
log at the bottom, with its reason, so a reviewer can see what was fixed in advance and what wasn't.*

## 1. The claim being tested

> A scandium-free aluminum alloy, printed by PBF-LB/M from powder atomized in-house, **expands the Sc-free front**
> of yield strength against critical-mineral burden. No commercial Sc-free powder printed and tested the same way
> on the same machine (EOS Al5X1, and Höganäs Al-HS1 if bought) dominates it, and neither does any reported Sc-free
> alloy. It is also **stronger than AlSi10Mg** printed and tested the same way, at no lower ductility, and carries
> **less critical-mineral burden than Scalmalloy** at every allowed import reliance.

The comparison set and the reason for it are in [`baselines.md`](baselines.md). Sc-free alloys stronger than
AlSi10Mg are already sold, so beating AlSi10Mg alone is a replication, not a discovery.

## 2. Comparators, and "printed and tested the same way"

- **Bought powders** (one lot each, with the vendor's lot certificate):
  1. commercial gas-atomized **AlSi10Mg**;
  2. **EOS Al5X1** (article 9030-0017), the front-defining baseline;
  3. **Höganäs forAM Al-HS1 GA** 20-63 µm, if bought;
  4. **Scalmalloy**, from APWORKS or a licensed producer, or the in-house D2 if none is bought.
- **In-house route control.** AlSi10Mg-type powder atomized in-house (runs D1 and D1-r), and, if Zr is in hand, the
  Al5X1 twin (O1 repurposed: Al-3.35Mg-0.55Mn-1.2Zr from dosed charges).
- **Until the bought powders are printed**, the April 2026 Utah AlSi10Mg build (228 ± 13 MPa yield, n = 4) is a
  provisional comparator and is reported as such.
- **Same procedure for every alloy:** one machine (the Aconity MIDI at the University of Utah), one layer thickness,
  plate temperature, scan strategy, gas flow and powder handling (sieve, dry, humidity log).
  - **Decide:** layer thickness and plate temperature. Ask Utah for the April build's values first.
- **Laser power and speed: the same rule, not the same numbers.** Every alloy gets the same power-speed grid of
  density cubes, and its tensile bars are printed at its densest grid point. Ties go to the lower energy density.
- **One powder per build.** "Same session" means consecutive builds on the same machine within one Utah visit.
- **Specimens.** Flat ASTM E8/E8M sub-size bars, 6 × 6 mm reduced section, built horizontal, with the same surface
  for all alloys.
  - **Decide:** as-printed or machined.
- **Test.** Room temperature, with a clip-on extensometer or DIC over a 25 mm gauge, and the strain rate within
  ASTM E8/E8M limits while yield is measured. Bars that break outside the gauge are excluded and reported.
- **Conditions:**
  - AlSi10Mg: as built and stress-relieved (**Decide:** 300 °C for 2 h or the vendor's 285 °C).
  - Al5X1: as built and 400 °C for 6 h with gas quench, inert atmosphere if available.
  - Al-HS1: as built and 375 °C for 4 h in air.
  - Scalmalloy: as built and 325 °C for 4 h.
  - Each candidate: as built and one direct age chosen before printing.
- **Floor rule: stronger than AlSi10Mg.** A candidate condition passes if all of these hold, against AlSi10Mg in
  *both* of its conditions:
  - mean yield(candidate) − mean yield(AlSi10Mg) > hw(candidate) + hw(AlSi10Mg), where hw is the half-width of the
    95 % Student-t confidence interval;
  - mean elongation(candidate) ≥ mean elongation(AlSi10Mg);
  - n ≥ 3 valid bars each.
- **Datasheets.** Vendor datasheet values are context and the reference for the on-par check (§4b). They are never
  the bar.

## 3. Critical-mineral burden

- **Inputs.** [`data/element-criticality.csv`](data/element-criticality.csv) at the freeze commit: USGS *Mineral
  Commodity Summaries 2026* net import reliance and 2025 prices, and the final 2025 U.S. List of Critical Minerals.
  Later USGS editions aren't swapped in.
- **Primary metric, B_NIR.** B_NIR = Σ wᵢ · NIRᵢ / 100 over alloying elements other than Al (wt % of the alloy).
  Fe counts zero.
- **Comparing two alloys.** Where USGS gives only a bound (Si > 50 %, Mg > 75 %, Zr < 25 %), the reliance is unknown
  but the same for every alloy. Two alloys are compared under the same reliances. B_NIR(a) − B_NIR(b) is linear in
  each reliance, so its range over all allowed values comes from the bounds
  (`paired_difference` in [`scripts/mineral_burden.py`](scripts/mineral_burden.py)).
- **"Less than Scalmalloy".** The candidate's B_NIR is below Scalmalloy's at every allowed reliance: the upper end of
  the paired difference is below zero.
  - **Decide:** this robust form, or a percentage below Scalmalloy at the midpoint reliances (FLAIME's O4 uses ≥ 40 %).
  - On current inputs, Al5X1 passes the robust form (−2.01 to −1.45 wt %). Al-HS1 does not (−0.48 to +0.82).
- **Plots** use the midpoint reliances.
- **Reported alongside, not used for the claim:**
  - B_mass, the wt % of elements on the 2025 list;
  - B_cost, the cost of the critical additions, with Sc priced as metal and as Al-2Sc master alloy;
  - Sc content;
  - B_NIR with Al counted.
- **Composition used.** The measured composition from the outside laboratory (§5), for candidates *and* for the
  bought powders. A vendor's typical values or range midpoints are only placeholders: Al5X1's range alone spans
  B_NIR 2.0-5.7 wt %.

## 4. "Expands the Sc-free front"

- **In-house front.** The bought baselines (Al5X1, Al-HS1 if bought, Scalmalloy), each in its vendor condition, as
  printed and tested under §2, at their measured compositions.
- **Rule against the in-house front.** A candidate condition is not dominated if, for every baseline whose B_NIR is
  not robustly above the candidate's (§3, paired), mean yield(candidate) − mean yield(baseline) > hw(candidate) +
  hw(baseline).
- **Rule against reported values (secondary).** No alloy in [`data/literature-alloys.csv`](data/literature-alloys.csv)
  at the freeze commit has both a higher reported yield strength and a B_NIR robustly below the candidate's. Every row
  is checked against its source or marked unverifiable; unverifiable rows are shown but left out of this test. The
  paper states this comparison as against reported values, mostly on machined bars from tuned processes.
- **Size of the step.** The hypervolume the candidate adds to the in-house front inside the region of interest. The
  region is yield above the in-house AlSi10Mg floor and B_NIR below Scalmalloy's, at the midpoint reliances.
- **Decide:** whether the claim also needs non-domination on elongation, and whether to buy Aheadd CP1 to anchor the
  front's low-burden end in-house (below Al5X1's B_NIR there is no bought baseline, only reported values).

## 4b. "On par with the industry datasheets"

- For each bought powder and each vendor condition, the ratio of the in-house mean yield to the vendor's typical
  value for horizontal bars, with its 95 % confidence interval (Fig. 5d).
- **On par** if the ratio is at least **0.90**. **Decide** the threshold. The 10 % allows for as-printed sub-size bars
  against machined ones, and a different machine.
- Elongation ratios are reported but not tested.
- If a bought powder is not on par, the claim stays relative to the in-house front. The paper then says how far the
  machine sits from the datasheets and makes no claim against datasheet values.

## 5. Composition and independent verification

- **In-house.** EDS on every powder lot, standards-based (DTSA-II), with the acquisition settings recorded.
- **Outside, accredited lab.**
  - The bought powders' lots (AlSi10Mg, Al5X1, Al-HS1, Scalmalloy) and the finalist powders, and one printed coupon
    of each finalist and each bought powder.
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
    aging temperature, the amount of Zr-, Sc- or Ti-bearing primary phase ahead of α-Al (the databases give
    equilibrium Al₃Zr as D0₂₃, so it isn't called L1₂ here), and B_NIR.
  - If no Thermo-Calc licence: pycalphad with MatCalc `mc_al`, which can't place the Al₃Zr liquidus, and COST 507,
    which supplies it. The finalists are re-checked in Thermo-Calc if it becomes available.
- **Seeds.** S1-S4, plus O1-O3 if there are slots. All are published alloys (#275), and the paper says so: they
  anchor the model and are not claimed as discoveries.
  - **Proposed: drop S1.** Its B_NIR is above Scalmalloy's at every allowed reliance (+0.97 to +2.21 wt %), so it
    can't satisfy §3 whatever its strength, and Al-HS1 now anchors the Mn-rich family in-house.
  - **Proposed: repurpose O1 as the Al5X1 twin** (Al-3.35Mg-0.55Mn-1.2Zr). Its burden equals Al5X1's (paired
    difference −0.19 to +0.04 wt %). Printed in the same session as commercial Al5X1, it measures the powder route on
    a front alloy (H5).

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
- **H3, powder route.** In-house AlSi10Mg-type powder (D1) and commercial AlSi10Mg, printed in the same session, differ
  in mean yield strength by less than 20 MPa (two one-sided tests at the 5 % level). Whatever the result, the primary
  comparator is D1, which shares the candidates' powder route; the commercial powder is reported alongside.
- **H4, the claim.** At least one candidate meets §2 and §3. Whether it also meets §4 is the paper's headline
  (version A); if not, version B.
- **H5, the machine against the datasheets.** Aged Al5X1 printed and tested here is on par with its datasheet
  (§4b, ratio ≥ 0.90), and its ratio is higher than as-built AlSi10Mg's. This tests whether AlSi10Mg's deficit
  (0.76-0.85 in April) is AlSi10Mg's or the process's. If the Al5X1 twin is made, its yield is within 20 MPa of
  commercial Al5X1's (two one-sided tests at the 5 % level), as in H3.
- **H6, the front's order.** Printed here, Al5X1 dominates Al-HS1 (stronger, at lower burden), as the datasheets
  suggest. If it doesn't, Al-HS1 joins the in-house front, and the paper says so.

## 9. What gets reported whatever happens

- Every atomizer run, including failed ones, and every specimen, including invalid ones, with the reason.
- The version of the paper (A or B) chosen at G4 by the rule in [`outline.md`](outline.md), and why.

## 10. Sign-off and change log

| Date | Commit | Who | Change and reason |
|---|---|---|---|
| | | | Frozen (fill in at G1) |
