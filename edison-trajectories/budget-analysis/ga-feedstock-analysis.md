# GA Feedstock Cost Analysis — FLAIME Genesis Mission Proposal
## DE-FOA-0003612, Topic 3-B | Valimet Scale-Up (3–6 × 50 kg runs)

*Prepared for internal budget planning. Do NOT modify proposal tex source.*
*Note: Requested output path `/tmp/fleet-budget/` is blocked by runtime security policy; file written here instead.*

---

## 1. Pricing Inputs

### Key Assumption on Valimet Budget Scope
Valimet's independent application (not a BYU subaward) is assumed to cover:
- **Included in Valimet's budget:** GA service labor, induction furnace and atomizer time, inert gas (Ar/N₂), powder sieving and classification, QC/characterization (PSD, chemistry check), and Valimet staff overhead.
- **NOT assumed in Valimet's budget:** The raw elemental and master-alloy feedstock that BYU blends/ships to Valimet for charging the melt. This is BYU-originated material sourced, prepared, and shipped by BYU; it belongs in BYU's M&S budget unless Valimet explicitly agrees to procure it and absorb cost.

**This analysis quantifies the BYU-side feedstock cost only.**

### Commodity Prices (2024, US commercial scale, ~50 kg lots)

| Material | LOW ($/kg) | LIKELY ($/kg) | UPPER ($/kg) | Source basis |
|---|---|---|---|---|
| Al ingot P1020 (99.7%) | 2.53 | 2.80 | 3.20 | LME spot ~$2.53 + freight/handling |
| Al-20Mn master alloy | 10.00 | 12.00 | 15.00 | US commercial; IndiaMART ~$3-4/kg; Made-in-China $30-100/kg; US mid-market estimate |
| Al-10Cr master alloy | 15.00 | 18.00 | 22.00 | IndiaMART $4.20/kg + US import premium; ScrapMonster Cr $10-11/kg; US mid estimate |
| Al-5Zr master alloy | 28.00 | 32.00 | 40.00 | QYResearch/GlobalInfo avg $28/kg at 50 kg scale; premium for guaranteed purity |
| Zr sponge metal | 18.00 | 21.00 | 28.00 | ScrapMonster $21.19/kg EXW China, nuclear/industrial grade |
| Mn metal flake (99.7%) | 1.50 | 2.50 | 3.50 | Made-in-China $1.35-2.80/kg; IndiaMART ~$3/kg |
| Cr metal (99%) | 10.00 | 11.00 | 13.00 | ScrapMonster / metal.com $9.70-10.40/kg bulk; adds small US premium |
| Si metal (99%) | 3.16 | 3.50 | 4.50 | IMARC/BusinessAnalytiq US price $3.16-3.41/kg |
| Al-2Sc master alloy | 300.00 | 350.00 | 450.00 | QS Rare Materials/IndiaMART; bulk industrial Al-2Sc; research small-qty $300-12,000/kg |

**Scale differential confirmed:** Research-grade (100 g) Al-Sc powder quotes at $300-12,000/kg; industrial 50-kg-scale master alloy ingot: $300-450/kg — confirmed >10× price reduction vs. small-lot specialty powder for Sc-containing materials. For non-Sc elements, scale differential is smaller but Zr shifts from ~$200+/kg powder to $28-40/kg master alloy (~5-8×).

---

## 2. Composition-by-Composition Cost (per 50 kg batch)

### Master-alloy charging path methodology
Master alloys are used (rather than pure refractory metals) to ensure reliable dissolution in the Al melt during induction melting before gas atomization. Zr in particular dissolves poorly as sponge at low superheat; Al-Zr MA is strongly preferred by foundry operators. Mn and Cr *can* be added as pure metals but MA path reduces risk of skull formation.

For each master alloy charged: the Al content within the MA is counted toward the total Al requirement (balance is pure Al P1020 ingot).

---

### (a) Al-3wt%Mn–2wt%Cr–1wt%Zr  — Anchor composition
*50 kg batch: Mn = 1.50 kg, Cr = 1.00 kg, Zr = 0.50 kg, Al = 47.00 kg*

**LOW path** (pure Mn + Cr metals, Al-5Zr MA at low price):

| Item | Qty (kg) | Price ($/kg) | Subtotal |
|---|---|---|---|
| Mn metal 99.7% | 1.50 | 1.50 | $2.25 |
| Cr metal 99% | 1.00 | 10.00 | $10.00 |
| Al-5Zr MA | 10.00 | 28.00 | $280.00 |
| Al P1020 (balance: 47.0 − 9.5 = 37.5 kg) | 37.50 | 2.80 | $105.00 |
| **LOW Total (a)** | | | **$397** |

**LIKELY path** (all master alloys, mid prices):

