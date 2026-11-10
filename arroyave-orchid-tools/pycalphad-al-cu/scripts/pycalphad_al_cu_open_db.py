#!/usr/bin/env python
"""pycalphad + open CALPHAD databases for the Al and Cu alloys of issue #235.

Compares pycalphad results from openly licensed databases with published Thermo-Calc
results and with experiments (ORCHID literature data, papers).

Databases (read in place, never copied; SHA-256 recorded in data/databases_used.csv):
  * MatCalc mc_al v2.032 (ODbL 1.0 / DbCL 1.0), pycalphad re-encoding from pycalphad/binder
  * MatCalc mc_ni v2.036 (ODbL 1.0 / DbCL 1.0), as in the ONR YIP pycalphad-cu work
  * SGTE binary collection, Hallstedt, Calphad 89 (2025) 102833 (CC BY 4.0)

Subcommands (`all` runs them in this order):
  orchid     ORCHID experimental invariants for the binaries used here -> data/orchid_*.csv
  al-alloys  AlSi10Mg and Si-enriched variants: equilibrium + Scheil (mc_al)
  alzr       Al-Zr, Al-rich side: SGTE Al-Zr datasets + mc_al
  almncrzr   Al-Mn-Cr-Zr printable alloys (Mehta et al. 2022 compositions), mc_al
  binaries   SGTE binary phase diagrams and invariants (Al-Si, Al-Cu, Cu-Ni, Cu-Zr, Cr-Cu, Cu-Sn)
  cu-alloys  C63000/C95800 NAB and Cu-Ni alloys, mc_ni v2.036 (reuses the ONR YIP helpers)
  figures    figures drawn from the CSVs (Scheil vs equilibrium, NAB fractions, Al-Zr)
  literature data/literature_values.csv (curated Thermo-Calc and experimental numbers, with sources)
  table      data/comparison.csv from the CSVs and data/literature_values.csv

Usage:  python pycalphad_al_cu_open_db.py <subcommand> [<subcommand> ...]
"""
import glob
import hashlib
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
DATA, FIG, LOGS = (os.path.join(OUT, d) for d in ('data', 'figures', 'logs'))
for _d in (DATA, FIG, LOGS):
    os.makedirs(_d, exist_ok=True)

DBROOT = os.environ.get('OPEN_TDB_ROOT', '/tmp/arroyave/src/orchid-calphad__orchid-project.org/data/databases')
ORCHID_LIT = os.environ.get('ORCHID_LIT', '/tmp/arroyave/src/orchid-calphad__orchid-data/literature')
os.environ.setdefault('CU_CALPHAD_CACHE', '/tmp/arroyave/work/pycalphad-al-cu/tdb_cache')
MC_AL = os.path.join(DBROOT, 'binder', 'mc_al_v2.032.pycalphad.tdb')
SGTE = os.path.join(DBROOT, 'sgte-binary')
P0 = 101325.0
MW = {'AL': 26.9815385, 'SI': 28.0855, 'MG': 24.305, 'FE': 55.845, 'MN': 54.938044, 'CR': 51.9961,
      'ZR': 91.224, 'CU': 63.546, 'NI': 58.6934, 'SN': 118.71, 'SC': 44.955908}

# MatCalc mc_al phases that are metastable precipitates, clusters or pure-element helper phases
# (header: "high priority metastable precipitates"). Excluded from equilibrium and Scheil.
METASTABLE_MC_AL = {
    'GP_MAT', 'GP_MGSI', 'MGSI_B_P', 'MG5SI6_B_DP', 'PRE_B_DP', 'B_PRIME_L', 'B_PRIME_H', 'BETA_DP',
    'AL_B_DP', 'TH_DP_GPB', 'THETA_PRIME', 'U1_PHASE', 'U2_PHASE', 'CL_CUMG0', 'CL_CUMG1', 'CL_MGSI',
    'CL_ALMGSI', 'L12AL3ZR', 'ALMGZN_GP', 'ETA_P_ALMGZN', 'ALCRSI', 'FCCAL', 'FCCMG', 'FCCSI'}


def T_C(TK):
    return float(TK) - 273.15


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def record_db(name, path, note=''):
    """Append one database to data/databases_used.csv (name, file, sha256, note)."""
    f = os.path.join(DATA, 'databases_used.csv')
    df = pd.read_csv(f) if os.path.exists(f) else pd.DataFrame(columns=['database', 'file', 'sha256', 'note'])
    if not ((df.database == name) & (df.file == os.path.basename(path))).any():
        df.loc[len(df)] = [name, os.path.basename(path), sha256(path), note]
        df.to_csv(f, index=False)


def wt_to_x(wt):
    n = {k: w / MW[k] for k, w in wt.items() if w > 0}
    s = sum(n.values())
    return {k: n[k] / s for k in n}


def with_balance(wt, bal):
    wt = dict(wt)
    wt[bal] = 100.0 - sum(wt.values())
    return wt


def x_to_wt(x):
    m = {k: xv * MW[k] for k, xv in x.items()}
    s = sum(m.values())
    return {k: 100 * m[k] / s for k in m}


# ----------------------------------------------------------------------------- pycalphad helpers
def load_mc_al():
    """mc_al v2.032 (binder re-encoding). One syntax patch, no number changed: the metastable
    GP-zone phase GP_MAT is declared in the file as the ordered partner of FCC_A1
    (TYPE_DEFINITION ^ GES A_P_D GP_MAT DIS_PART FCC_A1). pycalphad then hides FCC_A1 (the Al
    matrix!) as a disordered part, so the link is removed and GP_MAT is excluded."""
    from pycalphad import Database
    txt = open(MC_AL, encoding='utf-8', errors='ignore').read()
    a = 'TYPE_DEFINITION ^ GES A_P_D GP_MAT DIS_PART FCC_A1 !'
    assert a in txt
    txt = txt.replace(a, '$ GP_MAT order-disorder link removed (pycalphad_al_cu_open_db.py)')
    txt = txt.replace('PHASE GP_MAT %^', 'PHASE GP_MAT %')
    record_db('MatCalc mc_al v2.032 (pycalphad/binder re-encoding)', MC_AL,
              'ODbL 1.0/DbCL 1.0; GP_MAT order-disorder link removed at load time')
    return Database.from_string(txt, fmt='tdb')


def load_sgte(fname):
    from pycalphad import Database
    path = os.path.join(SGTE, fname)
    db = Database(path)
    record_db('SGTE binary collection (Hallstedt 2025)', path, 'CC BY 4.0; doi:10.1016/j.calphad.2025.102833')
    return db


def phases_for(db, comps, exclude=()):
    from pycalphad.core.utils import filter_phases, unpack_species
    return [p for p in filter_phases(db, unpack_species(db, comps)) if p not in set(exclude)]


class EqCalc:
    """Equilibrium calculator that builds models and phase records once."""

    def __init__(self, db, comps, phases, dep):
        from pycalphad import variables as v
        from pycalphad.core.utils import instantiate_models
        from pycalphad.codegen.phase_record_factory import PhaseRecordFactory
        self.db, self.comps, self.phases, self.dep = db, comps, phases, dep
        self.models = instantiate_models(db, comps, phases)
        self.prf = PhaseRecordFactory(db, comps, [v.N, v.P, v.T], self.models)

    def eq(self, x, T):
        from pycalphad import equilibrium, variables as v
        conds = {v.T: [float(t) for t in np.atleast_1d(T)], v.P: P0, v.N: 1.0}
        conds.update({v.X(e): x[e] for e in sorted(x) if e != self.dep})
        return equilibrium(self.db, self.comps, self.phases, conds, model=self.models, phase_records=self.prf)

    def pts(self, x, T):
        return points(self.eq(x, T))


def points(eq):
    """Per condition point: list of (phase, amount, {element: mole fraction})."""
    ph = eq.Phase.values.reshape(-1, eq.Phase.shape[-1])
    npv = eq.NP.values.reshape(-1, eq.NP.shape[-1])
    X = eq.X.values.reshape(-1, eq.X.shape[-2], eq.X.shape[-1])
    els = [str(c) for c in eq.component.values]
    res = []
    for i in range(ph.shape[0]):
        res.append([(str(p), float(npv[i][j]), {e: float(X[i][j][k]) for k, e in enumerate(els)})
                    for j, p in enumerate(ph[i]) if p != '' and np.isfinite(npv[i][j])])
    return res


