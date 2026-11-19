# Flange STLs with a single-track rectangle on top, one per set

Gage's request on [PR 243](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243) (2026-11-19):
copy the W011 flange file once for each set in
[the final table](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243#issuecomment-7021458367),
make the rectangle on top as wide as that set's spot, merge the bodies, and name the file after the set. The aim
is for the printer to lay a single track on top of each flange.

![End views of three of the files](fins-preview.png)

| File | What it is |
| --- | --- |
| `stl/<set name>.stl` | 33 binary STLs, one for each set in [`../out/wall_sets.csv`](../out/wall_sets.csv) (32 settings and the control). Walls that share a set use the same file |
| [`flange-fins-stl.zip`](flange-fins-stl.zip) | All 33 in one zip |
| [`fins.csv`](fins.csv) | For each file: spot, the rectangle's width and x range, height, length, volume, the walls that use it, and the sha256 |
| `template/` | The file as Gage sent it (`W011_348W_705_140um_h130.stl`) |
| [`make_fins.py`](make_fins.py) | Writes the STLs, `fins.csv` and the zip; standard library only: `python make_fins.py` |
| [`check_fins.py`](check_fins.py) | Rebuilds each part as a boolean union of two boxes (manifold3d) and checks the STL matches it |
| [`preview.py`](preview.py) | Draws `fins-preview.png` from the files' own end faces |

## Geometry

Every file is the template with only the rectangle's two long faces moved. Each one is a single closed body
of 28 triangles, in mm, in the same position as the template. W011's file is byte-identical to the template.

| | Same in every file | Changes |
| --- | --- | --- |
| Flange | 1.27 × 12.7 × 5.08 mm (x −0.705 to 0.565, y −12.7 to 0, z −5.08 to 0) | |
| Rectangle | 0.05 mm tall (z 0 to 0.05), 12.6 mm long (y −12.6 to 0), centred on the flange at x = −0.07 mm | width = the set's spot size, 0.050 to 0.190 mm |

Three things come from the template, not from the request's wording:

- **Height 0.05 mm, not 0.5 mm.** The template's rectangle is 0.05 mm tall, the request said only the width
  changes, and the aim is one pass. 0.05 mm is one layer at 50 µm; 0.5 mm would be about 10 layers.
- **Length 12.6 mm.** As in the template, the rectangle is flush with the flange's y = 0 end and stops 0.1 mm short
  of the other end.
- **33 files, not 28.** The table has 33 set names.

## Check in WRX before relying on it

Neither hatch tab can draw a strip this narrow. In the 316L set, Adv. surface area starts 0.11 mm inside the
outline and Upside surface area 0.14 mm inside, so a hatch needs a strip at least 0.22 to 0.28 mm wide. A contour
tab will draw the rectangle instead. In Carl's photos of the 316L set (2026-11-10) those are:

| Tab | Power (W) | Speed (mm/s) | Spot (µm) | Offset to original contour (mm) |
| --- | --- | --- | --- | --- |
| Upside contour | 120 | 220 | 70 | −0.035 |
| Adv. surface area contour | 120 | 220 | 50 | −0.015 |
| Downside contour | 100 | 130 | 50 | −0.01 |

So in WRX's layer view, on one flange:

1. Check that the rectangle appears on exactly one layer.
2. Count its vectors. A contour follows the outline, so on a strip it is usually a loop: two passes along the
   rectangle, one down each side, rather than one. Check the narrowest file too (W016, 50 µm), in case WRX
   drops it.
3. See which tab draws them. It is probably the Upside contour, since nothing is above the rectangle. If so, the
   rectangle prints at that tab's 120 W, 220 mm/s and 70 µm on every flange, unless each set's Upside contour
   tab also gets that set's power, speed and spot. That tab also draws the outline of the flange's top layers,
   so those would change too.

If WRX draws a loop or nothing, the plan's fallback for one vector per track is a Magics line support, which is
exposed as a single line, probably by the Adv. lattice support tab
([plan §2](../../m2-single-track-schedule.md#2-can-the-m2-run-many-parameter-sets-in-one-build)).