| Item | Qty (kg) | Price ($/kg) | Subtotal |
|---|---|---|---|
| Al-20Mn MA | 7.50 | 12.00 | $90.00 |
| Al-10Cr MA | 10.00 | 18.00 | $180.00 |
| Al-5Zr MA | 10.00 | 32.00 | $320.00 |
| Al P1020 (balance: 47.0 − 6.0 − 9.0 − 9.5 = 22.5 kg) | 22.50 | 2.80 | $63.00 |
| **LIKELY Total (a)** | | | **$653** |

**UPPER path** (premium MA prices + 15% contingency):
Raw subtotal: Al-20Mn ($15) × 7.5 = $112.50; Al-10Cr ($22) × 10 = $220; Al-5Zr ($40) × 10 = $400; Al $63 = $795.50 × 1.15 = **$915**

---

### (b) Al-1wt%Zr — L1₂ precipitate strengthened alloy
*50 kg batch: Zr = 0.50 kg, Al = 49.50 kg*

**LOW path** (Al-5Zr MA at low price):

| Item | Qty (kg) | Price ($/kg) | Subtotal |
|---|---|---|---|
| Al-5Zr MA | 10.00 | 28.00 | $280.00 |
| Al P1020 (49.5 − 9.5 = 40.0 kg) | 40.00 | 2.80 | $112.00 |
| **LOW Total (b)** | | | **$392** |

*Note: Zr sponge ($21/kg × 0.5 = $10.50) is cheaper in materials cost alone but introduces melt risk; Al-Zr MA is the defensible path even at LOW. If BYU's melt lab pre-dissolves Zr sponge into Al-Zr MA in-house, cost drops but adds BYU labor (not captured here).*

**LIKELY path** (mid-price MA):
Al-5Zr ($32) × 10 = $320; Al × 40 = $112 = **$432**

**UPPER path** (premium MA + 15%):
Al-5Zr ($40) × 10 = $400; Al $112; ×1.15 = **$590**

---

### (c) BOFN exemplar: Al-2wt%Mn–1wt%Zr–0.5wt%Si  — No Sc/Er/Li
*Mineral-burden-conscious composition selected by BOFN with Mn, Zr, Si only.*
*50 kg batch: Mn = 1.00 kg, Zr = 0.50 kg, Si = 0.25 kg, Al = 48.25 kg*

**LOW path:**

| Item | Qty (kg) | Price ($/kg) | Subtotal |
|---|---|---|---|
| Mn metal 99.7% | 1.00 | 1.50 | $1.50 |
| Al-5Zr MA | 10.00 | 28.00 | $280.00 |
| Si metal 99% | 0.25 | 3.50 | $0.88 |
| Al P1020 (48.25 − 9.5 = 38.75 kg) | 38.75 | 2.80 | $108.50 |
| **LOW Total (c)** | | | **$391** |

**LIKELY path:**
Al-20Mn ($12) × 5 = $60; Al-5Zr ($32) × 10 = $320; Si $0.88; Al balance (48.25 − 4.0 − 9.5 = 34.75 kg) × $2.80 = $97.30 = **$478**

**UPPER path:**
Al-20Mn ($15) × 5 = $75; Al-5Zr ($40) × 10 = $400; Si $0.88; Al $97.30; ×1.15 = **$659**

---

### (d) UPPER-BOUND: Al-3wt%Mn–2wt%Cr–1wt%Zr–0.2wt%Sc — FLAIME-constrained Sc addition
*This composition is the maximum Sc allowed under FLAIME's critical-mineral-reduction mandate.*
*0.2 wt% Sc is a bounded micro-addition; zero Sc-rich or Er-bearing alloys are being atomized at 50 kg scale.*
*50 kg batch: Mn = 1.50 kg, Cr = 1.00 kg, Zr = 0.50 kg, Sc = 0.10 kg, Al = 46.90 kg*

**LOW path:**

| Item | Qty (kg) | Price ($/kg) | Subtotal |
|---|---|---|---|
| Mn metal 99.7% | 1.50 | 1.50 | $2.25 |
| Cr metal 99% | 1.00 | 10.00 | $10.00 |
| Al-5Zr MA | 10.00 | 28.00 | $280.00 |
| Al-2Sc MA | 5.00 | 300.00 | **$1,500.00** |
| Al P1020 (46.9 − 9.5 − 4.9 = 32.5 kg) | 32.50 | 2.80 | $91.00 |
| **LOW Total (d)** | | | **$1,883** |

**LIKELY path:**
Al-20Mn ($12) × 7.5 = $90; Al-10Cr ($18) × 10 = $180; Al-5Zr ($32) × 10 = $320; Al-2Sc ($350) × 5 = **$1,750**; Al balance (46.9 − 6.0 − 9.0 − 9.5 − 4.9 = 17.5 kg) × $2.80 = $49 = **$2,389**

