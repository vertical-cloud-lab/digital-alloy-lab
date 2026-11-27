"""CALPHAD for the 316L of the M2 wall build, with pycalphad and an open database (issue #100, PR #243).

    python calphad_316l.py          # -> out/calphad_316l_summary.json, out/calphad_316l_scheil.csv,
                                    #    out/calphad_316l_keyhole.csv, out/m2-calphad-316l.png
                                    #    (about 7 min on 4 cores the first time; seconds once .cache/ has the results)
    python calphad_316l.py fresh    # recompute the CALPHAD part instead of reading .cache/
    python calphad_316l.py --sets other_sets.csv [--sheet other_sheet.csv]   # score another sheet

The keyhole table is rebuilt from out/wall_sets.csv (power, speed, spot and trace spacing of each set's hatch, the
"Adv. surface area" tab) on every run, so a changed sheet only needs a rerun (seconds). out/wall_sheet.csv is
optional: its Ke and Eagar-Tsai columns are copied when present and the set's P, v and spot match.

Needs pycalphad >= 0.11 (Workspace API), numpy, matplotlib. Findings and caveats: calphad.md.

What it computes, for a mid-spec 316L and the two ferrite corners of the 316L specification:

1. Equilibrium solidification: liquidus, solidus, primary solid phase, phase fractions from the liquidus down to
   1000 C (1273 K).
2. Scheil-Gulliver solidification, twice: classic (no diffusion in the solid), and with C and N treated as fast
   diffusers (lever rule for C and N, Scheil for the substitutional elements; an approximation to Thermo-Calc's
   "Scheil with fast diffusers"). Records the delta-ferrite formed, the residual liquid's composition and the
   composition of the austenite forming at each step (what EDS across a cell boundary samples).
3. A sweep along the line from the low-ferrite to the high-ferrite corner of the spec: liquidus, primary phase and
   the ferrite a 3-phase Scheil forms, against the WRC-1992 Creq/Nieq ratio.
4. Enthalpy from 298 K to melting, h_s, to the solidus and to the liquidus, with and without the latent heat.
5. King et al.'s normalized enthalpy for every wall set, dH/h_s = A P / (h_s sqrt(pi D v sigma^3))
   (J. Mater. Process. Technol. 214, 2915 (2014), Eq. 2.6, https://doi.org/10.1016/j.jmatprotec.2014.06.005),
   with each set's own spot and sigma the Gaussian standard deviation of the beam, D4sigma / 4 (their footnotes 1
   and 4). The script checks the formula and sigma against two values the paper quotes (Fig. 6: 44 and 57); reading
   sigma as the 1/e^2 radius (spot / 2) instead does not reproduce them, and gives values 2^1.5 = 2.83 times lower
   (column dH_hs_if_sigma_is_radius, for comparison only).

Database: MatCalc's open steel database mc_fe 2.062 (TU Wien, E. Povoden-Karadeniz and A. Jacob), released under
the Open Database License 1.0 with contents under the Database Contents License 1.0. It is not committed: the
script downloads it into .cache/ (gitignored) from a pinned URL and checks its sha256. pycalphad cannot read it
as distributed, so `load_database` applies these fixes in memory (counts go into the summary JSON):

- decode as Latin-1 and drop CR line ends;
- cut the reference list at the end, which is not commented out;
- drop MatCalc-only commands: REFERENCE_ELEMENT, ADD_COMPOSITION_SET (pycalphad finds miscibility gaps itself)
  and ATTACH_CONTRIBUTION (MatCalc's order-disorder link of BCC_B2 to BCC_A2; BCC_B2 is left out of every
  calculation here, as is MatCalc's dislocation pseudo-phase BCC_DISL);
- drop HMVA parameters (MatCalc's vacancy formation enthalpy, not a Gibbs energy term);
- keep only parameters whose constituents are all in Fe-Cr-Ni-Mo-Mn-Si-C-N-Va, and only phases that can form
  from those elements (this also skips typos in parameters for other elements, e.g. PDMN_B2);
- close commands that lack their '!' terminator, read '6000.00.00' as '6000.00', '(PHASE;' as '(PHASE,', strip
  reference tags (one has a space in it) and anything after the last ':' of a CONSTITUENT command.

Phase fractions are mole fractions of atoms (pycalphad's NP), and compositions are given in wt%.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
import time
import urllib.request
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
CACHE = HERE / ".cache"
sys.path.insert(0, str(HERE))

from eagar_tsai_316l import ABSORPTIVITY, MATERIALS, T0, T_BOIL  # noqa: E402  (numpy-only at import time)

CODE_VERSION = "2026-11-19.2"   # bump to invalidate .cache/ results after changing a calculation

# --- database ---------------------------------------------------------------------------------------------------
DB = dict(
    name="MatCalc open steel database mc_fe",
    version="2.062 (file mc_fe_v2.062_8.11.2024.tdb, dated 2024-11-08)",
    url="https://www.matcalc.at/images/stories/Download/Database/mc_fe_v2062.tdb",
    page="https://www.matcalc.at/index.php/databases/open-databases",
    sha256="aa02077eac3f602dd7479cbeafb09b450e282716752b3ae2b1fc3a57d9c64865",
    licence="Open Database License (ODbL) 1.0, http://opendatacommons.org/licenses/odbl/1.0/; individual contents "
            "under the Database Contents License (DbCL) 1.0, http://opendatacommons.org/licenses/dbcl/1.0/",
    holder="E. Povoden-Karadeniz and A. Jacob, TU Wien (copyright holder and editor: E. Povoden-Karadeniz)",
    assessed_range="673-2000 K (stated in the file)",
)
DB_FILE = CACHE / "mc_fe_v2062.tdb"

ELEMENTS = ("FE", "CR", "NI", "MO", "MN", "SI", "C", "N")
COMPS = list(ELEMENTS) + ["VA"]
MOLAR_MASS = dict(FE=55.845, CR=51.996, NI=58.693, MO=95.95, MN=54.938, SI=28.085, C=12.011, N=14.007)  # g/mol

# --- compositions (wt%, Fe balance) --------------------------------------------------------------------------------
# No powder certificate for the lab's 316L is in the repo (lpbf-runs/m2-single-track-schedule.md still lists the lot
# and certificate as to-do), so the nominal is the middle of the 316L ranges. The corners push every element to the
# ferrite-promoting or austenite-promoting end of the spec; the spec only caps C, N, Mn and Si, so the
# ferrite-promoting corner uses small floors (C 0.005, N 0.01, Mn 0.1) instead of zero, as a real powder would.
SPEC = dict(CR=(16.0, 18.0), NI=(10.0, 14.0), MO=(2.0, 3.0), MN=(0.0, 2.0), SI=(0.0, 1.0), C=(0.0, 0.03), N=(0.0, 0.10))
SPEC_NOTE = ("ASTM A240 (UNS S31603): C <= 0.030, Mn <= 2.00, Si <= 0.75, Cr 16.0-18.0, Ni 10.0-14.0, Mo 2.00-3.00, "
             "N <= 0.10 wt%; ASTM F3184 (316L for powder bed fusion) allows Si <= 1.00. P and S are left out "
             "(not in the database subset used).")
COMPOSITIONS = {
    "nominal": dict(CR=17.0, NI=12.0, MO=2.5, MN=1.0, SI=0.5, C=0.020, N=0.050),
    "high_ferrite": dict(CR=18.0, NI=10.0, MO=3.0, MN=0.1, SI=1.0, C=0.005, N=0.010),
    "low_ferrite": dict(CR=16.0, NI=14.0, MO=2.0, MN=2.0, SI=0.1, C=0.030, N=0.100),
}
SWEEP_N = 11   # points on the straight line (in wt%) from low_ferrite (t = 0) to high_ferrite (t = 1)

# --- phases ------------------------------------------------------------------------------------------------------
PH_SOLIDIFY = ["LIQUID", "FCC_A1", "BCC_A2"]
PH_LATE = ["HCP_A3", "M23C6", "M7C3", "M6C", "SIGMA", "LAVES_PHASE", "CHI_A12", "MU_PHASE"]
PH_SCHEIL = PH_SOLIDIFY + PH_LATE
PH_ALL = PH_SCHEIL + ["CEMENTITE", "PI_PHASE", "R_PHASE", "G_PHASE", "MOC_ETA", "KSI_CARBIDE", "M3C2"]
T_LOW = 1273.15            # K, 1000 C: bottom of the equilibrium scans
SCHEIL_STOP = 1e-4         # liquid fraction at which the Scheil runs stop
TC_TERMINAL_FL = 0.01      # Thermo-Calc's Scheil default stops at 1% liquid; its "solidus" is the T there

# --- WRC-1992 ------------------------------------------------------------------------------------------------------
# Creq = Cr + Mo + 0.7 Nb, Nieq = Ni + 35 C + 20 N + 0.25 Cu (Kotecki and Siewert, Weld. J. 71, 171s (1992)).
# Mode boundaries on Creq/Nieq as usually quoted for WRC-1992 (Lippold and Kotecki, Welding Metallurgy and
# Weldability of Stainless Steels, Wiley 2005): A < 1.25 <= AF < 1.48 <= FA < 1.95 <= F.
WRC_BOUNDS = ((1.25, "A"), (1.48, "AF"), (1.95, "FA"), (math.inf, "F"))

# --- keyhole criterion ----------------------------------------------------------------------------------------------
# Each set's spot is taken as the 1/e^2 = D4sigma diameter. King et al.'s sigma: I = I0 exp(-r^2 / (2 sigma^2)),
# so sigma = D4sigma / 4 (32.5 um for the control's 130 um spot).
SPOT_CONTROL_UM = 130.0
REPO = MATERIALS["nominal"]           # eagar_tsai_316l.py: k 26, rho 7300, cp 710, T_liq 1723 K
D_REPO = REPO["k"] / (REPO["rho"] * REPO["cp"])   # 5.02e-6 m^2/s
RHO_298 = 7980.0                      # kg/m^3, 316L at room temperature (King et al.'s Table 3) for h_s per volume
KING_T3 = dict(A=0.4, rho=7980.0, h_s_J_kg=1.2e6, D=5.38e-6)   # King et al., Table 3 (manuscript PDF p. 36)
KING_THRESHOLD, KING_ERR = 30.0, 4.0  # Sec. 5.6 and conclusion 4 (PDF pp. 19-20): dH/h_s = 30 +/- 4
KING_BAND = (26.0, 34.0)              # Sec. 5.3 (PDF p. 15): mode changes from ~26; above ~34 clearly keyhole
T_BOIL_KING = 3273.0                  # K, "for steel", Sec. 2 (PDF p. 5)
KING_CHECKS = (  # (P W, v mm/s, D4sigma um, dH/h_s quoted): Fig. 6 caption (PDF p. 28) and Sec. 5.3 (PDF p. 16)
    (334.0, 171.0, 130.0, 44.0), (265.0, 1004.0, 52.0, 57.0))
KE_BANDS = ((1.4, "conduction"), (6.0, "transition"), (16.0, "keyhole, stable"), (30.0, "keyhole, fluctuating"),
            (math.inf, "keyhole, unstable (pores)"))   # as line_sheet.KE_BANDS (Gan et al. 2021)


# --- helpers -------------------------------------------------------------------------------------------------------
def to_x(wt: dict) -> dict:
    """wt% (Fe balance) -> mole fractions of every element."""
    w = dict(wt)
    w["FE"] = 100.0 - sum(wt.values())
    mol = {k: w[k] / MOLAR_MASS[k] for k in w}
    tot = sum(mol.values())
    return {k: mol[k] / tot for k in mol}


def to_wt(x: dict) -> dict:
    """Mole fractions (any subset of ELEMENTS summing to ~1) -> wt%."""
    m = {k: x[k] * MOLAR_MASS[k] for k in x}
    tot = sum(m.values())
    return {k: 100.0 * m[k] / tot for k in m}


def molar_mass(x: dict) -> float:
    return sum(x[k] * MOLAR_MASS[k] for k in x)   # g per mole of atoms


def wrc1992(wt: dict) -> dict:
    creq = wt["CR"] + wt["MO"]
    nieq = wt["NI"] + 35.0 * wt["C"] + 20.0 * wt["N"]
    r = creq / nieq
    return dict(Creq=round(creq, 3), Nieq=round(nieq, 3), ratio=round(r, 4),
                mode=next(m for b, m in WRC_BOUNDS if r < b))


def file_sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fetch_database() -> Path:
    CACHE.mkdir(exist_ok=True)
    if not DB_FILE.exists():
        print(f"downloading {DB['url']}")
        req = urllib.request.Request(DB["url"], headers={"User-Agent": "Mozilla/5.0 (pycalphad script)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        DB_FILE.write_bytes(data)
    sha = file_sha256(DB_FILE)
    if sha != DB["sha256"]:
        raise RuntimeError(f"{DB_FILE} has sha256 {sha}, expected {DB['sha256']}; delete it or update DB['sha256'] "
                           "after checking what changed")
    return DB_FILE


_KW = re.compile(r"^\s*(PARAMETER|PARAM|FUNCTION|FUNCT|PHASE|CONSTITUENT|CONST|ELEMENT|TYPE_DEFINITION|"
                 r"REFERENCE_ELEMENT|ADD_COMPOSITION_SET|ATTACH_CONTRIBUTION)\b", re.I)
_PAR = re.compile(r"^PARAM[A-Z]*\s+([A-Z0-9_]+)\(\s*([A-Z0-9_]+)\s*[,;]\s*([^;]*);", re.I)
_CON = re.compile(r"^CONST[A-Z]*\s+([A-Z0-9_]+)\s*:(.*):", re.I | re.S)


def clean_tdb(raw_bytes: bytes) -> tuple[str, dict]:
    """The MatCalc file -> TDB text pycalphad can read, restricted to ELEMENTS (see the module docstring)."""
    els = set(ELEMENTS) | {"VA"}
    fixes = dict.fromkeys(["reference list cut", "MatCalc-only commands dropped", "HMVA parameters dropped",
                           "parameters for other elements dropped", "phases impossible here dropped",
                           "unterminated commands closed", "'(PHASE;' typos fixed", "'x.y.z' numbers fixed",
                           "CONSTITUENT tails stripped"], 0)
    raw = raw_bytes.decode("latin-1").replace("\r", "")
    cut = raw.find("$ E) List of references")
    if cut > 0:
        raw, fixes["reference list cut"] = raw[:cut], 1
    lines = [ln.split("$", 1)[0] for ln in raw.split("\n")]          # '$' starts a comment, as in pycalphad
    cmds, cur = [], []
    for ln in lines:
        if _KW.match(ln) and "".join(cur).strip():                   # previous command never got its '!'
            cmds.append(" ".join(cur))
            cur = []
            fixes["unterminated commands closed"] += 1
        parts = ln.split("!")
        for p in parts[:-1]:
            cur.append(p)
            cmds.append(" ".join(cur))
            cur = []
        cur.append(parts[-1])
    if "".join(cur).strip():
        cmds.append(" ".join(cur))
    cmds = [c.strip() for c in cmds if c.strip()]

    ok_phase = set()
    for c in cmds:
        if c.split()[0].upper().startswith("CONST"):
            m = _CON.match(c)
            subl = [set(s.replace("%", "").replace(" ", "").upper().split(",")) - {""} for s in m.group(2).split(":")]
            if all(sl & els for sl in subl):
                ok_phase.add(m.group(1).upper())
    keep = []
    for c in cmds:
        k = c.split()[0].upper()
        if k in ("REFERENCE_ELEMENT", "ADD_COMPOSITION_SET", "ATTACH_CONTRIBUTION"):
            fixes["MatCalc-only commands dropped"] += 1
            continue
        if k == "PHASE" or k.startswith("CONST"):
            if c.split()[1].upper() not in ok_phase:
                fixes["phases impossible here dropped"] += k == "PHASE"
                continue
            if k.startswith("CONST") and c[c.rfind(":") + 1:].strip():
                c = c[: c.rfind(":") + 1]
                fixes["CONSTITUENT tails stripped"] += 1
        if k.startswith("PARAM"):
            m = _PAR.match(c)
            ptype, phase, consts = m.groups()
            if ptype.upper() == "HMVA":
                fixes["HMVA parameters dropped"] += 1
                continue
            species = set(re.split(r"[,:]", consts.upper().replace(" ", ""))) - {"*"}
            if not species <= els or phase.upper() not in ok_phase:
                fixes["parameters for other elements dropped"] += 1
                continue
            c, n = re.subn(r"^(PARAM[A-Z]*\s+[A-Z0-9_]+\(\s*[A-Z0-9_]+)\s*;", r"\1,", c, flags=re.I)
            fixes["'(PHASE;' typos fixed"] += n
            c, n = re.subn(r"(?<![\d.])(\d+\.\d+)\.\d+(?![\d.])", r"\1", c)
            fixes["'x.y.z' numbers fixed"] += n
            c = re.sub(r"(;\s*[\d.]+\s+N)\b.*$", r"\1", c, flags=re.S | re.I)
        keep.append(c)
    return " !\n".join(keep) + " !\n", fixes


# Diagnostic variant. Two ternary FCC terms in mc_fe 2.062, L(FCC_A1,CR,FE,SI:VA;0) = L(FCC_A1,FE,MO,SI:VA;0) =
# 50000 - 80 T J/mol, are about -86 kJ/mol at 1700 K. With ~1 wt% Si they make austenite ~0.2 kJ/mol more stable
# than the Fe-Cr-Ni-Mo core alone, enough to make austenite the primary phase across the whole 316L spec. The
# variant "no_fcc_si_ternaries" drops them (the binaries then extrapolate, the usual default when a ternary is
# unassessed) to show how much the answer hangs on them. It is not a better database, just a sensitivity check.
SI_TERNARIES = (["CR", "FE", "SI"], ["FE", "MO", "SI"])
_DBF: dict = {}


def load_database(variant: str = "as_distributed"):
    """Parsed pycalphad Database (one per process and variant), and the parsing fixes applied."""
    from pycalphad import Database
    from tinydb import where

    if variant not in _DBF:
        text, fixes = clean_tdb(fetch_database().read_bytes())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            dbf = Database(text)
        if variant == "no_fcc_si_ternaries":
            gone = dbf._parameters.remove(
                (where("phase_name") == "FCC_A1") & (where("parameter_type") == "L")
                & where("constituent_array").test(lambda ca: sorted(str(sp) for sp in ca[0]) in SI_TERNARIES))
            assert len(gone) == 2, gone
        _DBF[variant] = (dbf, fixes)
    return _DBF[variant]


def _label(phase: str, xrow: dict) -> str:
    """Name a composition set: FCC/HCP sets rich in C+N are carbonitrides, not austenite or a metal."""
    if phase in ("FCC_A1", "HCP_A3", "BCC_A2") and xrow.get("C", 0) + xrow.get("N", 0) > 0.2:
        return {"FCC_A1": "MX (FCC_A1#2)", "HCP_A3": "M2X (HCP_A3)", "BCC_A2": "BCC_A2#2"}[phase]
    return phase


def _point(wks) -> list[tuple[str, float, dict]]:
    """Stable composition sets of a point equilibrium: (label, NP, {element: X})."""
    eq = wks.eq
    ph = np.asarray(eq.Phase).reshape(-1)
    npf = np.asarray(eq.NP).reshape(-1)
    xx = np.asarray(eq.X).reshape(len(ph), -1)
    names = [str(c) for c in eq.coords["component"]]
    out = []
    for j, p in enumerate(ph):
        if p and np.isfinite(npf[j]) and npf[j] > 0:
            xr = {names[i]: float(xx[j, i]) for i in range(len(names))}
            out.append((_label(str(p), xr), float(npf[j]), xr))
    return out


def _workspace(phases, x, variant="as_distributed"):
    from pycalphad import Workspace, variables as v

    dbf, _ = load_database(variant)
    conds = {v.T: 1800.0, v.P: 101325.0, v.N: 1.0, **{v.X(k): x[k] for k in x if k != "FE"}}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return Workspace(dbf, COMPS, phases, conds)


def _set(wks, T, x):
    from pycalphad import variables as v

    wks.conditions = {v.T: float(T), v.P: 101325.0, v.N: 1.0, **{v.X(k): float(x[k]) for k in x if k != "FE"}}


def _fractions(pt) -> dict:
    f = {}
    for lab, npf, _ in pt:
        f[lab] = f.get(lab, 0.0) + npf
    return f


def liquidus_solidus(wks, x, lo=1550.0, hi=1800.0, tol=0.05) -> dict:
    """Bisection with the phases in wks: T_liq (first solid appears) and T_sol (last liquid goes)."""
    def fl(T):
        _set(wks, T, x)
        return _fractions(_point(wks)).get("LIQUID", 0.0)

    a, b = lo, hi                     # fl(a) < 1, fl(b) = 1
    while b - a > tol:
        m = 0.5 * (a + b)
        a, b = (m, b) if fl(m) < 1 - 1e-9 else (a, m)
    t_liq = 0.5 * (a + b)
    a, b = lo, t_liq                  # fl(a) = 0, fl(b) > 0
    while b - a > tol:
        m = 0.5 * (a + b)
        a, b = (a, m) if fl(m) > 1e-9 else (m, b)
    t_sol = 0.5 * (a + b)
    _set(wks, t_liq - 0.3, x)
    f = _fractions(_point(wks))
    primary = max((k for k in f if k != "LIQUID"), key=lambda k: f[k])
    return dict(T_liq=t_liq, T_sol=t_sol, primary=primary)


def single_phase_hm(phase: str, x: dict, Ts) -> np.ndarray:
    """Molar enthalpy (J per mole of atoms) of one phase held at the alloy's composition (no partitioning)."""
    from pycalphad import Model, calculate

    dbf, _ = load_database()
    mod = Model(dbf, COMPS, phase)
    ratios = [float(r) for r in mod.site_ratios]
    xi = x.get("C", 0.0) + x.get("N", 0.0)
    y = []
    for sf in mod.site_fractions:
        s, name = sf.sublattice_index, sf.species.name
        if len(mod.constituents) == 1:                   # liquid: one sublattice, site fraction = mole fraction
            y.append(max(x.get(name, 0.0), 1e-12))
        elif s == 0:                                       # metals
            y.append(max(x.get(name, 0.0) / (1.0 - xi), 1e-12))
        else:                                              # interstitials and vacancies, r sites per metal site
            r = ratios[1] / ratios[0]
            y.append(1.0 - xi / (r * (1.0 - xi)) if name == "VA" else max(x.get(name, 0.0) / (r * (1.0 - xi)), 1e-12))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = calculate(dbf, COMPS, phase, T=np.asarray(Ts, float), P=101325.0, points=np.array([y]),
                        output="HM", model={phase: mod})
    return np.asarray(res.HM.values).reshape(-1)


