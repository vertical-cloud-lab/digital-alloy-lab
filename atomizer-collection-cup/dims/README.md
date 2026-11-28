# Stock collection cup: dimensions from photos and video frames

Measured on 2026-11-27 for [#269](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/269), to replace
the guesses in `../params.py`. Every number below comes from an image, and none from a caliper. The uncertainties
include judgement. `dims.json` holds the same numbers in machine-readable form, and `measure.py` re-runs the ellipse
fits, holds the pixel readings, and redraws `img/`.

**In short:** the joint at the cone's outlet is **ISO-KF, size KF-50 (flange OD 75 mm)**. The cup hangs on that clamp.
The stock cup is a KF-50 flange, a conical reducer, a sanitary butterfly valve, then a glass tube about 96-100 mm OD
between two plates about 170 mm across, held by four M12 tie rods. The height of the joint above the mat
**could not be measured** from the material available.

## Method

- **Ratios first.** Concentric circles in one plane carry the size. Ellipses are fitted with OpenCV (RANSAC around
  `cv2.fitEllipse`, using edge points found along rays from a guessed centre). The ratio of major axes is the ratio
  of diameters. One standard part in the same plane sets the scale.
- **Scales used:** ISO 2861 KF flange ODs and the PNEUROP 6606 centring-ring O-rings (KF-40: 42 × 5, KF-50: 55 × 5,
  from [Precision Polymer Engineering's table](https://www.prepol.com/products/kf-iso-nw-flange-fittings/)). In the
  4K photo of the parts, the scale is the 18 mm wrench's box end (8.4 px/mm) cross-checked against the tie-rod shank
  read as 12 mm (8.9 px/mm). The two agree within 6 %, and the mean, 8.67 px/mm, is used.
- **Hand readings.** Where an automatic edge is unreliable (wrench, rods, glass silhouette, gasket band, plate rim),
  pixel spans were read off gridded zoom crops. They are the `READ` constants in `measure.py`, each with its crop.
- **Limits.** The phone photos are close-ups with strong perspective: in the 4K parts photo, the glass's top rim is
  about 25 % nearer the camera than its bottom. The video frames are 720p and hand-held. Numbers that rest on one
  view, or that cross depths, are marked low confidence.

## Dimensions

| Item | Value | ± | Confidence | Source | Scale reference | Method |
|---|---|---|---|---|---|---|
| Joint type | ISO-KF: centring ring + O-ring, hinged clamp with wing nut | | high | photo 04; 4K top view; [video 4, 9:05](https://www.youtube.com/watch?v=1F9_4ccwhss&t=545s); [video 6, 0:40](https://www.youtube.com/watch?v=tfb4fsVNIFI&t=40s) | | metal ring inside a brown O-ring on a flat face. With the ring off, the face is flat, with a counterbore step at the bore and no bead groove. Tri-clamp uses a flat beaded gasket and no metal ring |
| Joint size | **KF-50** | | medium-high | photo 04 (`img/01`) | | O-ring OD / flange OD = **0.827**. Nominal: KF-50 0.867, ISO-K 63 0.901, KF-40 0.945 |
| Flange OD | **75** (KF-50 standard) | 2 | medium-high | photo 04 | ISO 2861 | the fit gives 78.6 if the O-ring is the standard 55 × 5, so caliper it |
| O-ring OD as seen | 62 | 2 | medium | photo 04 | flange 75 | ratio 0.827 |
| Centring-ring bore as seen | 44 | 2.5 | low | photo 04 | flange 75 | ratio 0.585. Common KF-50 rings are about 50, so this may be a reduced-bore ring, or the edge found may be deeper |
| Clamp | KF hinged clamp, finger-tight | | high | video 6, 0:40; video 4, 9:05; [video 5, 4:48](https://www.youtube.com/watch?v=58wJ_Khwgyk&t=288s) "just finger tightening" | | |
| Joint face above the mat | **not determined** (viz3d rough value 300) | 50 | — | | | no side view with the floor at a known scale |
| Cup support | hangs on the clamp | | high | video 4, 9:05; [video 5, 3:45](https://www.youtube.com/watch?v=58wJ_Khwgyk&t=225s) | | the cup stays on the cone when the cone swings out. The trainer: lift it and clamp at the same time, easier with two people |
| KF face to top of the valve body's flange | 53 | 10 | low | [cleaning video, 8:02](https://www.youtube.com/watch?v=boWsO0rxHvU&t=482s) (`img/11`) | KF-50 OD 75 (472 px) | centre-to-centre offset over sin 67° view tilt, 7 % depth correction |
| Reducer large end OD | 65 (fits 2.5 in, 63.5 mm tube) | 6 | low | cleaning video, 8:02 | KF-50 OD 75 | 390 px vs 472 px, 5 % depth correction |
| Valve body flange OD (4 bolts, acorn nuts) | 111 | 15 | low | cleaning video, 8:02 | KF-50 OD 75 | 650 px vs 472 px, 7 % depth correction |
| Stock cup overall height | ~225 | 30 | low | video frames | | sum of parts (KF face to valve flange 53, valve body ~50, top plate ~12, glass gap ~100, bottom plate ~6), not measured directly |
| Bottom plate OD | **170.5** | 9 | medium | 4K parts photo (`img/02`) | wrench + rod, 8.67 px/mm | ellipse fit, major axis 1478 px, rms 1.6 px |
| Bottom plate rim thickness | ~6 | 1.5 | low | 4K parts photo | 8.67 px/mm | front rim band 32 px / sin 38° |
| Top plate OD | same as bottom (by eye) | | low | [video 5, 0:34](https://www.youtube.com/watch?v=58wJ_Khwgyk&t=34s); video 6, 0:40 | | not measured |
| Glass OD | **96** (~100 per the run record) | 6 | medium | 4K parts photo (`img/04`) | plate OD | silhouette at the table, 859 px, over the plate's 1478 px. Lies between the gasket band's 92 and 107 |
| Glass wall | 5.7 | 1.0 | medium-low | 4K parts photo | glass OD | rim seen edge-on at its left extreme, 64 px of 1078 px |
| Glass length | ~110 | 15 | low | 4K parts photo; video 6, 0:40 | plate OD | rim ellipses give ~98, but the model ignores perspective; the side view gives a guard height of ~120 |
| Glass seal band in the bottom plate, OD / ID | 107 / 92 | 6 | medium-low | 4K parts photo | plate OD | edges of the black gasket band. The gasket is lifted and twisted, so the groove may differ. Depth not visible |
| Pocket in the bottom plate | about the band's ID, shallow | | low | 4K parts photo | | visual |
| Tie rods | **4 × M12** (shank 12.7) | 1.6 | medium | 4K parts photo | wrench, 8.4 px/mm | smooth rods with threaded ends. Plain hex nuts on the bottom plate: nut silhouette / rod = 1.63, which fits an ISO M12 nut (18 AF; AF/d 1.50, AC/d 1.73), and an 18 mm wrench lay with the parts. Acorn nuts on top |
| Tie-rod bolt circle | ~145 | 10 | low | 4K parts photo | plate OD | each nut's outer face sits 2-5 mm inside the rim |
| Perforated guard OD / height | ~116 / ~120 | 15 / 18 | low | video 6, 0:40 (`img/06`) | plate OD | 0.68 and 0.70 × plate width in a low side view |
| Valve | sanitary butterfly valve, EPDM seat ring, ball-knob lever on a side hub | | medium-high | photo 04; 4K top view; video 5, 0:34; video 6, 0:40 | | |
| Valve seat, axial | ~20 | 5 | low | 4K top view (`img/05`); Gage: "about 3/4 in tall" | | visual |
| Valve bore | ~60 (inferred) | 8 | low | cleaning video, 8:02 | | from the reducer's ~65 mm large end, so likely a DN65 / 2.5 in valve; not seen directly |
| Splash plate | curved strip across about half the bore, below the valve seat, notch near each end | | low | 4K top view; photo 04 | | visual only, no size |
| Cone shields | round thin discs in the cone's mouth, roughly 200 across | 30 | low (size) | [video 5, 2:15](https://www.youtube.com/watch?v=58wJ_Khwgyk&t=135s), [2:59](https://www.youtube.com/watch?v=58wJ_Khwgyk&t=179s) (`img/08`, `img/09`) | the hand | visual |
| Cup mass | ~6 kg | 2 | low | | | estimated by volume |

## Verdicts

1. **Joint: ISO-KF, KF-50, flange OD 75 mm.** The cup's top flange carries a metal centring ring inside a brown O-ring
   (FKM is usually brown). That is a KF centring ring, not a tri-clamp gasket. With the ring off (4K top view), the
   face is flat, with a step at the bore where the ring's lip sits. In photo 04 the O-ring's OD is 0.827 of the
   flange OD. That is close to KF-50's 0.867 and far from KF-40's 0.945, so the cup is not KF-40. The fitted ratio is
   about 5 % below nominal, so the flange OD should be calipered (75.0 expected; 78.6 would point to a non-standard
   flange). The training transcript calls the stack's flange "K50" too. The cone's own outlet flange was not seen with
   its ring off, but it must mate with this one. AMAZEMET's simpler metal cup (photo 09) is on another machine, and
   its sanitary clamps say nothing about this cone.
2. **Height of the sealing face above the mat: not determined.** No frame shows the mounted cup side-on with the floor
   and a known scale. The overhead frames (video 4 at 9:00, video 6 at 0:27) foreshorten the height too much. The
   Oct 2026 viz3d value, 300 ± 50 mm, is the only estimate. With the stock cup about 225 mm tall, about 75 mm would
   be free under it, but treat that as a guess. A KF joint separates after a few millimetres of drop, enough to clear
   the centring ring's lips, and the cup then slides out sideways.
3. **Stock cup.** There is a neck: a conical reducer between the KF-50 flange and the valve body (video 5, 0:34;
   video 6, 0:40; video 4, 9:05; cleaning video 8:02). It widens from the KF-50 neck to about 65 mm, likely 2 in to
   2.5 in tube, over about 53 mm from the KF face to the valve body's 4-bolt flange (about 111 mm OD). The back of
   the flange shows the KF 15° taper. The bottom plate is 170 ± 9 mm OD, with a rim about 6 mm thick. The glass is
   96-100 mm OD with a wall of about 5.7 mm. Its length, 100-120 mm, needs a tape. The seal band in the bottom plate
   is about 92-107 mm. There are four M12 tie rods on a bolt circle of about 145 mm, with plain hex nuts below
   (consistent with the 18 mm wrench) and acorn nuts on top. The guard is about 116 mm OD.
4. **Valve:** a sanitary butterfly valve. Two bolted body halves (acorn nuts) hold an EPDM seat ring, and the seat's
   burnt inner face is the white crust about 20 mm tall. A lever with a black ball knob on a side hub turns the disc
   90°. The bore was not seen. The reducer's ~65 mm large end suggests a DN65 / 2.5 in valve with a bore of about
   60 mm.
5. **Splash plate vs shields.** The splash plate belongs to the cup. It is a curved stainless strip in the bore below
   the valve seat, with a notch near each end, and it covers about half the bore; its size needs calipers. The
   **shields AMAZEMET means are different parts**: thin round discs, roughly cone-mouth size (about 200 mm), laid in
   the mouth of the swing-out water-cooled cone (video 5, 2:15-3:05). Splashes stick to them and the powder falls
   past. One is enough for aluminium; hot metals such as copper get more.
6. **Support:** the cup hangs on the KF clamp alone, with no floor support. It swings out with the cone, and mounting
   it means lifting and clamping at once. Estimated mass is about 6 ± 2 kg.
7. **AMAZEMET's metal cup (photo 09):** a plain stainless tube hung from the cone outlet with hinged sanitary clamps,
   about the outlet's diameter. A butterfly valve with a ball-knob lever sits on a side branch just below the outlet,
   and a second valve and clamp sit mid-height. The tube runs to near the floor of that machine's frame. No scale is
   in the photo, so there are no sizes. Training video 5 (0:00-0:35) describes it as "a very simple tube and the
   valve is added separately".

## Still needs calipers or a tape (in this order)

1. The cone outlet's flange OD and bore, and the clamp's size marking. This confirms KF-50, and whether the flange is
   75.0 or about 78.6 mm.
2. With the cone latched: the height of the outlet's sealing face above the mat, and the free height under it.
3. The cup's centring ring: its bore, OD and O-ring size (55 × 5 expected).
4. The stock cup's overall height, from the KF face to the bottom of the bottom plate.
5. The glass's OD, wall and length (the cracked glass is in hand).
6. Both plates' OD and thickness; the seal groove's ID, OD and depth in each plate; the pocket's diameter and depth.
7. Tie rods: thread (M12 expected), length, bolt circle, and the nut sizes across flats (18 expected).
8. The valve's bore and seat dimensions, and the reducer's length and large-end diameter.
9. The splash plate's width, radius, thickness and notch spacing, and what the notches hook onto.
10. The cone shields: diameter, thickness, how many, and how they sit in the cone's mouth.
11. The cup's mass on a scale.

## Files

- `measure.py`: run `python measure.py` (defaults read the photos from `/tmp/github-images`, the WhatsApp media from
  the Nov 13 run record, and the frames from `/tmp/meas/fr`). `--fetch` pulls the frames from YouTube with yt-dlp and
  ffmpeg; it needs a network YouTube accepts, given with `--proxy http://...`.
- `img/01`: photo 04 with the flange, O-ring and ring fits. `img/02`: the bottom-plate fit and spans. `img/03`: the
  wrench box end. `img/04`: the glass spans. `img/05`: the annotated top view. `img/06`-`img/11`: video frames,
  cropped to the hardware.
