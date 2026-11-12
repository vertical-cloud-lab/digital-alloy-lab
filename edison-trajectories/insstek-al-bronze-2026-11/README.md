# InssTek's aluminum bronze (UNS C95300) listing: what it means for the copper/DED work

Sterling's request on PR #117 (2026-11-10): "From InssTek. Comment on this. Use Edison." The listing, as posted
in the PR from the lab's Slack:

> InssTek's material database explicitly lists Aluminum Bronze (UNS C95300) as a qualified DED material [...]
> Chemistry: Cu balance, Al 9-11%, Fe 0.8-1.5%. Typical powder size average: ~83.8 µm. Melting range:
> 1040-1045°C. Applications listed: ship propellers and marine components. InssTek DMT-produced tensile
> strength: 628 MPa (XY) / 598 MPa (Z).

Ten Edison queries in two batches (8, then 2 follow-ups), plus checks of the numbers against primary sources.
The copper/DED proposal was submitted in late October, so nothing here edits the `.tex`; this is for the work
itself, the Utah DED step, and any later version of the proposal.

## Bottom line

- **The listing is plausible and useful for the Utah step.** The chemistry and melting range are exactly UNS
  C95300's. The strengths fit what laser-deposited Cu-10Al-1Fe hardness predicts. The closest published InssTek
  work deposited the same kind of nickel-free powder at 500 W average (750 W peak) on an MX-1000.
- **C95300 is not a seawater alloy we would design toward.** It has no nickel and up to 11% Al, so it sits
  outside the searched space on two counts (Al above 9.5; iron above nickel above 7% Al). The submitted Fig. 7b
  already plots it as an open circle outside the box. The classification-society propeller alloys don't include
  it, though aluminum bronze is an accepted *repair* filler, with a stress relief.
- **Nobody has published a corrosion test of a laser-deposited nickel-free aluminum bronze** (Edison c1-02,
  c1-07, c2-01; not found in batch 1 or 2). That gap, and the fact that a short test can rank a β′-rich surface
  *better* (Guo et al. 2026), make a C95300 deposit a good known-risk control for H5.
- **The submitted Facilities PDF is right.** `Baird_ONR_YIP_Facilities.pdf` on PR #218's branch says "aluminum
  bronze (UNS C95300)". The older LaTeX copies of Field 10 (`attachments/field10-facilities-cu-ded.tex`, here and
  on PR #218's branch) say "nickel-aluminum bronze (UNS C95300)", which is wrong: C95300 has no nickel.

## InssTek's numbers against the references

