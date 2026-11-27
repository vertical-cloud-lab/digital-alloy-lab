"""Make a copy of Phase-Compatibility-Model-NiTi/main.ipynb with one extra first cell: a
compatibility shim so helper.py (written for HEACalculator 1.x: HEACalculator(alloy, csv=True)
.get_csv_list()) runs against HEACalculator 2.x, the only series on PyPI.

Usage: python -I niti_pc_add_shim.py <main.ipynb> <out.ipynb>
"""
import json
import sys

SHIM = '''# --- compatibility shim added by the test harness (NOT part of the original repo) ---
import HEACalculator as _H


class _CompatHEACalculator(_H.HEACalculator):
    """Accept the 1.x `csv=` kwarg and provide get_csv_list() in the column order helper.py expects."""

    def __init__(self, formula, csv=False):
        super().__init__(formula)

    def get_csv_list(self):
        d = self.get_dict()
        return [d["formula"], d["density"], d["delta"], d["omega"], d["gamma"], d["lambda"],
                d["vec"], d["mixing_enthalpy"], d["mixing_entropy"], d["melting_temperature"]]


_H.HEACalculator = _CompatHEACalculator
'''

nb = json.load(open(sys.argv[1]))
cell = {"cell_type": "code", "execution_count": None, "id": "compat-shim", "metadata": {}, "outputs": [],
        "source": SHIM.splitlines(keepends=True)}
nb["cells"].insert(0, cell)
json.dump(nb, open(sys.argv[2], "w"), indent=1)
