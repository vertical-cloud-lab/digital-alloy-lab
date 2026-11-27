"""Markdown version of the comparison rows that have a Thermo-Calc or experimental value (for REPORT.md)."""
import os
import pandas as pd, numpy as np, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
d = pd.read_csv(os.path.join(OUT, 'data', 'comparison.csv'))
def short_db(s):
    s = str(s)
    if s.startswith('mc_al'): return 'mc_al 2.032'
    if s.startswith('mc_ni'): return 'mc_ni 2.036'
    return s.replace('SGTE binary ', 'SGTE ').replace('.tdb', '')
def f(x, frac=False):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return '' if (x is None or (isinstance(x, float) and np.isnan(x))) else str(x)
    if np.isnan(x): return ''
    return f'{x:.4f}' if frac else f'{x:.1f}'
keep = d[d.thermocalc_value.notna() | d.experiment_value.notna()]
lines = ['| System / alloy | Quantity | pycalphad | Database | Thermo-Calc (db; DOI) | Experiment (source) | Δ vs TC | Δ vs exp |',
         '|---|---|---|---|---|---|---|---|']
for _, r in keep.iterrows():
    fr = 'fraction' in r.quantity
    tc = f(r.thermocalc_value, fr)
    if tc:
        tc += f" ({str(r.thermocalc_db).split('(')[0].strip()}; doi:{r.thermocalc_source_doi})"
    ex = f(r.experiment_value, fr)
    if ex:
        src = str(r.experiment_source)
        src = src.replace('ORCHID literature record (CC BY 4.0), paper doi:', 'ORCHID, doi:')
        ex += f' ({src.split(" (")[0] if src.startswith("ORCHID") else src.split(",")[0] if "DSC" in src else "CDA handbook" if "CDA" in src else "handbook data sheet"})'
    lines.append(f"| {r.system_or_alloy} | {r.quantity} | {f(r.pycalphad_value, fr)} | {short_db(r.database)} | {tc} | {ex} | {f(r.delta_pycalphad_vs_tc, fr)} | {f(r.delta_pycalphad_vs_exp, fr)} |")
open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/arroyave/work/pycalphad-al-cu/table_tc_exp.md', 'w').write('\n'.join(lines) + '\n')
print(len(lines) - 2, 'rows')
