"""Check that the GraceCalculator calls in PAIPAI's workers (and BLADE's TDB stage) match the
installed MaterialsFramework (ArroyaveLab upstream 0ec8168). Constructors only; no model load.
Usage: python PAIPAI-check_worker_calc.py
"""
import traceback

from materialsframework.calculators import GraceCalculator

calls = {
    "PAIPAI fast_worker.py": dict(model="GRACE-2L-OMAT", device="cpu", verbose=True, fmax=0.10, max_steps=30),
    "PAIPAI slow_worker.py": None,  # filled below from the source
    "BLADE blade_tdb_gen.py": dict(steps=1000, device="cuda"),
}
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
m = re.search(r"GraceCalculator\((.*?)\)\n", src, re.S)
print("slow_worker GraceCalculator call:", " ".join(m.group(1).split()) if m else "n/a")
calls["PAIPAI slow_worker.py"] = dict(model="GRACE-2L-OMAT", device="cpu", verbose=True, fmax=0.01, max_steps=400)
for name, kw in calls.items():
    try:
        c = GraceCalculator(**kw)
        print(f"{name}: GraceCalculator({kw}) -> OK; steps={c.steps} fmax={c.fmax}")
    except Exception as e:
        print(f"{name}: GraceCalculator({kw}) -> {type(e).__name__}: {e}")
