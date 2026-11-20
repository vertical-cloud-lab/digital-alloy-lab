# Door as a seal carrier: CalculiX, held at its latches and hinges

Door: 6061-T6, 15 mm, from `cad/lpbf_low.py`. C3D10 mesh, 61769 nodes. Seal centre line 663 mm; O-ring reaction (Lindley, FKM 75A, 25 % squeeze) as a uniform pressure on the groove floor, +20 mbar on the face inside the seal; latch pads (top corners) held in y, hinge leaves (bottom) held in y and z.

| Cord | O-ring reaction | Each latch | Each hinge | Squeeze lost, worst point | Margin to 15 % squeeze | Result |
|---|---|---|---|---|---|---|
| 3.53 mm cord at 25 % (as drawn) | 2782 N | 801 N | 613 N | 26 µm at x 0, z 108 | 353 µm | OK |
| 1.78 mm cord at 25 % | 1403 N | 410 N | 314 N | 14 µm at x 0, z 108 | 178 µm | OK |
