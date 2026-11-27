"""Call BLADE 9d3859c's BladeTDBGen.fit() on the SQS tree made by BLADE-run_sqs_small.py,
against ArroyaveLab MaterialsFramework 0ec8168 (upstream, not the ichasekatz fork BLADE names).
Usage: python BLADE-tdb_stage_check.py <scratch_root_with_BLADE/SQS>
"""
import sys
import traceback
from pathlib import Path

from blade.tools.blade_tdb_gen import BladeTDBGen

root = Path(sys.argv[1]).resolve()
(root / "sqsdb").mkdir(exist_ok=True)
gen = BladeTDBGen(
    phases=[{"generator_name": "HEDB", "lattice": "HEDB1", "supercell_size": (2, 2, 2)}],
    liquid=False,
    paths=[root, root / "BLADE", root / "sqsdb"],
    composition_list=[["Cr", "Hf"]],
    level=3,
    sqsgen_levels2=[{"element": "B", "compositions": "1.0", "letter": "b", "count": "2"}],
    skip_existing=False,
)
try:
    gen.fit()
except Exception:
    traceback.print_exc()
    sys.exit(1)
