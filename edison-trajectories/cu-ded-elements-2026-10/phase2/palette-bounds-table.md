<!--
Edison Scientific ANALYSIS task (phase 2)
- Task ID: ea13ca40-78dd-4b62-9748-76c8cdd5e641
- Submitted: 2026-10-17T19:36:01Z
- Fetched: 2026-10-17T20:02:36Z (status: success)
- Raw trajectory JSON: ../raw/palette-bounds-table.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

TASK: FINAL PALETTE AND BOUNDS TABLE (synthesis of the attached files).

Attached are 50 per-element literature answers (phase1/el-NN-X.md: one per
element, each ending in a VERDICT line), a joint short-list answer
(phase1/joint-shortlist.md), a table of the parsed verdicts (verdicts.md),
and the coverage of each element in Thermo-Calc's TCCU7 copper database
(tccu7_coverage.md: assessed Cu-X-Y ternaries, and whether Cu-Ni-X and
Cu-Al-X are assessed).

Use ONLY the attached files. Produce:
1. The PALETTE: the elements to search over as designed additions (aim for
   8-14 besides Cu), ranked, with a two-sentence reason each that cites the
   attached answer. Apply these rules and say where you depart from them:
   (a) it must help seawater resistance, DED soundness, repair on cast NAB or
   wrought Cu-Ni, or replace nickel; (b) it must be meltable and atomizable
   in an alumina or zirconia crucible at <= 1,300 C; (c) no element whose
   main hazard (toxicity, regulation) blocks in-house powder making or laser
   deposition; (d) prefer elements whose Cu-X-Y systems are assessed in
   TCCU7, and flag any palette element that is not in TCCU7 at all; (e)
   critical-mineral status is a cost to carry as an objective, not a reason
   to exclude by itself.
2. One markdown table for Cu plus the palette with exactly these columns:
   | Element | Lower bound (wt%) | Recommended upper bound (wt%) | Conservative upper (wt%) | Non-conservative upper (wt%) | Functional floor when active (wt%) | Family (Cu-Ni / Al bronze / both) | Upper bound set by | TCCU7 tier | Source files |
   Recommended upper bound = the bound to USE in the search. Justify each
   choice between conservative and non-conservative from the attached
   evidence. Cu: give Cu_min instead.
3. A second table of IMPURITY LIMITS for the powder and the deposit (for
   example C, S, P, Pb, Bi, Se, Te, O, H, N, Zn in Cu-Ni), with the limit and
   its source.
4. A list of EXCLUDED elements, each with a one-line reason and the file it
   comes from, grouped by reason (toxicity; immiscible or above the melting
   limit; no benefit found; not in TCCU7 and little evidence; cost).
5. Disagreements between the per-element answers and the joint answer, and
   how you resolved each.
6. Elements whose evidence is thin or contradictory, as candidates for
   early CALPHAD checks or experiments.
Express all compositions in wt%. Output a single copy-pasteable markdown
section.

---

## Final designed-addition palette and bounds

**I recommend 13 additions besides Cu: Ni, Al, Fe, Mn, Cr, Sn, Si, Ti, Nb, Zr, Y, B, and Ge, in that order.** The first eight form the main search; Nb, Zr, Y, B, and Ge are conditional probes, initially tested individually against matched controls rather than all added together. These are **research-search bounds, not qualified powder specifications or evidence of as-deposited C71500 parity**.

I use only the supplied files. I retain the per-element bounds as provenance, read their family-specific qualifications rather than just `verdicts.md`, and use `tccu7_coverage.md` to settle database-coverage questions; references reported inside the answers have not been independently reverified.

### 1. Ranked palette

1. **Ni — corrosion-film and repair anchor.** Ni has the strongest directly relevant Cu–Ni seawater evidence, contributes to protective-film resistance, and provides the most straightforward compositional connection to wrought Cu–Ni repair substrates. I keep it despite its critical-mineral burden, but select a working ceiling of **30 wt%**, below the element answer’s **33/35 wt%**, because atomization thermal margin—not binary solid solubility—is the immediate constraint. **Source:** `el-02-Ni.md`, powder-production and bounds sections; `joint-shortlist.md`, liquidus constraint.

2. **Al — enables the aluminum-bronze route and NAB compatibility.** Al supplies the bronze-family corrosion/strength mechanism, and the answer reports directly relevant ultrasonic atomization of CuAl10Ni5Fe5 at **1,300 °C**. I select **9.5 wt%**, not **10.5 wt%**, because retained β/β′, selective attack, and poor ductility under rapid cooling are especially consequential without post-build heat treatment. **Source:** `el-03-Al.md`, powder manufacture and bounds.

3. **Fe — useful in both families, by different mechanisms.** Fe benefits Cu–Ni films when retained in solution and contributes Fe–Al-rich κ phases in NAB, so it cannot be assigned one unrestricted cross-family optimum. I select **4.5 wt%** overall, tighter than the element answer’s **5.0/6.0 wt%**, to anchor the first NAB search to C95800-like chemistry while imposing much lower Cu–Ni caps. **Source:** `el-04-Fe.md`, branch-specific bounds; `joint-shortlist.md`, Fe constraints.

