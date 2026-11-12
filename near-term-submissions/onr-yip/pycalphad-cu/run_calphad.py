#!/usr/bin/env python3
"""Preliminary pycalphad calculations for Cu-Ni and Cu-Al-Ni-Fe(-Mn) alloys (ONR YIP 2027).

Open database only: MatCalc mc_ni v2.036 (TU Wien, ODbL 1.0), copied next to this script
(downloaded and sha256-checked if missing). Nothing from Thermo-Calc TCCU is used.

    python run_calphad.py               # all calculations, CSVs, figures (about 2 to 3 min)
    python run_calphad.py --crosscheck  # also the three reference alloys with mc_fe v2.062
                                        # and COST 507 (pycalphad's bundled copy)
    python run_calphad.py --figures-only

Outputs (in this folder): reference_alloys.csv, nab_phase_fractions.csv, composition_map.csv,
crosscheck.csv (with --crosscheck), cu_calphad_prelim.{png,pdf}, cu_map.{png,pdf},
cu_panel2.{png,pdf}.
"""
import argparse
import hashlib
import os
import re
import sys
import tempfile
import time
import urllib.request
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))

TDBS = {
    'mc_ni': dict(file='mc_ni_v2036.tdb',
                  url='https://www.matcalc.at/images/stories/Download/Database/mc_ni_v2036.tdb',
                  sha256='84ba813156e1f7d8bde495d74420319afec03572b981f6b56103807f305313ab'),
    'mc_fe': dict(file='mc_fe_v2062.tdb',
                  url='https://www.matcalc.at/images/stories/Download/Database/mc_fe_v2062.tdb',
                  sha256='aa02077eac3f602dd7479cbeafb09b450e282716752b3ae2b1fc3a57d9c64865'),
}
COST507_SHA256 = '6565f4d67695fbbf779d68b9eeeb83e86e44a1a3dde9bafd612d99daffb9c34d'

ELEMENTS = ['AL', 'CU', 'FE', 'MN', 'NI']
# Phases plausible in Cu-rich Cu-Ni-Al-Fe-Mn alloys. Excluded: carbides/borides/nitrides (no C, B, N),
# Ni3Ti/Ni3Nb/Laves/sigma-type phases (no Ti, Nb, Mo, Cr), and alpha-/beta-Mn, which came out
# spuriously stable in plain Cu-Ni (Mn-phase parameters are not meant for Cu-Ni).
PHASES = {
    'mc_ni': ['LIQUID', 'FCC_A1', 'BCC_A2', 'NIAL', 'GAMMA_PRIME', 'HCP_A3'],
    'mc_fe': ['LIQUID', 'FCC_A1', 'BCC_A2', 'BCC_B2', 'HCP_A3'],
    'cost507': ['LIQUID', 'FCC_A1', 'BCC_A2', 'BCC_B2', 'HCP_A3'],
}
MW = {'AL': 26.9815385, 'CU': 63.546, 'FE': 55.845, 'MN': 54.938044, 'NI': 58.6934}
P0 = 101325.0

# Nominal compositions (wt%, balance Cu) and CDA handbook melting ranges (deg C)
ALLOYS = [
    dict(alloy='C71500 70-30 Cu-Ni', wt={'NI': 30.0, 'FE': 0.6, 'MN': 0.6}, hb_sol=1171, hb_liq=1238),
    dict(alloy='C70600 90-10 Cu-Ni', wt={'NI': 10.0, 'FE': 1.4, 'MN': 0.8}, hb_sol=1099, hb_liq=1149),
    dict(alloy='C95800 NAB', wt={'AL': 9.2, 'NI': 4.5, 'FE': 4.0, 'MN': 1.2}, hb_sol=1043, hb_liq=1060),
]
MAP_NI = [0, 5, 10, 15, 20, 25, 30]
MAP_AL = [0.0, 1.9, 3.8, 5.7, 7.6, 9.5]
MAP_FE = 1.0


