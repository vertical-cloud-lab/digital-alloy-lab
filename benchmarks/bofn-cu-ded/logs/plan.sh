#!/bin/bash
# The sweep in priority order (headline first); each step is resumable.
cd "$(dirname "$0")/.."
while pgrep -f "run_sweep.py --cells 1,1 --seeds 0-19" > /dev/null; do sleep 20; done  # a running headline step (restart only)
python run_sweep.py --cells 1,1 --seeds 0-19 --kinds pkgfn eifn eifn_reuse tiered ei random
python run_sweep.py --cells 0,0 --seeds 0-11 --kinds pkgfn eifn eifn_reuse tiered ei random
python run_sweep.py --cells 1,1 --seeds 0-7 --kinds pkgfn_screen pkgfn_audit mines_only funnel
python run_sweep.py --cells 1,0 0,1 --seeds 0-7 --kinds pkgfn eifn eifn_reuse tiered ei random
python run_sweep.py --cells 0,0 1,0 0,1 --seeds 0-7 --kinds pkgfn_audit pkgfn_screen funnel
python run_sweep.py --cells 1,1 --seeds 8-19 --kinds pkgfn_screen pkgfn_audit mines_only funnel
BOFN_SACQ=256 python run_sweep.py --cells 1,1 --seeds 0-3 --kinds pkgfn --out quality/results-hq/sacq256  # fidelity check