4. **Mn — deoxidation and a conditional lower-Ni bridge variable.** The answer documents a chloride response at **0.9 wt%**, established NAB use through **1.5 wt%**, and an experimental binary optimum at **4.4 wt%**, but also poor results for some low-Ni ternaries. I retain **4.4 wt%** only for a separately flagged Cu–Ni–Al–Mn bridge study, not as a general replacement for Ni, while keeping the main conventional-family search at **≤1.5 wt%**. **Source:** `el-05-Mn.md`, corrosion and bounds; `joint-shortlist.md`, MARINEL bridge discussion.

5. **Cr — a targeted Cu–Ni erosion-corrosion variable.** Approximately **0.5 wt% Cr** has commercial-service and quantitative high-flow seawater precedent, whereas the same record warns that stagnant or shielded exposure can be less favorable. I therefore use **0.5 wt%**, not **2.0 wt%**, and do not transfer the confounded Ni–Cr-underlayer/NAB result into a designed Cr-bearing NAB powder. **Source:** `el-06-Cr.md`, evidence table and bounds.

6. **Sn — a bounded bronze microstructure/corrosion probe.** The answer supports screening near **1.0 wt%** through cast-NAB microstructure results and indirect chloride evidence, but reports deteriorating behavior at **1.5 wt%** in the Cu–Al–Ni comparison. I use **1.0 wt%** and do not treat either aged Cu–Ni–Sn performance or a Sn surface coating’s optical response as proof for a pre-alloyed, as-deposited powder. **Source:** `el-07-Sn.md`, corrosion comparisons and bounds; `joint-shortlist.md`, Sn discussion.

7. **Si — preserves a distinct low-Al bronze exploration.** Si has deoxidation/strengthening roles and low-Al Cu–Al–Si–Mn casting evidence, but its **2.0 wt%** conservative ceiling is not a high-Al NAB allowance. I retain **2.0 wt%** only in that low-Al branch, cap the initial Cu–Ni exploration at **1.0 wt%**, and use **0.10 wt%** in C95800-like NAB rather than adopt one family-blind limit. **Source:** `el-09-Si.md`, screening bounds and interactions; `joint-shortlist.md`, C95800 Si limit.

8. **Ti — the strongest small-addition processability case.** The answer identifies Ti-bearing Cu–Ni welding consumables for oxygen/nitrogen scavenging and porosity control, plus cast and wire-arc NAB grain refinement. I allow **0.50 wt%** only in the Cu–Ni branch because that range has filler precedent, while retaining **0.10 wt%** for NAB because excess Ti, inclusions, and cracking are unresolved. **Source:** `el-13-Ti.md`, welding evidence and family-specific bounds.

9. **Nb — a conditional Cu–Ni/Si weldability and bridge probe.** Its most defensible task-specific role is historical Nb–Si-assisted cast-Cu–Ni weldability, supplemented by multicomponent marine-alloy precedent rather than isolated as-deposited corrosion evidence. I use **0.80 wt%**, not **1.00 wt%** or the joint answer’s **1.5 wt%**, and require demonstrated homogeneous dissolution and a deliberate Si balance rather than assuming refractory Nb particles are acceptable. **Source:** `el-10-Nb.md`, bounds and joint interactions.

10. **Zr — dilute grain-refinement/process probe.** Casting-derived grain refinement and Cu–Cr–Zr processing precedents justify a small experiment, but neither validates Cu–Ni/NAB seawater performance. I select **0.15 wt%**, not **0.50 wt%**, because limited solubility, boundary phases, oxidation, and uncertain ceramic-contact behavior make the higher level a poor first search limit. **Source:** `el-14-Zr.md`, solubility discussion and bounds.

11. **Y — a deliberate exception to the TCCU7 preference.** The answer reports a directly relevant **0.021 wt% Y** optimum in as-cast Cu–10Ni after 30 days in chloride solution, with deterioration as Y-rich oxysulfide inclusions increase. I retain only a **0.021 wt%** probe despite Y being **absent from TCCU7**, because this evidence is more specific to the target than the supplied elemental-La/Ce evidence; I do not adopt the unsupported **0.05 wt%** escalation. **Source:** `el-43-Y.md`, evidence and bounds; `tccu7_coverage.md`.

12. **B — a tightly bounded grain-refinement probe, not a corrosion claim.** The answer supplies copper-alloy casting grain-refinement evidence and a relevant **0.5 kg**, argon-protected induction-melting precedent, but no qualified marine DED result. I retain **0.020 wt%** overall with **0.010 wt%** in Cu–Ni, rather than **0.050 wt%**, because recovery, borides, segregation, and reproducible microdosing remain unqualified. **Source:** `el-19-B.md`, melting, phase assessment, and asymmetric family bounds.

13. **Ge — a narrowly scoped bronze-family hypothesis.** A nominal **0.20 wt% Ge** NAB-like material showed lower chloride-jet loss, but it was powder-metallurgy processed and heat treated, with composition changes that prevent attributing the result to Ge alone. I retain only **0.20 wt%**, not **3.0 wt%**, as a matched-control probe because it supplies a more target-related experimental lead than generic precipitation-hardening evidence, while carrying its cost and weak ternary coverage explicitly. **Source:** `el-37-Ge.md`, quantitative comparisons and bounds.

**Application of the selection rules.** Every retained element has a stated corrosion, soundness, repair, or nickel-reduction hypothesis; none is retained merely because it strengthens aged copper. No selected element has a demonstrated blanket hazard prohibition in the supplied record, but Ni-, Mn-, and reactive-metal powder/fume controls still require institutional approval; an alloy wt% limit is never an occupational exposure clearance. Critical-mineral content and procurement cost remain objectives/penalties, not automatic exclusions.

