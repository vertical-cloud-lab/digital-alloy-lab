# Outline: the Al alloy campaign paper (#277)

*Draft of 2026-11-27. Due Feb 28, 2027. The text is in [`manuscript/main.tex`](manuscript/main.tex); this file is the
argument behind it.*

## The claim, and the two versions

The campaign goal from [#277](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/277) is an alloy that
**performs better than AlSi10Mg and uses less critical minerals than Scalmalloy**. At the kickoff, Sterling loosened
"and" to "and/or" and said that "performs better" means stronger (transcript 09:03 to 10:30,
[PR #257](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/257)). The paper is written so that either
outcome can be submitted, and the choice is made at gate G4 of the
[#256 schedule](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/claude/issue-256-20261112-2149/al-campaign-schedule/README.md#gates).

| | Version A: a new alloy | Version B: a benchmarked screen |
|---|---|---|
| Headline | A scandium-free Al alloy, printed by LPBF from powder atomized in-house, with higher yield strength than AlSi10Mg printed and tested the same way, at equal or better elongation, and with a critical-mineral burden at least [X] % below Scalmalloy's | [N] scandium-free compositions atomized from dosed charges, printed and tested in 12 weeks, ranked against AlSi10Mg and Scalmalloy on one strength vs. mineral-burden map, with what CALPHAD got right and wrong |
| Needs | ≥ 1 finalist with ≥ 3 valid tensile specimens, the in-house AlSi10Mg comparator from the same machine and geometry, an outside composition check | Hardness and density on most compositions, tensile on the benchmarks and the best 1-2 alloys |
| Best journals | Letter: *Scripta Materialia*, *Materials Research Letters*, *Additive Manufacturing Letters* | Full article: *Additive Manufacturing*, *Materials & Design* |
| Decide at | G4 (Fri Jan 29 in the schedule) | |

Version A's sentence, with the brackets the campaign fills:

> Alloy [name], Al-[x]Mn-[y]Cr-[z]Zr (wt %), printed crack-free to [≥ 99.x] % density from powder atomized in-house,
> reaches [YS] MPa yield strength and [EL] % elongation [as built / after a [T] °C, [t] h direct age], [Δ] MPa above
> AlSi10Mg printed on the same machine and tested the same way (n = [n] each), with a critical-mineral burden [X] %
> below Scalmalloy's. An outside laboratory confirmed its composition to within [±] wt %.

The family in the brackets is only an example. It is whatever the screen picks.

## Two definitions to freeze before the screen ranks anything (by Dec 1, before G1)

The claim can only be checked if these are fixed in advance. Both should be committed to the repo before the CALPHAD
screen ranks anything (by Tue Dec 1, so the seeds can still be picked at G1 on Fri Dec 4), together with the
optimizer settings (SI S9). A draft is in [`preregistration.md`](preregistration.md).

**1. "Stronger than AlSi10Mg".** PR #285 showed that the datasheets can't be the bar: AlSi10Mg's datasheet rows already
pass both FLAIME G3 windows, and a desktop or sub-size result won't reproduce datasheet values anyway. Proposed rule:

- The comparator is AlSi10Mg **printed on the same machine, with the same specimen geometry, surface condition and
  test method** as the candidate. Two comparators are available or planned:
  1. commercial gas-atomized AlSi10Mg printed at Utah in April 2026: yield 228 ± 13 MPa, UTS 376 ± 10 MPa, elongation
     4.5 ± 0.5 % (as built, near-net-shape, horizontal, n = 4;
     [PR #288](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/288));
  2. AlSi10Mg-type powder atomized in-house (run D1 and its repeat D1-r), printed in the same session as the finalists.
     This one separates the alloy from the powder route.
- A candidate is "stronger" if its mean yield strength exceeds the comparator's by more than the half-widths of both
  95 % confidence intervals combined, at mean elongation no lower than the comparator's, with n ≥ 3 valid specimens
  each. AlSi10Mg is tested as built and stress-relieved, and the candidate as built and after the one heat treatment
  chosen before printing. A candidate condition counts only if it passes against AlSi10Mg in both of its conditions.
- Datasheet values (PR #285) are context in the paper, not the bar.

**2. "Less critical minerals than Scalmalloy".** A plain count or mass fraction of critical elements doesn't work for
aluminum alloys: aluminum itself is on the U.S. critical minerals list, and Mg, Mn, Cr and Zr are too (the 2025 list
is being checked element by element; see [`risks.md`](risks.md)). The kickoff said "the more that there is, that also
is expensive" (09:48), which points to an amount-weighted metric. Proposed:

- **Primary:** the mass-weighted U.S. net import reliance of the alloying additions,
  B = Σᵢ wᵢ · NIRᵢ / 100 over elements other than Al, with wᵢ in wt % and NIRᵢ from USGS *Mineral Commodity Summaries 2026*.
  It rewards using less of the elements the U.S. imports, and it is simple enough to check by hand.
- **Secondary (sensitivity):** the raw-material cost of the additions per kg of alloy, at USGS 2025 prices, and
  scandium content on its own. The paper reports all three and states the claim on the primary.
- [`scripts/mineral_burden.py`](scripts/mineral_burden.py) computes them from [`data/element-criticality.csv`](data/element-criticality.csv).
  Sterling picks the primary and the threshold [X] % (FLAIME's O4 uses ≥ 40 %, G3 uses 25 % on SRI).
- **What the inputs show (2026-11-27).**
  - Every element in play except Fe is on the final 2025 list, Al and Si included.
  - On B_NIR, AlSi10Mg (5.2-10.3 wt %) scores above Scalmalloy (4.7-6.0) at the midpoints; the intervals overlap.
    The Mn-rich seed S1 (6.6-7.3) sits above Scalmalloy's whole interval.
  - On B_cost, with Sc priced as metal, every Sc-free alloy except the two silver-bearing Al-Cu-Mg grades is at least
    97 % below Scalmalloy, and the silver-bearing ones are 74-87 % below. With Sc priced through an Al-2Sc master
    alloy, the floor is 92 % for the silver-free alloys and 14-56 % for the silver-bearing ones.
  - So B_NIR is the only one of the three that tells Sc-free alloys apart. It is still the proposed primary, with the
    claim region "stronger than in-house AlSi10Mg, and B_NIR below Scalmalloy's lower bound (4.7 wt %)". That region
    already holds five or six Sc-free alloys on their reported (mostly machined) values, or four or five against the
    strongest AlSi10Mg datasheet row (Fig. 1b), so a new alloy has to beat those, not only AlSi10Mg.
  - Details are in [`risks.md`](risks.md) (R1, R2).

## Sections and the claim each makes

Word budgets assume a full-length article of about 6,000 words (*Additive Manufacturing* or *Materials & Design*).
The letter version keeps §1, §3.4, §4 and one paragraph each of §3.1-3.3, and moves the rest of the methods to the SI.

| § | Title | Claim | Words | Data in hand | Data due |
|---|---|---|---|---|---|
| 1 | Introduction | Printable Al alloys trade strength (AlSi10Mg) against scandium (Scalmalloy); the alternatives are slow to test because powder for a new composition is hard to get | 800 | literature (written) | done |
| 2.1 | Design space and CALPHAD screen | The screen ranks [N] compositions on solidification range, crack susceptibility, strengthening phases and mineral burden | 450 | none | screen by G1 |
| 2.2 | Mineral burden | Defined above, frozen before the screen ranks anything | 200 | element inputs (in progress) | G1 |
| 2.3-2.5 | Charges, atomization, powder | Every composition is made the same way from dosed charges, and every lot has a provenance record | 600 | SOP draft, run table | first Al run |
| 2.6-2.7 | LPBF and heat treatment | Benchmarks and candidates are printed with the same specimen set on the same machine | 400 | Utah AlSi10Mg build (Apr 2026) | P1 |
| 2.8-2.10 | Density, hardness, tensile, corrosion | Standard methods, with the sub-size geometry and n stated | 500 | Utah tensile method | P1 |
| 2.11 | Independent verification | An outside lab checks composition (and, if funded, tensile) on the finalists | 200 | none | outside lab contracted by Dec 18; batch 1 ships Jan 8 |
| 3.1 | Screen and picks | Which compositions were made and why; how the optimizer's picks differed from the CALPHAD ranking | 500 | none | Jan 29 |
| 3.2 | Powders | Composition, size and shape of each powder; how close it came to the target | 500 | none | Feb 12 |
| 3.3 | Printability | Which compositions printed crack-free and dense, and whether CALPHAD's crack index predicted it | 500 | none | Feb 5 |
| 3.4 | Strength and ductility | Hardness on all, tensile on the benchmarks and finalists | 600 | in-house AlSi10Mg only | Feb 12 |
| 3.5 | Corrosion | The finalists against AlSi10Mg and wrought 6063 in 3.5 wt % NaCl | 300 | none | Feb 12 |
| 3.6 | Independent check | Outside results against in-house | 200 | none | Feb 19 |
| 4 | Benchmark comparison | Where the campaign's alloys sit against AlSi10Mg and Scalmalloy on strength, ductility and mineral burden | 600 | datasheets and in-house AlSi10Mg (written) | Feb 12 |
| 5 | Limits | Sub-size specimens, one machine, room temperature only, no fatigue | 300 | | Feb 19 |
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
| Atomization as a method (settings, yields per alloy, in the SI) | Reports, makes no claim about it | Owns the process window and repeatability (Block A), dosing fidelity, and the atomization model |
| The optimizer | One paragraph: which rounds it picked; no acceleration claim | Owns the cost-aware network optimizer, per-step costs and the replay/acceleration factor |
| CALIBER measurement settings | Uses the settings, cites CALIBER | Owns |
| Desktop LPBF, the digital twin | Only if a desktop print is in the paper | Owns |

Under this split, Block A (A1-A5) and the B dosing checks don't appear in this paper's figures; they go to #120.
Sterling decides.

## Title options

- A: *A scandium-free aluminum alloy for laser powder bed fusion that outperforms AlSi10Mg, found in a 12-week campaign on custom-atomized powder*
- A, letter: *Beating AlSi10Mg without scandium: [alloy] for laser powder bed fusion*
- B: *Twenty custom aluminum alloy powders in twelve weeks: screening scandium-free alloys for laser powder bed fusion against AlSi10Mg and Scalmalloy*

## Authors (to confirm)

From the kickoff and the schedule's leads: Gage Erickson (atomizer runs, consumables), Ronnie Guymon (powder, SEM/EDS),
Carl Robison (printing, U of U), Xavier Zaitzeff (CALPHAD, optimizer), Paul (cups and bar), Ben and Jarrett
(corrosion), Utah collaborators if they print (Spear lab), Sterling G. Baird (corresponding). Order, full names and
CRediT roles are Sterling's call; the CRediT block in `main.tex` is a placeholder.
