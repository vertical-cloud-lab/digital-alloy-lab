# bofn-clocked: the model and its assumptions

**Everything here is synthetic.** The truth is invented, the instruments are noise models, and the durations,
capacities and prices are assumptions. Where an assumption has a source, the source is given; where it doesn't, it
says "assumed". Partner prices in this table are not quotes.

## The truth

bofn-prelim's alloy network ([`../bofn-prelim/bofn_alloy.py`](../bofn-prelim/bofn_alloy.py), `AlloyTruth`), ported
to numpy node for node in [`truth.py`](truth.py). `tests/test_clocked.py` checks the port against the original to
1e-12 on 2,000 random designs at `kappa` = 0, 0.5 and 1.

| Node | Inputs | Notes |
|---|---|---|
| CALPHAD: strengthening phase `s`, freezing range `f`, nucleant `g` | composition (Zn+Mg, Cu, Zr, Sc) | exact; every policy gets the same 256 compositions at day 0 ($10 each, instant), the set tiered screening uses |
| powder quality `q` | atomizer setting, `g`, route | gas-atomized powder: 0.97 − 0.04 `g` whatever the setting (assumed) |
| dense, crack-free fraction `rho` | laser power, scan speed, `f`, `g`, `q`, machine, route | bofn-prelim's ridge and crack model; the partner's machine shifts the ridge by −0.05 and reads +0.01 denser, gas powder shifts it by +0.06 (assumed) |
| strength index `U` | `s`, `rho` | bofn-prelim's |
| log corrosion rate | composition, `rho` | new: 0.55 Zn+Mg + 1.7 Cu − 0.5 Zr − 0.3 Sc + 3 (1 − `rho`); an alloy passes at ≤ 0.95. Cu hurts and porosity hurts, as in 2xxx/7xxx alloys; the numbers are invented |
| objective | `U` − λ × mineral burden | bofn-prelim's; λ = 0.3 except in the time machine |

At `kappa = 1` the corrosion limit cuts 71 % of the designs within 60 % of the optimum (39 % at `kappa = 0`), but
barely moves the optimum (0.6937 against 0.6945 unconstrained). The CALPHAD screen's region (freezing-range index
≤ 0.25) tops out at 70 % of the constrained optimum at `kappa = 1` and 99 % at `kappa = 0` ([`optima.json`](optima.json)).

## Noise and failures (all assumed)

