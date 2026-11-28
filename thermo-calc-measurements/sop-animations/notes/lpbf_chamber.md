# `lpbf_chamber` and `lpbf_exterior`: where SOP 02's tracks are printed

SOP 02 asks which machine prints the first tracks: the desktop LPBF (#260), Utah's Aconity MIDI (P1, Dec 2-3), or
BYU's Concept Laser M2 (#243). The video uses the Aconity MIDI, the soonest, for the context shot, and draws the build
area at the plate, which is what the SOP's samples are about, at real size.

## `lpbf_exterior`

byu-vcl's `lab_models.equipment.aconity_midi()`, unchanged, as one `body` piece: 2450 x 1500 x 2320 mm (Aconity's
configurator data, 2026), its process chamber, beam tube, two scan heads, filter unit and control cabinet laid out from
Aconity's configurator layers and front photos (CMU's photo at 4.036 mm/px; byu-vcl's sources/aconity_midi.json). Not
registered again here: no video of a MIDI turned up on YouTube through the tunnel (`ytsearch15:AconityMIDI` found two
Aconity part videos, neither showing the machine; two more searches returned nothing).

## `lpbf_chamber`

Frame: origin on the build cylinder's axis at the chamber floor, z up, mm.

| Shown | Size | Source |
|---|---|---|
| Build plate | 170 mm across, 15 mm thick, 6061 | 170 mm platform: Aconity (byu-vcl equipment.py); 6061: Utah's plate, DAL PR #169; 15 mm: byu-vcl's assumption |
| One powder layer | 40 um (SOP: 30-50 um) | SOP 02; Edison v2 answer §1.1 (Aboulkhair et al. used 40 um for AlSi10Mg single tracks; 30 um is the usual machine layer) |
| Tracks | 12 mm long, 2 mm pitch, rows of 18 in two groups of nine 10 mm apart, mid-lengths on one line | DAL PR #243 §4 |
| Track width and height | from the synthetic tracks of `sop02_tracks.data()` (Eagar-Tsai through `melt_pool_calibration.py`), at least 15 um proud so they show | synthetic |
| Rows | bare-plate row at y = +46, Sobol blocks A-D at +23, 0, -23, -46 mm (each 42 mm wide) | layout ours, within #243's 15 mm-from-the-edge rule |
| Exposure | outlet side first, every track in +y (across the flow), never with it | SOP 02; #243 §4 |
| Beam | a faint cone to the spot; label: 1/e2 radius r0 from the machine's beam profile (~70 um diameter at focus on Aconity systems: Maddison 2022, in the Edison v2 answer §1.2; the analysis demo uses r0 = 40 um) | as cited |
| Gas | argon across the plate, inlet manifold on -x, outlet duct on +x (2.5-4 m/s at the inlet on an SLM 125: Edison v2 §1.3) | layout typical |
| Recoater, supply cylinder, overflow | a blade across x moving in +y; the supply in front of the build cylinder, the overflow behind it | typical bottom-up feed; Aconity publishes no inside drawing |
| Powder for one layer | ~1.2 g on the 170 mm plate (pi x 85^2 mm^2 x 40 um x 2.7 g/cm3 x 0.5 packing) | computed |

Joints: `plate` (15 mm up), `supply` (one dose, 0.2 mm), `recoater` (490 mm across), `gas` and `beam` (fades). The
recoater's arm rises over the outlet duct, so the blade's whole travel is clear of the chamber (FCL audit of chapter 1:
no contact).

## Uncertain

- Everything inside the chamber except the plate, the layer and the tracks is a typical layout, not the MIDI's.
  Which way the gas flows relative to the recoater on the Utah machine is one of #243's open questions; the SOP only
  needs the tracks scanned across or into it and exposed from the outlet side.
- The bare-plate row is drawn on the same plate, exposed before the layer goes down (#243's optional add-on); the
  powder then covers it until the plate is depowdered.
