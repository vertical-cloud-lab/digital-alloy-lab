# The first copper-alloy powder lot, Oct 27, 2026 (inputs to Fig. cupowder)

Powder code `k7m2q9`. Gage Erickson's run report is in #219: a 1,079.886 g charge, carbon-fiber
plate dipped in tungsten, 1:1.5 booster, 24 ppm O2, amplitude 90, 1,300 °C melt, graining pressure
0.19 bar, 2 minute melt, estimated 97% yield. **The alloy is 630 bronze** (UNS C63000, a wrought
nickel-aluminum bronze, about 82Cu-10Al-5Ni-3Fe; McMaster 8203K41, receipt "High-Strength 630 Bronze"),
not the "Cu70/Ni30" of the run log and video title: Sterling's clarification in #219
(comment 6460235121, Oct 28, 03:54 UTC). The EDS below agrees: aluminum and iron peaks, and a Ni Kα
about a tenth of Cu Kα.

| File | Source | Processing |
|---|---|---|
| `run_t060s.png`, `run_t240s.png`, `run_t330s.png`, `run_t570s.png` | BYU VCL YouTube [`2brsz-90seg`](https://www.youtube.com/watch?v=2brsz-90seg), "10/27/2026 Atomizer Run Cu70/Ni30 Video 5 of atomizer and furnace ports" (public, 720 x 1280) | Frames at 60, 240, 330 and 570 s (`ffmpeg -ss`), cropped to 720 x 805 at y = 400, 420, 475 and 250 px. No person in any frame |
| `lot_jar.jpg` | Gage Erickson's photograph of the jar, #219 (`user-attachments/assets/026807ba-...`) | Cropped to the jar (x 755–2365, y 1450–3250 of 3024 x 4032) |
| `sem_200x.png` | Ronnie Guymon, BYU Apreo, Oct 27, 2026, 5:54 PM, ETD, 5 kV, 0.10 nA, 200x, HFW 2.07 mm (Box `Baird_S_SEM/Ronnie Guymon/Bronze/not annotated.tif`, 3072 x 2188) | Databar removed (rows 0–2049 kept), resized to 1800 px wide: 1.150 µm/px |
| `sem_2548x_particle.png` | Same session, 6:01 PM, 2,548x, HFW 163 µm (`moon sphere.tif`) | Cropped to one particle (x 140–1840, y 150–1850), full resolution: 0.0531 µm/px |
| `eds_20kV_3p2nA.csv` | Same session, EDS at 20 kV and 3.2 nA, EDAX Octane Plus (`20kV 3_2 nA  USE THIS ONE.csv`) | Copied as is: energy (keV), counts. The carbon peak is from the mounting tape |

The figure is drawn by `../../make_cu_prelim_figure.py`; scale bars come from the HFW in each
image's databar.