# --- tasks (run in worker processes) ----------------------------------------------------------------------------------
def task_equilibrium(name: str, wt: dict) -> dict:
    """Liquidus, solidus, primary phase, the equilibrium path to 1000 C, and the enthalpies."""
    x = to_x(wt)
    wks = _workspace(PH_SOLIDIFY, x)
    ls = liquidus_solidus(wks, x)
    rows = []
    t_hi = math.ceil(ls["T_liq"]) + 5.0
    for T in np.arange(t_hi, ls["T_sol"] - 6.0, -0.5):
        _set(wks, T, x)
        pt = _point(wks)
        row = dict(T=float(T), phases=_fractions(pt), HM=float(np.squeeze(wks.get("HM"))))
        row["X"] = {lab: xr for lab, _, xr in pt}
        rows.append(row)
    wks_all = _workspace(PH_ALL, x)
    for T in np.arange(math.floor(ls["T_sol"]) - 10.0, T_LOW - 1.0, -10.0):
        _set(wks_all, T, x)
        pt = _point(wks_all)
        rows.append(dict(T=float(T), phases=_fractions(pt), HM=float(np.squeeze(wks_all.get("HM"))),
                         X={lab: xr for lab, _, xr in pt}))
    _set(wks_all, T_LOW, x)
    low = _fractions(_point(wks_all))
    # enthalpy: metastable single-phase austenite from 298 K, liquid at the solidus and liquidus
    Ts = np.array([298.15, ls["T_sol"], ls["T_liq"]])
    h_fcc = single_phase_hm("FCC_A1", x, Ts)
    h_liq = single_phase_hm("LIQUID", x, Ts[1:])
    t_grid = np.arange(300.0, 1801.0, 25.0)
    h_fcc_grid = single_phase_hm("FCC_A1", x, t_grid)
    h_liq_grid = single_phase_hm("LIQUID", x, t_grid[t_grid >= 1500])
    mm = molar_mass(x) * 1e-3                                      # kg per mole of atoms
    per_kg = lambda h: float(h) / mm                                # noqa: E731
    _set(wks, ls["T_sol"] - 0.3, x)
    h_eq_sol = float(np.squeeze(wks.get("HM")))
    enth = dict(
        to_solidus_sensible=per_kg(h_fcc[1] - h_fcc[0]),
        to_liquidus_sensible=per_kg(h_fcc[2] - h_fcc[0]),
        to_solidus_with_latent=per_kg(h_liq[0] - h_fcc[0]),
        to_liquidus_with_latent=per_kg(h_liq[1] - h_fcc[0]),
        latent_at_solidus=per_kg(h_liq[0] - h_fcc[1]),
        latent_at_liquidus=per_kg(h_liq[1] - h_fcc[2]),
        check_fcc_vs_equilibrium_at_solidus=per_kg(h_fcc[1] - h_eq_sol),
        mean_cp_298_to_solidus=per_kg(h_fcc[1] - h_fcc[0]) / (ls["T_sol"] - 298.15),
        grid_T=t_grid.tolist(), grid_H_fcc_J_kg=[per_kg(h - h_fcc[0]) for h in h_fcc_grid],
        grid_T_liq=t_grid[t_grid >= 1500].tolist(), grid_H_liq_J_kg=[per_kg(h - h_fcc[0]) for h in h_liq_grid],
    )
    return dict(name=name, wt=wt, x=x, **ls, rows=rows, at_1000C=low, enthalpy=enth, wrc=wrc1992(wt))