| What | Value |
|---|---|
| Powder-quality reading | σ = 0.02 |
| Build-to-build density offset (physical, the whole build) | σ = 0.015 |
| Coupon density reading | σ = 0.015 |
| Bar-to-bar scatter of the strength index | σ = 0.025 (about 4 % of a good alloy's) |
| An ultrasonic run yields no usable powder | 10 % |
| A gas-atomized or custom lot fails | 2 % |
| A build fails outright | 8 % |
| A bar breaks invalidly | 3 % (a coupon has 3 bars, so it then can't be claimed) |
| Immersion readings (estimate of ln rate) | day 1: σ 0.45, day 3: 0.32, day 7: 0.20, day 14: 0.12, day 30: 0.04; early readings carry the coupon's own film-growth factor |
| Calibration drift between campaigns (time machine) | density and strength readings each offset by N(0, 0.03) per campaign |

## Stations and routes

| Station or route | Capacity and timing | Cost | Source |
|---|---|---|---|
| Ultrasonic atomizer, automated lab | 1; starts 08:00, 10:30, 13:00 Mon-Fri and 09:00 Sat (16 a week); 2.5 h a run; lot ready a day later | $1,500 a run; a lot feeds 2 builds | starts and run time: byu-vcl round 3's capacity table (FLAIME App. 2); cost: bofn-prelim (the abstract's); lot size assumed |
| Ultrasonic atomizer, today's lab | one run a day Mon-Thu at 08:00 | as above | DAL #256's schedule, as encoded in byu-vcl's `facility.py` (`DAL256`) |
| Custom powder lots from an outside supplier (conventional) | lead time lognormal, median 42 days, GSD 1.3 | $6,000 a lot; enough for every build | assumed, to match the Genesis draft's 8-32-week conventional cycle ([L1048-L1050](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/8098afb597f6fa5233e8c63527a6c4d560f8a0ed/genesis-mission-proposal/flaime-genesis-proposal.tex#L1048-L1050)) |
| Outside gas atomization (the role Valimet has in FLAIME's plan) | 30-day booking lead, 21-day turnaround, one run a month, ≥ 50 kg | $20,000 a lot (assumed, not a quote) | timing: byu-vcl round 3's assumption for this route |
| In-house LPBF (PR 318's Aconity MIDI) | 1, round the clock; 5 h a build + 3 h to cool, depowder and check density | $500 a build, marginal | 5 h: byu-vcl (PR 318 `timelapse.py`); post time and cost assumed |
| Partner LPBF (Utah core facility) | ≤ 3 builds a week, 7-day booking lead, results 2 days after | $2,500 a build | timing: byu-vcl round 3's capacity table; cost: bofn-prelim |
| Coupons per build | 6 laser settings, each a density cube, 3 bars and a corrosion coupon | | assumed |
| Bars, automated lab | wire EDM and 2 frames in house, round the clock, 0.75 h a job | $50 a bar | PR 318 via byu-vcl; cost assumed |
| Bars, conventional and today's lab | outside EDM (7 days), then the frame on the day shift (Thursdays only in `conv_atomizer`, as DAL #256 plans) | $200 a bar | byu-vcl `facility.py` (EDM service, DAL #256); cost: bofn-prelim |
| Immersion | 24 positions, 30 days; readings at days 1, 3, 7, 14 (automated lab acts on them; conventional doesn't) | $100 a coupon | positions and days: byu-vcl rounds 1-3; cost assumed |
| CALPHAD | 256 compositions at day 0, then $10 for any new one | $10 | bofn-prelim |

Money is marginal: capital (the atomizer, the printer, robots, the lab build-out) and people's time are outside it.
Budget: $250k a campaign. Horizons: 1 year for the automated lab, 4 years for the conventional baselines.

## Decisions

- **Automated lab**: asynchronous. The policy is asked for a ranked list of actions whenever results come back (at
  most every 6 h) and at 08:00 every day; the lab admits each action whose first step can start within 12 h of the
  earliest time its booking lead allows, while money lasts. Every automated policy holds itself to the same batch:
  at most 3 powders made but not yet printed and 4 builds whose first bar isn't back (a lot left unprinted for two
  days stops counting).
- **Conventional**: rounds of 4 builds, decided at Monday 09:00 meetings once the previous round's bars are back
  (immersions run on in the background); three bars from each build's densest coupon; immersion when those bars
  could beat the claim; no interim actions.

Shared finishing rules for every automated policy (model-free, so the comparison is about what each policy makes and
prints): one bar on each build's densest coupon and on its second densest if that is ≥ 0.5 dense; for the six best
tested coupons that could beat the claim and aren't failing corrosion, the remaining bars and an immersion, in
parallel; stop an immersion when its latest reading says P(pass) < 5 %, or when the coupon, fully tested, can no
longer beat the claim.

## Discovery and targets

- A **claim** is a coupon with ≥ 3 valid bars and a passed 30-day immersion. The campaign claims the one with the
  highest measured objective; its value is the true objective of that design if it truly passes corrosion, else 0.
- **T1 = 60 %** and **T2 = 80 %** of the constrained optimum (pre-registered; see the pre-registration for why).
- **Confirmation** (E2b): the same claim rule on a gas-atomized lot printed on the partner's machine (T1c, T2c).

## Shared with byu-vcl's twin round 3, and what's left out

[byu-vcl PR 394](https://github.com/vertical-cloud-lab/byu-vcl/pull/394) (branch `claude/twin-round3-20261126`, read
at `f1606a9`) is the facility-level model. This benchmark takes its numbers where the two overlap and leaves the
facility out:

- **Shared:** the atomizer's start slots and run time; the partner printer's weekly cap, booking lead and turnaround;
  the in-house printer's 5 h build; the outside EDM's 7 days; DAL #256's schedule for today's lab; 24 immersion
  positions and interim readings at days 1, 3, 7 and 14 with a stop action; the outside gas-atomization route's lead
  and cadence; pending work handled by keeping new designs away from designs in flight (round 3's kriging believer
  by exclusion); stop decisions by the value of finishing over the claim, not by KG; tiered screening's funnel moving
  down its own ranking; pKGFN's bundles (powder with its first print) and its EI-per-cost fallback when every KG is
  flat.
- **Left out on purpose:** robots and people as resources, two campaigns sharing the atomizer, breakdowns,
  changeovers, a spending plan, instrument simulators, the copper campaign. One aluminium-like campaign at a time.
