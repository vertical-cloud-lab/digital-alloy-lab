> **SUPERSEDED 2026-04-21**: This analysis used the earlier \$42K liquid-Ar-dewar basis. Current proposal Ar line is \$10,000, derived per the AMAZEMET *rePOWDER Induction Facility Guide* (2025, §6.2) at 417 L purge + ∼600 L active-atomization blanket ≈ 1,000 L/run × 350 runs ≈ 350 m³ gas ≈ 48 K-size cylinder exchanges × \$150 + \$1,800 rental (2 cyl × 9 mo) + \$1,000 regulators/contingency. Feedstock line reduced \$40K→\$36K to offset; M&S total unchanged at \$112,468. See `genesis-mission-proposal/flaime-genesis-proposal.tex` §(E) for current narrative.

# Argon (Ar) Consumable Cost Analysis — FLAIME Genesis Mission Phase I
**Prepared for:** M&S budget sub-line "Inert gas (Ar) for atomization and inert handling"  
**Period:** 9 months, Jul 1 2026 – Mar 31 2027 (~39 weeks)  
**Site:** BYU (AMAZEMET rePOWDER atomizer, inert powder handling, glovebox); **not** U. Utah LPBF (covered under U. Utah facility rates)  
**File location note:** Written to project-relative path (`genesis-mission-proposal/fleet-budget/`) because `/tmp` is prohibited in this environment; intended content matches the `/tmp/fleet-budget/argon-analysis.md` request.

---

## 1. Assumptions & Usage Basis

| Parameter | Value | Basis |
|---|---|---|
| Phase I duration | 39 weeks ≈ 9 months | FOA schedule Jul 2026–Mar 2027 |
| Ar consumption rate | ~2 T-cylinders/week average | PI estimate; ~1–3 cylinders/atomization run, ~1–2 runs/week during active campaign; + glovebox topping/transfers |
| T-cylinder (UHP 300 cf) capacity | 300 SCF (~335 cf for Airgas "300 DS") | Airgas product spec |
| Total cylinder-equivalents | **78 refills** | 2/wk × 39 wks |
| Total SCF needed | **23,400 SCF** | 78 × 300 SCF |
| Purity requirement | UHP Ar, ≥99.999% | Required for reactive Al alloy atomization and inert handling |
| rePOWDER gas design | Recirculating inert atmosphere + chamber purge | AMAZEMET system uses recirculation, reducing per-run consumption vs. open-flow atomizers; purge cycles still consume ~0.5–1.5 cylinders per run for initial chamber evacuation/backfill with reactive materials |

---

## 2. Market Pricing Data (2024–2025)

### 2a. High-Pressure UHP Argon — T/K Cylinders (~278–335 cf)

| Source | Price/refill | Notes |
|---|---|---|
| **UNLV–Airgas state contract** (2024) | **$44.38** | UHP 335 cf T-cylinder; competitive state consortium rate [1] |
| **Baylor–Linde order form** (Jan 2024) | **$168–$173** | UHP K-cylinder (278 cf); non-consortium academic account [2] |
| **Typical blended academic range** | **$60–$175** | Span across Airgas/Linde university accounts; rate depends on whether institution holds a state/consortium contract |
| HighPrecisionGas.com (list price) | ~$0.111/SCF | Implies ~$33/T-cylinder at 300 SCF; list pricing, not necessarily delivered [3] |

**Cylinder rental fees (separate from gas cost):**
- Airgas (UIUC 2024): $0.0967/day ≈ $2.90/month per high-pressure cylinder [4]
- Northwestern (Airgas): ~$3.50/month per cylinder [5]
- Rice (Airgas): ~$13/month per cylinder [6]
- MIT/Linde transition: all-inclusive pricing (no separate rental) [7]
- Assumed for this analysis: ~$5/month per cylinder held on-site × 3 cylinders average = ~$135 total rental over 9 months

**Delivery fees:** ~$25–$60 per delivery; assuming biweekly delivery = 26 trips

### 2b. Liquid Argon Dewar Option (160 L Dewar, ~4,752 SCF equivalent)

