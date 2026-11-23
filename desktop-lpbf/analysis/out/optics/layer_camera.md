# Layer camera from its mounted position (`analysis/optics/layer_camera.py`)

Line of sight 32.7° off the plate normal, 161.7 mm from the lid face to the plate centre; entrance pupil taken 10 mm behind the lens front (assumed). Sensor IMX477, 1.55 µm pixels, 6.29 × 4.71 mm.

**The lid hole is vertical while the line of sight is tilted:** at the lid's underside (z 120) the axis is 10.3 mm from the hole's centre, against an 11 mm radius.

| Openings | Lens | N | Mag. | Pixel on plate, across / along tilt (µm) | Diffraction FWHM on plate (µm) | FOV (mm) | DOF, 2 px blur (mm) | Scheimpflug tilt (°) | S25 / M50 / L75: fits frame (land./port.) | edge light reaching the pupil, min (%) | plate area > 50 % lit (%) | edge blur without tilt (µm) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| as drawn | 6 mm (Raspberry Pi CS-mount) | 2.8 | 0.0287 | 54.0 / 64.2 | 55 | 219 × 164 | 21.7 | 1.1 | LP / LP / LP | 100 / 100 / 100 | 100 / 100 / 100 | 68 / 137 / 205 |
| as drawn | 6 mm (Raspberry Pi CS-mount) | 4.0 | 0.0287 | 54.0 / 64.2 | 79 | 219 × 164 | 30.9 | 1.1 | LP / LP / LP | 100 / 100 / 100 | 100 / 100 / 100 | 48 / 96 / 144 |
| as drawn | 6 mm (Raspberry Pi CS-mount) | 8.0 | 0.0287 | 54.0 / 64.2 | 158 | 219 × 164 | 61.9 | 1.1 | LP / LP / LP | 100 / 100 / 100 | 100 / 100 / 100 | 24 / 48 / 72 |
| as drawn | 12 mm C-mount | 2.8 | 0.0591 | 26.2 / 31.2 | 27 | 106 × 80 | 5.3 | 2.2 | LP / LP / LP | 100 / 100 / 100 | 100 / 100 / 100 | 137 / 274 / 411 |
| as drawn | 12 mm C-mount | 4.0 | 0.0591 | 26.2 / 31.2 | 38 | 106 × 80 | 7.5 | 2.2 | LP / LP / LP | 100 / 100 / 100 | 100 / 100 / 100 | 96 / 192 / 288 |
| as drawn | 12 mm C-mount | 8.0 | 0.0591 | 26.2 / 31.2 | 77 | 106 × 80 | 15.0 | 2.2 | LP / LP / LP | 100 / 100 / 100 | 100 / 100 / 100 | 48 / 96 / 144 |
| as drawn | 16 mm (Raspberry Pi C-mount) | 2.8 | 0.0804 | 19.3 / 22.9 | 20 | 78 × 59 | 2.9 | 3.0 | LP / LP / –– | 100 / 100 / 100 | 100 / 100 / 100 | 183 / 365 / 548 |
| as drawn | 16 mm (Raspberry Pi C-mount) | 4.0 | 0.0804 | 19.3 / 22.9 | 28 | 78 × 59 | 4.1 | 3.0 | LP / LP / –– | 100 / 100 / 100 | 100 / 100 / 100 | 128 / 256 / 383 |
| as drawn | 16 mm (Raspberry Pi C-mount) | 8.0 | 0.0804 | 19.3 / 22.9 | 56 | 78 × 59 | 8.3 | 3.0 | LP / LP / –– | 100 / 100 / 100 | 100 / 100 / 100 | 64 / 128 / 192 |
| as drawn | 25 mm C-mount | 2.8 | 0.1316 | 11.8 / 14.0 | 12 | 48 × 36 | 1.1 | 4.8 | LP / –– / –– | 100 / 100 / 88 | 100 / 100 / 100 | 285 / 571 / 856 |
| as drawn | 25 mm C-mount | 4.0 | 0.1316 | 11.8 / 14.0 | 17 | 48 × 36 | 1.6 | 4.8 | LP / –– / –– | 100 / 100 / 99 | 100 / 100 / 100 | 200 / 399 / 599 |
| as drawn | 25 mm C-mount | 8.0 | 0.1316 | 11.8 / 14.0 | 34 | 48 × 36 | 3.2 | 4.8 | LP / –– / –– | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 200 / 300 |
| before | 12 mm C-mount | 4.0 | 0.0591 | 26.2 / 31.2 | 38 | 106 × 80 | 7.5 | 2.2 | LP / LP / LP | 0 / 0 / 0 | 56 / 46 / 40 | 96 / 192 / 288 |
| before | 16 mm (Raspberry Pi C-mount) | 4.0 | 0.0804 | 19.3 / 22.9 | 28 | 78 × 59 | 4.1 | 3.0 | LP / LP / –– | 0 / 0 / 0 | 56 / 46 / 40 | 128 / 256 / 383 |
| lid hole drilled on the line of sight, Ø22 | 12 mm C-mount | 4.0 | 0.0591 | 26.2 / 31.2 | 38 | 106 × 80 | 7.5 | 2.2 | LP / LP / LP | 100 / 100 / 0 | 100 / 100 / 84 | 96 / 192 / 288 |
| lid hole drilled on the line of sight, Ø22 | 16 mm (Raspberry Pi C-mount) | 4.0 | 0.0804 | 19.3 / 22.9 | 28 | 78 × 59 | 4.1 | 3.0 | LP / LP / –– | 100 / 100 / 0 | 100 / 100 / 84 | 128 / 256 / 383 |
