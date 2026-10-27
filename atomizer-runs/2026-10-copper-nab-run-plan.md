# First copper-alloy run on the rePOWDER: NAB in a BN-coated crucible

Status: **planned, not run.** Feedstock and crucible spray arrived Oct 23, 2026
([#117 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-6377115493)).
Sourcing is in #123 and #162. The copper/DED proposal that wants this powder is #117
(`near-term-submissions/onr-yip/onr-yip-technical-proposal-cu-ded.tex` on `claude/onr-yip-fy27`).

## What we have

| Item | McMaster part | Notes |
|---|---|---|
| C63000 nickel-aluminum bronze (NAB) rod, ASTM B150, 3/4" dia., 3 ft | [8203K41](https://www.mcmaster.com/8203K41/) | Cu-10Al-5Ni-3Fe, liquidus about 1,054 °C. Download the lot certificate from Order History. |
| Boron nitride spray, 13 oz aerosol | [10515K35](https://www.mcmaster.com/10515K35/) | Momentive "Boron Nitride Spray II". Dried BN rated to 1,800 °C in inert gas or vacuum (850 °C in air). |

Not on hand: oxygen-free copper (C10100, [8965K72](https://www.mcmaster.com/8965K72/)) and 90/10 Cu-Ni
(C70600, [4644N14](https://www.mcmaster.com/4644N14/)). The Oct 18 plan ran C10100 first because no
crucible was coated; the order that was approved has NAB and the spray instead, so **NAB is the first
run** and C10100 is not part of this plan.

## Set-up

From AMAZEMET's applications engineer (Oct 17 messages, after we named the two McMaster rods) and the
Sep 28–30 training:

| Setting | Value | Source |
|---|---|---|
| Crucible | Graphite, BN-sprayed, kept for copper only | "The addition of Nickel/Iron etc. can lead to high reactivity with the crucible. A coating would be preferred" |
| Nozzle | hBN, 0.5 mm bore, copper-only | "+ a HBN nozzle"; 0.5 mm is his pure-copper bore |
| Sealing rod | Alumina, copper-only | Kit item for reactive melts (training Video 9, 34:17). A graphite tip would sit in the Ni/Fe melt for the whole hold, and coating the rod can block the nozzle. |
| Plate | Carbon-fibre plate with the Mo-coated tip | "CFC nozzle with Mo coating", read as the plate: he showed it as the copper plate "where copper doesn't want to wet" (Video 9, 39:01). The W-coated CF plate is the alternative. |
| Booster | 1:1.5 | CF plates only work on 1:1.5. If the stack was reversed for the Mo aluminum runs, turn it back. |
| Amplitude | Slider 80–90 | As for the aluminum CF runs |
| Charge | Two or three 2.75" slugs, about 150 g each | Each slug must sit fully inside the crucible: copper above the coil is "extremely hard to melt" (Video 4, 5:02). |
| Setpoint | Open, see below | |
| Start-up | Pour more at the start, pulse the turbo pressure | "You may need to do a bit more pouring at the beginning to heat it up but after it wets, it will atomize continuously" |

**Setpoint.** NAB's liquidus is about 1,054 °C. The two published NAB-on-AMAZEMET runs and AMAZEMET's
CuSn8 runs all melted at about 1,300 °C:
Müller et al. 2023 ([10.1088/1757-899X/1296/1/012036](https://doi.org/10.1088/1757-899X/1296/1/012036)),
Uhlmann et al. 2024 ([10.3390/ma17143396](https://doi.org/10.3390/ma17143396)) and
Choma et al. 2026 ([10.3390/ma19132803](https://doi.org/10.3390/ma19132803)).
The manual gives 1,300 °C as the maximum working temperature; the current proposal text says the module
reaches 1,400 °C and is typically run up to 1,300 °C. Start near 1,200 °C (about 150 °C of superheat,
close to our 6063 runs) and raise toward 1,300 °C only if the melt won't wet the plate. Ask AMAZEMET to
confirm.

## Steps

**The day before**
1. Cut two or three 2.75" NAB slugs. Degrease them.
2. Clean the copper-only crucible. Spray a thin, even BN coat inside it **in a fume hood**, away from
   ignition sources, with gloves and goggles. The can is an extremely flammable aerosol, and its
   carrier contains methanol and MIBK. Store it in the flammables cabinet.
3. Let the coat dry overnight in the hood. **Never pour onto a wet coat.** The coat may gray on first
   heating as its organic binder burns off; that is normal.
4. Check the cabinet for the hBN nozzle (confirm the bore), the alumina sealing rod, and the Mo-tipped
   and W-coated CF plates. These come from the Sep 30 consumables tour and haven't been counted.

**Run day**
1. Fit the copper-only crucible, hBN nozzle and alumina rod; mount the Mo-tipped CF plate on 1:1.5.
2. Load the slugs fully inside the crucible.
3. Purge and melt under argon as for the aluminum runs. Record the HMI pressures; how Choma's
   0.2 bar backfill, 1.5 bar turbo and 0.6 bar atomizing pressures map onto our HMI is still open
   (#160).
4. Heat to the setpoint and hold until fully molten.
5. Pour. Expect spatter until the plate heats and wets; keep pouring and pulse the turbo.
6. Record on the stream camera, and log setpoint, hold time, pressures, amplitude, and the mass charged,
   collected and left in the crucible.

**After**
1. Weigh the powder and the skull.
2. Sieve into the DED cuts (45–105 µm and 100–200 µm are the cuts the Mines X2 uses) and report the
   fraction in each.
3. SEM images and a size distribution from them, as for the aluminum powder.
4. Look for stray carbon fibres in the SEM images (Uhlmann's bare CF plate shed them).
5. Send a sample for oxygen **and carbon**, to see whether the melt picked up carbon from the crucible.
6. Inspect the crucible coat, nozzle and plate tip, and photograph them.
7. Compare with Uhlmann 2024 (d10/d50/d90 = 48/98/174 µm at 40 kHz for CuAl10Ni5Fe5).

## Risks

- **Hottest run so far.** Aluminum runs were at 830–840 °C.
- **Plate wetting.** The Oct 2, 6 and 8 aluminum runs all went wrong where the melt meets the plate.
  Treat this run as a learning run; the 3 ft rod leaves stock for retries.
- **Cross-contamination.** Copper left in a shared crucible, nozzle or rod would show up in the aluminum
  repeatability runs (#160). Keep every copper part separate and labelled. A charge that freezes in the
  crucible can cast the sealing rod in place.
- **Consumables.** Coated plates wear out after a few runs, and Mo plates last about 4–6 runs while the
  aluminum series needs 12–15 (#160). Spares ship from Poland.
- **Binder silicon.** If NAB's aluminum reduces a silicate binder, the worst case (0.5 g of coat, all
  silica, all dissolved into 300 g) adds 0.08% Si; C63000 allows up to 0.25%.

## Open questions for AMAZEMET

1. Is "CFC nozzle with Mo coating" the CF plate with the Mo-coated tip? For NAB, that plate or the
   W-coated one?
2. What bore are the hBN nozzles in our kit?
3. Is the McMaster BN spray (Momentive Boron Nitride Spray II) acceptable, or which spray does AMAZEMET
   use? (The product link has been sent.)
4. What setpoint for NAB? Is 90/10 Cu-Ni (liquidus about 1,150 °C) OK at 1,250–1,300 °C?
5. How fast can more coated plates and hBN nozzles ship?

## Timing

The proposal's copper powder figure could only be swapped in until the research office submits on
Oct 28, so this run is now unlikely to make the submission; the draft's copper powder figure (still a placeholder) and the Mines
Cu-Ni tracks (#213, #217) cover it. The powder is still the first preliminary result for the copper
work after submission, and a first lot is milestone M1 in the proposal.