def amounts(pt, labeler=None, mass=False):
    d = {}
    for p, a, xx in pt:
        k = labeler(p, xx) if labeler else p
        w = a * sum(xx[e] * MW[e] for e in xx if e in MW) if mass else a
        d[k] = d.get(k, 0.0) + w
    if mass and d:
        s = sum(d.values())
        d = {k: val / s for k, val in d.items()}
    return d


def find_events(calc, x, T_hi, T_lo, step, track=(), tol=0.1, eps=1e-5):
    """Liquidus (first solid), solidus (liquid gone) and first appearance of tracked phases
    on cooling: coarse scan, then bisection to `tol` K. Returns temperatures in K."""
    T = np.arange(T_hi, T_lo - 1e-9, -step)
    am = [amounts(p) for p in calc.pts(x, T)]
    for i in range(1, len(am)):          # failed points: carry the previous state
        if not am[i]:
            am[i] = am[i - 1]
    preds = {'liquidus': lambda a: a.get('LIQUID', 0.0) < 1 - eps,
             'solidus': lambda a: a.get('LIQUID', 0.0) < eps}
    for ph in track:
        preds[ph] = (lambda q: lambda a: a.get(q, 0.0) > eps)(ph)
    res = {}
    for name, pred in preds.items():
        idx = next((i for i, a in enumerate(am) if a and pred(a)), None)
        if idx is None or idx == 0:
            res[name] = np.nan
            continue
        lo, hi = T[idx], T[idx - 1]
        while hi - lo > tol:
            mid = 0.5 * (lo + hi)
            a = amounts(calc.pts(x, [mid])[0])
            if a and pred(a):
                lo = mid
            else:
                hi = mid
        res[name] = 0.5 * (lo + hi)
    return res


def run_scheil(calc, x, start_K, step=1.0):
    from pycalphad import variables as v
    from scheil import simulate_scheil_solidification
    comp = {v.X(e): x[e] for e in sorted(x) if e != calc.dep}
    return simulate_scheil_solidification(calc.db, calc.comps, calc.phases, comp, start_K,
                                          step_temperature=step,
                                          eq_kwargs={'models': calc.models, 'phase_record_factory': calc.prf})


def scheil_summary(res, eutectic_phase=None):
    T = np.array(res.temperatures) - 273.15
    fs = np.array(res.fraction_solid)
    out = dict(scheil_first_solid_C=float(T[np.argmax(fs > 1e-4)]) if (fs > 1e-4).any() else np.nan,
               scheil_terminal_C=float(T[-1]), scheil_final_fs=float(fs[-1]), scheil_converged=bool(res.converged))
    for f in (0.5, 0.9, 0.95, 0.99):
        out[f'scheil_T_fs{int(round(f * 100)):02d}_C'] = float(np.interp(f, fs, T)) if fs[-1] >= f else np.nan
    if eutectic_phase and eutectic_phase in res.cum_phase_amounts:
        cum = np.array(res.cum_phase_amounts[eutectic_phase])
        if (cum > 1e-6).any():
            i = int(np.argmax(cum > 1e-6))
            out['scheil_eutectic_start_C'] = float(T[i])
            out['scheil_fs_at_eutectic_start'] = float(fs[i - 1]) if i > 0 else 0.0
            out['scheil_fraction_eutectic'] = 1.0 - out['scheil_fs_at_eutectic_start']
    return out


def scheil_frame(res):
    T = np.array(res.temperatures) - 273.15
    df = pd.DataFrame({'T_C': T, 'fraction_solid': res.fraction_solid})
    for ph, cum in res.cum_phase_amounts.items():
        if np.max(cum) > 1e-6:
            df['cum_' + ph] = cum
    return df


# ----------------------------------------------------------------------------- ORCHID literature
ORCHID_SYSTEMS = ['AL-SI', 'AL-ZR', 'AL-CU', 'CU-NI', 'CU-ZR', 'CR-CU', 'CU-SN', 'AL-MN', 'AL-CR', 'AL-MG']


def run_orchid():
    rows = []
    for sysn in ORCHID_SYSTEMS:
        files = sorted(glob.glob(os.path.join(ORCHID_LIT, 'systems', f'{sysn}.json')) +
                       glob.glob(os.path.join(ORCHID_LIT, 'systems', f'{sysn}.part*.json')))
        for fn in files:
            d = json.load(open(fn))
            papers = d.get('papers', {})
            for r in d['records']:
                if r.get('property') not in ('INVARIANT_TEMPERATURE', 'TRANSITION_TEMPERATURE'):
                    continue
                fl = r.get('flags', {})
                comps = []
                for pc in r.get('phase_compositions') or []:
                    if pc.get('basis') == 'mole_fraction' and pc.get('composition'):
                        comps.append({'phase': pc['phase'], 'x': pc['composition']})
                phases = [(p.get('label'), p.get('model_phase')) for p in r.get('phases') or []]
                pap = r.get('paper', '')
                cs = r.get('cited_sources') or []
                rows.append(dict(
                    system=sysn, orchid_id=r.get('id'), evidence_class=r.get('evidence_class'),
                    accepted=bool(fl.get('extraction_accepted')), espei_ready=bool(fl.get('espei_ready')),
                    calphad_check=fl.get('calphad_check'), T_K=r.get('value'),
                    T_C=(r.get('value') - 273.15) if r.get('value') is not None else None,
                    transition_kind=r.get('transition_kind'),
                    reaction=(r.get('reaction') or {}).get('printed', ''),
                    phases=json.dumps(phases), phase_compositions=json.dumps(comps),
                    paper=pap, paper_doi=pap[4:] if pap.startswith('doi:') else '',
                    cited_source_doi=';'.join(c.get('doi') or '' for c in cs if c.get('doi')),
                    origin_measured_in=(r.get('origin') or {}).get('measured_in', '')))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA, 'orchid_invariants_all.csv'), index=False)
    exp = df[(df.evidence_class == 'experimental') & df.accepted]
    exp.to_csv(os.path.join(DATA, 'orchid_invariants_experimental_accepted.csv'), index=False)
    print(f'ORCHID: {len(df)} invariant/transition records, {len(exp)} accepted experimental', flush=True)
    for s, g in exp.groupby('system'):
        print(f'  {s}: {len(g)} accepted experimental', flush=True)


def orchid_points(system, A, B):
    """(x_B, T_K, label) points of accepted experimental invariants with printed compositions."""
    f = os.path.join(DATA, 'orchid_invariants_experimental_accepted.csv')
    if not os.path.exists(f):
        return []
    df = pd.read_csv(f)
    out = []
    for _, r in df[df.system == system].iterrows():
        for pc in json.loads(r.phase_compositions):
            x = pc['x']
            xb = x.get(B, (1 - x[A]) if A in x else None)
            if xb is not None and np.isfinite(r.T_K):
                out.append((float(xb), float(r.T_K), r.reaction, r.paper_doi))
    return out


# ----------------------------------------------------------------------------- Al: AlSi10Mg family
AL_ALLOYS = [
    dict(alloy='AlSi10Mg', wt={'SI': 10.0, 'MG': 0.35}),
    dict(alloy='AlSi10Mg+0.3Fe', wt={'SI': 10.0, 'MG': 0.35, 'FE': 0.3}),
    dict(alloy='AlSi12Mg (Si-enriched)', wt={'SI': 12.0, 'MG': 0.35}),
    dict(alloy='AlSi12Mg+0.3Fe (Si-enriched)', wt={'SI': 12.0, 'MG': 0.35, 'FE': 0.3}),
    # binary Al-12Si, to match the Thermo-Calc TCAL7 Scheil numbers of doi:10.1007/s11665-023-08502-3
    dict(alloy='AlSi12 (binary Al-12Si)', wt={'SI': 12.0}),
    # powder composition of doi:10.3390/ma16144920 (Thermo-Calc TCAL6 room-temperature phase fractions)
    dict(alloy='AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)', wt={'SI': 9.92, 'MG': 0.291, 'FE': 0.137}),
]
AL_TRACK = ['FCC_A1', 'SI_DIAMOND_A4', 'MG2SI_B', 'PI_ALFEMGSI', 'ALFESI_T6', 'ALFESI_T5', 'AL13FE4']


def slug(s):
    return ''.join(c if c.isalnum() else '_' for c in s).strip('_')