| Source | Price/dewar | $/SCF |
|---|---|---|
| **UNLV–Airgas state contract** (bulk, 2024) | **$261.47** | **$0.047–0.055/SCF** [1] |
| AllTex Welding Supply (bulk market) | $1.60–2.00/L liquid | $0.054–0.067/SCF [8] |
| JH-Gas / industry average | $0.50–2.00/m³ gas | $0.014–0.057/SCF [9] |

**SCF conversion:** 1 L liquid Ar → 841 L gas → 29.7 SCF; 160 L dewar ≈ 4,752 SCF  
**Dewars needed:** 23,400 SCF ÷ 4,752 SCF/dewar = **4.9 → ~5 dewar deliveries**

> **Note:** Dewar delivery requires cryogenic dewar ownership or rental. BYU may already own a dewar through the Chemistry Dept. (BYU Chem Stores, 126 NICB, 801-422-2678). If renting: ~$30–60/month for the dewar vessel itself.

---

## 3. Three-Scenario Cost Estimates

### Scenario A — LOW (~$2,000)
**Approach:** Exclusively liquid Ar dewar deliveries; BYU leverages a Utah state/consortium contract similar to UNLV–Airgas rate; BYU owns or already rents a cryogenic dewar.

| Line item | Qty | Unit cost | Subtotal |
|---|---|---|---|
| Liquid Ar (160 L dewars, 5 deliveries) | 5 | $261 | $1,305 |
| Delivery/hazmat fee | 5 | $55 | $275 |
| Cylinder/dewar vessel rental | 9 months | ~$35/mo | $315 |
| **Total LOW** | | | **~$1,900** |

*Rounded to: **$2,000***

> Requires: (a) BYU state contract pricing, (b) on-site dewar vessel available, (c) liquid Ar compatible with glovebox feed system.

---

### Scenario B — LIKELY (~$8,000)
**Approach:** Mixed high-pressure UHP T-cylinders under a BYU/UT state academic contract, biweekly delivery. Assumes blended rate of ~$90/refill (between UNLV-Airgas $44 and Baylor-Linde $168), reflecting a mid-tier university procurement contract.

| Line item | Qty | Unit cost | Subtotal |
|---|---|---|---|
| UHP Ar T-cylinder refills (78 total) | 78 | $90 | $7,020 |
| Cylinder rental (3 on-site × 9 mo) | 27 cyl-months | $5/mo | $135 |
| Delivery fees (biweekly, 26 trips) | 26 | $30 | $780 |
| **Total LIKELY** | | | **~$7,935** |

*Rounded to: **$8,000***

> This is the recommended budget figure. BYU has state procurement infrastructure; a $90/cylinder blended rate is realistic and defensible. If BYU's actual contract is closer to the UNLV $44 rate (possible under a Western States university purchasing agreement), the true cost may be $4,000–5,000.

---

### Scenario C — UPPER (~$16,000)
**Approach:** Ad-hoc purchasing without a consortium contract; fully contracted via Linde/Praxair at ~$170/cylinder (Baylor 2024 list rate); additional premium for hazmat/delivery and higher rental rates.

| Line item | Qty | Unit cost | Subtotal |
|---|---|---|---|
| UHP Ar T-cylinder refills (78 total) | 78 | $170 | $13,260 |
| Cylinder rental (3 on-site × 9 mo) | 27 cyl-months | $13/mo | $351 |
| Delivery fees (biweekly, 26 trips) | 26 | $55 | $1,430 |
| **Total UPPER** | | | **~$15,041** |

*Rounded to: **$15,000***

---

## 4. Summary of Scenarios

| Scenario | Total (9 mo) | $/cylinder-equiv. |
|---|---|---|
| LOW (liquid dewar, state contract) | ~$2,000 | ~$26 |
| **LIKELY (mixed cylinders, university contract)** | **~$8,000** | **~$103** |
| UPPER (ad-hoc, no contract) | ~$15,000 | ~$192 |

---

## 5. Institutional vs. Direct-Charge Treatment (2 CFR 200)

