# `riffle_splitter`: Humboldt H-3971C micro riffle splitter (SOP 01 and SOP 05, #262)

SOP 01 asks for "a riffle-split sub-sample, not a scoop off the top" of the 20–63 µm powder. ASTM B215 (sampling
metal powders) uses a chute splitter. The model is the Humboldt H-3971C, a Jones-type micro riffle splitter, and SOP
05's animation imports it too (`stage.get("riffle_splitter")`).

## Sources

| What | Source |
|---|---|
| 16 chutes, 0.125 in (3.2 mm); hopper 4.5 × 4.5 in (114 × 114 mm); stainless hopper with a manual gate, stainless and anodized aluminium riffle bank, stainless frame with legs; two stainless "Hy-Back" (notched L-shape) pans | Humboldt product page, [humboldtmfg.com/microriffle--splitter.html](https://www.humboldtmfg.com/microriffle--splitter.html) (read 2026-11-28) |
| The same design from Gilson: SP-171 / SP-171X Jones micro splitter, 14 × 1/8 in chutes, 1.8 kg shipping weight, ASTM B215, pans with an extended back | [globalgilson.com/jones-micro-splitters](https://www.globalgilson.com/jones-micro-splitters); the SP-171X product photos (certifiedmtp.com) |
| Larger siblings, for scale: MiniSplitter H-4291 (= Gilson SP-3), 48 × 3.2 mm chute bars, 214 × 216 × 343 mm, ASTM B215 | [humboldtmfg.com/minisplitter-125.html](https://humboldtmfg.com/minisplitter-125.html) |

Humboldt publishes no overall size and no usable photo of the H-3971C, so the look and the proportions between the
published hopper and chutes come from Gilson's photos of the same design.

## Published and model dimensions

| | Published | Model |
|---|---|---|
| Chutes | 16 × 3.2 mm | 16 × 3.2 mm, 0.8 mm dividers: a 64.8 mm bank, 40 mm across |
| Hopper | 114 × 114 mm | 114 × 114 mm, 35.8 mm deep (fitted) |
| Upright plates | – | 54.2 mm wide (fitted), 2 mm thick, with bent feet and acorn nuts |
| Pans | 2, notched, high back | 34 × 84 mm, 40 mm front, 88 mm back, notched round the uprights (estimates) |
| Overall height | – | 151 mm (estimate: the photos show it about 1.3 × the hopper's width) |

## Registration (`fit.py solve riffle_splitter`)

| View | Photo | Picks | RMS, starting model | RMS, fitted | Lens |
|---|---|---|---|---|---|
| `gilson_3q` | Gilson SP-171X, three-quarter (1000 px) | 4 rim corners, the front upright's top left | 10.34 px | 8.04 px | 2711 px |
| **`gilson_front` (held out)** | Gilson SP-171X, front-right (600 px) | 4 rim corners, the upright's top corners | 6.01 px | 4.52 px | 558 px |

The fit checks the hopper and the uprights only. The pans are not picked: in the photos their outlines overlap and
their orientation could not be read with confidence.

## Pieces and joints (for SOP 05)

`body` (hopper, bank, uprights, nuts); `pan_l`, `pan_r` (slide 90 mm out to −x / +x at v = 1); `feed`, `stream`,
`split_l`, `split_r` (fades: powder in the hopper, the curtain through the chutes, the halves in the pans, riding on
their pans). `RIFFLE_POINTS`: the hopper's rim centre and each pan's floor centre.

## What is uncertain

- The pans' size and how they sit (the photos are of the Gilson; Humboldt only says "notched L-shape").
- The manual gate Humboldt mentions is not modelled; Gilson's photos show none, and the sample is poured from a pan.
- Gilson's model has 14 chutes, Humboldt's 16; the model follows Humboldt.
