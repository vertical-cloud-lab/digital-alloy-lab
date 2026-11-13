"""Submit 4 Edison LITERATURE_HIGH queries — one per composition — asking
for recommended AM Module / LPBF scan parameters and a printability-map
grid sweep plan.

Compositions (to be sent to Thermo-Calc / Thermo-Calc's account manager for steady-state AM
Module sims, and also used to plan BYU / Aconity MIDI test prints):

  1. AlSi10Mg           — Si 10.0, Mg 0.325, bal. Al (wt%)
  2. BYU blend          — Al 75.56, Si 24.30, Mg 0.14 (wt%)
  3. Mehta "Alloy C"    — Al-5.0Mn-0.8Cr-0.5Zr (wt%)
  4. Al-1.5Zr (Glerum)  — Al-1.5Zr (wt%), supersaturated LPBF

One task per composition so each response is tightly focused. Does NOT
wait for completion; prints task IDs to stdout and writes them to
/tmp/edison_scanparams_task_ids.json for next-session fetch.
"""
import json
import os
import sys
import pathlib

from edison_client import EdisonClient, JobNames
from edison_client.models import TaskRequest, RuntimeConfig


REPO = pathlib.Path("/workspaces/digital-alloy-lab-private")
api_key = os.environ["EDISON_API_KEY"]
client = EdisonClient(api_key=api_key)


# Reference material — same set across all four queries. Keeps answers
# FLAIME-contextualized (BOFN/Aconity MIDI/AMAZEMET pipeline) rather than
# generic LPBF literature.
UPLOAD_CANDIDATES = [
    REPO / "genesis-mission-proposal" / "flaime-genesis-proposal-clean.pdf",
    REPO / "edison-trajectories" / "thermocalc_3b_calphad_strategy_full.md",
    REPO / "edison-trajectories" / "am-scaleup-test-structures.md",
    REPO / "edison-trajectories" / "pareto-am-al-alloys" / "pareto_front_analysis.md",
    REPO / "edison-trajectories" / "llm-warmstart-compositions.md",
    REPO / "thermocalc-discussion-transcript.md",
]
UPLOADS = [p for p in UPLOAD_CANDIDATES if p.exists()]
missing = [p for p in UPLOAD_CANDIDATES if not p.exists()]
for p in missing:
    print(f"  WARN: missing upload (skipping): {p}", file=sys.stderr)

print("Uploading reference files...", file=sys.stderr)
data_uris = []
for p in UPLOADS:
    ref = client.upload_file(str(p))
    print(f"  {p.name} -> {ref}", file=sys.stderr)
    data_uris.append(ref)