# ----------------------------------------------------------------------------- database handling
def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def get_tdb(key):
    meta = TDBS[key]
    path = os.path.join(HERE, meta['file'])
    if not os.path.exists(path):  # cross-check database: cached outside the repository
        cache = os.environ.get('CU_CALPHAD_CACHE', os.path.join(tempfile.gettempdir(), 'cu_calphad_tdb'))
        path = os.path.join(cache, meta['file'])
        if not os.path.exists(path):
            os.makedirs(cache, exist_ok=True)
            print(f'downloading {meta["url"]}')
            req = urllib.request.Request(meta['url'], headers={'User-Agent': 'Mozilla/5.0 (pycalphad script)'})
            with urllib.request.urlopen(req, timeout=120) as r, open(path, 'wb') as f:
                f.write(r.read())
    if sha256(path) != meta['sha256']:
        raise RuntimeError(f'{path}: sha256 mismatch (expected {meta["sha256"]})')
    return path


KEEP = {'ELEMENT', 'SPECIES', 'FUNCTION', 'TYPE_DEFINITION', 'PHASE', 'CONSTITUENT', 'PARAMETER',
        'TEMP_LIM', 'DEFINE_SYSTEM_DEFAULT', 'DEFAULT_COMMAND'}
ABBREV = {'PARA': 'PARAMETER', 'PARAM': 'PARAMETER', 'FUNC': 'FUNCTION', 'FUNCT': 'FUNCTION',
          'CONST': 'CONSTITUENT', 'TYPE_DEF': 'TYPE_DEFINITION', 'ELEM': 'ELEMENT', 'SPEC': 'SPECIES'}
PARAM_TYPES = {'G', 'L', 'TC', 'BMAGN'}
PARAM_RE = re.compile(r'^PARAMETER\s+(\w+)\(\s*([^,;:()]+?)\s*,\s*([^;()]+?)\s*;\s*(\d+)\s*\)\s')


def clean_tdb_text(raw, elements=None):
    """MatCalc TDB -> the TDB subset pycalphad parses. Syntax only; no number is changed.

    * latin-1 -> ASCII; comments ($ to end of line) dropped
    * MatCalc ``ATTACH_CONTRIBUTION <ord> <dis> ORDER_DISORDER`` -> ``TYPE_DEFINITION c GES A_P_D
      <ord> DIS_PART <dis>`` (the same partitioned order/disorder model), c added to the phase
    * other MatCalc-only commands dropped (REFERENCE_ELEMENT, ADD_COMPOSITION_SET, ...);
      pycalphad finds composition sets itself
    * free-text description and priority (``> text >> n``) stripped from PHASE/CONSTITUENT
    * only G, L, TC, BMAGN parameters kept (HMVA etc. are MatCalc kinetic data)
    * ``REF:xxx`` tags -> ``REF_xxx``; a PARAMETER missing its closing ``!`` is split off
    * with ``elements``: parameters involving any other element are dropped (they cannot
      contribute in that subsystem); a malformed parameter inside the subsystem raises
    """
    keep_el = None if elements is None else {e.upper() for e in elements} | {'VA', '*'}
    txt = raw.replace('\r', '').encode('ascii', 'ignore').decode('ascii')
    lines = [l.split('$', 1)[0] for l in txt.split('\n')]
    cmds = []
    for c in ' '.join(lines).split('!'):
        cmds.extend(re.split(r'\s(?=PARAMETER\s+\w+\()', c))
    order_disorder = {}
    used = set()
    for c in cmds:
        t = c.split()
        if len(t) == 4 and t[0].upper() == 'ATTACH_CONTRIBUTION' and t[3].upper() == 'ORDER_DISORDER':
            order_disorder[t[1].upper()] = t[2].upper()
        if len(t) > 2 and t[0].upper() == 'PHASE':
            used.update(t[2])
    free = [ch for ch in 'QXZJKUWY1234567' if ch not in used]
    od_char, out = {}, []
    for ordered, disordered in order_disorder.items():
        od_char[ordered] = free.pop(0)
        out.append(f'TYPE_DEFINITION {od_char[ordered]} GES A_P_D {ordered} DIS_PART {disordered} !')
    for c in cmds:
        c = re.sub(r'\s+', ' ', c).strip()
        if not c:
            continue
        kw = ABBREV.get(c.split(' ', 1)[0].upper(), c.split(' ', 1)[0].upper())
        if kw not in KEEP:
            continue
        c = kw + c[len(c.split(' ', 1)[0]):]
        if kw in ('PHASE', 'CONSTITUENT'):
            c = c.split('>', 1)[0].strip()
        if kw == 'PHASE':
            t = c.split()
            if t[1].upper() in od_char:
                t[2] += od_char[t[1].upper()]
                c = ' '.join(t)
        if kw == 'PARAMETER':
            m = PARAM_RE.match(c)
            if not m:
                toks = set(re.findall(r'[A-Z][A-Z]?', c.split(')', 1)[0].split('(', 1)[-1].upper()))
                if keep_el is not None and not toks <= keep_el:
                    continue
                raise ValueError('malformed PARAMETER in the requested subsystem: ' + c[:120])
            if m.group(1).upper() not in PARAM_TYPES:
                continue
            if keep_el is not None:
                species = {s.strip().rstrip('%').upper() for sub in m.group(3).split(':') for s in sub.split(',')}
                if not species <= keep_el:
                    continue
        c = re.sub(r'REF:\s*(\S+)', r'REF_\1', c)
        out.append(c + ' !')
    return '\n'.join(out) + '\n'


