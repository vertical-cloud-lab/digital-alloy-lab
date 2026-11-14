# SOP 03 (draft): Archimedes density, porosity and crack density of printed cubes

**Checks:** the printability map (lack of fusion, keyholing, balling and hot cracking) from the
AM Module or from the open criteria in #238 and #249, and the density Thermo-Calc reports.
**Analysis:** [`../analysis/density_porosity.py`](../analysis/density_porosity.py). The set-up
itself is #144. Draft.

## Samples
- **Cubes:** 5 × 5 × 5 mm (#144) or 10 mm, cut from the plate and labelled by position.
- **Cleaning:** remove support remnants, clean ultrasonically in ethanol for 5 min, and dry at
  60 °C for 30 min.
- **Reference:** a cube of wrought 6063 (or of the alloy cast dense) of the same size, measured
  with every batch.

## Archimedes (ASTM B962-type)
- **Balance:** 0.1 mg or better, with a density kit. Use 0.01 mg for 5 mm cubes, which weigh only ~0.33 g.
- **Water:** distilled, with one drop of wetting agent per 250 mL. Measure its temperature to 0.1 °C.
- **Weighing:** weigh each cube three times in air and three times immersed, after taring the
  basket in water. Remove bubbles with a fine brush.
- **Uncertainty:** for a 5 mm Al cube with 0.1 mg readings, the script gives about ±0.1 % in relative
  density, which is about the porosity of a good part. So use 10 mm cubes, or a 0.01 mg balance,
  when porosity is below 0.5 %.
- **Reference density:**
  - best: the He-pycnometer density of the same powder;
  - otherwise: Thermo-Calc's density at 20 °C for the measured composition (SOP 05).
  - Report which one you used.
- **Time:** about 10 min per cube.

```bash
python ../analysis/density_porosity.py archimedes --m-air 0.33412 --m-wet 0.20915 --T-water 21.4 --rho-ref 2.668
```

## Sections: porosity, pore type and cracks
1. Section one cube per condition parallel to the build direction (XZ). Polish as in SOP 02; leave it unetched.
2. Stitch optical images at 50–100× over the whole face.
3. **Porosity:** `density_porosity.py image section.png`. It thresholds with Otsu's method, and the
   Delesse principle makes the area fraction an estimate of the volume fraction.
4. **Pore type:** in Fiji, circularity above about 0.8 means a gas or keyhole pore; irregular pores along
   track boundaries mean lack of fusion.
5. **Cracks:** total crack length per area (mm/mm²), traced in Fiji. Count only cracks along grain
   boundaries in the build direction, the hot-cracking signature; leave out pores that look like cracks.
6. **Time:** about 1 h per batch of 8 sections after polishing.

## Acceptance
- The reference cube reads ≥ 99.9 % (or its known density).
- Repeat weighings agree within 0.05 % in density.
- Archimedes and image porosity agree within their uncertainties; if they don't, look for open
  porosity or bubbles.

## Notes
- Open surface porosity fills with water and makes Archimedes read high. If sections show
  surface-connected pores, coat the cube or use oil impregnation.
- Combine the results with the single tracks (SOP 02): tracks set the keyhole and balling
  boundaries, cubes set lack of fusion, and crack density gives the hot-cracking axis.