def run_al_alloys(which=None):
    db = load_mc_al()
    summ_f = os.path.join(DATA, 'al_alloys_summary.csv')
    rows = pd.read_csv(summ_f).to_dict('records') if os.path.exists(summ_f) else []
    for a in AL_ALLOYS:
        if which and a['alloy'] not in which:
            continue
        t0 = time.time()
        wt = with_balance(a['wt'], 'AL')
        x = wt_to_x(wt)
        comps = sorted(wt) + ['VA']
        phases = phases_for(db, comps, METASTABLE_MC_AL)
        calc = EqCalc(db, comps, phases, 'AL')
        print(f"[{a['alloy']}] {len(phases)} phases; models built {time.time() - t0:.0f} s", flush=True)
        ev = find_events(calc, x, 900.0, 760.0, 4.0, track=AL_TRACK)
        print(f"[{a['alloy']}] events " + ', '.join(f'{k}={T_C(t):.1f}C' for k, t in ev.items() if np.isfinite(t)) +
              f' ({time.time() - t0:.0f} s)', flush=True)
        # equilibrium phase fractions vs T (mole and mass fractions)
        Tgrid = sorted(set(np.round(np.arange(950.0, 449.0, -10.0), 3).tolist() +
                           [round(t + d, 3) for t in ev.values() if np.isfinite(t) for d in (0.3, -0.3)]),
                       reverse=True)
        P = calc.pts(x, Tgrid)
        fr = []
        for t, pt in zip(Tgrid, P):
            r = {'T_C': round(T_C(t), 2)}
            r.update({'mol_' + k: v_ for k, v_ in amounts(pt).items()})
            r.update({'mass_' + k: v_ for k, v_ in amounts(pt, mass=True).items()})
            fr.append(r)
        fdf = pd.DataFrame(fr).fillna(0.0)
        fdf.to_csv(os.path.join(DATA, f"al_eq_fractions_{slug(a['alloy'])}.csv"), index=False)
        liq, sol, tsi = ev['liquidus'], ev['solidus'], ev.get('SI_DIAMOND_A4', np.nan)
        prim = [p for p in AL_TRACK if np.isfinite(ev.get(p, np.nan)) and abs(ev[p] - liq) < 0.3]
        row = dict(alloy=a['alloy'], composition_wt=' '.join(f'{k}{wt[k]:.2f}' for k in sorted(wt)),
                   database='mc_al v2.032', eq_liquidus_C=T_C(liq), eq_solidus_C=T_C(sol),
                   eq_freezing_range_C=liq - sol, eq_primary_phase='+'.join(prim))
        for p in AL_TRACK:
            row[f'eq_{p}_start_C'] = T_C(ev[p]) if np.isfinite(ev.get(p, np.nan)) else np.nan
        if np.isfinite(tsi) and tsi < liq - 0.5:
            pa = amounts(calc.pts(x, [tsi + 0.05])[0])
            row['eq_fraction_liquid_at_Si_start'] = pa.get('LIQUID', np.nan)
        for tc in (500.0, 300.0, 25.0):
            pa = amounts(calc.pts(x, [tc + 273.15])[0])
            pm = amounts(calc.pts(x, [tc + 273.15])[0], mass=True)
            row[f'eq_all_phases_mass_{int(tc)}C'] = '; '.join(f'{k} {val:.4f}' for k, val in sorted(pm.items(), key=lambda kv: -kv[1]))
            for p in ('FCC_A1', 'SI_DIAMOND_A4', 'MG2SI_B', 'PI_ALFEMGSI', 'ALFESI_T6', 'ALFESI_T5', 'AL13FE4', 'ALCRFEMNSI_A'):
                row[f'eq_mol_{p}_{int(tc)}C'] = pa.get(p, 0.0)
                row[f'eq_mass_{p}_{int(tc)}C'] = pm.get(p, 0.0)
        print(f"[{a['alloy']}] equilibrium done ({time.time() - t0:.0f} s); Scheil...", flush=True)
        t1 = time.time()
        res = run_scheil(calc, x, liq + 2.0)
        row.update(scheil_summary(res, 'SI_DIAMOND_A4'))
        row['scheil_freezing_range_to_fs99_C'] = row['eq_liquidus_C'] - row['scheil_T_fs99_C']   # from the bisected liquidus
        row['scheil_freezing_range_to_terminal_C'] = row['eq_liquidus_C'] - row['scheil_terminal_C']
        row['scheil_phases'] = '+'.join(p for p, c in res.cum_phase_amounts.items() if np.max(c) > 1e-5)
        row['scheil_wall_s'] = round(time.time() - t1, 1)
        row['total_wall_s'] = round(time.time() - t0, 1)
        scheil_frame(res).to_csv(os.path.join(DATA, f"al_scheil_{slug(a['alloy'])}.csv"), index=False)
        rows = [r for r in rows if r['alloy'] != a['alloy']] + [row]
        pd.DataFrame(rows).to_csv(summ_f, index=False)
        print(f"[{a['alloy']}] liq {row['eq_liquidus_C']:.1f} sol {row['eq_solidus_C']:.1f} "
              f"Si-start {row['eq_SI_DIAMOND_A4_start_C']:.1f}; Scheil fs0.9 {row['scheil_T_fs90_C']:.1f} "
              f"fs0.99 {row['scheil_T_fs99_C']:.1f} end {row['scheil_terminal_C']:.1f} "
              f"f_eut {row.get('scheil_fraction_eutectic', np.nan):.3f} ({row['total_wall_s']} s)", flush=True)


# ----------------------------------------------------------------------------- Al-Zr
ALZR_SGTE = ['AlZr-98Sau-LB.tdb', 'AlZr-86Sau.tdb', 'AlZr-01Wan.tdb', 'AlZr-10Hir.tdb', 'AlZr-15Fis.tdb',
             'AlZr-18Khv.tdb', 'AlZr-18Tam.tdb', 'AlZr-20Lon.tdb']
ALZR_WT = [0.05, 0.1, 0.15, 0.2, 0.217, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2]


def alzr_one(db, phases, label):
    calc = EqCalc(db, ['AL', 'ZR', 'VA'], phases, 'AL')
    out = dict(database=label)
    x1 = wt_to_x({'AL': 99.0, 'ZR': 1.0})
    ev = find_events(calc, x1, 980.0, 900.0, 1.0, track=('FCC_A1',), tol=0.02)
    tp = ev['solidus']
    out['invariant_T_C'] = T_C(tp)
    xl, xf, below = [], [], []
    for dT in (0.05, 0.2, 0.5, 1.0):     # first offset at which the phase is found (failed points are empty)
        if not xl:
            xl = [xx['ZR'] for p, a, xx in calc.pts(x1, [tp + dT])[0] if p == 'LIQUID']
        if not xf:
            below = calc.pts(x1, [tp - dT])[0]
            xf = [xx['ZR'] for p, a, xx in below if p == 'FCC_A1' and xx['AL'] > 0.9]
    out['x_liq_at_invariant'] = xl[0] if xl else np.nan
    out['x_fcc_at_invariant'] = xf[0] if xf else np.nan
    out['wt_liq_at_invariant'] = x_to_wt({'AL': 1 - out['x_liq_at_invariant'], 'ZR': out['x_liq_at_invariant']})['ZR'] if xl else np.nan
    out['wt_fcc_at_invariant'] = x_to_wt({'AL': 1 - out['x_fcc_at_invariant'], 'ZR': out['x_fcc_at_invariant']})['ZR'] if xf else np.nan
    out['reaction'] = ('peritectic L + Al3Zr -> (Al)' if xl and xf and xf[0] > xl[0] else
                       'eutectic L -> (Al) + Al3Zr' if xl and xf else 'unclear')
    out['solid_with_fcc'] = '+'.join(sorted({p for p, a, xx in below if p not in ('FCC_A1',)}))
    liq_rows = []
    for w in ALZR_WT:
        x = wt_to_x({'AL': 100 - w, 'ZR': w})
        e = find_events(calc, x, 1400.0, 920.0, 4.0, track=('FCC_A1',), tol=0.1)
        prim = [p for p, a, xx in calc.pts(x, [e['liquidus'] - 0.3])[0] if p != 'LIQUID' and a > 1e-7]
        liq_rows.append(dict(database=label, wt_Zr=w, x_Zr=x['ZR'], liquidus_C=T_C(e['liquidus']),
                             solidus_C=T_C(e['solidus']), primary_phase='+'.join(prim)))
        out[f'liquidus_{w:g}wtZr_C'] = T_C(e['liquidus'])
    print(f"  Al-Zr {label}: invariant {out['invariant_T_C']:.2f} C ({out['reaction']}), x_liq {out['x_liq_at_invariant']:.5f}, "
          f"x_fcc {out['x_fcc_at_invariant']:.5f} (wt {out['wt_fcc_at_invariant']:.3f}); liquidus 0.5wt "
          f"{out['liquidus_0.5wtZr_C']:.1f}, 1.0wt {out['liquidus_1wtZr_C']:.1f}", flush=True)
    return out, liq_rows