**Meltability is a candidate-level hard gate, not a claim established by this palette.** Require a homogeneous liquid and a calculated/measured liquidus preferably **≤1,200 °C**; admit **1,200–1,250 °C** only after demonstrating useful, stable atomization superheat without exceeding **1,300 °C**. Master alloys can aid incorporation of refractory additions but do not waive that requirement; Ti, Zr, Y, B, Ge, and Nb need recovery/inclusion checks in the actual alumina or zirconia crucible, because the files do not certify those combinations. **Sources:** `el-01-Cu.md`, `el-02-Ni.md`, and the respective powder-making sections.

### 2. Bounds to encode in the search

All values are **wt% of the alloy**. Zero means an element may be absent; functional floors are literature-anchored starting doses, often transferred from another process or family, **not universal minimum-effective concentrations**. The recommended column is the working outer ceiling; the family restrictions immediately below it are mandatory parts of its interpretation, and the larger non-conservative numbers are **not** automatically available to the optimizer.

The conservative/non-conservative columns preserve the palette-wide values in the individual answers, including where those answers identify them as hypotheses. TCCU7 tiers count assessed Cu–X–Y ternaries: **1 = ≥6; 2 = 3–5; 3 = 0–2; 4 = element absent**; “Ni/Al yes/no” denotes assessed Cu–Ni–X/Cu–Al–X, not validation of a multicomponent alloy (`tccu7_coverage.md`).

| Element | Lower bound (wt%) | Recommended upper bound (wt%) | Conservative upper (wt%) | Non-conservative upper (wt%) | Functional floor when active (wt%) | Family (Cu-Ni / Al bronze / both) | Upper bound set by | TCCU7 tier | Source files |
|---|---|---|---|---|---|---|---|---|---|
| Cu | Cu_min = 65; balance | Cu_min = 65 | Cu_min = 65 | Cu_min = 60 | Not applicable | both | Total-solute budget; Cu-rich phase constitution and liquidus; not a universal phase boundary | Matrix | el-01-Cu.md; joint-shortlist.md |
| Ni | 0 | 30 | 33 | 35 | 2; screening floor, not C71500 parity | both | Liquidus/superheat; Ni-Al phase balance; use ≤5.5 in primary NAB | 1; 20 ternaries; Ni-Al assessed | el-02-Ni.md; joint-shortlist.md |
| Al | 0 | 9.5 | 9.5 | 10.5 | 1.8 provisional; established NAB starts at 8.5 | both | Retained β/β′, γ and selective attack; ≤3.0 initially in Cu-Ni-Al bridge | 1; 8; Ni yes | el-03-Al.md; joint-shortlist.md |
| Fe | 0 | 4.5 | 5.0 | 6.0 | 0.4 Cu-Ni; 2.0 exploratory Al bronze | both | Out-of-solution Fe and κ heterogeneity; family caps below | 1; 13; Ni/Al yes/yes | el-04-Fe.md; joint-shortlist.md |
| Mn | 0 | 4.4 | 1.5 | 4.4 | 0.9; background-dependent | both | Nonmonotonic chloride response, β stabilization, oxide/loss burden; >1.5 bridge trials only | 1; 9; Ni/Al yes/yes | el-05-Mn.md; joint-shortlist.md |
| Cr | 0 | 0.5 | 0.5 | 2.0 | 0.5; erosion-corrosion evidence | Cu-Ni | Segregation/particles; stagnant-water localized attack; no primary NAB addition | 1; 10; Ni/Al yes/no | el-06-Cr.md |
| Sn | 0 | 1.0 | 1.0 | 1.5 | 0.5; indirect Al-bronze-related evidence | both | Sn-rich boundary phases, segregation and reversed chloride benefit | 1; 12; Ni/Al yes/yes | el-07-Sn.md; joint-shortlist.md |
| Si | 0 | 2.0 | 2.0 | 3.8 | 0.5; brass-derived, unverified in target families | both | 2.0 only in low-Al silicon-bronze-like branch; silicides, cracking and selective attack | 1; 10; Ni/Al yes/yes | el-09-Si.md; joint-shortlist.md |
| Ti | 0 | 0.50 | 0.10 | 0.50 | 0.012 cast NAB; 0.05 wire-arc NAB; 0.20 Cu-Ni filler | both | Cracking at excess Ti, oxide/nitride inclusions and recovery; NAB cap 0.10 | 2; 4; Ni/Al yes/no | el-13-Ti.md |
| Nb | 0 | 0.80 | 0.80 | 1.00 | 0.50; conditional on Cu-Ni/Si context | Cu-Ni | Undissolved/coarse Nb-rich phases, ductility and melt homogeneity | 2; 5; Ni/Al yes/no | el-10-Nb.md; joint-shortlist.md |
| Zr | 0 | 0.15 | 0.15 | 0.50 | 0.010; casting-derived | both | Low solubility, boundary phases, oxides and unverified ceramic compatibility | 2; 3; Ni/Al no/no | el-14-Zr.md |
| Y | 0 | 0.021 | 0.021 | 0.05 — hypothesis only | 0.021; lowest retrieved beneficial dose | Cu-Ni | Nonmonotonic corrosion response and Y-rich oxysulfides; recovery unknown | 4; NOT IN TCCU7 | el-43-Y.md |
| B | 0 | 0.020 | 0.020 | 0.050 | 0.002; casting-derived, unverified transfer | both | Borides/segregation, ductility, recovery and dose control; Cu-Ni cap 0.010 | 3; 0; Ni/Al no/no | el-19-B.md |
| Ge | 0 | 0.20 | 0.20 | 3.0 | 0.20; provisional experimental dose | Al bronze | No validated higher-dose as-deposited precedent; phases, retention and cost | 3; 2; Ni/Al no/no | el-37-Ge.md |