def task_scheil(name: str, wt: dict, fast_cn: bool, phases=None, stop=SCHEIL_STOP, t_start=None,
                variant="as_distributed") -> dict:
    """Scheil-Gulliver on the liquid; with fast_cn, C and N follow the lever rule against all the solid so far."""
    phases = phases or PH_SCHEIL
    x0 = to_x(wt)
    wks = _workspace(phases, x0, variant)
    if t_start is None:
        t_start = liquidus_solidus(_workspace(PH_SOLIDIFY, x0), x0)["T_liq"] + 1.0
    T, dT, fl, xl = t_start, 1.0, 1.0, dict(x0)
    cum, k_last, steps = {}, {}, []
    while fl > stop and T > 1000.0:
        _set(wks, T, xl)
        pt = _point(wks)
        liq = [p for p in pt if p[0] == "LIQUID"]
        if not liq:                                   # stepped past the end: halve the step
            T += dT
            dT /= 2.0
            if dT < 0.02:
                break
            T -= dT
            continue
        np_l, x_l = liq[0][1], liq[0][2]
        formed = {}
        for lab, npf, xr in pt:
            if lab == "LIQUID":
                continue
            formed[lab] = formed.get(lab, 0.0) + fl * npf
            cum[lab] = cum.get(lab, 0.0) + fl * npf
            k_last[lab] = {e: xr[e] / max(x_l[e], 1e-12) for e in ("C", "N")}
        fl_new = fl * np_l
        x_next = dict(x_l)
        if fast_cn and cum:
            tot = sum(cum.values())
            for e in ("C", "N"):
                k_eff = sum(cum[lab] * k_last[lab][e] for lab in cum) / tot
                x_next[e] = x0[e] / (fl_new + k_eff * (1.0 - fl_new))
            subs = [e for e in ELEMENTS if e not in ("C", "N")]
            scale = (1.0 - x_next["C"] - x_next["N"]) / sum(x_l[e] for e in subs)
            for e in subs:
                x_next[e] = x_l[e] * scale
        steps.append(dict(T=T, f_solid=1.0 - fl_new, formed=formed, cum=dict(cum),
                          x_liquid=x_l, x_solid={lab: xr for lab, _, xr in pt if lab != "LIQUID"}))
        fl, xl = fl_new, x_next
        T -= dT
        if fl < 0.05:
            dT = min(dT * 1.05, 5.0)
    return dict(name=name, fast_cn=fast_cn, phases=phases, T_start=t_start, steps=steps, converged=fl <= stop)


