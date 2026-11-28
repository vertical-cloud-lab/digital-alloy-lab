# The rePowder CadQuery model, copied from PR #189 / PR #173

`model.py` and `scene.py` are copied unchanged from `atomizer-viewport-cameras/cad/viz3d/` on PR #189's branch
(`c4827e9`), which copied them unchanged from `atomizer-training/viz3d/` at `7ec59ab` (PR #173). They hold the whole
machine as named CadQuery parts and the `Scene` framework the atomizer animations are drawn with. The README with
where every dimension comes from is `atomizer-training/viz3d/README.md` on PR #173's branch.

Don't edit them here. Once PR #173 is merged, this copy can go and `../common.py` can put `atomizer-training/viz3d/`
on the path instead. `../integration.py` replaces three of the model's parts in these renders without touching the
file: the blue cabinet (hollowed behind the right-hand door), its right-hand door (now a part that swings open) and the
HMI's arm (its pivot post moved from inside the screen to behind the HMI's back, where it no longer shows through the
screen in close-ups).

| File | sha256 |
|---|---|
| `model.py` | `ae7a955c9c5ce97a0335c9b1dec0d086173f73dc594b5c8adcde607593d2a03b` |
| `scene.py` | `a424794739ff07ffb993ff644f4353d71866a5bcaac8c613abe4aeb5caa37787` |

`python model.py` builds the parts and caches their meshes in `.cache/`, which git ignores.