def load_db(key):
    from pycalphad import Database
    if key == 'cost507':
        import pycalphad
        path = os.path.join(os.path.dirname(pycalphad.__file__), 'tests', 'databases', 'COST507.tdb')
        if sha256(path) != COST507_SHA256:
            print(f'warning: {path} differs from the copy used for the README (sha256)')
        return Database(path)
    raw = open(get_tdb(key), encoding='latin-1').read()
    return Database.from_string(clean_tdb_text(raw, ELEMENTS), fmt='tdb')


# ----------------------------------------------------------------------------- thermodynamics
def wt_to_x(wt):
    n = {k: w / MW[k] for k, w in wt.items() if w > 0}
    s = sum(n.values())
    return {k: n[k] / s for k in n}


def setup(db, key, wt):
    from pycalphad.core.utils import filter_phases, unpack_species
    els = sorted(e for e in wt if wt[e] > 0 and e in db.elements)
    x = wt_to_x({e: wt[e] for e in els})
    comps = els + ['VA']
    phases = filter_phases(db, unpack_species(db, comps), [p for p in PHASES[key] if p in db.phases])
    return comps, x, phases


def equilibrium_at(db, comps, phases, x, T):
    from pycalphad import equilibrium, variables as v
    conds = {v.T: T, v.P: P0, v.N: 1.0}
    conds.update({v.X(e): x[e] for e in x if e != 'CU'})
    return equilibrium(db, comps, phases, conds)


def points(eq):
    """Per temperature: list of (phase, amount, {element: mole fraction})."""
    ph = eq.Phase.values.reshape(-1, eq.Phase.shape[-1])
    npv = eq.NP.values.reshape(-1, eq.NP.shape[-1])
    X = eq.X.values.reshape(-1, eq.X.shape[-2], eq.X.shape[-1])
    els = [str(c) for c in eq.component.values]
    res = []
    for i in range(ph.shape[0]):
        res.append([(str(p), float(npv[i][j]), {e: float(X[i][j][k]) for k, e in enumerate(els)})
                    for j, p in enumerate(ph[i]) if p != '' and np.isfinite(npv[i][j])])
    return res


def liquid_fraction(eq):
    return np.array([sum(a for p, a, _ in pt if p == 'LIQUID') if pt else np.nan for pt in points(eq)])


def melting_range(db, comps, phases, x, t_hi=1750.0, t_lo=900.0, step=10.0, tol=0.1, eps=1e-4):
    """Equilibrium liquidus (first solid) and solidus (liquid gone), deg C; coarse scan + bisection."""
    T = np.arange(t_hi, t_lo - 0.5 * step, -step)
    fl = liquid_fraction(equilibrium_at(db, comps, phases, x, T))

    def bisect(lo, hi, pred):
        while hi - lo > tol:
            mid = 0.5 * (lo + hi)
            f = liquid_fraction(equilibrium_at(db, comps, phases, x, [mid]))[0]
            lo, hi = (mid, hi) if pred(f) else (lo, mid)
        return 0.5 * (lo + hi)

    out = []
    for pred in (lambda f: f < 1 - eps, lambda f: f < eps):
        idx = np.where(pred(np.nan_to_num(fl, nan=0.5)))[0]
        out.append(np.nan if len(idx) == 0 or idx[0] == 0 else bisect(T[idx[0]], T[idx[0] - 1], pred) - 273.15)
    liq, sol = out
    primary = ''
    if np.isfinite(liq):
        pt = points(equilibrium_at(db, comps, phases, x, [liq + 273.15 - 1.0]))[0]
        primary = '+'.join(sorted({'alpha (fcc)' if p == 'FCC_A1' else label(p, xx)
                                   for p, a, xx in pt if p != 'LIQUID' and a > 1e-6}))
    return liq, sol, primary