**Family and joint gates—do not search the Cartesian product of the maxima:**

- **Mass balance:** \(\mathrm{Cu}=100-\sum w_i\), including measured residuals, with **Cu ≥65 wt%**; use **Cu ≥79 wt%** for the initial C95800-like NAB neighborhood. The **60 wt%** Cu alternative is not enabled in this search, and no universal Cu upper bound is claimed (`el-01-Cu.md`).
- **Cu–Ni:** use **Fe ≤1.0 wt%** near the C71500-like end and **≤1.8 wt%** in the conventional 90–10-like neighborhood, subject to Fe remaining in solution; neither the table’s **4.5 wt% Fe** nor **2.0 wt% Si** applies here. Initial Si is **≤1.0 wt%**, B **≤0.010 wt%**, and Y/Cr/Nb are Cu–Ni-family probes (`el-04-Fe.md`, `el-09-Si.md`, `el-19-B.md`).
- **C95800-like NAB:** use **Ni ≤5.5 wt%**, **Fe ≤4.5 wt%**, **Mn ≤1.5 wt%**, **Si ≤0.10 wt%**, **Ti ≤0.10 wt%**, and no designed Cr, Nb, or Y in the primary branch. Favor **Ni > Fe** as an evidence-informed starting prior, not a universal proven corrosion boundary; evaluate retained β/β′ and κ distribution after deposition and dilution (`el-02-Ni.md`, `el-04-Fe.md`, `el-06-Cr.md`, `el-10-Nb.md`, `el-13-Ti.md`, `el-43-Y.md`, `joint-shortlist.md`).
- **Low-Al Si-bearing bronze:** only this distinct branch may use **Si up to 2.0 wt%**; retain the paired Al–Si–Mn context of the element answer rather than combining maximum Si with maximum Al. Its extension toward NAB or Cu–Ni is an experiment, not commercial seawater precedent (`el-09-Si.md`).
- **Cu–Ni–Al–Mn bridge:** begin with **Al ≤3.0 wt%**, **Fe ≤1.0 wt%**, and allow **Mn up to 4.4 wt%** only in flagged exploratory candidates. The Al cap is the per-Al answer’s provisional Cu–Ni bound and the Fe cap is joint-answer guidance; neither qualifies a MARINEL-like alloy without aging, nor proves that Mn replaces Ni (`el-03-Al.md`, `el-05-Mn.md`, `joint-shortlist.md`).
- **Nb–Si balance:** evaluate the historical **Nb/Si ≥2** practice and **Nb −1.55Si +0.10 >0** separately, with all contents in wt%; they are not equivalent or universal DED laws. If adopting the former as a trial-design gate, **Nb ≤0.80 wt% implies Si ≤0.40 wt%** in that Nb-bearing sub-study, and compositions below the generic Si floor must be identified as interaction tests (`el-10-Nb.md`; the 0.40 value is arithmetic).
- **Repair dilution and thermal cycling:** evaluate phase constitution and selective attack at the first layer/heat-affected zone as well as the top deposit. A powder-average composition within bounds does not establish that its dilution trajectory on either substrate is sound (`el-02-Ni.md`, `el-03-Al.md`, `el-04-Fe.md`).

### 3. Impurity limits for powder and deposit

I adopt the following **initial chemistry screening/action limits**, measured separately in each powder lot and representative deposit. They are not demonstrated DED-safe thresholds: rows explicitly distinguish a published numerical anchor from a proposed project control, and substrate dilution can make deposit compliance different from powder compliance. All concentrations below are **wt%**; tighter controlling procurement specifications take precedence.

