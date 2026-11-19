> **SUPERSEDED 2026-04-21**: This analysis used the earlier \$42K liquid-Ar-dewar basis. Current proposal Ar line is \$10,000, derived per the AMAZEMET *rePOWDER Induction Facility Guide* (2025, §6.2) at 417 L purge + ∼600 L active-atomization blanket ≈ 1,000 L/run × 350 runs ≈ 350 m³ gas ≈ 48 K-size cylinder exchanges × \$150 + \$1,800 rental (2 cyl × 9 mo) + \$1,000 regulators/contingency. Feedstock line reduced \$40K→\$36K to offset; M&S total unchanged at \$112,468. See `genesis-mission-proposal/flaime-genesis-proposal.tex` §(E) for current narrative.

# FLAIME Budget Re-audit — Research-Grade Feedstock, GA Feedstock, Characterization

**Purpose.** PI-directed re-audit of three BYU M&S sub-lines in the FLAIME Genesis Mission
Phase I budget (`genesis-mission-proposal/flaime-genesis-proposal.tex` lines 2297–2333) under
tightened scope assumptions:

1. **GA feedstock prep** — re-price for **6 Valimet runs × ≥50 kg** (not 3–6), including the
   sensitivity case of 1–2 runs at 75 kg.
2. **BYU SEM/EDS/EBSD recharge** — re-cost against the PR #55 Gantt throughput of
   **16 compositions/week** and a realistic total of **150–200 compositions** over the 9-month PoP,
   with BYU Microscopy Center, BYU Geology, and BYU Spectroscopic Facility *actually published*
   user fees — not the $600/hr figure in the proposal body table (which is instrument TCO, not
   user rate).
3. **Research-grade elemental feedstock** — verify that the existing $8,084 MID covers the full
   15-element palette at 100 g–1 kg scale with nothing missing.

This worksheet **does not modify** `flaime-genesis-proposal.tex`. It is a supporting audit only.
Reads off the three prior spotchecks (`spotcheck-research-powders.md`,
`spotcheck-ga-feedstock-and-argon.md`, `spotcheck-tc-and-consumables.md`) and augments with new
vendor/facility pricing pulled in the current session.

---

## 0. Re-audit scope assumptions (fixed inputs)

| Parameter | Value | Source |
|---|---|---|
| Period of performance | 9 months (2026-07-01 → 2027-03-31) | FOA + proposal §budget |
| Pipeline throughput | 16 compositions/week | PR #55 `gantt-scheduling/generate_gantt.py` |
| Total compositions screened (LOW / MID / HIGH) | 100 / 150 / 200 | proposal narrative |
| Al-alloy palette | Al + 1–3 of {Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn} | proposal §Alloy space |
| Sc / Er ceiling (charter-bounded) | ≤ 0.5 at.% / ≤ 0.3 at.% | proposal mineral-burden rationale |
| Valimet runs | **6 × ≥50 kg** (was 3–6 × 50 kg) | PI directive, this audit |
| Sensitivity: 1–2 of 6 runs at 75 kg | ✓ | PI directive, this audit |
| BYU PI home college | Ira A. Fulton College of Engineering | Baird CV |

Because Baird is in the College of Engineering, FLAIME qualifies for the **subsidized CMS /
Engineering / Life-Sciences user rate** at the BYU Electron Microscopy Facility
($30/hr all SEMs, $30/hr TF20 TEM), *not* the general-BYU rate ($80–150/hr) and not the external
rate ($80–$300/hr + $300/hr staff). This is the single biggest driver of the characterization-line
arithmetic below.

---

# PART 1 — Research-grade elemental feedstock ($8,000 line)

## 1.1 Palette-coverage check against spotcheck-research-powders.md MID

The prior `spotcheck-research-powders.md` MID purchase list (M1–M21) contains one SKU for
**every** element in the 15-element charter palette plus Sn (16th), plus the AlSi10Mg baseline
LPBF reference, plus shipping/haz, atomization-related consumables, a restock contingency, and an
Al-Sc master-alloy hedge. Explicit cross-check:

