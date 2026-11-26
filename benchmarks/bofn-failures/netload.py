"""Load one of the vendored networks (aluminum LPBF or copper DED) in this process.

The two networks both call their module `bofn_alloy`, so only one can be imported per process.
`load("al")`, `load("cu-toy")` or `load("cu-phys")` puts the right folder on sys.path, sets the
copper truth's environment switch, imports the modules and returns them. run_sweep.py starts a
fresh process for every run, so each run loads exactly one network.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
NETS = ("al", "cu-toy", "cu-phys")


class Net:
    """The pieces of one network that the failure-aware policies use."""

    def __init__(self, name: str):
        if name not in NETS:
            raise ValueError(f"network {name!r}: expected one of {NETS}")
        self.name = name
        self.family = "al" if name == "al" else "cu"
        loaded = sys.modules.get("bofn_alloy")
        if loaded is not None and Path(loaded.__file__).resolve().parent != VENDOR / self.family:
            raise RuntimeError("another network's bofn_alloy is already imported in this process")
        if self.family == "cu":
            want = "phys" if name == "cu-phys" else "toy"
            if loaded is not None and loaded.TRUTH != want:
                raise RuntimeError("the copper network is already imported with the other truth")
            os.environ["BOFN_TRUTH"] = want
        folder = str(VENDOR / self.family)
        if folder not in sys.path:
            sys.path.insert(0, folder)
        self.BA = importlib.import_module("bofn_alloy")
        self.POL = importlib.import_module("policies")
        BA = self.BA
        self.D, self.COMP, self.IA, self.IPV = BA.D, BA.COMP, BA.IA, BA.IPV
        self.SPEC, self.ORDER, self.GROUPS = BA.SPEC, BA.ORDER, BA.GROUPS
        self.COSTS = BA.COSTS
        self.LAMBDA = BA.LAMBDA

    def truth(self, kappa: float, eta: float = 1.0):
        if self.family == "al":
            return self.BA.AlloyTruth(kappa)
        return self.BA.make_truth(kappa, eta)

    def objective(self, truth, X):
        """True objective at designs X [n, D] (both networks take a batch)."""
        return truth.objective(X)

    def feasible(self, X):
        """Rows of X inside the search-space limits (only the copper physics truth has any)."""
        if self.family == "cu":
            return self.POL.feas(X)
        return X


def load(name: str) -> Net:
    return Net(name)