**Regulatory basis:**
- **2 CFR 200.413** — Direct costs are those identifiable with a specific award; inert gases used exclusively for the funded project work are **allowable as direct costs**.
- **2 CFR 200.94** — Supplies (including consumable gases) are defined as tangible personal property with a useful life <1 year or <$5,000/unit; gases clearly fall in this category.
- Argon cylinders used for atomization runs and inert powder handling on FLAIME work should be **charged directly** to the award, since consumption is project-specific and can be documented by run logs.

**BYU facility recharge center note:**
- BYU Chem Stores (126 NICB) does supply compressed gases via departmental recharge. If ordered through Chem Stores at a negotiated rate and recharged to the grant, the cost structure is the same (direct supply cost to grant) but billing flows through the internal recharge system.
- Under 2 CFR 200.468, recharge/service center costs are allowable if rates are set to recover actual costs (not profit). BYU's chemistry recharge prices are typically set at or slightly below Airgas contract rates.
- **No portion is expected to be absorbed by F&A overhead** for this type of consumable, since Ar is project-specific and not a general departmental supply. It would be included in the MTDC base for indirect cost calculation.

---

## 6. Recommendation

**Budget $8,000 for "Inert gas (Ar) for atomization and inert handling" over Phase I (9 months).**

Justification language for proposal:
> "Argon (UHP, ≥99.999%) is consumed as a melt-chamber purge and inert-atmosphere medium during AMAZEMET rePOWDER atomization runs (~1–3 cylinders/run), Al powder transfer/handling, and glovebox maintenance at BYU. Estimated consumption is approximately 2 T-cylinders/week over 39 weeks (78 refills, 23,400 SCF). At a BYU/UT university contract rate of ~$90/refill plus delivery, this totals approximately **$8,000** for the Phase I period. U. Utah LPBF Ar consumption is not included here; it is covered within U. Utah facility service fees."

---

## 7. Citations

| # | Source | URL |
|---|---|---|
| [1] | UNLV–Airgas Contract Pricing Sheet (2024, incl. UHP 335cf @ $44.38 & LC160 @ $261.47) | https://www.unlv.edu/sites/default/files/32/6238-PRICING.pdf |
| [2] | Baylor University–Linde Order Form (Jan 2024, UHP K-cyl @ ~$168) | https://bsb.research.baylor.edu/sites/g/files/ecbvkj1151/files/2024-06/Linde%20Order%20Form%201.1.24.pdf |
| [3] | HighPrecisionGas.com UHP Ar listing (2024) | https://highprecisiongas.com/products/argon-ar-gaseous |
| [4] | UIUC New Airgas Contract announcement (Oct 2024, daily rental rates) | https://blogs.illinois.edu/view/9081/680666589 |
| [5] | Northwestern University Lab Gases & Dry Ice procurement page | https://www.northwestern.edu/procurement/source-purchase/preferred-vendors/internal-billing/lab-gases-dry-ice.html |
| [6] | Rice University Chemistry compressed gas orders | https://chemistry.rice.edu/compressed-gas-orders |
| [7] | MIT VPF – cost of keeping Airgas cylinders; Linde transition | https://vpf.mit.edu/sites/default/files/downloads/Cost%20of%20Keeping%20Airgas%20Cylinders.pdf |
| [8] | AllTex Welding Supply – bulk argon cost | https://alltexweld.com/argon-bulk-cost/ |
| [9] | JH-Gas – Understanding Liquid Argon Price | https://jh-gas.com/liquid-argon-price/ |
| [10] | 2 CFR 200.413 Direct Costs | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFR118e2fa1c6d875e/section-200.413 |
| [11] | 2 CFR 200.94 Supplies definition | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-A/subject-group-ECFR118e2fa1c6d8744/section-200.94 |
| [12] | AMAZEMET rePOWDER at CHiMaD (Northwestern) — recirculating Ar atmosphere confirmed | https://cmpf.northwestern.edu/equipment/amazemet-repowder-ultrasonic-atomizer-2/ |
| [13] | BYU Chem Stores — internal gas supply & recharge center | https://chem.byu.edu/fs-dashboard/chem-stores/ |

---

*Analysis prepared: 2025. All prices in USD. Do not modify proposal budget tables based solely on this document; confirm current BYU procurement contract rates before finalizing.*
