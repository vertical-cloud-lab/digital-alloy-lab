# Flash diffusivity analyser: NETZSCH LFA 717 HyperFlash (`laser_flash`, models_props.py)

README §5.1 sends laser flash out (NETZSCH contract testing), so the model stands at the contract lab. The LFA 717
replaces the LFA 467 HyperFlash, and its housing looks the same. TA's DLF 1600 is the alternative; it is a floor
unit with a separate laser cabinet, so it was not drawn.

## Sources

| Figure | Value | Source |
|---|---|---|
| Temperature | −100 to 500 °C (LN2 to −100 °C, compressed air to 0 °C); HT version RT–1250 °C | [LFA 717 technical specifications](https://analyzing-testing.netzsch.com/_Resources/Persistent/c/5/f/0/c5f0ccf6ae8efac108c4f49b1394c94f93fdac3c/Technical_Specifications_en_LFA_717_HyperFlash_Series.pdf) |
| Flash | xenon lamp, up to 10 J a pulse, 10–1500 µs | same; LFA 467 specification sheet |
| Detector | InSb (RT–500 °C) or MCT (−100 to 500 °C), LN2-cooled | same; [LFA 467 brochure](https://analyzing-testing.netzsch.com/_Resources/Persistent/3/6/7/f/367f54b9bc7fc3a5b36f6b41191f5dbaf802ecb7/LFA_467_HyperFlash_en_web.pdf) p.12 |
| Sample changer | 4 holders × 4 samples: 16 × 12.7 mm round or 10 mm square, or 4 × 25.4 mm | LFA 717 specifications |
| Sample thickness | 0.01–6 mm; NETZSCH's reference discs 12.7 × 2.5 and 10 × 2.0 mm; diameter / thickness above 5 | [Accessories LFA](https://analyzing-testing.netzsch.com/_Resources/Persistent/6/e/d/a/6eda2809d9120db34ba06e4f7df5bc427e8d9538/Accessories_LFA_E.pdf) p.8, 46–47 |
| Layout | flash at the bottom, sample in the middle, detector on top | LFA 467 brochure p.4 |
| Loading | from the top, with tweezers, under a lid | [NETZSCH e-learning video](https://www.youtube.com/watch?v=vkHcL_8jTZE), 1:43–2:17 |
| Coating | graphite spray, both faces, about 5 µm and even; a thick coat biases Al and Cu low | [NETZSCH: when and how must samples be coated](https://analyzing-testing.netzsch.com/en/know-how/tips-tricks/lfa/when-and-how-must-samples-be-coated-during-lfa-measurements) |
| Contract testing | ASTM E1461, standard size Ø 12.7 mm | [NETZSCH contract testing](https://analyzing-testing.netzsch.com/en-US/services/contract-testing) |
| External size | **not published** (no NETZSCH sheet, brochure or legacy page gives it) | — |
| Width | 620 mm, **estimated** from the operator beside a HyperFlash | vkHcL_8jTZE at 1:35 |
| Proportions | base, plinth, front panel, detector tower and collar, the block behind it | [NETZSCH LFA 717 video](https://www.youtube.com/watch?v=vxowKxtTS0A), 0:06 (front) and 0:52 |

Edison (v1, `edison/v1-dsc-lfa-hardware/artifact-02.md`) agrees on these points:

- a xenon flash lamp;
- graphite spray on both faces, in several thin coats;
- holders for 12.7 mm or 10 mm discs, 1–3 mm thick;
- an IR detector.

## The fit (`fit.py solve laser_flash`; overlays in `out/register/laser_flash/`)

The registration checks proportions only. With no published dimension, the scale is the 620 mm estimate.

| View | Picks | RMS before | RMS fitted |
|---|---|---|---|
| `front`: video 0:06 | 8 points, 2 circles, 2 edges | 5.6 px | 2.1 px |
| `angle`: video 0:52, **held out** | the same set | 3.1 px (first model) | 4.6–4.8 px (fitted model) |

A first pass with mis-read picks (a seam taken for the top edge) gave 26 → 19 px. It was re-picked from
labelled zooms. Fitted from the first guess:

| | First guess | Fitted |
|---|---|---|
| base height | 345 | 349 |
| depth | 640 | 618 |
| front panel width × drop | 302 × 140 | 296 × 134 |
| tower Ø × height (on a 37 mm collar) | 146 × 190 | 149 × 193 |
| tower offset left of centre | 100 | 99 |
| block behind the tower, w × h | 221 × 122 | 223 × 143 |

The held-out view got slightly worse with the fitted model (4.6 px). Both views are near-frontal renders, so
depth is weakly constrained.

## Inside (for the cutaway)

The internal layout is drawn after NETZSCH's cutaway render (vxowKxtTS0A, 0:37–0:48), and the sizes are
estimates:

- the xenon lamp under the measuring place;
- a light guide;
- the furnace ring round the sample;
- the optics;
- the LN2-cooled detector in the tower.

The well and lid are drawn in front of the tower, as in the e-learning video. The changer runs back from the well
to the measuring place, which is our simplification of how the HyperFlash moves its holders.

## Uncertain

- **All external dimensions.** NETZSCH publishes none; the width is scaled from a person.
- **The sample changer's mechanism and the inside.** Both are simplified.
