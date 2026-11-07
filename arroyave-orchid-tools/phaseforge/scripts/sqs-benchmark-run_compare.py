"""Run sqs-benchmark's scripts/compare_methods.py with its hard-coded config re-pointed.

compare_methods.py (b44ba79) hard-codes path0 = /Users/..., path2 = <path0>/PhaseForge/.../sqsdb
and n_runs = 10, and calls out_dir.mkdir() at import time (PermissionError on Linux).
This wrapper reads the repo file, substitutes only those three assignments, and executes it
unchanged otherwise. path2 is pointed at the BladeSQS staging tree written by
sqs-benchmark-mini.py (<root>/BLADE/SQS), which holds BCCmcsqs{i}_3/ and the reference
clusters.out / rndstr.in that compare_methods.py takes from BCCmcsqs1_3.
Usage: python sqs-benchmark-run_compare.py <compare_methods.py> <root> <n_runs>
"""

import re
import sys
from pathlib import Path

script = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve()
n_runs = int(sys.argv[3])

src = script.read_text()
subs = {
    r'path0 = Path\("/Users/[^"]*"\)': f'path0 = Path("{root}")',
    r'path2 = path0 / "PhaseForge" / "PhaseForge" / "atat" / "data" / "sqsdb"': 'path2 = path1 / "SQS"',
    r"n_runs = 10\n": f"n_runs = {n_runs}\n",
}
for pattern, new in subs.items():
    src, n = re.subn(pattern, lambda _m, new=new: new, src, count=1)
    if n != 1:
        raise SystemExit(f"pattern not found in {script.name}: {pattern!r}")

sys.argv = [str(script)]
exec(compile(src, str(script), "exec"), {"__name__": "__main__", "__file__": str(script)})