| Item | InssTek listing | Reference | Checked |
|---|---|---|---|
| Chemistry | Cu bal., Al 9-11, Fe 0.8-1.5 | C95300 (ASTM B505): Cu ≥ 86.0, Al 9.00-11.00, Fe 0.80-1.50, Cu + named elements ≥ 99.0; no Ni ([Concast](https://www.concast.com/c95300.php)) | Primary data sheet |
| Melting range | 1040-1045 °C | Solidus 1040 °C, liquidus 1045 °C (Concast, CDA data). C63000, the 630 bronze being atomized: 1035-1054 °C ([Concast](https://www.concast.com/c63000.php)) | Primary data sheet |
| UTS | 628 MPa (XY), 598 MPa (Z) | Continuous-cast C95300 minimums (ASTM B505): 483 MPa as cast (yield 179, elongation 25%), 552 MPa heat treated (yield 276, elongation 12%) ([as cast](https://www.concast.com/c95300.php), [HT](https://www.concast.com/c95300HT.php)). Cast NAB C95800 minimum: 586 MPa, yield 241, elongation 18% ([Concast](https://www.concast.com/c95800.php)) | Primary data sheets |
| Consistency with laser deposits | - | Linga et al. 2022 measured about 170 HV3 in Cu-(8.5-10.75)Al-(0.5-2)Fe deposited at 500 W ([doi](https://doi.org/10.1088/1757-899X/1249/1/012042)). Müller et al. 2023's NAB deposit gives 911 MPa / 266 HV ≈ 3.4 ([doi](https://doi.org/10.1088/1757-899X/1296/1/012036)). 170 HV × 3.4 ≈ 580 MPa. Edison reports 187 HV0.5 for Freiße's 2.5-3 kW CuAl10Fe1 build (≈ 640 MPa) | Linga and Müller full texts; Freiße Edison-only (PDF blocked here) |
| Powder size | "average" about 83.8 µm | Commercial gas-atomized CuAl9.5Fe (Oerlikon Metco 51NS): measured Cu 89.3, Al 9.3, Fe 1.1; X<sub>A</sub> 10/50/90 = 64/95/135 µm (Uhlmann et al. 2024, [doi](https://doi.org/10.3390/ma17143396)). Our first 630 bronze lot (#225): volume D50 about 104 µm, 70% by volume in 50-200 µm | Uhlmann full text; #225 |
| Uses | "ship propellers and marine components" | Concast lists C95300 for bearings, gears, valve bodies, pickling hooks and "covers for marine hardware, marine equipment", not propellers. C95800 is listed for propeller blades and hubs | Primary data sheets |

What the listing doesn't give: yield, elongation, hardness, whether the bars were heat treated, density, laser
power, machine, powder supplier, whether 83.8 µm is a mean or a d50, oxygen, and any corrosion result.

The ~5% drop from XY to Z (628 to 598 MPa) is the usual direction for DED, where Z bars cross the
interlayer boundaries.

## What it says about the Utah MX-Lab

- **InssTek has shown aluminum bronze on an MX-Lab.** Its own MX-Lab page shows a tensile bar labelled "Sample
  by MX-Lab" from a dissimilar-metal build that "fractured in the AI-Bronze [sic] region, not at the dissimilar
  metal joint interface" ([insstek.com, MX-Lab](https://www.insstek.com/kor/contents/10), in Korean). The same
  page offers the MX-Lab at 500 or 700 W with a 400 µm beam. Ask Prof. Fang which one Utah has.
- **The closest published InssTek recipe is for the same kind of powder.** Makarenko and Shishkovsky deposited
  aluminum bronze with 10% Al, alternating with 316L, on an InssTek MX-1000 in DMT mode: IPG 1 kW fiber laser,
  500 W average (750 W maximum) on the bronze, 0.85 m/min, 3.5 g/min, 5 s between layers, no preheat, 800 µm
  tracks ([IOP Conf. Ser. 969, 012104 (2020)](https://doi.org/10.1088/1757-899X/969/1/012104), full text read;
  also [Materials 13, 5665 (2020)](https://doi.org/10.3390/ma13245665)). Edison reports that the powder was
  Polema Cu-9.5Al-1Fe, 45-125 µm. They report no bronze-only tensile or corrosion data.
- **500 W has deposited nickel-free aluminum bronze elsewhere too:** Linga et al. 2022 used 500 W, an 800 µm
  spot, 1000 mm/min and 3.8 g/min (on H13 steel).
- **Still not shown:** dense fusion of any aluminum bronze powder to *thick cast NAB plate* at 500 W or less
  (Edison c1-05). That remains the hard case for the repair coupons.
- **Thermal conductivity:** C95300 62.8 W/m·K, C63000 39.1, C95800 36 (Concast/CDA). 630 bronze should melt
  more easily than C95300 at the same settings, so InssTek's C95300 parameter set is a reasonable starting point
  for our 630 bronze powder on the MX-Lab.

## Why C95300 is not a candidate

- **Search space.** Table 1 caps Al at 9.5 (retained β′ as deposited) and the NAB rule requires Ni ≥ Fe above 7%
  Al. C95300 has Al 9-11 and Ni 0 with Fe 0.8-1.5, so it fails both. (So does 630 bronze on Al: 9-11.)
- **Propellers.** The classification-society propeller alloys (IACS UR W24 types CU1-CU4: manganese bronze,
  nickel-manganese bronze, NAB with 3-6% Ni and 2-6% Fe, manganese-aluminum bronze) have no nickel-free
  Cu-10Al-1Fe grade. These ranges are as reproduced by Klassert and Tikana (2007, via Edison c1-04); I couldn't
  open the IACS or DNV text from this runner. But "Al-bronze" *is* an accepted repair filler: Polish Register of
  Shipping Publication 7/P (Jan 2025, based on UR W24), Table 3.3-1, lists Al-bronze filler for CU1, CU2 and CU3
  propellers. With any filler other than NAB on a NAB (CU3) propeller, a 450-500 °C stress relief applies ("Stress
  relieving not required if welding consumable Ni-Al-bronze is used"), and the rules specify metal-arc welding
  ([PRS 7/P](https://prs.pl/wp-content/uploads/p7p_en.pdf), read in full). So InssTek's "ship propellers" most
  plausibly means repair overlay followed by heat treatment, not as-deposited service.
- **Corrosion.** No published corrosion test of a laser-deposited or DED nickel-free Cu-Al-Fe was found
  (c1-02, c1-07, c2-01). The welded-NAB literature the proposal already cites shows retained β′ attacked
  selectively in seawater (Dobson et al. 2024).
- **Nickel doesn't obviously save 630 bronze either.** Müller et al. 2023's NAB (CuAl10Ni5Fe5) deposited at
  1300 W was > 99.8% dense, 266 HV, yield 646 MPa, UTS 911 MPa, about 9% elongation, with a "martensitic-like
  structure that mainly consists of fine needles in the β′-phase" (full text read). Edison found no
  same-process comparison of β′ fractions with and without nickel (c2-02).

## Short tests and β′ (H5)

The caption of the submitted proposal's synthetic workflow (Fig. 4 in PR #218's build) says "the 1-hour screen
misses the attack of beta-prime, which develops over weeks", and H5 tests whether the one-hour screen plus
microstructure predicts 30-day immersion.

- **A short test can favor β′.** Guo et al. 2026 laser-melted a near-nickel-free aluminum bronze (measured
  Cu-11.44Al-2.37Fe-0.49Ni-0.48Mn). The remelted layer had more martensitic β′ and less α, and after 30 min at
  open circuit in 3.5% NaCl its corrosion current fell from 13.1 to 5.3 µA/cm² ([Materials 19, 3995
  (2026)](https://doi.org/10.3390/ma19183995), full text read). No longer exposure was reported.
- **Selective attack starts early but shows late.** In cast NAB in 3.5% NaCl, β′ "suffers the most serious
  corrosion damage until a protective film is formed after 150 min", and after 48 h β′ and the α + κIII
  eutectoid "are visibly attacked" (Ding et al. 2019, [Materials 12, 209](https://doi.org/10.3390/ma12020209),
  full text read). Edison reports that bulk impedance separated cast from friction-stir-processed NAB only after
  about 10 days (Song et al. 2013, Corrosion 69, 1111), and that rankings flipped between simulated seawater and
  fresh water (Cobo Ocejo et al. 2022, Metals 12, 380); neither was checked here.
- **So a DMT C95300 coupon is a useful control.** It is β′-rich, nickel-free and commercially available. If the
  one-hour CubXL screen ranks it with NAB and Cu-Ni while 30-day immersion shows selective attack, that is the
  failure H5 is designed to catch, measured on a sample whose answer is known in advance. Edison suggests (c2-01)
  a 6-24 h potentiostatic hold slightly above open circuit, then a cross-section, as an intermediate test; that
  is its suggestion, not a validated method.

## Questions for InssTek (through the US representative)

1. Which machine and laser power made the C95300 bars, and what parameter set (power, spot, speed, feed)?
2. Were the 628/598 MPa bars as deposited or heat treated? Yield, elongation, hardness and density?
3. The powder: supplier, atomization route, d10/d50/d90 (is 83.8 µm a mean or a d50?), oxygen, flow.
4. Any corrosion data (3.5% NaCl, substitute or natural seawater), or any propeller repair done with it?
5. Could they sell 2 kg of the powder, and deposit two small as-deposited C95300 blocks for our corrosion tests?

## Where Edison went wrong or overreached

- c1-02 said as-deposited C95300 "will almost certainly fail in seawater". No published test exists; that is an
  expectation from β′ in welds, and Guo 2026 shows a short test can point the other way.
- c1-02 said a 675 °C anneal of C95300 would give "only γ2 (not κ)". Iron forms κ-type particles without nickel,
  and γ2 forms on slow cooling below about 565 °C; this was not checked and is not repeated here.
- c1-01 said 628 MPa "would almost certainly be" retained β′. The hardness check above shows the strength is in
  line with ~170-190 HV laser-deposited Cu-10Al-1Fe; the phase mix is unknown.
- c1-01 gave ASTM B148 C95300 minimums of 450 MPa as cast and 515 MPa (yield 205, elongation 20%) as TQ50. The
  ASTM B505 heat-treated minimum on Concast's sheet is 552 MPa (yield 276, elongation 12%). B148 itself wasn't
  checked.
- c2-01 said natural seawater rates are "10× higher" than substitute seawater. Its own source (Dobson 2024)
  gives annual averages of about 0.11 vs 0.06 mm/y, with a 1.27 mm/y initial natural-seawater rate.
- c2-01 called C95300 "the PI's planned" deposit. It isn't planned; the question proposed it as a control.
- Edison reports that Rubio-Ejchel et al. 2026 (J. Mater. Res. 41, 2899) deposited GRCop-42 on an MX-Lab at
  250 W through a 0.4 mm spot. The DOI resolves, but the abstract doesn't give the machine or power and the
  full text was blocked here.

## Queries

| Query | Job | Task | Answer |
|---|---|---|---|
| DED of nickel-free aluminum bronze: phases and tensile properties | LITERATURE_HIGH | `34cf5e9f` | [c1-01](batch1/c1-01-ded-ni-free-al-bronze-properties.md) |
| Seawater corrosion of rapidly solidified nickel-free aluminum bronze | LITERATURE_HIGH | `550d1439` | [c1-02](batch1/c1-02-ni-free-al-bronze-seawater-as-deposited.md) |
| InssTek DMT copper alloy work; class approvals | LITERATURE | `e77a7eff` | [c1-03](batch1/c1-03-insstek-dmt-copper-work.md) |
| C95300 marine use, propeller grades, properties | LITERATURE | `df874150` | [c1-04](batch1/c1-04-c95300-marine-use-and-specs.md) |
| Infrared laser power for aluminum bronze deposits | LITERATURE | `4a05f7ea` | [c1-05](batch1/c1-05-ir-laser-power-al-bronze.md) |
| Commercial aluminum bronze and NAB powders in DED cuts | LITERATURE | `d4473701` | [c1-06](batch1/c1-06-commercial-al-bronze-ded-powders.md) |
| Precedent: DED C95300 at 600-630 MPa | PRECEDENT | `b1de059d` | [c1-07](batch1/c1-07-precedent-dmt-c95300.md) |
| Propeller repair by laser and additive processes | LITERATURE | `40b1dc95` | [c1-08](batch1/c1-08-ded-propeller-repair-practice.md) |
| How fast β′ attack appears; can short tests see it | LITERATURE_HIGH | `fc6a3970` | [c2-01](batch2/c2-01-beta-prime-attack-timescale.md) |
| Nickel and retained β′ in laser deposits | LITERATURE | `6334bbd3` | [c2-02](batch2/c2-02-nickel-and-beta-prime-retention.md) |

Batch 1 was submitted at 15:58 UTC and batch 2 at 16:31 UTC on 2026-11-10; all ten succeeded. Full task ids
are in [`_task_ids.json`](_task_ids.json); [`queries.py`](queries.py) holds the questions and
[`edison_insstek.py`](edison_insstek.py) is `cu-ded-2026-10/edison_cu_ded.py` with a new docstring. The raw
trajectories are not committed (`raw/` is gitignored): they hold the text of the papers Edison read, including
authors' contact emails. They can be fetched again from the Edison API with the task ids. The answers are as
Edison returned them; they contain no email addresses.
