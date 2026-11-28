# SOP 04, animated: hardness, eddy-current conductivity and an aging series (#262, PR #263)

Script: `sop04_aging.py`. It renders six chapters, `sop04_c1` … `sop04_c6`, each its own render; `python
sop04_aging.py join` builds the joined video. Outputs:

- `out/mp4/sop04.mp4` and `out/sop04.json`;
- `out/sop04_steps.jpg` (the last frame of every sub-step);
- `out/sop04_preview.gif`.

Each chapter also writes a collision audit, `out/collisions/sop04_c*.json`. All data on screen are synthetic
examples, computed with `../analysis/kinetics.py` and `../analysis/conductivity.py`. Panels that only compute
from given inputs (the depth table, the temperature correction, Tabor) are badged "computed". The TC-PRISMA
comparison is badged as a synthetic stand-in.

## Models

| Key | What | Notes |
|---|---|---|
| `eddy_meter` | Foerster SIGMATEST 2.070, its probe (8 mm head) and two standards | `notes/eddy_meter.md`; registered to Foerster's video and photo |
| `laser_flash` | NETZSCH LFA 717 HyperFlash, at the contract lab | `notes/laser_flash.md`; registered to NETZSCH's video (width estimated; no published size) |
| `aging_rack`, `tongs`, `quench_bath`, `lab_timer`, `tc_reader` | the aging station | `notes/aging_rack.md` |
| `furnace_hinged` | byu-vcl's Nabertherm NAT 15/65 with hinges that don't pass through the door | `notes/aging_rack.md` |
| `hv_manual` | byu-vcl's Mitutoyo HM-220, with a hand-loaded stage | `notes/aging_rack.md` |

## Every SOP line, and where it is shown

The times are in the joined video, from `out/sop04.json`; the table at the end lists every sub-step.

| SOP line | Shown in |
|---|---|
| Checks: yield strength, precipitation kinetics, resistivity, solute in solution, thermal conductivity | c1, the opening card ("Checks") |
| Analysis scripts: kinetics.py, conductivity.py | c6 card; every data panel names the function it uses |
| Samples: polished XZ sections from SOP 03 (hardness) | c1 "Samples" (three 38 mm conductive mounts); c3 "Load" (the section goes on the HM-220) |
| Samples: flat coupons ≥ 10 × 10 mm, ≥ 2 mm (conductivity) | c1 "Samples"; c4 "Samples" |
| A 5 mm cube is too small for most probes: a small probe, or a four-point probe on the polished face | c1 "Samples" (cube beside a coupon); c4 "Samples" (the 8 mm head's footprint on each) |
| Aging matrix: as-built; 300, 350, 400 °C × 0.25, 1, 4, 16, 64 h, water quench; 250 °C for Sc/Zr/Er; 16 conditions | c1 matrix panel; c2: batches by temperature, every quench, the matrix filling |
| Small coupons cut from one cube row, so the build history is shared | c1 "Samples" (the cube row, then three 3 mm coupons per cube) |
| References: 6063-T5/T6, printed AlSi10Mg, Scalmalloy-type, through the same matrix | c1 "Reference"; c2 (one coupon of each on every boat) |
| Vickers load HV0.5 or HV1, 10 s dwell, 10 indents per sample | c3 card; "Load" (AVPAK settings); "Indent" (dwell gauge); "Spacing" (ten indents) |
| Spacing ≥ 2.5 diagonals from each other and from edges | c3 "Spacing" (to-scale panel, d = 86 µm) |
| Single tracks: HV0.05 inside the fusion zone, one indent per track | c3 "Tracks" (to-scale panel) |
| Report mean ± SD; on an automated stage, a line across the build height | c3 "Report" (ten values, mean ± SD); "Report" (auto-stage line map) |
| Tabor σy ≈ HV/3 only as a screen; calibrate on #255 tensile bars | c3 "Strength" (H = 9.807 × HV in MPa, then H/3) |
| Time: about 10 min per sample manual; unattended with an auto-stage | c3 "Time" |
| Eddy current: standards bracketing 25–60 %IACS, checked at the start of each session | c4 "Calibration" (≈ 26 and ≈ 59 %IACS discs, the meter's screen) |
| Measure at 20 ± 1 °C or record T and correct (`conductivity.py iacs --T --slope`); record the meter's compensation | c4 "Temperature" (room thermometer; the compensation gauge; the CLI run, computed) |
| Frequency: penetration depth well under the thickness; 3 readings per face | c4 "Frequency" (δ table, computed); "Measure" (three readings, coupon turned, three more) |
| Thermal conductivity: laser flash on 3–4 alloys, k = α·ρ·cp, Smith–Palmer fit, then k from %IACS | c5 (discs, graphite, the contract lab's LFA 717, the flash cutaway, thermogram, k, `fit_smith_palmer`, k from %IACS) |
| Time: about 2 min per sample (eddy current) | c4 "Time" |
| Analysis: HV(t) and ρ(t) at each temperature; time to peak → Arrhenius Q | c6 "Analysis" (curves; `arrhenius`) |
| f = (ρ0 − ρ)/(ρ0 − ρ∞) with JMAK → n, k(T) | c6 "Analysis" (`aging_fraction`, `fit_jmak`) |
| Compare with TC-PRISMA; resistivity vs Thermo-Calc's model | c6 "Analysis" (synthetic stand-in, badged; parity plot) |
| Acceptance: HV SD < 5 %; repeats within 0.3 %IACS; 6063 peaks near T6 | c3 "Report" (SD 1.3 %); c4 "Acceptance" (0.13 %IACS); c6 "Acceptance" card |
| Open questions: an eddy-current meter on campus? a used handheld unit; furnace capacity: batch by temperature | c4 "Open question"; c2 "Open question"; c6 "Open questions" card |

## Added from Edison, or left out, and why

These follow Edison's answer (v3, `edison/v3-hardness-eddy-icp-onh/answer.md`) and NETZSCH's notes:

- **Aging practice:**
  - The furnace is preheated empty.
  - A check thermocouple sits beside the coupons, and the clock starts only when it is back at set point.
  - Coupons come out with tongs, in heat-resistant gloves.
- **Vickers:** focus with the 10x objective, indent, then measure with the 50x (Edison: 40x).
- **Eddy current:** 100 %IACS = 58 MS/m, and δ = 1/√(π f μ σ).
- **Laser flash:** graphite on both faces, thin. That last point is from NETZSCH's notes.

Flagged, not changed:

- **Air cooling vs the SOP's quench.** Edison notes that published direct aging of Scalmalloy usually air-cools.
  SOP 04 asks for a water quench at every time point, and the animation follows the SOP.
- **6063 at 300–400 °C peaks too early.** Its peak comes within minutes, before the first 0.25 h point, so the
  acceptance check "6063 peaks near the T6 schedule" can't be read off this matrix. It needs a 175–200 °C point
  for 6063, or the Arrhenius line extrapolated to the T6 temperature. The animation states the criterion as the
  SOP does.

Simplified:

- **Cutting.** The cube row is shown before and after cutting, as a cut in time. The wire EDM or saw is SOP 03's
  equipment.
- **Four-point probe.** Mentioned, not drawn.
- **Later batches.** The 4, 16 and 64 h quenches and the 350, 400 and 250 °C batches are shown as cuts (the
  matrix fills). Only 0.25 h and 1 h are animated in full.
