"""Step-by-step equivalent of sqscal's FCC branch (after runstruct_vasp -nr failed to write POSCAR),
plus MaterialsFramework EOS of fcc Al/Cu/Ni, all with MaterialsFramework's GraceCalculator (GRACE-2L-OMAT, CPU).
Usage: python PhaseForge-mlip_stepwise.py <sqs_root_dir> <out.json>"""
import json, sys, time, glob, os
import numpy as np
from pymatgen.io.atat import Mcsqs
from pymatgen.core import Structure, Lattice
from ase.eos import EquationOfState
from materialsframework.calculators import GraceCalculator

root, out = sys.argv[1], sys.argv[2]
res = {"timings_s": {}}
t0 = time.time()
calc = GraceCalculator(model="GRACE-2L-OMAT", fmax=0.005)
res["timings_s"]["model_load"] = time.time() - t0

# EOS for fcc elements (primitive cell, 9 volumes within +-6 %)
for el, a_guess in [("Al", 4.04), ("Cu", 3.63), ("Ni", 3.52)]:
    t = time.time(); vols, ens = [], []
    for s in np.linspace(0.94, 1.06, 9):
        st = Structure(Lattice.cubic(a_guess * s ** (1 / 3)), [el] * 4,
                       [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]])
        r = calc.calculate(st)
        vols.append(st.volume / 4); ens.append(float(r["energy"]) / 4)
    eos = EquationOfState(vols, ens, eos="birchmurnaghan")
    v0, e0, B = eos.fit()
    res[f"eos_{el}"] = {"a0_A": (4 * v0) ** (1 / 3), "B_GPa": B * 160.21766, "E0_eV_per_atom": e0}
    res["timings_s"][f"eos_{el}"] = time.time() - t
    print(el, res[f"eos_{el}"], flush=True)

# relax the ATAT SQS (lev 0 endmembers + lev 1 x=0.5, 32 atoms), full cell, fmax 0.005 eV/A
for d in sorted(glob.glob(os.path.join(root, "sqs_lev=*"))):
    t = time.time()
    st = Mcsqs.structure_from_str(open(os.path.join(d, "str.out")).read())
    # ATAT str.out has unit-less lattice; scale to a Vegard-like volume (Cu 3.615, Ni 3.524 A fcc)
    comp = st.composition.fractional_composition
    a = 3.615 * comp["Cu"] + 3.524 * comp["Ni"]
    st.scale_lattice(len(st) * a ** 3 / 4)
    r = calc.relax(st)
    n = len(st)
    res[os.path.basename(d)] = {"n_atoms": n, "E_eV_per_atom": float(r["energy"]) / n,
                                "x_Ni": comp["Ni"], "V_A3_per_atom": r["final_structure"].volume / n}
    res["timings_s"][os.path.basename(d)] = time.time() - t
    print(os.path.basename(d), res[os.path.basename(d)], f"{time.time()-t:.1f}s", flush=True)
    json.dump(res, open(out, "w"), indent=1)

json.dump(res, open(out, "w"), indent=1)
