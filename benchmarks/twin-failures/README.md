# Failed vs. abandoned atomizer runs in a simulated year of the vertical lab (DAL #274)

**Work in progress (2026-11-26):** the code is in and the runs are going. Results, figures and the write-up follow
in this file.

This benchmark asks issue #274's question, how BOFN should treat failed and abandoned experiments, inside the byu-vcl
digital twin: [round 3](https://github.com/vertical-cloud-lab/byu-vcl/pull/394) (asynchronous acquisition,
physical capacity, interim readings), engine pinned at
[`f1606a9`](https://github.com/vertical-cloud-lab/byu-vcl/commit/f1606a93df64da25a99b168c198f5498f08469da). Both
campaigns run for one simulated year at once: aluminium (FLAIME) and copper (ONR YIP). They share the atomizer and
the other instruments. The method-level companion on DAL's own Al and Cu networks is on
[`claude/issue-274-20261126-0639`](https://github.com/vertical-cloud-lab/digital-alloy-lab/tree/claude/issue-274-20261126-0639)
(`benchmarks/bofn-failures/`). The strategy names follow its `bofn-failed-vs-abandoned.md`.

| File | What it is |
|---|---|
| `get_twin.sh` | fetches the twin at the pinned commit (sparse: `vertical-lab/twin/` only) |
| `failures.py` | failure regimes, a cause and the lab's diagnosis for every failed run, damage and repair, the per-run ledger a policy sees |
| `strategies.py` | the failure-handling strategies on round 3's time-aware BOFN (`Net3`) |
| `bench.py` | experiments and the runner (`results/*.jsonl`) |
| `analyze.py`, `figures.py` | statistics (paired, bootstrap, sign-flip, Holm) and figures |
| `calibrate_region.py` | places the hidden region against the twin's oracle (`results/region_calibration.json`) |
| `test_twin_failures.py` | 16 checks, among them that the `twin` regime reproduces round 3 run for run |

```bash
bash get_twin.sh                                    # -> /tmp/byu-vcl/vertical-lab
python -m venv /tmp/venv && /tmp/venv/bin/pip install numpy scipy scikit-learn scikit-image matplotlib pillow pytest botorch
export TWIN_DIR=/tmp/byu-vcl/vertical-lab
/tmp/venv/bin/python -m pytest -q test_twin_failures.py
TWIN_WORKERS=4 /tmp/venv/bin/python bench.py run main base region diag
/tmp/venv/bin/python analyze.py --figs
```
