# Gas Atomization Scale-Up Validation Plan

*FLAIME Phase I — Node 4 Integration into BOFN DAG*
*Generated 2026-04-05 | Edison task `0e34f629` (LITERATURE_HIGH)*

---

## 1. Motivation

FLAIME discovers alloys via ultrasonic atomization (UA, AMAZEMET rePOWDER, 1–5 kg batches). Industry-scale AM feedstock is gas-atomized (GA). **No published UA→GA transfer functions exist for Al alloys** — this gap is both a risk and a publishable contribution. A targeted GA validation of 3–5 top compositions bridges TRL 2–3 (lab discovery) → TRL 4–5 (process validation) within Phase I.

---

## 2. UA → GA Transfer: What We Know

### 2.1 Property-by-Property Summary

| Property | UA Advantage | GA Risk on Transfer | Prediction Quality |
|---|---|---|---|
| PSD (15–63 µm yield) | 40–75% in-spec (Yankin 2025, Ge 2025) | GA yield often 30–50%; different breakup physics | Directional only — must re-optimize |
| Sphericity | High (few satellites) (Yankin 2025) | Satellites increase with GA plume interactions | Not predictive — must measure |
| Flowability | 22–45% better compressibility/SE vs commercial GA (Yankin 2025) | Fines + satellites can degrade | Not predictive — must run Hall/Carney |
| Chemistry | Preserves well at lab scale | Volatile loss (Mg, Zn, Mn) differs; oxide pickup varies | Qualitative only |
| Solidification rate | ~10³–10⁴ K/s | GA ~10⁴–10⁵ K/s (size-dependent, CR ∝ d⁻¹·⁸⁶) | Phase selection may shift — XRD required |
| Internal porosity | Typically dense | Argon entrapment creates closed pores in GA | Not predictive — cross-section SEM required |

### 2.2 Key Transfer Risks

1. **Satellite formation** → degrades flowability and layer spreading
2. **Cooling-rate mismatch** → different solute trapping, phase constitution (critical for Al-Ce, Al-Cu metastable phases)
3. **Oxide film thickness** → different laser absorption and pore nucleation
4. **Gas porosity** → trapped Ar inheritable through LPBF melt pool
5. **Volatile element loss** → composition drift for Mg/Zn/Mn-bearing alloys

### 2.3 Literature Gap = Publication Opportunity

Direct UA vs GA comparison for the same Al alloy composition printed via LPBF is **essentially unpublished**. Żrodowski et al. (2021) compared UA vs GA 316L steel; Monti et al. (2023) developed Al-Cu via UA. A systematic UA→GA→LPBF transfer study for 3–5 Al alloy compositions would be a first-of-kind contribution.

---

## 3. BOFN DAG Integration: Node 4–6 Design

### 3.1 Extended DAG Architecture

```
Node 0: CALPHAD Screening (~$1/comp, minutes)
  ↓ [BOFN promotes]
Node 1: Ultrasonic Atomization (~$200/comp, 0.5–2 days)
  ↓ [BOFN promotes]
Node 2: LPBF Printing (~$500/comp, 1–3 days)
  ↓ [BOFN promotes]
Node 3: Tensile Testing (~$300/comp, 2–5 days)
  ↓ [Top 3–5 only — sparse gate]
  ↓                                    ← Main discovery loop continues in parallel
Node 4: Gas Atomization (~$5,000–8,000/comp, 6–12 weeks)  ← NEW
  ↓
Node 5: GA-LPBF Printing (~$500–1,000/comp, 1–3 days)     ← NEW
  ↓
Node 6: GA Mechanical Testing (~$300–600/comp, 2–5 days)   ← NEW
```

### 3.2 Node Cost Summary

