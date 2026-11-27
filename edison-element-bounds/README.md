# Edison element-bounds orchestrator

This directory contains a single Edison Scientific orchestration script,
`run_element_bounds.py`, that resolves the FLAIME element-palette bounds
issue (vertical-cloud-lab/digital-alloy-lab-private element bounds task).

## What it does

Three phases of Edison queries over the FLAIME 15-element palette
(Al + Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn):

1. **Phase 1 — LITERATURE (parallel)**
   * 16 per-element upper-bound queries (1 per element, including Al)
     asking for a *conservative* and *non-conservative* bound with
     justification + failure modes.
   * 1 lower-bound query (Al-rich constraint; Al is the only element with
     a meaningful nonzero lower bound).
   * 1 simultaneous all-bounds query (LITERATURE_HIGH).
2. **Phase 2 — ANALYSIS** (with all phase-1 markdown trajectories
   uploaded): produces a finalized bounds table for the BOFN search space.
3. **Phase 3 — ANALYSIS** (with phase-1 + phase-2 uploaded): produces
   special multi-element constraints (sum / ratio constraints, TCAl10
   coverage guardrails, atomization / printability edge cases).

All results land in `edison-trajectories/element-bounds/` as markdown.

## Usage

```bash
export EDISON_API_KEY=...
python edison-element-bounds/run_element_bounds.py
```

Useful flags:

```bash
# preview the prompts without contacting Edison
python edison-element-bounds/run_element_bounds.py --dry-run

# rerun only phase 2/3 against existing phase-1 markdown files
python edison-element-bounds/run_element_bounds.py --phases 2,3
```

LITERATURE queries can take 5–10 min; LITERATURE_HIGH up to ~15 min;
ANALYSIS queries another 5–15 min. The script polls patiently and writes
each result as soon as it returns.