def run_alzr():
    summ, liq = [], []
    for f in ALZR_SGTE:
        t0 = time.time()
        try:
            db = load_sgte(f)
            ph = phases_for(db, ['AL', 'ZR', 'VA'])
            o, l = alzr_one(db, ph, 'SGTE ' + f)
            o['wall_s'] = round(time.time() - t0, 1)
            summ.append(o)
            liq += l
        except Exception as e:  # keep going; record the failure
            print(f'  Al-Zr {f}: FAILED {type(e).__name__}: {str(e)[:200]}', flush=True)
            summ.append(dict(database='SGTE ' + f, reaction=f'failed: {type(e).__name__}'))
        pd.DataFrame(summ).to_csv(os.path.join(DATA, 'alzr_summary.csv'), index=False)
        pd.DataFrame(liq).to_csv(os.path.join(DATA, 'alzr_liquidus.csv'), index=False)
    t0 = time.time()
    db = load_mc_al()
    ph = phases_for(db, ['AL', 'ZR', 'VA'], METASTABLE_MC_AL)
    o, l = alzr_one(db, ph, 'mc_al v2.032')
    o['wall_s'] = round(time.time() - t0, 1)
    summ.append(o)
    liq += l
    pd.DataFrame(summ).to_csv(os.path.join(DATA, 'alzr_summary.csv'), index=False)
    pd.DataFrame(liq).to_csv(os.path.join(DATA, 'alzr_liquidus.csv'), index=False)


# ----------------------------------------------------------------------------- Al-Mn-Cr-Zr
# Mehta et al., J. Mater. Res. 37 (2022) 1256, doi:10.1557/s43578-022-00533-1, Table 1 (ICP-AES,
# as-printed, wt%). Fe and Si impurities are dropped in the quaternary calculation.
ALMN_ALLOYS = [
    dict(alloy='Mehta A Al-4.8Mn-0.47Zr', wt={'MN': 4.8, 'ZR': 0.47}),
    dict(alloy='Mehta B Al-4.9Mn-0.8Cr', wt={'MN': 4.9, 'CR': 0.8}),
    dict(alloy='Mehta C Al-5.0Mn-0.8Cr-0.6Zr', wt={'MN': 5.0, 'CR': 0.8, 'ZR': 0.60}),
]


def run_almncrzr():
    db = load_mc_al()
    rows = []
    for a in ALMN_ALLOYS:
        t0 = time.time()
        wt = with_balance(a['wt'], 'AL')
        x = wt_to_x(wt)
        comps = sorted(wt) + ['VA']
        phases = phases_for(db, comps, METASTABLE_MC_AL)
        calc = EqCalc(db, comps, phases, 'AL')
        track = [p for p in ('FCC_A1', 'AL3ZR', 'AL6MN', 'AL4MN', 'AL12MN', 'AL11MN4', 'AL13CR2', 'AL11CR2', 'AL4CR')
                 if p in phases]
        ev = find_events(calc, x, 1350.0, 860.0, 5.0, track=track)
        row = dict(alloy=a['alloy'], composition_wt=' '.join(f'{k}{wt[k]:.2f}' for k in sorted(wt)),
                   database='mc_al v2.032', eq_liquidus_C=T_C(ev['liquidus']), eq_solidus_C=T_C(ev['solidus']),
                   eq_freezing_range_C=ev['liquidus'] - ev['solidus'])
        row['eq_primary_phase'] = '+'.join(p for p in track if np.isfinite(ev.get(p, np.nan)) and abs(ev[p] - ev['liquidus']) < 0.3)
        for p in track:
            row[f'eq_{p}_start_C'] = T_C(ev[p]) if np.isfinite(ev.get(p, np.nan)) else np.nan
        row['eq_fcc_start_C'] = row.get('eq_FCC_A1_start_C', np.nan)
        for tc in (ev['solidus'] - 273.15 - 1.0, 400.0):
            pa = amounts(calc.pts(x, [tc + 273.15])[0])
            key = 'solidus-1C' if tc != 400.0 else '400C'
            row[f'eq_phases_mol_{key}'] = '; '.join(f'{p} {val:.4f}' for p, val in sorted(pa.items(), key=lambda kv: -kv[1]))
        t1 = time.time()
        try:
            res = run_scheil(calc, x, ev['liquidus'] + 2.0, step=2.0)
            row.update(scheil_summary(res))
            row['scheil_phases'] = '+'.join(p for p, c in res.cum_phase_amounts.items() if np.max(c) > 1e-5)
            scheil_frame(res).to_csv(os.path.join(DATA, f"almncrzr_scheil_{slug(a['alloy'])}.csv"), index=False)
        except Exception as e:
            row['scheil_phases'] = f'failed: {type(e).__name__}'
        row['scheil_wall_s'] = round(time.time() - t1, 1)
        row['total_wall_s'] = round(time.time() - t0, 1)
        rows.append(row)
        pd.DataFrame(rows).to_csv(os.path.join(DATA, 'almncrzr_summary.csv'), index=False)
        print(f"[{a['alloy']}] liq {row['eq_liquidus_C']:.1f} ({row['eq_primary_phase']}) fcc-start {row['eq_fcc_start_C']:.1f} "
              f"sol {row['eq_solidus_C']:.1f}; Scheil fs0.99 {row.get('scheil_T_fs99_C', np.nan):.1f} "
              f"({row['total_wall_s']} s)", flush=True)


# ----------------------------------------------------------------------------- SGTE binaries
BINARIES = [
    # system (ORCHID key), A, B (x axis = X(B)), files, T range (K), x range
    dict(system='AL-SI', A='AL', B='SI', files=['AlSi-97Feu-LB.tdb', 'AlSi-14Lia.tdb'], T=(500, 1800), x=(0, 1)),
    dict(system='AL-CU', A='AL', B='CU', files=['AlCu-21Kro.tdb', 'AlCu-98Sau-LB.tdb'], T=(500, 1500), x=(0, 1)),
    dict(system='CU-NI', A='CU', B='NI', files=['CuNi-92Mey-LB.tdb', 'CuNi-07Tur.tdb'], T=(300, 1800), x=(0, 1)),
    dict(system='CR-CU', A='CU', B='CR', files=['CrCu-17Liu.tdb', 'CrCu-95Zen-LB.tdb'], T=(800, 2300), x=(0, 1)),
    dict(system='CU-ZR', A='CU', B='ZR', files=['CuZr-22Zho.tdb', 'CuZr-94Zen-LB.tdb'], T=(700, 1500), x=(0, 0.5)),
    dict(system='CU-SN', A='CU', B='SN', files=['CuSn-24Oik.tdb', 'CuSn-96Shi-LB.tdb'], T=(500, 1400), x=(0, 0.35)),
]


def map_binary(db, A, B, Trange, xr, dx=0.02):
    from pycalphad import variables as v
    from pycalphad.mapping import BinaryStrategy
    comps = sorted([A, B]) + ['VA']
    ph = phases_for(db, comps)
    strat = BinaryStrategy(db, comps, ph, {v.X(B): (xr[0], xr[1], dx), v.T: (Trange[0], Trange[1], 10),
                                           v.P: P0, v.N: 1})
    strat.do_map()
    return strat


def strategy_invariants(strat, B):
    from pycalphad import variables as v
    seen, out = set(), []
    for inv in strat.get_invariant_data(v.X(B), v.T):
        d = sorted([(sd.phase, float(sd.x)) for sd in inv.data])
        T = float(inv.data[0].y)
        key = (tuple(p for p, _ in d), round(T, 1))
        if key in seen:
            continue
        seen.add(key)
        out.append(dict(T_K=T, T_C=T - 273.15, phases='+'.join(p for p, _ in d),
                        compositions=json.dumps({p: round(xx, 5) for p, xx in d})))
    return sorted(out, key=lambda r: -r['T_K'])


