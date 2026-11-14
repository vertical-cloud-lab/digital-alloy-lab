# SOP 01 (draft): DSC/DTA melting and freezing of atomized powder

**Checks:** liquidus, solidus, incipient melting, freezing range, fraction solid fs(T), latent
heat (Thermo-Calc equilibrium and Scheil; pycalphad with open databases, #238). Each alloy also
becomes ESPEI/ORCHID-style phase-boundary entries for systems with little data (Al–Si, Al–Mn–Cr–Zr,
Cu–Al–Ni–Fe). **Analysis:** [`../analysis/dsc_solidification.py`](../analysis/dsc_solidification.py),
then [`../analysis/espei_export.py`](../analysis/espei_export.py).
Draft for review; nothing here has been run on our instrument yet.

## Samples
- **Powder:** 10–25 mg of the 20–63 µm sieve cut from each atomizer run. Use a riffle-split
  sub-sample, not a scoop off the top. Run two replicates per alloy.
- **Printed or cast:** a chip of similar mass from a cube, or from the crucible remnant. Make it
  flat on one side for good contact. Clean it in ethanol and dry it.
- Record the run ID, sieve cut, storage humidity and days since atomization (#159 run record).

## Equipment and set-up
- A heat-flux DSC or DTA that reaches 750 °C for Al and 1150 °C for Cu alloys, with a high-purity Ar purge
  (≥ 99.999 %, about 50 mL/min). Pump down and backfill first if the cell allows it.
- **Alumina crucibles with lids. Never use platinum with aluminium**: molten Al alloys with Pt.
  Use alumina for the Cu alloys too.
- **Calibrate** temperature and enthalpy with pure-metal standards that bracket the range:
  - In (156.6 °C), Zn (419.5 °C) and Al (660.3 °C) for Al alloys;
  - Ag (961.8 °C) and Au (1064.2 °C) for Cu alloys.
- Fit the cell's time constant τ to the trailing edge of the Zn or Al standard peak
  (`estimate_tau`). Check it weekly and after any change of crucible type.

## Program (Al alloys; for Cu alloys shift all temperatures up by about 450 K)
1. Hold at 30 °C, then heat at 20 K/min to 450 °C.
2. **Heat 1** at β to 720 °C (β = 10 K/min), and hold 2 min.
3. Cool at β to 450 °C. Use this for undercooling and nucleation, not for the liquidus.
4. **Heat 2** at β to 720 °C. This is the solidified bead, closer to Scheil than the as-atomized powder.
5. Repeat on fresh powder at β = 5 and 20 K/min. Extrapolate onset and end temperatures to
   β → 0 (`extrapolate_to_zero_rate`).
6. Run an empty-crucible baseline with the same program each day, and subtract it.

Instrument time is about 2–2.5 h per run, so 3 rates per alloy fill a day. With an autosampler they run overnight.
Hands-on time is about 20 min per sample.

## Analysis
```bash
python ../analysis/dsc_solidification.py run.csv --mass-mg 15.2 --rate 10 --t1 520 --t2 680 \
    --baseline sigmoidal --tau 3.1 --model scheil_tc.csv --out out/S1_h2_10K
```
- **Solidus:** the extrapolated onset.
- **Liquidus:** the end of the peak (99.9 % of the partial area) after the lag correction.
- **Also report:** the 1 %/99 % temperatures, the latent heat (J/g), the Kou and CSC indices, and measured minus model ΔT at fs = 0.1–0.9.
- **Heat 1 vs Heat 2:** a lower onset on Heat 1 than on Heat 2 is incipient melting of segregated, rapidly solidified material.
- **Compare against:** Thermo-Calc (or pycalphad `scheil`) curves for the **measured** composition (SOP 05), not the nominal one.

## Acceptance
- **Al standard:** onset within ±0.5 K of 660.3 °C. Its heat of fusion should be close to the
  handbook 10.7 kJ/mol (~397 J/g); treat a gap of more than 3 % as a calibration problem.
- **Replicates:** onsets within 2 K of each other.
- **Mass:** loss over the run under 0.5 %. More than that means oxidation or evaporation (Mg, Zn).

## Open questions
- Which BYU DSC/DTA reaches 750 °C (1150 °C for Cu), and does it have an autosampler (see the README's access table)?
- Does the oxide shell on the powder distort Heat 1? Compare the powder with a chip of the same alloy.
- For multicomponent alloys, identify the primary phase (XRD/SEM of the DSC bead) before
  writing the ZPF entry.
