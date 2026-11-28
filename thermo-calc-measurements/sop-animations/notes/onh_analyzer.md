# `onh_analyzer`: LECO ONH836 inert-gas-fusion analyzer (SOP 05)

The model is `onh_analyzer()` in [`models_chem.py`](../models_chem.py), with its sources in `SPECS["onh_analyzer"]`. The
README's equipment table names the LECO ON836/ONH836 for O/N/H. BYU has none; the nearest is the Utah powder-metallurgy
group's LECO TCH 600.

## Sources

| What | Source |
|---|---|
| W × D × H | **LECO publishes no envelope for the 836 series that we could find.** 762 × 711 × 914 mm (30 × 28 × 36 in), about 186 kg, is a resale listing's figure (EquipNet), marked there as an estimate, and seen only in a search snippet. **Third party, unverified.** The fit moved the height to 928 mm |
| Detection | LECO's 736/836 page, model comparison ([leco.com/instrument/onh-elemental-analyzers](https://www.leco.com/instrument/onh-elemental-analyzers/)): the ONH836 measures **O as CO and CO2 by NDIR** (two cells), **H as H2O by NDIR**, and **N by thermal conductivity**. Helium or argon carrier; about 3-minute cycles |
| Method for Al | LECO application note 203-821-459 (O in aluminium): crucible 776-247 for solids, 782-720 for chips and powder; about 0.25 g of solid. Note 203-821-427 (powders): **0.10–0.15 g in a 502-822 nickel capsule with about 0.4 g of 501-598 nickel flux**, the crucible holding about 0.05 g of graphite powder; solids in 502-344 nickel baskets. Furnace power in those methods: 4.1–5.8 kW |
| Edison (v3) | Liu et al. 2025, [doi:10.1088/1742-6596/2959/1/012001](https://doi.org/10.1088/1742-6596/2959/1/012001) (FeSiAl powder): **80–100 mg in a tin capsule**; incomplete recovery above 120 mg; on an ONH836 the empty crucible is **degassed at 5.5 kW for 20 s, the analysis run at 5.0 kW for 45 s**; NDIR for CO/CO2, thermal conductivity for N2 (and H2 on instruments that use it); about 4 minutes per sample. Paplewski (gas fusion for powder metallurgy and AM): seal powders in airtight containers, preferably argon-filled, and open them only just before weighing |
| Look | LECO's "ONH836 Series" video ([youtu.be/W5IGSUMWQq8](https://youtu.be/W5IGSUMWQq8?t=22): renders at 0:13–0:29; the electrode at 1:31–1:35; the infrared cells at 1:37–1:55). A dealer's video of a real ONH836 ([youtu.be/SJcUGXPb1Dw](https://youtu.be/SJcUGXPb1Dw?t=40): the whole analyzer square-on at 0:34–1:57; the furnace at 2:02–3:30). LECO's talk-through ([youtu.be/bmuEksg945g](https://youtu.be/bmuEksg945g?t=21): the lower electrode with a graphite crucible, 0:18–0:27; "temperatures of up to 3000 °C" with the high-temperature crucible, 0:41) |

What the frames show:
- a light grey cabinet with a portrait touchscreen standing proud on the front left;
- the furnace on the right:
  - the electrode housing ("LECO"), with the loading head on top. The head has a round black port and a black handle
    on its right;
  - under it, a lit bay holding the lower electrode: a black cylinder with a steel rim and the crucible pedestal. It
    rises to clamp the crucible against the upper electrode and drops to open;
  - the electrode cleaner's brush, on a black body with a brass collar, left of it;
- a rounded plinth below the bay;
- a lid over the whole top.

## The fit

`fit.py solve onh_analyzer` uses the picks in `refs/onh_analyzer/`: the screen's corners, the housing's corners, the
cabinet's top left, the bay floor's right end, and the plinth's label. Each LECO render is its own shot, so each has
its own lens.

| View | Picks | RMS, starting model | RMS, fitted | Focal length |
|---|---|---|---|---|
| `leco22`: W5IGSUMWQq8 0:22, render, front left | 10 | 20.39 px | 2.96 px | 1061 px |
| `leco14`: W5IGSUMWQq8 0:14, render, close, front left | 5 | 26.49 px | 5.72 px | 1777 px |
| **Held out**: `dealer40`, SJcUGXPb1Dw 0:40, a real ONH836 (2016), square-on | 12 | 6.39 px | 13.91 px | 527 px |

**The held-out frame disagrees, and the reason is known.** The dealer's 2016 analyzer has a squarer touchscreen
(111 × 140 px, a ratio of 0.79) than the one in LECO's current renders (0.55). Its worst residuals are all on the
screen's corners (21–30 px). The rest of its picks fall within about 10 px. A test that assumed the dealer's video was
stretched sideways didn't help (9.7 px). So the model follows LECO's current renders, and the dealer frame records how
much an older unit differs.

Fitted dimensions, mm from the front's left edge and from the bench:

| | Start | Fitted |
|---|---|---|
| Height (to the lid's top) | 914 (third party) | 928 |
| Screen x, z | 40–396, 175–665 | 40–324, 177–719 |
| Electrode housing x, z | 419–655, 484–750 | 414–706, 462–718 |
| Bay floor, plinth's right end | 274, 670 | 271, 668 |

## Joints

- `lower_electrode`: drops 60 mm into its well to open (v 1, as it starts); v 0 closes the crucible against the upper
  electrode's tip.
- `crucible`, `glow`: fades riding on the lower electrode (the crucible, and the crucible dull orange at fusion).
- `sample`: a path from the loading head straight down through the upper electrode into the crucible.
- `gas`: a fade (the carrier gas's path from the furnace to the cells).
- `~housing`, `~shell`: the electrode housing and the cabinet, see-through when the drop and the detectors are shown.

## Uncertain

- **The envelope.** It is a third party's, not LECO's. The fit raised the height 1.6 %; the width and depth weren't
  free.
- **Inside the cabinet.** The two NDIR cells, the catalyst heater, the reagent tubes and the thermal-conductivity cell
  are drawn where the cutaway can show them. LECO's video shows the IR cell block (1:37–1:55) but not where it sits.
- **The lower electrode's 60 mm travel, the crucible (22 mm × 25 mm), and the capsule and basket (9 mm)** are
  estimates. LECO lists part numbers, not sizes.
- **Capsule material.** The brief and Edison's source (Liu 2025) use a tin capsule, with nickel flux or a basket only
  where the matrix method requires it. LECO's own note for powders (203-821-427) uses a nickel capsule with nickel
  flux. The model shows a tin capsule in a nickel basket, and the caption says the lab's method decides.
