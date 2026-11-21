# Door as a seal carrier: CalculiX, held at its latches and hinges

Door: 6061-T6, 15 mm, from `cad/lpbf_low.py`. C3D10 mesh, 67236 nodes. Seal centre line 662 mm; O-ring reaction (Lindley, FKM 75A, 25 % squeeze) as a uniform pressure on the groove floor, +20 mbar on the face inside the seal; latch pads (the ears' front faces at mid-height) held in y, hinge leaves (bottom) held in y and z.

| Cord | O-ring reaction | Each latch | Each hinge | Squeeze lost, worst point | Margin to 15 % squeeze | Result |
|---|---|---|---|---|---|---|
| 1.78 mm cord at 25 % (gland 1.32 x 2.3) | 1401 N | 724 N | 0 N | 34 µm at x 0, z 107 | 178 µm | OK |
