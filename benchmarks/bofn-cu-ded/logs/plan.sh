#!/bin/bash
# The sweep in priority order (headline first); each step is resumable.
cd "$(dirname "$0")/.."
python run_sweep.py --cells 1,1 --seeds 0-19 --kinds pkgfn eifn eifn_reuse tiered ei random
python run_sweep.py --cells 1,1 --seeds 0-7 --kinds pkgfn_screen pkgfn_audit mines_only funnel
python run_sweep.py --cells 0,0 --seeds 0-11 --kinds pkgfn eifn eifn_reuse tiered ei random
python run_sweep.py --cells 1,0 0,1 --seeds 0-7 --kinds pkgfn eifn eifn_reuse tiered ei random
python run_sweep.py --cells 0,0 1,0 0,1 --seeds 0-7 --kinds pkgfn_audit pkgfn_screen funnel
python run_sweep.py --cells 1,1 --seeds 8-19 --kinds pkgfn_screen pkgfn_audit mines_only funnel
