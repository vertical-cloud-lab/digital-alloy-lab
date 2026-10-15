# AI-ICME Persona Mock-Organizer Review — PENDING (Edison LITERATURE_HIGH)

*For the **AI-ICME** variant of [`tms-2027-lpbf-process-parameter-optimization-abstract.md`](../../tms-2027-lpbf-process-parameter-optimization-abstract.md).*
*Target symposium: **Artificial Intelligence Applications in Integrated Computational Materials Engineering (AI-ICME)**.*

> **Status: submitted, awaiting response.** A high-effort `LITERATURE_HIGH`
> (`job-futurehouse-paperqa3-high`) persona mock-review was submitted to Edison Scientific and takes up to
> ~10–15 min to complete. This stub records provenance so the report can be fetched on a follow-up `@claude`
> pass (the same submit-now / fetch-later pattern used for
> [round 1](round1-organizer-feedback.md)). Once fetched, replace this file with
> `ai-icme-persona-review.md` carrying the full report.

## Provenance

| Field | Value |
|---|---|
| Edison job | `job-futurehouse-paperqa3-high` (`JobNames.LITERATURE_HIGH`) |
| Task ID | `f7ca5bda-0232-452b-b9d3-0e32482082e3` |
| Submitted | 2026-07-07 (PR #101) |
| Endpoint | `https://api.platform.edisonscientific.com` |
| Trigger | [PR #101 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/101) — "create an updated AI-ICME title/abstract and send an Edison persona mock-review" |

## Title reviewed

> An ICME Loop for Composition-Aware LPBF Parameter Qualification: CALPHAD-Predicted Printability, Bayesian
> Optimization, and Cross-Section Feedback to the Thermo-Calc AM Module

## Abstract reviewed (150 words)

> Integrated computational materials engineering (ICME) promises to compress laser powder bed fusion (LPBF)
> parameter qualification by predicting printable windows before printing — but CALPHAD-based predictions are
> least tested exactly where new alloys live: unexplored regions of composition space. We build an ICME loop
> spanning a wide aluminum elemental palette. Thermo-Calc AM Module simulations translate CALPHAD-derived
> thermophysical properties into melt-pool geometry and keyholing/lack-of-fusion/balling boundaries in
> power–speed space; Bayesian optimization proposes an efficient experiment sequence; and a matched campaign on
> an Aconity MIDI at the University of Utah climbs an escalating ladder (single-track cross-sections, density
> cubes, ISO/ASTM 52902 artifacts, tensile bars). Single-track cross-sections feed back to calibrate the
> module's aluminum absorptivity, testing where predictions hold — and where they degrade — as composition
> moves away from calibrated baselines. An LLM agent orchestrates the simulation and optimization tool calls.
> We report composition-resolved model–experiment agreement, cross-machine/instance transfer, and the
> experimental budget each alloy requires.

## Personas requested (AI-ICME organizers)

Per the organizer read in [PR #101 comment #4870800010](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/pull/101#issuecomment-4870800010):

1. **Ghanshyam Pilania** — GE Aerospace Research (ex-LANL); materials-informatics heavyweight, industry
   Thermo-Calc/CALPHAD end-user.
2. **Ram Devanathan** — PNNL; DOE computational-materials / data-science lead (provenance, reproducibility,
   physics-informed ML).
3. **Avanish Mishra** — LANL; DOE/NNSA computational scientist (simulation fidelity, model validation).
4. **Victoria M. Miller** — University of Florida; microstructure / physical metallurgy.
5. **Vikas Tomar** — Purdue; mechanics / in-situ characterization.
6. **Wenwu Xu / Yang Yang** — San Diego State University; symposium co-leads (ML + AM), scope/program balance.

The panel was asked, per organizer, for a verdict, an enthusiasm score (1–10), what lands, top concerns, and the
single highest-leverage edit — plus an overall synthesis covering: accept likelihood; whether the
composition-space "where CALPHAD degrades" hook lands vs. over-promises for a CALPHAD-native audience; whether to
keep/expand/drop the single LLM-agent clause for this room; how to position the AM-Module absorptivity
calibration-feedback loop (headline vs. supporting); and the top 3 ranked edits.

## To fetch

Re-run against task `f7ca5bda-0232-452b-b9d3-0e32482082e3`:

```python
from edison_client import EdisonClient
client = EdisonClient(api_key=EDISON_PLATFORM_API_KEY)
task = client.get_task("f7ca5bda-0232-452b-b9d3-0e32482082e3")
```