def run_binaries(which=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from pycalphad import variables as v
    from pycalphad.mapping import plot_binary
    f_inv = os.path.join(DATA, 'binary_invariants_pycalphad.csv')
    allrows = pd.read_csv(f_inv).to_dict('records') if os.path.exists(f_inv) else []
    for spec in BINARIES:
        if which and spec['system'] not in which:
            continue
        for i, fname in enumerate(spec['files']):
            t0 = time.time()
            try:
                db = load_sgte(fname)
                strat = map_binary(db, spec['A'], spec['B'], spec['T'], spec['x'])
            except Exception as e:
                print(f"  {spec['system']} {fname}: FAILED {type(e).__name__}: {str(e)[:200]}", flush=True)
                continue
            inv = strategy_invariants(strat, spec['B'])
            allrows = [r for r in allrows if r['tdb'] != fname]
            for r in inv:
                r.update(system=spec['system'], tdb=fname, x_axis=f"X({spec['B']})")
                allrows.append(r)
            pd.DataFrame(allrows).to_csv(f_inv, index=False)
            print(f"  {spec['system']} {fname}: {len(inv)} invariants, {time.time() - t0:.0f} s", flush=True)
            if i == 0:   # figure from the first (preferred) dataset
                draw_binary_figure(strat, spec, fname, plt, plot_binary, v)


def draw_binary_figure(strat, spec, fname, plt, plot_binary, v):
    A, B = spec['A'], spec['B']
    pts = orchid_points(spec['system'], A, B)
    views = [('full', None, None)]
    if spec['system'] == 'AL-CU':
        views = [('Al-rich', (0, 0.35), (700, 950)), ('Cu-rich', (0.65, 1.0), (750, 1400)), ('full', None, None)]
    if spec['system'] == 'AL-SI':
        views = [('full', None, None), ('Al-rich', (0, 0.3), (750, 1000))]
    for name, xl, yl in views:
        fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=110)
        plot_binary(strat, x=v.X(B), y=v.T, ax=ax, tielines=0)
        if pts:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.scatter(xs, ys, s=22, marker='D', facecolor='none', edgecolor='k', lw=0.9, zorder=10,
                       label='ORCHID experimental invariants')
        # systems whose ORCHID experimental records carry no compositions / no accepted invariant
        if spec['system'] == 'AL-SI':
            ax.axhline(850.15, color='k', lw=0.8, ls='--')
            ax.text(0.02 if not xl else xl[0] + 0.01, 853, 'experimental eutectic 850.15 K = 577 °C (ORCHID record, '
                    'doi:10.1007/s11669-024-01160-5; not accepted by ORCHID)', fontsize=6)
        if spec['system'] == 'CU-NI':
            hb = [(wt_to_x({'CU': 90, 'NI': 10})['NI'], 1099, 1149), (wt_to_x({'CU': 70, 'NI': 30})['NI'], 1171, 1238)]
            for xn, ts, tl in hb:
                ax.plot([xn, xn], [ts + 273.15, tl + 273.15], 'k-', lw=1.0, marker='_', ms=10, zorder=11)
            leg0 = ax.get_legend()
            hb_line, = ax.plot([], [], 'k-', marker='_', ms=10)
            ax.legend(handles=[hb_line], labels=['handbook C70600 / C71500 melting ranges (contain Fe, Mn)'],
                      fontsize=6, loc='upper left', framealpha=0.8)
            if leg0 is not None:
                ax.add_artist(leg0)
        if xl:
            ax.set_xlim(*xl)
        if yl:
            ax.set_ylim(*yl)
        ax.set_title(f"{A.title()}-{B.title()} ({name}), pycalphad + SGTE {fname.replace('.tdb', '')}", fontsize=9)
        ax.set_xlabel(f'X({B.title()}) (mole fraction)')
        ax.set_ylabel('T (K)')
        leg = ax.get_legend()          # phase legend made by plot_binary
        if leg is not None:
            for t in leg.get_texts():
                t.set_fontsize(6)
        if pts:
            leg2 = ax.legend(handles=[ax.collections[-1]], labels=['ORCHID experimental invariants'],
                             fontsize=6, loc='lower left', framealpha=0.8)
            if leg is not None:
                ax.add_artist(leg)
        fig.tight_layout()
        out = os.path.join(FIG, f"pd_{spec['system'].lower()}_{name.lower().replace('-', '')}.png")
        fig.savefig(out, dpi=110)
        plt.close(fig)
        print(f'    figure {out}', flush=True)


# ----------------------------------------------------------------------------- Cu alloys (mc_ni)
CU_ALLOYS = [
    dict(alloy='C63000 NAB (Cu-10Al-5Ni-3Fe)', wt={'AL': 10.0, 'NI': 5.0, 'FE': 3.0}, hb=None),
    dict(alloy='C63000 NAB (Cu-10Al-5Ni-3Fe-1Mn)', wt={'AL': 10.0, 'NI': 5.0, 'FE': 3.0, 'MN': 1.0}, hb=None),
    dict(alloy='C95800 NAB (Cu-9.2Al-4.5Ni-4Fe-1.2Mn)', wt={'AL': 9.2, 'NI': 4.5, 'FE': 4.0, 'MN': 1.2}, hb=(1043, 1060)),
    dict(alloy='C70600 (Cu-10Ni-1.4Fe-0.8Mn)', wt={'NI': 10.0, 'FE': 1.4, 'MN': 0.8}, hb=(1099, 1149)),
    dict(alloy='C71500 (Cu-30Ni-0.6Fe-0.6Mn)', wt={'NI': 30.0, 'FE': 0.6, 'MN': 0.6}, hb=(1171, 1238)),
    dict(alloy='Cu-10Ni (binary)', wt={'NI': 10.0}, hb=None),
    dict(alloy='Cu-30Ni (binary)', wt={'NI': 30.0}, hb=None),
]
CUNI_SGTE = ['CuNi-92Mey-LB.tdb', 'CuNi-07Tur.tdb', 'CuNi-87Jan.tdb', 'CuNi-89Sri.tdb']


def run_cu_alloys():
    sys.path.insert(0, HERE)
    import onr_yip_run_calphad_ref as onr   # ONR YIP helpers (copied unchanged from the branch)
    db = onr.load_db('mc_ni')
    record_db('MatCalc mc_ni v2.036', onr.get_tdb('mc_ni'), 'ODbL 1.0/DbCL 1.0; downloaded from matcalc.at; '
              'syntax-converted at load time by the ONR YIP clean_tdb_text (no numbers changed)')
    rows = []
    for a in CU_ALLOYS:
        wt = with_balance(a['wt'], 'CU')
        comps, x, phases = onr.setup(db, 'mc_ni', wt)
        t0 = time.time()
        liq, sol, primary = onr.melting_range(db, comps, phases, x)
        row = dict(alloy=a['alloy'], database='mc_ni v2.036', composition_wt=' '.join(f'{k}{wt[k]:.2f}' for k in sorted(wt)),
                   eq_liquidus_C=liq, eq_solidus_C=sol, eq_range_C=liq - sol, eq_primary_phase=primary,
                   handbook_solidus_C=a['hb'][0] if a['hb'] else np.nan,
                   handbook_liquidus_C=a['hb'][1] if a['hb'] else np.nan)
        try:
            first, t99, tend, conv = onr.scheil_range(db, comps, phases, x, liq + 273.15 + 20)
            row.update(scheil_first_solid_C=first, scheil_T_fs99_C=t99, scheil_terminal_C=tend, scheil_converged=conv)
        except Exception as e:
            row['scheil_converged'] = f'failed {type(e).__name__}'
        row['wall_s'] = round(time.time() - t0, 1)
        rows.append(row)
        pd.DataFrame(rows).to_csv(os.path.join(DATA, 'cu_alloys_summary.csv'), index=False)
        print(f"  mc_ni {a['alloy']}: {sol:.1f}-{liq:.1f} C primary {primary}; Scheil 99% {row.get('scheil_T_fs99_C', np.nan):.1f}", flush=True)
    # NAB C63000 equilibrium phase fractions vs T (mole fractions; ONR labels)
    for a, tag in ((CU_ALLOYS[0], 'C63000'), (CU_ALLOYS[2], 'C95800')):
        comps, x, phases = onr.setup(db, 'mc_ni', with_balance(a['wt'], 'CU'))
        Tc = np.arange(1150.0, 499.0, -5.0)
        pts = onr.points(onr.equilibrium_at(db, comps, phases, x, Tc + 273.15))
        fr = []
        for t, pt in zip(Tc, pts):
            r = {'T_C': t}
            for p, amt, xx in pt:
                k = onr.label(p, xx)
                r[k] = r.get(k, 0.0) + amt
            fr.append(r)
        pd.DataFrame(fr).fillna(0.0).to_csv(os.path.join(DATA, f'nab_{tag}_phase_fractions_mc_ni.csv'), index=False)
    # Cu-Ni binary: SGTE datasets vs mc_ni, liquidus/solidus vs composition
    from pycalphad import Database
    cr = []
    for f in CUNI_SGTE:
        try:
            dbs = load_sgte(f)
        except Exception as e:
            print(f'  {f}: FAILED {e}', flush=True)
            continue
        calc = EqCalc(dbs, ['CU', 'NI', 'VA'], phases_for(dbs, ['CU', 'NI', 'VA'], ('BCC_A2', 'HCP_A3')), 'CU')
        for w in (5, 10, 20, 30, 45, 70):
            x = wt_to_x({'CU': 100 - w, 'NI': w})
            e = find_events(calc, x, 1800.0, 1300.0 if w < 50 else 1500.0, 5.0, tol=0.1)
            if w < 50:
                e2 = find_events(calc, x, 1700.0, 1300.0, 5.0, tol=0.1)
                e = e2
            cr.append(dict(database='SGTE ' + f, wt_Ni=w, liquidus_C=T_C(e['liquidus']), solidus_C=T_C(e['solidus'])))
        pd.DataFrame(cr).to_csv(os.path.join(DATA, 'cuni_binary_liquidus_solidus.csv'), index=False)
    for w in (5, 10, 20, 30, 45, 70):
        comps, x, phases = onr.setup(db, 'mc_ni', {'CU': 100 - w, 'NI': w})
        liq, sol, _ = onr.melting_range(db, comps, phases, x)
        cr.append(dict(database='mc_ni v2.036', wt_Ni=w, liquidus_C=liq, solidus_C=sol))
    pd.DataFrame(cr).to_csv(os.path.join(DATA, 'cuni_binary_liquidus_solidus.csv'), index=False)
    print(pd.DataFrame(cr).to_string(), flush=True)


