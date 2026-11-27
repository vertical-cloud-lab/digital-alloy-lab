# Our own 3D melt-flow solver: validation runs (#249)

[`scripts/keyhole_meltflow.py`](../../../../scripts/keyhole_meltflow.py) solves the steady Navier–Stokes and energy
equations in the beam frame. It has:
- Marangoni shear on a flat surface;
- a Carman–Kozeny mushy zone;
- the keyhole as a fixed cavity at its wall temperature;
- the material's full H(T) and k(T).

The physics, the checks and the results at version 2's keyhole states are in
[`../v2/README.md`, section 6](../v2/README.md#6-melt-flow-our-own-3d-solver).

This folder has the solver's own validation runs, made with version 1's materials and cones at three points: AlSi10Mg 250 W
(conduction), the blend at 375 W, and NIST's Al 5182 track.
- `python scripts/keyhole_meltflow.py runs`, about 6 min: [`meltflow-runs.csv`](meltflow-runs.csv), with the convergence histories in [`meltflow-runs.json`](meltflow-runs.json).
- `python scripts/keyhole_meltflow.py sensitivity`: [`meltflow-darcy-sensitivity-alsi10mg.csv`](meltflow-darcy-sensitivity-alsi10mg.csv). The Carman–Kozeny constant, from 10⁸ to 10¹⁰, changes pool sizes by under 0.6 %.
- [`meltflow-blend-375W-section.png`](meltflow-blend-375W-section.png) shows the top surface and centre plane of the blend run.

The 5 checks in [`scripts/test_keyhole_meltflow.py`](../../../../scripts/test_keyhole_meltflow.py) pass in about 1.5–2.5 min.