| Node | Cost/Composition | Turnaround | Queried For |
|------|----------------:|------------|-------------|
| 0 – CALPHAD | ~$1 | Minutes–hours | All candidates (~5,000+) |
| 1 – UA Powder | ~$200 | 0.5–2 days | ~200 compositions |
| 2 – LPBF Print | ~$500 | 1–3 days | ~200 compositions |
| 3 – Tensile | ~$300 | 2–5 days | ~200 compositions |
| **4 – GA Powder** | **$3,000–8,000** | **6–12 weeks** | **3–5 top compositions** |
| **5 – GA-LPBF** | **$500–1,000** | **1–3 days** | **3–5 compositions** |
| **6 – GA Tensile** | **$300–600** | **2–5 days** | **3–5 compositions** |

### 3.3 Decision Logic

- **Trigger**: Node 4 activated only when BOFN posterior identifies compositions with high predicted performance AND low predictive uncertainty from Nodes 0–3
- **Timing**: GA validation orders placed at Month 4–5 (after ~100+ compositions screened); powder received Month 6–8; GA-LPBF/testing Month 7–9
- **Independence**: Main UA discovery loop (Nodes 0–3) continues without blocking on GA results
- **In BOFN terms**: Heterotopic costly task sampled at ~100× lower frequency than UA tasks (per Alvi et al. 2026 deep GP framework)

### 3.4 Minimum Compositions for Statistical Confidence

- **3 compositions** (minimum): Detects systematic UA→GA biases vs composition-specific anomalies
- **5 compositions** (recommended): Enough data points for preliminary UA↔GA regression on powder/mechanical properties
- **Per composition**: n≥3 replicate powder measurements; ≥3 tensile bars per build orientation

---

## 4. GA Service Providers & Costs

### 4.1 Recommended Partners (Ranked)

| Provider | Type | Batch Size | Estimated Cost | Lead Time | Best For | Letter Potential |
|----------|------|-----------|---------------|-----------|----------|-----------------|
| **Valimet** (Stockton, CA) | Commercial | 5–50+ kg | [partner pricing removed] | 6–12 weeks | Fastest turnaround; established Al powder producer; no Genesis Mission internal deadline constraints | **HIGH** — **Letter of Collaboration** (official team member); Phase I GA service provider |
| **Ames National Lab / Iowa State** | DOE Lab + University | 4–20 kg (GARS demonstrated) | [partner pricing removed] | 8–16 weeks | World-leading GARS expertise; custom Al alloys; DOE Category 1 | **MEDIUM** — **Letter of Support** (pointing to Phase II collaboration); Ames internal Genesis Mission deadline may preclude Phase I letter of collaboration |
| **ORNL MDF** | DOE User Facility | Flexible | Varies (user proposal) | 8–16 weeks | Bundle GA + LPBF + characterization at one facility | **HIGH** — already identified as teaming target; Category 1 |
| **Carpenter Technology** | Commercial | 25+ kg minimum typical | $8,000–15,000/comp (25 kg) | 6–12 weeks | Larger validation batches | LOW — minimum batch too large for Phase I |
| **Colorado School of Mines** | University | Lab-scale | TBD (subaward) | 8–16 weeks | Academic collaboration | MEDIUM — Category 3 partner |
| **Arcast Inc.** | Commercial (lab-scale) | <1–5 kg | $3,000–5,000/comp | 4–8 weeks | Feasibility runs; smallest batches | LOW — limited scale |

### 4.2 Cost Breakdown per Composition (10 kg batch)

| Item | Cost Range |
|------|-----------|
| GA powder production (10 kg) | $3,000–8,000 |
| Powder characterization (full protocol) | $2,000–3,000 |
| GA-LPBF builds (3–5 builds) | $1,500–5,000 |
| GA mechanical testing (tensile) | $900–1,800 |
| Shipping/handling/storage | $500–1,000 |
| **Total per composition** | **$8,000–19,000** |

### 4.3 Access Mechanisms

| Provider | Mechanism | Proposal Structure |
|----------|-----------|-------------------|
| Ames Lab | Work-for-Others (WFO) or subaward through Iowa State | Subaward line item |
| ORNL MDF | User Facility proposal or CRADA | User proposal (free if accepted) or subaward |
| Valimet | Service contract with quote | Other Direct Costs — Services |
| University | Subaward in federal proposal | Subaward with SOW |

