# Context for the uploaded PSD files

These files come from PR #226 in vertical-cloud-lab/digital-alloy-lab (commit 80f3fa5), an SEM image-analysis
particle size distribution of powder lot `k7m2q9`: a nickel-aluminium bronze (UNS C63000, Cu-10Al-5Ni-4Fe,
density about 7.6 g/cm3) atomized on 2026-10-27 on the lab's AMAZEMET rePOWDER ultrasonic atomizer
(sonotrode scan peak about 39.7 kHz, molybdenum plate, 1.5:1 booster).

- `nab_k7m2q9_particles.csv`: one row per segmented region (8,828 rows). Count only rows with
  `included == True`. `ecd_um` is the projected-area equivalent circle diameter in micrometres, already
  corrected for the threshold edge offset. `weight` is the Miles-Lantuejoul edge-correction weight to apply
  to each counted particle. `field` is the SEM field; fields are 0.67-1.01 um per pixel, and particles smaller
  than 10 px across were excluded (`below_cut`), so the counts are complete only above about 6.7 um (200x
  fields) and 9.0-10.1 um (133-150x fields). `flag` marks irregular, agglomerated or oversize particles.
- `nab_k7m2q9_summary.md`: the published summary (number D10/D50/D90 = 34.8/46.9/71.5 um; volume
  45.8/103.7/208.5 um; under 20 um: 2.1 % by number, under 0.1 % by volume).
- `fields.csv`: per-field pixel size and magnification.

The aluminium powder we want to print is Al 4047 (AlSi12) and 6063 from the same atomizer and settings
(about 40 kHz, Mo plate, 1.5:1 booster, amplitude 90-100 %). No image PSD of the Al lots exists yet. A
first SEM look at four Al lots found "the particles seem to be pretty large, around 40-60 um for the smaller
particles", highly spherical, with one sample showing "a few smaller particles". Liquid Al-12Si near its
liquidus: density about 2.4 g/cm3, surface tension about 0.8-0.9 N/m. Liquid NAB: density about 7.0 g/cm3,
surface tension about 1.2-1.3 N/m.

The sieves on hand are 8 in (200 mm) stainless: No. 60 (250 um), No. 230 (63 um), and No. 325 (45 um) on
order. The target LPBF machine is an Aconity MIDI; the runs plan targets 15-45 um, the doc it replaces
targets 20-63 um. A typical run gives 100-250 g of powder.