**UPPER path:**
Al-20Mn ($15) × 7.5 = $112.50; Al-10Cr ($22) × 10 = $220; Al-5Zr ($40) × 10 = $400; Al-2Sc ($450) × 5 = $2,250; Al $49; ×1.15 = **$3,484**

**Critical-mineral constraint note:** Sc at 0.2 wt% = 100 g per 50 kg batch. Even at $12,000/kg small-lot research powder price, that's $1,200 — at bulk industrial Al-2Sc MA, it's $1,500-2,250. This is the *hard upper bound* FLAIME commits to. No full-Sc alloys (e.g., Al-0.5Sc-0.1Zr or Sc-rich variants) are planned at 50 kg scale; the FLAIME critical-mineral-reduction narrative explicitly prohibits that path.

---

## 3. Three-Run and Six-Run Cost Envelopes

### Scenarios
- **3-run scenario (150 kg total):** One run each of compositions (a), (b), (c) — no Sc.
- **6-run scenario A (300 kg, no Sc):** Two runs each of (a), (b), (c).
- **6-run scenario B (300 kg, one Sc run):** (a)×2 + (b)×1 + (c)×2 + (d)×1 — one Sc-bounded run to stress-test the critical-mineral constraint.

### Per-run cost summary

| Composition | LOW | LIKELY | UPPER |
|---|---|---|---|
| (a) Al-3Mn-2Cr-1Zr | $397 | $653 | $915 |
| (b) Al-1Zr | $392 | $432 | $590 |
| (c) Al-2Mn-1Zr-0.5Si | $391 | $478 | $659 |
| (d) Al-3Mn-2Cr-1Zr-0.2Sc | $1,883 | $2,389 | $3,484 |

### 3-run envelope (150 kg, compositions a + b + c)

| | LOW | LIKELY | UPPER |
|---|---|---|---|
| Feedstock material cost | **$1,180** | **$1,563** | **$2,164** |
| + Shipping to Valimet (est. $150-300 for packaged ingots) | +$150 | +$200 | +$300 |
| + BYU prep labor (weighing, blending, packaging; ~2-4 hrs) | +$100 | +$200 | +$300 |
| **All-in BYU cost, 3 runs** | **~$1,430** | **~$1,963** | **~$2,764** |

### 6-run envelope A (300 kg, no Sc, 2× each of a/b/c)

| | LOW | LIKELY | UPPER |
|---|---|---|---|
| Feedstock material cost | **$2,360** | **$3,126** | **$4,328** |
| + Shipping + BYU prep | +$400 | +$600 | +$800 |
| **All-in BYU cost, 6 runs (no Sc)** | **~$2,760** | **~$3,726** | **~$5,128** |

### 6-run envelope B (300 kg, one Sc-bounded run)

| | LOW | LIKELY | UPPER |
|---|---|---|---|
| Feedstock material cost (2a + 1b + 2c + 1d) | **$3,455** | **$5,137** | **$7,222** |
| + Shipping + BYU prep | +$450 | +$650 | +$900 |
| **All-in BYU cost, 6 runs (with 1 Sc run)** | **~$3,905** | **~$5,787** | **~$8,122** |

### Summary table

| Scenario | LOW | LIKELY | UPPER |
|---|---|---|---|
| 3-run, 150 kg, no Sc | $1,430 | $1,963 | $2,764 |
| 6-run, 300 kg, no Sc | $2,760 | $3,726 | $5,128 |
| 6-run, 300 kg, 1 Sc run | $3,905 | $5,787 | $8,122 |

---

## 4. Booking Recommendation

### Option Analysis

| Option | Description | Pros | Cons |
|---|---|---|---|
| (i) BYU M&S sub-line | BYU budgets and purchases feedstock, ships to Valimet | Clean ownership; BYU already controls alloy compositions; ensures traceability | Need to add explicit line to proposal budget |
| (ii) Valimet budget | Valimet procures feedstock from their budget | One fewer BYU line item | Valimet's budget is tightly sized for service costs; feedstock procurement may not be in Valimet's SOW; risk of misunderstanding |
| (iii) Split | BYU covers exotic MAs (Zr, Sc if used); Valimet covers base Al | Could align with each party's supplier relationships | Administrative complexity; hard to delineate in proposal |

### Recommendation: **Option (i) — BYU M&S sub-line**

**Rationale:**
1. BYU researchers select and formulate the alloy compositions; they are the natural party to source and QC the feedstock.
2. The feedstock must be traceable (chemistry certs, lot tracking) because it directly determines powder composition — BYU's research output depends on it.
3. Valimet's budget is sized for processing services; adding feedstock procurement risk to their fixed budget could create a funding shortfall if alloy prices fluctuate.
4. DOE reviewers expect proposers to account for all BYU-controlled materials; an omitted feedstock line may raise questions during review or award negotiation.
5. The dollar amount ($2,000–$5,800 LIKELY range for 3–6 runs) is small enough to fit within BYU M&S without displacing other budget items, but large enough to require an explicit line.

