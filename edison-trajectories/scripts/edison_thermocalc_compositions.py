"""Submit an Edison analysis query to recommend specific compositions
for the Thermo-Calc AM Module simulations.

Bundles: FLAIME proposal PDF + key Edison trajectory files on the
anchor Al-Zr and Al-Mn-Cr-Zr systems and LLM-warm-start composition
recommendations. Does NOT wait for completion; prints task ID.
"""
import os
from edison_client import EdisonClient, JobNames
from edison_client.models import TaskRequest, RuntimeConfig

api_key = os.environ["EDISON_API_KEY"]
client = EdisonClient(api_key=api_key)

REPO = "/workspaces/digital-alloy-lab-private"

UPLOADS = [
    f"{REPO}/genesis-mission-proposal/flaime-genesis-proposal-clean.pdf",
    f"{REPO}/edison-trajectories/thermocalc_3b_calphad_strategy_full.md",
    f"{REPO}/edison-trajectories/llm-warmstart-compositions.md",
    f"{REPO}/edison-trajectories/calphad_alloy_design.md",
    f"{REPO}/edison-trajectories/pareto-am-al-alloys/pareto_front_analysis.md",
    f"{REPO}/edison-trajectories/pareto-am-al-alloys/batch5_pareto_synthesis.md",
    f"{REPO}/edison-trajectories/am-scaleup-test-structures.md",
]

print("Uploading files...")
data_uris = []
for p in UPLOADS:
    ref = client.upload_file(p)
    print(f"  {p} -> {ref}")
    data_uris.append(ref)