def task_sweep(t: float, variant: str = "as_distributed") -> dict:
    lo, hi = COMPOSITIONS["low_ferrite"], COMPOSITIONS["high_ferrite"]
    wt = {k: lo[k] + t * (hi[k] - lo[k]) for k in lo}
    x = to_x(wt)
    ls = liquidus_solidus(_workspace(PH_SOLIDIFY, x, variant), x)
    sch = task_scheil(f"sweep_{t:.2f}", wt, False, phases=PH_SOLIDIFY, stop=TC_TERMINAL_FL, t_start=ls["T_liq"] + 1.0,
                      variant=variant)
    last = sch["steps"][-1]
    cum = last["cum"]
    fs = sum(cum.values())
    second = [lab for lab in cum if lab != ls["primary"] and cum[lab] > 0.005 * fs]
    return dict(t=t, variant=variant, wt=wt, wrc=wrc1992(wt), **ls, scheil_T_end=last["T"], scheil_f_solid=last["f_solid"],
                scheil_BCC=cum.get("BCC_A2", 0.0) / fs, scheil_FCC=cum.get("FCC_A1", 0.0) / fs,
                mode=_mode(ls["primary"], cum.get("BCC_A2", 0.0) / fs, cum.get("FCC_A1", 0.0) / fs))


def _mode(primary: str, f_bcc: float, f_fcc: float) -> str:
    """Weld-metallurgy mode from a Scheil path: A, AF (primary austenite + ferrite), FA, F."""
    if primary == "FCC_A1":
        return "AF" if f_bcc > 0.005 else "A"
    return "FA" if f_fcc > 0.005 else "F"


