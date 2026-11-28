# `icp_oes`: Agilent 5900 ICP-OES with an SPS 4 autosampler (SOP 05)

The model is `icp_oes()` in [`models_chem.py`](../models_chem.py). Every number below has its source in `SPECS["icp_oes"]`.
The README's list of ICP-OES instruments (section 5.1: Agilent 5900, Thermo iCAP PRO X, PerkinElmer Avio) names the
5900 first, so the model is a 5900. BYU's own instruments are Thermo iCAP 7400s.

## Sources

| What | Source |
|---|---|
| W × D × H, mass | Agilent 5800/5900 Site Preparation Guide G8020-90003, Ed. 4 (May 2024), p. 19, Table 3: **625 × 740 × 887 mm, 90 kg**. agilent.com refused the runner, so this was read from the Wayback Machine's copy of the Agilent URL |
| Exhaust chimney | Same guide, pp. 15 and 21: a 150 mm flue **887 mm above the bench** (so the 887 mm height is to the top of the chimney), its centre 520 mm from the rear and 210 mm from the side; 2.5–6.0 m³/min |
| SPS 4 | Same guide, p. 19: **600 × 363 × 510 mm, 15 kg**; four racks (Agilent's SPS 4 page) |
| Torch, views | Agilent technical overview 5994-1514EN, p. 2: a vertical one-piece torch; the 5900 has radial, axial and SVDV views; the dichroic spectral combiner merges the axial and radial light into one reading. p. 3: RF 27 MHz, 750–1500 W |
| Sample introduction | App note 5994-5874EN, p. 2: SeaSpray concentric glass nebulizer, double-pass glass cyclonic spray chamber; Table 1: argon 12.0 L/min plasma, 1.00 auxiliary, 0.7 nebulizer. User's guide G8020-90002, pp. 26–27: 1.8 mm quartz injector for the dual-view torch. Agilent's ICP-OES help ("About the instrument"): a 3- or 5-channel peristaltic pump |
| Look | Pro Lab Support's walk-round of a 5900 ([youtu.be/SU6AoWTDZcY](https://youtu.be/SU6AoWTDZcY?t=24): 0:24 and 1:19 square-on, 2:10 with the torch compartment open). ASU Core Research Facilities' 5900 ([youtu.be/VkMy6cp2-Y0](https://youtu.be/VkMy6cp2-Y0?t=5): 0:04–0:33, with the door being opened, the sample introduction bay and the SPS 4) |

What the frames show:
- a white upper housing the full width of the instrument. Most of its front is a door hinged at the left, holding a
  black glass window with a grey grip strip at its right. In the 2:10 frame the door is open and the torch
  compartment is visible: stainless walls with the vertical torch;
- a fixed white strip at the right with an amber status light;
- the exhaust chimney, a white box on top, right of centre;
- under the housing, a white pedestal set back from the left edge (the housing overhangs there), and to its right the
  open sample introduction bay. Its walls are dark navy. The spray chamber and nebulizer sit high on the left of the
  bay, under the torch, and the peristaltic pump sits low on the right.

## The fit

`fit.py solve icp_oes` uses the picks in `refs/icp_oes/`: the housing's corners, the window's corners, the door's seam,
the pedestal's and bay's edges, and the chimney's corners. The two frames from the same video share one lens. The
fitted parameters are millimetres from the front's left edge and from the bench; `register.py` rounds what it writes to
0.1, which is why the model isn't parametrized in fractions.

| View | Picks | RMS, starting model | RMS, fitted | Focal length |
|---|---|---|---|---|
| `front24`: SU6AoWTDZcY 0:24, square-on | 16 | 4.54 px | 3.30 px | 971 px (shared) |
| `front79`: SU6AoWTDZcY 1:19, a little from the right | 15 | 4.09 px | 2.46 px | 971 px (shared) |
| **Held out**: `asu56`, VkMy6cp2-Y0 0:05.6, another lab, another camera (640 × 360) | 8 | 3.36 px | 3.65 px | 534 px |

Fitted dimensions, with their starting values:

| | Start | Fitted |
|---|---|---|
| Top of the box (the chimney above it to 887) | 740 | 748 |
| Underside of the upper housing | 350 | 358 |
| Pedestal, from the left edge | 110–230 | 101–230 |
| Window (glass), x | 70–512 | 67–521 |
| Window, z | 426–647 | 439–655 |
| Door's right edge | 554 | 564 |
| Chimney centre from the left, its width | 440, 250 | 455, 252 |

Published against the model, mm:

| | Published | Model |
|---|---|---|
| 5900 W × D × H | 625 × 740 × 887 | 625 × 740 × 887 (the door and the grip add nothing: the door sits flush) |
| SPS 4 W × D × H | 600 × 363 × 510 | 600 × 363 × 510 |
| Chimney | centre 520 mm from the rear | the same; its centre fitted 170 mm from the right side (the guide says 210 mm "from the side") |

One pick was dropped from both frames: the bay frame's lower right corner. It sits 7–11 px right of the housing's
edge in both frames, as if a base stood proud of the housing there. That isn't modelled.

## Joints (`inst.joints`)

- `door`: the torch compartment door, hinged at the left edge, opens 105°.
- `pump_rotor`: the peristaltic pump's head, 4 turns over v 0 → 1.
- `plasma`, `beam`: fades (the plasma, the radial and axial light paths).
- `sps_lid`: the SPS 4 cover's top and front, hinged at the back, up 100°.
- `sps_arm`: the probe arm, along the beam to the sampled tube's column.
- `sps_probe`: a path, first along the arm to the tube's row and then down into the tube, 8 mm off its floor.
- `~shell`: the upper housing's skin, see-through for the cutaway (Rig's see-through amount).

## Uncertain

- **Inside the housing.** The torch's position (60 % of the width from the left, 160 mm behind the front), the
  compartment's depth, the optics' box, the axial interface and the radial port are drawn to show what each is. They
  aren't measured. The plasma is drawn pale and translucent, not as a glow.
- **The pump head (92 mm) and the spray chamber (46 mm × 70 mm)** are estimates.
- **The SPS 4's racks** are drawn as 3 × 7 racks of 50 mL tubes. The real racks come in several formats.
- **The door.** In the frames it sits flush with the housing and is about 40 mm thick. Its window's lower edge was
  fitted, but how it seals isn't visible.