### 4.4 Information Required for GA Provider

1. Target composition (nominal wt% with tolerances)
2. Target PSD (15–63 µm for LPBF; D10/D50/D90 targets)
3. Quantity of usable powder needed (distinguish from total atomized mass)
4. Atomization gas preference (Ar recommended for Al)
5. Certification requirements (chemistry, PSD, flowability, O₂ content)
6. Feedstock form (pre-alloyed ingot or elemental charge)
7. Safety data (MSDS for any reactive elements)

---

## 5. Required Characterization: UA ↔ GA Comparison Protocol

### 5.1 Essential Tests (Minimum)

| Test | Standard | What It Reveals |
|------|----------|----------------|
| PSD (laser diffraction) | ASTM B822 / ISO 13320 | Size window shift; yield to LPBF cut |
| Morphology/Sphericity (SEM + image analysis) | ASTM F3049 (guide) | Satellites, shape change, surface roughness |
| Flowability — Hall funnel | ASTM B213 / ISO 4490 | Gross flowability degradation |
| Apparent Density | ASTM B212 / B417 | Packing behavior change |
| Tap Density | ASTM B527 | Compactability change |
| Chemical Composition (ICP-OES) | Lab-validated under ASTM F3049 | Composition drift, volatile loss |
| Oxygen/Nitrogen (inert gas fusion) | LECO ONH under ASTM F3049 | Oxide pickup difference |
| Cross-section Microstructure (SEM) | Metallographic SOP | Internal porosity, solidification structure |
| XRD Phase Analysis | Powder XRD + Rietveld | Phase constitution change (metastable retention) |

### 5.2 Recommended Additional Tests

| Test | Standard | Value-Add |
|------|----------|-----------|
| Flowability — Carney funnel | ASTM B964 | Captures borderline flow failures |
| Hausner Ratio / Carr Index | ASTM D6393 (derived) | Simple cohesion transfer metric |
| Powder Rheology (FT4) | Instrument SOP + ASTM F3049 | Sensitive to subtle cohesion changes |
| True/Skeletal Density (pycnometry) | ASTM B923 | Internal porosity detection |
| Moisture Content | TGA / gravimetric | Handling stability |

---

## 6. Budget Allocation

### 6.1 Recommended Budget: 3–5 Compositions

| Scenario | Total GA Budget | % of $750K | Compositions |
|----------|---------------:|:----------:|:------------:|
| Conservative (3 comps, 10 kg each) | $30,000–56,000 | 4–7.5% | 3 |
| **Recommended (4 comps, 10 kg each)** | **$40,000–65,000** | **5.3–8.7%** | **4** |
| Comprehensive (5 comps, 10 kg each) | $50,000–94,000 | 6.7–12.5% | 5 |

### 6.2 Proposed Budget Line Items

| Line Item | Amount | Category |
|-----------|-------:|----------|
| Service contract with Valimet for GA production + powder QC (3–4 compositions × 5–10 kg) | [partner amount removed] | Other Direct Costs — Services |
| GA-LPBF printing at BYU/U of U (using GA powder) | $3,000–5,000 | Materials + Machine Time |
| GA mechanical testing (tensile specimens) | $2,000–4,000 | Testing Services |
| Shipping + handling | $1,500–2,500 | Other Direct Costs |
| **Total** | [removed: includes partner amount] | |

### 6.3 Impact on Overall Budget

From the existing $750K budget, the GA validation fits within the existing **materials ($55K)** and could partially draw from **other ($6K)** lines. Structured as a service contract with Valimet (not a subaward), this simplifies budget structure compared to a national lab subaward. Ames Lab Phase II collaboration would be budgeted separately in the Phase II proposal.

---

## 7. Letter Targets (Collaboration & Support)

> **Updated April 10, 2026:** Revised strategy based on actual outreach. Valimet elevated to Priority 1 for **letter of collaboration** (official team member). Ames downgraded to **letter of support** (Phase II pathway) due to their internal Genesis Mission deadline constraint.