def scheil_range(db, comps, phases, x, start_K):
    from pycalphad import variables as v
    from scheil import simulate_scheil_solidification
    res = simulate_scheil_solidification(db, comps, phases, {v.X(e): x[e] for e in x if e != 'CU'},
                                         start_K, step_temperature=1.0)
    T = np.array(res.temperatures) - 273.15
    fl = np.array(res.fraction_liquid)
    first = T[np.argmax(fl < 0.9999)]
    t99 = T[np.argmax(fl <= 0.01)] if (fl <= 0.01).any() else np.nan
    return first, t99, T[-1], bool(res.converged)


def label(phase, xx):
    """Name a composition set the way the NAB literature would."""
    if phase == 'LIQUID':
        return 'liquid'
    if phase == 'FCC_A1':
        return 'alpha (fcc)' if xx.get('CU', 0) > 0.5 else 'fcc (Fe/Ni-rich)'
    if phase in ('BCC_A2', 'BCC_B2'):
        if xx.get('CU', 0) > 0.5:
            return 'beta (Cu-rich bcc)'
        return 'kappa Fe-rich bcc' if xx.get('FE', 0) >= xx.get('NI', 0) else 'kappa NiAl-type bcc'
    if phase == 'NIAL':
        return 'kappa NiAl (B2)'
    if phase == 'GAMMA_PRIME':
        return "gamma' Ni3Al"
    return phase


def wt_with_cu(wt):
    wt = dict(wt)
    wt['CU'] = 100.0 - sum(wt.values())
    return wt


# ----------------------------------------------------------------------------- calculations
def run_reference_alloys(db, key='mc_ni', do_scheil=True):
    rows = []
    for a in ALLOYS:
        wt = wt_with_cu(a['wt'])
        comps, x, phases = setup(db, key, wt)
        t0 = time.time()
        liq, sol, primary = melting_range(db, comps, phases, x)
        t_eq = time.time() - t0
        row = dict(database=key, alloy=a['alloy'],
                   composition_wt=' '.join(f'{e}{wt[e]:g}' for e in ['CU', 'NI', 'AL', 'FE', 'MN'] if e in wt),
                   handbook_solidus_C=a['hb_sol'], handbook_liquidus_C=a['hb_liq'],
                   handbook_range_C=a['hb_liq'] - a['hb_sol'],
                   eq_liquidus_C=round(liq, 1), eq_solidus_C=round(sol, 1), eq_range_C=round(liq - sol, 1),
                   eq_primary_phase=primary, eq_wall_s=round(t_eq, 2))
        if do_scheil:
            t0 = time.time()
            first, t99, tend, conv = scheil_range(db, comps, phases, x, liq + 273.15 + 30)
            row.update(scheil_first_solid_C=round(first, 1), scheil_T_at_99pct_solid_C=round(t99, 1),
                       scheil_end_C=round(tend, 1), scheil_range_C=round(first - t99, 1),
                       scheil_converged=conv, scheil_wall_s=round(time.time() - t0, 1))
        rows.append(row)
        print(f"  {key} {a['alloy']}: eq {sol:.1f}-{liq:.1f} C (handbook {a['hb_sol']}-{a['hb_liq']}), "
              f"primary {primary}", flush=True)
    return pd.DataFrame(rows)


def run_nab_fractions(db):
    a = ALLOYS[2]
    comps, x, phases = setup(db, 'mc_ni', wt_with_cu(a['wt']))
    T_C = np.arange(1150.0, 599.0, -2.0)
    pts = points(equilibrium_at(db, comps, phases, x, T_C + 273.15))
    cols = ['liquid', 'alpha (fcc)', 'beta (Cu-rich bcc)', 'kappa Fe-rich bcc', 'kappa NiAl (B2)',
            'kappa NiAl-type bcc', "gamma' Ni3Al", 'fcc (Fe/Ni-rich)', 'HCP_A3']
    rows = []
    for t, pt in zip(T_C, pts):
        r = dict(T_C=t, **{c: 0.0 for c in cols})
        for p, amt, xx in pt:
            r[label(p, xx)] = r.get(label(p, xx), 0.0) + amt
        rows.append(r)
    df = pd.DataFrame(rows)
    return df.loc[:, (df != 0).any(axis=0)]