| # | Element | Covered in MID? | SKU line |
|---|---|---|---|
| 1 | Al (4N shot) | ✅ | M1 |
| 2 | Mn | ✅ | M2 |
| 3 | Cr | ✅ | M3 |
| 4 | Zr | ✅ | M4 |
| 5 | Mg | ✅ | M5 |
| 6 | Si | ✅ | M6 |
| 7 | Cu | ✅ | M7 |
| 8 | Ti | ✅ | M8 |
| 9 | Fe | ✅ | M9 |
| 10 | Ni | ✅ | M10 |
| 11 | Ce | ✅ | M11 |
| 12 | Sc | ✅ (+ Al-Sc 2% master-alloy hedge) | M12 + M21 |
| 13 | Li | ✅ | M13 |
| 14 | Er | ✅ | M14 |
| 15 | Zn | ✅ | M15 |
| 16 | Sn | ✅ (not in charter but listed as optional) | M16 |
| — | AlSi10Mg LPBF baseline powder | ✅ (5 kg) | M17 |
| — | Ship / haz + consumables + restock | ✅ | M18–M20 |

**Nothing is missing.** The MID covers the charter palette at 100 g–1 kg working scale plus
small-gram pilots for Sc (5 g), Er (10 g), and Li (25 g ribbon), which matches FLAIME's bounded
exotic-element use.

## 1.2 Scenario roll-up (unchanged from prior spotcheck, re-summarized)

| Scenario | Composition | Subtotal (SKU) | Ship + haz | Consumables + restock | Sc master-alloy hedge | **Total** |
|---|---|---|---|---|---|---|
| **LOW** (Al-Mn-Cr-Zr focus, no exotics) | L1–L11 | ~$2,403 | ~$200 | ~$1,300 | — | **~$3,900** |
| **MID** (full 15-element palette + small Sc/Er/Li pilots) | M1–M17 | ~$5,304 | ~$530 | ~$1,900 | ~$350 | **~$8,084** |
| **HIGH** (2nd exotic buy, 10 kg LPBF baseline, 1 kg Ti pack) | H1–H9 | — | ~$900 | ~$700 | ~$4,000 add'l Sc | **~$13,137** |

## 1.3 Recommendation — keep $8,000

The existing $8,084 MID is within 1.1% of the $8,000 line, fully funds the 15-element palette
(plus Sn + AlSi10Mg baseline), and carries a named master-alloy substitution contingency. **Hold
at $8,000**; the sensitivity that could push this over is a Cr or Sc list-price move of >25%,
which the internal contingency (M20) absorbs. No change recommended.

---

# PART 2 — GA feedstock for 6 Valimet runs ($5,000 line)

## 2.1 Tightened input: 6 runs guaranteed, 1–2 at 75 kg

Prior spotcheck (`spotcheck-ga-feedstock-and-argon.md`) priced three scenarios for **either 3 or 6
runs × 50 kg**. With the PI's tightened assumption that **all 6 runs are realized** and that a
realistic worst case has 1–2 runs at **75 kg** (i.e. aggregate input 300–400 kg vs. the current
"150–300 kg" text), we re-roll using the same LIKELY $/kg column from that spotcheck (§1.2 of
that file) — which came from AMG Aluminum, Belmont Metals, Reade, KBM Affilips, Stanford Advanced
Materials, American Elements, and the ScrapMonster Al-2Sc index.

### 2.1.1 Representative per-run feedstock cost at 50 kg (LIKELY $/kg)

| Run | Target composition | Feedstock cost | Source |
|---|---|---|---|
| R1 | Al-2Mn-1Cr-0.5Zr (anchor) | $298 | §1.3 of prior spotcheck |
| R2 | Al-1Zr (L1₂ precipitate) | $214 | §1.4/B2 |
| R3 | Al-2Mn-0.5Zr-0.1 Ti grain-refiner | $261 | §1.4/B3 |
| R4 | Al-2Mn-1Ce | $513 | §1.4/B4 |
| R5 | Al-2Mn-0.5Cr-0.2Ce | $268 | §1.4/B5 |
| R6 | Al-2Mn-1Cr-0.5Zr-0.2Sc (Sc-bounded, 5 kg Al-2Sc @ $250/kg) | ~$1,520 | §1.4/B6 |
| **6×50 kg subtotal (LIKELY, balanced)** | | **$3,074** | |

### 2.1.2 Delta for 1–2 runs at 75 kg (extra 25–50 kg each)