### 7.1 Priority 1: Valimet (Commercial) — LETTER OF COLLABORATION

- **Contact**: Sales/Technical team (Stockton, CA) — key contact emails obtained via phone (April 8–9)
- **Rationale**: Established commercial Al powder producer; fastest turnaround; no internal Genesis Mission deadline constraints; can serve as official Phase I GA team member
- **Letter type**: **Letter of Collaboration** (official team member, per RFA 2-sentence format)
- **Letter content**: Valimet agrees to provide custom gas atomization services for 3–5 novel Al alloy compositions at 5–10 kg batch scale during Phase I; contributes GA expertise, powder characterization support, and process parameter optimization
- **Budget**: Service contract (Other Direct Costs — Services)

### 7.2 Priority 2: Ames National Laboratory / Iowa State University — LETTER OF SUPPORT

**Key Contacts:**

| Contact | Role | Email | Phone | Notes |
|---|---|---|---|---|
| Powder Group lead | Head, Powder Group | (via PSD@ameslab.gov) | — | Primary contact for new GA collaborations (confirmed via April 2026 correspondence) |
| MPC manager | Manager, Materials Preparation Center (MPC) | (via MPC contact page) | — | MPC provides purification, preparation, and characterization services; handles Work-for-Others (WFO) agreements; initial point of contact who routed the inquiry to the Powder Group |
| Atomization specialist | Senior Technologist, Atomization Specialist | — | — | Hands-on atomization operations; key for technical discussions on batch parameters |
| Emeritus senior metallurgist | Senior Metallurgist (Emeritus) | — | — | Pioneered the GARS process; possible adviser/consultant |
| ~~Former PSDC group lead~~ | ~~Former PSDC Group Leader~~ | — | — | No longer at Ames National Laboratory (early 2026) |

**General Inquiry Channels:**
- PSDC Services: **PSD@ameslab.gov** or **Powdercapable@ameslab.gov**
- Online service request form: https://www.ameslab.gov/dmse/powder-synthesis-and-development-capability/request-psdc-services
- MPC Contact: https://www.ameslab.gov/dmse/materials-preparation-center/contact-mpc
- Ames Lab main: 515-294-2770, 2408 Pammel Dr, Ames, IA 50011

**Letter type**: **Letter of Support** (not collaboration) — expressing interest in Phase II GARS partnership for scale-up validation of FLAIME-discovered alloys at 10–25 kg scale. If Ames makes an exception on their internal deadline, upgrade to letter of collaboration.
**Rationale**: Ames had an internal Genesis Mission intent-to-submit cut-off (prior to April 10) which likely precludes joining as an official Phase I partner. A letter of support still signals DOE lab engagement and establishes the Phase II pathway.
**Budget**: No Phase I budget allocation for Ames; Phase II would include a subaward

> ⚠️ **Note (April 2026):** Ames Powder Group leadership changed in early 2026. Contact information updated based on direct correspondence with Ames Lab staff (April 10, 2026).

### 7.3 Priority 3: ORNL Manufacturing Demonstration Facility

- **Contact**: MDF User Program Office
- **Rationale**: Integrated GA + LPBF + characterization under one roof; DOE Category 1; already identified as FLAIME teaming target
- **Letter content**: Offer user facility access for GA validation builds; complementary LPBF and characterization if needed
- **Budget**: User facility access (potentially no-cost) or subaward

---

## 7A. Outreach Status (as of April 10, 2026)

### Ames National Laboratory — CONTACTED ⚠️ → LETTER OF SUPPORT TARGET

**Date:** April 10, 2026
**Status:** Initial response received; follow-up pending
**Letter target:** **Letter of Support** (not collaboration) — pointing to Phase II partnership for GARS scale-up

