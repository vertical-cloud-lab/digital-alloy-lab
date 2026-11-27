"""One objective evaluation of the Pt-W example with the PyPI install (pip install phaseforgeplus)."""
import sys
import time
import traceback
from importlib.metadata import version

import numpy as np

from phaseforgeplus import PhaseForgePlus
from phaseforgeplus.utils.objective import objective_function

d = sys.argv[1]
print("phaseforgeplus", version("phaseforgeplus"), "espei", version("espei"), "pycalphad", version("pycalphad"), flush=True)
pfp = PhaseForgePlus(db=d + "/pt-w.tdb", zpf_path=d, points=[1801, 1601, 1401, 1201, 1001, 802, 602, 402, 202],
                     pressure=101325, temperature=298.15)
x0 = pfp.get_initial_values()
func = objective_function(pfp.db, pfp.db_zpf, pfp.db_neq)
t = time.time()
try:
    f, g = func(x0)
    print("objective OK", f, np.linalg.norm(g), round(time.time() - t, 1), "s")
except Exception as e:
    traceback.print_exc(limit=-3)
    print("objective FAILED:", type(e).__name__, e)