# ----------------------------------------------------------------------------- figures from CSVs
def run_figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    # 1. AlSi10Mg family: Scheil vs equilibrium solidification
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=110)
    colors = {'AlSi10Mg': '#0072B2', 'AlSi10Mg+0.3Fe': '#56B4E9', 'AlSi12Mg (Si-enriched)': '#D55E00',
              'AlSi12Mg+0.3Fe (Si-enriched)': '#E69F00'}
    for a in AL_ALLOYS:
        s = slug(a['alloy'])
        fe, fs = os.path.join(DATA, f'al_eq_fractions_{s}.csv'), os.path.join(DATA, f'al_scheil_{s}.csv')
        if not (os.path.exists(fe) and os.path.exists(fs)):
            continue
        e = pd.read_csv(fe).sort_values('T_C')
        e = e[(e.T_C > 520) & (e.T_C < 640)]
        e = e[(e['mol_LIQUID'] > 0) | (e.T_C >= e.loc[e['mol_LIQUID'] > 0, 'T_C'].min() - 1.0)]
        sc = pd.read_csv(fs)
        if a['alloy'] not in colors:
            continue
        c = colors[a['alloy']]
        ax.plot(1 - e['mol_LIQUID'], e.T_C, color=c, ls='--', lw=1.3, label=f"{a['alloy']} equilibrium")
        ax.plot(sc.fraction_solid, sc.T_C, color=c, ls='-', lw=1.6, label=f"{a['alloy']} Scheil")
    ax.set_xlabel('Fraction solid (mole basis)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_xlim(0, 1)
    ax.set_ylim(530, 615)
    ax.set_title('AlSi10Mg vs Si-enriched: Scheil vs equilibrium (pycalphad + MatCalc mc_al v2.032)', fontsize=8.5)
    ax.legend(fontsize=6.5, frameon=False, loc='lower left')
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, 'alsi10mg_scheil_vs_equilibrium.png'), dpi=110)
    plt.close(fig)
    # 2. NAB phase fractions vs T
    for tag in ('C63000', 'C95800'):
        f = os.path.join(DATA, f'nab_{tag}_phase_fractions_mc_ni.csv')
        if not os.path.exists(f):
            continue
        d = pd.read_csv(f)
        fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=110)
        sty = {'liquid': ('#000000', '--'), 'alpha (fcc)': ('#0072B2', '-'), 'beta (Cu-rich bcc)': ('#D55E00', '-'),
               'kappa Fe-rich bcc': ('#009E73', '-'), 'kappa NiAl (B2)': ('#CC79A7', '-'),
               'kappa NiAl-type bcc': ('#999999', ':'), "gamma' Ni3Al": ('#E69F00', ':'), 'fcc (Fe/Ni-rich)': ('#56B4E9', ':')}
        for k in d.columns[1:]:
            if d[k].max() < 1e-4:
                continue
            c, ls = sty.get(k, ('#777777', '-.'))
            ax.plot(d.T_C, d[k], color=c, ls=ls, lw=1.5, label=k)
        ax.set_xlabel('Temperature (°C)')
        ax.set_ylabel('Equilibrium phase fraction (mole)')
        ax.set_xlim(500, 1150)
        ax.set_ylim(0, 1.0)
        ax.set_title(f'{tag} nickel-aluminium bronze: equilibrium phases (pycalphad + MatCalc mc_ni v2.036)', fontsize=8.5)
        ax.legend(fontsize=7, frameon=False, loc='center left')
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, f'nab_{tag.lower()}_phase_fractions.png'), dpi=110)
        plt.close(fig)
    # 3. Al-Zr Al-rich liquidus, all databases, with experimental invariant
    f = os.path.join(DATA, 'alzr_liquidus.csv')
    if os.path.exists(f):
        d = pd.read_csv(f)
        s = pd.read_csv(os.path.join(DATA, 'alzr_summary.csv'))
        fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=110)
        cyc = plt.rcParams['axes.prop_cycle'].by_key()['color']
        for i, (name, g) in enumerate(d.groupby('database', sort=False)):
            c = cyc[i % len(cyc)]
            g = g.sort_values('wt_Zr')
            r = s[s.database == name]
            lw = 2.2 if 'mc_al' in name else 1.1
            ax.plot(g.wt_Zr, g.liquidus_C, color=c, lw=lw, marker='.', ms=3, label=name.replace('SGTE ', '').replace('.tdb', ''))
            if len(r) and np.isfinite(r.invariant_T_C.iloc[0]):
                ax.hlines(r.invariant_T_C.iloc[0], r.wt_liq_at_invariant.iloc[0], 1.25, color=c, lw=0.8, ls=':')
                ax.plot(r.wt_fcc_at_invariant.iloc[0], r.invariant_T_C.iloc[0], marker='|', ms=10, color=c)
        ax.axhline(660.85, color='k', lw=0.7, ls='--')
        ax.text(0.30, 663.5, 'experiment: peritectic L + Al3Zr -> (Al), 934 K = 660.85 °C (ORCHID; doi:10.1007/s11669-015-0398-y)', fontsize=6)
        ax.axhline(655.85, color='0.4', lw=0.7, ls=':')
        ax.text(0.30, 645.5, 'alternative reading: eutectic at 929 K = 655.85 °C, liquid 0.72 at% Zr (doi:10.1007/s10973-013-3113-4)', fontsize=6, color='0.3')
        ax.set_xlim(0, 1.25)
        ax.set_ylim(640, 1000)
        ax.set_xlabel('Zr (wt%)')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Al-Zr, Al-rich: Al3Zr liquidus and peritectic, pycalphad with 8 SGTE datasets + mc_al', fontsize=8.5)
        ax.legend(fontsize=6.5, frameon=False, loc='upper left', ncol=2)
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, 'pd_al-zr_alrich_liquidus.png'), dpi=110)
        plt.close(fig)


