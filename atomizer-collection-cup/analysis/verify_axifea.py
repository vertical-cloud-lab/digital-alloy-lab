"""Check the axisymmetric CalculiX set-up against closed-form answers before trusting the cup models.

    python analysis/verify_axifea.py     # writes analysis/out/verify.json

1. Steady conduction through a tube wall (inner face held hot, outer face cooled by a film): the outer
   temperature against the series-resistance answer. Tests axisymmetry and the film face labels.
2. The same tube cooled by radiation alone: outer temperature against the solved energy balance.
   Tests *RADIATE, the Stefan-Boltzmann constant and the absolute-zero offset.
3. Transient: a solid steel cylinder dropped into a film (lumped, Biot < 0.1): T(t) against the
   exponential. Tests density, specific heat and the time stepping.
4. Surface flux: a uniform *DFLUX on the outer face of the tube with the inner face held: the
   temperature rise against q * r_o * ln(r_o/r_i) / k. Tests the S-face labels used for radiation input.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import axifea as F  # noqa: E402

OUT = HERE / "out" / "verify"
OUT.mkdir(parents=True, exist_ok=True)


def tube_model(ri=20.0, ro=30.0, h=10.0, size=1.0):
    return F.build_mesh([F.Region("tube", "steel", [(ri, 0), (ro, 0), (ro, h), (ri, h)], size=size)])


def header(f, k=16.0, rho=8000, cp=500):
    f.write("*HEADING\nverify\n")


def material(f, k=16.0, rho=8000, cp=500):
    f.write(f"*MATERIAL, NAME=STEEL\n*CONDUCTIVITY\n{k}\n*DENSITY\n{rho * F.KG_M3:.4e}\n"
            f"*SPECIFIC HEAT\n{cp * F.J_PER_KGK:.4e}\n*SOLID SECTION, ELSET=E_tube, MATERIAL=STEEL\n")
    f.write(f"*PHYSICAL CONSTANTS, ABSOLUTE ZERO={F.ABS0}, STEFAN BOLTZMANN={F.SIGMA}\n")


def faces(m, test):
    return [e for e in m.edges if test(e)]


def steady(case, ri=20.0, ro=30.0, Ti=500.0, Tinf=20.0, k=16.0, hW=50.0, eps=None, q=None):
    m = tube_model(ri, ro)
    inner = sorted({n for e in faces(m, lambda e: abs(e["mid"][0] - ri) < 1e-6) for n in e["n"]})
    outer_f = faces(m, lambda e: abs(e["mid"][0] - ro) < 1e-6)
    outer_n = sorted({n for e in outer_f for n in e["n"]})
    job = f"verify_{case}"
    with open(OUT / f"{job}.inp", "w") as f:
        header(f)
        F.write_mesh(f, m)
        F.write_set(f, "NSET", "INNER", inner)
        F.write_set(f, "NSET", "OUTER", outer_n)
        material(f, k)
        f.write("*STEP\n*HEAT TRANSFER, STEADY STATE\n1., 1.\n*BOUNDARY\nINNER, 11, 11, %g\n" % Ti)
        if hW:
            f.write("*FILM\n")
            for e in outer_f:
                f.write(f"{e['elem']}, F{e['face']}, {Tinf}, {hW * F.W_M2K:.6e}\n")
        if eps:
            f.write("*RADIATE\n")
            for e in outer_f:
                f.write(f"{e['elem']}, R{e['face']}, {Tinf}, {eps}\n")
        if q:
            f.write("*DFLUX\n")
            for e in outer_f:
                f.write(f"{e['elem']}, S{e['face']}, {q:.6e}\n")
        f.write("*NODE PRINT, NSET=OUTER\nNT\n*END STEP\n")
    F.run_ccx(job, OUT)
    blocks = F.read_dat_blocks(OUT / f"{job}.dat")
    (t, vals), = blocks[next(k for k in blocks if k[1] == "OUTER")]
    return float(np.mean([v[0] for v in vals.values()]))


def transient(R=10.0, H=20.0, T0=800.0, Tinf=20.0, hW=20.0, k=16.0, rho=8000, cp=500, t_end=600.0):
    m = F.build_mesh([F.Region("tube", "steel", [(0, 0), (R, 0), (R, H), (0, H)], size=2.0)])
    ext = faces(m, lambda e: e["mid"][0] > 1e-6)
    job = "verify_transient"
    with open(OUT / f"{job}.inp", "w") as f:
        header(f)
        F.write_mesh(f, m)
        material(f, k, rho, cp)
        f.write(f"*INITIAL CONDITIONS, TYPE=TEMPERATURE\nNALL, {T0}\n")
        f.write(f"*STEP, INC=10000\n*HEAT TRANSFER, DELTMX=5\n1., {t_end}, 0.01, 20.\n*FILM\n")
        for e in ext:
            f.write(f"{e['elem']}, F{e['face']}, {Tinf}, {hW * F.W_M2K:.6e}\n")
        f.write(f"*NODE PRINT, NSET=NALL, TIME POINTS=TP\nNT\n*END STEP\n")
    txt = (OUT / f"{job}.inp").read_text().replace("*STEP", f"*TIME POINTS, NAME=TP\n{t_end / 2}, {t_end}\n*STEP", 1)
    (OUT / f"{job}.inp").write_text(txt)
    F.run_ccx(job, OUT)
    blocks = F.read_dat_blocks(OUT / f"{job}.dat")
    series = blocks[next(k for k in blocks if k[1] == "NALL")]
    t, vals = series[-1]
    T_fe = float(np.mean([v[0] for v in vals.values()]))
    A = 2 * math.pi * R * H + 2 * math.pi * R ** 2
    V = math.pi * R ** 2 * H
    tau = rho * F.KG_M3 * cp * F.J_PER_KGK * V / (hW * F.W_M2K * A)
    T_an = Tinf + (T0 - Tinf) * math.exp(-t / tau)
    return T_fe, T_an, t


def main():
    res = {}
    ri, ro, Ti, Tinf, k, h = 20.0, 30.0, 500.0, 20.0, 16.0, 50.0
    Rw = math.log(ro / ri) / (2 * math.pi * k)
    Rf = 1 / (2 * math.pi * ro * h * F.W_M2K)
    To_an = Tinf + (Ti - Tinf) * Rf / (Rw + Rf)
    res["film"] = dict(fe=steady("film", ri, ro, Ti, Tinf, k, h), analytic=To_an)
    eps = 0.5

    def bal(To):
        q_cond = (Ti - To) / Rw
        q_rad = 2 * math.pi * ro * eps * F.SIGMA * ((To + 273.15) ** 4 - (Tinf + 273.15) ** 4)
        return q_cond - q_rad
    res["radiation"] = dict(fe=steady("rad", ri, ro, Ti, Tinf, k, 0.0, eps=eps), analytic=brentq(bal, Tinf, Ti))
    q = 0.05   # mW/mm2 = 50 kW/m2
    res["dflux"] = dict(fe=steady("dflux", ri, ro, 100.0, Tinf, k, 0.0, q=q),
                        analytic=100.0 + q * ro * math.log(ro / ri) / k)
    fe, an, t = transient()
    res["transient"] = dict(fe=fe, analytic=an, t=t)
    for kk, v in res.items():
        v["error_K"] = round(v["fe"] - v["analytic"], 3)
        v["fe"], v["analytic"] = round(v["fe"], 3), round(v["analytic"], 3)
        print(f"{kk:>10s}: FE {v['fe']:9.3f}  closed form {v['analytic']:9.3f}  error {v['error_K']:+.3f} K")
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out" / "verify.json").write_text(json.dumps(res, indent=2) + "\n")


if __name__ == "__main__":
    main()