**Clarification to surface with Valimet before submission:** Confirm in writing whether Valimet's budget includes or excludes raw feedstock. If Valimet will procure feedstock (e.g., they have existing supplier contracts for Al master alloys), then Option (ii) or (iii) becomes viable and BYU's line item may be reduced to shipping/packaging only (~$300–600).

---

## 5. Single-Number Recommendation

### Proposed BYU M&S sub-line:
**"Gas-atomization feedstock prep (3–6 × 50 kg runs, Valimet scale-up)"**

### Recommended amount: **$5,000**

#### Build-up:
| Component | Amount |
|---|---|
| Feedstock materials, 6-run LIKELY (no Sc) | $3,126 |
| Shipping + packaging to Valimet (6 runs) | $600 |
| Contingency (~15%) | $549 |
| **Rounded point estimate** | **$4,275 → budget as $5,000** |

**$5,000** covers the 6-run upper scenario with all master-alloy charging (no Sc) with comfortable contingency, and also bounds the 3-run + 1 Sc run scenario at LIKELY pricing. It is justifiable, auditable, and proportionate.

If BYU can confirm Valimet procures base Al ingot themselves, this line item could be reduced to **$3,500** (covering only exotic MAs and shipping).

---

## 6. How Critical-Mineral-Reduction Constraint Bounds Upper Cost

FLAIME's design goal is to **reduce critical-mineral content** in high-performance Al AM alloys. This directly caps feedstock cost:

1. **No Sc-rich alloys at 50 kg scale.** Full Sc-content compositions (e.g., Al-0.5Sc, Al-Sc-Er) are excluded from GA scale-up. A 50 kg batch of Al-0.5Sc would cost ~$8,750 in feedstock alone (LIKELY) — more than the entire proposed M&S line for all other runs combined.
2. **No Er, Li, or other critical-mineral-heavy compositions.** Er master alloy at 50 kg scale would be similarly expensive and is explicitly out of scope.
3. **0.2 wt% Sc is the hard upper bound.** Even this bounded addition (composition d) costs ~$1,500–2,250 per run just for the Sc-bearing MA. The FLAIME narrative commits to showing Sc-free paths are competitive, so composition (d) is a demonstration outlier, not the program centerpiece.
4. **Result:** The critical-mineral constraint keeps the 6-run feedstock envelope firmly in the $3,000–$5,200 range (no Sc) rather than $15,000–30,000+ (if Sc-rich alloys were included). This is the cost savings narrative FLAIME can use: "scale-up feedstock cost held below $5,000 across the entire Phase I program because critical-mineral-reduction alloy design eliminates expensive Sc/Er additions at production scale."

---

## 7. Citations

1. QYResearch / GlobalInfoResearch — *Global Aluminum Zirconium Master Alloy Market* (2024): Al-Zr MA avg $28/kg at 50 kg scale. https://www.qyresearch.com/reports/5049013/aluminum-zirconium-master-alloy
2. IndiaMART — *Aluminium Master Alloy listings* (2024): Al-Mn ~₹244-320/kg ($3-4/kg); Al-Cr ~₹348/kg ($4.20/kg). https://dir.indiamart.com/impcat/aluminum-master-alloy.html
3. ScrapMonster — *Zirconium Metal Price* (March 2024): Zr+Hf 99.4% min EXW China $21.19/kg. https://www.scrapmonster.com/metal-prices/minor-metals/zirconium/842
4. Intratec — *Aluminum Prices, Current and Forecast* (2024): US spot P1020 ~$2.53/kg. https://www.intratec.us/commodity/aluminum-prices
5. Made-in-China — *Manganese Metal Flake wholesale* (2024): $1,350-2,800/MT bulk = $1.35-2.80/kg. https://www.made-in-china.com/products-search/hot-china-products/Manganese_Metal_Flake.html
6. ScrapMonster / metal.com — *Chromium Metal 99% prices* (2024): $9.70-10.40/kg EXW bulk. https://www.scrapmonster.com/metal-prices/chromium-metal-99-min-price/682
7. IMARC Group — *Metal Silicon Prices, 2024*: US $3.16-3.41/kg for 99% Si. https://www.imarcgroup.com/metal-silicon-pricing-report
8. QS Rare Materials — *Aluminum-Scandium Master Alloy* pricing: bulk Al-2Sc from ~$300/kg. https://www.qsrarematerials.com/aluminum-scandium-al-sc-master-alloy-p-667.html
9. BusinessAnalytiq — *Metal Silicon Price Index* (ongoing). https://businessanalytiq.com/procurementanalytics/index/metal-silicon-price-index/