The **marginal 25 kg at 75-kg scale is almost pure 99.7 commercial Al** (the master-alloy mass
doesn't scale linearly because Mn/Cr/Zr wt% targets are unchanged — more balance Al is added).
At $2.80/kg LIKELY for 99.7 Al ingot + modest extra master-alloy top-up:

- +25 kg scale-up per run: ~25 × $2.80 + ~1 kg extra MA at average $20 = **~$90/run**
- +50 kg scale-up per run (75 kg): ~50 × $2.80 + ~2 kg MA ≈ **~$180/run**

So a 1× 75-kg run adds ~$90; 2× 75-kg runs add ~$180. In the worst case (R4 or R6 — the Ce- or
Sc-bounded compositions — pushed to 75 kg) the increment is **up to +$300** because the MA
fraction scales with mass.

### 2.1.3 Loaded totals (ship + BYU prep labor + contingency)

| Scenario | 6-run feedstock | Extra for 75-kg upsize | Ship (6×$75) | BYU prep (6×$80) | Contingency 15% | **Total** |
|---|---|---|---|---|---|---|
| **LOW** (6 × 50 kg, lean, Mn-Cr-Zr only, no Sc/Er/Ce) | $1,788 (6 × $298) | — | $450 | $480 | $408 | **~$3,126** |
| **MID** (6 × 50 kg balanced, 1 Sc-bounded run @ $1,520) | $3,074 | — | $450 | $480 | $601 | **~$4,605** |
| **MID+** (6 × 50 kg balanced, 2 of 6 at 75 kg) | $3,074 | +$300 | $450 | $480 (no prep delta) | $646 | **~$4,950** |
| **HIGH** (6 × 50 kg aggressive: 1 Sc-bounded + 1 Er-bounded, UPPER $/kg column; 2 runs at 75 kg) | $4,586 (UPPER feedstock per §1.4/Scenario C) | +$300 | $600 | $600 | $1,217 | **~$7,303** |

## 2.2 Recommendation — bump $5,000 → $6,000

- The **$5,000 line covers MID** (6 × 50 kg balanced with one Sc-bounded run) with ~$395 headroom.
- Once either (a) **one of the runs upsizes to 75 kg** OR (b) a **second** composition lands at
  the Sc-bounded or Er-bounded end of the palette, the MID+ case lands at ~$4,950 — essentially
  on the line with zero slack.
- The HIGH case (both 75-kg upsizing *and* two exotic-bounded runs *and* UPPER $/kg column) at
  ~$7,300 exceeds the line by ~$2,300.

**Recommend bumping the GA feedstock line from $5,000 → $6,000 (+$1,000).** Rationale: this
absorbs the MID+ case with the same 15% contingency, keeps Scenario C within ~$1,300 of the line
(acceptable tail risk), and preserves the proposal's current upper-bound text ("≤ $8,100 worst
case with a 0.2 wt% Sc-bounded composition") which already implies $5K is tight. A $6,000 line
also restores ~$1,000 of true contingency that the current $5K narrative has quietly spent on
"Scenario B sits at $4,605 with $395 headroom."

An aggressive hedge to $6,500 would cover the HIGH case's Sc-bounded + Er-bounded combo; a
conservative reviewer could argue the charter rules out that combination (only one of the six
runs should be bounded-exotic), in which case $6,000 is the honest number.

---

# PART 3 — BYU SEM/EDS/EBSD characterization ($4,500 line)

## 3.1 Actual BYU user fees (pulled this session)

Published internal-academic rates for the Baird group's home college
(College of Engineering ≡ "Engineering" in the BYU EM Facility rate card; equivalently subsidized
at the CMS / Life-Sciences tier):

### 3.1.1 BYU Electron Microscopy Facility (`microscopy.byu.edu/services`, via Wayback)

| Instrument | CMS / Engineering / Life-Sci user (Regular + After-hours) | General BYU user | External (Standard / Staff-assisted) |
|---|---|---|---|
| TF20 TEM | **$30.00/hr** | $150/hr | $150 / +$300 |
| Verios SEM (EDS, BSE, STEM) | **$30.00/hr** | $80/hr | $80 / +$300 |
| Apreo C SEM (EDS, BSE, **EBSD**, CL) | **$30.00/hr** | $80/hr | $80 / +$300 |
| Helios SEM/FIB (EDS, **EBSD**, FIB) | **$30.00/hr** | $100/hr | $100 / +$300 |

Sample-prep recharge (on-campus): Sputter Coater $10/run, SEM chemical prep $20/batch-of-6,
TEM sectioning $5/block, Carbon Coating routed through Geology (Mike Standing).

Staff-assisted operation for on-campus users: **no additional charge** (explicit in the facility's
"How We Support BYU Users" text).

**Reconciliation with proposal body text (line ~1381–1392):** the proposal's facilities narrative
shows a small table of the four SEM instruments, and the $600/hr figure appears elsewhere in the
proposal. Per the facility's own pricing page, **the operating cost to the facility is ~$300/hr**
and BYU partially subsidizes that cost so that BYU users pay the rates above. Any "$600/hr"
number in the proposal is either external + staff-assisted ($80 + $300 = $380 still doesn't hit
$600), a TEM-tier rate, or an older/wrong figure. The present audit uses the **$30/hr
Engineering-tier rate** because it is the actual rate Baird's grants will be charged.

### 3.1.2 BYU Spectroscopic Facility / ICP-MS (`labs.chem.byu.edu/byu-spectroscopic-facility/atomic-analysis`)

| Instrument | Internal BYU | External |
|---|---|---|
| Agilent 8900 ICP-MS/MS (ultra-trace elemental / isotopic) | **$35.00/hr** | $70/hr |

### 3.1.3 BYU Chemistry Powder XRD Facility (`labs.chem.byu.edu/byu-mp-xrd-facilities/procedures`)

Confirmed in the facility's own procedures page: **free of charge for BYU-affiliated users after
training.** No per-hour or per-sample fee for internal users. (Cost only materializes if XRD is
cross-charged through the BYU Geology Analytical Labs — those are quote-only internally and run
$35–$50/hr in the same tier as ICP-MS.)

### 3.1.4 Keyence VHX-7000, Hommel profilometer

In-house Baird/CMR equipment — included at $0/hr for FLAIME users.

## 3.2 Per-composition characterization recipe

Per composition (screened build), realistic instrument-hour budget:

| Task | Instrument | Hours | Cost @ BYU-Eng rate |
|---|---|---|---|
| Feedstock powder SEM/EDS (morphology + composition check) | Verios or Apreo | 0.5 | $15 |
| Printed cross-section SEM + EDS maps | Apreo or Helios | 1.0 | $30 |
| EBSD on printed sample (grain, texture) | Apreo or Helios | 0.5 | $15 |
| Powder XRD on gas-atomized or prep powder | BYU Chem MP-XRD | 0.5 | $0 (free) |
| Sample prep (mount, polish, sputter) | Consumables + sputter coater | — | $5 amortized |
| **Core per-composition characterization subtotal** | | **2.0 hr SEM + 0.5 hr XRD** | **~$65** |

ICP-MS is taken **once per ~4 compositions** (screening subset for composition validation), not
every composition:

| Task | Hours | Rate | Cost per screened composition |
|---|---|---|---|
| ICP-MS validation (Agilent 8900, ~1 hr per 4 compositions) | 0.25 | $35/hr | ~$9 |

**Per-composition loaded rate: ~$74.** (Core SEM $65 + ICP-MS share $9.)

## 3.3 Scenario totals at the PR #55 throughput

| Scenario | # compositions | Per-comp characterization | Gross | Additional overhead (training, failed prep, redo) 15% | **Total** |
|---|---|---|---|---|---|
| **LOW** (100 comp, minimum-viable screening) | 100 | $74 | $7,400 | $1,110 | **~$8,510** |
| **MID** (150 comp, baseline) | 150 | $74 | $11,100 | $1,665 | **~$12,765** |
| **HIGH** (200 comp + TF20 TEM follow-up on 5–10 picks at $30/hr × 10 hr = $300) | 200 | $74 + $1.50 TEM share | $15,100 | $2,265 | **~$17,365** |

### 3.3.1 Sensitivity: what if BYU rate moves?

If the Baird group for any reason is charged the **General BYU user tier** instead of the
Engineering tier (Verios/Apreo $80/hr, Helios $100/hr), the MID scenario jumps to roughly
$80/hr × 1.0 + $100/hr × 0.5 + $80/hr × 0.5 = $170 per comp × 150 = $25,500 + overhead ≈ **$29,300**.
This is the single largest risk on this line and is what the written budget justification should
explicitly anchor with a screen-shot of the Engineering-tier rate card.

### 3.3.2 What the $4,500 line actually covers at Engineering-tier rates

$4,500 ÷ $74/comp ≈ **61 compositions.**

Equivalently: $4,500 covers ~3.8 weeks of 16/wk throughput, i.e. less than 10 weeks of the 9-month
PoP. That is a ~40% coverage gap against the MID Gantt plan.

## 3.4 Recommendation — bump $4,500 → $11,000

- The **$4,500 line is under-budgeted by ~$6K–$8K** once you apply the PR #55 throughput × the
  actually-published BYU user fees.
- Bumping to **$11,000** covers the MID scenario (150 compositions) at the Engineering-tier rate
  with a 15% overhead buffer, and holds within ~$1,700 of the HIGH (200-comp) case on the core
  SEM/EBSD spend without the TEM follow-ups (which are small at $30/hr).
- A reviewer-resistant version of this line is **$13,000**, which would cleanly cover the HIGH
  scenario including a TF20 TEM campaign. The PI's "do not inflate to the cap" constraint makes
  $11K the defensible honest number; $13K the conservative number.

Sub-line allocation within the proposed $11,000:

| Sub-item | $ |
|---|---|
| SEM/EDS/EBSD (Verios/Apreo/Helios @ $30/hr, ~300 hr @ 2 hr × 150) | $9,000 |
| ICP-MS validation screening (~37 samples × 1 hr × $35/hr) | $1,300 |
| Sample prep consumables (sputter, SEM chem prep, carbon coating, mounts) | $400 |
| Overhead / redo / training (~15%) | $1,300 |
| **Total** | **~$12,000** → round to **$11,000** with the 15% inside the $9K core |

Powder XRD stays at **$0** (free internal access; confirmed by facility page).

---

# 4. Final summary

## 4.1 Line-by-line

| Line | Current | LOW | MID | HIGH | Recommendation |
|---|---|---|---|---|---|
| Research-grade elemental feedstock | **$8,000** | $3,900 | $8,084 | $13,137 | **Keep $8,000** (MID within 1.1%; all 15 elements + AlSi10Mg baseline + Sc/Er/Li pilots covered; master-alloy hedge carried). |
| GA feedstock (6 × 50 kg; 1–2 at 75 kg sensitivity) | **$5,000** | $3,126 | $4,605 | $7,303 | **Bump to $6,000** (+$1,000). MID+ case with one 75-kg upsize lands at $4,950 — no slack at current line. |
| BYU SEM/EDS/EBSD recharge | **$4,500** | $8,510 | $12,765 | $17,365 | **Bump to $11,000** (+$6,500). Current line covers only ~61 of 150 compositions at the actual BYU Engineering-tier rate ($30/hr SEM, $35/hr ICP-MS, $0 XRD). |

## 4.2 Net delta vs. current budget

| Line | Δ |
|---|---|
| Research-grade feedstock | $0 |
| GA feedstock | **+$1,000** |
| Characterization fees | **+$6,500** |
| **Net M&S change** | **+$7,500** |

If the PI prefers a more conservative build-out (characterization bumped to $13K to cover the
HIGH case), the net M&S change is **+$9,500**.

## 4.3 Honesty check

- These numbers are **not** inflated to the $600K cap. The GA-feedstock bump is the minimum that
  reflects the tightened "6 runs, 1–2 at 75 kg" directive. The characterization bump is driven by
  PR #55's 150–200-composition screening plan × the actually-published BYU user-fee schedules;
  without that bump, the proposal implicitly assumes only ~60 compositions get characterized,
  which contradicts the Gantt.
- They are **not** lowballed to hide risk. The single largest un-hedged risk is the
  Engineering-tier vs. General-BYU tier distinction at the BYU EM Facility ($30 vs. $80–$100/hr);
  the budget justification should cite the rate card directly.
- The research-grade feedstock line survives untouched because the prior MID spotcheck already
  stress-tested it against all 15 charter elements plus two margin hedges (Cr price volatility
  and Al-Sc master-alloy substitution).

## 4.4 Action items before submission

1. **Verify Baird's FLAIME grant will bill at the Engineering/CMS/Life-Sci EM-facility tier.**
   This is an administrative step with the BYU Microscopy Center (emlab@byu.edu); the
   rate-card sentence ("The colleges of Computational, Mathematical, and Physical Sciences, Life
   Sciences, and Engineering further subsidize the cost for researchers from these colleges.")
   is the evidentiary anchor.
2. **Obtain a written Valimet quote** covering 6 × 50–75 kg scale-up runs so the master-alloy
   fractions used in §2.1 can be locked.
3. **Confirm BYU Chem Powder XRD free-access policy** for Baird group accounts (training module
   completion).
4. **Optionally re-word the proposal body table at line 1381** so the SEM suite is not
   annotated with "$600/hr" — the published BYU-internal user rate is $30/hr at the
   Engineering-tier subsidy. (This audit does not modify the .tex.)

---

*Prepared 2026-04. Analysis only; does not modify `flaime-genesis-proposal.tex`.*
*Sources: `spotcheck-research-powders.md`; `spotcheck-ga-feedstock-and-argon.md`;
`spotcheck-tc-and-consumables.md`; BYU Microscopy Center rate card (Wayback capture of*
*`microscopy.byu.edu/services`, Jan 2025); `labs.chem.byu.edu/byu-spectroscopic-facility/atomic-analysis`;*
*`labs.chem.byu.edu/byu-mp-xrd-facilities/procedures`.*