def run_map(db):
    rows = []
    t_all = time.time()
    for ni in MAP_NI:
        for al in MAP_AL:
            wt = wt_with_cu({'NI': ni, 'AL': al, 'FE': MAP_FE})
            comps, x, phases = setup(db, 'mc_ni', wt)
            t0 = time.time()
            liq, sol, primary = melting_range(db, comps, phases, x)
            rows.append(dict(Ni_wt=ni, Al_wt=al, Fe_wt=MAP_FE, Cu_wt=round(wt['CU'], 2),
                             eq_liquidus_C=round(liq, 1), eq_solidus_C=round(sol, 1),
                             eq_range_C=round(liq - sol, 1), primary_phase=primary,
                             wall_s=round(time.time() - t0, 2)))
            print(f'  map Ni {ni} Al {al}: {sol:.0f}-{liq:.0f} C {primary} ({rows[-1]["wall_s"]} s)', flush=True)
    print(f'  map total {time.time() - t_all:.0f} s')
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- figures
OKABE_ITO = {'liquid': '#000000', 'alpha (fcc)': '#0072B2', 'beta (Cu-rich bcc)': '#D55E00',
             'kappa Fe-rich bcc': '#009E73', 'kappa NiAl (B2)': '#CC79A7'}
STYLE = {'liquid': (0, (4, 2)), 'alpha (fcc)': '-', 'beta (Cu-rich bcc)': '-',
         'kappa Fe-rich bcc': (0, (1, 1.2)), 'kappa NiAl (B2)': (0, (5, 1.5, 1, 1.5))}
SHORT = {'liquid': 'liquid', 'alpha (fcc)': r'$\alpha$ (fcc)', 'beta (Cu-rich bcc)': r'$\beta$ (Cu-rich bcc)',
         'kappa Fe-rich bcc': r'Fe-rich bcc ($\kappa_{I,II,IV}$)', 'kappa NiAl (B2)': r'NiAl B2 ($\kappa_{III}$)'}


def _style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'STIXGeneral', 'DejaVu Serif'],
                         'mathtext.fontset': 'stix', 'font.size': 8, 'axes.labelsize': 8, 'xtick.labelsize': 8,
                         'ytick.labelsize': 8, 'legend.fontsize': 7.5, 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'pdf.fonttype': 42, 'ps.fonttype': 42})
    return plt


def draw_map(ax, fig, m, ref):
    ni = np.array(sorted(m.Ni_wt.unique())); al = np.array(sorted(m.Al_wt.unique()))
    L = m.pivot(index='Al_wt', columns='Ni_wt', values='eq_liquidus_C').loc[al, ni].values
    R = m.pivot(index='Al_wt', columns='Ni_wt', values='eq_range_C').loc[al, ni].values
    vmax = np.ceil(np.nanmax(R) / 10) * 10
    pc = ax.pcolormesh(ni, al, R, shading='nearest', cmap='Blues', vmin=0, vmax=vmax, edgecolors='white', linewidth=0.6)
    cb = fig.colorbar(pc, ax=ax, pad=0.02, fraction=0.06)
    cb.set_label('Equilibrium freezing range (°C)')
    cb.outline.set_linewidth(0.5)
    levels = [lv for lv in range(1050, 1400, 50) if np.nanmin(L) < lv < np.nanmax(L)]
    cs = ax.contour(ni, al, L, levels=[lv for lv in levels if lv not in (1250, 1300)], colors='0.25', linewidths=0.6)
    ax.clabel(cs, fmt='%d', fontsize=7, inline_spacing=2)
    for lv, ls in ((1250, '--'), (1300, ':')):
        if np.nanmin(L) < lv < np.nanmax(L):
            c2 = ax.contour(ni, al, L, levels=[lv], colors='#D55E00', linewidths=1.3, linestyles=ls)
            ax.clabel(c2, fmt={lv: f'{lv} °C'}, fontsize=7, inline_spacing=2)
    for r in ref:
        ax.plot(r['ni'], r['al'], marker=r['marker'], ms=6, mfc='white', mec='black', mew=0.9, clip_on=False, zorder=5)
        ax.annotate(r['name'], (r['ni'], r['al']), xytext=r['offset'], textcoords='offset points', fontsize=7,
                    ha=r.get('ha', 'left'), va='center', zorder=6)
    ax.set_xlabel('Ni (wt%)'); ax.set_ylabel('Al (wt%)')
    ax.set_xlim(-1.5, 31.5); ax.set_ylim(-0.4, 9.9)


