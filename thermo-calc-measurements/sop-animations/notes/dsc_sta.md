# `dsc_sta`: NETZSCH STA 449 F5 Jupiter (SOP 01, #262)

The SOP asks for a heat-flux DSC or DTA that reaches 750 °C for Al alloys and 1150 °C for Cu alloys, is
vacuum-tight, and takes alumina crucibles. The README's purchase table (section 5.1) names the TA Discovery SDT 650,
the NETZSCH STA 509 Jupiter and the Mettler Toledo TGA/DSC 3+. The model is the **NETZSCH STA 449 F5 Jupiter**:

- it is the only one of the NETZSCH candidates with published outer dimensions;
- it has the most usable footage: NETZSCH's product video, and a lab's 14-minute operating video that raises the
  furnace, swings it aside and loads crucibles with tweezers;
- its successor, the STA 509 Jupiter Classic, has the same key data (RT–1600 °C, 1e-2 mbar, three mass-flow
  controllers, an optional 20-position sample changer), so the model also stands for it.

The STA 449 F3, DSC 404 F3 and STA 509 have no published dimensions, and the SDT 650 is a horizontal
instrument, which the SOP's loading steps do not describe.

## Sources

| What | Source |
|---|---|
| 600 × 700 × 650 mm, 900 mm with the furnace raised, 83 kg without the PC | NETZSCH, *Key technical data STA 449 F5 Jupiter*, p. 1 ([PDF](https://analyzing-testing.netzsch.com/_Resources/Persistent/5/4/2/d/542d78584e0dcac952e90debb30f9424d3d9f054/Key_Technical_Data_en_STA_449_F5_Jupiter.pdf)); brochure p. 14 ([PDF](https://analyzing-testing.netzsch.com/_Resources/Persistent/e/7/9/6/e796f7361432facdefd82d616296d644353ace37/STA_449_F5_Jupiter_en_web.pdf)) |
| RT–1600 °C (SiC furnace); 1e-2 mbar with automatic evacuation; 3 mass-flow controllers (1 protective, 2 purge); 20-position sample changer in system version II | same |
| The hoist lifts the furnace, which then swings to the left or the right; the sample crucible goes on the front position ("close to user"), the empty one behind | lab operating video, [youtu.be/mmuGqG-1LNE](https://youtu.be/mmuGqG-1LNE) at 3:04–3:29 |
| Look: curved front, navy panel with a teal band (lifting device open/close, purge 1, purge 2, protective, power), NETZSCH badge at the front right, round grey deck plate, sensor carrier (copper flange, alumina radiation shields, carrier tube, sensor), wire guard, the furnace (light grey, dark middle band, gas fitting on top) on an arm from a white head on a stainless lifting column, green solenoid valves on the left side | NETZSCH's video [youtu.be/XDOAhT8CybU](https://youtu.be/XDOAhT8CybU) (0:08, 0:29, 0:45) and the lab video (1:04, 3:04–3:29) |
| Al2O3 crucible 85 µL, ø 6.8 mm, 99.7 %, to 1700 °C (GB399972) and lid (GB399973); Pt/Rh 85 µL ø 6.8 mm NGB825767 | NETZSCH accessories catalogue, pp. 7, 8, 12 ([PDF](https://at-messe.netzsch.com/_Resources/Persistent/4/d/3/5/4d35822b3610ccb3706904ec1d3c3099ebdb64ac/Accessories_DSC_TGA_STA.pdf)) |
| Type S TG-DSC sensor on the STA 449 F3; 85 µL Al2O3 or Pt-Rh 6.8 mm crucibles with vented lids; Ar at 35–60 mL/min; three evacuate/backfill cycles typical | Edison literature search, `edison/v1-dsc-lfa-hardware/answer.md` (xu2018, teodorescu2026, tadgell2019, rawson2021) |

## Published and model dimensions

| | Published | Model | Note |
|---|---|---|---|
| Width × depth | 600 × 700 mm | 600 × 700 mm | NETZSCH does not label the axes; 600 is read as the width, as the footage shows |
| Height, furnace closed | 650 mm | 663 mm to the top of the furnace's gas fitting | the thin glass capillary above it is not in the model |
| Height, furnace raised | 900 mm | 801 mm (lift 137.5 mm, fitted) | **does not match**; see below |
| Deck (top of the base) | – | 283.6 mm (fitted) | |
| Furnace | – | ø 159 mm, 312 mm tall (fitted) | |
| Sensor top over the deck | – | 127.5 mm (fitted) | |
| Front panel | – | x −180 to −2 mm, z 71–269 mm (fitted) | |
| Crucible | ø 6.8 mm, 85 µL | ø 6.8 × 4.0 mm, bore 6.0 mm, floor 0.5 mm | height not published: 85 µL in a 6.0 mm bore needs 3.0 mm |

## Registration (`fit.py solve dsc_sta`)

Three frames, picks in `refs/dsc_sta/*.json` (frames not committed; `video` and `t` fetch them again). Fourteen
dimensions free; the published width and depth fixed.

| View | Frame | Picks | RMS, starting model | RMS, fitted | Lens |
|---|---|---|---|---|---|
| `front_raised` | NETZSCH video 0:45, square-on, furnace raised | 19 points: base corners, panel corners, badge, furnace band edges, fitting, sensor | 5.03 px | 2.75 px | 2104 px (33.8°) |
| `lab_front` | lab video 1:04, front-on from above, furnace closed | 11 points: panel corners, badge, deck corners, furnace band edges | 6.59 px | 5.42 px | 1179 px (57°) |
| **`lab_left` (held out)** | lab video 3:04, front-left from above, closed | 6 points and 3 ring curves on the furnace's band edges | 6.26 px | 6.06 px | lab lens, shared |

Overlays: `out/register/dsc_sta/*.jpg` (yellow: the model's silhouette; green: picks; red: where the fitted model puts
them).

## What is uncertain

- **The lift.** Both videos show the furnace raised about 140 mm, enough to clear the sensor before it swings away,
  while 650 → 900 mm in the key data implies 250 mm. The model follows the footage. The 900 mm may include the thin
  gas capillary on top of the furnace (it reaches about 940 mm in the 0:45 frame).
- **The swing.** It is modelled as the furnace and its white head turning 70° about the lifting column. Whether the
  swing is motorized or by hand is not stated; the animation shows a hand guiding it.
- **The sensor.** The two positions are 11.2 mm apart along the depth (sample in front), an estimate; NETZSCH does
  not publish the sensor plate's size.
- **Not modelled:** the furnace's water cooling hoses, the balance's own vacuum flange, cable connections, the logo
  lettering.
- **The sample changer** is drawn only as an outline (tray of 20 positions and a turret) for the one step that
  mentions it.
