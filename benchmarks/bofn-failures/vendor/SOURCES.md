# Vendored code: unmodified copies

These files are byte-for-byte copies of the two synthetic alloy networks this benchmark runs on.
They live on branches that are not merged yet, so they are copied here to make the benchmark
reproducible on its own. Do not edit them; `tests/test_failures.py` checks their sha256.

| Copy | Source (repo path at commit) | Branch / PR | sha256 |
|---|---|---|---|
| `al/bofn_alloy.py` | `benchmarks/bofn-prelim/bofn_alloy.py` @ `d1ca727fb37fa044cbcf78c420e17aa1ac827bc5` | `claude/onr-yip-fy27` (PR #117) | `fbd79c9da726b112d6a2bb4e6f5f806e1c6613bd21db41338f91c22f43b5613e` |
| `al/policies.py` | `benchmarks/bofn-prelim/policies.py` @ `d1ca727` | same | `55036cdff0ce6036f6b5407fc2f0f2f0f64cc6bdf7c79a9a706d9c445f63a670` |
| `cu/bofn_alloy.py` | `benchmarks/bofn-cu-ded/bofn_alloy.py` @ `b1ba843b33d57e8fbb15e6bbf1aa7468b815f8d7` | `claude/issue-205-20261025-0045` (PR #206) | `acbb3bf9bcf902035dc5c902bc538ef8e4f1bcf3308e65e4a02e2910c5c664fa` |
| `cu/policies.py` | `benchmarks/bofn-cu-ded/policies.py` @ `b1ba843` | same | `8fd8052658baf6ae33748ef509257b1165c8bdf1c06bf3bfeda29f5d2216d76e` |
| `cu/truth_phys.py` | `benchmarks/bofn-cu-ded/truth_phys.py` @ `b1ba843` | same | `f56368df72ee78847c5854a1e8073fdcd65bcab33da1322373ad8f3370298c4a` |
| `cu/phys/calphad_grid.csv` | `benchmarks/bofn-cu-ded/phys/calphad_grid.csv` @ `b1ba843` | same | `5672bcb4a3bd14eb3818011348ed8f6dc1a60c6bb0c2e1912aed1b51c57c7975` |
| `cu/phys/corrosion_fit.json` | `benchmarks/bofn-cu-ded/phys/corrosion_fit.json` @ `b1ba843` | same | `e752e98541394f5fb54aec31253cb5ddd33b8a025bf853aba8e52385c6b72cf3` |

The aluminum network is the MS&T26 benchmark (`bofn-prelim`): CALPHAD → ultrasonic atomization
→ LPBF → tensile, with the inoculant bias `kappa`. The copper network is the ONR YIP benchmark
(`bofn-cu-ded`): CALPHAD + heat flow → atomization → small DED (Utah) → large DED (Mines) →
microscopy → tensile → one-hour screen → 30-day immersion, with the bias knobs `kappa` and `eta`,
and two truths: the hand-written one (`BOFN_TRUTH=toy`) and the physics-based one
(`BOFN_TRUTH=phys`: a pycalphad grid, a corrosion model fitted to seawater data, and the
proposal's search-space limits).