def draw_nab(ax, f):
    ax.axvspan(1043, 1060, color='0.85', lw=0, zorder=0)
    ax.annotate('CDA\nmelting\nrange', xy=(1060, 0.55), xytext=(1072, 0.55), ha='left', va='center',
                fontsize=7, color='0.3', arrowprops=dict(arrowstyle='-', color='0.5', lw=0.6))
    for k in OKABE_ITO:
        if k in f.columns:
            ax.plot(f.T_C, f[k], color=OKABE_ITO[k], ls=STYLE[k], lw=1.4, label=SHORT[k])
    ax.set_xlim(600, 1150); ax.set_ylim(0, 1.0)
    ax.set_xlabel('Temperature (°C)'); ax.set_ylabel('Equilibrium phase fraction (mol)')
    ax.legend(loc='center left', bbox_to_anchor=(0.0, 0.45), frameon=False, handlelength=2.2,
              borderaxespad=0.1, fontsize=7, labelspacing=0.3)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def make_figures():
    plt = _style()
    m = pd.read_csv(os.path.join(HERE, 'composition_map.csv'))
    f = pd.read_csv(os.path.join(HERE, 'nab_phase_fractions.csv'))
    ref = [dict(name='90-10', ni=10, al=0, marker='o', offset=(0, 9), ha='center'),
           dict(name='70-30', ni=30, al=0, marker='s', offset=(-5, 9), ha='right'),
           dict(name='NAB', ni=4.5, al=9.2, marker='D', offset=(6, -5))]
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.6), gridspec_kw=dict(width_ratios=[1.08, 1]))
    draw_map(axs[0], fig, m, ref)
    draw_nab(axs[1], f)
    for ax, letter in zip(axs, 'ab'):
        ax.text(-0.2, 1.0, f'({letter})', transform=ax.transAxes, fontsize=9, fontweight='bold', va='top')
    fig.tight_layout(pad=0.3, w_pad=1.2)
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(HERE, f'cu_calphad_prelim.{ext}'), dpi=300)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(3.1, 2.4))
    draw_map(ax, fig, m, ref)
    fig.tight_layout(pad=0.3)
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(HERE, f'cu_map.{ext}'), dpi=300)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(3.1, 2.4))
    draw_nab(ax, f)
    fig.tight_layout(pad=0.3)
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(HERE, f'cu_panel2.{ext}'), dpi=300)
    plt.close(fig)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--crosscheck', action='store_true')
    ap.add_argument('--crosscheck-only', action='store_true')
    ap.add_argument('--figures-only', action='store_true')
    ap.add_argument('--no-scheil', action='store_true')
    args = ap.parse_args()
    if args.crosscheck_only:
        args.crosscheck = args.figures_only = True
    if not args.figures_only:
        import pycalphad
        import scheil
        print(f'pycalphad {pycalphad.__version__}, scheil {scheil.__version__}, python {sys.version.split()[0]}')
        t0 = time.time()
        db = load_db('mc_ni')
        print(f'mc_ni loaded in {time.time() - t0:.1f} s')
        ref = run_reference_alloys(db, 'mc_ni', do_scheil=not args.no_scheil)
        ref.to_csv(os.path.join(HERE, 'reference_alloys.csv'), index=False)
        frac = run_nab_fractions(db)
        frac.round(5).to_csv(os.path.join(HERE, 'nab_phase_fractions.csv'), index=False)
        beta = frac[frac['beta (Cu-rich bcc)'] > 1e-3].T_C
        print(f'  NAB beta (Cu-rich bcc) present from {beta.max():.0f} down to {beta.min():.0f} C (2 C grid)')
        run_map(db).to_csv(os.path.join(HERE, 'composition_map.csv'), index=False)
    if args.crosscheck:
        rows = [run_reference_alloys(load_db(key), key, do_scheil=False) for key in ('mc_ni', 'mc_fe', 'cost507')]
        pd.concat(rows).to_csv(os.path.join(HERE, 'crosscheck.csv'), index=False)
    make_figures()


if __name__ == '__main__':
    main()