| Impurity | Powder limit (wt%) | Deposit limit (wt%) | Basis, status, and failure mode | Source files |
|---|---:|---:|---|---|
| C | ≤0.005; aim ≤0.002 | ≤0.005; aim ≤0.002 | Proposed project limit, not a specification; carbon precipitation, carbides and possible C–O porosity. | `el-32-C.md` |
| S | ≤0.005 | ≤0.005 | I adopt the joint answer’s tighter working value; the element answer’s 0.010 ceiling and 0.005 procurement target are not measured DED thresholds. Sulfides, hot ductility/cracking and film damage motivate control. | `el-27-S.md`; `joint-shortlist.md` |
| P | ≤0.010 | ≤0.010 | Joint answer’s tighter project target, below the element answer’s 0.020 Cu–Ni-related and 0.015 Al-bronze-related anchors; detrimental weldability, phosphides and segregation. | `el-22-P.md`; `joint-shortlist.md` |
| Pb | ≤0.010; aim ≤0.005 | ≤0.010; aim ≤0.005 | Welding-oriented ceiling in the element answer; low-melting segregants/hot cracking and toxic fume. No designed Pb. | `el-23-Pb.md` |
| Bi | ≤0.001 | ≤0.001 | Published Cu–Ni hot-workability control, transferred provisionally to DED/NAB; severe boundary embrittlement. Not a DED qualification limit. | `el-24-Bi.md` |
| Se | ≤0.006 | ≤0.006 | Cu–Ni hot-workability control, provisionally extended to both families; no marine DED benefit. | `el-25-Se.md` |
| Te | ≤0.003; aim ≤0.002 | ≤0.003; aim ≤0.002 | Cu–Ni hot-workability/HAZ-cracking literature anchor; NAB transfer and tighter aim are project choices. | `el-26-Te.md` |
| O | ≤0.013; prefer ≤0.005 | ≤0.013; prefer ≤0.005 | 0.013 was measured in ultrasonic-atomized NAB-like powder, not established as a safe limit or measured deposit value; transfer to deposit is provisional. Oxides and H–O porosity require separate defect checks. | `el-29-O.md`; `el-03-Al.md` |
| H | <0.0001; stretch <0.00006 | <0.0001; stretch <0.00006 | Copper electron-beam-welding/OFP cleanliness analogues; provisional for these alloys and DED. Gas/steam porosity; hydrogen and oxygen cannot be treated independently. | `el-30-H.md` |
| N | ≤0.0005 | ≤0.0005 | Explicit engineering screen, not a standard or solubility allowance; gas rejection/porosity and nitrides. Validate assay sensitivity. | `el-31-N.md` |
| Zn | ≤0.50 | ≤0.50 | Element/joint project ceiling, not a verified Cu–Ni/NAB specification; use any tighter controlling procurement limit. Volatility, drift, fumes and selective attack; not a designed addition. | `el-08-Zn.md`; `joint-shortlist.md` |
| As | ≤0.0005 | ≤0.0005 | C10100 numerical anchor transferred as a precautionary project criterion, not a Cu–Ni/NAB weld qualification; toxicity and Ni-associated hot-cracking concern. | `el-20-As.md` |
| Sb | ≤0.020 | ≤0.020 | Provisional project control, not a standard; boundary embrittlement and poor welding compatibility. | `el-21-Sb.md` |
| Mg | <0.010 | <0.010 | Low-Mg cast-NAB substrate analysis is the anchor, not a tolerance study; retention, oxides and unqualified NAB ductility/service response. | `el-16-Mg.md` |
| Mo | ≤0.020 | ≤0.020 | Project contamination-action ceiling near a Cu-rich equilibrium estimate; not validated tolerance. Check sonotrode pickup and refractory particles. | `el-33-Mo.md` |
| In | ≤0.010 | ≤0.010 | Proposed procurement/reporting rule only; surface/terminal-liquid enrichment is a concern, not a demonstrated In-induced DED crack threshold. | `el-38-In.md` |
| Li | ≤0.005 | ≤0.005 | Proposed residual screen below a reported melt-treatment charge; no retained-Li seawater benefit or validated tolerance. | `el-39-Li.md` |
| Ce | ≤0.040 | ≤0.040 | Weak project ceiling anchored to retained **total mixed rare earth**, not a Ce-specific permissible concentration; oxides and uncertain recovery. | `el-45-Ce.md` |
| Nd | ≤0.010 | ≤0.010 | Explicit project quality-control policy, not a specification; intermetallic/inclusion and retention concerns without chloride qualification. | `el-47-Nd.md` |
| Cd | No intentional Cd; ≤0.010 is only a provisional impurity screen | Same | The file’s 0.010 value is regulatory/project-oriented, not demonstrated technical tolerance or permission to melt Cd-bearing material; institutional hazard review controls acceptance. | `el-28-Cd.md` |
| Be | No intentional Be; no routine processing clearance inferred from a wt% value | Same | The file’s possible 0.10 NAB impurity allowance concerns metallurgy, not safe powder making or laser exposure; do not adopt it as an in-house acceptance permission. | `el-11-Be.md`; `joint-shortlist.md` |

For Ga, La, Hf, V, W, Ta, Ca, Sr, Sc, Pr, Er, Gd, and Pd, the supplied answers do **not** establish a transferable numerical impurity tolerance: require no intentional charge, measured/reportable contamination where relevant, and review unexpected pickup rather than inventing a zero-tolerance or “safe” number. For the joint answer’s proposed impurity sums, the selected individual limits already give **Pb + Bi ≤0.011**, **S + P ≤0.015**, and **Pb + S + P + C + Bi ≤0.031 wt%**, respectively tighter than its **0.015**, **0.020**, and **0.050 wt%** suggestions; these are arithmetic consistency checks, not validated cracking laws (`joint-shortlist.md`).

### 4. Excluded elements—excluded as design variables, not automatically forbidden as traces

The following **36 elements**, together with Cu and the 13 additions above, account for all 50 element answers. “No benefit” below means no sufficiently demonstrated incremental benefit for this specific as-deposited marine-repair task, not no useful metallurgy anywhere.

**Toxicity/exposure trade-off incompatible with intentional use in this program**

- **Be:** severe inhalation hazard outweighs nonqualifying Cu–Be/impurity evidence; the reported **0.10 wt%** metallurgical allowance is not a powder-processing safety limit (`el-11-Be.md`).
- **Cd:** toxic, volatile melting/welding emissions with no demonstrated target-service gain; historical conductor use is irrelevant to qualification (`el-28-Cd.md`).
- **As:** brass-specific dezincification benefit does not transfer to these Ni-bearing repairs, which add hot-cracking concern to toxicity (`el-20-As.md`).
- **Pb:** free-machining benefits conflict with weldability through low-melting segregants, with an additional toxic-fume burden (`el-23-Pb.md`).