# ---- Shared preamble: parameter menu available in the AM Module + the
# kind of answer we want back ----------------------------------------------
SHARED_PREAMBLE = r"""
# Task

Recommend **LPBF (laser powder-bed fusion) scan parameters** and a
**printability-map grid-search plan** for the single composition
identified below, suitable for:

  (a) a Thermo-Calc AM Module *steady-state* calculation
      (Thermo-Calc's account manager will run this for us at Thermo-Calc Software AB as a
      preliminary deliverable for the FLAIME DOE Genesis Mission
      proposal, DE-FOA-0003612, Topic 3-B); and
  (b) a matching physical LPBF test print on a BYU / validation-partner
      **Aconity MIDI** system (representative of the fleet FLAIME will
      drive in closed-loop mode).

## Available AM Module parameter menu (please pick values from these)

The AM Module's *Conditions* tab exposes the following fields.  The
values in parentheses are the Thermo-Calc defaults; deviating from
them is discouraged unless the literature for this specific composition
clearly motivates a different starting point.

* **Global**: gas pressure (1e5 Pa), base-plate temperature (30 °C; may
  increase to 150–200 °C for Al alloys if literature supports), ambient
  temperature (23 °C), fluid-flow / Marangoni on (default), separate
  powder density 80% of solid (default).
* **Geometry**: height 2.0 mm, mesh Coarse (default).
* **Heat source type**: Gaussian (default), Core-ring, Top-hat,
  Electron Beam, Double ellipsoidal, Conical.  Pick Gaussian unless
  the composition or Aconity MIDI ring-mode capability clearly
  motivates Core-ring.
* **Heat source parameters**: power (default 200 W; Aconity MIDI range
  roughly 50–400 W), absorptivity mode = *Calculated* with prefactor
  1.0 (default — calibrated against AlSi10Mg), laser wavelength
  (default 1064 nm — near-IR fiber laser, matches Aconity MIDI), beam
  radius (default 40 µm, Aconity MIDI typical 40–80 µm), keyhole model
  on (default), beam-quality factor M² (default 1.0).
* **Scanning strategy**: scanning speed (default 1000 mm/s, Aconity
  MIDI range roughly 100–3000 mm/s), layer thickness (default 40 µm;
  Al-alloy LPBF commonly 30 µm).
* **Top boundary**: radiation emissivity (default 0.8), convective HTC
  (default 20 W/m²/K), evaporation on (default).
* **Calculation Type**: Single Point, Heat-Source Calibration, Batch,
  or **Grid** — we will use Grid to produce a P–v printability map.

## What to return

A single structured response with these sections:

1. **Single-point reference parameters** — one recommended starting
   point for a steady-state Single-Point AM Module run.  Give a value
   for every field in the menu above; *explicitly note which values
   you are leaving at Thermo-Calc's default vs.\ changing, and justify
   each deviation from default* with 1–2 literature citations
   (DOI/reference) tied to this specific composition (or the closest
   published analogue).
2. **Grid-search plan for a P–v printability map** — recommended
   sweep bounds for *laser power* and *scan speed* (the two axes
   conventionally used for LPBF printability maps) plus recommended
   grid resolution (n × m), rationalised against expected melt-pool
   depth vs.\ layer thickness and hatch spacing.  State which hatch
   spacing and layer-thickness values to hold constant during the
   sweep.  If a third parameter (e.g.\ beam radius, preheat) would
   meaningfully shift the window for this composition, say so but do
   not add it to the main grid.
3. **Expected LPBF windows / regimes** — a brief textual prediction
   of where lack-of-fusion, conduction-mode, transition, and keyhole
   regimes are expected to land on that P–v grid for this composition,
   and which regions are most informative for the FLAIME BOFN
   surrogate.
4. **Composition-specific flags** — any peculiarities of *this*
   composition that Thermo-Calc's account manager (or a downstream BYU operator) should be
   warned about before running.  In particular:
     * absorptivity behaviour relative to AlSi10Mg (oxide-skin effects,
       resistivity shifts),
     * L1₂ vs.\ D0₂₃ phase handling for Zr-bearing systems (please
       explicitly recommend whether metastable L1₂-Al₃Zr should be
       *active* and equilibrium D0₂₃ *suspended* in the Scheil /
       AM-Module setup),
     * hot-cracking / solidification-cracking susceptibility windows,
     * known atomization issues (Zr dissolution requiring Al-10Zr
       master alloy, Mg vapour loss, etc.) only where they *change the
       recommended scan parameters*.
5. **Citations** — DOI/reference list for every literature-backed
   value.

## Constraints

* Stay within the Aconity MIDI operating envelope.  If a literature
  value falls outside that envelope, flag it rather than pretending
  the machine can reach it.
* Do not invent absorptivity values — recommend either "use
  Thermo-Calc's Calculated mode with prefactor 1.0" or "override to a
  literature-calibrated constant of X" with an explicit citation.
* Be concise.  The downstream use is a ~1-page email to Thermo-Calc's account manager
  plus a Phase-I Aconity MIDI setpoint sheet; avoid recapping BOFN
  theory.

## Attached reference material

Attached: FLAIME proposal (clean build), Thermo-Calc 3-B CALPHAD
strategy, AM scale-up test-structures doc, Pareto-front synthesis of
AM Al alloys, prior LLM warm-start composition recommendations, and
the Thermo-Calc discussion transcript (Thermo-Calc's account manager, a Thermo-Calc specialist, Sterling
Baird, 9 Apr 2026) that motivated this request.
""".strip()