# ----------------------------------------------------------------------------- main
def main(argv):
    steps = argv or ['all']
    order = ['orchid', 'al-alloys', 'alzr', 'almncrzr', 'binaries', 'cu-alloys', 'figures', 'literature', 'table']
    if 'all' in steps:
        steps = order
    for s in steps:
        t0 = time.time()
        print(f'=== {s} ===', flush=True)
        if s == 'orchid':
            run_orchid()
        elif s == 'al-alloys':
            run_al_alloys()
        elif s.startswith('al-alloys:'):
            run_al_alloys(s.split(':', 1)[1].split('|'))
        elif s == 'alzr':
            run_alzr()
        elif s == 'almncrzr':
            run_almncrzr()
        elif s == 'binaries':
            run_binaries()
        elif s.startswith('binaries:'):
            run_binaries(s.split(':', 1)[1].split('|'))
        elif s == 'cu-alloys':
            run_cu_alloys()
        elif s == 'figures':
            run_figures()
        elif s == 'literature':   # curated Thermo-Calc / experimental values -> data/literature_values.csv
            import runpy
            runpy.run_path(os.path.join(HERE, 'make_literature_values.py'), run_name='__main__')
        elif s == 'table':
            build_table()
        else:
            raise SystemExit(f'unknown step {s}')
        print(f'=== {s} done in {time.time() - t0:.0f} s ===', flush=True)


def _inv(sysn, tdb, phases, Twin):
    """One pycalphad invariant from binary_invariants_pycalphad.csv: phase set + T window (C)."""
    b = pd.read_csv(os.path.join(DATA, 'binary_invariants_pycalphad.csv'))
    g = b[(b.system == sysn) & (b.tdb == tdb) & (b.phases == '+'.join(sorted(phases))) &
          (b.T_C >= Twin[0]) & (b.T_C <= Twin[1])]
    if not len(g):
        return None
    r = g.iloc[0]
    return float(r.T_C), json.loads(r.compositions)


def pyc_rows():
    """All pycalphad numbers that enter comparison.csv, keyed for the literature lookup."""
    rows = []

    def add(key, sysn, qty, val, db, notes=''):
        rows.append(dict(key=key, system_or_alloy=sysn, quantity=qty, pycalphad_value=val, database=db, notes_pyc=notes))
    mcal = 'mc_al v2.032 (MatCalc open, pycalphad/binder TDB; sha256 54624a7b...)'
    mcni = 'mc_ni v2.036 (MatCalc open; sha256 84ba8131...)'
    # AlSi10Mg family
    a = pd.read_csv(os.path.join(DATA, 'al_alloys_summary.csv')).set_index('alloy')
    for al in a.index:
        r = a.loc[al]
        k = al
        add(f'{k}|liquidus', al, 'equilibrium liquidus (C)', r.eq_liquidus_C, mcal)
        add(f'{k}|solidus', al, 'equilibrium solidus (C)', r.eq_solidus_C, mcal)
        add(f'{k}|eutectic', al, 'Al-Si eutectic start, equilibrium (C)', r.eq_SI_DIAMOND_A4_start_C, mcal)
        add(f'{k}|eq_range', al, 'equilibrium freezing range (K)', r.eq_freezing_range_C, mcal)
        add(f'{k}|scheil_fs90', al, 'Scheil T at fs=0.90 (C)', r.scheil_T_fs90_C, mcal)
        add(f'{k}|scheil_fs99', al, 'Scheil T at fs=0.99 (C)', r.scheil_T_fs99_C, mcal)
        add(f'{k}|scheil_end', al, 'Scheil terminal (final eutectic) T (C)', r.scheil_terminal_C, mcal)
        add(f'{k}|scheil_range', al, 'Scheil freezing range, equilibrium liquidus to fs=0.99 (K)',
            r.eq_liquidus_C - r.scheil_T_fs99_C, mcal, 'Scheil uses 1 K steps from liquidus + 2 K')
        add(f'{k}|scheil_feut', al, 'Scheil fraction eutectic (mole)', r.scheil_fraction_eutectic, mcal,
            'solid formed after Si first appears')
        add(f'{k}|eq_feut', al, 'equilibrium liquid fraction at eutectic start (mole)', r.eq_fraction_liquid_at_Si_start, mcal)
        add(f'{k}|Si_mass_300', al, 'equilibrium Si mass fraction at 300 C', r.eq_mass_SI_DIAMOND_A4_300C, mcal)
        add(f'{k}|Mg2Si_mass_300', al, 'equilibrium Mg2Si mass fraction at 300 C', r.eq_mass_MG2SI_B_300C, mcal)
        if 'Fe' in al:
            add(f'{k}|beta_mass_500', al, 'equilibrium beta-AlFeSi (ALFESI_T6) mass fraction at 500 C',
                r.eq_mass_ALFESI_T6_500C, mcal)
        if 'powder' in al:
            for ph, lab in (('FCC_A1', '(Al) FCC_A1'), ('SI_DIAMOND_A4', 'Si (diamond)'), ('MG2SI_B', 'Mg2Si'),
                            ('ALFESI_T6', 'beta-AlFeSi (ALFESI_T6)'), ('PI_ALFEMGSI', 'pi-AlFeMgSi'),
                            ('ALCRFEMNSI_A', 'alpha-Al(Fe,Mn)Si (ALCRFEMNSI_A)')):
                add(f'{k}|mass_{ph}_25', al, f'equilibrium {lab} mass fraction at 25 C', r.get(f'eq_mass_{ph}_25C', np.nan), mcal)
            fe = sum(r.get(f'eq_mass_{ph}_25C', 0.0) for ph in ('ALFESI_T6', 'ALFESI_T5', 'PI_ALFEMGSI', 'AL13FE4', 'ALCRFEMNSI_A'))
            add(f'{k}|mass_FeIMC_25', al, 'equilibrium total Fe-bearing intermetallics, mass fraction at 25 C', fe, mcal,
                'all Fe phases: ' + str(r.get('eq_all_phases_mass_25C', '')))
    # Al-Zr
    z = pd.read_csv(os.path.join(DATA, 'alzr_summary.csv'))
    for _, r in z.iterrows():
        db = r.database.replace('SGTE ', 'SGTE binary ') if 'SGTE' in r.database else mcal
        if not isinstance(r.get('reaction'), str) or r.reaction.startswith('failed'):
            continue
        add('AlZr|invariant_T', 'Al-Zr (Al-rich)', 'Al-rich invariant T (C)', r.invariant_T_C, db, r.reaction)
        add('AlZr|fcc_solubility', 'Al-Zr (Al-rich)', 'max Zr solubility in (Al) at the invariant (wt%)', r.wt_fcc_at_invariant, db)
        add('AlZr|liq_at_invariant', 'Al-Zr (Al-rich)', 'liquid composition at the invariant (at% Zr)', 100 * r.x_liq_at_invariant, db)
        add('AlZr|liquidus_0.217', 'Al-0.217Zr (wt%)', 'liquidus (C)', r.get('liquidus_0.217wtZr_C', np.nan), db)
        add('AlZr|liquidus_0.5', 'Al-0.5Zr (wt%)', 'liquidus (C)', r['liquidus_0.5wtZr_C'], db)
        add('AlZr|liquidus_1.0', 'Al-1.0Zr (wt%)', 'liquidus (C)', r['liquidus_1wtZr_C'], db)
    # Al-Mn-Cr-Zr
    m = pd.read_csv(os.path.join(DATA, 'almncrzr_summary.csv'))
    for _, r in m.iterrows():
        k = r.alloy.split(' ')[1]
        add(f'AlMn{k}|liquidus', r.alloy, 'equilibrium liquidus (C)', r.eq_liquidus_C, mcal, f'primary {r.eq_primary_phase}; Fe, Si omitted')
        add(f'AlMn{k}|fcc_start', r.alloy, '(Al) start T, equilibrium (C)', r.eq_fcc_start_C, mcal)
        add(f'AlMn{k}|solidus', r.alloy, 'equilibrium solidus (C)', r.eq_solidus_C, mcal)
        add(f'AlMn{k}|scheil_fs99', r.alloy, 'Scheil T at fs=0.99 (C)', r.get('scheil_T_fs99_C', np.nan), mcal)
    # SGTE binary invariants: (key, system label, ORCHID system, phases, T window C, liquid element)
    specs = [
        ('AlSi|eut', 'Al-Si', 'AL-SI', ['AlSi-97Feu-LB.tdb', 'AlSi-14Lia.tdb'], ['DIAMOND_A4', 'FCC_A1', 'LIQUID'], (560, 590), 'eutectic L -> (Al) + (Si)'),
        ('AlCu|eut_Al', 'Al-Cu', 'AL-CU', ['AlCu-21Kro.tdb', 'AlCu-98Sau-LB.tdb'], ['AL2CU_C16', 'FCC_A1', 'LIQUID'], (530, 560), 'eutectic L -> (Al) + theta-Al2Cu'),
        ('AlCu|perit_theta', 'Al-Cu', 'AL-CU', ['AlCu-21Kro.tdb'], ['AL2CU_C16', 'ALCU_ETA_HT', 'LIQUID'], (580, 600), 'peritectic L + eta -> theta'),
        ('AlCu|perit_theta', 'Al-Cu', 'AL-CU', ['AlCu-98Sau-LB.tdb'], ['AL2CU_C16', 'ALCU_ETA', 'LIQUID'], (580, 600), 'peritectic L + eta -> theta'),
        ('AlCu|eut_Cu', 'Cu-Al', 'AL-CU', ['AlCu-21Kro.tdb', 'AlCu-98Sau-LB.tdb'], ['BCC_A2', 'FCC_A1', 'LIQUID'], (1020, 1060), 'eutectic L -> (Cu) + beta'),
        ('AlCu|eutectoid', 'Cu-Al', 'AL-CU', ['AlCu-21Kro.tdb'], ['BCC_A2', 'FCC_A1', 'GAMMA_D83'], (550, 580), 'eutectoid beta -> (Cu) + gamma2'),
        ('AlCu|eutectoid', 'Cu-Al', 'AL-CU', ['AlCu-98Sau-LB.tdb'], ['AL4CU9_D83', 'BCC_A2', 'FCC_A1'], (550, 580), 'eutectoid beta -> (Cu) + gamma2'),
        ('CrCu|eut', 'Cu-Cr', 'CR-CU', ['CrCu-17Liu.tdb', 'CrCu-95Zen-LB.tdb'], ['BCC_A2', 'FCC_A1', 'LIQUID'], (1060, 1082), 'eutectic L -> (Cu) + (Cr)'),
        ('CuZr|eut', 'Cu-Zr', 'CU-ZR', ['CuZr-22Zho.tdb', 'CuZr-94Zen-LB.tdb'], ['CU5ZR_C15B', 'FCC_A1', 'LIQUID'], (950, 990), 'eutectic L -> (Cu) + Cu5Zr'),
        ('CuSn|perit', 'Cu-Sn', 'CU-SN', ['CuSn-24Oik.tdb'], ['BCC_4SL', 'FCC_A1', 'LIQUID'], (770, 810), 'peritectic L + (Cu) -> beta'),
        ('CuSn|perit', 'Cu-Sn', 'CU-SN', ['CuSn-96Shi-LB.tdb'], ['BCC_A2', 'FCC_A1', 'LIQUID'], (770, 810), 'peritectic L + (Cu) -> beta'),
    ]
    for key, lab, sysn, tdbs, phases, Tw, reac in specs:
        for tdb in tdbs:
            r = _inv(sysn, tdb, phases, Tw)
            if r is None:
                add(key, lab, f'{reac}: T (C)', np.nan, 'SGTE binary ' + tdb, 'invariant not found in the map')
                continue
            T, comp = r
            add(key, lab, f'{reac}: T (C)', T, 'SGTE binary ' + tdb)
            if 'LIQUID' in comp:
                ax_el = {'AL-SI': 'Si', 'AL-CU': 'Cu', 'CR-CU': 'Cr', 'CU-ZR': 'Zr', 'CU-SN': 'Sn'}[sysn]
                add(key + '|xliq', lab, f'{reac}: liquid composition (at% {ax_el})', 100 * comp['LIQUID'], 'SGTE binary ' + tdb)
    # Cu alloys (mc_ni) and Cu-Ni binaries
    c = pd.read_csv(os.path.join(DATA, 'cu_alloys_summary.csv'))
    for _, r in c.iterrows():
        k = r.alloy.split(' ')[0]
        if 'Mn)' in r.alloy and k == 'C63000':
            k = 'C63000Mn'
        add(f'{k}|liquidus', r.alloy, 'equilibrium liquidus (C)', r.eq_liquidus_C, mcni, f'primary {r.eq_primary_phase}')
        add(f'{k}|solidus', r.alloy, 'equilibrium solidus (C)', r.eq_solidus_C, mcni)
        add(f'{k}|scheil_fs99', r.alloy, 'Scheil T at fs=0.99 (C)', r.get('scheil_T_fs99_C', np.nan), mcni)
    cn = pd.read_csv(os.path.join(DATA, 'cuni_binary_liquidus_solidus.csv'))
    for _, r in cn[cn.wt_Ni.isin([10, 30]) & cn.database.str.startswith('SGTE')].iterrows():   # mc_ni rows: Cu alloys above
        db = r.database.replace('SGTE ', 'SGTE binary ')
        add(f'Cu-{int(r.wt_Ni)}Ni|liquidus', f'Cu-{int(r.wt_Ni)}Ni (binary)', 'equilibrium liquidus (C)', r.liquidus_C, db)
        add(f'Cu-{int(r.wt_Ni)}Ni|solidus', f'Cu-{int(r.wt_Ni)}Ni (binary)', 'equilibrium solidus (C)', r.solidus_C, db)
    # NAB phase landmarks (mc_ni)
    for tag in ('C63000', 'C95800'):
        f = os.path.join(DATA, f'nab_{tag}_phase_fractions_mc_ni.csv')
        if not os.path.exists(f):
            continue
        d = pd.read_csv(f).sort_values('T_C')
        if 'beta (Cu-rich bcc)' in d:
            b = d[d['beta (Cu-rich bcc)'] > 1e-4]
            add(f'{tag}|beta_out', f'{tag} NAB', 'lowest T with equilibrium beta, 5 C grid (C)', b.T_C.min() if len(b) else np.nan, mcni)
        if 'alpha (fcc)' in d:
            al = d[d['alpha (fcc)'] > 1e-4]
            add(f'{tag}|alpha_in', f'{tag} NAB', 'alpha (fcc) start on cooling, 5 C grid (C)', al.T_C.max() if len(al) else np.nan, mcni)
        for t in (900, 800, 600):
            rr = d[np.isclose(d.T_C, t)]
            if len(rr):
                rr = rr.iloc[0]
                desc = '; '.join(f'{k} {rr[k]:.3f}' for k in d.columns[1:] if rr[k] > 1e-3)
                add(f'{tag}|fractions_{t}', f'{tag} NAB', f'equilibrium phase mole fractions at {t} C', desc, mcni)
    return pd.DataFrame(rows)


