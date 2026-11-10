"""Time GRACE-2L-OMAT on one candidate the PAIPAI master generated from the shipped
example/struc.in (254 atoms: Nb113 Ta63 Ti37 Hf37 + B2 O2), on 1 CPU thread, to estimate what
the full example would cost. Uses the same MaterialsFramework GraceCalculator as the workers.
Usage: python PAIPAI-time_example_size.py <POSCAR> [n_fire_steps]
"""
import sys
import time

from pymatgen.core import Structure

from materialsframework.calculators.grace import GraceCalculator

s = Structure.from_file(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
calc = GraceCalculator(model="GRACE-2L-OMAT", fmax=0.1, steps=n)
t0 = time.time()
calc.calculator  # build the model
t1 = time.time()
r = calc.relax(s)
t2 = time.time()
r2 = calc.relax(s)
t3 = time.time()
print(f"atoms={len(s)} formula={s.composition.formula}")
print(f"model load {t1 - t0:.1f} s; first relax ({n} FIRE steps, includes graph build) {t2 - t1:.1f} s; "
      f"second relax ({n} steps) {t3 - t2:.1f} s -> {(t3 - t2) / (n + 1):.2f} s per force call")
print(f"E after {n} steps = {r2['energy']:.4f} eV ({r2['energy'] / len(s):.4f} eV/atom)")
