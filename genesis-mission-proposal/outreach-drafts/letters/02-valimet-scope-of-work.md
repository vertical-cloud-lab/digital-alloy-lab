# Scope of Work — Valimet, Inc. (Funded Subrecipient)

**Project:** FLAIME — Fast Learning AI for Mineral Efficiency
**Prime:** Brigham Young University (PI: Sterling G. Baird, Ph.D.)
**Funding instrument:** DOE Genesis Mission RFA DE-FOA-0003612, Topic 3-B
**Period of performance:** Phase I, 9 months (FOA-defined: 2026-07-01 through 2027-03-31)
**Subaward value:** [removed from the public copy]

---

## (a) Objective

Provide gas-atomized aluminum-alloy feedstock powders, on a
BOFN-pipeline-driven cadence, that meet laser powder-bed fusion (LPBF)
specification and enable FLAIME's closed-loop AI discovery of
critical-mineral-lean aluminum alloys. Valimet is the **sole funded
industry partner** for scale-up powder production in Phase I and is the
production-grade complement to BYU's in-house ultrasonic atomization
(rePOWDER, AMAZEMET) used for early-stage screening.

## (b) Powder Specifications

- **Particle size distribution (PSD):** 20–63 µm (LPBF target band).
  Acceptance: **D10 ≥ 15 µm, D50 in 30–45 µm, D90 ≤ 63 µm** (tightened
  from the ~70 µm upper band typical of cold-spray cuts, to match
  LPBF recoater clearance), with band tolerance ±10% of nominal
  D-values per lot. *Valimet may propose a relaxed D90 ≤ 70 µm if
  recoverable yield in the 20–63 µm cut would otherwise fall below
  ~30%; PI to confirm before each lot.*
- **Alloy family:** Al-based, critical-mineral-lean (low Mn / Cr / Co)
  compositions drawn from FLAIME's BOFN engine. Compositions confirmed
  by BYU PI ≥60 days before each scale-up run.
- **Default lot size:** ≥50 kg per composition.
- **Sensitivity:** 1–2 of the ~6 Phase I lots may be upsized to **75 kg**
  if a BOFN-identified hit composition warrants extended LPBF
  build-and-test campaigns. Upsize confirmed by BYU PI ≥60 days ahead.

## (c) Composition Pipeline

- **Source:** Compositions selected by the FLAIME BOFN (Bayesian
  optimization with function networks) discovery engine running at BYU
  on the merged CALPHAD + experimental data lake.
- **Volume:** Approximately **6 scale-up runs** in Phase I (one per
  ~2 months once the BOFN engine is producing scale-worthy candidates;
  scaled-down feasibility lots for atomizer setup are not counted in
  the 6).
- **Coordination:** BYU PI provides Valimet with target composition,
  master-alloy bill of materials, and run-window confirmation **≥60
  calendar days** ahead of each scheduled atomization run, to allow
  master-alloy procurement and atomizer scheduling.

## (d) Schedule

Quarterly lot cadence, gated on FLAIME milestones:

| Quarter | Run window | Notes |
|---------|------------|-------|
| W1 | (PoP month 1–2) | Setup + first composition (baseline / control) |
| W2 | (PoP month 3–4) | 2 compositions (one BOFN-selected) |
| W3 | (PoP month 5–6) | 2 compositions; 1 candidate for 75 kg upsize |
| W4 | (PoP month 7–9) | Final composition + Phase II hand-off documentation |

Schedule will flex with BOFN engine readiness; net cadence ~6 lots/year.

## (e) Deliverables

For each lot, Valimet delivers to BYU:

1. **Powder** (≥50 kg, or upsized 75 kg as agreed) in sealed,
   moisture-controlled containers, ground-shipped per Valimet's standard
   hazmat protocol for Al powders.
2. **Certificate of Analysis (COA)** including: ICP composition (all
   alloying elements + key impurities), PSD curve (laser diffraction
   or sieve, per Valimet standard), apparent + tap density, oxygen
   content (LECO), Hall flow.
3. **Lot traceability record** — master-alloy heat numbers, atomizer
   run number, atomization date, gas (N₂ / Ar) and process parameters
   (within Valimet's disclosable envelope; see (f)).
4. **Retain sample** — 500 g sealed retain held at Valimet for ≥3 years
   for forensic re-analysis if needed.

## (f) Data Sharing

- **Open-data scope (DOE-aligned):** Composition (as-shipped ICP), PSD,
  density, flow, oxygen, atomization gas type, and high-level process
  metadata (atomizer class, nominal melt-and-atomize temperature window)
  flow into FLAIME's open data lake and are eligible for DOE Public
  Access Plan deposit.
- **Proprietary scope and IP terms:** [removed from the public copy]

## (g) Acceptance Criteria

A lot is **accepted** if:

- **PSD:** D10, D50, D90 within ±10% of agreed nominal values for the
  20–63 µm band; <5% mass below 20 µm and <5% mass above 63 µm.
- **Oxygen content:** ≤ **500 ppm** for Al alloys (industry-standard
  AM-LPBF Al feedstock spec; Valimet AM-C grade routinely meets this;
  PI may relax to ≤800 ppm for screening lots if Valimet flags
  recovery concerns for a specific composition).
- **Composition (ICP):** Each alloying element within ±5% relative of
  target (or ±0.05 wt% absolute, whichever is larger), with all critical
  minerals (Mn, Cr, Co) below the BOFN-set ceiling.
- **Documentation:** COA + traceability record complete and signed.

A lot failing acceptance triggers a no-cost rework or scope substitution
discussion within 10 business days; cost-share treatment of failed-lot
materials is addressed in the cost-share guide.