def build_table():
    p = pyc_rows()
    lit_f = os.path.join(DATA, 'literature_values.csv')
    lit = pd.read_csv(lit_f) if os.path.exists(lit_f) else pd.DataFrame(columns=['key'])
    cols = ['thermocalc_value', 'thermocalc_db', 'thermocalc_source_doi', 'experiment_value', 'experiment_source', 'notes']
    for c in cols:
        if c not in lit:
            lit[c] = np.nan
    m = p.merge(lit[['key'] + cols], on='key', how='left')

    def delta(a, b):
        try:
            return float(a) - float(b)
        except (TypeError, ValueError):
            return np.nan
    m['delta_pycalphad_vs_tc'] = [delta(a, b) for a, b in zip(m.pycalphad_value, m.thermocalc_value)]
    m['delta_pycalphad_vs_exp'] = [delta(a, b) for a, b in zip(m.pycalphad_value, m.experiment_value)]
    m['notes'] = [' | '.join(str(x) for x in (a, b) if isinstance(x, str) and x) for a, b in zip(m.notes_pyc, m.notes)]

    def rnd(x):
        try:
            return round(float(x), 4) if abs(float(x)) < 2 else round(float(x), 1)
        except (TypeError, ValueError):
            return x
    for c in ('pycalphad_value', 'thermocalc_value', 'experiment_value', 'delta_pycalphad_vs_tc', 'delta_pycalphad_vs_exp'):
        m[c] = m[c].map(rnd)
    out = m[['system_or_alloy', 'quantity', 'pycalphad_value', 'database', 'thermocalc_value', 'thermocalc_db',
             'thermocalc_source_doi', 'experiment_value', 'experiment_source', 'delta_pycalphad_vs_tc',
             'delta_pycalphad_vs_exp', 'notes']]
    out.to_csv(os.path.join(DATA, 'comparison.csv'), index=False)
    print(f'comparison.csv: {len(out)} rows; {out.thermocalc_value.notna().sum()} with a Thermo-Calc value, '
          f'{out.experiment_value.notna().sum()} with an experimental value', flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
