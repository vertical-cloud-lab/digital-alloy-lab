"""Does the PhaseForgePlus NEQ ("MLIP regularizer") data work once the two visible bugs are patched?
Patches (in memory only): phases -> [phase], 'sublattice_configuraations' -> 'sublattice_configurations';
with a third argument "reshape", values (1, n) -> (1, 1, n) as ESPEI expects (P, T, configs)."""
import json
import sys
import traceback

import numpy as np
from espei.error_functions.non_equilibrium_thermochemical_error import FixedConfigurationPropertyResidual
from espei.utils import MemoryStorage, PickleableTinyDB, database_symbols_to_fit
from pycalphad import Database

from phaseforgeplus import PhaseForgePlus

d, summary_json = sys.argv[1], sys.argv[2]
pts = [1801, 1601, 1401, 1201, 1001, 802, 602, 402, 202]
pfp = PhaseForgePlus(db=d + "/pt-w.tdb", zpf_path=d, points=pts, pressure=101325, temperature=298.15)
syms = database_symbols_to_fit(pfp.db)
x0 = np.asarray(pfp.get_initial_values(), dtype=float)
b0 = pfp.db_neq.all()[0]
out = {"block_components": b0["components"], "first_configuration": b0["solver"]["sublattice_configuraations"][0],
       "values_shape": list(np.shape(b0["values"])), "occupancies_shape": list(np.shape(b0["solver"]["sublattice_occupancies"]))}
fixed = PickleableTinyDB(storage=MemoryStorage)
for b in pfp.db_neq.all():
    b = json.loads(json.dumps(b))
    b["phases"] = [b["phases"]]
    b["solver"]["sublattice_configurations"] = b["solver"].pop("sublattice_configuraations")
    if len(sys.argv) > 3 and sys.argv[3] == "reshape":
        b["values"] = [b["values"]]
    fixed.insert(b)
try:
    neq = FixedConfigurationPropertyResidual(Database(d + "/pt-w.tdb"), fixed, phase_models=None, symbols_to_fit=syms)
    out["blocks_used_after_patch"] = len(neq.thermochemical_data)
    out["configs_kept_per_block"] = [len(t["calculate_dict"]["values"]) for t in neq.thermochemical_data]
    ln, gn = neq.get_likelihood(x0)
    out["neq_loglik_x0"], out["neq_grad_norm_x0"] = float(ln), float(np.linalg.norm(gn))
    best = np.array([v["best"] for v in json.load(open(summary_json))["params"].values()])
    ln, gn = neq.get_likelihood(best)
    out["neq_loglik_ptw_tuned"], out["neq_grad_norm_ptw_tuned"] = float(ln), float(np.linalg.norm(gn))
except Exception as e:
    out["error"] = f"{type(e).__name__}: {e}"
    traceback.print_exc(limit=-2)
print(json.dumps(out, indent=1))