**Key findings from correspondence:**
- **The previous Ames PSDC contact has left Ames National Laboratory** — email bounced/was redirected
- A new Powder Group lead is in place (confirmed by the MPC manager)
- The MPC manager responded and routed the inquiry to the Powder Group lead
- The Powder Group lead indicated FLAIME is of interest and potentially within the group's capabilities
- ⚠️ **Ames had an internal Genesis Mission intent-to-submit cut-off date** (prior to April 10) — this likely precludes a letter of collaboration (official team member) for Phase I
- Most powder group members were on travel the week of April 7–11; expect more detailed response the following week

**Revised strategy:** Pursue a **letter of support** from Ames expressing interest in Phase II collaboration (GARS validation of FLAIME-discovered alloys at 10–25 kg scale). This still signals DOE lab engagement to reviewers without requiring Ames to go through their internal Genesis Mission approval process. If Ames makes an exception and can provide a letter of collaboration, upgrade accordingly.

**Action items:**
1. Follow up with an Ames Lab contact (via PSD@ameslab.gov) week of April 14 — request letter of support framed around Phase II GARS partnership
2. If Ames can make an exception on their internal deadline, pursue letter of collaboration instead
3. Ames letter of support language: "Ames National Laboratory's Powder Group has reviewed the FLAIME project and is interested in collaborating on gas atomization scale-up validation of FLAIME-discovered alloy compositions in a potential Phase II effort"

**Draft reply to an Ames Lab contact (send week of April 14):**

> Subject: Re: FLAIME — Gas Atomization Partnership for Genesis Mission
>
> Hi [Ames contact],
>
> Thanks for the kind words about the project and for taking the time to watch the video. Great to connect with you.
>
> I completely understand the internal deadline situation — I know the Genesis Mission RFA has generated a lot of activity. A few thoughts on how we might still work together:
>
> 1. **Letter of support (low overhead for Ames):** If a formal letter of collaboration isn't feasible given the internal cut-off, would Ames be open to providing a **letter of support** expressing interest in a potential Phase II collaboration? The idea would be that FLAIME discovers and validates novel Al alloy compositions via ultrasonic atomization + LPBF in Phase I, and then we partner with Ames for GARS scale-up validation (10–25 kg batches) in Phase II. This signals DOE lab engagement to reviewers without requiring Ames to go through the full internal Genesis Mission approval process.
>
> 2. **If an exception is possible:** If there's any path to a letter of collaboration (official team member) for our BYU-led submission, we'd welcome that. We're targeting Topic 3B (Critical Minerals — AI-Enabled Materials Discovery) under AMMTO, and having Ames as a DOE Category 1 partner would significantly strengthen the proposal. The scope would be a subaward for custom Al alloy gas atomization at 5–10 kg batch scale.
>
> 3. **Either way, I'd love to set up a brief call** to discuss how FLAIME's autonomous alloy discovery pipeline could complement Ames's atomization capabilities. We're building a closed-loop system (CALPHAD screening → ultrasonic atomization → LPBF → tensile testing, all guided by Bayesian optimization over function networks), and the UA→GA transfer validation is a key scientific contribution we'd like to develop together.
>
> Happy to work around your schedule. Would any time the week of April 14 work for a 20–30 min call?
>
> Best,
> Sterling

### Valimet — CONTACTED, AWAITING RESPONSE → LETTER OF COLLABORATION TARGET

**Date:** ~April 8–9, 2026
**Status:** Phone call completed; key contact emails obtained; waiting for follow-up (contacts out of town until early week of April 14)
**Letter target:** **Letter of Collaboration** (official team member) — Phase I GA service provider

**Details:**
- Made phone contact with Valimet (Stockton, CA)
- Obtained key contact emails for custom Al powder production inquiry
- Valimet reps out of office; expect response early week of April 14
- Valimet is a commercial partner — no internal Genesis Mission deadline constraints
- As commercial partner, Valimet provides the fastest path to an official letter of collaboration