QUERY = r"""
# Task: Recommend specific composition points for Thermo-Calc AM Module simulations

## Context
FLAIME is a DOE Genesis Mission proposal (DE-FOA-0003612, Topic 3-B) for AI-driven
discovery of additively manufacturable, critical-mineral-lean aluminum alloys. The
proposal identifies two "anchor" Al-alloy sub-systems as the initial focus for
Activity 1 CALPHAD screening and early atomization campaigns:

  1. **Al-Mn-Cr-Zr** (transition-metal grain-refined, high-temperature AM aluminum)
  2. **Al-Zr**      (dispersoid-strengthened, L1_2-Al_3Zr precipitate family)

Thermo-Calc's account manager and a Thermo-Calc specialist have agreed in principle to run AM Module
simulations for **up to 2-3 compositions per anchor system** as a coordinated
partner deliverable (alongside a separately-budgeted Letter of Commitment).
These simulations feed the higher-fidelity CALPHAD tier of FLAIME's BOFN
(Bayesian Optimization of Function Networks) surrogate hierarchy and inform the
first-wave atomization campaign with AMAZEMET rePOWDER + BYU induction crucible.

In parallel, two additional compositions have already been selected for the
non-anchor "baseline readiness" track:

  3. **AlSi10Mg** (MSE Supplies midpoint: Si 10.0 / Mg 0.325 / Al bal wt%) -
     commercial Al-Si-Mg benchmark
  4. **Al-Si-Mg blend** (Al 75.56 / Si 24.30 / Mg 0.14 wt%) - the AA1100-wire +
     Si + AlSi10Mg induction-crucible blend atomized at BYU as the end-to-end
     readiness demonstration

These 3 and 4 are fixed. We need your recommendations for points 1 and 2.

## What we need from you
For EACH of Al-Mn-Cr-Zr and Al-Zr, recommend **2-3 specific candidate
compositions (wt%)** for Thermo-Calc AM Module simulation, with:

(a) The specific wt% of each alloying element (Mn, Cr, Zr for the first system;
    Zr for the second), balance Al. Provide uncertainty bounds if the literature
    supports a sensitivity window rather than a single point.

(b) A short rationale tying each composition to:
    - Expected equilibrium / Scheil-solidification phase assemblage
      (e.g., primary Al_3Zr L1_2 vs Al_11Mn_4, Al_45Cr_7, etc.)
    - AM-relevant processing window (solidification range, hot-cracking
      susceptibility indicators, printability scores if available)
    - Downstream target property (high-T strength retention, grain refinement,
      precipitation strengthening, solidification crack resistance)
    - Relevance to DOE's critical-mineral-lean framing (avoidance of Co, Cr>5%,
      Ni, or other flagged elements; Cr is on the critical list but low-loading
      dispersoid-regime usage may be acceptable - please flag)

(c) A priority ordering within each system (1st choice, 2nd, 3rd) so that if
    Thermo-Calc accepts only 2 per system we know which to drop.

(d) Any flags where the AM Module specifically adds value beyond what
    equilibrium or Scheil alone would reveal (e.g., back-diffusion,
    segregation profiles across LPBF cooling rates, Marangoni effects on
    composition drift, or non-equilibrium phase suppression).

## Constraints and preferences
- Stay within the **15-element FLAIME palette** (Al + Mn, Cr, Zr, Mg, Si, Cu,
  Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn). Pure-binary/ternary/quaternary within
  {Al, Mn, Cr, Zr} and {Al, Zr} respectively is fine; do NOT suggest adding
  off-palette elements.
- Prioritize compositions that are **atomization-realistic** for the
  AMAZEMET rePOWDER + BYU induction-crucible platform: i.e., melting-point
  and vapor-pressure behaviour consistent with induction heating of Al-based
  melts, with no exotic containment requirements. Zr loadings above the
  ~0.1-0.5 wt% peritectic sensitivity threshold should be called out
  explicitly.
- Favour **published Pareto-relevant compositions** (printability vs
  strength vs temperature capability) over wholly novel guesses, but do NOT
  restrict yourself to only published compositions if the literature has
  obvious gaps worth filling. When citing a composition from literature,
  provide the DOI/reference.
- Compositions that **anchor existing CALPHAD validation data** (enabling
  surrogate-vs-ground-truth checks in Activity 1) are especially valuable.
  Compositions that are **already in TCAL10 well-validated regions** are
  preferred over bleeding-edge extrapolation.
- Where the literature or CALPHAD strategy docs (attached) favour a specific
  point, lean toward it.

## Deliverable format
Return a structured response with:

  - Section 1: Al-Mn-Cr-Zr candidate compositions (2-3, priority-ordered)
  - Section 2: Al-Zr candidate compositions (2-3, priority-ordered)
  - Section 3: Concise justification for the top pick in each system
    (suitable for dropping directly into a 1-paragraph email to Thermo-Calc's account manager)
  - Section 4: Caveats, uncertainties, and "things we should ask Thermo-Calc to
    sanity-check" before he runs the sims
  - Section 5: Cross-references to the attached Edison trajectory documents
    where your recommendations build on prior FLAIME analysis

## Attached reference materials
  1. FLAIME full proposal PDF (clean build) - contains palette, BOFN
     surrogate design, Activity 1 methodology, CALPHAD strategy, timeline,
     success criteria
  2. thermocalc_3b_calphad_strategy_full.md - full Thermo-Calc strategy
     analysis for Topic 3-B (includes TCAL10 database coverage)
  3. llm-warmstart-compositions.md - prior Edison LLM-based composition
     recommendations for FLAIME warm-start
  4. calphad_alloy_design.md - CALPHAD alloy-design methodology review
  5. pareto_front_analysis.md + batch5_pareto_synthesis.md - Pareto front
     synthesis for AM Al alloys from literature review
  6. am-scaleup-test-structures.md - AM scale-up considerations that inform
     printability/hot-cracking requirements

Please integrate across these sources rather than treating them in isolation.
""".strip()

print("\nSubmitting Edison analysis task...")
task_request = TaskRequest(
    name=JobNames.ANALYSIS,
    query=QUERY,
    runtime_config=RuntimeConfig(
        environment_config={"data_storage_uris": data_uris},
    ),
)
task = client.create_task(task_data=task_request)
print(f"\nTask ID: {task.id}")
print(f"Status: {task.status}")
print(f"Submitted at: {task.created_at if hasattr(task, 'created_at') else 'n/a'}")