**Immiscibility or unfavorable refractory incorporation within the melting route**

- **Mo:** near-immiscible Cu–Mo and confounded, heat-treated corrosion evidence do not support homogeneous pre-alloyed powder; track incidental sonotrode pickup instead (`el-33-Mo.md`).
- **W:** the relevant laser studies use solid W particles attached to Cu powder, not a homogeneous induction-melted alloy, and report heterogeneous interfaces/pores (`el-34-W.md`).
- **Ta:** essentially immiscible Cu–Ta requires nonequilibrium routes unlike the proposed melt/atomize process, with no relevant marine bound (`el-35-Ta.md`).
- **V:** strengthening/grain-refinement analogues do not establish a workable marine composition, and the reported high-V liquidus is about **1,600 °C**—not a claimed melting limit for trace V (`el-18-V.md`).

**No sufficient target-specific benefit found, or unfavorable processing trade-off**

- **Zn:** volatility and composition drift plus selective-attack risk outweigh brass-family benefits; retain only a residual limit (`el-08-Zn.md`).
- **Co:** favorable evidence mainly concerns aged electrical alloys, while the bulk-bronze chloride result is adverse/confounded; added powder hazard and cost buy no demonstrated incremental benefit (`el-12-Co.md`).
- **Mg:** a melt-treatment role does not establish a useful retained marine-alloy concentration, and NAB ductility/service concerns and oxide/recovery uncertainty remain (`el-16-Mg.md`).
- **Sb:** α-brass inhibition does not justify boundary-embrittling, welding-unfriendly Sb in Cu–Ni/NAB repairs (`el-21-Sb.md`).
- **P:** deoxidation or brass inhibition is insufficient justification for a designed phosphide/segregation-prone constituent in the first DED campaign (`el-22-P.md`).
- **Bi:** lead-replacement machinability conflicts with severe Cu grain-boundary embrittlement and hot-workability requirements (`el-24-Bi.md`).
- **Se:** chip-breaking/free-machining roles do not offset the Cu–Ni hot-workability penalty (`el-25-Se.md`).
- **Te:** free machining is not a marine-film benefit, while Cu₂Te segregation and HAZ cracking are relevant liabilities (`el-26-Te.md`).
- **S:** no required alloying function offsets film damage, sulfides and welding/hot-ductility uncertainty (`el-27-S.md`).
- **O:** useful environmental protective-film formation is not evidence for intentionally adding bulk oxygen, which can produce inclusions and H–O pores (`el-29-O.md`).
- **H:** gas/steam porosity and possible embrittlement have no balancing intended alloying benefit (`el-30-H.md`).
- **N:** no established marine benefit offsets gas rejection/porosity and reactive-solute nitrides (`el-31-N.md`).
- **C:** carbon precipitation, carbides and contamination-related defects have no demonstrated target-service benefit (`el-32-C.md`).
- **Ca:** the cited deoxidizer/nucleant suggestion does not establish a beneficial retained-Ca composition, and powder-making reactivity is unqualified (`el-40-Ca.md`).
- **Sr:** proposed SrO nucleation is not evidence for retained elemental Sr improving marine copper DED (`el-41-Sr.md`).
- **La:** the proposed **0.05 wt%** dose is chiefly acid/casting-derived, not verified chloride DED benefit; I prioritize the more specific Y probe despite La’s better database coverage (`el-44-La.md`).
- **Ce:** accessible results do not establish a Ce-specific chloride dose response or retained-content bound, and mixed-RE or oxide-dispersion evidence cannot supply one (`el-45-Ce.md`).

**Not in TCCU7 and little directly relevant evidence**

- **Hf:** attractive Cu₅Hf strengthening depends on treatment/deformation/aging, with no marine as-deposited gain and additional ceramic-contact concerns (`el-15-Hf.md`; `tccu7_coverage.md`).
- **Ga:** phase/surface-reaction evidence supplies neither a useful marine DED interval nor a tolerable impurity concentration (`el-36-Ga.md`; `tccu7_coverage.md`).
- **In:** surface segregation is documented, but seawater protection and sound marine repair are not; even its residual ceiling is only a project rule (`el-38-In.md`; `tccu7_coverage.md`).
- **Li:** melt deoxidation does not establish retained-Li benefit after atomization/DED, and corrosion/retention concerns remain (`el-39-Li.md`; `tccu7_coverage.md`).
- **Sc:** precipitation-hardening evidence is from subsequently aged nearly pure Cu, with unqualified grain-boundary constituents rather than relevant marine DED evidence (`el-42-Sc.md`; `tccu7_coverage.md`).
- **Pr:** Cu–Pr intermetallic assessment supplies no beneficial marine-DED interval or powder-route qualification (`el-46-Pr.md`; `tccu7_coverage.md`).
- **Nd:** an acid-corrosion lead is not chloride-service evidence, and retained intermetallic/oxide behavior is unresolved (`el-47-Nd.md`; `tccu7_coverage.md`).
- **Er:** documented compounds do not establish seawater benefit, crack-free DED, or a numeric marine design bound (`el-48-Er.md`; `tccu7_coverage.md`).
- **Gd:** Al–Cu–Gd/shape-memory leads do not establish a useful as-deposited Cu–Ni/NAB interval (`el-49-Gd.md`; `tccu7_coverage.md`).

