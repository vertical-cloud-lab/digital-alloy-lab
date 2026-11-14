# SOP 04 (draft): fast property screen with Vickers hardness and eddy-current conductivity, as-built and through an aging series

**Checks:**
- yield strength: Thermo-Calc's General Model Library, and TC-PRISMA peak- and over-aged estimates;
- precipitation kinetics: TC-PRISMA, and TTP diagrams as times to peak hardness;
- electrical resistivity: Thermo-Calc's property model;
- solute left in solution after LPBF;
- an estimate of thermal conductivity, an AM Module input.

**Analysis:** [`../analysis/kinetics.py`](../analysis/kinetics.py) and
[`../analysis/conductivity.py`](../analysis/conductivity.py). Draft.

## Samples
- **Sections:** the polished XZ sections from SOP 03 (hardness), and flat coupons at least
  10 × 10 mm and at least 2 mm thick (conductivity). A 5 mm cube is too small for most eddy-current
  probes; use a small-diameter probe, or a four-point probe on the polished face.
- **Aging matrix for each candidate:**
  - as-built;
  - then 300, 350 and 400 °C for 0.25, 1, 4, 16 and 64 h, with a water quench.
  - For Sc/Zr/Er alloys add 250 °C.
  - That is 16 conditions. Use small coupons cut from one cube row, so the build history is shared.
- **Reference:** wrought 6063-T5/T6 and printed AlSi10Mg (and Scalmalloy-type if we have it), through the same matrix.

## Vickers hardness (ASTM E384)
- **Load:** HV0.5 or HV1, 10 s dwell, 10 indents per sample.
- **Spacing:** at least 2.5 diagonals from each other and from edges.
- **Tracks:** on a single track use HV0.05 inside the fusion zone (one indent per track).
- **Report:** mean ± SD. On an automated stage, map a line across the build height.
- **Strength:** σy ≈ HV/3 (Tabor) is only a screen; calibrate it on our own tensile bars (#255 finalists)
  before quoting MPa.
- **Time:** about 10 min per sample (manual); unattended with an auto-stage.

## Eddy-current conductivity (%IACS)
- **Calibration:** the meter's conductivity standards bracketing 25–60 %IACS, checked at the start of each session.
- **Temperature:** measure at 20 ± 1 °C, or record the temperature and correct it
  (`conductivity.py iacs --T --slope`). Record whether the meter's own compensation was on.
- **Frequency:** pick one whose penetration depth is well under the coupon thickness (see the meter's table).
  Use 3 readings per face.
- **Thermal conductivity:** on 3–4 alloys spanning the range, measure k by laser flash
  (k = α·ρ·c_p). Fit the Smith–Palmer constants (`fit_smith_palmer`), then estimate k for
  everything else from %IACS.
- **Time:** about 2 min per sample.

## Analysis
- **Aging curves:** HV(t) and ρ(t) at each temperature.
  - Time to peak gives an Arrhenius Q (`arrhenius`).
  - The fraction transformed from resistivity, f = (ρ0 − ρ)/(ρ0 − ρ∞), fitted with JMAK, gives n and k(T).
- **Compare with TC-PRISMA** for the measured composition:
  - predicted yield strength vs time, peak time vs temperature;
  - the matrix solute (resistivity drop) vs the predicted matrix composition.
- **Resistivity vs Thermo-Calc:** compare the as-built and fully aged resistivity with Thermo-Calc's
  electrical resistivity of the predicted phase assemblage.

## Acceptance
- Hardness SD under 5 % on dense material.
- Conductivity repeat readings within 0.3 %IACS.
- The reference alloys reproduce their known temper response: a 6063 peak near the T6 schedule.

## Open questions
- Is there an eddy-current meter on campus, for example in an NDE or aerospace lab? If not, a used
  handheld unit is the cheapest high-throughput instrument on the list.
- Furnace capacity for 16 conditions per alloy: batch by temperature.
