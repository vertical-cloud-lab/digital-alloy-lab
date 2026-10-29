# Pour estimates for the Oct 27 and Oct 28 runs

Output of `python estimates.py`. Inputs: liquid C63000 6.9 g/cm³, surface tension 1.15 N/m, 140° contact angle on hBN, discharge coefficient 0.7, crucible ID 50 mm (assumed), chamber at 150 mbar, all pressures gauge. Treat the absolute numbers as ±30–50 %; the comparisons between runs are the point.

```text
## Metallostatic head (crucible ID 50 mm)
  1080 g: melt height 8.0 cm, head 54 mbar
   858 g: melt height 6.3 cm, head 43 mbar
   430 g: melt height 3.2 cm, head 21 mbar

## Capillary pressure to push NAB into a non-wetting bore
  0.5 mm: 70 mbar
  0.7 mm: 50 mbar
  1.0 mm: 35 mbar

## Net push and flow at the start of the pour
  bore 0.5 mm
    Oct 27: graining 0.19 bar, 1080 g        net   +23 mbar  flow 0.8 g/s
    Oct 27: turbo 1.5 bar, 1080 g            net +1333 mbar  flow 5.9 g/s
    Oct 28: graining 0.23 bar, 858 g         net   +52 mbar  flow 1.2 g/s
    Oct 28: back to 0.19 bar, ~430 g left    net    -9 mbar  flow 0.0 g/s
    Oct 28: turbo 1.5 bar, 858 g             net +1322 mbar  flow 5.9 g/s
  bore 1.0 mm
    Oct 27: graining 0.19 bar, 1080 g        net   +59 mbar  flow 4.9 g/s
    Oct 27: turbo 1.5 bar, 1080 g            net +1369 mbar  flow 23.9 g/s
    Oct 28: graining 0.23 bar, 858 g         net   +88 mbar  flow 6.0 g/s
    Oct 28: back to 0.19 bar, ~430 g left    net   +26 mbar  flow 3.3 g/s
    Oct 28: turbo 1.5 bar, 858 g             net +1358 mbar  flow 23.8 g/s

## Time to drain the charge at a fixed setting (stops when the net push reaches zero)
  bore 0.5 mm, 0.23 bar, 858 g        1020 s
  bore 0.5 mm, 0.19 bar, 1080 g       stops with 610 g left
  bore 0.5 mm, turbo 1.5 bar, 858 g   146 s
  bore 1.0 mm, 0.23 bar, 858 g        164 s
  bore 1.0 mm, 0.19 bar, 1080 g       336 s
  bore 1.0 mm, turbo 1.5 bar, 858 g   36 s

## Capillary wavelength and Lang d50 = 0.34 lambda at 40 kHz
  C63000     lambda 138 um, d50 47 um
  aluminium  lambda 179 um, d50 61 um

## Argon: cylinder pressure 1500 -> 1150 psi in one run = 350 psi (training notes: 100-160 psi per run)

## Observed pours (display 'Min. Grain' and narration)
  Oct 27: 1080 g in ~3.5 min = 5.1 g/s average
  Oct 28:  858 g in ~3.7 min = 3.8 g/s average (if it all drained)
  Oct 28 at 0.23 bar: a non-wetting bore of ~0.88 mm drains 858 g in 223 s
  Oct 28 at 0.30 bar: a non-wetting bore of ~0.73 mm drains 858 g in 223 s
  Oct 27 at 1.48 bar: a non-wetting bore of ~0.47 mm drains 1080 g in 210 s
  jet speed leaving a 0.5 mm bore, Oct 27, 1.48 bar: 6.0 m/s
  jet speed leaving a 0.5 mm bore, Oct 28, 0.30 bar: 1.5 m/s
  jet speed leaving a 0.5 mm bore, Oct 28, 0.23 bar: 0.5 m/s
```
