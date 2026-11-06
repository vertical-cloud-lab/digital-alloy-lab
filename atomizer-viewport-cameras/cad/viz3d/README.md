# The rePowder CadQuery model, copied from `atomizer-training/viz3d/`

`model.py` and `scene.py` are copied unchanged from `atomizer-training/viz3d/` at commit `7ec59ab` (PR #173, which
brought byu-vcl PR #255 over): the whole machine as named CadQuery parts, with the ultrasonic stack measured on 8
October, and the `Scene` framework its step animations are drawn with. [`../render.py`](../render.py) and
[`../assembly.py`](../assembly.py) draw the machine with them, and [`../units.py`](../units.py) reads the window
positions from `model.py`. Their own README, with where every dimension comes from, is
`atomizer-training/viz3d/README.md` on that branch.

Don't edit them here. Change the model in `atomizer-training/viz3d/`, copy it again, then run `../units.py` (the
moves follow the model's windows) and the renders. Once PR #173 is merged, this copy can go, and `../units.py` can put
`atomizer-training/viz3d/` on the path instead.

| File | sha256 |
|---|---|
| `model.py` | `ae7a955c9c5ce97a0335c9b1dec0d086173f73dc594b5c8adcde607593d2a03b` |
| `scene.py` | `a424794739ff07ffb993ff644f4353d71866a5bcaac8c613abe4aeb5caa37787` |

`python model.py` builds the parts and caches their meshes in `.cache/`, which git ignores.
