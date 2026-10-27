# First copper-alloy run on the rePOWDER: 630 bronze in a BN-coated crucible

Status: **planned, not run.** Feedstock and crucible spray arrived Oct 23, 2026
([#117 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/117#issuecomment-6377115493)).
Sourcing is in #123 and #162. The copper/DED proposal that wants this powder is #117
(`near-term-submissions/onr-yip/onr-yip-technical-proposal-cu-ded.tex` on `claude/onr-yip-fy27`).

## What we have

| Item | McMaster part | Notes |
|---|---|---|
| 630 bronze rod (UNS C63000), ASTM B150, temper HR50, 3/4" dia., 3 ft | [8203K41](https://www.mcmaster.com/8203K41-8203K412/) (3 ft) | McMaster: "Also known as nickel aluminum bronze." Download the lot certificate from Order History. |
| Boron nitride spray, 13 oz aerosol | [10515K35](https://www.mcmaster.com/10515K35/) | Momentive "Boron Nitride Spray II". Dried BN rated to 1,800 °C in inert gas or vacuum (850 °C in air). |

**What 630 bronze is.** UNS C63000, a wrought nickel-aluminum bronze. From
[Concast's data sheet](https://www.concast.com/c63000.php) (AMS 4640 limits, CDA physical properties):
- **Composition:** nominally Cu-10Al-5Ni-3Fe, within Al 9–11, Ni 4–5.5, Fe 2–4, Mn ≤ 1.5 and
  Si ≤ 0.25 wt%. McMaster's page gives the same.
- **Melting:** solidus 1,035 °C, liquidus 1,054 °C. McMaster lists a single "melting point" of
  1,913 °F (1,045 °C), the middle of that range, so superheat here is counted from the liquidus.
- **Slug mass:** at 7.58 g/cm³, a 2.75" slug of the 3/4" rod is about 150 g.
- **Not the proposal's NAB:** the copper proposal's "NAB" is cast C95800 (Cu-9.2Al-4.5Ni-4Fe-1.2Mn,
  liquidus about 1,060 °C), and the published NAB runs below atomized chips from cast propellers. The
  chemistries are close, so those runs are still the nearest comparison.

Not on hand: oxygen-free copper (C10100, [8965K72](https://www.mcmaster.com/8965K72/)) and 90/10 Cu-Ni
(C70600, [4644N14](https://www.mcmaster.com/4644N14/)). The Oct 18 plan ran C10100 first because no
crucible was coated. The order that was approved has the 630 bronze and the spray instead, so
**630 bronze is the first run** and C10100 is not part of this plan.

## Set-up

From AMAZEMET's applications engineer (Oct 17 messages, from just before and after we named the two
McMaster rods) and the Sep 28–30 training:

| Setting | Value | Source |
|---|---|---|
| Crucible | Graphite, BN-sprayed, kept for copper only | "The addition of Nickel/Iron etc. can lead to high reactivity with the crucible. A coating would be preferred" |
| Nozzle | hBN, 0.5 mm bore, copper-only | "+ a HBN nozzle"; 0.5 mm is his pure-copper bore |
| Sealing rod | Alumina, copper-only | Kit item for reactive melts (training Video 9, 34:17). A graphite tip would sit in the Ni/Fe melt for the whole hold, and coating the rod can block the nozzle. |
| Plate | Carbon-fibre plate with the Mo-coated tip, unless AMAZEMET says the W-coated one (question 1) | "CFC nozzle with Mo coating", read as the plate: he showed it as the copper plate "where copper doesn't want to wet" (Video 9, 39:01). But he said it in answer to "Will it be pure copper?", before we named the rods, and in the same tour he listed the W plasma-coated CF plate for Cu alloys, as the one that survives anything (Video 9, 38:35). AMAZEMET's CuSn8 study rated its W-based coating the best balanced and its Mo-based one a relevant alternative (Choma 2026). |
| Booster | 1:1.5 | CF plates only work on 1:1.5. If the stack was reversed for the Mo aluminum runs, turn it back. |
| Amplitude | Slider 80–90 | As for the aluminum CF runs |
| Charge | Two or three 2.75" slugs, about 150 g each | Each slug must sit fully inside the crucible: copper above the coil is "extremely hard to melt" (Video 4, 5:02). Three slugs (450 g) are over the SOP's 250–300 g per charge (Video 9, 29:05), but that figure was for aluminum: they take up about 60 cm³, a bit over half the volume of an aluminum charge, and AMAZEMET's CuSn8 runs used about 500 g (Choma 2026). |
| Setpoint | 1,300 °C | The published NAB and CuSn8 runs on this atomizer; see below |
| Hold | Once fully liquid, 2 min and no longer | The thermocouple reads the crucible wall, which lags the melt by 2 min; a longer hold only adds oxidation (Video 5, 57:22–58:43) and, here, time for Ni and Fe to react with the crucible |
| Start-up | Pour more at the start, pulse the turbo pressure | "You may need to do a bit more pouring at the beginning to heat it up but after it wets, it will atomize continuously" |
| Splash guard | More than the single splash plate used for aluminum | Hot metals such as copper splash when atomization goes wrong (Video 5, 02:21–02:47). The extended pack also has a splash cover for spitting materials (Sep 28 phone video, 12:25). |

**Setpoint: 1,300 °C.** That is about 250 °C above 630 bronze's 1,054 °C liquidus, and it is the
temperature the two published NAB-on-AMAZEMET runs and AMAZEMET's CuSn8 runs all melted at:
Müller et al. 2023 ([10.1088/1757-899X/1296/1/012036](https://doi.org/10.1088/1757-899X/1296/1/012036)),
Uhlmann et al. 2024 ([10.3390/ma17143396](https://doi.org/10.3390/ma17143396)) and
Choma et al. 2026 ([10.3390/ma19132803](https://doi.org/10.3390/ma19132803)).
The bronze's aluminum forms a tough alumina skin, so the extra superheat helps the melt flow through the
0.5 mm bore and stay liquid long enough to wet a cold plate. The manual gives 1,300 °C as the maximum
working temperature, which is also the rating of the furnace's type N thermocouple (Video 1, 34:11;
the proposal text says the module reaches 1,400 °C and is typically run up to 1,300 °C), so there is
no headroom above it: do not exceed 1,300 °C, and if the melt freezes in the nozzle, fix the start-up
(more pouring, turbo pulses) rather than the temperature. If AMAZEMET recommends a lower setpoint,
1,200–1,250 °C still leaves 150–200 °C of superheat.

## What else is different from the aluminum runs

- **Glare.** At 1,300 °C the melt is too bright to watch without a filter or shaded glasses
  (Video 5, 54:24), and someone watches the window for the whole pour.
- **The thermocouple runs at its rating.** Its thin ceramic cover cracks in normal use (Video 1,
  35:49). If the thermocouple fails, the HMI shows "master temperature sensor", and any displayed error
  stops the heating at once (Video 1, 17:49 and 38:06), so a failure with the charge molten would
  freeze it around the sealing rod. The kit has two spare thermocouples (Video 9, 35:18).
- **No hotter melt-down setpoint.** The aluminum runs melt at 850–1,000 °C, then drop to 780–800 °C
  to pour. Here the pour setpoint is already the maximum, so the charge melts at 1,300 °C.
  AMAZEMET's CuSn8 charges of about 500 g took 6–6.5 min of heating to become fully fluid
  (Choma 2026).
- **Metal vapour.** The trainer called pure copper hard partly because of evaporation, which leaves
  no view through the viewport (Video 9, 48:36). Copper itself evaporates a little at 1,300 °C, and
  630 bronze's most volatile elements are Mn (up to 1.5%) and Zn (up to 0.30%); the lot certificate
  gives the actual values. Melting under argon, as in the aluminum runs, slows evaporation; Choma's
  near-vacuum melt (0.006 bar) would speed it up. Expect a film on the viewport and dust in the
  furnace's brass pre-filter and in the filters between chamber and pump, which stay clean unless
  something evaporates (Video 1, 38:53; Video 9, 37:40). That dust is why a used HEPA filter goes in a
  sand tray (Video 1, 08:51).
- **A glowing plate is normal.** With copper or brass, the CF plate glows orange and can take it
  (Video 5, 71:01).
- **Finer powder.** Denser melts give smaller particles on the same plate and booster (Video 3, 18:34),
  so expect finer powder than aluminum gives at the same settings.
- **Contamination only matters one way.** Aluminum carried into the bronze does no harm (630 bronze is
  9–11% Al), but copper, nickel or iron carried into the 6063 runs does: 6063 allows at most 0.10% Cu
  and 0.35% Fe. So the full material-change clean (vacuum, wipe, scrape, and the powder container;
  about 1 h, Video 5, 67:38) matters most after this run, before the next 6063 run. Clean before it
  too, so leftover 6063 powder doesn't end up in the bronze's size distribution.
- **Longer cooldown.** The chamber opens at or below 400 °C (Video 2, 33:16), and the furnace has
  900 °C to lose instead of about 400 °C.
- **Nickel.** The powder is about 5% nickel, a skin sensitizer and an inhalation hazard as dust, so
  keep to the SOP's respirator and gloves for every powder step.

## Steps

**The day before**
1. Cut two or three 2.75" slugs from the 630 bronze rod. It is much harder than 6063 (HB 187–241 in
   this temper), so saw slowly with coolant, then deburr and degrease. Keep an offcut as the oxygen and
   carbon baseline (After, step 5).
2. Clean the copper-only crucible. Spray a thin, even BN coat inside it **in a fume hood**, away from
   ignition sources, with gloves and goggles. The can is an extremely flammable aerosol, and its
   carrier contains methanol and MIBK. Store it in the flammables cabinet.
3. Let the coat dry overnight in the hood. **Never pour onto a wet coat.** The coat may gray on first
   heating as its organic binder burns off; that is normal.
4. Check the cabinet for the hBN nozzle (confirm the bore), the alumina sealing rod, the Mo-tipped
   and W-coated CF plates, and the spare thermocouples. These come from the Sep 30 consumables tour and
   haven't been counted.
5. If the last run was 6063, do the material-change clean. Check the W-alloy top sonotrode for the
   aluminum build-up noted on Oct 2; one of the kit's spare top sonotrodes (Video 9, 37:25) could
   become the copper one.
6. Put a filter or shaded glasses for the window, a spare thermocouple and the extra splash guard by
   the machine.

**Run day**
1. Look through the hBN nozzle for light, then fit the copper-only crucible, nozzle and alumina rod.
   Mount the plate on 1:1.5 and fit the extra splash guard.
2. Before heating, check where the stream will land (a laser down the nozzle, or with the door open)
   and mark the stack position. This is the G0 check from the aluminum runs plan (#160); the Oct 2, 6
   and 8 runs all went wrong there.
3. Load the slugs fully inside the crucible.
4. Purge and melt under argon as for the aluminum runs, not under vacuum. Record the HMI pressures;
   how Choma's 0.2 bar backfill, 1.5 bar turbo and 0.6 bar atomizing pressures map onto our HMI is
   still open (#160). The fresh coat may give off its binder as it heats, so if O₂ is still above
   100 ppm after the 500 °C wash, do the fourth wash the SOP allows.
5. Heat to 1,300 °C. Once the charge is fully liquid, wait 2 min and no longer.
6. Pour: vibration on before the sealing rod goes up (the Oct 6 lesson), then draining pressure, rod
   up and turbo. Expect spatter until the plate heats and wets; keep pouring and pulse the turbo.
7. Record on the stream camera from before the rod goes up until the stream stops. Log the setpoint,
   time to melt, hold time, pressures, amplitude, O₂ when the rod goes up, and the mass charged,
   collected and left in the crucible.

**After**
1. Open the chamber at or below 400 °C, which takes longer than after aluminum. Weigh the powder and
   the skull.
2. Sieve into the DED cuts (45–105 µm and 100–200 µm are the cuts the Mines X2 uses) and report the
   fraction in each.
3. SEM images and a size distribution from them, as for the aluminum powder.
4. Look for stray carbon fibres in the SEM images (Uhlmann's bare CF plate shed them).
5. Send a powder sample and the rod offcut for oxygen **and carbon**, to see whether the melt picked up
   carbon from the crucible. The lot certificate is unlikely to give either, since C63000's
   specification doesn't limit them.
6. Inspect the crucible coat, nozzle and plate tip, and photograph them. Wipe the viewport, and check
   the brass pre-filter and the filters between chamber and pump.
7. Do the material-change clean before the next 6063 run.
8. Compare with Uhlmann 2024 (d10/d50/d90 = 48/98/174 µm at 40 kHz for CuAl10Ni5Fe5 propeller chips).

## Risks

- **Hottest run so far, at the manual's maximum.** Aluminum runs were at 830–840 °C; this one is
  at 1,300 °C. Watch the heater power and the temperature overshoot on the way up. The thermocouple is
  at its rating, and if it fails the heating stops (see above).
- **Plate wetting.** The Oct 2, 6 and 8 aluminum runs all went wrong where the melt meets the plate.
  Treat this run as a learning run; the 3 ft rod makes about 12 slugs, so there is stock for retries.
- **Cross-contamination.** Copper, nickel or iron left in a shared crucible, nozzle, rod or chamber
  would show up in the aluminum repeatability runs (#160). Keep every copper part separate and
  labelled. A charge that freezes in the crucible can cast the sealing rod in place.
- **Consumables.** Coated plates wear out after a few runs, and Mo plates last about 4–6 runs while the
  aluminum series needs 12–15 (#160). Spares ship from Poland.
- **Binder silicon.** If the bronze's aluminum reduces a silicate binder, the worst case (0.5 g of coat,
  all silica, all dissolved into 300 g) adds 0.08% Si; 630 bronze allows up to 0.25%.

## Open questions for AMAZEMET

1. Is "CFC nozzle with Mo coating" the CF plate with the Mo-coated tip? You suggested it before we
   said the rod was bronze, and in the Sep 30 tour you listed the W-coated CF plate for Cu alloys. For
   630 bronze, which?
2. What bore are the hBN nozzles in our kit?
3. Is the McMaster BN spray (Momentive Boron Nitride Spray II) acceptable, or which spray does AMAZEMET
   use? (The product link has been sent.)
4. Is 1,300 °C right for 630 bronze (liquidus 1,054 °C), or would you go lower? Is 90/10 Cu-Ni
   (liquidus about 1,150 °C) OK at 1,250–1,300 °C?
5. How fast can more coated plates and hBN nozzles ship?
6. Anything to change for a run at 1,300 °C? In particular: a heat ramp for the alumina rod (program
   setup allows one for ceramics, Video 1, 33:03); the denser blue insulation (Video 9, 33:04); a last
   gas wash hotter than 500 °C to clear the fresh coat's binder, since the bronze stays solid to
   1,035 °C; and what to do if the thermocouple fails with the charge molten.

## Timing

The proposal's copper powder figure could only be swapped in until the research office submits on
Oct 28, so this run is now unlikely to make the submission; the draft's copper powder figure (still a placeholder) and the Mines
Cu-Ni tracks (#213, #217) cover it. The powder is still the first preliminary result for the copper
work after submission, and a first lot is milestone M1 in the proposal.
