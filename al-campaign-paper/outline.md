# Outline: the Al alloy campaign paper (#277)

*Draft of 2026-11-27 (revised the same day for the in-house Sc-free baselines). Due Feb 28, 2027. The text is in [`manuscript/main.tex`](manuscript/main.tex); this file is the
argument behind it.*

## The claim, and the two versions

The campaign goal from [#277](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/277) is an alloy that
**performs better than AlSi10Mg and uses less critical minerals than Scalmalloy**. At the kickoff, Sterling loosened
"and" to "and/or" and said that "performs better" means stronger (transcript 09:03 to 10:30,
[PR #257](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/257)).

**Reframed on 2026-11-27** ([#277 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/277#issuecomment-7228308921)).
Sc-free LPBF aluminum stronger than AlSi10Mg is already sold, so beating AlSi10Mg is not a discovery. The campaign
now tries to **expand the Sc-free Pareto front of yield strength against critical-mineral burden**. The front is
anchored by commercial Sc-free powders that the lab buys, prints and tests exactly as it does its own candidates,
AlSi10Mg and Scalmalloy: **EOS Al5X1** (Al-Mg-Zr-Mn), and **Höganäs Al-HS1** (Al-Mn-Cr-Zr) if the budget allows
([`baselines.md`](baselines.md)). AlSi10Mg stays as the floor, and Scalmalloy as the burden reference.

| | Version A: a new alloy beyond the front | Version B: a benchmarked screen on one machine |
|---|---|---|
| Headline | A scandium-free Al alloy, printed by PBF-LB/M from powder atomized in-house, that lies beyond the Sc-free front: stronger than in-house Al5X1 at equal or lower burden, or less burden at equal strength, and below Scalmalloy's burden at every allowed import reliance | [N] Sc-free compositions from dosed charges, printed and tested on the same machine as four commercial powders (AlSi10Mg, Al5X1, Al-HS1, Scalmalloy), placed on one strength vs. burden map, with what CALPHAD got right and wrong and how far the machine's results sit from the vendors' datasheets |
| Needs | ≥ 1 finalist with ≥ 3 valid tensile bars, in-house Al5X1 (and AlSi10Mg) from the same session, an outside composition check of finalist and baselines | In-house tensile on the commercial powders; hardness and density on most compositions; tensile on the best 1-2 |
| Best journals | Letter: *Scripta Materialia*, *Materials Research Letters*, *Additive Manufacturing Letters* | Full article: *Additive Manufacturing*, *Materials & Design* |
| Decide at | G4 (Fri Jan 29 in the schedule), or when in-house Al5X1 data exist if that is later | |

Version A's sentence, with the brackets the campaign fills:

> Alloy [name], Al-[x]Fe-[y]Mg-[z]Zr (wt %), printed crack-free to [≥ 99.x] % density from powder atomized in-house,
> reaches [YS] MPa yield strength and [EL] % elongation after [a [T] °C, [t] h direct age]. That is [Δ] MPa above
> commercial Al5X1 printed in the same session and tested the same way (n = [n] each), at [equal / X % lower]
> import-weighted critical-mineral burden, which is below Scalmalloy's at every allowed import reliance. An outside
> laboratory confirmed both compositions to within [±] wt %.

The family in the brackets is only an example. It is whatever the screen picks. Under B_NIR the screen leans toward
Fe-, Zr- and Mg-lean families, because that is where the front has room (Fig. 1b).

**What "expanding the front" means, and why one front isn't enough.** On reported values the Sc-free front inside the
region of interest has four alloys: Aheadd CP1 (Al-Fe-Zr, 300 MPa aged, B_NIR 0.14 wt %), Al-1.87Fe-1.02Mg-1.03Zr
(376 MPa aged, 1.02), Al5X1 (385 MPa aged, 3.63) and EOS Al2139 T4 (460 MPa, 3.89). Al-HS1 sits behind Al5X1:
weaker, at 1.4-2.4 wt % more burden at the same reliances. Measuring Al5X1 and Al-HS1 in-house fixes the front's
middle on our own machine. Its low-burden end (B_NIR below about 3) has no bought baseline, so a low-burden candidate
must also be checked against the reported values there (pre-registration §4). A third purchase, Aheadd CP1, would
close that gap and is worth deciding after the screen.

## Definitions to freeze before the screen ranks anything (by Dec 1, before G1)

The claim can only be checked if these are fixed in advance. They go into [`preregistration.md`](preregistration.md)
and are committed before the CALPHAD screen ranks anything (by Tue Dec 1, so the seeds can still be picked at G1 on
Fri Dec 4), together with the optimizer settings (SI S9).

**1. The comparators and "printed and tested the same way".**

- **Every alloy, bought or made, gets the same procedure:** same machine (Utah's Aconity MIDI), layer thickness, plate
  temperature, scan strategy, gas, powder handling, specimen geometry and surface, test and statistics.
- **Laser power and speed follow the same rule, not the same numbers.** Each alloy gets the same power-speed grid of
  density cubes, and its bars are printed at its densest grid point. One parameter set for all alloys would favour
  whichever alloy it was tuned for.
- **Each alloy is its own build** (one powder per build), so "the same session" means consecutive builds, not one
  build. The earlier draft's "same build" can't happen on a single-powder machine.
- **Heat treatments are each vendor's**:
  - Al5X1: 400 °C for 6 h, gas quench.
  - Al-HS1: 375 °C for 4 h.
  - Scalmalloy: 325 °C for 4 h.
  - AlSi10Mg: as built and stress-relieved.
  - Each candidate: as built and one direct age chosen before printing.

**2. "Expands the front".** A candidate condition expands the front if all of these hold:

- it is **stronger than in-house AlSi10Mg** by more than the two 95 % confidence half-widths combined, at no lower
  elongation (the floor), in both of AlSi10Mg's conditions;
- its **B_NIR is below Scalmalloy's at every allowed import reliance** (paired test, measured compositions);
- **no in-house baseline dominates it.** Every baseline whose burden is not robustly above the candidate's must be
  weaker by more than the two half-widths combined. Baseline means in-house Al5X1, Al-HS1 and Scalmalloy, each in its
  vendor condition;
- **no reported Sc-free alloy dominates it** on reported values ([`data/literature-alloys.csv`](data/literature-alloys.csv),
  frozen with the pre-registration). This is a secondary check, stated as against reported values.

The size of the step is reported as the area it adds to the in-house front, measured inside the region of interest
(hypervolume improvement, burden at the midpoint reliances).

**3. "On par with the industry datasheets".** For each bought powder, the in-house mean yield, in the vendor's
condition and the horizontal orientation, is at least 0.90 of the vendor's typical value (Fig. 5d). Elongation is
reported, not tested, because as-printed sub-size bars lose more elongation than yield against machined bars. On
April's data AlSi10Mg is at 0.76-0.85, so not on par ([`baselines.md`](baselines.md#alsi10mg-at-228-mpa-what-it-means-for-using-it-as-a-baseline)).

**4. The burden metric: B_NIR** ([recommendation](baselines.md#the-burden-metric-to-freeze-before-the-screen-ranks-anything)).

- **Definition.** B_NIR = Σᵢ wᵢ · NIRᵢ / 100 over the alloying elements other than Al, with wᵢ in wt % and NIRᵢ from
  USGS *Mineral Commodity Summaries 2026*. Fe counts zero.
- **Comparing two alloys:** under the same import reliances (Si, Mg and Zr have only bounds), so "below Scalmalloy"
  means below at every allowed reliance.
- **Plotting:** at the midpoint reliances.
- **Compositions:** measured by the outside lab, for the baselines too. Al5X1's composition range alone spans B_NIR 2.0-5.7.
- **Reported as sensitivity, not used for the claim:** B_mass (wt % of listed elements) and B_cost (cost of the
  critical additions).
- **Why B_NIR:**
  - Of the three, it is the only one that both counts how much critical material an alloy uses (the kickoff's
    "the more that there is", 09:48) and separates Sc-free alloys, which a front needs.
  - B_cost puts every silver-free Sc-free alloy at 0.25-0.94 USD/kg against Scalmalloy's 39.9, so it can't rank them.
  - B_NIR is FLAIME's mineral-burden node with USGS import-reliance weights.
- **What it says now** (Table 1, SI table of paired differences):
  - Al5X1 is below Scalmalloy at every reliance (−2.01 to −1.45 wt %).
  - Al-HS1 depends on Mg's reliance (−0.48 to +0.82).
  - AlSi10Mg depends on Si's (−0.66 to +5.51).
  - Seeds S2 and O1 are below. S3 depends. S1, S4, O2 and O3 are above, so they can't meet the claim whatever
    their strength.

## Sections and the claim each makes

Word budgets assume a full-length article of about 6,000 words (*Additive Manufacturing* or *Materials & Design*).
The letter version keeps §1, §3.4, §4 and one paragraph each of §3.1-3.3, and moves the rest of the methods to the SI.

| § | Title | Claim | Words | Data in hand | Data due |
|---|---|---|---|---|---|
| 1 | Introduction | Printable Al alloys trade strength (AlSi10Mg) against scandium (Scalmalloy); the alternatives are slow to test because powder for a new composition is hard to get | 800 | literature (written) | done |
| 2.1 | Design space and CALPHAD screen | The screen ranks [N] compositions on solidification range, crack susceptibility, strengthening phases and mineral burden | 450 | none | screen by G1 |
| 2.2 | Mineral burden | Defined above, frozen before the screen ranks anything | 200 | element inputs (in progress) | G1 |
| 2.3-2.5 | Charges, atomization, powder | Every composition is made the same way from dosed charges, and every lot has a provenance record | 600 | SOP draft, run table | first Al run |
| 2.3a | Commercial powders | AlSi10Mg, Al5X1, Al-HS1 and Scalmalloy bought, with lot certificates, handled like in-house powder | 150 | sourcing in [`baselines.md`](baselines.md); nothing ordered | PO by Dec 11 |
| 2.6-2.7 | LPBF and heat treatment | Every alloy is printed on one machine by one procedure (same grid rule, own densest point), each vendor's heat treatment for the bought powders | 450 | Utah AlSi10Mg build (Apr 2026) | P1 |
| 2.8-2.10 | Density, hardness, tensile, corrosion | Standard methods, with the sub-size geometry and n stated | 500 | Utah tensile method | P1 |
| 2.11 | Independent verification | An outside lab checks composition (and, if funded, tensile) on the finalists | 200 | none | outside lab contracted by Dec 18; batch 1 ships Jan 8 |
| 3.1 | Screen and picks | Which compositions were made and why; how the optimizer's picks differed from the CALPHAD ranking | 500 | none | Jan 29 |
| 3.2 | Powders | Composition, size and shape of each powder; how close it came to the target | 500 | none | Feb 12 |
| 3.3 | Printability | Which compositions printed crack-free and dense, and whether CALPHAD's crack index predicted it | 500 | none | Feb 5 |
| 3.4a | The commercial powders on our machine | In-house AlSi10Mg, Al5X1, Al-HS1 and Scalmalloy against their datasheets (on par or not), and the in-house front | 400 | in-house AlSi10Mg only (0.76-0.85 of its datasheets) | Jan 29 (best case) to Feb 12 |
| 3.4b | Strength and ductility | Hardness on all, tensile on the finalists, placed against the in-house front | 500 | none | Feb 12 |
| 3.5 | Corrosion | The finalists against AlSi10Mg and wrought 6063 in 3.5 wt % NaCl | 300 | none | Feb 12 |
| 3.6 | Independent check | Outside results against in-house | 200 | none | Feb 19 |
| 4 | The front and the burden metric | Where the campaign's alloys sit against the Sc-free front (in-house and reported) and Scalmalloy, on the frozen metric and its sensitivity | 600 | datasheets, in-house AlSi10Mg, the front on reported values (written) | Feb 12 |
| 5 | Limits | Sub-size specimens, one machine, one lot per bought powder, vendor parameter sets not used, room temperature only, no fatigue | 300 | | Feb 19 |
| 6 | Conclusions | | 150 | | Feb 22 |

## Keeping this paper apart from the *Advanced Materials* article (#120)

[#120](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/120) is now due in early 2028. Its October
outline said "the atomization results are being saved for this article rather than a separate paper", and the
[#256 schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#assumptions-to-confirm)
had assumed the two were the same paper. They now aren't, and a run on #120 started at the same time as this one. A
journal will check whether the second paper's results were already published, so the split should be decided now.
Proposed:

| Result | This paper (Feb 2027) | *Adv. Mater.* (2028) |
|---|---|---|
| The alloys: compositions, powders, prints, properties, corrosion, benchmark map, mineral burden | **Owns** | Cites this paper |
| The commercial powders printed here (AlSi10Mg, Al5X1, Al-HS1, Scalmalloy), their on-par ratios and the in-house front | **Owns** | Cites this paper |
| Atomization as a method (settings, yields per alloy, in the SI) | Reports, makes no claim about it | Owns the process window and repeatability (Block A), dosing fidelity, and the atomization model |
| The optimizer | One paragraph: which rounds it picked; no acceleration claim | Owns the cost-aware network optimizer, per-step costs and the replay/acceleration factor |
| CALIBER measurement settings | Uses the settings, cites CALIBER | Owns |
| Desktop LPBF, the digital twin | Only if a desktop print is in the paper | Owns |

Under this split, Block A (A1-A5) and the B dosing checks don't appear in this paper's figures; they go to #120.
Sterling decides.

## Title options

- A: *Beyond the scandium-free front: an aluminum alloy for laser powder bed fusion that outperforms commercial Al-Mg-Zr-Mn on our machine, with less critical-mineral burden than Scalmalloy*
- A, letter: *Expanding the scandium-free strength-burden front of PBF-LB/M aluminum with custom-atomized powder*
- B: *Twenty custom aluminum alloy powders and four commercial ones on one machine: where scandium-free alloys for laser powder bed fusion stand against AlSi10Mg and Scalmalloy*

## Authors (to confirm)

From the kickoff and the schedule's leads: Gage Erickson (atomizer runs, consumables), Ronnie Guymon (powder, SEM/EDS),
Carl Robison (printing, U of U), Xavier Zaitzeff (CALPHAD, optimizer), Paul (cups and bar), Ben and Jarrett
(corrosion), Utah collaborators if they print (Spear lab), Sterling G. Baird (corresponding). Order, full names and
CRediT roles are Sterling's call; the CRediT block in `main.tex` is a placeholder.
