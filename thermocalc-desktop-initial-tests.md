# Initial Thermo-Calc / TC-Python Tests on the BYU Desktop Machine

**Audience:** @XZaitzeff (BYU Thermo-Calc desktop machine, byu-vcl
[#122](https://github.com/vertical-cloud-lab/byu-vcl/issues/122);
HPC access tracked in [#123](https://github.com/vertical-cloud-lab/byu-vcl/issues/123))

**Goal:** A short, ordered set of tests that (a) confirm the install/license work,
and (b) generate the *specific* CALPHAD artifacts that matter for the FLAIME
Genesis Mission proposal (Topic 3B, AMMTO critical minerals — PR
[#58](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/58),
`consolidation-2` branch).

**What we have on this machine:** Thermo-Calc + **TC-Python** + an **Al alloy
database** (most likely **TCAL8** per BYU's current license — Test 0 confirms the
exact name/version) + the **Precipitation (TC-PRISMA)** module.

**What we do NOT have yet:** the **AM Module**. Steps that require it are flagged
and deferred — Thermo-Calc is providing those simulations directly as preliminary
results, and we are separately pursuing a TCAl10 + AM Module quote. Do **not** try
to run melt-pool / printability-map calculations here.

**Why these tests (proposal alignment):** The proposal screens **Al-Zr** and
**Al-Mn-Cr-Zr** alloy families against **Scalmalloy** and **AlSi10Mg** baselines,
under a **mineral-burden** objective, with CALPHAD acting as cheap
partial-evaluation nodes (TC-Python/TCAl + Scheil + TC-PRISMA) feeding the
pKGFN/BOFN loop. The tests below produce exactly those node outputs
(equilibrium phase fractions, Scheil solidification + freezing range, and Al₃Zr
precipitation kinetics) plus a database-adequacy assessment that tells us whether
**TCAL8 is sufficient or whether the TCAl10 upgrade is required** for the
quaternary Al-Zr-Mn-Cr space.

> Element palette (proposal single source of truth):
> `Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn` (Al base).
> The primary families use **Zr, Mn, Cr** (+ Al); baselines add **Si, Mg** (AlSi10Mg)
> and **Mg, Sc, Zr** (Scalmalloy).

---

## Setup (once)

1. Confirm TC-Python is importable from the same Python you'll use for the proposal
   work (a dedicated conda/venv is cleanest):

   ```bash
   python -c "import tc_python; print('TC-Python OK')"
   ```

   If this fails, (re)install the TC-Python wheel that ships with the Thermo-Calc
   installation (`.../SDK/TC-Python/`), following the
   [TC-Python install guide](https://thermocalc.com/products/software-development-kits/tc-python/).

2. Keep every script's output (CSV + PNG) in a dated folder so results can be
   committed back here as preliminary data. Each script below writes a CSV (and,
   where useful, a plot via `matplotlib`).

> All scripts use `with TCPython() as session:` so the license is checked out and
> released cleanly. Run them one at a time first (don't parallelize on the desktop —
> the desktop license is a single seat; HPC scale-out is a separate effort, #123).

---

## Test 0 — Environment, license, and database inventory (5 min)

**Purpose:** Confirm the license checks out and find the *exact* Al database name
that is actually installed (we currently aren't sure — TCAL8 vs TCAL10, etc.).

```python
"""Test 0: license + database inventory."""
from tc_python import *

with TCPython() as session:
    dbs = session.get_databases()           # list of installed database short names
    print("Installed databases:")
    for d in sorted(dbs):
        print("  ", d)

    # Pick the Al database (TCAL*) for later tests and confirm elements.
    al_dbs = [d for d in dbs if d.upper().startswith("TCAL")]
    print("\nAl alloy database(s) found:", al_dbs)
```

**Record:** the full database list and the exact `TCAL*` name/version. Paste it
into #122. This resolves the "I forget which one" question and tells us whether we
already have the elements we need (next test) or need the **TCAl10** upgrade.

---

## Test 1 — Single equilibrium sanity check on AlSi10Mg baseline (5 min)

**Purpose:** Smallest end-to-end equilibrium. Reproduces a known baseline so we can
sanity-check against literature/the existing AlSi10Mg preliminary data.

```python
"""Test 1: single equilibrium, AlSi10Mg at 300 C (wt%: Si 10, Mg 0.4, bal Al)."""
from tc_python import *

DB = "TCAL8"  # <-- replace with the exact name from Test 0

with TCPython() as session:
    calc = (
        session
        .select_database_and_elements(DB, ["Al", "Si", "Mg"])
        .get_system()
        .with_single_equilibrium_calculation()
        .set_condition("W(Si)", 0.10)
        .set_condition("W(Mg)", 0.004)
        .set_condition(ThermodynamicQuantity.temperature(), 573.15)  # 300 C
        .set_condition(ThermodynamicQuantity.pressure(), 1e5)
    )
    result = calc.calculate()
    phases = result.get_stable_phases()
    print("Stable phases at 300 C:", phases)
    for ph in phases:
        f = result.get_value_of(f"NP({ph})")   # moles of phase
        print(f"  {ph}: NP = {f:.4f}")
```

**Expect:** FCC_A1 (Al matrix) + a Si-rich phase (DIAMOND_A4 / Si) and a small
Mg-bearing phase. If the phase names look reasonable, the database is wired up
correctly.

---

## Test 2 — Scheil solidification: Al-Zr peritectic vs. AlSi10Mg eutectic (20 min) ⭐

**Purpose:** This is the **highest-value** early test. The proposal's Stage-2
CALPHAD node is **Scheil**, and the Al-Zr family solidifies **peritectically**
(very different from the Al-Si **eutectic** of AlSi10Mg). Scheil gives us the
**freezing range** and terminal-phase sequence that feed the crack-susceptibility /
printability reasoning *without* the AM Module.

Run Scheil for three compositions and compare freezing ranges:

```python
"""Test 2: Scheil solidification, freezing range comparison."""
from tc_python import *
import csv

DB = "TCAL8"  # <-- from Test 0

# (label, elements, weight-fraction conditions)
CASES = [
    ("AlSi10Mg",  ["Al", "Si", "Mg"], {"Si": 0.10, "Mg": 0.004}),
    ("Al-0.5Zr",  ["Al", "Zr"],       {"Zr": 0.005}),
    ("Al-1.0Zr",  ["Al", "Zr"],       {"Zr": 0.010}),
]

with TCPython() as session, open("scheil_freezing_ranges.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["alloy", "T_liquidus_C", "T_solidus_C", "freezing_range_C"])
    for label, elems, conds in CASES:
        calc = session.select_database_and_elements(DB, elems).get_system() \
            .with_scheil_calculation()
        for el, w in conds.items():
            calc = calc.set_composition_unit(CompositionUnit.MASS_FRACTION) \
                       .set_composition(el, w)
        scheil = calc.calculate()
        # Temperature vs. fraction-solid curve for the liquid:
        T, fs = scheil.get_values_grouped_by_quantity_of(
            ScheilQuantity.mole_fraction_of_all_solid_phases(),
            ScheilQuantity.temperature(),
        ).get_lines()[0].get_x(), None
        # Liquidus = first T, solidus ~= last T where solid fraction ~1:
        temps = scheil.get_values_of(ScheilQuantity.temperature())
        T_liq = max(temps) - 273.15
        T_sol = min(temps) - 273.15
        writer.writerow([label, f"{T_liq:.1f}", f"{T_sol:.1f}", f"{T_liq - T_sol:.1f}"])
        print(f"{label}: liquidus {T_liq:.1f} C, solidus {T_sol:.1f} C, "
              f"range {T_liq - T_sol:.1f} C")
```

> API note: the exact Scheil getter names vary slightly by TC-Python version. If
> `get_values_grouped_by_quantity_of` differs in your version, use
> `scheil.get_values_of(ScheilQuantity.temperature())` and
> `ScheilQuantity.mole_fraction_of_a_solid_phase("*")` and inspect with
> `dir(ScheilQuantity)`. The deliverable is the **liquidus, solidus, and freezing
> range** per alloy, plus the terminal solid phases.

**Deliverable:** `scheil_freezing_ranges.csv` + (optional) overlaid T-vs-fraction-solid
plots. A **wider** freezing range / long low-temperature tail flags higher hot-cracking
risk — directly relevant to the proposal's printability gating. This is the data that
maps to the proposal's "Scheil solidification curves comparing Al-Zr peritectic vs
Al-Si eutectic" figure.

---

## Test 3 — Equilibrium phase fraction vs. temperature (Al₃Zr former check) (15 min)

**Purpose:** Confirm the database actually predicts the **L1₂-Al₃Zr** (or D0₂₃)
strengthening phase that is the *entire basis* for Al-Zr strengthening in AM. If
TCAL8 cannot resolve Al₃Zr discrimination, that's strong evidence we need TCAl10.

```python
"""Test 3: equilibrium phase amount vs T for Al-1Zr (step calculation)."""
from tc_python import *
import csv

DB = "TCAL8"  # <-- from Test 0

with TCPython() as session, open("alzr_phase_vs_T.csv", "w", newline="") as f:
    calc = (
        session
        .select_database_and_elements(DB, ["Al", "Zr"]).get_system()
        .with_property_diagram_calculation()
        .with_axis(CalculationAxis(ThermodynamicQuantity.temperature())
                   .set_min(573.15).set_max(933.15).with_axis_type(Linear().set_max_step_size(2.0)))
        .set_condition("W(Zr)", 0.01)
        .set_condition(ThermodynamicQuantity.pressure(), 1e5)
    )
    result = calc.calculate()
    groups = result.get_values_grouped_by_stable_phases_of(
        ThermodynamicQuantity.temperature(),
        ThermodynamicQuantity.volume_fraction_of_a_phase("ALL_PHASES"),
    )
    writer = csv.writer(f)
    writer.writerow(["phase", "T_K", "volume_fraction"])
    for label, group in groups.items():
        for x, y in zip(group.get_x(), group.get_y()):
            writer.writerow([label, f"{x:.2f}", f"{y:.5f}"])
    print("Phases observed:", list(groups.keys()))
```

**Check:** Do an Al₃Zr-type phase (e.g. `AL3ZR`, `ALZR3_L12`, or `D023`) appear?
Note the solvus temperature (where it dissolves). Record the exact phase label —
we need it for the precipitation model in Test 4 and for the proposal's phase
discrimination claims.

---

## Test 4 — TC-PRISMA precipitation kinetics for Al₃Zr (30 min) ⭐

**Purpose:** PRISMA is on this license, and Al₃Zr precipitation during a post-print
age is what gives Al-Zr its strength. A precipitate radius / number-density /
volume-fraction-vs-time curve at a realistic aging temperature is a compelling,
*generatable-now* preliminary result that needs **no AM Module**.

```python
"""Test 4: TC-PRISMA isothermal precipitation of Al3Zr in Al-1Zr at 375 C."""
from tc_python import *
import csv

THERMO_DB = "TCAL8"     # <-- from Test 0
MOB_DB    = "MOBAL"     # mobility database; confirm exact name in Test 0 list

MATRIX = "FCC_A1"
PRECIP = "AL3ZR"        # <-- use the exact Al3Zr/L1_2 phase label from Test 3

with TCPython() as session, open("alzr_prisma.csv", "w", newline="") as f:
    calc = (
        session
        .select_thermodynamic_and_kinetic_databases_with_elements(
            THERMO_DB, MOB_DB, ["Al", "Zr"])
        .get_system()
        .with_isothermal_precipitation_calculation()
        .set_composition_unit(CompositionUnit.MASS_PERCENT)
        .set_composition("Zr", 1.0)
        .set_temperature(648.15)        # 375 C aging
        .set_simulation_time(3600 * 8)  # 8 h
        .with_matrix_phase(
            MatrixPhase(MATRIX).add_precipitate_phase(PrecipitatePhase(PRECIP)))
    )
    result = calc.calculate()
    time_s, mean_r = result.get_mean_radius_of(PRECIP)
    _, vol_frac    = result.get_volume_fraction_of(PRECIP)
    _, num_den     = result.get_number_density_of(PRECIP)

    writer = csv.writer(f)
    writer.writerow(["time_s", "mean_radius_m", "volume_fraction", "number_density_m-3"])
    for t, r, v, n in zip(time_s, mean_r, vol_frac, num_den):
        writer.writerow([f"{t:.1f}", f"{r:.4e}", f"{v:.5e}", f"{n:.4e}"])
    print(f"Final: r={mean_r[-1]:.3e} m, Vf={vol_frac[-1]:.3e}, "
          f"N={num_den[-1]:.3e} /m^3")
```

**Deliverable:** `alzr_prisma.csv` + radius/Vf-vs-time plot. Needs the **mobility
database** (`MOBAL`/`MOBAL*`) — confirm it's in the Test 0 list. If no mobility
database is licensed, note that as a gap (PRISMA needs both thermodynamic and
mobility data).

---

## Test 5 — Small batch equilibrium screen (Al-Mn-Cr-Zr) + database-adequacy probe (20 min)

**Purpose:** A tiny version of the proposal's Stage-1/2 screening node, *and* the
decisive **TCAL8-vs-TCAl10** test: does the database even accept the **quaternary
Al-Zr-Mn-Cr** system and return sensible phases?

```python
"""Test 5: small Al-Mn-Cr-Zr batch equilibrium screen at 400 C."""
from tc_python import *
import numpy as np, csv

DB = "TCAL8"  # <-- from Test 0
ELEMENTS = ["Al", "Mn", "Cr", "Zr"]   # quaternary — this is the database stress test

with TCPython() as session:
    try:
        system = session.select_database_and_elements(DB, ELEMENTS).get_system()
    except Exception as e:
        print("DATABASE GAP: cannot build Al-Mn-Cr-Zr system with", DB, "->", e)
        print("This indicates the TCAl10 upgrade is required for quaternary work.")
        raise SystemExit

    batch = system.with_batch_equilibrium_calculation()
    grid, cid = [], 0
    for mn in (0.005, 0.01, 0.02):
        for cr in (0.005, 0.01):
            for zr in (0.005, 0.01):
                batch.set_condition_for_calculation(cid, ThermodynamicQuantity.temperature(), 673.15)
                batch.set_condition_for_calculation(cid, "W(Mn)", mn)
                batch.set_condition_for_calculation(cid, "W(Cr)", cr)
                batch.set_condition_for_calculation(cid, "W(Zr)", zr)
                grid.append((cid, mn, cr, zr)); cid += 1

    print(f"Running {cid} quaternary equilibria...")
    res = batch.calculate()
    with open("almncrzr_screen.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["id", "Mn", "Cr", "Zr", "stable_phases"])
        for cid, mn, cr, zr in grid:
            try:
                phases = res.get_stable_phases(cid)
                w.writerow([cid, mn, cr, zr, ";".join(phases)])
            except Exception as e:
                w.writerow([cid, mn, cr, zr, f"error: {e}"])
    print("Saved almncrzr_screen.csv")
```

**Deliverable + verdict:** `almncrzr_screen.csv`. Watch for whether the expected
detrimental intermetallics (e.g. `AL6MN`, `AL13CR2`) and the desired `AL3ZR` all
appear with sensible amounts. If the database errors out on the quaternary, or
returns clearly wrong/missing phases, that is the empirical justification for the
**TCAl10** upgrade called out in the proposal budget.

---

## What the BO campaign actually consumes: numeric outputs → pKGFN/BOFN inputs

*(For a materials-science audience without deep Thermo-Calc/thermodynamic-modeling
background.)* The Bayesian optimization framework in proposal #58 (pKGFN over a
function network) doesn't consume phase diagrams or pretty plots — it consumes
**scalar numbers per candidate composition**, each attached to a node in the DAG
with a known evaluation cost. CALPHAD's role is to be the *cheap, fast node*: for
any composition the BO proposes, these simulations return numbers in seconds-to-minutes
that either (a) filter the candidate out before any powder is made, or (b) become
structured inputs that the downstream GP surrogates (atomization → print → tensile)
condition on. Concretely, the tests above produce:

| # | Numeric output | From | Intuition (mat sci terms) | Role in the BO campaign |
|---|---|---|---|---|
| 1 | **Equilibrium phase fractions** `NP(phase)` / `VPV(phase)` at a given T (e.g., vol. frac. of FCC_A1 matrix, Al₃Zr, Al₆Mn, Al₁₃Cr₂) | Tests 1, 3, 5 | "How much of each phase exists at this temperature" — like reading a lever-rule answer off a phase diagram, but for any multicomponent composition | **Feasibility filter + strength proxy.** Vol. frac. of L1₂-Al₃Zr is the strengthening-potential proxy (more = stronger, up to coarsening limits); vol. frac. of brittle intermetallics (Al₆Mn, Al₁₃Cr₂) above a threshold ⇒ reject before spending \$300+ on atomization. Feeds the CALPHAD partial-evaluation node (Node 1) as a vector input to the downstream GPs. |
| 2 | **Liquidus temperature** T_liq (°C) | Test 2 (Scheil) | Temperature where the alloy starts to solidify | Sets required melt superheat for atomization; a structured input to the atomization-node GP (predicts powder yield/sphericity). |
| 3 | **Solidus / terminal solidification temperature** T_sol (°C) | Test 2 | Temperature where the last liquid disappears | With T_liq gives the freezing range (next row). |
| 4 | **Freezing range** ΔT = T_liq − T_sol (°C) | Test 2 | Wide range = lots of mushy zone = hot-tearing risk during LPBF | **Printability scalar.** Directly correlates with hot-cracking susceptibility; used as a constraint (e.g., ΔT below threshold) or as an input feature to the print-node GP. Cheapest available crack-risk signal without the AM Module. |
| 5 | **Fraction-solid vs. temperature curve → crack-susceptibility index (CSI)**, e.g. Kou's criterion \|dT/d(f_s^{1/2})\| near f_s ≈ 1, or the T(f_s=0.9)→T(f_s=0.99) interval | Test 2 | Steep terminal solidification = thin liquid films persisting between grains = cracking | A single scalar per composition that ranks hot-cracking risk; this is the Stage-2 screening criterion in the proposal funnel and a printability gate before the AM Module / physical print nodes. |
| 6 | **Al₃Zr solvus temperature** (°C) | Test 3 | Temperature above which the strengthening phase dissolves | Defines the usable heat-treatment/service window; can serve as a thermal-stability objective or constraint (target alloys keep strengthening phase stable at elevated T — key for the high-T tensile story). |
| 7 | **Precipitate mean radius r(t), volume fraction V_f(t), number density N(t)** at aging T | Test 4 (TC-PRISMA) | How fast and how fine the Al₃Zr dispersoids form during post-print aging | r and N at end-of-age feed an Orowan-type **yield-strength estimate** Δσ ∝ V_f^{1/2}/r — a quantitative pre-experiment strength prediction that the tensile-node GP can be conditioned on, sharpening the prior before any specimen is pulled. |
| 8 | **Driving force for nucleation** ΔG_m (J/mol) of Al₃Zr at aging T | Test 4 (or single-equilibrium `DGM(phase)`) | "Thermodynamic push" for the precipitate to form | Fast proxy for precipitation propensity when full PRISMA kinetics are too slow for 100K-point screening. |
| 9 | **Per-calculation success/failure + phase-set sanity** across the quaternary grid | Test 5 | Does the database even handle Al-Zr-Mn-Cr together | Determines the **trust region** of the CALPHAD node (where its outputs are reliable enough to feed the GPs) and settles the TCAL8-vs-TCAl10 budget question. |
| 10 | **Mineral-burden score** MB = Σᵢ wᵢ·xᵢ (computed from composition + USGS weights, no Thermo-Calc needed — but evaluated on the same grid) | alongside Tests 3/5 | Supply-risk-weighted composition penalty | The Topic 3B objective itself; analytical and noise-free, so it enters the BOFN as an exact (non-GP) node combined with the CALPHAD-derived feasibility/strength scalars. |

**How they plug in, in one paragraph:** for each composition the pKGFN acquisition
proposes, the CALPHAD node returns the vector
(V_f^{Al₃Zr}, V_f^{intermetallics}, T_liq, ΔT, CSI, solvus, Δσ_est) in ~1–5 CPU-min.
Hard constraints (intermetallic fraction, ΔT/CSI thresholds) prune candidates at
near-zero cost; the surviving scalars become inputs the downstream GP surrogates
(atomization, LPBF, tensile) condition on, so the network "knows" a lot about a
candidate before any expensive physical evaluation. That's the entire reason
CALPHAD is a node in the DAG rather than a side study: every number above shrinks
posterior uncertainty at the expensive nodes per dollar spent.

### These outputs are element-agnostic — they cover the full 16-element palette

The Al₃Zr / Al₆Mn / Al₁₃Cr₂ phase names above are **concrete examples for the
Phase-I primary families**, not the limit of what CALPHAD provides. The numeric
*quantities* (rows 1–10) are computed identically for **any** composition the BO
proposes across the full **16-element palette** (Al base + 15 additions:
Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn). Thermo-Calc returns
the stable phase set and its properties for whatever elements are present — the
node doesn't need to be told in advance which strengthening or detrimental phase
to expect. The BO consumes the outputs as **abstract, element-independent features**:

| Abstract feature fed to the BO | Concrete instances across the palette |
|---|---|
| **Strengthening-phase volume fraction** (coherent/ordered precipitate former) | L1₂-Al₃Zr / D0₂₃-Al₃Zr (**Zr**); L1₂-Al₃Sc and Al₃(Sc,Zr) (**Sc**, baseline); Al₃(Er,Zr) (**Er**); θ′-Al₂Cu (**Cu**); β″/β′-Mg₂Si (**Mg+Si**); Al₃(Li) δ′ (**Li**) |
| **Detrimental / brittle-intermetallic volume fraction** (rejection filter) | Al₆Mn, Al₁₃Cr₂ (**Mn, Cr**); primary Si (**Si**); Al₃Ti (**Ti**); Al₃Fe / Al₁₃Fe₄, AlₓFeₓSi (**Fe**); Al₃Ni (**Ni**); Al-Ce intermetallics (**Ce**) |
| **Liquidus / solidus / freezing range / CSI** | Computed from the multicomponent Scheil path — **fully general**, no per-element assumption (this is why Test 2 is the most broadly reusable) |
| **Solvus of the strengthening phase** | Any of the above precipitate formers (sets the thermal-stability / high-T-tensile window for that composition) |
| **Precipitate r/V_f/N → Orowan Δσ** | Any matrix+precipitate pair PRISMA can model with the licensed mobility data (e.g. Al₃Zr, Al₃Sc, Al₂Cu, Mg₂Si) |
| **Mineral-burden MB = Σᵢ wᵢ·xᵢ** | Spans the entire palette by construction — wᵢ is defined for all 15 additions, penalizing Sc/REE(Ce,Er)/Mg and rewarding Mn/Cr/Fe/Si |

So the apparent "subset" framing reflects only where Phase-I screening is
**focused** (Al-Zr and Al-Mn-Cr-Zr, ~80%), not a limitation of the simulation
outputs. Tests 2 (Scheil freezing range/CSI) and the mineral-burden score are
already palette-wide today; Tests 1/3/5 generalize to any element subset simply by
changing the element list passed to `select_database_and_elements(...)` — the
**only** real constraint is database coverage. This is exactly the TCAL8-vs-TCAl10
question: a given Al database assesses a specific element set, so the practical
limit on "which of the 16 elements can the CALPHAD node score reliably" is set by
the database, not by the BO or the output types. (Cu-Cr-Zr for the ~20% Be-Cu
replacement complement, and the Sc/Mg/Si baselines, are all inside this same
machinery.)

---

## What to report back

Post a short summary to #122 (and #123 for the HPC angle) with:

1. **Database inventory** from Test 0 — exact `TCAL*` name + whether a mobility
   database (`MOBAL*`) is present.
2. **Pass/fail** for each test (did it run, did the phases look sane).
3. The **CSV/PNG artifacts** from Tests 2–5 — these are committable preliminary
   CALPHAD results for the proposal (Scheil freezing ranges, Al₃Zr phase fractions
   and precipitation curves, quaternary screen).
4. A one-line **TCAL8-vs-TCAl10 verdict** based on Tests 3 and 5: did the installed
   database resolve Al₃Zr discrimination and accept the Al-Zr-Mn-Cr quaternary, or
   do we need the upgrade?

## Out of scope on this machine (for now)

- **AM Module** (melt-pool, process maps, printability) — not licensed here;
  Thermo-Calc is supplying these as preliminary results. Don't attempt them.
- **HPC / parallel scale-out** — the desktop is a single license seat. Multi-job
  HPC runs are tracked separately in
  [#123](https://github.com/vertical-cloud-lab/byu-vcl/issues/123); see
  `high-throughput-calphad.md` (TC-Python 32-logical-processor cap, SLURM patterns)
  before scaling out.
