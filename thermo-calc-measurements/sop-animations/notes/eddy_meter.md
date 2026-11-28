# Eddy-current conductivity meter: Foerster SIGMATEST 2.070 (`eddy_meter`, models_props.py)

README §5.1 names two meters, the Foerster SIGMATEST 2.070 and the Fischer SIGMASCOPE SMP350.
The SIGMATEST is modelled because it is better documented:

- Foerster's datasheet gives the housing (211 × 102 × 40 mm, 0.62 kg).
- Foerster's own setup video shows the meter from above and at an angle, and the probe on a two-disc standard.
- The SMP350 is also dimensioned in its manual (170 × 89 × 40 mm, 395 g). Its only real footage is amateur and
  top-down, though, and the FS40 probe's diameter appears only in a third-party copy of Fischer's data sheet.

## Sources

| Figure | Value | Source |
|---|---|---|
| Housing (H × W × D) | 211 × 102 × 40 mm, 0.62 kg | [SIGMATEST datasheet](https://www.foerstergroup.com/web2print/en/mobile-testing/SIGMATEST.pdf) p.3 |
| Frequencies | 60 / 120 / 240 / 480 / 960 kHz | datasheet p.3 |
| Range | 0.5–65 MS/m (1–112 %IACS) | datasheet p.3 |
| Accuracy | ±0.7 % of reading (60 kHz, 14 mm probe); resolution 0.1 % | datasheet p.3 |
| Lift-off compensation | automatic, to 750 µm | datasheet p.2–3 |
| Temperature | readings normalised to 20 °C from the probe's built-in sensor (or an external one) | datasheet p.1 |
| Probes | heads 5, 8 and 14 mm; straight, angled, flexible | [SIGMATEST PROBES](https://www.foerstergroup.com/web2print/en/mobile-testing/SIGMATEST%20PROBES.pdf) p.1–2 |
| Minimum flat area | the shielded 14 mm probe reads a 14 mm bar's end face | [SIGMATEST 2.069 manual](https://www.bergeng.com/mm5/downloads/foerster/Foerster-Sigmatest-2.069-Operating-Manual.pdf) p.65 |
| Minimum thickness | 3δ, δ [mm] = 503 / √(σ [MS/m] · f [Hz]) | 2.069 manual p.62 |
| Standards | NPL-traceable discs in a black stadium-shaped carrier (pictured: Cu 59.34 MS/m and 4.28 MS/m) | [REFERENCE STANDARD sheet](https://www.foerstergroup.com/web2print/en/reference-defects-and-standards/REFERENCE%20STANDARD%20CONDUCTIVITY%20MEASUREMENT.pdf) p.1 |
| Look and proportions | the waisted bumper, the screen, the F1–F4 row, the navigation block, the 4 × 3 number block, the connector block | [FOERSTER SIGMATEST Unpacking and Setup](https://www.youtube.com/watch?v=l8calAolJpM), 4:32–4:38; [product photo](https://www.foerstergroup.com/FOERSTER/Images/PRODUCTS/sigmatest/4759/image-thumb__4759__912/Sigmatest_2070-schatten.f97d461b.png) |

The SOP's standards bracket 25–60 %IACS. The model's two discs are labelled about 26 and 59 %IACS, the values
of the brass and Al 99.5 standards in Fischer's KAL-N set. That set also has 2024-T3511 at 29.3, 7175-T7351 at
37.9 and AlMgSi at 48.3 %IACS. Foerster supplies standards to order. The disc size (32 mm) is an estimate.

Edison (v3, `edison/v3-hardness-eddy-icp-onh/answer.md`) agrees on these points:

- 100 %IACS = 58 MS/m at 20 °C, and δ = 1/√(π f μ σ).
- Published Al-alloy work used a Fischer SIGMASCOPE SMP10 with an 11 mm probe (Shen 2012), and 60 kHz on
  15 × 15 × 10 mm coupons (Li 2021, 10.3390/ma14133615).
- Calibrate with certified blocks at the start of each session, and let the coupons, probe and standards reach
  about 20 °C.
- Hold the probe normal to the surface and take at least 3 readings; published aging work used 15 or more.

## Published against modelled

| | Published | Model |
|---|---|---|
| Length × width × thickness | 211 × 102 × 40 mm | 211 × 102 × 40 mm, plus a 12 mm connector block (the datasheet's H leaves it out, from the top view's proportions) |
| Waist (narrowest), half-width | — | 41.4 mm (fitted) |
| Screen | 240 × 320 px | 58 × 75 mm (fitted; the photo's display including its UI frame) |
| Key pitch | — | 14.7 mm (fitted) |
| Probe | heads 5, 8, 14 mm | 8 mm head (for 10 × 10 mm coupons), 19 mm ribbed grip, 98 mm long (estimate from the video) |

## Fit (`fit.py solve eddy_meter`; overlays in `out/register/eddy_meter/`)

| View | Picks | RMS, first model | RMS, fitted | Focal length |
|---|---|---|---|---|
| `top`: video frame 4:38, top down | 29 points, 5 edges | 1.4 px | 2.2 px | 510 px (640 × 360 frame) |
| `product34`: Foerster's three-quarter photo | 29 points, 4 edges | 8.8 px | 4.8 px | 981 px (912 × 684) |

The first model was measured off the top view with the 102 mm width as scale, so it already fit that view.
The three-quarter photo then moved four things:

- the waist lower, to about 19 mm below the middle;
- a 7 mm taper of the bumper towards the back;
- the screen slightly larger;
- the key pitch to 14.7 mm.

Worst remaining picks (photo):

- the right waist edge, 19 px;
- the lower right side and the bottom edge, 13–16 px.

The bumper's front edges are rounded more than the model's, so the silhouette there is soft.

## Uncertain

- **No independent held-out view.** The case photo reuses the same image of the meter, and a second top-down
  frame (4:32) comes from the same shot.
- **Probe size.** Its grip diameter and length are read off the video.
- **The 8 mm head** is the one the SOP needs for 10 mm coupons. The video shows the 14 mm head.
- **The standards** are not dimensioned anywhere public.