**Action items:**
1. Follow up week of April 14 if no response received
2. Request pricing quote for 3–5 custom Al alloy compositions at 5–10 kg batch scale
3. **Request letter of collaboration** for DOE Genesis Mission proposal — Valimet as official Phase I GA partner
4. Letter of collaboration language (per RFA 2-sentence format): "Valimet, Inc. agrees to collaborate with BYU on the FLAIME project by providing custom gas atomization services for 3–5 novel Al alloy compositions at 5–10 kg batch scale during Phase I. Valimet will contribute gas atomization expertise, powder characterization support, and process parameter optimization for LPBF-targeted powder specifications."

### ORNL MDF — NOT YET CONTACTED

**Status:** Identified as Priority 2 GA partner; not yet contacted for Genesis Mission specifically
**Next step:** Contact MDF User Program Office if Ames partnership falls through

### Full Partnership Summary (Updated April 12, 2026)

**Letters of Collaboration (3 — official team members):**
| Partner | Role | Budget |
|---|---|---|
| **Valimet** | GA service provider — Phase I scale-up (5–10 kg batches, 3–5 compositions) | [partner amount removed] |
| **AMAZEMET** | UA atomizer vendor — consumables, process support, powder characterization | [partner amount removed] |
| **Thermo-Calc** | CALPHAD/AM Module — funded collaboration, simulations on BYU HPC | [partner amount removed] |

**Letters of Support (8 — advisors and collaborators):**
| Partner | Affiliation | Role |
|---|---|---|
| **Ames National Lab** | DOE National Lab (an Ames Lab contact, Powder Group) | Phase II GARS partnership pathway |
| **Fehrmann Alloys** | Industry | Master alloy / feedstock expertise |
| **Taylor Sparks** | University of Utah | LPBF printing access; specimen already printed |
| **Ashley Speer** | BYU | Departmental support |
| **Adam Clare** | University of Nottingham / UBC (FREng) | AM process expertise |
| **Chris Stiles** | JHU APL | Defense/nuclear application pathway |
| **Jae Hattrick-Simpers** | University of Toronto | Autonomous experimentation |
| **Keith Brown** | Boston University | SDL pioneer; closed-loop experimentation |

---

## 8. Timeline Integration

| Month | Activity |
|------:|---------|
| 1–3 | Main UA discovery loop running (Nodes 0–3); BOFN accumulating data |
| 3–4 | BOFN identifies top 3–5 candidate compositions for GA validation |
| 4 | Place GA orders with Valimet (primary) or backup provider; ship feedstock |
| 4–5 | Continue UA discovery loop; GA production underway at Valimet |
| 6–7 | Receive GA powders; begin characterization protocol |
| 7–8 | GA-LPBF builds at U of U; begin tensile specimen prep |
| 8–9 | GA mechanical testing; UA↔GA transfer analysis; publish comparison |
| 9 | Final report includes UA↔GA transferability data for DOE review |

---

## 9. Proposal Narrative Framing

> *"The FLAIME platform's cost-aware Bayesian optimization framework intelligently allocates gas atomization validation resources to only the highest-performing compositions identified through rapid ultrasonic atomization screening, maximizing information value per dollar. This GA scale-up validation step serves as the critical TRL bridge from laboratory discovery (TRL 2–3) to process validation (TRL 4–5), ensuring that FLAIME-discovered alloys are industrially reproducible. The novel UA→GA transfer dataset generated by this validation — the first of its kind for Al AM alloys — will be a standalone scientific contribution enabling future SDL platforms to predict scalability from screening data."*

---

## Edison Scientific Source

- **Task ID**: `0e34f629-5bd5-4917-8939-47364fc00354`
- **Job**: LITERATURE_HIGH
- **Date**: 2026-04-05
- **Key references**: Yankin et al. 2025 (UA AlSi12), Ciftcli et al. 2025 (rePOWDER alloy dev), Zhang et al. 2025 (Ames ARPA-E GA scale-up), Gianoglio et al. 2021 (GA cooling rates), Alvi et al. 2026 (deep GP BOFN), Żrodowski et al. 2021 (UA 316L), Groarke et al. 2021 (powder characterization standards)
