# The CubXL and the corrosion screen (copper/DED version)

*2026-10-17, for PR #117. Sterling asked: "look into use of our CubXL for
this project (see many byu-vcl conversations) on the electrochemical side,
noting that we have access to a potentiostat, but not sure if that's
necessary." The byu-vcl facts below come from issues #26, #133, #148, #165,
#203, #213, #231, #266 and PR #278 (aluminum corrosion on the CubXL). The
literature behind it is in
[`edison-trajectories/cu-ded-elements-2026-10/electrochem/`](../../edison-trajectories/cu-ded-elements-2026-10/electrochem/).*

## Short answer

- **The screen does need a potentiostat.** Linear polarization, impedance
  and cyclic polarization are potentiostat measurements, and H5 is a test
  of exactly that screen. Without a potentiostat, the CubXL can still
  measure open-circuit potential with a high-impedance meter, metal released
  into the solution (by ICP-MS), mass loss, and images. These add to the
  screen; they do not replace it.
- **An $18,000 benchtop unit with a flat cell is probably not needed.**
  - **Currents:** copper alloys in seawater corrode faster than passive
    aluminum, so a 3-4 mm well gives about 50 nA to 0.6 µA in linear
    polarization and well under 1 mA in cyclic polarization (estimate
    below).
  - **Instrument:** a PalmSens EmStat Pico covers those currents and also
    does impedance (0.016 Hz to 200 kHz). #231 lists it at about $580.
  - **Software:** CubOS, the CubXL's software, already has an EmStat
    driver family.
  - **Cross-check:** a borrowed laboratory potentiostat (Dr. Porter's)
    serves as the reference instrument.
- **The CubXL is what makes the screen cheap.** The cost-aware search needs
  the screen to cost little, so the CubXL is what earns the screen its place
  as a cheap step in the search. It also makes three measurements possible
  that a hand-run flat cell does not:
  - many spots on one specimen, including across the fusion line of a
    repair coupon;
  - the used electrolyte of every spot, collected for ICP-MS;
  - samples drawn from immersion vials over time.

## What the CubXL is today (byu-vcl)

- **Hardware:**
  - **Origin and motion:** an Ursa Laboratories system on a SainSmart
    Genmitsu PROVerXL 4030 V2 gantry running GRBL (#133).
  - **Working volume:** about 388 × 234 × 121 mm (#165, #266).
  - **One head, no tool changer (#213):** it carries an Opentrons P20
    pipette, an electromagnetic vial capper and two Pi cameras.
- **What has run:** pipetting tests only, run by Claude from the Pi over
  Tailscale (#133, #169, #203). The lab rules require a person at the
  machine and one approval per run. No chemistry has been run yet.
- **Electrochemistry:**
  - **Driver support:** CubOS drives Admiral Squidstat and PalmSens EmStat
    potentiostats for open-circuit potential, cyclic voltammetry,
    chronoamperometry and chronopotentiometry.
  - **Missing methods:** it has no linear sweep below 1 mV/s, no reversal
    at a set current, and no impedance (#278).
  - **Hardware owned:** the lab owns no potentiostat, cell or electrodes
    (#26, #231). Jarrett plans to use Dr. Porter's potentiostat the week of
    Oct 19 (#231); its model is not known.
- **Corrosion plan (PR #278, aluminum, on paper):**
  - **Cell:** printed clamps with 3-4 mm FKM O-ring wells (0.071-0.126 cm²,
    about 150 µL each), a pogo pin on the bare back, and a leak-free Ag/AgCl
    mini-reference plus a Pt counter on the head.
  - **Sequence:** 30 min open-circuit potential, then linear polarization at
    ±10 mV and 0.167 mV/s, then cyclic polarization reversing at 1 mA/cm².
  - **Records:** a photo of each spot; the used electrolyte goes to ICP.
  - **Throughput:** about 6 spots per 12-hour night at G61 scan rates.
  - **The copper plan below reuses this cell and sequence.**

## What the copper project needs

The copper proposal (Task 2) asks for:

- **The screen:** open-circuit potential, linear polarization, impedance and
  cyclic polarization on polished faces in ASTM D1141 substitute ocean
  water, run every round.
- **References:** wrought 70-30 Cu-Ni and heat-treated cast NAB, measured
  every round.
- **Long tests:** 30-day immersions with mass loss and the depth of
  selective attack on selected candidates.
- **Hypothesis H5:** the screen predicts which candidates pass the immersion
  test.

**Current estimate (mine, from published rates).**

- **Rates:** 90-10 and 70-30 Cu-Ni corrode at about 0.0025-0.025 mm/yr in
  seawater ([copper.org](https://copper.org/applications/marine/cuni/properties/corrosion)),
  about 0.2-2 µA/cm² (1 µA/cm² is about 0.011 mm/yr for 70-30). A fresh
  surface runs higher: on wrought 70-30 the current fell about eightfold
  over 10 days (Yuan 2007, already cited).
- **Linear polarization:** with a Stern-Geary constant of about 25 mV,
  ±10 mV on a 3 mm well (0.071 cm²) gives about 50 nA (2 µA/cm²) to 0.6 µA
  (20 µA/cm²).
- **Cyclic polarization:** reversing at 1 mA/cm² gives 71 µA.

**What that means for the instruments on the #231 list.**

| | Rodeostat HC | MYSTAT | EmStat Pico | Benchtop unit with flat cell |
| --- | --- | --- | --- | --- |
| Price in #231 / #26 | $240 (sold out) | about $340 to build | about $580 | Squidstat about $4-6k; the proposal's line is $18,000 |
| Linear polarization on a 3 mm copper well | workable: 50 nA is about 10 steps of 4.9 nA | yes | yes (100 nA range, 5.5 pA resolution) | yes |
| Impedance | no | no | yes, 0.016 Hz-200 kHz (high-speed mode) | yes |
| CubOS driver | none | none | EmStat family driver (Pico untested) | Squidstat or EmStat4 drivers |

So for copper the low-current problem of PR #278 (passive aluminum, down to
about 1 nA) mostly goes away. Impedance is then what decides. Of the cheap
units, only the EmStat Pico does it.

## What the CubXL adds for the copper work

1. **Several wells per specimen,** with every spot photographed before and
   after. Images catch crevice attack at the O-ring, the usual small-cell
   artifact.
2. **Repair coupons measured across the fusion line,** with wells in the
   deposit, at the fusion line and heat-affected zone, and in the cast NAB
   or wrought Cu-Ni substrate. Retained β′ in the heat-affected zone of
   welded NAB corroded selectively in seawater (Dobson 2024, already cited),
   so this is where a repair is most likely to fail.
3. **Which elements leave the surface.**
   - **Method:** the used electrolyte of each well goes to ICP-MS at BYU
     (Agilent 8900).
   - **What it shows:** aluminum released from NAB faster than its share
     of the alloy points to de-aluminification; the nickel-to-copper ratio
     from Cu-Ni shows whether nickel leaves preferentially.
   - **Cost:** it needs no potentiostat time.
4. **Immersion vials sampled over time.**
   - **Setup:** coupons sit in capped vials of substitute ocean water on
     the deck. The capper opens each vial, and the pipette draws 20 µL at
     about 1, 3, 10 and 30 days for ICP-MS.
   - **Effect on the vial:** 20 µL from 40 mL is 0.05% of the solution.
     ASTM G31's minimum of 0.20 mL of solution per mm² of specimen keeps a
     40 mL vial to small coupons.
   - **What it gives the search:** the metal released over time is an
     intermediate result between the one-hour screen and the 30-day mass
     loss, which is the "elapsed time as a fidelity" idea from the
     previous round.
5. **Scheduling.** The search can queue a screen like any other step.
   - **Overnight runs need a rule change:** they need the lab's
     human-present rule relaxed for this protocol, or a person on shift.

## What the literature says (two Edison queries)

Edison answered two LITERATURE questions:
[`ec-01-droplet-cell-screen.md`](../../edison-trajectories/cu-ded-elements-2026-10/electrochem/ec-01-droplet-cell-screen.md)
and [`ec-02-potentiostat-free.md`](../../edison-trajectories/cu-ded-elements-2026-10/electrochem/ec-02-potentiostat-free.md).
The DOIs named here were checked on Crossref.

- **Small cells rank well but shift absolute values.**
  - **Steel weld (da Cruz and Bertazzoli 2020, 10.1007/s11665-019-04531-z):**
    a 250 µm microcell kept the ranking of the weld zones, but gave about
    twice the corrosion current and half the polarization resistance of a
    larger cell, and a corrosion potential about 0.25 V different.
  - **Pure copper (Sakairi et al. 2010, 10.2355/isijinternational.50.1466):**
    the rest potential in a droplet cell differed from a macrocell by about
    100 mV.
  - **Matched footprints (Sur et al. 2023, 10.1149/1945-7111/aceeb8):**
    with a ~3 mm droplet cell against a conventional cell with an O-ring
    opening of the same size, the differences were minimal, in acid on
    non-copper alloys.
  - **The gap:** no paired small-cell versus flat-cell study exists for
    Cu-Ni, NAB or aluminum bronze in seawater. The cross-check below is
    therefore a small result of its own, not just a calibration.
- **Map across the fusion line, at about 0.5-1 mm.** Edison suggests
  0.5-1 mm apertures for reproducible ranking, and 100-250 µm only where the
  heat-affected zone is narrower. Two published cases show why this matters:
  - **90-10 Cu-Ni weld joints in flowing seawater (Xing et al. 2023,
    10.3390/met13020294):** the heat-affected zone was the least resistant
    region.
  - **Cast NAB (Ding et al. 2019, 10.3390/ma12020209):** β′ was attacked
    within an hour in 3.5% NaCl.

  A 3 mm well averages over a narrow zone, so the plan should include a
  smaller well for fusion-line spots, compared only with wells of its own
  size.
- **Throughput on one head.** From published timings (15 min open-circuit
  potential, about 2.5 min of impedance down to 0.1 Hz, about 5 min of
  linear polarization), one spot takes about 22.5 min, so at most about
  2.7 spots per hour before moving, filling and rinsing. Cyclic
  polarization and impedance down to 0.01 Hz are best kept for finalists.
  Low-frequency |Z| and linear polarization need not agree (Heyne et al.
  2026, 10.1007/s00216-026-06609-9), so one is not a stand-in for the other.
- **What a potentiostat-free tier can and cannot do (ec-02):**
  - **Open-circuit potential and photos are triage only.** On wire-arc
    Cu-30Ni (Song et al. 2024, already cited), the open-circuit potential
    barely changed between conditions while impedance film resistance
    ranged 0.68-1.66 × 10⁵ Ω.
  - **Dissolved Cu and Ni (ICP-MS, filtered and unfiltered aliquots) are a
    strong multi-day addition.** But no time-resolved dissolved-copper
    release rates for C70600 or C71500 were found; the often-quoted
    62 mg/m²/day is a weight-loss figure.
  - **Mass loss is barely detectable on small coupons:** 1 cm² at
    0.01-0.05 mm/yr loses only 0.07-0.37 mg in 30 days. Immersion coupons
    need several cm² of exposed area and a 0.01 mg balance.
  - **A deposit coupled to cast NAB or wrought Cu-Ni through a
    zero-resistance ammeter measures the galvanic current of a repair
    directly.** Separate tests cannot give it.
- **Cheap instruments.** ACEstat (an Army Corps of Engineers open design,
  about $60 in parts, 50 pA-3 mA, with impedance) matched an EmStat Pico on
  test redox chemistry (Brown et al. 2022, 10.1021/acs.analchem.1c04226).
  MYSTAT is DC-only (Irving et al. 2021, 10.1016/j.ohx.2020.e00163). None has
  been validated on copper alloys in seawater, so any low-cost unit needs
  the same-cell comparison against a benchtop instrument first.

## Risks and gaps

- **Small wells change some numbers.** Breakdown potentials depend on the
  area tested (Frankel 1998, doi:10.1149/1.1838615). Compare only wells of
  one size, and cross-check against a 1 cm² flat cell on the two references
  once per campaign.
- **CubOS needs four additions:** linear sweep, scan rates below 1 mV/s,
  reversal at a set current, and impedance. #278 lists the first three, and
  the EmStat's MethodSCRIPT supports all four. This is a Task 2 software
  item, and it can be tested against CubOS's simulation driver first.
- **One head.** The pipette, capper, cameras, reference and counter all
  share it, which limits reach and needs a layout check (#266 found about
  334 × 221 mm reachable).
- **Polishing is manual (#110),** so specimens arrive in batches.
- **The electrolyte is not seawater.** ASTM D1141 lacks the biofilm and
  sulfide chemistry of natural seawater, and welded NAB corroded more in
  natural than in simulated seawater (Dobson 2024b, already cited). That is
  why the proposal leaves flowing natural seawater to Navy laboratories.

## Recommendation

1. **Proposal text (done in this pass).**
   - **Task 2:** the screen now runs on the CubXL, with several wells per
     specimen, wells across the fusion line, ICP-MS of used electrolyte,
     and immersion vials sampled over time.
   - **Fields 10 and 11:** the CubXL is listed under equipment available.
2. **Budget (your call; the budget script is private).** Two options:
   - **(a)** Keep the $18,000 benchtop unit and flat cell, and add the CubXL
     cell parts.
   - **(b)** Buy an EmStat Pico (about $580 in #231; get a current quote)
     and the cell parts. PR #278 prices those parts at a few hundred
     dollars; the mini-reference is not yet priced. Borrow a benchtop unit
     (Dr. Porter's, or another BYU lab's) for the flat-cell cross-checks.
   - **What (b) changes:** it frees about $17,000, roughly what a few DED
     sessions cost, and moves the item from Equipment (Field 11) to
     Materials and supplies, since it is below the equipment threshold.
     Check BYU's threshold.
   - **Risk of (b):** reviewers may trust a module instrument less, which
     is why the cross-check is written into the plan.
3. **Before Oct 23 (optional).** If Dr. Porter's session next week has
   time, run linear polarization and impedance on any 70-30 Cu-Ni or NAB
   offcut (#286 is sourcing copper alloys). One curve each would be the
   first copper corrosion data in the preliminary results.
