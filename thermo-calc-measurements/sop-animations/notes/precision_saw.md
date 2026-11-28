# `precision_saw`: the LECO VC50 Vari/Cut low-speed diamond saw

SOP 02 sections each piece of nine tracks 0.5 mm from its target plane (#243 §3, "fine wet saw"), and SOP 03 cuts its
cubes and coupons. A LECO saw fits the lab's LECO metallography line (MX400 press, PX500 polisher). The VC50 is LECO's
low-speed, low-deformation precision saw: a gravity-fed arm with a sliding weight lowers the work onto a thin diamond
blade that dips in a coolant tank, the way Buehler's IsoMet Low Speed works. (MIT's single tracks were cut on a Buehler
IsoMet 4000, a higher-speed precision saw; #243 §3.)

Model: `models_track.precision_saw()`, key `precision_saw`. Frame: x right, y away from you, z up from the bench,
origin at the centre of the chassis' footprint, mm.

## Sources

| What | Source |
|---|---|
| 330 H x 432 W x 457 D mm, 24 kg; 5 in (127 mm) x 0.014 in (0.36 mm) diamond blade on a 0.5 in arbor; 0-500 rpm (50-650 SFM on a tachometer); 1/15 hp motor; micrometer positioning; sliding weight; vise for samples up to 1.5 in (38 mm); automatic shut-off | LECO brochure, form 200-952 (7/26 REV12), https://www.leco.com/wp-content/uploads/documents/brochures/200-952-VC50.pdf (read through the Pi; not committed) |
| Layout and the controls: cutting force "through a sliding counterweight", "integrated vice", micrometer in metric or US | LECO's VC50 page, https://www.leco.com/instrument/vc50-precision-wafering-saw/ (2026), and its six product photos (whole saw, the sectioning assembly, the cooling-tank drawer, the sample holder, the adjustment wheel, the speed knob) |
| The machine in use, from the front, the right and above | "Leco VC 50 Precision Diamond Saw Instructional Video", https://youtu.be/BkWFULiNy-k (0:17, 1:02, 1:10); "Leco VC-50 Diamond Saw #59586" (Bid Service LLC), https://youtu.be/WqqdOjjtBu0 (0:02, 0:33) |

What the photos and frames show, and the model has: a light warm-grey chassis on a plinth; a control box on the left
(POWER / START / STOP, the tachometer, SPEED SELECT, the LECO / VC-50 label, four screws); on the right a lower base
whose front is the coolant drawer (a knob; a stainless trough of cutting oil inside); on the base the blade guard, a
grey sheet box open at the top with a green window on its right side and a perforated strainer at deck level; the
blade in the y-z plane on a spindle from the control box, its flanges and knurled nut on the +x side; behind the guard
a casting that carries the arm's pivot and, out of its right side, the micrometer (black ring, sleeve, thimble,
ratchet); the arm, level through the pivot, with the sliding weight on a rail and the vise hanging over the blade; a
clear cover with a grey top, hinged at the back, its steel lip hanging over the guard's front.

## Published against model

| | Published | Model |
|---|---|---|
| Overall width, with the micrometer | 432 mm | 364 chassis + 76 micrometer = 440 |
| Depth | 457 mm | 440 chassis + 15 knobs = 455 |
| Height, cover closed | 330 mm | 330 (cover top) |
| Blade | 127 x 0.36 mm | 127 x 0.36 mm |
| Vise capacity | 38 mm | holds the 22 x 10 x 10 mm piece of #243 |

## Registration (fit.py, refs/precision_saw/)

Picks: corners of the control box, the right base, the plinth, the blade guard; the tachometer's four corners; the
speed and drawer knobs; the micrometer's root and end; verticals for the lens. The first solve started from the
envelope and the proportions read off the front frame; its fitted values are now `VC50` in the model. Depth (440) and
the micrometer's reach (76) are held at the published envelope: freed, the fit drifts to D 389 mm and a 92-106 mm
micrometer (overall width 455-470 mm), because no view pins the depth down (LECO's photo has a long lens, f ~ 4000 px).

| View | Picks | RMS, starting model -> fitted | Focal length |
|---|---|---|---|
| LECO product photo (front right, high) | 19 | 32.6 -> 11.5 px | 3990 px |
| Video 1:02, front, square-on | 15 | 35.5 -> 5.9 px | 2732 px |
| **Held out:** Bid Service 0:02, front right, high, another unit (no cover) | 13 | 39.5 -> 30.0 px | 1481 px |
| **Held out:** video 1:10, right side, cover up | 8 | 63.1 -> 27.8 px | (poorly fixed: 492 px) |

Re-solved with the fitted values built in: front 5.8 px, LECO photo 9.5 px; held out 28.4 and 26.1 px. Overlays:
`out/register/precision_saw/*.jpg` (yellow: the model's silhouette; green dots: picks; red crosses: where the fitted
model puts them).

Fitted against the first guess: chassis W 356 -> 364, control box 247 x 168 -> 252 x 170, deck 102 -> 105, blade
guard set back 60 -> 57 mm, 220 -> 173 mm deep, walls 100 -> 108 mm tall; the micrometer 47 mm lower and 38 mm
further forward; the tachometer centred 70 % across the control box.

## Joints

`cover` (hinge at the back of the casting, 0 closed -> 1 up 105 deg), `carriage` (the micrometer's 25 mm along -x),
`arm` (the feed about the pivot: 0 = the piece 5 mm over the blade, 1 = 16 mm lower, through the 10 mm piece; < 0 lifts
it), `weight` (80 mm along the arm), `wheel` (12 turns from 0 to 1), `tank` (the drawer 150 mm out), and two props on
the arm, `specimen` (the clamped piece) and `slice` (the 2 mm sliver the cut takes off). `saw_points()` gives the blade
top, the piece, the pivot and the drawer knob in the saw's frame. A self-check (every moving piece against the body in
its end poses, FCL) finds no overlap deeper than 1.5 mm.

## Uncertain

- The depth and the micrometer's reach (above).
- The arm's linkage and the vise: drawn from the close-up photos (a knurled screw, a steel jaw plate, a brass
  insert); the vise here clamps the piece by its ends so its jaws stay off the blade's path.
- The inside of the base (the drawer's cavity, the spindle's bearing) is not seen in any source; it is drawn so the
  blade dips into the oil, as the cooling-tank photo shows.
- The older VC-50 in the videos and LECO's 2026 VC50 look the same; small differences (the meter's face, the drawer
  knob's height) would show in the held-out residuals.