# --- driver ----------------------------------------------------------------------------------------------------------
def _cache_key() -> str:
    blob = json.dumps(dict(v=CODE_VERSION, db=DB["sha256"], comps=COMPOSITIONS, sweep=SWEEP_N, ph=PH_ALL,
                           sch=PH_SCHEIL, low=T_LOW, stop=SCHEIL_STOP), sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def _run(job):
    kind, args = job
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return kind, args, {"eq": task_equilibrium, "scheil": task_scheil, "sweep": task_sweep}[kind](*args)


def compute(fresh: bool = False) -> dict:
    cache = CACHE / f"calphad_results_{_cache_key()}.json"
    if cache.exists() and not fresh:
        return json.loads(cache.read_text())
    _, fixes = load_database()                       # download, check and parse once before forking
    jobs = [("scheil", (n, wt, f)) for n, wt in COMPOSITIONS.items() for f in (False, True)]
    jobs += [("eq", (n, wt)) for n, wt in COMPOSITIONS.items()]
    jobs += [("sweep", (float(t), var)) for var in ("as_distributed", "no_fcc_si_ternaries")
             for t in np.linspace(0.0, 1.0, SWEEP_N)]
    t0 = time.time()
    res = dict(eq={}, scheil={}, sweep=[], fixes=fixes, db=DB, key=_cache_key())
    with ProcessPoolExecutor(max_workers=4) as ex:
        for kind, args, r in ex.map(_run, jobs):
            print(f"  {kind} {args[0]:.4g} {args[1]}" if kind == "sweep" else
                  f"  {kind} {args[0]}{' fast C,N' if kind == 'scheil' and args[2] else ''}", f"{time.time() - t0:.0f} s")
            if kind == "eq":
                res["eq"][args[0]] = r
            elif kind == "scheil":
                res["scheil"][f"{args[0]}|{'fast_CN' if args[2] else 'classic'}"] = r
            else:
                res["sweep"].append(r)
    cache.write_text(json.dumps(res))
    return res


def at_fs(steps: list, fs: float, key):
    """Interpolate key(step) at solid fraction fs along a Scheil path."""
    f = np.array([s["f_solid"] for s in steps])
    vals = np.array([key(s) for s in steps], float)
    if fs < f[0]:
        return float(vals[0])
    return float(np.interp(fs, f, vals))


def scheil_summary(r: dict, wt0: dict) -> dict:
    st = r["steps"]
    T_at = {f"T_K_at_fs_{fs}": round(at_fs(st, fs, lambda s: s["T"]), 1) for fs in (0.5, 0.9, 0.95, 0.99)}
    end = st[-1]
    i01 = next(i for i, s in enumerate(st) if s["f_solid"] >= 1 - TC_TERMINAL_FL) if st[-1]["f_solid"] >= 0.99 else -1
    s01 = st[i01]
    tot01 = sum(s01["cum"].values())
    els = ("CR", "NI", "MO", "MN", "SI", "C", "N")

    def wt_of(xr):
        return to_wt({e: xr[e] for e in ELEMENTS})

    liq = {}
    for fs in (0.0, 0.5, 0.9, 0.95, 0.99):
        w = {e: at_fs(st, fs, lambda s, e=e: wt_of(s["x_liquid"])[e]) for e in els}
        liq[f"fs_{fs}"] = {e: round(w[e], 4 if e in ("C", "N") else 3) for e in els}
    fcc = {}
    for fs in (0.0, 0.5, 0.9, 0.95, 0.99):
        def g(s, e):
            xr = s["x_solid"].get("FCC_A1")
            return wt_of(xr)[e] if xr else np.nan
        pts = [s for s in st if "FCC_A1" in s["x_solid"]]
        if pts:
            fcc[f"fs_{fs}"] = {e: round(at_fs(pts, fs, lambda s, e=e: g(s, e)), 4 if e in ("C", "N") else 3)
                               for e in els}
    first = next(s for s in st if s["formed"])        # the first step that forms solid: the cell core
    k0 = {}
    prim = max(first["formed"], key=lambda lab: first["formed"][lab])
    if prim:
        k0 = {e: round(first["x_solid"][prim][e] / first["x_liquid"][e], 3) for e in els}
    bcc_steps = [s for s in st if "BCC_A2" in s["formed"] and s["formed"]["BCC_A2"] > 0]
    return dict(
        model="Scheil, C and N as fast diffusers (lever rule)" if r["fast_cn"] else "Scheil (classic)",
        phases_allowed=r["phases"], T_start_K=round(r["T_start"], 2), **T_at,
        T_K_at_1pct_liquid=round(s01["T"], 1), T_K_end=round(end["T"], 1), f_liquid_end=float(1 - end["f_solid"]),
        primary_phase=prim, partition_k_first_solid=k0,
        phase_fractions_at_1pct_liquid={k: round(v / tot01, 4) for k, v in s01["cum"].items() if v > 1e-6},
        phase_fractions_end={k: round(v, 5) for k, v in end["cum"].items() if v > 1e-7},
        delta_ferrite_first_T_K=round(bcc_steps[0]["T"], 1) if bcc_steps else None,
        delta_ferrite_first_f_solid=round(bcc_steps[0]["f_solid"], 3) if bcc_steps else None,
        liquid_wt_pct=liq, austenite_forming_wt_pct=fcc,
        cell_wall_over_core={e: round(fcc["fs_0.95"][e] / fcc["fs_0.0"][e], 2) for e in ("CR", "NI", "MO", "MN", "SI")}
        if "fs_0.95" in fcc else None,
        nominal_wt_pct=wt0,
    )


def king(P, v_mm_s, A, D, h_s_vol, sigma):
    """King et al. (2014) Eq. 2.6: dH/h_s = A P / (h_s sqrt(pi D v sigma^3)), sigma in m."""
    return A * P / (h_s_vol * math.sqrt(math.pi * D * v_mm_s * 1e-3 * sigma ** 3))


def keyhole_number(P, v_mm_s, spot_um):
    """Gan et al.'s Ke, as line_sheet.keyhole_number: eta P / ((T_l - T0) pi rho c sqrt(alpha v r0^3)), r0 = spot/2."""
    rhoc = REPO["rho"] * REPO["cp"]
    r0 = spot_um * 1e-6 / 2.0
    return ABSORPTIVITY * P / ((REPO["T_liq"] - T0) * math.pi * rhoc * math.sqrt(D_REPO * v_mm_s * 1e-3 * r0 ** 3))


def _col(header: list[str], *words) -> str:
    """The column of a WRX-style sheet whose name has every word, preferring the hatch tab."""
    hits = [h for h in header if all(w.lower() in h.lower() for w in words)]
    hatch = [h for h in hits if "adv. surface area" in h.lower()]
    if not (hatch or hits):
        raise KeyError(f"no column with {words} in {header}")
    return (hatch or hits)[0]


def read_sets(path: Path) -> list[dict]:
    """Hatch P (W), v (mm/s), spot (um) and trace spacing (mm) of every set in a wall_sets.csv."""
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        rows = list(rd)
        hdr = rd.fieldnames
    cP, cv, cd = _col(hdr, "power"), _col(hdr, "speed"), _col(hdr, "spot")
    ch = _col(hdr, "trace spacing")
    cw = next((h for h in hdr if h.lower().startswith("walls")), None)
    return [dict(set=r[_col(hdr, "set name")], P=float(r[cP]), v=float(r[cv]), spot=float(r[cd]), h=float(r[ch]),
                 walls=r[cw].split() if cw else []) for r in rows]


def keyhole_table(h_s_calphad_vol: float, sets_path: Path, sheet_path: Path) -> tuple[list, dict]:
    sheet = {}
    if sheet_path.exists():
        with open(sheet_path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                sheet.setdefault(r.get("set_name", ""), r)
    h_t3 = KING_T3["h_s_J_kg"] * KING_T3["rho"]
    rows = []
    for st in read_sets(sets_path):
        P, v, d = st["P"], st["v"], st["spot"]
        sig = d * 1e-6 / 4.0
        dh = king(P, v, KING_T3["A"], KING_T3["D"], h_t3, sig)
        dh_c = king(P, v, ABSORPTIVITY, D_REPO, h_s_calphad_vol, sig)
        ke = keyhole_number(P, v, d)
        sh = sheet.get(st["set"], {})
        same = sh and all(abs(float(sh.get(k, "nan") or "nan") - x) < 1e-6 for k, x in
                          (("power_W", P), ("speed_mm_s", v), ("spot_um", d)) if k in sh)
        sh = sh if same else {}

        def num(k):
            try:
                return float(sh[k])
            except (KeyError, ValueError, TypeError):
                return ""

        W, Dp = num("ET_width_um"), num("ET_depth_um")
        rows.append(dict(
            set=st["set"], P_W=P, v_mm_s=v, spot_um=d, trace_spacing_mm=st["h"], P_over_v_J_mm=round(P / v, 4),
            n_walls=len(st["walls"]), sigma_um=round(sig * 1e6, 2),
            dH_hs_King_constants=round(dh, 2),
            King_regime=("conduction (<26)" if dh < KING_BAND[0] else
                         ("transition (26-34)" if dh < KING_BAND[1] else "keyhole (>=34)")),
            King_keyhole=dh >= KING_THRESHOLD,
            dH_hs_CALPHAD_hs=round(dh_c, 2), King_keyhole_CALPHAD_hs=dh_c >= KING_THRESHOLD,
            dH_hs_if_sigma_is_radius=round(king(P, v, KING_T3["A"], KING_T3["D"], h_t3, d * 1e-6 / 2.0), 2),
            Ke=round(ke, 2), Ke_regime=next(n for b, n in KE_BANDS if ke < b), Ke_sheet=num("Ke"),
            ET_width_um=W, ET_depth_um=Dp,
            ET_depth_over_half_width=round(Dp / (W / 2.0), 3) if W and Dp else "",
        ))
    ratio = float(np.median([r["dH_hs_King_constants"] / r["Ke"] for r in rows]))
    ratio_c = float(np.median([r["dH_hs_CALPHAD_hs"] / r["Ke"] for r in rows]))
    return rows, dict(dH_hs_over_Ke_King_constants=round(ratio, 3), dH_hs_over_Ke_CALPHAD_hs=round(ratio_c, 3))


def write_outputs(res: dict, sets_path: Path, sheet_path: Path) -> dict:
    eqn = res["eq"]["nominal"]
    enth = eqn["enthalpy"]
    h_cal_kg = enth["to_solidus_sensible"]
    h_cal_vol = h_cal_kg * RHO_298
    rows, ratios = keyhole_table(h_cal_vol, sets_path, sheet_path)

    checks = []
    for P, v, d4s, quoted in KING_CHECKS:
        val = king(P, v, KING_T3["A"], KING_T3["D"], KING_T3["h_s_J_kg"] * KING_T3["rho"], d4s * 1e-6 / 4.0)
        alt = KING_T3["A"] * P / (math.pi * KING_T3["h_s_J_kg"] * KING_T3["rho"]
                                  * math.sqrt(KING_T3["D"] * v * 1e-3 * (d4s * 1e-6 / 2.0) ** 3))
        checks.append(dict(P_W=P, v_mm_s=v, D4sigma_um=d4s, quoted=quoted, eq_2_6_sigma_D4s_over_4=round(val, 1),
                           pi_outside_root_sigma_D4s_over_2=round(alt, 1)))
        assert abs(val / quoted - 1) < 0.03, (val, quoted)

    def kh(fl):
        return [r["set"] for r in rows if fl(r)]

    t_m = dict(T_liq=eqn["T_liq"], T_sol=eqn["T_sol"])
    summary = dict(
        what="pycalphad equilibrium and Scheil solidification of 316L, h_s for King et al.'s keyhole criterion, and "
             "dH/h_s for every wall set (calphad_316l.py; findings in calphad.md)",
        wall_sets=dict(file=str(sets_path.relative_to(HERE)) if sets_path.is_relative_to(HERE) else sets_path.name,
                       sha256=file_sha256(sets_path), n_sets=len(rows),
                       spot_um_range=[min(r["spot_um"] for r in rows), max(r["spot_um"] for r in rows)],
                       trace_spacing_mm_range=[min(r["trace_spacing_mm"] for r in rows),
                                               max(r["trace_spacing_mm"] for r in rows)]),
        database=dict(**DB, parsing_fixes=res["fixes"], elements=list(ELEMENTS),
                      phases_equilibrium=PH_ALL, phases_scheil=PH_SCHEIL,
                      left_out="BCC_B2 (needs MatCalc's ATTACH_CONTRIBUTION order-disorder link), BCC_DISL, gas; "
                               "P and S (not in the subset), O"),
        software=dict(pycalphad=__import__("pycalphad").__version__, numpy=np.__version__),
        compositions_wt_pct=COMPOSITIONS, composition_notes=dict(
            spec=SPEC_NOTE,
            nominal="middle of the 316L ranges (Cr 17, Ni 12, Mo 2.5), Mn 1.0, Si 0.5, C 0.02, N 0.05",
            corners="every element at the ferrite-promoting (high_ferrite) or austenite-promoting (low_ferrite) end of "
                    "the spec; floors C 0.005, N 0.01, Mn 0.1 wt% where the spec has only a cap",
            powder_certificate="none in the repo: lpbf-runs/m2-single-track-schedule.md lists the lot and certificate "
                               "as still to record; rerun with the certificate's composition when it arrives"),
        equilibrium={n: dict(T_liq_K=round(e["T_liq"], 2), T_sol_K=round(e["T_sol"], 2),
                             T_liq_C=round(e["T_liq"] - 273.15, 1), T_sol_C=round(e["T_sol"] - 273.15, 1),
                             freezing_range_K=round(e["T_liq"] - e["T_sol"], 1), primary_phase=e["primary"],
                             max_BCC_during_solidification=round(max(r["phases"].get("BCC_A2", 0.0) for r in e["rows"]
                                                                     if r["T"] >= e["T_sol"] - 0.5), 4),
                             BCC_just_below_solidus=round(next(r["phases"].get("BCC_A2", 0.0) for r in e["rows"]
                                                               if r["T"] < e["T_sol"]), 4),
                             phases_at_1000C={k: round(v, 4) for k, v in e["at_1000C"].items()},
                             wrc1992=e["wrc"])
                     for n, e in res["eq"].items()},
        scheil={k: scheil_summary(r, COMPOSITIONS[k.split("|")[0]]) for k, r in res["scheil"].items()},
        spec_sweep={var: [dict(t=round(s["t"], 2), wt=({k: round(v, 4) for k, v in s["wt"].items()}),
                               wrc_ratio=s["wrc"]["ratio"], wrc_mode=s["wrc"]["mode"], T_liq_K=round(s["T_liq"], 2),
                               T_sol_K=round(s["T_sol"], 2), primary_phase=s["primary"],
                               scheil3_ferrite_fraction=round(s["scheil_BCC"], 4), scheil3_mode=s["mode"],
                               scheil3_T_K_at_1pct_liquid=round(s["scheil_T_end"], 1))
                          for s in sorted(res["sweep"], key=lambda s: s["t"]) if s["variant"] == var]
                    for var in ("as_distributed", "no_fcc_si_ternaries")},
        spec_sweep_note="t = 0 is the low-ferrite corner, t = 1 the high-ferrite corner, linear in wt%. "
                        "no_fcc_si_ternaries: the database without L(FCC_A1,CR,FE,SI:VA;0) and "
                        "L(FCC_A1,FE,MO,SI:VA;0) (both 50000 - 80 T J/mol), a sensitivity check only",
        enthalpy=dict(
            note="J/kg from 298.15 K, metastable austenite (FCC_A1 at the alloy composition) for the solid and the "
                 "liquid at the alloy composition, nominal composition; per volume with rho = 7980 kg/m^3 (room "
                 "temperature, as King et al.'s Table 3)",
            rho_kg_m3=RHO_298, T_sol_K=round(eqn["T_sol"], 2), T_liq_K=round(eqn["T_liq"], 2),
            **{k: round(v, 1) for k, v in enth.items() if not k.startswith("grid")},
            per_volume_J_m3={k: float(f"{enth[k] * RHO_298:.4g}") for k in
                             ("to_solidus_sensible", "to_liquidus_sensible", "to_solidus_with_latent",
                              "to_liquidus_with_latent")},
            corners={n: {k: round(res["eq"][n]["enthalpy"][k], 1) for k in
                         ("to_solidus_sensible", "to_liquidus_with_latent", "latent_at_liquidus")}
                     for n in ("high_ferrite", "low_ferrite")},
            King_table3_h_s=dict(J_kg=KING_T3["h_s_J_kg"], J_m3=KING_T3["h_s_J_kg"] * KING_T3["rho"],
                                 definition="h_s = rho c T_m, the 'enthalpy at melting' (Sec. 2.1, PDF p. 7, and "
                                            "footnote 2), no latent heat; Table 3 (PDF p. 36) gives 1.2e6 J/kg, "
                                            "citing Rai et al. 2007"),
            repo_rho_c_T_m=dict(J_m3=REPO["rho"] * REPO["cp"] * REPO["T_liq"],
                                J_m3_from_298=REPO["rho"] * REPO["cp"] * (REPO["T_liq"] - T0)),
        ),
        keyhole=dict(
            formula="dH/h_s = A P / (h_s sqrt(pi D v sigma^3)), King et al. 2014 Eq. 2.6 (PDF p. 7)",
            sigma="Gaussian standard deviation, I = I0 exp(-r^2/(2 sigma^2)) (footnotes 1 and 4, PDF pp. 6, 10), "
                  "so sigma = D4sigma/4 with each set's spot as D4sigma; 32.5 um for the control's 130 um spot",
            check_against_paper=checks,
            King_constants=dict(**KING_T3, h_s_J_m3=KING_T3["h_s_J_kg"] * KING_T3["rho"]),
            CALPHAD_variant=dict(A=ABSORPTIVITY, D=D_REPO, h_s_J_kg=round(h_cal_kg, 1), h_s_J_m3=float(f"{h_cal_vol:.4g}"),
                                 note="A and D as eagar_tsai_316l.py; h_s = CALPHAD sensible enthalpy 298 K -> "
                                      "solidus (nominal) x 7980 kg/m^3"),
            thresholds=dict(
                experimental=f"{KING_THRESHOLD:g} +/- {KING_ERR:g} (Sec. 5.6, PDF p. 19; conclusion 4, PDF p. 20); "
                             f"transition from ~{KING_BAND[0]:g}, clearly keyhole above ~{KING_BAND[1]:g} "
                             "(Sec. 5.3, PDF p. 15)",
                theoretical="dH/h_s > pi T_b / T_m ~ 6 (Eq. 2.7, PDF p. 8), with T_b = 3273 K for steel (PDF p. 5)",
                theoretical_values={f"T_b {tb:g} K, T_m = {tm}": round(math.pi * tb / t_m[tm], 2)
                                    for tb in (T_BOIL, T_BOIL_KING) for tm in ("T_sol", "T_liq")},
                experimental_in_CALPHAD_hs_units=round(KING_THRESHOLD * (KING_T3["h_s_J_kg"] * KING_T3["rho"] / h_cal_vol)
                                                       * math.sqrt(KING_T3["D"] / D_REPO), 1),
                Ke_equivalent_of_26_30_34=[round(t / ratios["dH_hs_over_Ke_King_constants"], 2) for t in
                                           (KING_BAND[0], KING_THRESHOLD, KING_BAND[1])],
                Ke_equivalent_of_theoretical=round(math.pi * T_BOIL_KING / 1700.0
                                                   / ratios["dH_hs_over_Ke_King_constants"], 2),
            ),
            ratios=ratios,
            range_King_constants=[min(r["dH_hs_King_constants"] for r in rows),
                                  max(r["dH_hs_King_constants"] for r in rows)],
            range_if_sigma_is_radius=[min(r["dH_hs_if_sigma_is_radius"] for r in rows),
                                      max(r["dH_hs_if_sigma_is_radius"] for r in rows)],
            regime_counts_King_constants={k: sum(r["King_regime"] == k for r in rows)
                                          for k in ("conduction (<26)", "transition (26-34)", "keyhole (>=34)")},
            n_at_or_above_30_King_constants=sum(r["King_keyhole"] for r in rows),
            Ke_range=[min(r["Ke"] for r in rows), max(r["Ke"] for r in rows)],
            range_CALPHAD_hs=[min(r["dH_hs_CALPHAD_hs"] for r in rows), max(r["dH_hs_CALPHAD_hs"] for r in rows)],
            control=next(r for r in rows if r["set"].startswith("C_")),
            keyhole_sets_King_constants=kh(lambda r: r["King_keyhole"]),
            transition_or_keyhole_King_constants=kh(lambda r: r["dH_hs_King_constants"] >= KING_BAND[0]),
            keyhole_sets_CALPHAD_hs_at_30=kh(lambda r: r["King_keyhole_CALPHAD_hs"]),
            Ke_at_least_6=kh(lambda r: r["Ke"] >= 6.0),
            Ke_matches_sheet=all(abs(r["Ke"] - r["Ke_sheet"]) < 0.02 for r in rows if r["Ke_sheet"] != ""),
            ET_depth_over_half_width_max=max((r["ET_depth_over_half_width"] for r in rows
                                              if r["ET_depth_over_half_width"] != ""), default=None),
        ),
    )
    OUT.mkdir(exist_ok=True)
    (OUT / "calphad_316l_summary.json").write_text(json.dumps(summary, indent=1, default=float) + "\n")

    with open(OUT / "calphad_316l_keyhole.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    els = ("CR", "NI", "MO", "MN", "SI", "C", "N")
    fields = (["composition", "calc", "T_K", "T_C", "f_solid", "f_FCC", "f_BCC", "f_other", "other_phases"]
              + [f"liquid_wt_{e}" for e in els] + [f"austenite_wt_{e}" for e in els] + [f"ferrite_wt_{e}" for e in els])

    def wtd(xr):
        return to_wt({e: xr[e] for e in ELEMENTS}) if xr else {}

    out_rows = []
    for n, e in res["eq"].items():
        for r in e["rows"]:
            ph = r["phases"]
            other = {k: v for k, v in ph.items() if k not in ("LIQUID", "FCC_A1", "BCC_A2") and v > 1e-6}
            lw, aw, fw = wtd(r["X"].get("LIQUID")), wtd(r["X"].get("FCC_A1")), wtd(r["X"].get("BCC_A2"))
            out_rows.append(dict(composition=n, calc="equilibrium", T_K=round(r["T"], 2), T_C=round(r["T"] - 273.15, 2),
                                 f_solid=round(1 - ph.get("LIQUID", 0.0), 5), f_FCC=round(ph.get("FCC_A1", 0.0), 5),
                                 f_BCC=round(ph.get("BCC_A2", 0.0), 5), f_other=round(sum(other.values()), 6),
                                 other_phases=";".join(f"{k}={v:.2g}" for k, v in other.items()),
                                 **{f"liquid_wt_{x}": round(lw[x], 4) if lw else "" for x in els},
                                 **{f"austenite_wt_{x}": round(aw[x], 4) if aw else "" for x in els},
                                 **{f"ferrite_wt_{x}": round(fw[x], 4) if fw else "" for x in els}))
    for k, r in res["scheil"].items():
        n, model = k.split("|")
        for s in r["steps"]:
            cum = s["cum"]
            other = {a: b for a, b in cum.items() if a not in ("FCC_A1", "BCC_A2") and b > 1e-7}
            lw, aw, fw = wtd(s["x_liquid"]), wtd(s["x_solid"].get("FCC_A1")), wtd(s["x_solid"].get("BCC_A2"))
            out_rows.append(dict(composition=n, calc="scheil" if model == "classic" else "scheil_fast_CN",
                                 T_K=round(s["T"], 2), T_C=round(s["T"] - 273.15, 2), f_solid=round(s["f_solid"], 6),
                                 f_FCC=round(cum.get("FCC_A1", 0.0), 6), f_BCC=round(cum.get("BCC_A2", 0.0), 6),
                                 f_other=round(sum(other.values()), 7),
                                 other_phases=";".join(f"{a}={b:.2g}" for a, b in other.items()),
                                 **{f"liquid_wt_{x}": round(lw[x], 4) for x in els},
                                 **{f"austenite_wt_{x}": round(aw[x], 4) if aw else "" for x in els},
                                 **{f"ferrite_wt_{x}": round(fw[x], 4) if fw else "" for x in els}))
    with open(OUT / "calphad_316l_scheil.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)
    return summary


# --- figure ----------------------------------------------------------------------------------------------------------
INK, INK2, MUTED, SURFACE, GRIDC, NEUTRAL = "#0b0b0b", "#52514e", "#8a8984", "#fcfcfb", "#e1e0d9", "#f0efec"
SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100")      # categorical slots 1-4, fixed order


def figure(res: dict, summary: dict) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 9.5, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                         "legend.frameon": False})
    fig, axs = plt.subplots(2, 2, figsize=(12.5, 9.4), layout="constrained")
    (a, b), (c, d) = axs

    # (a) solid fraction vs T, nominal
    e = res["eq"]["nominal"]
    rows = [r for r in e["rows"] if r["T"] >= e["T_sol"] - 5]
    a.plot([r["T"] - 273.15 for r in rows], [1 - r["phases"].get("LIQUID", 0.0) for r in rows], color=SERIES[0], lw=2,
           label="equilibrium")
    for i, (key, lab) in enumerate((("nominal|classic", "Scheil"), ("nominal|fast_CN", "Scheil, C and N fast"))):
        st = res["scheil"][key]["steps"]
        a.plot([s["T"] - 273.15 for s in st], [s["f_solid"] for s in st], color=SERIES[i + 1], lw=2, label=lab)
    s_cl, s_fa = summary["scheil"]["nominal|classic"], summary["scheil"]["nominal|fast_CN"]
    for s, col in ((s_cl, SERIES[1]), (s_fa, SERIES[2])):
        a.plot(s["T_K_at_1pct_liquid"] - 273.15, 0.99, "o", ms=8, color=col, mec=SURFACE, mew=2, zorder=5)
    eqs = summary["equilibrium"]["nominal"]
    a.axvline(eqs["T_liq_C"], color=MUTED, lw=0.8, ls=":")
    a.axvline(eqs["T_sol_C"], color=MUTED, lw=0.8, ls=":")
    a.text(eqs["T_liq_C"] + 1, 0.04, f"liquidus\n{eqs['T_liq_C']:.0f} °C", color=INK2, fontsize=8.5)
    a.text(eqs["T_sol_C"] - 1, 0.04, f"solidus\n{eqs['T_sol_C']:.0f} °C", color=INK2, fontsize=8.5, ha="right")
    a.annotate(f"1% liquid left: {s_cl['T_K_at_1pct_liquid'] - 273.15:.0f} °C", (s_cl["T_K_at_1pct_liquid"] - 273.15, 0.99),
               (s_cl["T_K_at_1pct_liquid"] - 273.15 + 8, 0.83), color=INK2, fontsize=8.5,
               arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    a.annotate(f"{s_fa['T_K_at_1pct_liquid'] - 273.15:.0f} °C", (s_fa["T_K_at_1pct_liquid"] - 273.15, 0.99),
               (s_fa["T_K_at_1pct_liquid"] - 273.15 + 8, 0.7), color=INK2, fontsize=8.5,
               arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    a.set_xlim(s_cl["T_K_at_1pct_liquid"] - 273.15 - 15, eqs["T_liq_C"] + 12)
    a.set_ylim(0, 1.02)
    a.set_xlabel("Temperature (°C)")
    a.set_ylabel("Solid fraction (mole fraction of atoms)")
    a.set_title("(a) Mid-spec 316L: equilibrium and Scheil solidification", loc="left", fontsize=10, color=INK)
    a.legend(loc="center left")
    a.grid(color=GRIDC, lw=0.6)

    # (b) enrichment of the residual liquid and of the austenite forming, classic Scheil, nominal
    st = res["scheil"]["nominal|classic"]["steps"]
    w0 = COMPOSITIONS["nominal"]
    fs = np.array([s["f_solid"] for s in st])
    keep = fs <= 0.995
    for i, (el, name) in enumerate((("CR", "Cr"), ("NI", "Ni"), ("MO", "Mo"))):
        lw_ = np.array([to_wt({k: s["x_liquid"][k] for k in ELEMENTS})[el] for s in st]) / w0[el]
        b.plot(fs[keep], lw_[keep], color=SERIES[i], lw=2, label=f"{name}, residual liquid")
        aus = [(s["f_solid"], to_wt({k: s["x_solid"]["FCC_A1"][k] for k in ELEMENTS})[el] / w0[el]) for s in st
               if "FCC_A1" in s["x_solid"] and s["f_solid"] <= 0.995]
        b.plot(*zip(*aus), color=SERIES[i], lw=1.4, ls="--", label=f"{name}, austenite forming")
        b.text(fs[keep][-1] + 0.004, lw_[keep][-1], name, color=INK, fontsize=9, va="center")
    b.axhline(1, color=MUTED, lw=0.8)
    fdelta = s_cl["delta_ferrite_first_f_solid"]
    if fdelta:
        b.axvline(fdelta, color=MUTED, lw=0.8, ls=":")
        b.text(fdelta + 0.01, 0.62, f"δ-ferrite starts\nforming (f_s {fdelta:.2f})", ha="left", va="center",
               color=INK2, fontsize=8.5)
    b.set_xlim(0, 1.04)
    b.set_xlabel("Solid fraction")
    b.set_ylabel("Concentration / nominal (wt%)")
    b.set_title("(b) Scheil segregation, mid-spec 316L (classic)", loc="left", fontsize=10, color=INK)
    b.legend(loc="upper left", fontsize=8.5, ncols=1)
    b.grid(color=GRIDC, lw=0.6)

    # (c) the spec sweep: primary phase and Scheil ferrite vs WRC-1992 Creq/Nieq, both database variants
    for var, ls_, lab in (("as_distributed", "-", "mc_fe 2.062 as distributed"),
                          ("no_fcc_si_ternaries", "--", "without its two FCC Cr-Fe-Si, Fe-Mo-Si terms")):
        sw = summary["spec_sweep"][var]
        xr = [q["wrc_ratio"] for q in sw]
        yf = [100 * q["scheil3_ferrite_fraction"] for q in sw]
        c.plot(xr, yf, color=INK2, lw=1, ls=ls_, zorder=1, label=lab)
        for q, x_, y_ in zip(sw, xr, yf):
            prim_fcc = q["primary_phase"] == "FCC_A1"
            c.plot(x_, y_, "o" if prim_fcc else "s", ms=8, color=SERIES[0] if prim_fcc else SERIES[1], mec=SURFACE,
                   mew=2, zorder=3)
    for bnd, lab in ((1.25, "A | AF"), (1.48, "AF | FA"), (1.95, "FA | F")):
        c.axvline(bnd, color=MUTED, lw=0.8, ls=":")
        c.text(bnd, 101, lab, ha="center", va="bottom", color=INK2, fontsize=8.5)
    c.plot([], [], "o", ms=8, color=SERIES[0], label="primary austenite (FCC)")
    c.plot([], [], "s", ms=8, color=SERIES[1], label="primary δ-ferrite (BCC)")
    c.set_ylim(-3, 108)
    c.set_xlabel("WRC-1992 Creq/Nieq, along the spec from the low- to the high-ferrite corner")
    c.set_ylabel("Ferrite formed, 3-phase Scheil to 1% liquid (%)")
    c.set_title("(c) Primary phase within the 316L spec, against WRC-1992 modes", loc="left", fontsize=10, color=INK)
    c.legend(loc="upper left", bbox_to_anchor=(0.0, 0.93), fontsize=8.5)
    c.grid(color=GRIDC, lw=0.6)

    # (d) King et al.'s dH/h_s for every set against its spot size, King's own constants
    kt = list(csv.DictReader(open(OUT / "calphad_316l_keyhole.csv", newline="", encoding="utf-8")))
    d.axhspan(KING_BAND[0], KING_BAND[1], color=NEUTRAL, zorder=0)
    d.axhline(KING_THRESHOLD, color=INK, lw=1.2)
    d.text(198, KING_THRESHOLD * 1.03, "keyhole threshold 30 ± 4 (26–34 shaded)", color=INK, fontsize=8.5,
           va="bottom", ha="right")
    th = summary["keyhole"]["thresholds"]["theoretical_values"]
    t_lo, t_hi = min(th.values()), max(th.values())
    d.axhline(0.5 * (t_lo + t_hi), color=MUTED, lw=0.8, ls="--")
    d.text(51, 0.5 * (t_lo + t_hi) * 1.04, f"theory: π T_b/T_m ≈ {t_lo:.1f}–{t_hi:.1f}", color=INK2, fontsize=8.5,
           va="bottom")
    for r in kt:
        ctrl = r["set"].startswith("C_")
        col = SERIES[1] if r["King_keyhole"] == "True" else (SERIES[0] if r["King_regime"].startswith("conduction")
                                                              else SERIES[2])
        d.plot(float(r["spot_um"]), float(r["dH_hs_King_constants"]), "*" if ctrl else "o", ms=14 if ctrl else 7,
               color=col, mec=SURFACE, mew=1.5, zorder=4)
    for lab, col in (("conduction (< 26)", SERIES[0]), ("transition (26–34, below 30)", SERIES[2]),
                     ("keyhole (≥ 30)", SERIES[1])):
        d.plot([], [], "o", ms=7, color=col, label=lab)
    d.plot([], [], "*", ms=13, color=INK2, label="control, 370 W 1350 mm/s 130 µm")
    d.set_xscale("log")
    d.set_yscale("log")
    from matplotlib.ticker import FixedLocator, NullFormatter, NullLocator, ScalarFormatter

    d.xaxis.set_major_locator(FixedLocator([50, 70, 100, 130, 200]))
    d.yaxis.set_major_locator(FixedLocator([6, 10, 20, 30, 40, 60]))
    for ax_ in (d.xaxis, d.yaxis):
        ax_.set_major_formatter(ScalarFormatter())
        ax_.set_minor_formatter(NullFormatter())
        ax_.set_minor_locator(NullLocator())
    d.set_ylim(5, 70)
    d.set_xlabel("Spot size, 1/e² (D4σ) diameter (µm, log scale)")
    d.set_ylabel("dH/h_s (King et al.'s constants, log scale)")
    d.set_title(f"(d) King et al.'s normalized enthalpy for the {len(kt)} wall sets", loc="left", fontsize=10,
                color=INK)
    d.legend(loc="upper right", fontsize=8.5)
    d.grid(color=GRIDC, lw=0.6, which="both")
    eqs_hi, eqs_lo = summary["equilibrium"]["high_ferrite"], summary["equilibrium"]["low_ferrite"]
    fig.text(0.0, -0.045,
             f"pycalphad {summary['software']['pycalphad']} with MatCalc's open mc_fe 2.062 database (ODbL), Fe-Cr-Ni-Mo-"
             f"Mn-Si-C-N. Mid-spec 316L: Fe-17Cr-12Ni-2.5Mo-1Mn-0.5Si-0.02C-0.05N wt%. Equilibrium liquidus "
             f"{eqs['T_liq_C']:.0f} °C, solidus {eqs['T_sol_C']:.0f} °C; high-ferrite corner {eqs_hi['T_liq_C']:.0f}/"
             f"{eqs_hi['T_sol_C']:.0f} °C (primary {eqs_hi['primary_phase']}), low-ferrite corner "
             f"{eqs_lo['T_liq_C']:.0f}/{eqs_lo['T_sol_C']:.0f} °C (primary {eqs_lo['primary_phase']}).\n"
             "(c): 3-phase (liquid, FCC, BCC) Scheil to 1% liquid. (d): dH/h_s = A P / (h_s √(π D v σ³)), σ = D4σ/4 "
             "of each set's spot, A 0.4, h_s 1.2 MJ/kg × 7980 kg/m³, D 5.38e-6 m²/s (King et al., J. Mater. Process. "
             "Technol. 214, 2915 (2014), Eq. 2.6, Table 3); keyhole at 30 ± 4.",
             fontsize=8, color=INK2, ha="left", va="top")
    fig.savefig(OUT / "m2-calphad-316l.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main(argv: list[str]) -> None:
    fresh = "fresh" in argv
    opt = {a: Path(argv[i + 1]).resolve() for i, a in enumerate(argv[:-1]) if a in ("--sets", "--sheet")}
    sets_path = opt.get("--sets", OUT / "wall_sets.csv")
    sheet_path = opt.get("--sheet", OUT / "wall_sheet.csv" if "--sets" not in opt else Path("/nonexistent"))
    t0 = time.time()
    res = compute(fresh=fresh)
    summary = write_outputs(res, sets_path, sheet_path)
    figure(res, summary)
    eq = summary["equilibrium"]
    for n, e in eq.items():
        print(f"{n:13s} WRC {e['wrc1992']['ratio']:.2f} ({e['wrc1992']['mode']}): T_liq {e['T_liq_C']:.1f} C, "
              f"T_sol {e['T_sol_C']:.1f} C, range {e['freezing_range_K']:.1f} K, primary {e['primary_phase']}")
    for k, s in summary["scheil"].items():
        print(f"{k:24s} 1% liquid at {s['T_K_at_1pct_liquid'] - 273.15:.0f} C, ferrite "
              f"{s['phase_fractions_at_1pct_liquid'].get('BCC_A2', 0):.3f}")
    kh = summary["keyhole"]
    print(f"dH/h_s (King constants) {kh['range_King_constants']}, keyhole: {kh['keyhole_sets_King_constants']}")
    print(f"done in {time.time() - t0:.0f} s -> {OUT}")


if __name__ == "__main__":
    main(sys.argv[1:])