**Cost without a demonstrated compensating benefit—not critical-mineral status alone**

- **Ag:** the dilute corrosion lead is an indirect nanoparticle/shape-memory result, whereas laser-process improvements use much larger Ag contents without marine qualification; that evidence does not justify the added cost (`el-17-Ag.md`).
- **Pd:** positive chloride evidence is Ni-balanced filler or uncontrolled electrodeposit evidence, not Cu-rich repair qualification or demonstrated Ni displacement, so its added cost is unjustified here (`el-50-Pd.md`).

### 5. Disagreements and their resolution

- **Ni and Cu:** the joint answer proposes **20/30 wt% Ni** conservative/aggressive bounds, versus **33/35 wt%** in the Ni answer, while both allow **Cu_min =65/60 wt%**. I use **Ni ≤30 wt%** and **Cu ≥65 wt%**, but reject an exact universal “30 wt% Ni equals the liquidus ceiling” rule: each composition must pass the thermal gate (`el-01-Cu.md`, `el-02-Ni.md`, `joint-shortlist.md`).
- **Al and Fe:** the joint answer extends Al to **12 wt%** and gives **4.5 wt%** conservative Fe, whereas the element answers give **9.5/10.5 wt% Al** and **5.0/6.0 wt% Fe**. I select **9.5 wt% Al** and **4.5 wt% Fe**, favoring the C95800-like first search and as-deposited phase/corrosion uncertainty rather than the largest demonstrated melting or strength range (`el-03-Al.md`, `el-04-Fe.md`).
- **Mn:** the joint **2.0/4.0 wt%** bounds differ from the element **1.5/4.4 wt%** bounds. I preserve **1.5 wt%** for conventional families but deliberately carry **4.4 wt%** for flagged bridge candidates; the binary optimum and MARINEL precedent motivate a test, not a prediction for low-Ni ternaries (`el-05-Mn.md`).
- **Cr and Sn:** joint bounds of **0.8/1.5 wt% Cr** and **1.0/2.5 wt% Sn** are broader/different from the element answers’ **0.5/2.0 wt% Cr** and **1.0/1.5 wt% Sn**. I use **0.5 wt% Cr** and **1.0 wt% Sn**, where the service or experimental anchors are clearest, and reject higher limits merely inferred from alloy classes, coatings, or aged material (`el-06-Cr.md`, `el-07-Sn.md`).
- **Si:** the joint **0.30/1.0 wt%** proposal cannot replace the element answer’s **2.0/3.8 wt%** low-Al-bronze bounds without discarding a distinct family. I retain the **2.0 wt%** low-Al branch, **≤1.0 wt%** Cu–Ni exploration and **≤0.10 wt%** C95800-like NAB control; no single family-blind Si cap is defensible (`el-09-Si.md`).
- **Nb and Ti:** joint **0.50/1.5 wt% Nb** and **0.20/0.80 wt% Ti** lack the element answers’ narrower qualifications. I use **Nb ≤0.80 wt%** and Ti **≤0.50 wt% in Cu–Ni / ≤0.10 wt% in NAB**; the Ti choice departs from the pooled conservative **0.10 wt%** because the Cu–Ni filler evidence independently supports **0.20–0.50 wt%** (`el-10-Nb.md`, `el-13-Ti.md`).
- **B:** the joint answer’s **0.10 wt%** aggressive bound exceeds the element answer’s **0.050 wt%** overall and **0.020 wt%** Cu–Ni aggressive bounds. I select **0.020 wt%** bronze/**0.010 wt%** Cu–Ni and do not present the joint answer’s generic low-melting-film warning as a demonstrated Cu–B mechanism: the element assessment reports no binary Cu–B intermetallic, although Fe/Ni borides and segregation remain concerns (`el-19-B.md`).
- **Rare earths:** the joint answer merges Ce/Y into a **0.05/0.20 wt%** slot and says Ce or Y has better CALPHAD coverage than La. The supplied coverage file shows **La: four**, **Ce: three** assessed Cu ternaries, and **Y: absent**; I reject both the coverage claim and element interchangeability, retain only **Y ≤0.021 wt%** as an explicitly non-TCCU7 probe, and keep Ce/La out of the main palette (`el-43-Y.md`–`el-45-Ce.md`, `tccu7_coverage.md`).
- **Co, Ag, and Ge:** Co and Ag are INCLUDE in their element answers but dropped jointly; Ge was outside the joint candidate list. I agree with dropping Co/Ag because their incremental task-specific evidence is weak relative to cost/hazard, but add **Ge ≤0.20 wt%** as a restricted bronze probe; none of those decisions is based solely on critical-mineral designation (`el-12-Co.md`, `el-17-Ag.md`, `el-37-Ge.md`).
- **Impurities and Be:** joint ceilings are much looser for O (**0.020/0.050 wt%**), H (**0.0005/0.0010 wt%**), N (**0.005/0.020 wt%**) and C (**0.010/0.030 wt%**) than the respective element recommendations. I use the tighter element-based project screens, adopt the joint answer’s tighter S/P working targets, and reject interpreting the per-Be **0.10 wt%** metallurgical proposal as permission for in-house Be-containing powder processing (`el-11-Be.md`, `el-22-P.md`, `el-27-S.md`, `el-29-O.md`–`el-32-C.md`).
- **Search topology and numerical interaction rules:** the Cu answer favors constrained family spaces plus a small bridge, whereas the joint answer favors a continuous simplex with soft transitions. I use one composition representation with **explicit family-gated candidate sets and a limited bridge**, and do not encode the joint answer’s incomplete aluminum-equivalent formula, universal **Fe + Mn ≤2.5 wt%**, or zinc-equivalent rule as verified laws; the supplied answers do not establish those universal thresholds, and the Ni answer itself reports a **Cu–30Ni–2Fe–2Mn** precedent (`el-01-Cu.md`, `el-02-Ni.md`, `el-04-Fe.md`, `el-05-Mn.md`, `joint-shortlist.md`).
- **Database coverage:** the joint answer repeatedly says systems are “likely” assessed and speculates about an NAB quaternary assessment. I replace that with the supplied TCCU7 inventory: all included database elements have assessed Cu binaries; Cu–Ni–Nb, Cu–Ni–Ti and Cu–Ni–Cr are assessed, Cu–Al–Cr is not, and Cu–Ni–Zr/Cu–Al–Zr, Cu–Ni–B/Cu–Al–B, and Cu–Ni–Ge/Cu–Al–Ge are not; a well-covered core is not proof of a validated high-order alloy (`tccu7_coverage.md`).

### 6. Thin or contradictory evidence: first CALPHAD checks and experiments

1. **Thermal feasibility at the Ni-rich end, and Nb incorporation:** calculate equilibrium liquidus and solidification paths for actual multi-solute compositions, then verify thermal margin and homogeneous melting experimentally before powder production. Neither a **30 wt% Ni** cap nor a low addition of refractory Nb guarantees a homogeneous, atomizable melt (`el-02-Ni.md`, `el-10-Nb.md`).
2. **Al–Ni–Fe–Mn phase selection without heat treatment:** compare conventional NAB, a lower-Al bridge, and high-Mn bridge controls for retained β/β′, κ morphology, cracking and selective attack. Cast/annealed and powder-bed findings are not uniformly consistent, so neither “all martensite is unacceptable” nor “rapid solidification fixes corrosion” is supported as a universal rule (`el-02-Ni.md`–`el-05-Mn.md`).
3. **Tier-2 extrapolations:** Nb and Ti have assessed Cu–Ni ternaries but not Cu–Al ternaries; Zr has neither, despite assessed Cu–Cr–Zr coverage. Prioritize their modeled phase/segregation sensitivity and actual recovery in both ceramics, with microscopy for oxide/intermetallic particles and examination after repeated DED thermal cycles (`tccu7_coverage.md`, `el-10-Nb.md`, `el-13-Ti.md`, `el-14-Zr.md`).
4. **Y, B and Ge:** Y is the only palette element entirely outside TCCU7, B has **zero** assessed Cu ternaries, and Ge has **two** but neither target-family ternary. Compute a Y-free base alloy if useful, but label it as such rather than silently omitting Y from a claimed full-alloy prediction; use paired retained-composition trials at the literature anchors and establish dose response before expanding their bounds (`tccu7_coverage.md`, `el-19-B.md`, `el-37-Ge.md`, `el-43-Y.md`).
5. **Cr/Sn/Si mechanisms versus the actual screen:** distinguish high-flow Cr benefit from stagnant localized corrosion, Sn coating optics from bulk-alloy behavior, and low-Al Si-bronze evidence from high-Al NAB. The proposed stagnant electrochemical/immersion screen cannot by itself establish erosion-corrosion performance, while increased corrosion potential alone cannot establish lower attack (`el-06-Cr.md`, `el-07-Sn.md`, `el-09-Si.md`, `el-12-Co.md`).
6. **Interstitial and impurity limits:** establish assay detection limits, powder-to-deposit pickup/loss, inclusion populations, and porosity/attack correlations before treating the proposed O/H/N/C ceilings as qualified acceptance specifications. Rare-earth gettering can convert O/S into retained particles rather than remove them, and bulk chemistry does not distinguish all harmful oxide-bound from useful dissolved solute (`el-29-O.md`–`el-32-C.md`, `el-43-Y.md`–`el-45-Ce.md`).
7. **Actual repair interfaces and benchmark comparison:** test the same powder on itself and on each requested substrate, with locally resolved chemistry and attack depths rather than only top-surface electrochemistry. None of the supplied bounds proves that one as-deposited powder is crack-free on both substrates and at least as seawater-resistant as wrought C71500; the 30-day result remains a screening comparison, not long-term service qualification (`el-01-Cu.md`–`el-04-Fe.md`).

**Discretionary analytical decisions**

- I use **eight main variables plus five conditional probes** to preserve both alloy families and a limited bridge without making every weakly supported addition an independent co-addition in every alloy.
- I preserve source bounds but select **family-gated working caps**, tightening Ni/Fe for equipment and first-search relevance, allowing higher Mn only in the bridge, and using the Cu–Ni-specific Ti filler range rather than its pooled conservative number.
- I make **one explicit database-preference exception for Y**, prioritize TCCU7’s supplied coverage inventory over speculative claims, and retain B/Ge only as low-dose experiments with clearly identified assessment gaps.
- I treat most impurity numbers as **provisional project controls**, retain hazard review independently of wt%, and carry cost/critical-mineral burden as objectives rather than exclusion rules.