# ---- Per-composition specifics -------------------------------------------
COMPOSITIONS = [
    {
        "slug": "alsi10mg",
        "title": "AlSi10Mg (commercial reference)",
        "spec": (
            "Al-9.0–11.0 wt% Si, 0.25–0.45 wt% Mg, bal. Al (use "
            "midpoint: Si 10.0, Mg 0.325, bal. Al for the single-point "
            "run). This is the commercial LPBF-Al reference and the "
            "Thermo-Calc AM Module's *calibration* alloy — your "
            "recommendation here effectively re-verifies the default "
            "parameter set."
        ),
        "context": (
            "This is FLAIME's commercial baseline. The interesting "
            "question is NOT 'what are the AlSi10Mg LPBF parameters' "
            "(well-published) but 'what scan parameters, and what P–v "
            "grid bounds, are the best match to the AM Module's "
            "AlSi10Mg-calibrated absorptivity so the sim is "
            "representative of the Aconity MIDI we will print on'. "
            "Prioritize agreement with published Aconity / EOS M290 / "
            "SLM 280 AlSi10Mg process windows; flag where the AM "
            "Module's default absorptivity prefactor of 1.0 is known "
            "to over- or under-predict melt-pool depth."
        ),
    },
    {
        "slug": "byu-blend",
        "title": "BYU AA1100 + Si + AlSi10Mg blend (Al 75.56 / Si 24.30 / Mg 0.14 wt%)",
        "spec": (
            "Al 75.56, Si 24.30, Mg 0.14 (wt%); balance Al. Treat as "
            "a single effective chemistry. This is the 100 g "
            "ultrasonic-atomization blend being prepared at BYU "
            "(38.16 g AA1100 wire + 20.30 g Si powder + 41.55 g "
            "AlSi10Mg powder, normalized to 100 wt%). Feedstock "
            "tolerances give Al 74.94–75.88 / Si 23.63–24.77 / "
            "Mg 0.08–0.19 — note for absorptivity sensitivity but "
            "recommend a single nominal parameter set."
        ),
        "context": (
            "This is a hypereutectic Al-Si composition (24.3 wt% Si "
            "≫ 12.6 wt% eutectic). LPBF parameter databases are "
            "sparse here — recommendations should lean on the "
            "hypereutectic Al-Si LPBF literature (e.g. Al-20Si, "
            "Al-50Si studies) rather than AlSi10Mg extrapolation. "
            "Primary-Si nucleation at ~10⁴–10⁶ K/s LPBF cooling "
            "rates is the dominant physics concern. Flag whether the "
            "AM Module's AlSi10Mg absorptivity calibration is valid "
            "here; Si-rich melts have materially different optical "
            "behaviour."
        ),
    },
    {
        "slug": "mehta-alloy-c",
        "title": 'Mehta et al. "Alloy C" — Al-5.0Mn-0.8Cr-0.5Zr (wt%)',
        "spec": (
            "Al-5.0 Mn - 0.8 Cr - 0.5 Zr (wt%), bal. Al. Zr above the "
            "~0.28 wt% peritectic threshold to maximize L1₂-Al₃Zr "
            "volume fraction; Mehta et al. (2022/2024) report "
            "crack-free PBF-LB with YS 250–500 MPa and high-T YS "
            "~170 MPa at 300 °C."
        ),
        "context": (
            "This is FLAIME's literature-anchored Al-Mn-Cr-Zr "
            "high-temperature ground-truth node. It is the "
            "highest-priority composition after AlSi10Mg because "
            "the downstream BOFN surrogate is calibrated against "
            "Mehta's published YS/ductility. Recommendations should: "
            "(i) specify scan parameters that reproduce Mehta's "
            "reported crack-free window, (ii) explicitly recommend "
            "L1₂-Al₃Zr *active* / D0₂₃ *suspended* in the Scheil "
            "setup, (iii) comment on Mn solute-trapping at LPBF "
            "cooling rates and its impact on melt-pool absorptivity, "
            "(iv) flag whether TCAL10 has assessed Al-Mn-Zr and "
            "Al-Cr-Zr ternaries or is binary-extrapolating."
        ),
    },
    {
        "slug": "glerum-al-1-5zr",
        "title": "Glerum et al. Al-1.5 Zr supersaturated LPBF (wt%)",
        "spec": (
            "Al-1.5 Zr (wt%), bal. Al. Strongly supersaturated "
            "relative to the ~0.28 wt% equilibrium peritectic, but "
            "within the 1–3 at% retention limit reported for LPBF "
            "rapid cooling. Glerum et al. (2020, Add. Manuf. 36, "
            "101461) demonstrated crack-free SLM prints and ~600 "
            "MPa hardness from massive primary L1₂-Al₃Zr."
        ),
        "context": (
            "This is the Al-Zr anchor. It forces the AM Module to "
            "handle non-equilibrium Zr retention and the G/R "
            "conditions required for intrinsic equiaxed nucleation. "
            "Atomization note: dissolving 1.5 wt% Zr in the BYU "
            "induction crucible requires an Al-10Zr (or Al-5Zr) "
            "master alloy rather than elemental Zr — but this does "
            "*not* change the CALPHAD/AM-Module input. "
            "Recommendations should: (i) specify scan parameters "
            "that preserve primary L1₂-Al₃Zr nucleation (high G, "
            "moderate R), (ii) explicitly recommend L1₂ *active* / "
            "D0₂₃ *suspended*, (iii) suggest whether a warmer "
            "base-plate (150–200 °C) is justified to stabilize "
            "the nucleation window vs.\ the Thermo-Calc 30 °C "
            "default."
        ),
    },
]


def build_query(spec: str, title: str, context: str) -> str:
    return (
        SHARED_PREAMBLE
        + "\n\n---\n\n"
        + f"## Target composition\n\n**{title}**\n\n{spec}\n\n"
        + f"## Composition-specific context\n\n{context}\n"
    )


submitted = []
for comp in COMPOSITIONS:
    query = build_query(comp["spec"], comp["title"], comp["context"])
    task_request = TaskRequest(
        name=JobNames.LITERATURE_HIGH,
        query=query,
        runtime_config=RuntimeConfig(
            environment_config={"data_storage_uris": data_uris},
        ),
    )
    task = client.create_task(task_data=task_request)
    # create_task may return a Task object or a task-id string depending on
    # edison-client version. Handle both.
    task_id = getattr(task, "id", None) or str(task)
    status = getattr(task, "status", "submitted")
    row = {
        "slug": comp["slug"],
        "title": comp["title"],
        "task_id": task_id,
        "status": str(status),
    }
    submitted.append(row)
    print(f"[{comp['slug']:18s}] task_id={task_id}  status={status}")

out = pathlib.Path("/tmp/edison_scanparams_task_ids.json")
out.write_text(json.dumps(submitted, indent=2))
print(f"\nWrote {out}")
print("Do NOT wait — fetch results next session with:")
print("  client.get_task(task_id)  or the existing poll_and_save helper.")
